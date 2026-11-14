"""Multi-frequency L-band (NISAR) vs. C-band (Sentinel-1 / OPERA DISP-S1) analysis.

Evaluates Challenge B1 ("different frequency, other sensor") over California's
Central Valley (Tulare Basin):
1. Queries NASA CMR for ``OPERA_L3_DISP-S1_V1`` and ``SENTINEL-1A/C_SLC`` coverage
   and attempts authenticated granule retrieval (max 1 file at a time; deleting
   any temporary NetCDF-4 immediately). Documents exact temporal coverage gaps
   and HTTP 401 access blockers honestly without fabricating C-band rasters.
2. Computes station-level agreement (Pearson r, RMSE, OLS slope) between NISAR
   L-band displacements and Nevada Geodetic Laboratory continuous GPS stations
   (``data/central_valley/validation.json``).
3. Quantifies observed L-band (24.20 cm) interferometric coherence and 12-to-24 day
   phase-gradient margins across all 25 Central Valley interferograms
   (``2025-11-24`` to ``2026-10-14``) inside both the full scene and the irrigated
   Tulare-Corcoran agricultural core, contrasting L-band (NISAR, SAOCOM) against
   C-band (Sentinel-1 OPERA DISP-S1, RCM / RADARSAT-1) physics and published
   Central Valley C-band InSAR rates (Neely et al. 2021; Ojha et al. 2019).
4. Saves compact machine-readable outputs to:
     - ``pipeline/subset/opera_disp/opera_disp_cv_coverage.json``
     - ``data/central_valley_s1/cross_sensor.json``
     - ``docs/story/media/pc5_cross_sensor.png``

Usage:
    python analysis/pc5/cross_sensor.py
    python analysis/pc5/cross_sensor.py --offline
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import requests

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.pc5.uncertainty_map import lonlat_to_utm

OPERA_DIR = ROOT / "pipeline" / "subset" / "opera_disp"
S1_OUT_DIR = ROOT / "data" / "central_valley_s1"
FIG_OUT = ROOT / "docs" / "story" / "media" / "pc5_cross_sensor.png"

DISCLAIMER = (
    "NISAR data are provisional. Calibration and validation are carried out by the "
    "NISAR project (NASA-JPL and ISRO), not by our team."
)
CV_BBOX = (-120.2, 35.6, -119.0, 36.6)
AG_CORE_BBOX = (-119.85, 35.85, -119.30, 36.20)
CMR_URL = "https://cmr.earthdata.nasa.gov/search/granules.json"

C_LIGHT_M_S = 299_792_458.0
NISAR_LAMBDA_CM = 24.19632429378531
S1_LAMBDA_CM = (C_LIGHT_M_S / 5.405e9) * 100.0  # 5.5466 cm Sentinel-1 C-band
RCM_LAMBDA_CM = (C_LIGHT_M_S / 5.405e9) * 100.0  # 5.5466 cm RADARSAT Constellation Mission C-band
R1_LAMBDA_CM = (C_LIGHT_M_S / 5.300e9) * 100.0   # 5.6565 cm RADARSAT-1 C-band
SAOCOM_LAMBDA_CM = (C_LIGHT_M_S / 1.275e9) * 100.0  # 23.5131 cm CONAE SAOCOM L-band

# Snapshot fallback used only when offline / in isolated test runs without network.
OFFLINE_CMR_SNAPSHOT: dict[str, Any] = {
    "source": "offline_snapshot_verified_2026-11-14",
    "opera_total_bbox_hits": 2663,
    "opera_2026_hits": 66,
    "opera_summer_2026_hits": 0,
    "sentinel1a_slc_summer_2026_hits": 0,
    "sentinel1c_slc_summer_2026_hits": 55,
    "latest_opera_any_frame_end": "2026-04-26",
    "full_coverage_frame": "F38502",
    "f38502_coverage": {"cv_points": "12/12", "fullyear_points": "12/12", "gps_stations": "10/10"},
    "f38502_summer2025_window": ["2025-07-19", "2025-10-17"],
    "f38502_latest_winter_window": ["2025-10-17", "2026-02-14"],
    "raw_download_status": (
        "HTTP 401 access denied (cumulus.asf.earthdatacloud.nasa.gov / "
        "ASFAuthenticationError: Invalid/Expired token passed; OAuth client "
        "BO_n7nTIlMljdvU6kRRB3g pre-authorization required)."
    ),
}

VALLEY_SUBSIDING_STATIONS = {"CAHA", "HANF", "QCAP", "TLBN", "P056"}


def _point_in_poly(lon: float, lat: float, poly_str: str) -> bool:
    """Ray-casting point-in-polygon test on a CMR lat-lon space-separated string."""
    coords = [float(v) for v in poly_str.split()]
    lats = coords[0::2]
    lons = coords[1::2]
    inside = False
    j = len(lats) - 1
    for i in range(len(lats)):
        yi, xi = lats[i], lons[i]
        yj, xj = lats[j], lons[j]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside


def regression_metrics(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """Return Pearson r, RMSE, bias (mean y - x), and OLS slope/intercept (y = slope*x + b)."""
    xv = np.asarray(x, dtype=np.float64)
    yv = np.asarray(y, dtype=np.float64)
    ok = np.isfinite(xv) & np.isfinite(yv)
    xv, yv = xv[ok], yv[ok]
    if xv.size < 2:
        return {"n": int(xv.size), "r": math.nan, "rmse_cm": math.nan, "bias_cm": math.nan, "slope": math.nan, "intercept_cm": math.nan}
    r = float(np.corrcoef(xv, yv)[0, 1]) if np.std(xv) > 0 and np.std(yv) > 0 else math.nan
    rmse = float(np.sqrt(np.mean((yv - xv) ** 2)))
    bias = float(np.mean(yv - xv))
    slope, intercept = np.polyfit(xv, yv, 1)
    return {
        "n": int(xv.size),
        "r": round(r, 4),
        "rmse_cm": round(rmse, 3),
        "bias_cm": round(bias, 3),
        "slope": round(float(slope), 4),
        "intercept_cm": round(float(intercept), 3),
    }


def query_cmr_opera_status(
    cv_pts: list[dict[str, Any]],
    fy_pts: list[dict[str, Any]],
    gps_pts: list[dict[str, Any]],
    attempt_download: bool = True,
    offline: bool = False,
) -> dict[str, Any]:
    """Inspect live CMR OPERA_L3_DISP-S1_V1 + Sentinel-1 SLC coverage over Central Valley."""
    if offline:
        return dict(OFFLINE_CMR_SNAPSHOT)

    bbox_str = ",".join(str(v) for v in CV_BBOX)
    queries = {
        "total": ("OPERA_L3_DISP-S1_V1", {"bounding_box": bbox_str, "page_size": 1}),
        "yr2026": (
            "OPERA_L3_DISP-S1_V1",
            {"bounding_box": bbox_str, "temporal": "2026-01-01T00:00:00Z,2026-12-31T23:59:59Z", "page_size": 100},
        ),
        "summer2026": (
            "OPERA_L3_DISP-S1_V1",
            {"bounding_box": bbox_str, "temporal": "2026-06-28T00:00:00Z,2026-10-14T23:59:59Z", "page_size": 1},
        ),
        "s1a_summer": (
            "SENTINEL-1A_SLC",
            {"bounding_box": bbox_str, "temporal": "2026-06-28T00:00:00Z,2026-10-14T23:59:59Z", "page_size": 1},
        ),
        "s1c_summer": (
            "SENTINEL-1C_SLC",
            {"bounding_box": bbox_str, "temporal": "2026-06-28T00:00:00Z,2026-10-14T23:59:59Z", "page_size": 1},
        ),
        "tulare_center": (
            "OPERA_L3_DISP-S1_V1",
            {"point": "-119.5,36.0", "temporal": "2025-06-01T00:00:00Z,2026-12-31T23:59:59Z", "page_size": 200},
        ),
    }

    res: dict[str, tuple[int, list[dict[str, Any]]]] = {}
    for key, (sn, extra) in queries.items():
        resp = requests.get(CMR_URL, params={"short_name": sn, **extra}, timeout=25)
        resp.raise_for_status()
        hits = int(resp.headers.get("CMR-Hits", "0"))
        entries = resp.json().get("feed", {}).get("entry", [])
        res[key] = (hits, entries)

    yr26_entries = res["yr2026"][1]
    latest_end_2026 = max((e["time_end"][:10] for e in yr26_entries), default=None)
    frames_2026 = sorted({e["title"].split("_")[4] for e in yr26_entries})

    f38502 = [e for e in res["tulare_center"][1] if "_F38502_" in e["title"]]
    f38502.sort(key=lambda x: (x["time_start"][:10], x["time_end"][:10]))
    sample_poly = f38502[-1]["polygons"][0][0] if f38502 else ""
    cov_cv = sum(_point_in_poly(p["lon"], p["lat"], sample_poly) for p in cv_pts) if sample_poly else 0
    cov_fy = sum(_point_in_poly(p["lon"], p["lat"], sample_poly) for p in fy_pts) if sample_poly else 0
    cov_gps = sum(_point_in_poly(p["lon"], p["lat"], sample_poly) for p in gps_pts) if sample_poly else 0

    summer25 = [e for e in f38502 if e["time_start"][:10] == "2025-07-19"]
    winter26 = [e for e in f38502 if e["time_start"][:10] == "2025-10-17"]

    raw_status = "Download skipped by flag."
    if attempt_download and f38502:
        raw_status = _probe_one_opera_granule(f38502[-1])

    return {
        "source": "live_cmr_earthdata",
        "opera_total_bbox_hits": res["total"][0],
        "opera_2026_hits": res["yr2026"][0],
        "opera_2026_frames": frames_2026,
        "opera_summer_2026_hits": res["summer2026"][0],
        "sentinel1a_slc_summer_2026_hits": res["s1a_summer"][0],
        "sentinel1c_slc_summer_2026_hits": res["s1c_summer"][0],
        "latest_opera_any_frame_end": latest_end_2026,
        "full_coverage_frame": "F38502",
        "f38502_total_since_2025_06": len(f38502),
        "f38502_coverage": {
            "cv_points": f"{cov_cv}/{len(cv_pts)}",
            "fullyear_points": f"{cov_fy}/{len(fy_pts)}",
            "gps_stations": f"{cov_gps}/{len(gps_pts)}",
        },
        "f38502_summer2025_window": [summer25[0]["time_start"][:10], summer25[-1]["time_end"][:10]] if summer25 else None,
        "f38502_latest_winter_window": [winter26[0]["time_start"][:10], winter26[-1]["time_end"][:10]] if winter26 else None,
        "raw_download_status": raw_status,
    }


def _probe_one_opera_granule(entry: dict[str, Any]) -> str:
    """Attempt single-granule download (strictly deleting any temporary file afterward)."""
    nc_urls = [lnk["href"] for lnk in entry.get("links", []) if lnk.get("href", "").endswith(".nc")]
    if not nc_urls:
        return "No .nc download URL listed in CMR entry."
    OPERA_DIR.mkdir(parents=True, exist_ok=True)
    tmp_path = OPERA_DIR / "_tmp_probe_opera.nc"
    try:
        from pipeline.download import download_file

        p, _ = download_file(nc_urls[0], tmp_path, timeout=45, max_attempts=1)
        p.unlink(missing_ok=True)
        return f"Downloaded and deleted temporary probe {entry['title']}"
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"
    finally:
        for leftover in OPERA_DIR.glob("_tmp*"):
            leftover.unlink(missing_ok=True)


def evaluate_nisar_vs_gnss(validation: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute station-terminal and pooled-epoch L-band NISAR vs. continuous GPS stats."""
    station_rows = []
    term_insar, term_gnss = [], []
    term_insar_los, term_gnss_los = [], []
    pooled_insar, pooled_gnss = [], []
    valley_insar, valley_gnss = [], []

    for st in validation:
        inc_rad = math.radians(float(st["incidence_deg"]))
        cos_inc = math.cos(inc_rad)
        ins_v = np.asarray(st["insar"], dtype=np.float64)
        gns_v = np.asarray(st["gnss"], dtype=np.float64)
        ins_los = ins_v * cos_inc
        gns_los = gns_v * cos_inc

        term_insar.append(float(ins_v[-1]))
        term_gnss.append(float(gns_v[-1]))
        term_insar_los.append(float(ins_los[-1]))
        term_gnss_los.append(float(gns_los[-1]))
        pooled_insar.extend(ins_v[1:].tolist())
        pooled_gnss.extend(gns_v[1:].tolist())

        in_valley = st["station"] in VALLEY_SUBSIDING_STATIONS
        if in_valley:
            valley_insar.append(float(ins_v[-1]))
            valley_gnss.append(float(gns_v[-1]))

        station_rows.append(
            {
                "station": st["station"],
                "lon": float(st["lon"]),
                "lat": float(st["lat"]),
                "incidence_deg": float(st["incidence_deg"]),
                "valley_subsiding_core": in_valley,
                "temporal_corr": round(float(st["corr"]), 4),
                "rmse_vertical_cm": round(float(st["rmse_cm"]), 3),
                "terminal_nisar_vertical_cm": round(float(ins_v[-1]), 3),
                "terminal_gnss_up_cm": round(float(gns_v[-1]), 3),
                "terminal_nisar_los_cm": round(float(ins_los[-1]), 3),
                "terminal_gnss_los_cm": round(float(gns_los[-1]), 3),
            }
        )

    return {
        "n_stations": len(station_rows),
        "terminal_vertical_metrics": regression_metrics(np.array(term_gnss), np.array(term_insar)),
        "terminal_los_metrics": regression_metrics(np.array(term_gnss_los), np.array(term_insar_los)),
        "pooled_70epochs_vertical_metrics": regression_metrics(np.array(pooled_gnss), np.array(pooled_insar)),
        "valley_core_5stations_terminal_vertical": regression_metrics(np.array(valley_gnss), np.array(valley_insar)),
        "stations": station_rows,
    }


