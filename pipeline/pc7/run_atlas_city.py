"""Run a PC7 global-city NISAR Vision analysis with an independently sourced ref site.

The search is for the requested target bbox. Each downloaded GUNW is clipped to
an expanded bbox that includes the external reference locality. Processing is
performed by the repository cumulative engine in a temporary work root so its
intermediate grids do not overwrite another PC's analysis/out products.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import tempfile
import types
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "analysis"
PROVISIONAL_START = "2026-06-17"
REFERENCE_RADIUS_PX = 3
MIN_REFERENCE_VALID_PIXELS = 48  # a 7x7 median can tolerate one masked cell


def parse_pair(raw: str) -> tuple[float, float]:
    parts = [part.strip() for part in raw.split(",")]
    if len(parts) != 2:
        raise ValueError("Expected lon,lat")
    lon, lat = (float(part) for part in parts)
    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        raise ValueError("Reference/center coordinate outside lon/lat bounds")
    return lon, lat


def core_bbox(center: tuple[float, float], half_width: float = 0.25) -> tuple[float, float, float, float]:
    lon, lat = center
    return (round(lon-half_width, 4), round(lat-half_width, 4),
            round(lon+half_width, 4), round(lat+half_width, 4))


def expanded_bbox(core: tuple[float, float, float, float], ref: tuple[float, float],
                  margin_deg: float = 0.02) -> tuple[float, float, float, float]:
    w, s, e, n = core
    lon, lat = ref
    return (min(w, lon-margin_deg), min(s, lat-margin_deg),
            max(e, lon+margin_deg), max(n, lat+margin_deg))


def _coherence_float(values: np.ndarray) -> np.ndarray:
    data = np.asarray(values)
    return data.astype(np.float32) / (255.0 if np.issubdtype(data.dtype, np.integer) else 1.0)


def choose_reference_window(pair_files: list[Path], anchor: tuple[float, float],
                            search_radius_m: float = 3000.0,
                            minimum_mean_coherence: float = 0.5) -> tuple[int, int, float, np.ndarray, np.ndarray, int]:
    """Pick the most coherent common-valid 7x7 window near a published stable locality."""
    with np.load(pair_files[0], allow_pickle=False) as first:
        x, y, epsg = first["x"].copy(), first["y"].copy(), int(first["epsg"].item())
        shape = first["unw"].shape
    common = np.ones(shape, dtype=bool)
    coh_sum = np.zeros(shape, dtype=np.float64)
    for path in pair_files:
        with np.load(path, allow_pickle=False) as data:
            unw = data["unw"]
            if unw.shape != shape or int(data["epsg"].item()) != epsg:
                raise ValueError(f"inconsistent grid in {path.name}")
            coh = _coherence_float(data["coh"])
            valid = np.isfinite(unw) & np.isfinite(coh) & (coh >= minimum_mean_coherence)
            if "conncomp" in data and data["conncomp"].size:
                valid &= data["conncomp"] != 0
            if "ion" in data and data["ion"].shape == unw.shape:
                valid &= np.isfinite(data["ion"])
            common &= valid
            coh_sum += coh
    mean_coh = coh_sum / len(pair_files)

    transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    ax, ay = transformer.transform(*anchor)
    c0 = int(np.argmin(np.abs(x - ax)))
    r0 = int(np.argmin(np.abs(y - ay)))
    pixel = float(np.median(np.abs(np.diff(x))))
    max_radius = max(1, int(math.ceil(search_radius_m / pixel)))
    rlo, rhi = max(REFERENCE_RADIUS_PX, r0-max_radius), min(shape[0]-REFERENCE_RADIUS_PX, r0+max_radius+1)
    clo, chi = max(REFERENCE_RADIUS_PX, c0-max_radius), min(shape[1]-REFERENCE_RADIUS_PX, c0+max_radius+1)

    best: tuple[float, int, int] | None = None
    radius = REFERENCE_RADIUS_PX
    for row in range(rlo, rhi):
        for col in range(clo, chi):
            valid_win = common[row-radius:row+radius+1, col-radius:col+radius+1]
            if (valid_win.shape != (2*radius+1, 2*radius+1) or
                    int(valid_win.sum()) < MIN_REFERENCE_VALID_PIXELS):
                continue
            score = float(mean_coh[row-radius:row+radius+1, col-radius:col+radius+1].mean())
            if best is None or score > best[0]:
                best = (score, row, col)
    if best is None:
        raise ValueError(f"no common-valid {2*radius+1}x{2*radius+1} high-coherence reference window within {search_radius_m:g} m of source locality {anchor}")
    return best[1], best[2], best[0], x, y, epsg


def _write_quality_metrics(data_dir: Path, cum_npz: Path,
                           bbox: tuple[float, float, float, float],
                           reference_source: str, reference_anchor: tuple[float, float],
                           reference_actual: tuple[float, float], reference_coherence: float,
                           reference_outside_basin: bool) -> dict[str, Any]:
    from pipeline.nisarpulse.process import compute_quality_metrics

    with np.load(cum_npz, allow_pickle=False) as grid:
        cum = np.asarray(grid["cum_cm"], dtype=np.float32)
        x, y, epsg = grid["x"], grid["y"], int(grid["epsg"])
    xx, yy = np.meshgrid(x, y)
    lon, lat = Transformer.from_crs(epsg, 4326, always_xy=True).transform(xx, yy)
    inside = ((lon >= bbox[0]) & (lon <= bbox[2]) &
              (lat >= bbox[1]) & (lat <= bbox[3]))
    core = np.where(inside, cum, np.nan)
    summary_path = data_dir / "summary.json"
    meta_path = data_dir / "meta.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    range_cm = summary.get("range_cm")
    summary.update(compute_quality_metrics(core, float(summary["max_subsidence_cm"]),
                                           summary["period"], range_cm))
    if isinstance(range_cm, list) and len(range_cm) == 2:
        summary["ref_range_cm"] = round(float(range_cm[-1])-float(range_cm[0]), 2)
    else:
        summary["ref_range_cm"] = None
    summary["bbox"] = list(bbox)
    summary["reference_outside_basin"] = bool(reference_outside_basin)
    summary["reference_point"] = {
        "lon": round(reference_actual[0], 6), "lat": round(reference_actual[1], 6),
        "source": reference_source,
    }
    summary["reference_anchor"] = {
        "lon": reference_anchor[0], "lat": reference_anchor[1],
        "mean_coherence": round(reference_coherence, 4),
        "window": "7x7; at least 48/49 common-valid pixels; nearest high-coherence window within 3 km of source locality",
    }
    summary["rate_cm_per_100d"] = round(
        float(summary["max_subsidence_cm"]) * 100 /
        (date.fromisoformat(summary["period"][1])-date.fromisoformat(summary["period"][0])).days, 3)
    summary["quality"] = "provisional"
    summary["quality_note"] = ("NISAR L2 GUNW CRID P05023 provisional products only; "
                               "calibration and validation are carried out by NASA-JPL/ISRO.")
    meta["bbox"] = list(bbox)
    meta["reference_point"] = summary["reference_point"]
    meta["reference_anchor"] = summary["reference_anchor"]
    meta["quality"] = "provisional"
    meta["quality_note"] = summary["quality_note"]
    meta["reference_outside_basin"] = bool(reference_outside_basin)
    summary_path.write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    meta_path.write_text(json.dumps(meta, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    return summary


def process_city(name: str, bbox: tuple[float, float, float, float],
                 reference_anchor: tuple[float, float], reference_source: str,
                 reference_outside_basin: bool,
                 subset_dir: Path | None = None,
                 start: str = PROVISIONAL_START, end: str = "2026-10-31") -> dict[str, Any]:
    from pipeline.nisarpulse.fetch import fetch_subsets
    from pipeline.nisarpulse.search import search_granules

    if start < PROVISIONAL_START:
        raise ValueError("provisional processing cannot start before 2026-06-17")
    subset_bbox = expanded_bbox(bbox, reference_anchor)
    rows, chain, gaps, total_mb = search_granules(bbox, start, end, quality_mode="provisional")
    if not chain:
        return {"coverage": "none", "city": name, "bbox": bbox, "granules": 0,
                "chain_pairs": 0, "error": "No provisional GUNW coverage"}
    if gaps:
        raise ValueError(f"temporal chain has gaps: {gaps}")
    # Callers may direct new cuts to scratch so PC7 does not overwrite PC2's
    # shared pipeline/subset ownership. The cumulative worker copies inputs to
    # its isolated work root below.
    out_subset = subset_dir or (ROOT / "pipeline" / "subset" / f"global_{name}")
    files = fetch_subsets(name, subset_bbox, chain, out_dir=out_subset, resume=True)
    if len(files) != len(chain):
        raise ValueError(f"subset count {len(files)} differs from chain count {len(chain)}")
    for path in files:
        with np.load(path, allow_pickle=False) as data:
            if str(data["quality"].item()) != "provisional":
                raise ValueError(f"non-provisional input: {path.name}")
            if str(data["date1"].item()) < PROVISIONAL_START or str(data["date2"].item()) < PROVISIONAL_START:
                raise ValueError(f"pre-provisional date in {path.name}")

    r, c, mean_coh, x, y, epsg = choose_reference_window(files, reference_anchor)
    lonlat = Transformer.from_crs(epsg, 4326, always_xy=True)
    actual = lonlat.transform(float(x[c]), float(y[r]))

    with tempfile.TemporaryDirectory(prefix=f"pc7_{name}_") as tmp:
        work = Path(tmp)
        work_subset = work / "pipeline" / "subset" / name
        work_subset.mkdir(parents=True)
        for path in files:
            shutil.copy2(path, work_subset / path.name)
        (work / "analysis" / "out").mkdir(parents=True)
        sys.path.insert(0, str(ANALYSIS))
        import cumulative  # type: ignore[import-not-found]
        import gunw_io  # type: ignore[import-not-found]

        old_root = cumulative.ROOT
        old_choose = cumulative.choose_reference
        old_argv = list(sys.argv)
        first_reference = True
        def choose_primary_then_default(coh, valid=None, radius=3, stride=5, exclude=None):
            nonlocal first_reference
            if first_reference:
                first_reference = False
                return r, c, mean_coh
            return old_choose(coh, valid, radius, stride, exclude)
        dummy_dem = types.ModuleType("dem")
        def unavailable_dem(*_args, **_kwargs):
            raise RuntimeError("PC7 city processing uses plane-only deramp; no DEM download")
        dummy_dem.dem_on_grid = unavailable_dem
        old_dem = sys.modules.get("dem")
        try:
            cumulative.ROOT = work
            cumulative.choose_reference = choose_primary_then_default
            gunw_io.BBOX[name] = bbox
            sys.modules["dem"] = dummy_dem
            data_dir = ROOT / "data" / "global" / name
            sys.argv = ["cumulative.py", name, "--data-dir", str(data_dir), "--no-names", "--deramp", "1"]
            cumulative.main()
        finally:
            cumulative.ROOT = old_root
            cumulative.choose_reference = old_choose
            sys.argv = old_argv
            if old_dem is None:
                sys.modules.pop("dem", None)
            else:
                sys.modules["dem"] = old_dem
        summary = _write_quality_metrics(
            data_dir, work / "analysis" / "out" / f"{name}_cum.npz", bbox,
            reference_source, reference_anchor,
            (float(actual[0]), float(actual[1])), mean_coh,
            reference_outside_basin,
        )

    coverage = {
        "site": name, "bbox": list(bbox), "subset_bbox": list(subset_bbox),
        "quality": "provisional", "coverage": "ok", "granules": len(rows),
        "chain_pairs": len(chain), "path": chain[0]["path"], "frame": chain[0]["frame"],
        "period": [chain[0]["date1"], chain[-1]["date2"]], "gaps": [],
        "total_raw_mb": round(total_mb, 1), "raw_files_deleted_after_subsetting": True,
    }
    (data_dir / "coverage.json").write_text(json.dumps(coverage, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    return {"coverage": "ok", "city": name, "summary": summary, "coverage_report": coverage}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--center", required=True, help="Target city center lon,lat")
    parser.add_argument("--reference", required=True, help="Published stable locality lon,lat")
    parser.add_argument("--reference-source", required=True, help="Source text and URL for the reference locality")
    parser.add_argument("--reference-outside-basin", choices=("yes", "no"), required=True)
    parser.add_argument("--subset-dir", type=Path,
                        help="Optional scratch directory for cuts; avoids writing PC2-owned pipeline/subset paths")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    from pipeline.nisarpulse.search import search_granules
    bbox = core_bbox(parse_pair(args.center))
    ref = parse_pair(args.reference)
    if args.dry_run:
        rows, chain, gaps, total = search_granules(bbox, PROVISIONAL_START, "2026-10-31", quality_mode="provisional")
        print(json.dumps({"city": args.name, "bbox": bbox, "granules": len(rows),
                          "chain_pairs": len(chain), "gaps": gaps, "total_raw_mb": round(total, 1)}, indent=2))
        return 0 if chain and not gaps else 2
    result = process_city(args.name, bbox, ref, args.reference_source,
                          args.reference_outside_basin == "yes", subset_dir=args.subset_dir)
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["coverage"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
