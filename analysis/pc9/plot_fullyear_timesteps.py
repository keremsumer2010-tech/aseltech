"""Plot 12-day and monthly time-step rhythm figures for Central Valley full year (PC9, A6).

Reads:
  data/central_valley_fullyear/points.json
  data/central_valley_fullyear/summary.json
  data/central_valley_fullyear/decomp.json
Writes:
  docs/story/media/pc9_fullyear_12day_steps.png
  docs/story/media/pc9_fullyear_monthly_steps.png
"""
from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "central_valley_fullyear"
MEDIA_DIR = ROOT / "docs" / "story" / "media"

BETA_CUTOFF = "2026-06-28"


def _load_points():
    pts = {p["id"]: p for p in json.loads((DATA_DIR / "points.json").read_text(encoding="utf-8"))}
    return pts["p01"], pts["p06"], pts["p11"]


def compute_pair_steps(point: dict) -> list[dict]:
    """Compute exact inter-pair displacement steps and 12-day normalized rates."""
    dates = point["dates"]
    vals = point["disp_cm"]
    rows = []
    for i in range(1, len(dates)):
        d1 = date.fromisoformat(dates[i - 1])
        d2 = date.fromisoformat(dates[i])
        dt = (d2 - d1).days
        dv = float(vals[i]) - float(vals[i - 1])
        rows.append({
            "d1": d1,
            "d2": d2,
            "mid_dt": datetime.combine(d1, datetime.min.time()) + (datetime.combine(d2, datetime.min.time()) - datetime.combine(d1, datetime.min.time())) / 2,
            "dt_days": dt,
            "dv_cm": dv,
            "rate_12d_cm": dv * (12.0 / dt),
            "cum_cm": float(vals[i]),
            "quality": "beta-precal" if dates[i] <= BETA_CUTOFF else "provisional",
        })
    return rows


def compute_monthly_bins(point: dict) -> list[dict]:
    """Group exact consecutive pairs by end-date calendar month (YYYY-MM).

    Uses actual cumulative endpoints (zero synthetic temporal interpolation) so
    monthly steps sum identically to the observed 324-day total displacement.
    """
    dates = point["dates"]
    vals = point["disp_cm"]
    groups: dict[str, list[int]] = {}
    for i in range(1, len(dates)):
        ym = dates[i][:7]
        groups.setdefault(ym, []).append(i)

    bins = []
    for ym, idxs in groups.items():
        i0 = idxs[0] - 1
        i1 = idxs[-1]
        d1 = date.fromisoformat(dates[i0])
        d2 = date.fromisoformat(dates[i1])
        span = (d2 - d1).days
        dv = float(vals[i1]) - float(vals[i0])
        # All pairs ending <= 2026-06-28 are beta-precal; >= 2026-07 are provisional
        qual = "beta-precal" if dates[i1] <= BETA_CUTOFF else "provisional"
        lbl = datetime.strptime(ym, "%Y-%m").strftime("%b %Y")
        bins.append({
            "ym": ym,
            "label": lbl,
            "start": dates[i0],
            "end": dates[i1],
            "span_days": span,
            "n_pairs": len(idxs),
            "dv_cm": dv,
            "rate_30d_cm": dv * (30.0 / span),
            "cum_cm": float(vals[i1]),
            "quality": qual,
        })
    return bins


