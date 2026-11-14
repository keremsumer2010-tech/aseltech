"""Per-pixel Cramér-Rao InSAR displacement uncertainty map for provisional NISAR GUNW chains.

Usage:
    python analysis/pc5/uncertainty_map.py central_valley
    python analysis/pc5/uncertainty_map.py karapinar
    python analysis/pc5/uncertainty_map.py central_valley --looks 100

Model (Rodriguez & Martin 1992 / Cramér-Rao lower bound for multilook InSAR phase):
    sigma_phi(gamma, L) = sqrt(1 - gamma^2) / (gamma * sqrt(2 * L))   [rad]
    sigma_d             = (lambda / (4 * pi)) * sigma_phi * 100       [cm, LOS]
    sigma_total         = sqrt(sum_i sigma_{d,i}^2)                   [cm, LOS]

Default looks L = 208 (16 azimuth x 13 range nominal looks) is sourced directly from
docs/gunw_structure.md (HDF5 metadata of NISAR L2 PR GUNW Frequency A 80 m grids).
Note: This formal phase-noise lower bound captures short-scale thermal/decorrelation
speckle ONLY and explicitly excludes spatially correlated tropospheric delay,
elevation-ramp residuals, and phase-unwrapping errors.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DISCLAIMER = (
    "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
    "(NASA-JPL and ISRO), not by our team."
)
SITE_BBOX: dict[str, tuple[float, float, float, float]] = {
    "central_valley": (-120.2, 35.6, -119.0, 36.6),
    "konya": (32.4, 37.4, 33.9, 38.1),
    "karapinar": (33.3, 37.6, 33.8, 37.9),
}
DEFAULT_LOOKS = 208.0  # 16 azimuth x 13 range nominal looks (docs/gunw_structure.md §2)
DEFAULT_COH_THR = 0.3
VMIN_CM = 0.0
VMAX_CM = 1.0
COLORMAP = "viridis"


def _utm_params(epsg: int) -> tuple[float, float, float, float, float, float, bool]:
    if 32601 <= epsg <= 32660:
        zone, north = epsg - 32600, True
    elif 32701 <= epsg <= 32760:
        zone, north = epsg - 32700, False
    else:
        raise ValueError(f"Unsupported UTM EPSG without pyproj: {epsg}")
    a = 6378137.0
    f = 1.0 / 298.257223563
    e2 = f * (2.0 - f)
    ep2 = e2 / (1.0 - e2)
    k0 = 0.9996
    lon0_r = np.deg2rad((zone - 1) * 6.0 - 180.0 + 3.0)
    return a, e2, ep2, k0, lon0_r, f, north


def lonlat_to_utm(lon: np.ndarray, lat: np.ndarray, epsg: int) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized WGS84 geographic (lon, lat) -> UTM (Easting, Northing) in meters."""
    try:
        from pyproj import Transformer

        x, y = Transformer.from_crs(4326, epsg, always_xy=True).transform(lon, lat)
        return np.asarray(x, dtype=np.float64), np.asarray(y, dtype=np.float64)
    except ImportError:
        pass

    a, e2, ep2, k0, lon0_r, _, north = _utm_params(epsg)
    lat_r = np.deg2rad(np.asarray(lat, dtype=np.float64))
    dlon = np.deg2rad(np.asarray(lon, dtype=np.float64)) - lon0_r

    sin_l = np.sin(lat_r)
    cos_l = np.cos(lat_r)
    tan_l = np.tan(lat_r)

    n_val = a / np.sqrt(1.0 - e2 * sin_l**2)
    t_val = tan_l**2
    c_val = ep2 * cos_l**2
    a_val = cos_l * dlon

    m_val = a * (
        (1.0 - e2 / 4.0 - 3.0 * e2**2 / 64.0 - 5.0 * e2**3 / 256.0) * lat_r
        - (3.0 * e2 / 8.0 + 3.0 * e2**2 / 32.0 + 45.0 * e2**3 / 1024.0) * np.sin(2.0 * lat_r)
        + (15.0 * e2**2 / 256.0 + 45.0 * e2**3 / 1024.0) * np.sin(4.0 * lat_r)
        - (35.0 * e2**3 / 3072.0) * np.sin(6.0 * lat_r)
    )

    easting = k0 * n_val * (
        a_val
        + (1.0 - t_val + c_val) * a_val**3 / 6.0
        + (5.0 - 18.0 * t_val + t_val**2 + 72.0 * c_val - 58.0 * ep2) * a_val**5 / 120.0
    ) + 500000.0
    northing = k0 * (
        m_val
        + n_val * tan_l * (
            a_val**2 / 2.0
            + (5.0 - t_val + 9.0 * c_val + 4.0 * c_val**2) * a_val**4 / 24.0
            + (61.0 - 58.0 * t_val + t_val**2 + 600.0 * c_val - 330.0 * ep2) * a_val**6 / 720.0
        )
    )
    if not north:
        northing = northing + 10000000.0
    return easting, northing


