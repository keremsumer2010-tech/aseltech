#!/usr/bin/env python3
"""Generate infrastructure subsidence profile plots (risk_1..10.png) and risk_dossier.md."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from risk.compute_risk import (  # noqa: E402
    BLOCK_RADIUS_M,
    MIN_SPAN_M,
    densify_utm_line,
    make_batch_projector,
    sample_block_median,
)

ASSETS_JSON = REPO_ROOT / "data" / "central_valley" / "assets.json"
CUM_NPZ = REPO_ROOT / "analysis" / "out" / "central_valley_cum.npz"
MEDIA_ROOT = REPO_ROOT / "docs" / "story" / "media"
DOSSIER_MD = REPO_ROOT / "docs" / "story" / "risk_dossier.md"


def extract_segment_profile(
    feat: dict,
    cum_grid: np.ndarray,
    x_axis: np.ndarray,
    y_axis: np.ndarray,
    epsg: int,
    proj_fn,
) -> dict:
    coords = feat["geometry"]["coordinates"]
    lons = np.array([c[0] for c in coords], dtype=np.float64)
    lats = np.array([c[1] for c in coords], dtype=np.float64)
    px, py = proj_fn(lons, lats, epsg)
    sx, sy, dist_m = densify_utm_line(px, py)
    vals = sample_block_median(cum_grid, x_axis, y_axis, sx, sy, radius_m=BLOCK_RADIUS_M)

    valid_mask = np.isfinite(vals)
    valid_idx = np.where(valid_mask)[0]
    best_grad = 0.0
    bi, bj = 0, 0
    for a_pos in range(len(valid_idx)):
        i = int(valid_idx[a_pos])
        for b_pos in range(a_pos + 1, len(valid_idx)):
            j = int(valid_idx[b_pos])
            span = float(dist_m[j] - dist_m[i])
            if span >= MIN_SPAN_M:
                grad = abs(float(vals[j] - vals[i])) * 10.0 / (span / 1000.0)
                if grad > best_grad:
                    best_grad = grad
                    bi, bj = i, j

    min_valid_pos = int(valid_idx[int(np.argmin(vals[valid_idx]))])
    return {
        "dist_km": dist_m / 1000.0,
        "vals_cm": vals,
        "valid_mask": valid_mask,
        "grad_i": bi,
        "grad_j": bj,
        "calc_grad_mm_km": best_grad,
        "min_idx": min_valid_pos,
        "total_km": float(dist_m[-1] / 1000.0),
    }


def plot_profile(rank: int, feat: dict, prof: dict, period: list[str], out_path: Path) -> None:
    props = feat["properties"]
    dist_km = prof["dist_km"]
    vals_cm = prof["vals_cm"]
    valid = prof["valid_mask"]
    gi, gj = prof["grad_i"], prof["grad_j"]
    mi = prof["min_idx"]

    is_major_canal = props.get("type") == "canal" or "aqueduct" in str(props.get("name", "")).lower()
    line_col = "#0284c7" if is_major_canal else "#dc2626"

    fig, ax = plt.subplots(figsize=(8.6, 4.3), dpi=160, facecolor="#ffffff")
    ax.set_facecolor("#f8fafc")

    ax.axhline(0.0, color="#94a3b8", linestyle="--", linewidth=0.9, zorder=1)

    # Shaded peak differential gradient window (>= 1 km span)
    d0, d1 = float(dist_km[gi]), float(dist_km[gj])
    ax.axvspan(d0, d1, color="#fef3c7", alpha=0.85, zorder=1, label=f"Peak gradient span ({d0:.2f}–{d1:.2f} km: {props['gradient_mm_per_km']:.2f} mm/km)")

    # Plot masked values cleanly (Matplotlib breaks lines automatically across NaNs)
    ax.plot(
        dist_km,
        vals_cm,
        color=line_col,
        linewidth=2.3,
        zorder=3,
        label=f"Block-median NISAR LOS ({int(valid.sum())}/{len(vals_cm)} valid samples)",
    )
    ax.fill_between(
        dist_km,
        0.0,
        vals_cm,
        where=valid & (vals_cm < 0.0),
        color=line_col,
        alpha=0.14,
        interpolate=False,
        zorder=2,
    )

    # Highlight shear endpoints and peak subsidence point
    ax.plot(
        [d0, d1],
        [vals_cm[gi], vals_cm[gj]],
        color="#d97706",
        marker="o",
        markersize=6.0,
        linewidth=1.8,
        linestyle="-",
        zorder=5,
        label=f"Shear change: {vals_cm[gi]:+.2f} → {vals_cm[gj]:+.2f} cm",
    )
    ax.scatter(
        [dist_km[mi]],
        [vals_cm[mi]],
        s=110,
        marker="*",
        color="#991b1b",
        edgecolors="#ffffff",
        linewidths=0.8,
        zorder=6,
        label=f"Max subsidence: {vals_cm[mi]:+.2f} cm at km {dist_km[mi]:.2f}",
    )

    finite_vals = vals_cm[valid]
    span_y = max(2.0, float(finite_vals.max()) - float(finite_vals.min()))
    y_min = min(-1.8, float(finite_vals.min()) - 0.38 * span_y - 0.8)
    y_max = max(1.2, float(finite_vals.max()) + 0.16 * span_y + 0.4)
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(-0.02 * prof["total_km"], 1.02 * prof["total_km"])

    ax.grid(True, color="#e2e8f0", linestyle="--", linewidth=0.75, zorder=0)
    ax.set_xlabel("Distance along asset segment (km)", fontsize=9.5, fontweight="bold", color="#0f172a")
    ax.set_ylabel("Cumulative LOS displacement (cm)", fontsize=9.5, fontweight="bold", color="#0f172a")

    asset_badge = "MAJOR CANAL" if is_major_canal else str(props.get("type", "asset")).upper()
    ax.set_title(
        f"#{rank} {props['name']} [{asset_badge} · {props['length_km']:.2f} km]\n"
        f"Peak Gradient: {props['gradient_mm_per_km']:.2f} mm/km  ·  Max LOS Subsidence: {props['max_cm']:.2f} cm",
        fontsize=10.2,
        fontweight="bold",
        color="#0f172a",
        pad=10,
    )
    ax.legend(loc="lower left", fontsize=8.0, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", ncol=2)

    fig.text(
        0.5,
        0.015,
        f"Period {period[0]} → {period[1]} | 480 m block-median LOS | NASA-ISRO NISAR PROVISIONAL (JPL/ISRO Cal/Val)",
        ha="center",
        fontsize=7.8,
        color="#64748b",
        style="italic",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def write_dossier(assets_data: dict, profiles: list[tuple[int, dict, dict]], out_md: Path) -> None:
    summary = assets_data["summary"]
    period = summary["period"]
    thresholds = summary["thresholds"]

    lines: list[str] = [
        "# Infrastructure Subsidence Risk Dossier — Central Valley Top 10 Segments",
        "",
        "> **Provisional Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.",
        "",
        f"**Observation Window:** `{period[0]}` → `{period[1]}` (Track 34 Ascending, Frame 20, 108 days)  ",
        f"**Asset Screening:** `{summary['evaluated_segments']}` evaluated OpenStreetMap segments (`{summary['total_features_in_geojson']}` total mapped) — **`{summary['high_risk_count']}` high risk**, `{summary['medium_risk_count']}` medium risk, `{summary['low_risk_count']}` low risk  ",
        f"**High-Risk Thresholds:** Differential LOS gradient ≥ `{thresholds['high_gradient_mm_per_km']} mm/km` over ≥ `{int(thresholds['min_span_m'])} m` OR max subsidence ≥ `{thresholds['high_subsidence_cm']} cm` (`480 m` spatial block median along `200 m`-densified centerlines).",
        "",
        "---",
        "",
        "## 1. What This Means for Conveyance & Linear Infrastructure",
        "",
        (
            "Steep subsidence gradients of **44–57 mm/km** measured over just 108 days show localized, uneven ground flexure "
            "that warps gravity-fed canal inverts, cracks concrete linings, and reduces bridge clearance far more severely than "
            "uniform basin-wide sinking. As documented on the **Friant-Kern Canal** near Terra Bella (where the Middle Reach "
            "Capacity Correction Project / Friant Water Authority and KVPR 2017 report over **60% conveyance capacity loss**, "
            "from ~4,000 cfs design flow down to ~1,600 cfs in the worst reach, requiring over USD 300M remediation), differential "
            "compaction directly bottlenecks California's water delivery corridors as well as rail tracks and highways."
        ),
        "",
        "## 2. Spotlight: California Aqueduct & Major Irrigation Canals",
        "",
        "Five of the Top 10 highest-gradient segments across the entire San Joaquin footprint are water-conveyance canals:",
        "",
        "- **#1 Tulare Irrigation District Canal (`canal`, `2.17 km`, `57.01 mm/km`, max `-6.75 cm`):** Highest differential shear rate in the footprint, transitioning sharply across a 1.08 km span (`0.60 → 1.68 km`).",
        "- **#4 California Aqueduct (`canal`, `102.82 km`, `49.12 mm/km`, max `-7.42 cm` LOS / `~-9.6 cm` vertical estimate):** State Water Project's flagship arterial aqueduct exhibits multiple deep bowls and a `49.12 mm/km` shear transition near `65.6–66.7 km` along the evaluated corridor. This directly extends NASA's airborne L-band UAVSAR monitoring highlighted in the official **NASA NISAR Land Subsidence StoryMap** ([Peacock et al. 2024](https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828); [Zenodo DOI: 10.5281/zenodo.10818833](https://doi.org/10.5281/zenodo.10818833)), where UAVSAR measured **over 40 inches (`>100 cm`, or `~20–25 cm/yr`)** of cumulative sinking along the California Aqueduct between 2013 and 2017 (Miller et al. 2020; Jones et al. 2020). Our 2026 spaceborne NISAR 108-day peak of `-7.42 cm` LOS (`~-25.1 cm/yr` annualized summer rate estimate) is of the same order of magnitude, showing that drought-era compaction along the aqueduct remains active in 2026.",
        "- **#5 Alta East Branch Canal (`canal`, `6.68 km`, `48.10 mm/km`, max `-6.87 cm`):** East-side irrigation feeder experiencing steep differential settling toward the Tulare/Visalia sub-basin.",
        "- **#7 & #9 Friant-Kern Canal (`canal`, `1.54 km` & `2.09 km`, `46.06` & `44.47 mm/km`, max `-4.51` & `-5.92 cm`):** Two distinct reaches of the federal canal register Top-10 gradients directly matching historically impacted conveyance segments near Terra Bella / Porterville.",
        "",
        "*(Rail and highway lifelines round out the list: **Exeter Subdivision** `#2` at `55.61 mm/km` and `#3` reaching `-7.80 cm` valley-wide peak LOS, **Porterville Subdivision** `#6` at `47.85 mm/km`, and **CA 65** `#10` at `42.34 mm/km`.)*",
        "",
        "### 2.1 Comparison: 2026 Spaceborne NISAR vs. 2013–2017 Airborne NASA UAVSAR along the California Aqueduct",
        "",
        "| Metric | NASA Airborne UAVSAR (2013–2017) | 2026 Spaceborne NISAR (Track 34 Asc, Provisional) | Physical & Operational Comparison |",
        "| :--- | :--- | :--- | :--- |",
        "| **Sensor & Wavelength** | Airborne L-band SAR (`~24 cm`, UAVSAR) | Spaceborne L-band SAR (`24.2 cm`, NISAR L2 GUNW) | Same L-band wavelength; spaceborne 12-day repeat covers the full valley simultaneously |",
        "| **Observation Period** | `2013–2017` (~4.5 years, multi-year drought) | `2026-06-28` → `2026-10-14` (`108 days`, 1 irrigation season) | Single summer season captures peak agricultural pumping drawdown |",
        "| **California Aqueduct Peak Sinking** | `> 40 inches` (`> 101.6 cm` cumulative; `~20–25 cm/yr`) | `-7.42 cm` LOS (`~-9.6 cm` vertical *estimate* in 108 d; `~-25.1 cm/yr` LOS annualized *estimate*) | Same order of magnitude (`~20–25 cm/yr` during active summer pumping) |",
        "| **Peak Differential Tilt** | Localized subsidence bowls warping concrete canal linings | `49.12 mm/km` over `1.03 km` (`km 65.62` to `km 66.65`: `-1.34` → `-6.40 cm` LOS) | Pinpoints the exact 1 km shear transition requiring liner and freeboard inspection |",
        "| **Primary Reference** | [NASA NISAR StoryMap](https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828) ([Peacock et al. 2024](https://doi.org/10.5281/zenodo.10818833)); Miller et al. (2020); Jones et al. (2020) | `data/central_valley/assets.json` (`osm_id=24016778`, [risk_4.png](media/risk_4.png)) | Demonstrates how spaceborne NISAR operationalizes NASA's StoryMap decision-support vision in 2026 |",
        "",
        "## 3. Top 10 High-Risk Segments Summary Table",
        "",
        "| Rank | Segment Name | Type | Length (km) | Peak Gradient (mm/km) | Max Subsidence (cm) | OSM ID | Profile Chart |",
        "| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    for rank, feat, _prof in profiles:
        p = feat["properties"]
        tag = " **(Major Canal)**" if p["type"] == "canal" else ""
        lines.append(
            f"| **{rank}** | {p['name']}{tag} | `{p['type']}` | {p['length_km']:.2f} | "
            f"**{p['gradient_mm_per_km']:.2f}** | {p['max_cm']:.2f} | `{p['osm_id']}` | "
            f"[risk_{rank}.png](media/risk_{rank}.png) |"
        )

    lines.extend(["", "## 4. Individual Distance–Displacement Profile Charts", ""])
    for rank, feat, prof in profiles:
        p = feat["properties"]
        gi, gj = prof["grad_i"], prof["grad_j"]
        d0, d1 = float(prof["dist_km"][gi]), float(prof["dist_km"][gj])
        v0, v1 = float(prof["vals_cm"][gi]), float(prof["vals_cm"][gj])
        lines.extend(
            [
                f"### #{rank} — {p['name']} (`{p['type']}`)",
                "",
                f"- **Length:** `{p['length_km']:.2f} km` | **Peak Differential Gradient:** `{p['gradient_mm_per_km']:.2f} mm/km` (between `km {d0:.2f}` at `{v0:+.2f} cm` and `km {d1:.2f}` at `{v1:+.2f} cm`) | **Max LOS Subsidence:** `{p['max_cm']:.2f} cm`",
                "",
                f"![Rank {rank} {p['name']} subsidence profile](media/risk_{rank}.png)",
                "",
            ]
        )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    with out_md.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines).rstrip() + "\n")


def main() -> int:
    with ASSETS_JSON.open(encoding="utf-8") as fh:
        assets_data = json.load(fh)
    with np.load(CUM_NPZ) as z:
        cum_grid = np.array(z["cum_cm"], dtype=np.float32)
        x_axis = np.array(z["x"], dtype=np.float64)
        y_axis = np.array(z["y"], dtype=np.float64)
        epsg = int(z["epsg"])

    proj_fn = make_batch_projector(epsg)
    period = assets_data["summary"]["period"]
    top_feats = assets_data["features"][:10]

    profiles: list[tuple[int, dict, dict]] = []
    for rank, feat in enumerate(top_feats, 1):
        prof = extract_segment_profile(feat, cum_grid, x_axis, y_axis, epsg, proj_fn)
        plot_profile(rank, feat, prof, period, MEDIA_ROOT / f"risk_{rank}.png")
        profiles.append((rank, feat, prof))

    write_dossier(assets_data, profiles, DOSSIER_MD)
    print(f"[OK] Wrote {DOSSIER_MD.relative_to(REPO_ROOT)} and {len(profiles)} risk profile PNGs (risk_1..{len(profiles)}.png)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
