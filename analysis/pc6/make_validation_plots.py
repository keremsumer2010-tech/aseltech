#!/usr/bin/env python3
"""Generate GNSS validation scatter plot, 10 per-station charts, and Markdown report."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

REPO_ROOT = Path(__file__).resolve().parents[2]
VAL_JSON = REPO_ROOT / "data" / "central_valley" / "validation.json"
MEDIA_ROOT = REPO_ROOT / "docs" / "story" / "media"
REPORT_MD = REPO_ROOT / "docs" / "story" / "validation_report.md"

MOVING_THRESHOLD_CM = 2.0


def load_validation(path: Path = VAL_JSON) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        rows = json.load(fh)
    # Sort descending by absolute GNSS final magnitude, then RMSE ascending
    rows.sort(key=lambda r: (-abs(float(r["gnss"][-1])), float(r["rmse_cm"])))
    return rows


def compute_summary_stats(rows: list[dict]) -> dict:
    gx = np.array([float(r["gnss"][-1]) for r in rows], dtype=float)
    iy = np.array([float(r["insar"][-1]) for r in rows], dtype=float)
    moving_mask = np.abs(gx) > MOVING_THRESHOLD_CM

    r_all = float(np.corrcoef(gx, iy)[0, 1])
    rmse_all = float(np.sqrt(np.mean((iy - gx) ** 2)))
    rmse_mov = float(np.sqrt(np.mean((iy[moving_mask] - gx[moving_mask]) ** 2)))
    rmse_stab = float(np.sqrt(np.mean((iy[~moving_mask] - gx[~moving_mask]) ** 2)))

    mean_ts_rmse_all = float(np.mean([float(r["rmse_cm"]) for r in rows]))
    mean_ts_rmse_mov = float(np.mean([float(r["rmse_cm"]) for r, m in zip(rows, moving_mask) if m]))
    mean_ts_r_mov = float(np.mean([float(r["corr"]) for r, m in zip(rows, moving_mask) if m]))
    mean_ts_rmse_stab = float(np.mean([float(r["rmse_cm"]) for r, m in zip(rows, moving_mask) if not m]))
    mean_ts_r_stab = float(np.mean([float(r["corr"]) for r, m in zip(rows, moving_mask) if not m]))

    slope, intercept = np.polyfit(gx, iy, 1)
    return {
        "n_total": len(rows),
        "n_moving": int(moving_mask.sum()),
        "n_stable": int((~moving_mask).sum()),
        "r_all": r_all,
        "rmse_final_all": rmse_all,
        "rmse_final_mov": rmse_mov,
        "rmse_final_stab": rmse_stab,
        "mean_ts_rmse_all": mean_ts_rmse_all,
        "mean_ts_rmse_mov": mean_ts_rmse_mov,
        "mean_ts_r_mov": mean_ts_r_mov,
        "mean_ts_rmse_stab": mean_ts_rmse_stab,
        "mean_ts_r_stab": mean_ts_r_stab,
        "slope": float(slope),
        "intercept": float(intercept),
        "moving_mask": moving_mask,
    }


def plot_scatter(rows: list[dict], stats: dict, out_path: Path) -> None:
    gx = np.array([float(r["gnss"][-1]) for r in rows], dtype=float)
    iy = np.array([float(r["insar"][-1]) for r in rows], dtype=float)
    moving = stats["moving_mask"]

    fig, ax = plt.subplots(figsize=(9.5, 7.6), dpi=160, facecolor="#ffffff")
    ax.set_facecolor("#f8fafc")

    lim_min = min(float(gx.min()), float(iy.min())) - 1.1
    lim_max = max(float(gx.max()), float(iy.max())) + 1.95
    xs_line = np.linspace(lim_min, lim_max, 200)

    # Shaded +-1.5 cm tolerance around 1:1
    ax.fill_between(xs_line, xs_line - 1.5, xs_line + 1.5, color="#cbd5e1", alpha=0.28, zorder=1, label="±1.5 cm envelope around 1:1")
    ax.plot(xs_line, xs_line, color="#0f172a", linestyle="--", linewidth=1.5, zorder=2, label="1:1 Perfect agreement (y = x)")
    ax.plot(
        xs_line,
        stats["slope"] * xs_line + stats["intercept"],
        color="#64748b",
        linestyle=":",
        linewidth=1.3,
        zorder=2,
        label=f"OLS fit (y = {stats['slope']:.2f}x {stats['intercept']:+.2f} cm)",
    )
    ax.axhline(0.0, color="#cbd5e1", linewidth=0.9, zorder=1)
    ax.axvline(0.0, color="#cbd5e1", linewidth=0.9, zorder=1)

    # Stable vs Moving points
    ax.scatter(
        gx[~moving],
        iy[~moving],
        s=115,
        marker="D",
        color="#0284c7",
        edgecolors="#0f172a",
        linewidths=1.0,
        zorder=4,
        label=f"Stable / low-signal (|GPS| ≤ 2 cm, n={stats['n_stable']})",
    )
    ax.scatter(
        gx[moving],
        iy[moving],
        s=140,
        marker="o",
        color="#dc2626",
        edgecolors="#0f172a",
        linewidths=1.0,
        zorder=5,
        label=f"Active subsiding (|GPS| > 2 cm, n={stats['n_moving']})",
    )

    # Hand-tuned clean label offsets in points with leader lines so zero labels touch
    label_offsets = {
        "TLBN": (14, -6),
        "CAHA": (-16, 10),
        "QCAP": (-14, 18),
        "HANF": (16, -12),
        "P056": (16, 4),
        "CAFP": (-16, -6),
        "CAD1": (-18, 12),
        "P565": (18, -16),
        "P564": (-18, 16),
        "P566": (16, 8),
    }
    for row, is_mov in zip(rows, moving):
        sta = row["station"]
        x_val = float(row["gnss"][-1])
        y_val = float(row["insar"][-1])
        dx, dy = label_offsets.get(sta, (8, 8))
        ha = "left" if dx >= 0 else "right"
        col = "#991b1b" if is_mov else "#075985"
        ax.annotate(
            f"{sta} ({x_val:+.2f}, {y_val:+.2f})",
            xy=(x_val, y_val),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=8.3,
            fontweight="bold",
            color=col,
            ha=ha,
            va="center",
            arrowprops=dict(arrowstyle="-", color=col, lw=0.8, shrinkA=0, shrinkB=4),
            bbox=dict(boxstyle="round,pad=0.22", facecolor="#ffffff", edgecolor=col, alpha=0.92, linewidth=0.75),
            zorder=6,
        )

    # Metrics summary box
    summary_text = (
        f"All {stats['n_total']} stations (final epoch {rows[0]['dates'][-1]}):\n"
        f"  Pearson r = {stats['r_all']:.3f}   |   Final RMSE = {stats['rmse_final_all']:.2f} cm   (TS mean RMSE = {stats['mean_ts_rmse_all']:.2f} cm)\n"
        f"Moving (|GPS| > 2 cm, n={stats['n_moving']}):  final RMSE = {stats['rmse_final_mov']:.2f} cm, mean TS r = {stats['mean_ts_r_mov']:.3f}\n"
        f"Stable (|GPS| ≤ 2 cm, n={stats['n_stable']}):  final RMSE = {stats['rmse_final_stab']:.2f} cm, mean TS r = {stats['mean_ts_r_stab']:.3f}"
    )
    ax.text(
        0.025,
        0.975,
        summary_text,
        transform=ax.transAxes,
        fontsize=8.8,
        family="DejaVu Sans",
        color="#0f172a",
        va="top",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#ffffff", edgecolor="#94a3b8", linewidth=1.0),
        zorder=7,
    )

    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, color="#e2e8f0", linestyle="--", linewidth=0.8, zorder=0)
    ax.set_xlabel("NGL GPS cumulative vertical displacement (cm, ref 2026-06-28)", fontsize=10.5, fontweight="bold", color="#0f172a")
    ax.set_ylabel("NISAR vertical estimate = LOS / cos(inc) (cm, ref 2026-06-28)", fontsize=10.5, fontweight="bold", color="#0f172a")
    ax.set_title(
        "Central Valley — NISAR Cumulative Vertical Estimate vs. GNSS Final Epoch (108 days)",
        fontsize=12.5,
        fontweight="bold",
        color="#0f172a",
        pad=12,
    )
    ax.legend(loc="lower right", fontsize=8.8, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")
    fig.text(
        0.5,
        0.014,
        "NASA-ISRO NISAR · PROVISIONAL — Calibration & validation are carried out by NASA-JPL and ISRO, not by our team.",
        ha="center",
        fontsize=8.3,
        color="#475569",
        style="italic",
    )
    fig.tight_layout(rect=[0, 0.035, 1, 1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_station_series(row: dict, out_path: Path) -> None:
    sta = row["station"]
    dates = row["dates"]
    d0 = datetime.strptime(dates[0], "%Y-%m-%d")
    x_days = np.array([(datetime.strptime(d, "%Y-%m-%d") - d0).days for d in dates], dtype=float)
    gnss = np.asarray(row["gnss"], dtype=float)
    insar = np.asarray(row["insar"], dtype=float)
    is_moving = abs(gnss[-1]) > MOVING_THRESHOLD_CM

    fig, ax = plt.subplots(figsize=(7.6, 4.3), dpi=150, facecolor="#ffffff")
    ax.set_facecolor("#f8fafc")

    ax.axhline(0.0, color="#94a3b8", linestyle="--", linewidth=0.9, zorder=1)
    ax.fill_between(x_days, gnss, insar, color="#64748b", alpha=0.12, zorder=2, label="InSAR − GNSS gap")
    ax.plot(
        x_days,
        gnss,
        marker="o",
        markersize=5.8,
        linewidth=2.2,
        color="#0284c7",
        zorder=4,
        label=f"NGL GPS Vertical (final: {gnss[-1]:+.2f} cm)",
    )
    ax.plot(
        x_days,
        insar,
        marker="s",
        markersize=5.4,
        linewidth=2.2,
        color="#dc2626",
        zorder=5,
        label=f"NISAR Vertical Est. (final: {insar[-1]:+.2f} cm)",
    )

    badge_text = "MOVING (|GPS| > 2 cm)" if is_moving else "STABLE (|GPS| ≤ 2 cm)"
    badge_bg = "#fee2e2" if is_moving else "#e0f2fe"
    badge_fg = "#991b1b" if is_moving else "#075985"
    ax.text(
        0.985,
        0.95,
        f"{badge_text}\nr = {float(row['corr']):+.3f}  |  RMSE = {float(row['rmse_cm']):.2f} cm",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8.8,
        fontweight="bold",
        color=badge_fg,
        bbox=dict(boxstyle="round,pad=0.35", facecolor=badge_bg, edgecolor=badge_fg, linewidth=0.9),
        zorder=6,
    )

    ax.set_xticks(x_days)
    ax.set_xticklabels([d[5:] for d in dates], fontsize=8.5)
    all_v = np.concatenate([gnss, insar, np.array([0.0])])
    pad = max(0.8, 0.18 * (float(all_v.max()) - float(all_v.min())))
    ax.set_ylim(float(all_v.min()) - pad, float(all_v.max()) + pad + 0.5)
    ax.grid(True, color="#e2e8f0", linestyle="--", linewidth=0.75, zorder=0)
    ax.set_xlabel(f"Observation date in 2026 (baseline {dates[0]} = 0.00 cm)", fontsize=9.2, color="#334155")
    ax.set_ylabel("Vertical displacement (cm)", fontsize=9.2, color="#334155")
    ax.set_title(
        f"Station {sta} ({row['lat']:.3f}°N, {abs(row['lon']):.3f}°W)  ·  Incidence {row['incidence_deg']:.2f}°",
        fontsize=11,
        fontweight="bold",
        color="#0f172a",
        pad=9,
    )
    ax.legend(loc="lower left", fontsize=8.4, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")
    fig.text(
        0.5,
        0.015,
        "NISAR data are provisional (NASA-JPL/ISRO Cal/Val). GPS from Nevada Geodetic Laboratory.",
        ha="center",
        fontsize=7.8,
        color="#64748b",
        style="italic",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def write_report(rows: list[dict], stats: dict, out_md: Path) -> None:
    moving_names = ", ".join(r["station"] for r in rows if abs(float(r["gnss"][-1])) > MOVING_THRESHOLD_CM)
    stable_names = ", ".join(r["station"] for r in rows if abs(float(r["gnss"][-1])) <= MOVING_THRESHOLD_CM)

    lines: list[str] = [
        "# NISAR vs. GNSS Validation Report — Central Valley, California",
        "",
        "> **Provisional Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.",
        "",
        f"**Period:** `{rows[0]['dates'][0]}` → `{rows[0]['dates'][-1]}` (8 epochs, 108 days)  ",
        f"**Stations evaluated:** `{stats['n_total']}` NGL continuous GPS stations inside the valid NISAR Track 34 Ascending footprint  ",
        f"**Component compared:** NISAR vertical estimate (`LOS / cos(incidence)`) vs. 7-day-window median NGL vertical GPS, both zeroed on `{rows[0]['dates'][0]}`.",
        "",
        "---",
        "",
        "## 1. Final-Epoch Cross-Station Scatter",
        "",
        "![NISAR vs GNSS Final Epoch Scatter](media/validation_scatter.png)",
        "",
        f"- **All {stats['n_total']} stations (final epoch `{rows[0]['dates'][-1]}`):** cross-station Pearson **`r = {stats['r_all']:.3f}`**, final-epoch **`RMSE = {stats['rmse_final_all']:.2f} cm`** (mean time-series RMSE = `{stats['mean_ts_rmse_all']:.2f} cm`).",
        f"- **Active moving stations (`|GPS| > 2.0 cm`, `n = {stats['n_moving']}` — `{moving_names}`):** final-epoch **`RMSE = {stats['rmse_final_mov']:.2f} cm`**, mean time-series RMSE = `{stats['mean_ts_rmse_mov']:.2f} cm`, mean temporal **`r = {stats['mean_ts_r_mov']:.3f}`**.",
        f"- **Stable / valley-margin stations (`|GPS| <= 2.0 cm`, `n = {stats['n_stable']}` — `{stable_names}`):** final-epoch **`RMSE = {stats['rmse_final_stab']:.2f} cm`**, mean time-series RMSE = `{stats['mean_ts_rmse_stab']:.2f} cm`, mean temporal **`r = {stats['mean_ts_r_stab']:.3f}`**.",
        "",
        "## 2. Scientific Interpretation (Moving vs. Stable Stations)",
        "",
        (
            f"Active subsiding stations inside the San Joaquin groundwater bowl ({moving_names}) accumulate "
            f"-2.22 cm to -4.45 cm of vertical compaction over 108 days, placing their deformation signal cleanly above "
            f"unmodeled L-band propagation noise and yielding high temporal correlations (r = 0.793 to 0.896) with "
            f"sub-centimeter to ~1.2 cm time-series RMSE. "
            f"In contrast, stable and valley-margin stations (|GPS| ≤ 2.0 cm) experience small real ground motion (-1.45 cm "
            f"to +0.19 cm) that falls below the residual tropospheric water-vapor noise floor (~1–3 cm per pair, because "
            f"external weather-model troposphere and solid-earth-tide screens were not subtracted in these provisional products). "
            f"When the true physical displacement amplitude is smaller than the atmospheric noise variance, temporal Pearson "
            f"correlation degrades toward zero or turns negative (r = -0.410 to +0.661) even though absolute errors stay "
            f"bounded around 0.6–2.0 cm. "
            f"Additionally, planar plus elevation-linear deramping anchored to the northeastern reference window (-119.1456°E, "
            f"36.4532°N) leaves a +1.2 to +1.9 cm apparent positive offset across far-field margin stations (P564, P566, P565, CAD1). "
            f"Overall, the strong 10-station cross-sectional fit (r = {stats['r_all']:.3f}, final RMSE = {stats['rmse_final_all']:.2f} cm) "
            f"confirms that NISAR reliably captures active subsidence magnitude while temporal tracking is physically diagnostic "
            f"above ~2 cm of cumulative vertical motion."
        ),
        "",
        "## 3. Per-Station Metrics Summary",
        "",
        "| Station | Regime | Lat / Lon | Incidence (°) | GPS Final (cm) | NISAR Est. Final (cm) | Time-Series RMSE (cm) | Time-Series r | Plot |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for row in rows:
        sta = row["station"]
        g_fin = float(row["gnss"][-1])
        i_fin = float(row["insar"][-1])
        regime = "Moving (`|GPS| > 2 cm`)" if abs(g_fin) > MOVING_THRESHOLD_CM else "Stable (`|GPS| <= 2 cm`)"
        lines.append(
            f"| **{sta}** | {regime} | {row['lat']:.3f}°N, {abs(row['lon']):.3f}°W | "
            f"{row['incidence_deg']:.2f} | {g_fin:+.2f} | {i_fin:+.2f} | "
            f"{float(row['rmse_cm']):.2f} | {float(row['corr']):+.3f} | "
            f"[gnss_{sta}.png](media/gnss_{sta}.png) |"
        )

    lines.extend(["", "## 4. Individual Station Time-Series Plots", ""])
    for row in rows:
        sta = row["station"]
        lines.extend(
            [
                f"### {sta}",
                "",
                f"![Station {sta} NISAR vs GNSS](media/gnss_{sta}.png)",
                "",
            ]
        )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    with out_md.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines).rstrip() + "\n")


def main() -> int:
    rows = load_validation()
    stats = compute_summary_stats(rows)
    plot_scatter(rows, stats, MEDIA_ROOT / "validation_scatter.png")
    for row in rows:
        plot_station_series(row, MEDIA_ROOT / f"gnss_{row['station']}.png")
    write_report(rows, stats, REPORT_MD)
    print(
        f"[OK] Wrote {REPORT_MD.relative_to(REPO_ROOT)}, validation_scatter.png, and {len(rows)} station charts "
        f"(all r={stats['r_all']:.3f}, final_rmse={stats['rmse_final_all']:.2f} cm)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