def plot_12day_steps(p1: dict, p6: dict, p11: dict) -> Path:
    s1 = compute_pair_steps(p1)
    s6 = compute_pair_steps(p6)
    s11 = compute_pair_steps(p11)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.edgecolor": "#cbd5e1",
        "axes.linewidth": 0.9,
    })

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(11.8, 7.6), sharex=True,
        gridspec_kw={"height_ratios": [1.85, 1.0], "hspace": 0.16},
    )
    fig.patch.set_facecolor("#ffffff")

    split_dt = datetime(2026, 6, 28)
    start_dt = datetime(2025, 11, 20)
    end_dt = datetime(2026, 10, 18)

    for ax in (ax1, ax2):
        ax.set_facecolor("#ffffff")
        ax.axvspan(start_dt, split_dt, color="#fef3c7", alpha=0.38, zorder=0)
        ax.axvspan(split_dt, end_dt, color="#f0f9ff", alpha=0.45, zorder=0)
        ax.axvline(split_dt, color="#64748b", linestyle="--", linewidth=1.15, zorder=2)
        ax.axhline(0.0, color="#64748b", linewidth=0.95, zorder=2)
        ax.grid(axis="y", color="#e2e8f0", linewidth=0.7, zorder=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # Top panel: 12-day incremental displacement at Earlimart p01 (bars) + Delano p06 (markers/line)
    mids = [r["mid_dt"] for r in s1]

    for r in s1:
        is_beta = r["quality"] == "beta-precal"
        is_up = r["rate_12d_cm"] >= 0
        facecolor = "#60a5fa" if is_up else "#dc2626"
        alpha = 0.58 if is_beta else 0.88
        edge = "#1e3a8a" if is_up else "#7f1d1d"
        ls = "--" if is_beta else "-"
        hatch = "///" if r["dt_days"] > 12 else None
        ax1.bar(
            r["mid_dt"], r["rate_12d_cm"],
            width=r["dt_days"] * 0.72,
            color=facecolor, alpha=alpha,
            edgecolor=edge, linestyle=ls, linewidth=1.05,
            hatch=hatch, zorder=3,
        )

    ax1.plot(
        mids, [r["rate_12d_cm"] for r in s6],
        color="#0f766e", linestyle="-", linewidth=1.45, marker="o", markersize=4.2,
        label=f"Valley median step ({p6['name']})", zorder=5,
    )

    # Regime banners cleanly above all spikes (max spike +4.37 cm on 2026-08-27)
    ax1.text(
        datetime(2026, 3, 10), 6.2,
        "BETA PRE-CALIBRATION (18 x 12-day pairs)\nDashed outlines — elevated amplitude uncertainty",
        ha="center", va="top", fontsize=8.3, fontweight="bold", color="#92400e",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "#fef9c3", "edgecolor": "#f59e0b", "alpha": 0.94},
    )
    ax1.text(
        datetime(2026, 8, 22), 6.2,
        "PROVISIONAL CRID P05023\n(5 x 12-day + 2 x 24-day pairs)",
        ha="center", va="top", fontsize=8.3, fontweight="bold", color="#0c4a6e",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "#e0f2fe", "edgecolor": "#0284c7", "alpha": 0.94},
    )

    # Key onset annotations
    ax1.annotate(
        "Spring pumping onset:\n-4.3 cm (24 Mar–05 Apr)\n-4.7 cm (17 Apr–29 Apr)",
        xy=(datetime(2026, 4, 23), -4.72),
        xytext=(datetime(2026, 1, 20), -4.8),
        fontsize=8.2, fontweight="bold", color="#7f1d1d", ha="center",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "#ffffff", "edgecolor": "#fca5a5", "alpha": 0.95},
        arrowprops={"arrowstyle": "->", "color": "#991b1b", "lw": 1.0},
        zorder=6,
    )
    ax1.annotate(
        "Single-pair noise jump\n(+2.8 cm p01, +4.4 cm p06\n15–27 Aug 2026)",
        xy=(datetime(2026, 8, 21), 2.84),
        xytext=(datetime(2026, 5, 22), 2.95),
        fontsize=7.9, color="#1e293b", ha="center",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "#ffffff", "edgecolor": "#cbd5e1", "alpha": 0.94},
        arrowprops={"arrowstyle": "->", "color": "#475569", "lw": 0.95},
        zorder=6,
    )

    # Custom legend patches for bars
    p_up_beta = mpatches.Patch(facecolor="#60a5fa", alpha=0.58, edgecolor="#1e3a8a", linestyle="--", label="Earlimart p01 uplift (beta-precal)")
    p_up_prov = mpatches.Patch(facecolor="#60a5fa", alpha=0.88, edgecolor="#1e3a8a", linestyle="-", label="Earlimart p01 uplift (provisional)")
    p_dn_beta = mpatches.Patch(facecolor="#dc2626", alpha=0.58, edgecolor="#7f1d1d", linestyle="--", label="Earlimart p01 sinking (beta-precal)")
    p_dn_prov = mpatches.Patch(facecolor="#dc2626", alpha=0.88, edgecolor="#7f1d1d", linestyle="-", label="Earlimart p01 sinking (provisional)")
    p_24d = mpatches.Patch(facecolor="#cbd5e1", edgecolor="#334155", hatch="///", label="24-day pair (rate per 12 d)")
    h_line, _ = ax1.get_legend_handles_labels()
    ax1.legend(
        handles=[p_up_beta, p_dn_beta, p_up_prov, p_dn_prov, p_24d] + h_line,
        loc="lower right", ncol=2, frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=7.4,
    )

    ax1.set_ylim(-6.1, 6.6)
    ax1.set_ylabel("Step motion (cm per 12 days)", fontweight="bold", color="#0f172a")
    ax1.set_title(
        "12-Day Revisit Time Steps: Short-Term Irrigation Onset vs. Atmospheric Pair Scatter (Earlimart p01)",
        loc="left", fontsize=11.8, fontweight="bold", color="#0f172a", pad=10,
    )

    # Bottom panel: 12-day noise contrast (Woodlake stable control p11 vs Earlimart cumulative step trace)
    ax2.plot(
        mids, [r["rate_12d_cm"] for r in s11],
        color="#475569", linewidth=1.5, marker="s", markersize=3.8,
        label=f"Stable foothills control step ({p11['name']}: max |step| = 0.34 cm)", zorder=4,
    )
    ax2.axhspan(-1.0, 1.0, color="#e2e8f0", alpha=0.45, zorder=1, label="Typical single-pair tropospheric scatter (~+/-1 cm)")
    ax2.set_ylim(-1.6, 1.6)
    ax2.set_ylabel("Control step (cm / 12 d)", fontweight="bold", color="#0f172a")
    ax2.legend(loc="lower left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.0)
    ax2.set_title(
        "Foothill Reference Stability Across Every 12-Day Pair (Woodlake p11 vs. ±1 cm Weather Band)",
        loc="left", fontsize=10.0, fontweight="bold", color="#334155", pad=5,
    )

    ax2.set_xlim(start_dt, end_dt)
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax2.get_xticklabels(), rotation=22, ha="right", fontsize=8.6)

    fig.text(
        0.06, 0.015,
        "Data: NASA-ISRO NISAR L2 GUNW (quality: mixed — 18 beta-precal + 7 provisional CRID P05023), ASF DAAC. Analysis: Team Taykut.\n"
        "Note: Two summer pairs span 24 days (22 Jul–15 Aug and 20 Sep–14 Oct, hatched) and are shown normalized to cm per 12 days. NISAR calibration is performed by NASA-JPL and ISRO.",
        fontsize=7.8, color="#475569", ha="left", va="bottom",
    )
    fig.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.14)
    out = MEDIA_DIR / "pc9_fullyear_12day_steps.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def plot_monthly_steps(p1: dict, p6: dict, p11: dict) -> Path:
    m1 = compute_monthly_bins(p1)
    m6 = compute_monthly_bins(p6)
    m11 = compute_monthly_bins(p11)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.edgecolor": "#cbd5e1",
        "axes.linewidth": 0.9,
    })

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(11.8, 7.6), sharex=True,
        gridspec_kw={"height_ratios": [1.7, 1.05], "hspace": 0.16},
    )
    fig.patch.set_facecolor("#ffffff")

    x = np.arange(len(m1))
    split_x = 6.5  # between Jun 2026 (idx 6) and Jul 2026 (idx 7)

    for ax in (ax1, ax2):
        ax.set_facecolor("#ffffff")
        ax.axvspan(-0.6, split_x, color="#fef3c7", alpha=0.38, zorder=0)
        ax.axvspan(split_x, len(m1) - 0.4, color="#f0f9ff", alpha=0.45, zorder=0)
        ax.axvline(split_x, color="#64748b", linestyle="--", linewidth=1.15, zorder=2)
        ax.axhline(0.0, color="#64748b", linewidth=0.95, zorder=2)
        ax.grid(axis="y", color="#e2e8f0", linewidth=0.7, zorder=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # Top panel: Monthly net displacement bars (grouped p01 Earlimart vs p06 Delano)
    w = 0.36
    for i, (r1, r6) in enumerate(zip(m1, m6)):
        is_beta = r1["quality"] == "beta-precal"
        # p01 bars
        c1 = "#2563eb" if r1["dv_cm"] >= 0 else "#dc2626"
        a1 = 0.62 if is_beta else 0.90
        ls1 = "--" if is_beta else "-"
        ax1.bar(i - w / 2, r1["dv_cm"], width=w, color=c1, alpha=a1, edgecolor="#0f172a", linestyle=ls1, linewidth=0.9, zorder=3)
        # Value annotations on p01 bars
        va1 = "bottom" if r1["dv_cm"] >= 0 else "top"
        off1 = 0.18 if r1["dv_cm"] >= 0 else -0.18
        ax1.text(
            i - w / 2, r1["dv_cm"] + off1, f"{r1['dv_cm']:+.1f}",
            ha="center", va=va1, fontsize=7.5, fontweight="bold",
            color="#1e3a8a" if r1["dv_cm"] >= 0 else "#7f1d1d",
        )
        # p06 Delano median bars
        c6 = "#0ea5e9" if r6["dv_cm"] >= 0 else "#f97316"
        ax1.bar(i + w / 2, r6["dv_cm"], width=w, color=c6, alpha=0.60 if is_beta else 0.85, edgecolor="#334155", linestyle=ls1, linewidth=0.8, hatch="..", zorder=3)

    # Regime banners placed strictly clear of the Mar 2026 (+4.1 cm p06) uplift bar
    ax1.text(
        2.85, 6.7,
        "BETA PRE-CALIBRATION MONTHS (Dec 2025 – Jun 2026)\nDashed outlines — winter recharge (+2.6 cm Mar p01; +4.1 cm p06) & spring onset (-9.5 cm Apr)",
        ha="center", va="top", fontsize=7.9, fontweight="bold", color="#92400e",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "#fef9c3", "edgecolor": "#f59e0b", "alpha": 0.95},
        zorder=7,
    )
    ax1.text(
        8.5, 6.7,
        "PROVISIONAL MONTHS\n(Jul – Oct 2026, CRID P05023)\nSolid outlines",
        ha="center", va="top", fontsize=7.9, fontweight="bold", color="#0c4a6e",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "#e0f2fe", "edgecolor": "#0284c7", "alpha": 0.95},
        zorder=7,
    )

    p_1up = mpatches.Patch(facecolor="#2563eb", alpha=0.85, edgecolor="#0f172a", label="Earlimart peak (p01): monthly uplift (+)")
    p_1dn = mpatches.Patch(facecolor="#dc2626", alpha=0.85, edgecolor="#0f172a", label="Earlimart peak (p01): monthly drawdown (-)")
    p_6up = mpatches.Patch(facecolor="#0ea5e9", alpha=0.75, edgecolor="#334155", hatch="..", label="Valley median (p06 Delano): uplift (+)")
    p_6dn = mpatches.Patch(facecolor="#f97316", alpha=0.75, edgecolor="#334155", hatch="..", label="Valley median (p06 Delano): drawdown (-)")
    ax1.legend(
        handles=[p_1up, p_1dn, p_6up, p_6dn],
        loc="lower left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=7.8,
    )

    ax1.set_ylim(-11.4, 7.3)
    ax1.set_ylabel("Monthly net change (cm LOS)", fontweight="bold", color="#0f172a")
    ax1.set_title(
        "Monthly Time Steps: Winter Rebound (Dec–Mar) vs. Spring–Summer Compaction (Apr–Oct)",
        loc="left", fontsize=11.8, fontweight="bold", color="#0f172a", pad=10,
    )

    # Bottom panel: Normalized monthly rate (cm / 30 days) + Woodlake foothills control
    ax2.plot(
        x, [r["rate_30d_cm"] for r in m1],
        color="#991b1b", linewidth=2.2, marker="o", markersize=5.2,
        label="Earlimart peak rate (p01, cm / 30 d)", zorder=5,
    )
    ax2.plot(
        x, [r["rate_30d_cm"] for r in m6],
        color="#0f766e", linewidth=1.8, marker="D", markersize=4.5,
        label="Valley median rate (p06 Delano, cm / 30 d)", zorder=4,
    )
    ax2.plot(
        x, [r["rate_30d_cm"] for r in m11],
        color="#64748b", linewidth=1.3, linestyle=":", marker="s", markersize=3.8,
        label="Stable foothills control (p11 Woodlake)", zorder=3,
    )
    ax2.set_ylim(-9.4, 6.2)
    ax2.set_ylabel("Rate (cm per 30 days)", fontweight="bold", color="#0f172a")
    ax2.legend(loc="lower right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.0)
    ax2.set_title(
        "Length-Normalized Monthly Tempo (accounting for 24-day vs. 36-day radar windows)",
        loc="left", fontsize=10.0, fontweight="bold", color="#334155", pad=5,
    )

    xtick_lbls = [f"{r['label']}\n({r['span_days']}d)" for r in m1]
    ax2.set_xticks(x)
    ax2.set_xticklabels(xtick_lbls, fontsize=8.3)
    ax2.set_xlim(-0.6, len(m1) - 0.4)

    fig.text(
        0.06, 0.015,
        "Data: NASA-ISRO NISAR L2 GUNW (quality: mixed — 18 beta-precal + 7 provisional CRID P05023), ASF DAAC. Analysis: Team Taykut.\n"
        "Monthly bins group consecutive pairs by end date (summing identically to -20.32 cm at p01, -4.49 cm at p06, -0.64 cm at p11). Calibration by NASA-JPL and ISRO.",
        fontsize=7.8, color="#475569", ha="left", va="bottom",
    )
    fig.subplots_adjust(left=0.08, right=0.97, top=0.93, bottom=0.14)
    out = MEDIA_DIR / "pc9_fullyear_monthly_steps.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    return out


def main() -> None:
    p1, p6, p11 = _load_points()
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    out12 = plot_12day_steps(p1, p6, p11)
    outm = plot_monthly_steps(p1, p6, p11)
    print(f"wrote {out12} ({out12.stat().st_size / 1e3:.1f} KB)")
    print(f"wrote {outm} ({outm.stat().st_size / 1e3:.1f} KB)")


if __name__ == "__main__":
    main()
