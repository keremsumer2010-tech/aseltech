"""Generate compact 3D terrain surface JSON for the Q16 web3d/ Breathing Earth viewer.

Reads existing NISAR GUNW provisional subsets (`pipeline/subset/central_valley/*.npz`
and `analysis/out/karapinar_20260918_20260930.npz`), reuses `analysis/` physics
functions without duplicating formulas, and writes `web3d/surfaces.json` (< 500 KB).
Never modifies `data/central_valley/` or `analysis/`.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path

import numpy as np
from scipy.ndimage import median_filter

try:
    from pyproj import Transformer
except ImportError:
    import types

    class Transformer:  # type: ignore[no-redef]
        """Pure-NumPy WGS84 UTM <-> EPSG:4326 fallback when pyproj is unavailable."""

        _A = 6378137.0
        _F = 1.0 / 298.257223563
        _E2 = _F * (2.0 - _F)
        _EP2 = _E2 / (1.0 - _E2)
        _K0 = 0.9996

        def __init__(self, zone: int, north: bool, inverse: bool) -> None:
            self.zone, self.north, self.inverse = zone, north, inverse
            self.lon0 = np.deg2rad((zone - 1) * 6 - 180 + 3)

        @classmethod
        def from_crs(cls, src: int, dst: int, always_xy: bool = True) -> "Transformer":
            epsg = dst if src == 4326 else src
            if not (32601 <= epsg <= 32660 or 32701 <= epsg <= 32760):
                raise ValueError(f"Fallback supports WGS84 UTM EPSG only, got {src}->{dst}")
            north = epsg < 32700
            zone = epsg % 100
            return cls(zone, north, inverse=(dst == 4326))

        def transform(self, x_in, y_in):
            a, e2, ep2, k0 = self._A, self._E2, self._EP2, self._K0
            arr1 = np.asarray(x_in, dtype=np.float64)
            arr2 = np.asarray(y_in, dtype=np.float64)
            c1 = 1.0 - e2 / 4.0 - 3.0 * e2**2 / 64.0 - 5.0 * e2**3 / 256.0
            c2 = 3.0 * e2 / 8.0 + 3.0 * e2**2 / 32.0 + 45.0 * e2**3 / 1024.0
            c3 = 15.0 * e2**2 / 256.0 + 45.0 * e2**3 / 1024.0
            c4 = 35.0 * e2**3 / 3072.0
            if not self.inverse:
                lon = np.deg2rad(arr1)
                lat = np.deg2rad(arr2)
                n_r = a / np.sqrt(1.0 - e2 * np.sin(lat) ** 2)
                t = np.tan(lat) ** 2
                c = ep2 * np.cos(lat) ** 2
                dl = np.cos(lat) * (lon - self.lon0)
                m = a * (c1 * lat - c2 * np.sin(2 * lat) + c3 * np.sin(4 * lat) - c4 * np.sin(6 * lat))
                east = k0 * n_r * (dl + (1 - t + c) * dl**3 / 6 + (5 - 18 * t + t**2 + 72 * c - 58 * ep2) * dl**5 / 120) + 500000.0
                north = k0 * (m + n_r * np.tan(lat) * (dl**2 / 2 + (5 - t + 9 * c + 4 * c**2) * dl**4 / 24 + (61 - 58 * t + t**2 + 600 * c - 330 * ep2) * dl**6 / 720))
                if not self.north:
                    north = north + 10000000.0
                return east, north
            east = arr1 - 500000.0
            north = arr2 if self.north else (arr2 - 10000000.0)
            m = north / k0
            mu = m / (a * c1)
            e1 = (1.0 - np.sqrt(1.0 - e2)) / (1.0 + np.sqrt(1.0 - e2))
            phi1 = (mu + (3 * e1 / 2 - 27 * e1**3 / 32) * np.sin(2 * mu)
                    + (21 * e1**2 / 16 - 55 * e1**4 / 32) * np.sin(4 * mu)
                    + (151 * e1**3 / 96) * np.sin(6 * mu))
            s1, c_p, t_p = np.sin(phi1), np.cos(phi1), np.tan(phi1)
            n1 = a / np.sqrt(1.0 - e2 * s1**2)
            r1 = a * (1.0 - e2) / (1.0 - e2 * s1**2) ** 1.5
            c_v = ep2 * c_p**2
            t_v = t_p**2
            d = east / (n1 * k0)
            lat = phi1 - (n1 * t_p / r1) * (d**2 / 2 - (5 + 3 * t_v + 10 * c_v - 4 * c_v**2 - 9 * ep2) * d**4 / 24 + (61 + 90 * t_v + 298 * c_v + 45 * t_v**2 - 252 * ep2 - 3 * c_v**2) * d**6 / 720)
            lon = self.lon0 + (d - (1 + 2 * t_v + c_v) * d**3 / 6 + (5 - 2 * c_v + 28 * t_v - 3 * c_v**2 + 8 * ep2 + 24 * t_v**2) * d**5 / 120) / c_p
            return np.rad2deg(lon), np.rad2deg(lat)

    shim = types.ModuleType("pyproj")
    shim.Transformer = Transformer
    sys.modules["pyproj"] = shim

try:
    import h5py  # noqa: F401
except ImportError:
    import types as _types
    sys.modules["h5py"] = _types.ModuleType("h5py")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))

from cumulative import (  # noqa: E402
    DISCLAIMER,
    ISLAND_MIN_PX,
    PAIR_OUTLIER_CM,
    chain,
    load_places,
    place_label,
    to_latlon_grid,
)
from gunw_io import BBOX  # noqa: E402
from insar import (  # noqa: E402
    choose_reference,
    cycle_outliers,
    deramp,
    mask_coherence,
    mask_components,
    phase_to_cm,
    remove_islands,
    reference,
)


def process_pair(d: np.lib.npyio.NpzFile, thr: float = 0.3, deramp_order: int = 1) -> tuple[np.ndarray, bool]:
    """Convert one provisional GUNW npz subset to referenced-ready LOS displacement (cm)."""
    unw = d["unw"].astype(np.float32)
    ion_used = "ion" in d and d["ion"].shape == unw.shape
    if ion_used:
        unw = unw - d["ion"]
    cm = phase_to_cm(unw, float(d["wavelength"]))
    if "conncomp" in d and d["conncomp"].size:
        cm = mask_components(cm, d["conncomp"])
    cm = mask_coherence(cm, d["coh"], thr)
    cm = remove_islands(cm, ISLAND_MIN_PX)
    if deramp_order:
        cm = deramp(cm, order=deramp_order)
    cm = cycle_outliers(cm, thr_cm=float(d["wavelength"]) / 4.0 * 100.0)
    return cm, bool(ion_used)


def grid_to_flat_list(grid: np.ndarray) -> list[float | None]:
    """Flatten north-up float grid into JSON-safe list rounded to 2 decimals (no NaN)."""
    out: list[float | None] = []
    for v in grid.ravel():
        vf = float(v)
        out.append(round(vf, 2) if math.isfinite(vf) else None)
    return out


def build_region_payload(
    site: str,
    title: str,
    subtitle: str,
    npz_files: list[Path],
    bbox: tuple[float, float, float, float],
    step_deg: float,
    extra_notes: str = "",
) -> dict:
    """Process one or more consecutive provisional GUNW pairs into a 3D surface payload."""
    used, notes = chain(npz_files)
    d0 = used[0][3]
    x, y, epsg = d0["x"], d0["y"], int(d0["epsg"])
    dates = [used[0][0]] + [p[1] for p in used]

    pair_cm = []
    ion_flags = []
    for _, _, f, d in used:
        if d["unw"].shape != d0["unw"].shape or not np.allclose(d["x"], x) or not np.allclose(d["y"], y):
            raise RuntimeError(f"Grid mismatch in {f.name}")
        cm, ion_ok = process_pair(d)
        pair_cm.append(cm)
        ion_flags.append(ion_ok)

    valid_all = np.logical_and.reduce([np.isfinite(c) for c in pair_cm])
    coh_mean = np.mean([np.load(f, allow_pickle=False)["coh"].astype(np.float32) / 255.0 for _, _, f, _ in used], axis=0)
    r_ref, c_ref, mcoh = choose_reference(coh_mean, valid_all, radius=3, stride=3)
    tr_to_ll = Transformer.from_crs(epsg, 4326, always_xy=True)
    lon_r, lat_r = tr_to_ll.transform(x[c_ref], y[r_ref])

    cum = [np.zeros_like(pair_cm[0])]
    cum[0][~valid_all] = np.nan
    for cm in pair_cm:
        cm_ref = reference(cm, (r_ref, c_ref), radius=3)
        cm_ref[np.abs(cm_ref) > PAIR_OUTLIER_CM] = np.nan
        cum.append(cum[-1] + cm_ref)
    for k in range(len(cum)):
        cum[k][~valid_all] = np.nan

    final = cum[-1]
    valid = np.isfinite(final)
    sm = median_filter(np.where(valid, final, np.nan), size=5, mode="nearest")
    sm = np.where(valid & np.isfinite(sm), sm, np.nan)
    rmin, cmin = np.unravel_index(np.nanargmin(sm), sm.shape)
    max_sub = float(sm[rmin, cmin])
    lon_m, lat_m = tr_to_ll.transform(x[cmin], y[rmin])
    days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
    vlim = float(np.ceil(np.nanpercentile(np.abs(sm), 99.5)))
    vmin, vmax = -vlim, vlim
    p2, p50, p98 = [round(float(v), 2) for v in np.nanpercentile(final[valid], [2, 50, 98])]

    # Downsampled regular lon/lat grids for interactive 3D mesh
    w, s, e, n = bbox
    lons = np.arange(w + step_deg / 2.0, e, step_deg)
    lats = np.arange(n - step_deg / 2.0, s, -step_deg)
    nrows, ncols = len(lats), len(lons)

    # Light spatial median pass at coarse step so sparse single invalid pixels don't punch holes
    grids = []
    for k, g in enumerate(cum):
        g_smooth = median_filter(np.where(np.isfinite(g), g, np.nan), size=5, mode="nearest") if k > 0 else g
        g_smooth = np.where(valid, g_smooth, np.nan)
        ll = to_latlon_grid(g_smooth, x, y, epsg, bbox, step=step_deg)
        assert ll.shape == (nrows, ncols), (ll.shape, (nrows, ncols))
        grids.append(grid_to_flat_list(ll))

    places = load_places(site)
    inc = d0["incidence"] if "incidence" in d0 and d0["incidence"].size else None
    inc_at = round(float(inc[rmin, cmin]), 1) if inc is not None and math.isfinite(float(inc[rmin, cmin])) else None
    vert_est = round(max_sub / math.cos(math.radians(inc_at)), 1) if inc_at is not None else None

    hemi_lat = "N" if lat_m >= 0 else "S"
    hemi_lon = "E" if lon_m >= 0 else "W"
    fallback_lbl = f"{abs(lat_m):.3f}{hemi_lat}, {abs(lon_m):.3f}{hemi_lon}"

    granules = [str(p[3]["granule"]) for p in used if "granule" in p[3]]
    return {
        "site": site,
        "title": title,
        "subtitle": subtitle,
        "bbox": list(bbox),
        "rows": nrows,
        "cols": ncols,
        "step_deg": step_deg,
        "dates": dates,
        "days": days,
        "n_pairs": len(used),
        "units": "cm",
        "component": "LOS (negative = away from radar = subsidence)",
        "vmin": vmin,
        "vmax": vmax,
        "p2_cm": p2,
        "median_cm": p50,
        "p98_cm": p98,
        "max_subsidence_cm": round(max_sub, 1),
        "max_subsidence_vertical_cm_estimate": vert_est,
        "incidence_deg_at_max": inc_at,
        "rate_cm_per_yr_estimate": round(max_sub / days * 365.25, 1) if (len(used) >= 2 and days >= 28) else None,
        "max_subsidence_location": {
            "lon": round(float(lon_m), 5),
            "lat": round(float(lat_m), 5),
            "label": place_label(lon_m, lat_m, places) if places else fallback_lbl,
        },
        "reference_point": {
            "lon": round(float(lon_r), 5),
            "lat": round(float(lat_r), 5),
            "mean_coh": round(float(mcoh), 2),
        },
        "valid_frac": round(float(valid.mean()), 3),
        "ionosphere_applied": all(ion_flags),
        "quality": "provisional",
        "quality_note": DISCLAIMER,
        "granules": granules,
        "notes": (
            f"Gap-free chain of {len(used)} NISAR L2 GUNW Provisional pair(s) ({dates[0]} to {dates[-1]}). "
            + ("Product ionosphere screen subtracted; plane deramp + cycle-outlier guard applied. " if all(ion_flags) else "")
            + " ".join(notes)
            + (" " + extra_notes if extra_notes else "")
        ).strip(),
        "grids": grids,
    }


def build_precomputed_stack_payload(
    site: str,
    title: str,
    subtitle: str,
    bbox: tuple[float, float, float, float],
    step_deg: float,
) -> dict | None:
    """Build 3D payload directly from PC3's official cumulative stack & summary JSON."""
    stack_path = ROOT / "analysis" / "out" / f"{site}_cum_stack.npz"
    cum_path = ROOT / "analysis" / "out" / f"{site}_cum.npz"
    summary_path = ROOT / "data" / site / "summary.json"
    meta_path = ROOT / "data" / site / "meta.json"
    points_path = ROOT / "data" / site / "points.json"
    if not (stack_path.exists() and summary_path.exists() and meta_path.exists()):
        return None

    stack_npz = np.load(stack_path, allow_pickle=False)
    cum_stack = stack_npz["cum_stack_cm"].astype(np.float32)
    x, y, epsg = stack_npz["x"], stack_npz["y"], int(stack_npz["epsg"])
    dates = [str(d) for d in stack_npz["dates"]]

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    ref_rc = None
    if cum_path.exists():
        cum_npz = np.load(cum_path, allow_pickle=False)
        if "reference_rc" in cum_npz:
            ref_rc = [int(v) for v in cum_npz["reference_rc"]]

    mean_coh = None
    if ref_rc is not None:
        r0, c0 = ref_rc
        subset_files = sorted((ROOT / "pipeline" / "subset" / site).glob("*.npz"))
        if not subset_files and site == "karapinar":
            kp_single = ROOT / "analysis" / "out" / "karapinar_20260918_20260930.npz"
            if kp_single.exists():
                subset_files = [kp_single]
        if subset_files:
            cohs = [
                float(np.load(f, allow_pickle=False)["coh"][max(0, r0 - 3): r0 + 4, max(0, c0 - 3): c0 + 4].mean()) / 255.0
                for f in subset_files
            ]
            mean_coh = round(float(np.mean(cohs)), 2)

    final = cum_stack[-1]
    valid = np.isfinite(final)
    p2, p50, p98 = [round(float(v), 2) for v in np.nanpercentile(final[valid], [2, 50, 98])]

    w, s, e, n = bbox
    lons = np.arange(w + step_deg / 2.0, e, step_deg)
    lats = np.arange(n - step_deg / 2.0, s, -step_deg)
    nrows, ncols = len(lats), len(lons)

    grids = []
    for k in range(cum_stack.shape[0]):
        g = cum_stack[k]
        g_smooth = median_filter(np.where(np.isfinite(g), g, np.nan), size=5, mode="nearest") if k > 0 else g
        g_smooth = np.where(valid, g_smooth, np.nan)
        ll = to_latlon_grid(g_smooth, x, y, epsg, bbox, step=step_deg)
        assert ll.shape == (nrows, ncols), (ll.shape, (nrows, ncols))
        grids.append(grid_to_flat_list(ll))

    max_loc = dict(summary["max_subsidence_location"])
    label = None
    if points_path.exists():
        pts = json.loads(points_path.read_text(encoding="utf-8"))
        for pt in pts:
            if abs(pt["lon"] - max_loc["lon"]) < 1e-4 and abs(pt["lat"] - max_loc["lat"]) < 1e-4:
                label = pt["name"]
                break
    if not label:
        places = load_places(site)
        hemi_lat = "N" if max_loc["lat"] >= 0 else "S"
        hemi_lon = "E" if max_loc["lon"] >= 0 else "W"
        label = place_label(max_loc["lon"], max_loc["lat"], places) if places else f"{abs(max_loc['lat']):.3f}{hemi_lat}, {abs(max_loc['lon']):.3f}{hemi_lon}"
    max_loc["label"] = label

    ref_pt = dict(summary["reference_point"])
    ref_pt["mean_coh"] = mean_coh

    days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
    return {
        "site": site,
        "title": title,
        "subtitle": subtitle,
        "bbox": list(bbox),
        "rows": nrows,
        "cols": ncols,
        "step_deg": step_deg,
        "dates": dates,
        "days": days,
        "n_pairs": int(summary["n_pairs"]),
        "units": meta.get("units", "cm"),
        "component": meta.get("component", "LOS (negative = away from radar = subsidence)"),
        "vmin": float(meta.get("vmin", -6.0)),
        "vmax": float(meta.get("vmax", 6.0)),
        "p2_cm": p2,
        "median_cm": p50,
        "p98_cm": p98,
        "max_subsidence_cm": summary["max_subsidence_cm"],
        "max_subsidence_vertical_cm_estimate": summary.get("max_subsidence_vertical_cm_estimate"),
        "incidence_deg_at_max": summary.get("incidence_deg_at_max"),
        "rate_cm_per_yr_estimate": summary.get("rate_cm_per_yr_estimate"),
        "max_subsidence_location": max_loc,
        "reference_point": ref_pt,
        "valid_frac": round(float(valid.mean()), 3),
        "ionosphere_applied": True,
        "quality": summary.get("quality", "provisional"),
        "quality_note": summary.get("quality_note", DISCLAIMER),
        "granules": meta.get("granules", []),
        "notes": meta.get("notes", ""),
        "grids": grids,
    }


