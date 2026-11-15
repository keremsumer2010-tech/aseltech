"""Compute GHSL GHS-POP (E2025, 3 arcsec ~100 m) population and area exposure for all atlas regions."""
from __future__ import annotations

import json
import math
import sys
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import requests
import rasterio
from rasterio.windows import from_bounds
from pyproj import Transformer

ROOT = Path(__file__).resolve().parent.parent  # was hard-coded to one team machine (PC1 fix)
sys.path.insert(0, str(ROOT / "analysis"))

from insar import (  # noqa: E402
    cycle_outliers,
    deramp,
    mask_coherence,
    mask_components,
    phase_to_cm,
    reference,
    remove_islands,
)
from cumulative import block_median, BLOCK_PX, BLOCK_MIN_VALID, BLOCK_MAX_STD, ISLAND_MIN_PX, PAIR_OUTLIER_CM  # noqa: E402

ATLAS_PATH = ROOT / "data" / "global" / "atlas.json"
DETECT_PATH = ROOT / "data" / "global" / "detectability.json"
OUT_EXPOSURE = ROOT / "data" / "global" / "exposure_atlas.json"
OUT_VITAL = ROOT / "data" / "global" / "vital_signs.json"
RAW_GHSL = ROOT / "raw" / "ghsl"

GHSL_BASE = (
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/"
    "GHS_POP_GLOBE_R2023A/GHS_POP_E2025_GLOBE_R2023A_4326_3ss/V1-0/tiles/"
)
GHSL_SOURCE = (
    "GHSL GHS-POP E2025 R2023A 3-arcsecond (~100 m, WGS84, European Commission JRC) "
    "intersected with provisional NISAR L2 GUNW cumulative LOS displacement scaled to 108 days, "
    "excluding pixels with |disp| < 2*sigma (data/global/detectability.json)"
)
CALIBRATION_NOTE = (
    "NISAR data are provisional. Calibration and validation are carried out by the "
    "NISAR project (NASA-JPL and ISRO), not by our team."
)


def _find_subset_dir(rid: str) -> Path:
    for cand in (f"global_{rid}", rid):
        p = ROOT / "pipeline" / "subset" / cand
        if p.exists() and list(p.glob("*.npz")):
            return p
    raise FileNotFoundError(f"No subset npz directory found for {rid}")


def _load_chain_npz(sub_dir: Path, dates: list[str]) -> list[Path]:
    from collections import deque

    by_pair: dict[tuple[str, str], Path] = {}
    adj: dict[str, list[str]] = {}
    for f in sorted(sub_dir.glob("*.npz")):
        with np.load(f, allow_pickle=False) as d:
            d1 = str(d["date1"]) if "date1" in d else f.stem.split("_")[0]
            d2 = str(d["date2"]) if "date2" in d else f.stem.split("_")[1]
        by_pair[(d1, d2)] = f
        adj.setdefault(d1, []).append(d2)

    files = []
    for i in range(len(dates) - 1):
        d_start, d_end = dates[i], dates[i + 1]
        if (d_start, d_end) in by_pair:
            files.append(by_pair[(d_start, d_end)])
            continue
        # Bridge dropped QC outlier dates via shortest consecutive .npz chain
        q = deque([(d_start, [])])
        seen = {d_start}
        found = None
        while q:
            cur, path = q.popleft()
            for nxt in sorted(adj.get(cur, [])):
                if nxt > d_end or nxt in seen:
                    continue
                npath = path + [by_pair[(cur, nxt)]]
                if nxt == d_end:
                    found = npath
                    break
                seen.add(nxt)
                q.append((nxt, npath))
            if found is not None:
                break
        if found is None:
            raise FileNotFoundError(f"Missing pair {(d_start, d_end)} in {sub_dir}")
        files.extend(found)
    return files


def _cramer_rao_2sigma(pair_files: list[Path], valid_all: np.ndarray, in_bbox: np.ndarray) -> float:
    looks = 208.0
    sigma2_sum = np.zeros(valid_all.shape, dtype=np.float64)
    for f in pair_files:
        with np.load(f, allow_pickle=False) as d:
            lam = float(d["wavelength"])
            coh_raw = d["coh"]
            coh = coh_raw.astype(np.float64) / (255.0 if np.issubdtype(coh_raw.dtype, np.integer) else 1.0)
            coh = np.clip(coh, 0.05, 0.9999)
            sigma_phi = np.sqrt(1.0 - coh**2) / (coh * math.sqrt(2.0 * looks))
            sigma_d = (lam / (4.0 * math.pi)) * sigma_phi * 100.0
            sigma2_sum += sigma_d**2
    sigma_total = np.sqrt(sigma2_sum)
    mask = valid_all & in_bbox
    med = float(np.nanmedian(sigma_total[mask])) if mask.any() else 0.35
    return round(2.0 * med, 3)