def analyze_lband_coherence_series() -> dict[str, Any]:
    """Measure L-band coherence retention across all 25 beta+provisional Central Valley pairs."""
    beta_files = sorted((ROOT / "pipeline" / "subset" / "central_valley_beta").glob("*.npz"))
    prov_files = sorted((ROOT / "pipeline" / "subset" / "central_valley").glob("*.npz"))
    all_files = [(fp, "beta-precal") for fp in beta_files] + [(fp, "provisional") for fp in prov_files]
    if not all_files:
        raise FileNotFoundError("Missing Central Valley .npz subsets for coherence analysis.")

    z0 = np.load(all_files[0][0])
    x, y, epsg = z0["x"], z0["y"], int(z0["epsg"])
    w_e, w_n = lonlat_to_utm(
        np.array([AG_CORE_BBOX[0], AG_CORE_BBOX[2]]),
        np.array([AG_CORE_BBOX[1], AG_CORE_BBOX[3]]),
        epsg,
    )
    mx = (x >= min(w_e)) & (x <= max(w_e))
    my = (y >= min(w_n)) & (y <= max(w_n))

    pairs = []
    lam_cm = float(z0["wavelength"]) * 100.0
    for fp, qclass in all_files:
        z = np.load(fp)
        coh = z["coh"].astype(np.float64) / 255.0
        pos = coh > 0
        vals = coh[pos]
        core = coh[np.ix_(my, mx)]
        core_pos = core[core > 0]
        date1 = str(z["date1"])
        date2 = str(z["date2"])
        dt_days = (datetime.strptime(date2, "%Y-%m-%d") - datetime.strptime(date1, "%Y-%m-%d")).days
        pairs.append(
            {
                "pair": f"{date1}_{date2}",
                "date1": date1,
                "date2": date2,
                "dt_days": dt_days,
                "quality_class": qclass,
                "bbox_median_coh": round(float(np.median(vals)), 4),
                "bbox_p25_coh": round(float(np.percentile(vals, 25)), 4),
                "bbox_p75_coh": round(float(np.percentile(vals, 75)), 4),
                "bbox_valid_frac_ge_03": round(float(np.mean(coh >= 0.3)), 4),
                "ag_core_median_coh": round(float(np.median(core_pos)), 4),
                "ag_core_p25_coh": round(float(np.percentile(core_pos, 25)), 4),
                "ag_core_valid_frac_ge_03": round(float(np.mean(core >= 0.3)), 4),
            }
        )

    def _season_avg(subset: list[dict[str, Any]]) -> dict[str, float]:
        return {
            "n_pairs": len(subset),
            "mean_bbox_median_coh": round(float(np.mean([p["bbox_median_coh"] for p in subset])), 3),
            "mean_ag_core_median_coh": round(float(np.mean([p["ag_core_median_coh"] for p in subset])), 3),
            "mean_ag_core_valid_frac": round(float(np.mean([p["ag_core_valid_frac_ge_03"] for p in subset])), 3),
        }

    return {
        "wavelength_cm": round(lam_cm, 4),
        "ag_core_bbox": list(AG_CORE_BBOX),
        "n_pairs_total": len(pairs),
        "seasonal_summary": {
            "winter_dec_feb": _season_avg([p for p in pairs if p["date2"] <= "2026-02-28"]),
            "spring_mar_may": _season_avg([p for p in pairs if "2026-02-28" < p["date2"] <= "2026-06-04"]),
            "summer_jun_oct": _season_avg([p for p in pairs if p["date2"] > "2026-06-04"]),
        },
        "pairs": pairs,
    }


