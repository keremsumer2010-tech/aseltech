"""O1 — Permanent Aquifer Storage Loss (km3/yr) from Full-Year Permanent Compaction (PC8).

Computes permanent (inelastic) groundwater storage-capacity loss across the California
Central Valley (and Karapinar when full-year decomp is available) using the USGS
Circular 1182 / Poland (1984) principle: permanent aquitard compaction volume equals
permanent aquifer storage capacity loss:
    V_loss = sum( (-v_permanent_vertical) * A_pixel )
over valid pixels (`reason == 0` inside site bbox).

Outputs:
  - data/central_valley_fullyear/storage_loss.json
  - docs/story/media/pc8_storage_loss.png
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = ROOT / "analysis"
DECOMP_DIR = ANALYSIS_DIR / "decomp"

MIXED_QUALITY_NOTE = (
    "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
    "(NASA-JPL and ISRO), not by our team. This series MIXES provisional products with pre-calibration "
    "BETA products (dates before 2026-06-17); treat amplitudes before that date with extra caution."
)

# Verified physical & literature constants
MILLERTON_LAKE_KM3 = 0.64203  # USBR Friant Dam / Millerton Lake total capacity ~520,500 acre-ft
OLYMPIC_POOL_M3 = 2500.0      # Standard 50m x 25m x 2m Olympic swimming pool


def compute_storage_loss_metrics(
    v_vert_cm_yr: np.ndarray,
    se_vert_cm_yr: np.ndarray,
    ok_mask: np.ndarray,
    pixel_area_m2: float,
    subsidence_threshold_cm_yr: float = 1.0,
    block_px: int = 13,
) -> dict[str, float | int]:
    """Integrate permanent vertical compaction rate into annual storage-loss volume.

    Positive returned volumes represent permanent groundwater storage capacity loss.
    `v_vert_cm_yr` is negative for subsidence (downward motion).
    """
    valid = np.asarray(ok_mask, dtype=bool) & np.isfinite(v_vert_cm_yr) & np.isfinite(se_vert_cm_yr)
    sub_mask = valid & (v_vert_cm_yr < -abs(subsidence_threshold_cm_yr))

    def _integrate(mask: np.ndarray) -> dict[str, float | int]:
        n_px = int(mask.sum())
        if n_px == 0:
            return {
                "n_pixels": 0,
                "area_km2": 0.0,
                "mean_rate_cm_per_yr": 0.0,
                "volume_m3_per_yr": 0.0,
                "volume_million_m3_per_yr": 0.0,
                "volume_km3_per_yr": 0.0,
                "se_independent_km3_per_yr": 0.0,
                "se_block_km3_per_yr": 0.0,
            }
        # Downward rate is positive loss (-v_vert) in meters/yr
        loss_m_yr = -v_vert_cm_yr[mask].astype(np.float64) / 100.0
        se_m_yr = np.abs(se_vert_cm_yr[mask].astype(np.float64)) / 100.0
        vol_m3 = float(np.sum(loss_m_yr) * pixel_area_m2)
        se_ind_m3 = float(np.sqrt(np.sum((se_m_yr * pixel_area_m2) ** 2)))

        # Block-level spatial correlation approximation (~1 km blocks = block_px x block_px)
        H, W = mask.shape
        hb = (H // block_px) * block_px
        wb = (W // block_px) * block_px
        if hb >= block_px and wb >= block_px:
            m_blk = mask[:hb, :wb].reshape(H // block_px, block_px, W // block_px, block_px)
            v_blk = np.where(mask[:hb, :wb], -v_vert_cm_yr[:hb, :wb] / 100.0, np.nan).reshape(
                H // block_px, block_px, W // block_px, block_px
            )
            s_blk = np.where(mask[:hb, :wb], np.abs(se_vert_cm_yr[:hb, :wb]) / 100.0, np.nan).reshape(
                H // block_px, block_px, W // block_px, block_px
            )
            counts = m_blk.sum(axis=(1, 3))
            has_blk = counts > 0
            # Mean SE within each 1 km block (accounts for strong intra-block spatial correlation)
            s_flat = s_blk.transpose(0, 2, 1, 3).reshape(H // block_px, W // block_px, block_px * block_px)
            blk_se = np.nanmean(s_flat[has_blk], axis=1)
            blk_area = counts[has_blk].astype(np.float64) * pixel_area_m2
            se_blk_m3 = float(np.sqrt(np.sum((blk_se * blk_area) ** 2)))
        else:
            se_blk_m3 = se_ind_m3

        return {
            "n_pixels": n_px,
            "area_km2": round(n_px * pixel_area_m2 / 1e6, 2),
            "mean_rate_cm_per_yr": round(float(np.mean(loss_m_yr) * 100.0), 3),
            "volume_m3_per_yr": vol_m3,
            "volume_million_m3_per_yr": round(vol_m3 / 1e6, 2),
            "volume_km3_per_yr": round(vol_m3 / 1e9, 4),
            "se_independent_km3_per_yr": round(se_ind_m3 / 1e9, 5),
            "se_block_km3_per_yr": round(se_blk_m3 / 1e9, 5),
        }

    return {
        "active_subsiding_gt_threshold": _integrate(sub_mask),
        "net_all_valid_in_bbox": _integrate(valid),
    }


def _reconstruct_fullyear_cv() -> dict[str, Any]:
    """Reconstruct the 25-pair mixed Central Valley stack & decomposition in memory."""
    if str(ANALYSIS_DIR) not in sys.path:
        sys.path.insert(0, str(ANALYSIS_DIR))
    if str(DECOMP_DIR) not in sys.path:
        sys.path.insert(0, str(DECOMP_DIR))
    sys.modules.setdefault("dem", None)  # type: ignore[arg-type]

    import cumulative as cum_mod  # noqa: WPS433
    import decompose as dec_mod   # noqa: WPS433
    from gunw_io import BBOX      # noqa: WPS433

    site = "central_valley"
    bbox = BBOX[site]
    _, files = cum_mod.load_pairs(site, (f"{site}_beta",))
    used, _ = cum_mod.chain(files, ("provisional", "beta-precal"))
    d0 = used[0][3]
    x, y, epsg = d0["x"], d0["y"], int(d0["epsg"])

    pair_cm = []
    for _, _, _, d in used:
        unw = d["unw"]
        if "ion" in d and d["ion"].shape == unw.shape:
            unw = unw - d["ion"]
        cm = cum_mod.phase_to_cm(unw, float(d["wavelength"]))
        if "conncomp" in d and d["conncomp"].size:
            cm = cum_mod.mask_components(cm, d["conncomp"])
        cm = cum_mod.mask_coherence(cm, d["coh"], 0.3)
        cm = cum_mod.remove_islands(cm, cum_mod.ISLAND_MIN_PX)
        cm = cum_mod.deramp(cm, order=1)
        cm = cum_mod.cycle_outliers(cm, thr_cm=float(d["wavelength"]) / 4 * 100)
        pair_cm.append(cm)

    valid_all = np.logical_and.reduce([np.isfinite(c) for c in pair_cm])
    coh_mean = np.mean([np.load(f)["coh"].astype(np.float32) / 255 for _, _, f, _ in used], axis=0)
    XX, YY = np.meshgrid(x, y)
    LON, LAT = Transformer.from_crs(epsg, 4326, always_xy=True).transform(XX, YY)
    in_bbox = (LON >= bbox[0]) & (LON <= bbox[2]) & (LAT >= bbox[1]) & (LAT <= bbox[3])
    r, c, _ = cum_mod.choose_reference(coh_mean, valid_all & in_bbox, 3, stride=3)

    dates = [used[0][0]] + [p[1] for p in used]
    stack = [np.where(valid_all, 0.0, np.nan).astype(np.float32)]
    for cm in pair_cm:
        cm_ref = cum_mod.reference(cm, (r, c), 3)
        cm_ref[np.abs(cm_ref) > cum_mod.PAIR_OUTLIER_CM] = np.nan
        stack.append((stack[-1] + cm_ref).astype(np.float32))

    cum_stack = np.stack(stack, axis=0)
    t = np.array([dec_mod.decimal_year(dt) for dt in dates])
    res = dec_mod.fit(t, cum_stack)

    geom = np.load(ANALYSIS_DIR / "out" / "central_valley_geometry.npz")
    inc = np.asarray(geom["incidence"], dtype=np.float64)
    inc_filled = np.where(np.isfinite(inc), inc, 40.9)
    cos_inc = np.cos(np.radians(inc_filled))

    v_los = np.asarray(res["v_cm_per_yr"], dtype=np.float64)
    se_los = np.asarray(res["v_se"], dtype=np.float64)
    v_vert = v_los / cos_inc
    se_vert = se_los / cos_inc
    ok_bbox = (res["reason"] == 0) & in_bbox
    dx = float(abs(x[1] - x[0]))
    dy = float(abs(y[1] - y[0]))

    return {
        "x": x,
        "y": y,
        "epsg": epsg,
        "LON": LON,
        "LAT": LAT,
        "dates": dates,
        "v_los": v_los,
        "v_vert": v_vert,
        "se_vert": se_vert,
        "ok_bbox": ok_bbox,
        "pixel_area_m2": dx * dy,
        "inc_median_deg": float(np.nanmedian(inc[ok_bbox])),
    }


def _window_median(arr: np.ndarray, mask: np.ndarray, lon_grid: np.ndarray, lat_grid: np.ndarray,
                   lon0: float, lat0: float, half_deg: float = 0.02) -> float:
    win = mask & (np.abs(lon_grid - lon0) <= half_deg) & (np.abs(lat_grid - lat0) <= half_deg)
    if win.sum() < 10:
        dist2 = np.where(mask, (lon_grid - lon0) ** 2 + (lat_grid - lat0) ** 2, np.inf)
        r0, c0 = np.unravel_index(int(np.argmin(dist2)), dist2.shape)
        r1, r2 = max(0, r0 - 3), min(arr.shape[0], r0 + 4)
        c1, c2 = max(0, c0 - 3), min(arr.shape[1], c0 + 4)
        return float(np.nanmedian(arr[r1:r2, c1:c2]))
    return float(np.nanmedian(arr[win]))


def make_figure(out_png: Path, payload: dict[str, Any], v_vert: np.ndarray, ok_bbox: np.ndarray) -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.titlesize": 10.5,
        "axes.labelsize": 9.5,
    })
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.8), dpi=160, gridspec_kw={"width_ratios": [1.1, 1.0]})
    fig.patch.set_facecolor("#ffffff")

    # Panel A: Annual storage loss vs 3-ref uncertainty & physical/literature benchmarks
    ax1.set_facecolor("#fafafa")
    refs = payload["reference_sensitivity_volumes"]
    labels = [
        "Active Zone (>1 cm/yr)\nMain Ref (36.46N, 119.15W)",
        "Active Zone (>1 cm/yr)\nAlt Ref 1 (35.78N, 120.06W)",
        "Active Zone (>1 cm/yr)\nAlt Ref 2 (35.63N, 119.59W)",
        "Millerton Lake Capacity\n(USBR Friant Dam, 520.5k af)",
        "Smith et al. (2017) Lower\nSo. SJV (2007-10 avg/yr)",
        "Ojha et al. (2018) Drought\nTotal / 3 yr (2012-15)",
    ]
    vals = [
        refs[0]["active_gt_1cm_km3_per_yr"],
        refs[1]["active_gt_1cm_km3_per_yr"],
        refs[2]["active_gt_1cm_km3_per_yr"],
        MILLERTON_LAKE_KM3,
        0.138,  # 0.414 km3 / 3 yr (2007-2010 Smith et al.)
        0.440,  # ~1.32 km3 avg (~0.4-3.25% of ~24-29 km3 drought) -> show 0.25 km3/yr benchmark
    ]
    # Use exact literature ranges directly as clear comparison bars
    labels = [
        "NISAR Active Zone\n(>1 cm/yr, Main Ref)",
        "NISAR Active Zone\n(3-Ref Range: Alt1-Alt2)",
        "NISAR Basin Net\n(All Valid Pixels)",
        "Millerton Lake Total\n(Friant Dam, USBR)",
        "So. San Joaquin (2007-10)\nInSAR Annualized Avg*",
    ]
    y_pos = np.arange(len(labels))
    bar_vals = [
        payload["volume_km3_per_yr"],
        max(r["active_gt_1cm_km3_per_yr"] for r in refs),
        payload["net_basin_km3_per_yr"],
        MILLERTON_LAKE_KM3,
        0.138,
    ]
    colors = ["#1d4ed8", "#60a5fa", "#0f766e", "#d97706", "#64748b"]
    ax1.barh(y_pos, bar_vals, height=0.52, color=colors, alpha=0.88, edgecolor="#1e293b", linewidth=0.7)
    # Error bar on Main Ref showing [lower, upper]
    lo, hi = payload["lower"], payload["upper"]
    v0 = payload["volume_km3_per_yr"]
    ax1.errorbar([v0], [0], xerr=[[max(0.0, v0 - lo)], [max(0.0, hi - v0)]],
                 fmt="none", ecolor="#0f172a", elinewidth=2.0, capsize=4, zorder=5)

    for i, val in enumerate(bar_vals):
        extra = f" (range {lo:.2f}-{hi:.2f})" if i == 0 else ""
        ax1.text(val + 0.015, y_pos[i], f"{val:.3f} km3/yr{extra}" if i != 3 else f"{val:.3f} km3",
                 va="center", ha="left", fontsize=8.3, fontweight="bold", color="#0f172a")

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(labels, fontsize=8.3)
    ax1.invert_yaxis()
    ax1.set_xlim(0, max(bar_vals + [hi]) * 1.48)
    ax1.set_xlabel("Permanent aquifer storage-capacity loss or reservoir volume (km3/yr or km3)")
    ax1.set_title("A. Central Valley permanent storage loss vs. references", fontweight="bold", loc="left")
    ax1.grid(True, axis="x", linestyle=":", alpha=0.6)

    # Panel B: Distribution of pixel-level permanent vertical rates
    ax2.set_facecolor("#fafafa")
    rates = -v_vert[ok_bbox]  # positive = subsidence rate (cm/yr)
    clipped = np.clip(rates, -5.0, 22.0)
    bins = np.linspace(-5.0, 22.0, 55)
    ax2.hist(clipped, bins=bins, weights=np.full_like(clipped, 0.0064), color="#2563eb", alpha=0.75, edgecolor="#1e3a8a", linewidth=0.4)
    ax2.axvline(1.0, color="#dc2626", lw=1.4, ls="--", label="Active threshold (1.0 cm/yr)")
    med_rate = float(np.median(rates))
    ax2.axvline(med_rate, color="#0f172a", lw=1.3, ls=":", label=f"Basin median ({med_rate:.2f} cm/yr)")
    ax2.set_xlabel("Permanent vertical subsidence rate (cm/yr, positive = sinking)")
    ax2.set_ylabel("Valid footprint area (km2 per 0.5 cm/yr bin)")
    ax2.set_title("B. Pixel-level permanent compaction distribution", fontweight="bold", loc="left")
    ax2.grid(True, axis="y", linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right", fontsize=8.2, frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0")

    fig.suptitle(
        "Central Valley (24 Nov 2025 - 14 Oct 2026): Permanent Aquifer Storage-Capacity Loss Estimate",
        fontsize=11.0, fontweight="bold", y=0.98
    )
    fig.text(
        0.5, 0.012,
        "Data: NASA-ISRO NISAR L2 GUNW (mixed: 18 beta-precal + 7 provisional pairs); USGS Circular 1182 compaction=storage-loss method; *Smith et al. (2017) 0.414-0.748 km3 / 3 yr.\n"
        "NISAR data are provisional (calibration by NASA-JPL/ISRO). Estimates carry mixed-product and 3-reference uncertainty bounds. Analysis: Team Taykut.",
        fontsize=7.5, color="#334155", ha="center"
    )
    plt.tight_layout(rect=[0.0, 0.055, 1.0, 0.94])
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=160)
    plt.close(fig)


def run() -> dict[str, Any]:
    data = _reconstruct_fullyear_cv()
    v_vert = data["v_vert"]
    se_vert = data["se_vert"]
    ok_bbox = data["ok_bbox"]
    px_area = data["pixel_area_m2"]

    main_metrics = compute_storage_loss_metrics(v_vert, se_vert, ok_bbox, px_area, subsidence_threshold_cm_yr=1.0)

    # 3-reference sensitivity from data/central_valley_fullyear/summary.json
    summary = json.loads((ROOT / "data" / "central_valley_fullyear" / "summary.json").read_text(encoding="utf-8"))
    ref_coords = [
        ("Main ref", summary["reference_point"]["lon"], summary["reference_point"]["lat"]),
        ("Alt ref 1", summary["reference_sensitivity_all"][0]["alt_reference"]["lon"], summary["reference_sensitivity_all"][0]["alt_reference"]["lat"]),
        ("Alt ref 2", summary["reference_sensitivity_all"][1]["alt_reference"]["lon"], summary["reference_sensitivity_all"][1]["alt_reference"]["lat"]),
    ]

    ref_results = []
    for label, lon0, lat0 in ref_coords:
        offset_v = _window_median(v_vert, ok_bbox, data["LON"], data["LAT"], lon0, lat0)
        shifted_v = v_vert - offset_v
        m_ref = compute_storage_loss_metrics(shifted_v, se_vert, ok_bbox, px_area, subsidence_threshold_cm_yr=1.0)
        ref_results.append({
            "label": label,
            "lon": lon0,
            "lat": lat0,
            "ref_offset_v_cm_per_yr": round(offset_v, 3),
            "active_gt_1cm_km3_per_yr": m_ref["active_subsiding_gt_threshold"]["volume_km3_per_yr"],
            "active_gt_1cm_area_km2": m_ref["active_subsiding_gt_threshold"]["area_km2"],
            "net_basin_km3_per_yr": m_ref["net_all_valid_in_bbox"]["volume_km3_per_yr"],
        })

    active_vols = [r["active_gt_1cm_km3_per_yr"] for r in ref_results]
    se_blk = float(main_metrics["active_subsiding_gt_threshold"]["se_block_km3_per_yr"])
    vol_km3 = float(main_metrics["active_subsiding_gt_threshold"]["volume_km3_per_yr"])
    lower = round(max(0.0, min([vol_km3] + active_vols) - 1.96 * se_blk), 4)
    upper = round(max([vol_km3] + active_vols) + 1.96 * se_blk, 4)

    vol_mm3 = float(main_metrics["active_subsiding_gt_threshold"]["volume_million_m3_per_yr"])
    vol_m3 = float(main_metrics["active_subsiding_gt_threshold"]["volume_m3_per_yr"])

    payload = {
        "site": "central_valley_fullyear",
        "period": ["2025-11-24", "2026-10-14"],
        "quality": "mixed",
        "quality_note": MIXED_QUALITY_NOTE,
        "volume_km3_per_yr": vol_km3,
        "volume_million_m3_per_yr": vol_mm3,
        "lower": lower,
        "upper": upper,
        "area_km2": main_metrics["active_subsiding_gt_threshold"]["area_km2"],
        "mean_permanent_rate_cm_per_yr_estimate": main_metrics["active_subsiding_gt_threshold"]["mean_rate_cm_per_yr"],
        "net_basin_km3_per_yr": main_metrics["net_all_valid_in_bbox"]["volume_km3_per_yr"],
        "net_basin_million_m3_per_yr": main_metrics["net_all_valid_in_bbox"]["volume_million_m3_per_yr"],
        "net_basin_area_km2": main_metrics["net_all_valid_in_bbox"]["area_km2"],
        "se_independent_km3_per_yr": main_metrics["active_subsiding_gt_threshold"]["se_independent_km3_per_yr"],
        "se_block_km3_per_yr": se_blk,
        "incidence_median_deg": round(data["inc_median_deg"], 2),
        "reference_sensitivity_volumes": ref_results,
        "equivalents": {
            "millerton_lake_fraction_estimate": round(vol_km3 / MILLERTON_LAKE_KM3, 2),
            "millerton_lake_capacity_km3": MILLERTON_LAKE_KM3,
            "millerton_lake_source": "USBR Friant Dam / Millerton Lake (~520,500 acre-ft = 0.642 km3)",
            "olympic_swimming_pools_per_yr_estimate": int(round(vol_m3 / OLYMPIC_POOL_M3)),
            "olympic_pool_m3": OLYMPIC_POOL_M3,
        },
        "literature_comparison": [
            {
                "source": "Galloway, Jones, & Ingebritsen (1999), USGS Circular 1182",
                "url": "https://pubs.usgs.gov/circ/circ1182/",
                "relevance": "Establishes that inelastic aquitard compaction volume equals permanent groundwater storage capacity loss.",
            },
            {
                "source": "Smith et al. (2017), Water Resources Research (Southern San Joaquin Valley 2007-2010)",
                "relevance": "InSAR-derived permanent storage loss of 0.414-0.748 km3 over 3 years (~0.138-0.249 km3/yr annualized).",
            },
            {
                "source": "Ojha et al. (2018), Scientific Reports (San Joaquin Valley 2012-2015 drought)",
                "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6136988/",
                "relevance": "0.4%-3.25% permanent storage-capacity reduction alongside ~24-29 km3 total groundwater depletion.",
            },
        ],
        "method": (
            "Permanent aquifer storage loss V_loss = sum((-v_permanent_vertical) * A_pixel) integrated across "
            "valid decomposed pixels (reason == 0, within Central Valley bbox, active threshold v_vert < -1.0 cm/yr; "
            "net all-valid integral also reported). Line-of-sight permanent rates from 25-pair harmonic-linear fit "
            "(2025-11-24 to 2026-10-14) are projected to vertical via pixel-wise incidence angles (cos theta, median "
            f"{data['inc_median_deg']:.1f} deg). Uncertainty combines 1-km block-correlated standard error (13x13 px) "
            "with empirical 3-reference sensitivity re-referencing."
        ),
        "assumptions": [
            "Assumes inelastic compaction dominates the linear permanent trend term (v_cm_per_yr), while seasonal elastic recovery is absorbed by the annual sin/cos terms.",
            "Vertical projection assumes predominantly vertical compaction (v_vert = v_los / cos(theta)), neglecting minor horizontal tectonic/lateral motion.",
            "Series mixes 18 pre-calibration beta pairs (before 2026-06-17) with 7 provisional pairs (quality='mixed'); pre-calibration amplitudes carry extra uncertainty.",
            "Only valid coherent pixels (46.0% of bbox) are integrated; decorrelated irrigated fields inside the bowl are not extrapolated, making the integrated volume conservative where coherence drops.",
            "Standard errors of cumulative InSAR epochs are temporally correlated; 1-km block aggregation reduces but does not eliminate spatial/temporal correlation.",
        ],
    }

    out_json = ROOT / "data" / "central_valley_fullyear" / "storage_loss.json"
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    out_png = ROOT / "docs" / "story" / "media" / "pc8_storage_loss.png"
    make_figure(out_png, payload, v_vert, ok_bbox)
    print(json.dumps({
        "volume_km3_per_yr": payload["volume_km3_per_yr"],
        "lower": payload["lower"],
        "upper": payload["upper"],
        "area_km2": payload["area_km2"],
        "net_basin_km3_per_yr": payload["net_basin_km3_per_yr"],
        "olympic_pools": payload["equivalents"]["olympic_swimming_pools_per_yr_estimate"],
    }, indent=2))
    return payload


if __name__ == "__main__":
    run()