def load_or_reconstruct(region: dict[str, Any]) -> dict[str, Any]:
    rid = region["id"]
    data_dir = ROOT / region["path"]
    meta = json.loads((data_dir / "meta.json").read_text(encoding="utf-8"))
    dates = meta["dates"]
    bbox = meta["bbox"]
    days = max(1, (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days)

    cum_npz = ROOT / "analysis" / "out" / f"{rid}_cum.npz"
    if cum_npz.exists():
        with np.load(cum_npz, allow_pickle=False) as d:
            cum = np.asarray(d["cum_cm"] if "cum_cm" in d else d["cum"], dtype=np.float32)
            x = np.asarray(d["x"], dtype=np.float64)
            y = np.asarray(d["y"], dtype=np.float64)
            epsg = int(d["epsg"].item() if hasattr(d["epsg"], "item") else d["epsg"])
        sub_dir = _find_subset_dir(rid)
        pair_files = _load_chain_npz(sub_dir, dates)
    else:
        ref_pt = meta["reference_point"]
        sub_dir = _find_subset_dir(rid)
        pair_files = _load_chain_npz(sub_dir, dates)
        with np.load(pair_files[0], allow_pickle=False) as d0:
            x = d0["x"].copy()
            y = d0["y"].copy()
            epsg = int(d0["epsg"].item())
        tr = Transformer.from_crs(4326, epsg, always_xy=True)
        rx, ry = tr.transform(float(ref_pt["lon"]), float(ref_pt["lat"]))
        c_ref = int(np.argmin(np.abs(x - rx)))
        r_ref = int(np.argmin(np.abs(y - ry)))

        pair_cm = []
        for f in pair_files:
            with np.load(f, allow_pickle=False) as d:
                unw = d["unw"].astype(np.float32)
                if "ion" in d and d["ion"].shape == unw.shape:
                    unw = unw - d["ion"].astype(np.float32)
                lam = float(d["wavelength"])
                cm = phase_to_cm(unw, lam)
                if "conncomp" in d and d["conncomp"].size:
                    cm = mask_components(cm, d["conncomp"])
                cm = mask_coherence(cm, d["coh"], 0.3)
                cm = remove_islands(cm, ISLAND_MIN_PX)
                cm = deramp(cm, order=1)
                cm = cycle_outliers(cm, thr_cm=lam / 4.0 * 100.0)
                pair_cm.append(cm)

        valid_all = np.logical_and.reduce([np.isfinite(c) for c in pair_cm])
        cum = np.zeros_like(pair_cm[0], dtype=np.float32)
        for cm in pair_cm:
            cm_r = reference(cm, (r_ref, c_ref), radius=3)
            cm_r[np.abs(cm_r) > PAIR_OUTLIER_CM] = np.nan
            cum = cum + cm_r
        cum[~valid_all] = np.nan

    xx, yy = np.meshgrid(x, y)
    lon, lat = Transformer.from_crs(epsg, 4326, always_xy=True).transform(xx, yy)
    in_bbox = (lon >= bbox[0]) & (lon <= bbox[2]) & (lat >= bbox[1]) & (lat <= bbox[3])
    cr_2sig = _cramer_rao_2sigma(pair_files, np.isfinite(cum), in_bbox)

    return {
        "id": rid,
        "cum": cum,
        "x": x,
        "y": y,
        "epsg": epsg,
        "bbox": bbox,
        "in_bbox": in_bbox,
        "days": days,
        "cramer_rao_2sigma_cm": cr_2sig,
    }


def _ghsl_tiles_for_bbox(bbox: list[float]) -> list[tuple[int, int]]:
    lon_min, lat_min, lon_max, lat_max = bbox
    # GHSL 4326_3ss grid starts at top=89.0995834, left=-180.007917, 10 deg per tile
    r_top = int(math.floor((89.1 - lat_max) / 10.0)) + 1
    r_bot = int(math.floor((89.1 - lat_min) / 10.0)) + 1
    c_left = int(math.floor((lon_min + 180.008) / 10.0)) + 1
    c_right = int(math.floor((lon_max + 180.008) / 10.0)) + 1
    tiles = []
    for r in range(max(1, r_top), min(18, r_bot) + 1):
        for c in range(max(1, c_left), min(36, c_right) + 1):
            tiles.append((r, c))
    return tiles


def _ensure_ghsl_tif(r: int, c: int) -> Path:
    RAW_GHSL.mkdir(parents=True, exist_ok=True)
    stem = f"GHS_POP_E2025_GLOBE_R2023A_4326_3ss_V1_0_R{r}_C{c}"
    tif_path = RAW_GHSL / f"{stem}.tif"
    if tif_path.exists():
        return tif_path
    zip_path = RAW_GHSL / f"{stem}.zip"
    tmp_path = RAW_GHSL / f"{stem}.zip.tmp"
    if zip_path.exists():
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extract(f"{stem}.tif", RAW_GHSL)
            return tif_path
        except Exception:
            zip_path.unlink(missing_ok=True)
    url = f"{GHSL_BASE}{stem}.zip"
    for attempt in range(1, 4):
        try:
            print(f"  Downloading GHSL tile {stem}.zip (attempt {attempt}) ...")
            resp = requests.get(url, stream=True, timeout=180)
            resp.raise_for_status()
            with tmp_path.open("wb") as f:
                for chunk in resp.iter_content(chunk_size=1 << 20):
                    if chunk:
                        f.write(chunk)
            tmp_path.replace(zip_path)
            break
        except Exception as exc:
            tmp_path.unlink(missing_ok=True)
            if attempt == 3:
                raise exc
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extract(f"{stem}.tif", RAW_GHSL)
    return tif_path


def compute_ghsl_exposure(
    grid: dict[str, Any],
    two_sigma_cm: float,
) -> dict[str, Any]:
    cum = grid["cum"]
    x = grid["x"]
    y = grid["y"]
    epsg = grid["epsg"]
    bbox = grid["bbox"]
    in_bbox = grid["in_bbox"]
    days = grid["days"]

    # Normalize displacement to 108 days, while gating on actual measured |cum| >= 2*sigma
    scale_108 = 108.0 / float(days)
    cum_108 = cum * scale_108
    detectable = np.isfinite(cum) & (np.abs(cum) >= two_sigma_cm)

    px_area_km2 = abs(float(x[1] - x[0])) * abs(float(y[1] - y[0])) / 1e6
    mask_lt2 = in_bbox & detectable & (cum_108 < -2.0)
    mask_lt5 = in_bbox & detectable & (cum_108 < -5.0)
    area_lt2_km2 = float(mask_lt2.sum()) * px_area_km2
    area_lt5_km2 = float(mask_lt5.sum()) * px_area_km2

    # Intersect with GHSL GHS-POP tiles in bbox
    tiles = _ghsl_tiles_for_bbox(bbox)
    tr_ll_to_utm = Transformer.from_crs(4326, epsg, always_xy=True)
    x0, dx = float(x[0]), float(x[1] - x[0])
    y0, dy = float(y[0]), float(y[1] - y[0])
    H, W = cum.shape

    pop_total = 0.0
    pop_lt2 = 0.0
    pop_lt5 = 0.0

    lon_min, lat_min, lon_max, lat_max = bbox
    for r_tile, c_tile in tiles:
        tif = _ensure_ghsl_tif(r_tile, c_tile)
        with rasterio.open(tif) as src:
            b = src.bounds
            w_lon = max(lon_min, b.left)
            e_lon = min(lon_max, b.right)
            s_lat = max(lat_min, b.bottom)
            n_lat = min(lat_max, b.top)
            if w_lon >= e_lon or s_lat >= n_lat:
                continue
            win = from_bounds(w_lon, s_lat, e_lon, n_lat, src.transform)
            arr = src.read(1, window=win).astype(np.float64)
            if src.nodata is not None:
                arr = np.where(arr == src.nodata, 0.0, arr)
            arr = np.where(np.isfinite(arr) & (arr > 0), arr, 0.0)
            pop_total += float(arr.sum())

            w_tfm = src.window_transform(win)
            rows, cols = np.indices(arr.shape)
            lons, lats = rasterio.transform.xy(w_tfm, rows.ravel(), cols.ravel())
            ux, uy = tr_ll_to_utm.transform(np.asarray(lons), np.asarray(lats))
            ic = np.rint((ux - x0) / dx).astype(np.int64)
            ir = np.rint((uy - y0) / dy).astype(np.int64)
            inside = (ir >= 0) & (ir < H) & (ic >= 0) & (ic < W)

            pop_flat = arr.ravel()
            ir_in = ir[inside]
            ic_in = ic[inside]
            p_in = pop_flat[inside]
            pop_lt2 += float(p_in[mask_lt2[ir_in, ic_in]].sum())
            pop_lt5 += float(p_in[mask_lt5[ir_in, ic_in]].sum())

    # Top 3 spatially separated (>= 5 km) 1 km block-median subsiding areas
    sm = block_median(np.where(in_bbox & detectable, cum, np.nan), BLOCK_PX, BLOCK_MIN_VALID, BLOCK_MAX_STD)
    top3 = []
    sm_work = sm.copy()
    tr_utm_to_ll = Transformer.from_crs(epsg, 4326, always_xy=True)
    for _ in range(3):
        if not np.isfinite(sm_work).any():
            break
        rmin, cmin = np.unravel_index(np.nanargmin(sm_work), sm_work.shape)
        val = float(sm_work[rmin, cmin])
        if val >= -two_sigma_cm:
            break
        lon_m, lat_m = tr_utm_to_ll.transform(float(x[cmin]), float(y[rmin]))
        top3.append({
            "lon": round(float(lon_m), 4),
            "lat": round(float(lat_m), 4),
            "cum_cm_los": round(val, 2),
            "rate_cm_per_100d": round(val * 100.0 / float(days), 2),
        })
        dist = np.hypot((np.arange(H)[:, None] - rmin) * abs(dy), (np.arange(W)[None, :] - cmin) * abs(dx))
        sm_work[dist < 5000.0] = np.nan

    return {
        "people_lt_minus2cm": int(round(pop_lt2)),
        "people_lt_minus5cm": int(round(pop_lt5)),
        "area_km2_lt_minus5cm": round(area_lt5_km2, 2),
        "area_km2_lt_minus2cm": round(area_lt2_km2, 2),
        "bbox_population_ghsl": int(round(pop_total)),
        "two_sigma_cm": two_sigma_cm,
        "days": days,
        "top_subsiding_areas": top3,
    }


def main() -> None:
    atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    det = json.loads(DETECT_PATH.read_text(encoding="utf-8"))
    det_map = {c["id"]: c for c in det.get("cities", [])}

    records = []
    for region in atlas["regions"]:
        rid = region["id"]
        print(f"Processing {rid} ...")
        grid = load_or_reconstruct(region)
        d_entry = det_map.get(rid, {})
        two_sig = d_entry.get("min_detectable_disp_2sigma_cm")
        two_sig_src = "data/global/detectability.json"
        if two_sig is None:
            two_sig = grid["cramer_rao_2sigma_cm"]
            two_sig_src = "Cramer-Rao 2*sigma computed from pipeline/subset"

        res = compute_ghsl_exposure(grid, float(two_sig))
        rec = {
            "id": rid,
            "name": region["name"],
            "country": region.get("country", ""),
            "people_lt_minus2cm": res["people_lt_minus2cm"],
            "people_lt_minus5cm": res["people_lt_minus5cm"],
            "area_km2_lt_minus5cm": res["area_km2_lt_minus5cm"],
            "area_km2_lt_minus2cm": res["area_km2_lt_minus2cm"],
            "bbox_population_ghsl": res["bbox_population_ghsl"],
            "two_sigma_threshold_cm": res["two_sigma_cm"],
            "two_sigma_source": two_sig_src,
            "days_measured": res["days"],
            "normalized_window_days": 108,
            "top_subsiding_areas": res["top_subsiding_areas"],
            "source": GHSL_SOURCE,
            "quality": "provisional",
        }
        records.append(rec)
        print(
            f"  {rid:15s} pop<-2cm={rec['people_lt_minus2cm']:7,d} "
            f"pop<-5cm={rec['people_lt_minus5cm']:7,d} "
            f"area<-5cm={rec['area_km2_lt_minus5cm']:6.2f} km2 "
            f"(2sig={rec['two_sigma_threshold_cm']:.3f} cm)"
        )

    # Note: karapinar is a spatial subset inside konya_plain; avoid double-counting in global totals.
    # Headline totals count only reliable basins (indicative-only basins stay per-city but are not summed).
    indicative_ids = {r["id"] for r in atlas["regions"] if r.get("indicative_only")}
    non_subset = [r for r in records if r["id"] != "karapinar"]
    reliable_recs = [r for r in non_subset if r["id"] not in indicative_ids]
    total_area_lt5 = round(sum(r["area_km2_lt_minus5cm"] for r in reliable_recs), 2)
    total_pop_lt5 = sum(r["people_lt_minus5cm"] for r in reliable_recs)
    total_pop_lt2 = sum(r["people_lt_minus2cm"] for r in reliable_recs)
    all_area_lt5 = round(sum(r["area_km2_lt_minus5cm"] for r in non_subset), 2)
    all_pop_lt5 = sum(r["people_lt_minus5cm"] for r in non_subset)
    all_pop_lt2 = sum(r["people_lt_minus2cm"] for r in non_subset)

    exposure_doc = {
        "title": "Global Atlas Population and Area Exposure on Sinking Ground (108-day equivalent)",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": GHSL_SOURCE,
        "quality": "provisional",
        "quality_note": CALIBRATION_NOTE,
        "notes": (
            "karapinar is reported separately as a local subset inside konya_plain and is never summed. "
            "totals_excluding_nested_karapinar sums reliable basins only (indicative-only basins in atlas.json are listed per city "
            "but excluded from the headline); totals_all_regions_excluding_nested_karapinar adds the indicative-only basins."
        ),
        "totals_excluding_nested_karapinar": {
            "people_lt_minus2cm": total_pop_lt2,
            "people_lt_minus5cm": total_pop_lt5,
            "area_km2_lt_minus5cm": total_area_lt5,
            "scope": "reliable basins only",
            "n_basins": len(reliable_recs),
        },
        "totals_all_regions_excluding_nested_karapinar": {
            "people_lt_minus2cm": all_pop_lt2,
            "people_lt_minus5cm": all_pop_lt5,
            "area_km2_lt_minus5cm": all_area_lt5,
            "scope": "reliable and indicative-only basins",
            "n_basins": len(non_subset),
        },
        "cities": records,
    }
    OUT_EXPOSURE.write_text(json.dumps(exposure_doc, indent=2) + "\n", encoding="utf-8")

    # Item 2: data/global/vital_signs.json (fastest among reliable, non-QC-flagged regions)
    qc_path = ROOT / "data" / "global" / "qc_flags.json"
    qc_flagged: set[str] = set()
    if qc_path.exists():
        qc_data = json.loads(qc_path.read_text(encoding="utf-8"))
        qc_flagged = set((qc_data.get("flags") or {}).keys())
    regions = atlas["regions"]
    reliable = [r for r in regions if not r.get("indicative_only") and r["id"] not in qc_flagged]
    pool = reliable if reliable else regions
    def _rate_key(r: dict) -> float:
        return float(
            r.get("rate_cm_per_100d_common")
            if r.get("rate_cm_per_100d_common") is not None
            else r.get("rate_cm_per_100d", 999.0)
        )

    fastest_r = min(pool, key=_rate_key)
    fastest_rate = _rate_key(fastest_r)
    vital_doc = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "quality": "provisional",
        "quality_note": CALIBRATION_NOTE,
        "cities_measured": len(regions),
        "cities_measured_source": "data/global/atlas.json (n_regions)",
        "fastest": {
            "id": fastest_r["id"],
            "name": fastest_r["name"],
            "country": fastest_r.get("country", ""),
            "rate_cm_per_100d": fastest_rate,
            "source": "data/global/atlas.json (fastest among reliable regions; QC-flagged regions excluded, tools/atlas_qc.py)",
        },
        "area_km2_lt_minus5cm": total_area_lt5,
        "area_km2_lt_minus5cm_source": "data/global/exposure_atlas.json (sum excluding nested karapinar)",
        "people_on_sinking_ground": total_pop_lt5,
        "people_on_sinking_ground_threshold": "< -5 cm (108-day equivalent, |disp| >= 2*sigma)",
        "people_on_sinking_ground_gt2cm": total_pop_lt2,
        "people_on_sinking_ground_source": "data/global/exposure_atlas.json (GHSL GHS-POP E2025 R2023A 3ss, excluding nested karapinar)",
    }
    OUT_VITAL.write_text(json.dumps(vital_doc, indent=2) + "\n", encoding="utf-8")
    print("Wrote", OUT_EXPOSURE, "and", OUT_VITAL)


if __name__ == "__main__":
    main()