def evaluate_phase_ambiguity_margins(
    cv_pts: list[dict[str, Any]],
    fy_pts: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compare observed 12-to-24 day LOS increments against L-band vs. C-band wrap limits."""
    l_fringe = NISAR_LAMBDA_CM / 2.0
    l_half = NISAR_LAMBDA_CM / 4.0
    c_fringe = S1_LAMBDA_CM / 2.0
    c_half = S1_LAMBDA_CM / 4.0

    def _inspect_top5(pts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        out = []
        for p in pts[:5]:
            disp = np.asarray([np.nan if v is None else float(v) for v in p["disp_cm"]], dtype=np.float64)
            steps = np.diff(disp)
            abs_steps = np.abs(steps)
            imax = int(np.nanargmax(abs_steps))
            n_gt_c_half = int(np.sum(abs_steps > c_half))
            n_gt_c_full = int(np.sum(abs_steps > c_fringe))
            out.append(
                {
                    "id": p["id"],
                    "name": p["name"],
                    "max_abs_step_cm": round(float(abs_steps[imax]), 2),
                    "signed_max_step_cm": round(float(steps[imax]), 2),
                    "pair": f"{p['dates'][imax]}->{p['dates'][imax+1]}",
                    "intervals_exceeding_c_band_half_fringe_1_39cm": n_gt_c_half,
                    "intervals_exceeding_c_band_full_fringe_2_77cm": n_gt_c_full,
                    "intervals_exceeding_l_band_half_fringe_6_05cm": int(np.sum(abs_steps > l_half)),
                }
            )
        return out

    return {
        "wavelength_ratio_L_over_C": round(NISAR_LAMBDA_CM / S1_LAMBDA_CM, 3),
        "sensors": [
            {
                "mission": "NISAR (NASA-ISRO)",
                "band": "L-band",
                "frequency_ghz": 1.257,
                "wavelength_cm": round(NISAR_LAMBDA_CM, 2),
                "full_2pi_fringe_cm": round(l_fringe, 2),
                "half_cycle_limit_cm": round(l_half, 2),
            },
            {
                "mission": "SAOCOM-1A/1B (CONAE, Argentina)",
                "band": "L-band",
                "frequency_ghz": 1.275,
                "wavelength_cm": round(SAOCOM_LAMBDA_CM, 2),
                "full_2pi_fringe_cm": round(SAOCOM_LAMBDA_CM / 2.0, 2),
                "half_cycle_limit_cm": round(SAOCOM_LAMBDA_CM / 4.0, 2),
            },
            {
                "mission": "Sentinel-1A/1C / OPERA DISP-S1 (ESA / NASA)",
                "band": "C-band",
                "frequency_ghz": 5.405,
                "wavelength_cm": round(S1_LAMBDA_CM, 2),
                "full_2pi_fringe_cm": round(c_fringe, 2),
                "half_cycle_limit_cm": round(c_half, 2),
            },
            {
                "mission": "RCM / RADARSAT-1 (CSA, Canada)",
                "band": "C-band",
                "frequency_ghz": "5.405 / 5.300",
                "wavelength_cm": f"{RCM_LAMBDA_CM:.2f} / {R1_LAMBDA_CM:.2f}",
                "full_2pi_fringe_cm": f"{RCM_LAMBDA_CM / 2.0:.2f} / {R1_LAMBDA_CM / 2.0:.2f}",
                "half_cycle_limit_cm": f"{RCM_LAMBDA_CM / 4.0:.2f} / {R1_LAMBDA_CM / 4.0:.2f}",
            },
        ],
        "cv_108d_top5": _inspect_top5(cv_pts),
        "cv_fullyear_top5": _inspect_top5(fy_pts),
    }


def make_figure(
    gnss_eval: dict[str, Any],
    coh_data: dict[str, Any],
    cmr_status: dict[str, Any],
    out_path: Path,
) -> Path:
    """Render two-panel Figure comparing NISAR L-band validation and C-band limitations."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.6, 5.6), dpi=180)
    fig.patch.set_facecolor("white")

    # Panel A: NISAR L-band vertical estimate vs. Continuous GPS + published C-band envelope
    stations = gnss_eval["stations"]
    gx = np.array([s["terminal_gnss_up_cm"] for s in stations])
    iy = np.array([s["terminal_nisar_vertical_cm"] for s in stations])
    valley = np.array([s["valley_subsiding_core"] for s in stations])

    m = gnss_eval["terminal_vertical_metrics"]
    grid_x = np.linspace(-5.2, 1.0, 100)
    ax1.plot(grid_x, grid_x, linestyle="--", color="#555555", linewidth=1.1, label="1:1 reference line")
    ax1.plot(
        grid_x,
        m["slope"] * grid_x + m["intercept_cm"],
        color="#005f73",
        linewidth=1.6,
        label=f"OLS fit (r = {m['r']:.3f}, slope = {m['slope']:.2f})",
    )
    ax1.scatter(gx[valley], iy[valley], s=72, color="#b2182b", edgecolor="white", linewidth=0.9, zorder=4, label="Tulare Valley core GPS (n = 5)")
    ax1.scatter(gx[~valley], iy[~valley], s=68, color="#2166ac", edgecolor="white", linewidth=0.9, zorder=4, label="Margin / foothill GPS (n = 5)")

    offsets = {
        "TLBN": (0.14, -0.34),
        "CAHA": (-0.65, -0.40),
        "QCAP": (-0.15, 0.34),
        "HANF": (0.14, -0.28),
        "P056": (0.14, -0.24),
        "CAFP": (-0.90, -0.45),
        "CAD1": (-0.95, 0.25),
        "P565": (0.18, -0.58),
        "P564": (-0.75, 0.42),
        "P566": (0.16, 0.28),
    }
    for s in stations:
        dx, dy = offsets.get(s["station"], (0.1, 0.1))
        gx_i, iy_i = s["terminal_gnss_up_cm"], s["terminal_nisar_vertical_cm"]
        ax1.annotate(
            s["station"],
            xy=(gx_i, iy_i),
            xytext=(gx_i + dx, iy_i + dy),
            fontsize=8.0,
            color="#222222",
            arrowprops=dict(arrowstyle="-", color="#999999", lw=0.7, shrinkA=0, shrinkB=3),
        )

    ax1.axhline(0, color="#aaaaaa", linewidth=0.7)
    ax1.axvline(0, color="#aaaaaa", linewidth=0.7)
    ax1.set_xlim(-5.1, 0.9)
    ax1.set_ylim(-5.6, 2.8)
    ax1.set_xlabel("NGL Continuous GPS Vertical (cm, 2026-06-28 to 2026-10-14)", fontsize=9.5)
    ax1.set_ylabel("NISAR L-band Vertical Estimate (cm, LOS / cos i)", fontsize=9.5)
    ax1.set_title("A. L-band NISAR vs. Continuous GPS (108 d, N = 10)", fontsize=10.5, fontweight="bold", pad=10)
    ax1.grid(alpha=0.25, linewidth=0.6)
    ax1.legend(loc="lower right", fontsize=8.2, frameon=True, facecolor="white", framealpha=0.94)

    stats_txt = (
        f"All 10 GPS: r = {m['r']:.3f}, RMSE = {m['rmse_cm']:.2f} cm\n"
        f"Valley core (5): RMSE = {gnss_eval['valley_core_5stations_terminal_vertical']['rmse_cm']:.2f} cm\n"
        f"Pooled 70 epochs: r = {gnss_eval['pooled_70epochs_vertical_metrics']['r']:.3f}"
    )
    ax1.text(
        0.03,
        0.96,
        stats_txt,
        transform=ax1.transAxes,
        va="top",
        ha="left",
        fontsize=8.2,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#f7f7f7", edgecolor="#cccccc"),
    )

    # Panel B: 11-Month L-band agricultural coherence vs. OPERA DISP-S1 C-band window
    pairs = coh_data["pairs"]
    dates = [datetime.strptime(p["date2"], "%Y-%m-%d") for p in pairs]
    bbox_med = [p["bbox_median_coh"] for p in pairs]
    core_med = [p["ag_core_median_coh"] for p in pairs]
    core_p25 = [p["ag_core_p25_coh"] for p in pairs]
    core_vfrac = [p["ag_core_valid_frac_ge_03"] for p in pairs]

    # Highlight OPERA DISP-S1 coverage cutoff vs NISAR summer window
    ax2.axvspan(datetime(2025, 11, 24), datetime(2026, 2, 14), color="#d1e5f0", alpha=0.45, label="OPERA DISP-S1 F38502 overlap (to 2026-02-14)")
    ax2.axvspan(datetime(2026, 6, 28), datetime(2026, 10, 14), color="#fddbc7", alpha=0.45, label="NISAR summer 108 d (0 OPERA DISP-S1 granules)")

    ax2.plot(dates, bbox_med, color="#1b7837", marker="o", markersize=4.0, linewidth=1.6, label="NISAR L-band full-bbox median coherence")
    ax2.plot(dates, core_med, color="#762a83", marker="s", markersize=4.0, linewidth=1.7, label="NISAR L-band Tulare ag-core median coherence")
    ax2.plot(dates, core_vfrac, color="#d95f02", linestyle="-.", linewidth=1.5, label="Tulare ag-core valid fraction (coh >= 0.30)")
    ax2.fill_between(dates, core_p25, core_med, color="#762a83", alpha=0.14)
    ax2.axhline(0.30, color="#b2182b", linestyle=":", linewidth=1.2, label="Unwrapping coherence mask (0.30)")
    ax2.axvline(datetime(2026, 4, 26), color="#2166ac", linestyle="--", linewidth=1.2)
    ax2.text(
        datetime(2026, 4, 29),
        0.99,
        "Last OPERA DISP-S1\nin CV (2026-04-26)",
        fontsize=7.8,
        color="#2166ac",
        va="top",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#c6dbef", alpha=0.9),
    )

    ax2.set_ylim(-0.02, 1.04)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax2.set_ylabel("Coherence / Valid Pixel Fraction", fontsize=9.5)
    ax2.set_xlabel("NISAR Pair Secondary Date (25 pairs, 2025-11-24 to 2026-10-14)", fontsize=9.5)
    ax2.set_title("B. L-band Crop Coherence Preservation & OPERA C-band Window", fontsize=10.5, fontweight="bold", pad=10)
    ax2.grid(alpha=0.25, linewidth=0.6)
    ax2.legend(loc="lower left", fontsize=7.3, frameon=True, facecolor="white", framealpha=0.94, ncol=1)

    fig.suptitle(
        "Cross-Sensor & Multi-Frequency Validation: L-band NISAR (24.2 cm), Continuous GPS, and C-band Sentinel-1 (5.55 cm)",
        fontsize=11.5,
        fontweight="bold",
        y=0.99,
    )
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.text(
        0.5,
        0.008,
        f"Data: NASA-ISRO NISAR L2 GUNW (ASF DAAC), NASA CMR OPERA DISP-S1 V1 ({cmr_status['opera_summer_2026_hits']} summer granules), NGL GPS. Analysis: Team Taykut.",
        ha="center",
        fontsize=7.8,
        color="#555555",
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=180)
    plt.close(fig)
    return out_path


def run_cross_sensor_analysis(
    offline: bool = False,
    opera_dir: Path = OPERA_DIR,
    s1_out_dir: Path = S1_OUT_DIR,
    fig_out: Path = FIG_OUT,
) -> dict[str, Any]:
    """Execute full B1 multi-sensor / multi-frequency workflow and persist JSON + PNG outputs."""
    cv_pts = json.loads((ROOT / "data" / "central_valley" / "points.json").read_text(encoding="utf-8"))
    fy_pts = json.loads((ROOT / "data" / "central_valley_fullyear" / "points.json").read_text(encoding="utf-8"))
    gps_pts = json.loads((ROOT / "data" / "central_valley" / "validation.json").read_text(encoding="utf-8"))

    cmr_status = query_cmr_opera_status(cv_pts, fy_pts, gps_pts, attempt_download=(not offline), offline=offline)
    gnss_eval = evaluate_nisar_vs_gnss(gps_pts)
    coh_data = analyze_lband_coherence_series()
    ambiguity = evaluate_phase_ambiguity_margins(cv_pts, fy_pts)

    opera_dir.mkdir(parents=True, exist_ok=True)
    s1_out_dir.mkdir(parents=True, exist_ok=True)

    opera_coverage_out = {
        "dataset": "OPERA_L3_DISP-S1_V1",
        "site": "central_valley",
        "bbox": list(CV_BBOX),
        "nisar_summer_window": ["2026-06-28", "2026-10-14"],
        "nisar_fullyear_window": ["2025-11-24", "2026-10-14"],
        "cmr_status": cmr_status,
        "quality_note": DISCLAIMER,
    }
    (opera_dir / "opera_disp_cv_coverage.json").write_text(
        json.dumps(opera_coverage_out, indent=2), encoding="utf-8"
    )

    cross_sensor_out = {
        "title": "L-band NISAR vs. C-band Sentinel-1 (OPERA DISP-S1) & Continuous GPS Synthesis",
        "quality_note": DISCLAIMER,
        "cmr_opera_disp_s1": cmr_status,
        "nisar_vs_gnss_validation": gnss_eval,
        "lband_coherence_25_pairs": coh_data,
        "radar_frequency_and_ambiguity": ambiguity,
        "literature_cband_vs_lband_benchmarks": [
            {
                "source": "Neely et al. (2021), Water Resources Research 57(4)",
                "sensor": "Sentinel-1 C-band (5.55 cm) + cGPS",
                "period": "Oct 2015 - Sep 2017",
                "rate_cm_per_yr": "Dry WY2016 mean -4.20, peak -34.5; Wet WY2017 mean -2.04, peak -17.7; Apr 2015-Oct 2017 peak -27.0",
                "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8047915/",
            },
            {
                "source": "Ojha, Werth & Shirzaei (2019), JGR Solid Earth 124:3127-3143",
                "sensor": "ALOS L-band + Sentinel-1 C-band + GPS + GRACE",
                "period": "2007-2009 & Jan 2015-Sep 2016",
                "rate_cm_per_yr": "Up to -25.0 in Tule/Kaweah (~ -15.0 Chowchilla); ~ -30.0 to > -30.0 in southern Central Valley",
                "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6559157/",
            },
            {
                "source": "NASA NISAR StoryMap (Peacock et al. 2024) / JPL UAVSAR (Miller et al. 2020; Jones et al. 2020)",
                "sensor": "UAVSAR Airborne L-band",
                "period": "2013-2017",
                "rate_cm_per_yr": "Cumulative subsidence bowl > 100 cm (> 40 in) along California Aqueduct",
                "url": "https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828",
            },
        ],
    }
    (s1_out_dir / "cross_sensor.json").write_text(
        json.dumps(cross_sensor_out, indent=2), encoding="utf-8"
    )
    make_figure(gnss_eval, coh_data, cmr_status, fig_out)
    return cross_sensor_out


def main() -> None:
    parser = argparse.ArgumentParser(description="B1 Cross-sensor & multi-frequency InSAR evaluation.")
    parser.add_argument("--offline", action="store_true", help="Skip network queries and use verified CMR snapshot.")
    args = parser.parse_args()
    out = run_cross_sensor_analysis(offline=args.offline)
    m = out["nisar_vs_gnss_validation"]["terminal_vertical_metrics"]
    print(
        f"B1 cross-sensor complete | CMR summer2026 OPERA={out['cmr_opera_disp_s1']['opera_summer_2026_hits']} "
        f"(raw S1C={out['cmr_opera_disp_s1']['sentinel1c_slc_summer_2026_hits']}) | "
        f"GPS 10-station r={m['r']}, RMSE={m['rmse_cm']} cm, slope={m['slope']} | "
        f"Ag-core summer med coh={out['lband_coherence_25_pairs']['seasonal_summary']['summer_jun_oct']['mean_ag_core_median_coh']}"
    )


if __name__ == "__main__":
    main()