def utm_to_lonlat(x: np.ndarray, y: np.ndarray, epsg: int) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized UTM (Easting, Northing) in meters -> WGS84 geographic (lon, lat)."""
    try:
        from pyproj import Transformer

        lon, lat = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x, y)
        return np.asarray(lon, dtype=np.float64), np.asarray(lat, dtype=np.float64)
    except ImportError:
        pass

    a, e2, ep2, k0, lon0_r, _, north = _utm_params(epsg)
    xx = np.asarray(x, dtype=np.float64) - 500000.0
    yy = np.asarray(y, dtype=np.float64) - (0.0 if north else 10000000.0)

    e1 = (1.0 - np.sqrt(1.0 - e2)) / (1.0 + np.sqrt(1.0 - e2))
    m_val = yy / k0
    mu = m_val / (a * (1.0 - e2 / 4.0 - 3.0 * e2**2 / 64.0 - 5.0 * e2**3 / 256.0))
    phi1 = (
        mu
        + (3.0 * e1 / 2.0 - 27.0 * e1**3 / 32.0) * np.sin(2.0 * mu)
        + (21.0 * e1**2 / 16.0 - 55.0 * e1**4 / 32.0) * np.sin(4.0 * mu)
        + (151.0 * e1**3 / 96.0) * np.sin(6.0 * mu)
        + (1097.0 * e1**4 / 512.0) * np.sin(8.0 * mu)
    )

    sin1 = np.sin(phi1)
    cos1 = np.cos(phi1)
    tan1 = np.tan(phi1)
    c1 = ep2 * cos1**2
    t1 = tan1**2
    n1 = a / np.sqrt(1.0 - e2 * sin1**2)
    r1 = a * (1.0 - e2) / np.power(1.0 - e2 * sin1**2, 1.5)
    d = xx / (n1 * k0)

    lat_r = phi1 - (n1 * tan1 / r1) * (
        d**2 / 2.0
        - (5.0 + 3.0 * t1 + 10.0 * c1 - 4.0 * c1**2 - 9.0 * ep2) * d**4 / 24.0
        + (61.0 + 90.0 * t1 + 298.0 * c1 + 45.0 * t1**2 - 252.0 * ep2 - 3.0 * c1**2) * d**6 / 720.0
    )
    lon_r = lon0_r + (
        d
        - (1.0 + 2.0 * t1 + c1) * d**3 / 6.0
        + (5.0 - 2.0 * c1 + 28.0 * t1 - 3.0 * c1**2 + 8.0 * ep2 + 24.0 * t1**2) * d**5 / 120.0
    ) / cos1
    return np.rad2deg(lon_r), np.rad2deg(lat_r)


def to_latlon_grid(arr: np.ndarray, x: np.ndarray, y: np.ndarray, epsg: int, bbox: Sequence[float], step: float = 0.001) -> np.ndarray:
    """Nearest-neighbour resample a UTM grid onto the regular north-up lon/lat grid matching cumulative.py."""
    w, s, e, n = bbox
    lons = np.arange(w + step / 2.0, e, step)
    lats = np.arange(n - step / 2.0, s, -step)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    xx, yy = lonlat_to_utm(lon_grid, lat_grid, epsg)
    dx, dy = float(x[1] - x[0]), float(y[1] - y[0])
    ix = np.rint((xx - float(x[0])) / dx).astype(int)
    iy = np.rint((yy - float(y[0])) / dy).astype(int)
    ok = (ix >= 0) & (ix < len(x)) & (iy >= 0) & (iy < len(y))
    out = np.full(lon_grid.shape, np.nan, dtype=np.float32)
    out[ok] = arr[iy[ok], ix[ok]]
    return out


def normalize_coherence(coh: np.ndarray) -> np.ndarray:
    """Convert raw coherence array (uint8 [0..255] or float [0..1]) to float64."""
    arr = np.asarray(coh)
    if np.issubdtype(arr.dtype, np.integer):
        return arr.astype(np.float64) / 255.0
    return arr.astype(np.float64)


def cramer_rao_phase_std(coherence: np.ndarray | float, looks: float = DEFAULT_LOOKS) -> np.ndarray | float:
    """Return multilook InSAR phase std (rad) using the Cramér-Rao approximation.

    Args:
        coherence: Interferometric coherence gamma in (0, 1] (values <= 0 or > 1 yield NaN).
        looks: Effective number of looks L (> 0).

    Returns:
        Phase standard deviation in radians (0.0 where gamma == 1.0).
    """
    if looks <= 0:
        raise ValueError(f"looks must be positive, got {looks}")
    scalar_input = np.isscalar(coherence)
    gamma = np.asarray(coherence, dtype=np.float64)
    valid = np.isfinite(gamma) & (gamma > 0.0) & (gamma <= 1.0)
    out = np.full(gamma.shape, np.nan, dtype=np.float64)
    g_val = np.clip(gamma[valid], 1e-12, 1.0)
    sigma = np.sqrt(np.maximum(0.0, 1.0 - g_val**2)) / (g_val * np.sqrt(2.0 * float(looks)))
    sigma[g_val >= 1.0] = 0.0
    out[valid] = sigma
    return float(out) if scalar_input else out


def phase_std_to_los_cm(
    sigma_phi_rad: np.ndarray | float,
    wavelength_m: float,
) -> np.ndarray | float:
    """Convert interferometric phase std (rad) to LOS displacement std (cm)."""
    if wavelength_m <= 0:
        raise ValueError(f"wavelength_m must be positive, got {wavelength_m}")
    factor = (float(wavelength_m) / (4.0 * np.pi)) * 100.0
    if np.isscalar(sigma_phi_rad):
        return float(sigma_phi_rad) * factor
    return np.asarray(sigma_phi_rad, dtype=np.float64) * factor


def compute_chain_sigma_cm(
    coherences: Sequence[np.ndarray],
    wavelengths_m: Sequence[float],
    valid_masks: Sequence[np.ndarray] | None = None,
    looks: float = DEFAULT_LOOKS,
) -> tuple[np.ndarray, np.ndarray]:
    """Propagate per-pair Cramér-Rao LOS noise (cm) in quadrature across a chain of pairs.

    Returns:
        (sigma_total_cm, valid_all_mask)
    """
    if not coherences:
        raise ValueError("coherences sequence must not be empty")
    if len(coherences) != len(wavelengths_m):
        raise ValueError("coherences and wavelengths_m must have equal length")

    shape = np.asarray(coherences[0]).shape
    var_sum = np.zeros(shape, dtype=np.float64)
    valid_all = np.ones(shape, dtype=bool)

    for idx, (coh_raw, lam) in enumerate(zip(coherences, wavelengths_m)):
        coh = normalize_coherence(coh_raw)
        mask = np.isfinite(coh) & (coh > 0.0) & (coh <= 1.0)
        if valid_masks is not None:
            mask = mask & np.asarray(valid_masks[idx], dtype=bool)

        sigma_phi = cramer_rao_phase_std(np.where(mask, coh, np.nan), looks=looks)
        sigma_cm = phase_std_to_los_cm(sigma_phi, float(lam))
        valid_all &= mask & np.isfinite(sigma_cm)
        var_sum += np.where(mask & np.isfinite(sigma_cm), sigma_cm**2, 0.0)

    sigma_total = np.full(shape, np.nan, dtype=np.float32)
    sigma_total[valid_all] = np.sqrt(var_sum[valid_all]).astype(np.float32)
    return sigma_total, valid_all


def load_site_provisional_chain(site: str, subset_dir: Path | None = None):
    """Load strictly gap-free consecutive provisional .npz pairs from pipeline/subset/<site>."""
    sdir = subset_dir or (ROOT / "pipeline" / "subset" / site)
    files = sorted(sdir.glob("*.npz"))
    if not files:
        raise FileNotFoundError(f"No .npz pair files found in {sdir}")
    pairs, notes = [], []
    for f in files:
        d = np.load(f, allow_pickle=False)
        q = str(d["quality"])
        d1, d2 = (str(d["date1"]), str(d["date2"])) if "date1" in d else tuple(f.stem.split("_"))
        if q != "provisional":
            notes.append(f"skipped {f.name}: quality={q}")
            continue
        pairs.append((d1, d2, f, d))
    if not pairs:
        raise ValueError(f"No provisional pairs found in {sdir}")
    pairs.sort(key=lambda p: p[0])
    used = [pairs[0]]
    for p in pairs[1:]:
        if p[0] == used[-1][1]:
            used.append(p)
        elif p[0] > used[-1][1]:
            notes.append(f"chain gap {used[-1][1]} -> {p[0]}: stopped at {used[-1][1]}")
            break
        else:
            notes.append(f"skipped overlapping pair {p[0]}_{p[1]}")
    return used, notes


def save_uncertainty_png(
    grid_latlon: np.ndarray,
    out_path: Path,
    vmin: float = VMIN_CM,
    vmax: float = VMAX_CM,
    cmap_name: str = COLORMAP,
) -> None:
    """Save north-up lat/lon grid as RGBA PNG with transparent NaNs and fixed range."""
    cmap = plt.get_cmap(cmap_name).copy()
    cmap.set_bad((0, 0, 0, 0))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.imsave(out_path, np.ma.masked_invalid(grid_latlon), cmap=cmap, vmin=vmin, vmax=vmax)


def generate_site_uncertainty(
    site: str,
    looks: float = DEFAULT_LOOKS,
    coh_thr: float = DEFAULT_COH_THR,
    subset_dir: Path | None = None,
    out_dir: Path | None = None,
    meta_file: Path | None = None,
) -> dict:
    """Compute sigma_cm.png and meta.json for a site and write outputs cleanly."""
    if meta_file is None:
        cand_std = ROOT / "data" / site / "meta.json"
        cand_global = ROOT / "data" / "global" / site / "meta.json"
        meta_file = cand_std if cand_std.exists() else cand_global
    if site in SITE_BBOX:
        bbox = list(SITE_BBOX[site])
    elif meta_file.exists():
        bbox = list(json.loads(meta_file.read_text(encoding="utf-8"))["bbox"])
    else:
        raise ValueError(f"Unknown site '{site}' and meta.json not found at {meta_file}")

    used, notes = load_site_provisional_chain(site, subset_dir=subset_dir)
    d0 = used[0][3]
    x, y, epsg = d0["x"], d0["y"], int(d0["epsg"])
    granules = [str(u[3]["granule"]) for u in used if "granule" in u[3]]
    dates = [used[0][0]] + [u[1] for u in used]

    coherences: list[np.ndarray] = []
    wavelengths: list[float] = []
    masks: list[np.ndarray] = []
    for _, _, _, d in used:
        coh = normalize_coherence(d["coh"])
        m = np.isfinite(d["unw"]) & (coh >= float(coh_thr))
        if "conncomp" in d:
            m &= d["conncomp"] != 0
        coherences.append(coh)
        wavelengths.append(float(d["wavelength"]))
        masks.append(m)

    sigma_utm, valid_all = compute_chain_sigma_cm(
        coherences=coherences,
        wavelengths_m=wavelengths,
        valid_masks=masks,
        looks=looks,
    )

    xx_grid, yy_grid = np.meshgrid(x, y)
    lon_grid, lat_grid = utm_to_lonlat(xx_grid, yy_grid, epsg)
    in_bbox = (lon_grid >= bbox[0]) & (lon_grid <= bbox[2]) & (lat_grid >= bbox[1]) & (lat_grid <= bbox[3])
    valid_bbox = valid_all & in_bbox
    sigma_vals = sigma_utm[valid_bbox]
    if sigma_vals.size == 0:
        raise ValueError(f"Zero valid pixels inside bbox for {site}")

    med = float(np.median(sigma_vals))
    p10 = float(np.percentile(sigma_vals, 10))
    p90 = float(np.percentile(sigma_vals, 90))
    p99 = float(np.percentile(sigma_vals, 99))
    vmin_val = float(np.min(sigma_vals))
    vmax_val = float(np.max(sigma_vals))
    mean_val = float(np.mean(sigma_vals))

    scale_100 = float(np.sqrt(float(looks) / 100.0))

    target_dir = out_dir or (ROOT / "data" / site / "uncertainty")
    target_dir.mkdir(parents=True, exist_ok=True)
    png_path = target_dir / "sigma_cm.png"
    grid_ll = to_latlon_grid(np.where(valid_all, sigma_utm, np.nan), x, y, epsg, bbox)
    save_uncertainty_png(grid_ll, png_path, vmin=VMIN_CM, vmax=VMAX_CM, cmap_name=COLORMAP)

    clipped_frac = float((sigma_vals > VMAX_CM).mean())
    meta = {
        "site": site,
        "bbox": bbox,
        "units": "cm",
        "component": "LOS 1-sigma Cramér-Rao formal phase-noise lower bound",
        "vmin": VMIN_CM,
        "vmax": VMAX_CM,
        "colormap": f"{COLORMAP} (dark/purple = lower sigma, bright/yellow = higher sigma; NaN transparent)",
        "median_sigma_cm": round(med, 3),
        "p90_sigma_cm": round(p90, 3),
        "p10_sigma_cm": round(p10, 3),
        "p99_sigma_cm": round(p99, 3),
        "mean_sigma_cm": round(mean_val, 3),
        "min_sigma_cm": round(vmin_val, 3),
        "max_sigma_cm": round(vmax_val, 3),
        "fraction_above_vmax": round(clipped_frac, 4),
        "n_pairs": len(used),
        "period": [dates[0], dates[-1]],
        "dates": dates,
        "wavelength_m": round(float(np.mean(wavelengths)), 6),
        "coherence_threshold": float(coh_thr),
        "effective_looks_L": float(looks),
        "looks_source": (
            "Nominal 16 azimuth x 13 range = 208 looks from docs/gunw_structure.md "
            "(/science/LSAR/GUNW/metadata/processingInformation/parameters/unwrappedInterferogram/frequencyA)"
        ),
        "sensitivity_L100": {
            "looks": 100.0,
            "scale_vs_nominal": round(scale_100, 4),
            "median_sigma_cm": round(med * scale_100, 3),
            "p90_sigma_cm": round(p90 * scale_100, 3),
        },
        "valid_pixels_in_bbox": int(valid_bbox.sum()),
        "total_pixels_in_bbox": int(in_bbox.sum()),
        "valid_pixel_fraction": round(float(valid_bbox.sum() / max(1, int(in_bbox.sum()))), 4),
        "granules": granules,
        "chain_notes": notes,
        "method": (
            "Per-pair phase std via Cramér-Rao / Rodriguez & Martin (1992): "
            "sigma_phi = sqrt(1 - gamma^2) / (gamma * sqrt(2 * L)), converted to LOS cm via "
            "(lambda / (4 * pi)) * sigma_phi * 100, and summed in quadrature across N consecutive "
            "provisional pairs: sigma_total = sqrt(sum(sigma_d_i^2)). Pixels masked per cumulative.py "
            "(coh >= 0.3, conncomp != 0, finite unwrapped phase in all pairs)."
        ),
        "assumptions": [
            f"Uses nominal multilooking L = {looks:g} (16 azimuth x 13 range looks inspected in docs/gunw_structure.md for CV 4000_SH; parameterizable via --looks).",
            "If RSLC spectral weighting, oversampling, geocoding bilinear resampling, or 20 MHz mode (2000_SH at Karapinar) lowers effective independent looks to L_eff = 100, all sigma values scale up by sqrt(208/100) = 1.442x (reported in sensitivity_L100).",
            "Assumes statistically independent interferometric pair noise summed in quadrature (sqrt(N) scaling).",
            "DOES NOT INCLUDE ATMOSPHERE: captures short-scale thermal/decorrelation phase noise ONLY; excludes spatially correlated tropospheric wet-delay turbulence (~1-3 cm/pair), elevation-ramp residuals, and phase-unwrapping errors.",
        ],
        "quality": "provisional",
        "quality_note": DISCLAIMER,
    }
    meta_path = target_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate per-pixel Cramér-Rao uncertainty map.")
    ap.add_argument("site", help="Site identifier (e.g. central_valley, karapinar, beijing)")
    ap.add_argument("--looks", type=float, default=DEFAULT_LOOKS, help="Effective looks L (default 208)")
    ap.add_argument("--thr", type=float, default=DEFAULT_COH_THR, help="Coherence mask threshold (default 0.3)")
    ap.add_argument("--subset-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--meta-file", type=Path, default=None)
    args = ap.parse_args()

    meta = generate_site_uncertainty(
        args.site,
        looks=args.looks,
        coh_thr=args.thr,
        subset_dir=args.subset_dir,
        out_dir=args.out_dir,
        meta_file=args.meta_file,
    )
    print(
        f"[{meta['site']}] pairs={meta['n_pairs']} L={meta['effective_looks_L']:g} "
        f"median={meta['median_sigma_cm']} cm, p90={meta['p90_sigma_cm']} cm, "
        f"max={meta['max_sigma_cm']} cm (valid={meta['valid_pixel_fraction']:.1%})"
    )


if __name__ == "__main__":
    main()
