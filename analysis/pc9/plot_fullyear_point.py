"""Plot the 11-month Central Valley displacement & decomposition figure (PC9, Task 3).

Reads:
  data/central_valley_fullyear/points.json
  data/central_valley_fullyear/decomp.json
  data/central_valley_fullyear/summary.json
Writes:
  docs/story/media/pc9_fullyear_point.png
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "decomp"))
import decompose  # noqa: E402


def _fit_point(dates_iso: list[str], values: list[float]):
    t = np.array([decompose.decimal_year(d) for d in dates_iso], dtype=np.float64)
    y = np.asarray(values, dtype=np.float64)
    res = decompose.fit(t, y[:, None])
    t0 = float(res["t0"])
    G = np.stack([np.ones_like(t), t - t0, np.sin(2.0 * np.pi * t), np.cos(2.0 * np.pi * t)], axis=1)
    coef, *_ = np.linalg.lstsq(G, y, rcond=None)
    return t, t0, y, coef, float(res["amp_cm"][0]), float(res["r2"][0]), int(res["low_month"][0])


def main() -> None:
    data_dir = ROOT / "data" / "central_valley_fullyear"
    pts = json.loads((data_dir / "points.json").read_text(encoding="utf-8"))
    decomp = json.loads((data_dir / "decomp.json").read_text(encoding="utf-8"))
    summ = json.loads((data_dir / "summary.json").read_text(encoding="utf-8"))

    p1 = next(p for p in pts if p["id"] == "p01")
    p6 = next(p for p in pts if p["id"] == "p06")
    p11 = next(p for p in pts if p["id"] == "p11")

    dates_iso = p1["dates"]
    dt_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates_iso]
    split_date = "2026-06-28"
    split_idx = dates_iso.index(split_date)
    split_dt = dt_objs[split_idx]

    t, t0, y1, coef1, amp1, r2_1, _ = _fit_point(dates_iso, p1["disp_cm"])
    _, t0_6, y6, coef6, amp6, r2_6, _ = _fit_point(dates_iso, p6["disp_cm"])
    _, _, y11, _, _, _, _ = _fit_point(dates_iso, p11["disp_cm"])

    a1, v1, A1, B1 = coef1
    days_span = (date.fromisoformat(dates_iso[-1]) - date.fromisoformat(dates_iso[0])).days
    perm_324d = v1 * (days_span / 365.25)
    p2p_1 = 2.0 * amp1

    # Smooth model curves evaluated cleanly across full window
    t_dense = np.linspace(t[0], t[-1], 400)
    dt_dense = [
        datetime(2025, 11, 24) + (dt_objs[-1] - datetime(2025, 11, 24)) * f
        for f in np.linspace(0.0, 1.0, 400)
    ]
    y_model_dense = a1 + v1 * (t_dense - t0) + A1 * np.sin(2.0 * np.pi * t_dense) + B1 * np.cos(2.0 * np.pi * t_dense)
    y_trend_dense = a1 + v1 * (t_dense - t0)
    y_trend_at_pts = a1 + v1 * (t - t0)
    seasonal_resid_1 = y1 - y_trend_at_pts
    seasonal_model_dense = A1 * np.sin(2.0 * np.pi * t_dense) + B1 * np.cos(2.0 * np.pi * t_dense)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.edgecolor": "#cbd5e1",
        "axes.linewidth": 0.9,
    })

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(11.5, 7.6),
        sharex=True,
        gridspec_kw={"height_ratios": [2.25, 1.05], "hspace": 0.14},
    )
    fig.patch.set_facecolor("#ffffff")

    # ---- Top Panel: Observed 11-month cumulative series + Beta dashed vs Provisional solid + fit ----
    ax1.set_facecolor("#ffffff")
    ax1.axvspan(dt_objs[0], split_dt, color="#fef3c7", alpha=0.42, zorder=0)
    ax1.axvspan(split_dt, dt_objs[-1], color="#f8fafc", alpha=0.9, zorder=0)
    ax1.axvline(split_dt, color="#64748b", linestyle="--", linewidth=1.15, alpha=0.8, zorder=2)
    ax1.axhline(0.0, color="#94a3b8", linewidth=0.9, zorder=1)
    ax1.grid(axis="y", color="#e2e8f0", linewidth=0.7, zorder=0)

    # Trend + harmonic model
    ax1.plot(
        dt_dense, y_trend_dense,
        color="#334155", linestyle=":", linewidth=1.8,
        label=f"Permanent linear trend: {v1:.1f} cm/yr LOS ({perm_324d:.1f} cm over {days_span} d)",
        zorder=3,
    )
    ax1.plot(
        dt_dense, y_model_dense,
        color="#0f766e", linestyle="-", linewidth=1.7, alpha=0.9,
        label=f"Permanent + annual sine fit (R² = {r2_1:.2f}, amp = {amp1:.1f} cm)",
        zorder=3,
    )

    # Observed data: Beta pre-calibration dashed vs Provisional solid
    ax1.plot(
        dt_objs[: split_idx + 1], y1[: split_idx + 1],
        color="#c2410c", linestyle="--", linewidth=2.2,
        marker="o", markersize=5.2, markerfacecolor="#ffffff", markeredgewidth=1.6,
        label="Beta-precal (18 pairs, 24 Nov 2025 – 28 Jun 2026) [dashed]",
        zorder=5,
    )
    ax1.plot(
        dt_objs[split_idx:], y1[split_idx:],
        color="#991b1b", linestyle="-", linewidth=2.6,
        marker="o", markersize=5.8, markerfacecolor="#991b1b", markeredgewidth=1.0,
        label="Provisional CRID P05023 (7 pairs, 28 Jun – 14 Oct 2026) [solid]",
        zorder=6,
    )

    # Control points for contrast (reference foothills)
    ax1.plot(
        dt_objs, y11,
        color="#64748b", linestyle="-", linewidth=1.1, alpha=0.8,
        label="Near-reference control (Woodlake, p11)",
        zorder=4,
    )

    # Regime banners at top of ax1
    ax1.text(
        datetime(2026, 3, 10), 4.6,
        "BETA PRE-CALIBRATION PERIOD\n18 pairs (before 17 Jun transition; treat amplitudes with caution)",
        ha="center", va="top", fontsize=8.5, fontweight="bold", color="#92400e",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#fef9c3", "edgecolor": "#f59e0b", "alpha": 0.92},
    )
    ax1.text(
        datetime(2026, 8, 22), 4.6,
        "PROVISIONAL PERIOD\n7 pairs (calibrated P05023)",
        ha="center", va="top", fontsize=8.5, fontweight="bold", color="#1e293b",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#e0f2fe", "edgecolor": "#0284c7", "alpha": 0.92},
    )

    # Event annotations
    imax = int(np.argmax(y1))
    ax1.annotate(
        f"Winter uplift peak\n+{y1[imax]:.1f} cm ({dates_iso[imax][5:]})",
        xy=(dt_objs[imax], y1[imax]),
        xytext=(datetime(2026, 2, 12), -6.2),
        fontsize=8.6, color="#1e293b", ha="center",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "#ffffff", "edgecolor": "#cbd5e1", "alpha": 0.92},
        arrowprops={"arrowstyle": "->", "color": "#475569", "lw": 1.0},
        zorder=7,
    )
    ax1.annotate(
        f"End of 11-month series: {y1[-1]:.1f} cm LOS\n({summ['max_subsidence_vertical_cm_estimate']:.1f} cm vertical est. at {summ['incidence_deg_at_max']:.1f}° inc.)",
        xy=(dt_objs[-1], y1[-1]),
        xytext=(datetime(2026, 7, 10), -23.2),
        fontsize=8.6, fontweight="bold", color="#7f1d1d", ha="right",
        arrowprops={"arrowstyle": "->", "color": "#991b1b", "lw": 1.1},
    )

    # Summary callout box inside top-left lower whitespace
    ratio = abs(perm_324d) / p2p_1
    perm_share = abs(perm_324d) / (abs(perm_324d) + p2p_1) * 100.0
    box_text = (
        f"Earlimart peak (p01, 324 days):\n"
        f"• Permanent compaction: {perm_324d:.1f} cm ({v1:.1f} cm/yr LOS)\n"
        f"• Recoverable seasonal wave: {p2p_1:.1f} cm peak-to-peak (±{amp1:.1f} cm)\n"
        f"• Permanent / seasonal swing: {ratio:.2f}:1 ({perm_share:.0f}% permanent share)"
    )
    ax1.text(
        0.015, 0.06, box_text,
        transform=ax1.transAxes, fontsize=8.6, va="bottom", ha="left", color="#0f172a",
        bbox={"boxstyle": "round,pad=0.45", "facecolor": "#ffffff", "edgecolor": "#cbd5e1", "alpha": 0.95},
        zorder=7,
    )

    ax1.set_ylim(-25.5, 6.2)
    ax1.set_ylabel("Cumulative LOS displacement (cm)", fontweight="bold", color="#0f172a")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="center left", bbox_to_anchor=(0.01, 0.42), frameon=True, facecolor="#ffffff",
               edgecolor="#cbd5e1", fontsize=8.2)
    ax1.set_title(
        f"Central Valley Full-Year Ground Motion ({p1['name']}): Winter Rebound and Summer Compaction",
        loc="left", fontsize=12.5, fontweight="bold", color="#0f172a", pad=10,
    )

    # ---- Bottom Panel: Detrended Recoverable Seasonal Dance ("Earth breathing") ----
    ax2.set_facecolor("#ffffff")
    ax2.axvspan(dt_objs[0], split_dt, color="#fef3c7", alpha=0.42, zorder=0)
    ax2.axvspan(split_dt, dt_objs[-1], color="#f8fafc", alpha=0.9, zorder=0)
    ax2.axvline(split_dt, color="#64748b", linestyle="--", linewidth=1.15, alpha=0.8, zorder=2)
    ax2.axhline(0.0, color="#94a3b8", linewidth=0.9, zorder=1)
    ax2.grid(axis="y", color="#e2e8f0", linewidth=0.7, zorder=0)

    ax2.plot(
        dt_dense, seasonal_model_dense,
        color="#0f766e", linewidth=1.9,
        label=f"Annual sinusoid at p01 (peak-to-peak {p2p_1:.1f} cm; August trough)",
        zorder=3,
    )
    ax2.plot(
        dt_objs[: split_idx + 1], seasonal_resid_1[: split_idx + 1],
        color="#c2410c", linestyle="--", linewidth=1.5, marker="o", markersize=4.2,
        markerfacecolor="#ffffff", zorder=4,
    )
    ax2.plot(
        dt_objs[split_idx:], seasonal_resid_1[split_idx:],
        color="#991b1b", linestyle="-", linewidth=1.8, marker="o", markersize=4.5,
        markerfacecolor="#991b1b", zorder=5,
    )
    # Show valley-floor Delano median point detrended for contrast
    y6_trend = coef6[0] + coef6[1] * (t - t0_6)
    ax2.plot(
        dt_objs, y6 - y6_trend,
        color="#1d4ed8", linestyle="-", linewidth=1.3, alpha=0.85,
        label=f"Valley median example ({p6['name']}: perm {coef6[1]:.1f} cm/yr, amp {amp6:.1f} cm)",
        zorder=4,
    )

    ax2.set_ylim(-9.0, 10.2)
    ax2.set_ylabel("Detrended seasonal (cm)", fontweight="bold", color="#0f172a")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="lower left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.2)
    ax2.set_title(
        "Isolated Elastic Seasonal Cycle (Observed minus Permanent Linear Trend)",
        loc="left", fontsize=10.2, fontweight="bold", color="#334155", pad=5,
    )

    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax2.get_xticklabels(), rotation=25, ha="right", fontsize=8.8)

    fig.text(
        0.065, 0.015,
        "Data: NASA-ISRO NISAR L2 GUNW (quality: mixed — 18 beta-precal pairs + 7 provisional pairs, CRID P05023), ASF DAAC. "
        "Analysis: Team Taykut.\nNISAR data are provisional (pre-2026-06-17 pairs are pre-calibration beta). Calibration and validation "
        "are carried out by NASA-JPL and ISRO.",
        fontsize=8.0, color="#475569", ha="left", va="bottom",
    )

    fig.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.14)
    out_path = ROOT / "docs" / "story" / "media" / "pc9_fullyear_point.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"wrote {out_path} ({out_path.stat().st_size / 1e3:.1f} KB)")


if __name__ == "__main__":
    main()