def main() -> None:
    cv_payload = build_precomputed_stack_payload(
        site="central_valley",
        title="San Joaquin Valley (California)",
        subtitle="7 provisional NISAR GUNW pairs (2026-06-28 → 2026-10-14, DEM + iono deramped)",
        bbox=BBOX["central_valley"],
        step_deg=0.0125,
    )
    if cv_payload is None:
        cv_files = sorted((ROOT / "pipeline" / "subset" / "central_valley").glob("*.npz"))
        cv_payload = build_region_payload(
            site="central_valley",
            title="San Joaquin Valley (California)",
            subtitle="Multi-epoch summer irrigation compaction (NISAR GUNW pairs)",
            npz_files=cv_files,
            bbox=BBOX["central_valley"],
            step_deg=0.0125,
        )

    kp_payload = build_precomputed_stack_payload(
        site="karapinar",
        title="Karapınar Basin (Konya, Türkiye)",
        subtitle="8 provisional NISAR GUNW pairs (2026-06-26 → 2026-10-12) + 29 verified obruk sinkholes",
        bbox=BBOX["karapinar"],
        step_deg=0.00625,
    )
    if kp_payload is None:
        kp_files = [ROOT / "analysis" / "out" / "karapinar_20260918_20260930.npz"]
        kp_payload = build_region_payload(
            site="karapinar",
            title="Karapınar Basin (Konya, Türkiye)",
            subtitle="Single 12-day provisional checkpoint overlaid with 29 verified obruk sinkholes",
            npz_files=kp_files,
            bbox=BBOX["karapinar"],
            step_deg=0.00625,
            extra_notes="Single 12-day pair shown alongside verified field sinkhole coordinates from Tapur & Bozyigit (2015).",
        )

    gj_path = ROOT / "data" / "karapinar" / "sinkholes.geojson"
    gj = json.loads(gj_path.read_text(encoding="utf-8"))
    kp_payload["sinkholes"] = [f["properties"] for f in gj["features"]]

    bundle = {
        "generated_from": "NISAR L2 GUNW Provisional (CRID P05023)",
        "quality": "provisional",
        "quality_note": DISCLAIMER,
        "regions": {
            "central_valley": cv_payload,
            "karapinar": kp_payload,
        },
    }

    out_path = ROOT / "web3d" / "surfaces.json"
    out_path.write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":"), allow_nan=False), encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024.0
    print(f"Wrote {out_path} ({size_kb:.1f} KB)")
    for k, reg in bundle["regions"].items():
        print(
            f"  {k}: grid={reg['rows']}x{reg['cols']}, dates={reg['dates']}, "
            f"max_sub={reg['max_subsidence_cm']} cm at {reg['max_subsidence_location']}, "
            f"rate={reg['rate_cm_per_yr_estimate']} cm/yr, p2..p98={reg['p2_cm']}..{reg['p98_cm']} cm"
        )


if __name__ == "__main__":
    main()
