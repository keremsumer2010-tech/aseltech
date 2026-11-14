#!/usr/bin/env python3
"""Lagged correlation & statistical-power analysis for Central Valley hydro-agricultural drivers.

Reads:
  - data/central_valley/drivers.json (8 NISAR L3 SME2 + L2 GUNW epochs, 2026-06-28 to 2026-10-14)

Writes:
  - docs/story/media/pc5_drivers.png

Evaluates synchronous (lag 0) and lagged (lag 1: 12-24 d, lag 2: 24-36 d) Pearson and
Spearman correlations between NISAR soil moisture, HV radar backscatter, and irrigation index
versus cumulative subsidence and detrended interval subsidence rates, including exact
exhaustive permutation p-values (all n! <= 40,320 permutations) and N=8 statistical power limits.

Usage:
    python analysis/pc5/drivers_analysis.py
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.pc5.sinkhole_stats import student_t_two_sided_p  # noqa: E402
from analysis.pc5.uncertainty_map import DISCLAIMER  # noqa: E402

DEFAULT_JSON = ROOT / "data" / "central_valley" / "drivers.json"
DEFAULT_PNG = ROOT / "docs" / "story" / "media" / "pc5_drivers.png"

DRIVER_KEYS: tuple[tuple[str, str], ...] = (
    ("soil_moisture", "Mean soil moisture (m³/m³)"),
    ("soil_moisture_median", "Median soil moisture (m³/m³)"),
    ("hv_backscatter_db", "HV backscatter (dB)"),
    ("irrigation_index", "Irrigation proxy index"),
)


def _rankdata(x: np.ndarray) -> np.ndarray:
    """Average-tie rank transform for Spearman correlation."""
    arr = np.asarray(x, dtype=np.float64)
    order = np.argsort(arr, kind="mergesort")
    sorted_vals = arr[order]
    n = len(arr)
    ranks = np.empty(n, dtype=np.float64)
    i = 0
    while i < n:
        j = i + 1
        while j < n and sorted_vals[j] == sorted_vals[i]:
            j += 1
        avg_r = 0.5 * (i + j - 1) + 1.0
        ranks[order[i:j]] = avg_r
        i = j
    return ranks


def critical_r_alpha(n: int, alpha: float = 0.05) -> float:
    """Two-sided critical |r| where Student-t p-value equals alpha (for df = n - 2)."""
    if n <= 2:
        return float("nan")
    df = float(n - 2)
    lo, hi = 0.0, 1.0 - 1e-12
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        t_val = mid * math.sqrt(df / max(1e-15, 1.0 - mid * mid))
        p_val = student_t_two_sided_p(t_val, df)
        if p_val > alpha:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def fisher_z_ci(r: float, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Approximate 95% confidence interval for Pearson r via Fisher's arctanh transform."""
    if n <= 3 or not math.isfinite(r):
        return float("nan"), float("nan")
    r_clip = max(-0.999999, min(0.999999, r))
    z = math.atanh(r_clip)
    se = 1.0 / math.sqrt(n - 3)
    # Normal quantile z_{1-alpha/2}; default 1.959964 for alpha=0.05
    z_crit = 1.959963984540054 if abs(alpha - 0.05) < 1e-9 else 1.6448536269514722
    return float(math.tanh(z - z_crit * se)), float(math.tanh(z + z_crit * se))


def exact_perm_corr_p(x: np.ndarray, y: np.ndarray) -> float:
    """Exact two-sided permutation p-value over all n! pairings when n <= 8 (else Monte Carlo)."""
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    n = len(x)
    sx = float(x.std(ddof=0))
    sy = float(y.std(ddof=0))
    if sx <= 0.0 or sy <= 0.0:
        return 1.0
    zx = (x - x.mean()) / (sx * n)
    zy = (y - y.mean()) / sy
    r_obs = abs(float(np.dot(zx, zy)))

    if n <= 8:
        perms = np.fromiter(
            itertools.chain.from_iterable(itertools.permutations(range(n))),
            dtype=np.intp,
            count=math.factorial(n) * n,
        ).reshape(-1, n)
        r_null = np.abs(zy[perms] @ zx)
        # Allow 1e-12 float tolerance around |r_obs|
        return float(np.mean(r_null >= r_obs - 1e-12))

    rng = np.random.default_rng(42)
    n_mc = 20_000
    cnt = 1
    for _ in range(n_mc):
        perm = rng.permutation(n)
        if abs(float(np.dot(zx, zy[perm]))) >= r_obs - 1e-12:
            cnt += 1
    return float(cnt / (n_mc + 1))


def corr_stats(x: np.ndarray, y: np.ndarray) -> dict:
    """Compute Pearson r, Spearman rho, Student-t p, exact permutation p, Fisher-z CI, and r_crit."""
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    n = len(x)
    if n < 3:
        return {"n": int(n), "pearson_r": float("nan")}
    sx = float(x.std(ddof=1))
    sy = float(y.std(ddof=1))
    if sx <= 0.0 or sy <= 0.0:
        r = 0.0
    else:
        r = float(np.cov(x, y, ddof=1)[0, 1] / (sx * sy))
    r = max(-1.0, min(1.0, r))
    df = float(n - 2)
    t_stat = r * math.sqrt(df / max(1e-15, 1.0 - r * r)) if abs(r) < 1.0 else float("inf")
    p_t = student_t_two_sided_p(t_stat, df)
    p_perm = exact_perm_corr_p(x, y)
    ci_lo, ci_hi = fisher_z_ci(r, n)

    rx = _rankdata(x)
    ry = _rankdata(y)
    srx, sry = float(rx.std(ddof=1)), float(ry.std(ddof=1))
    rho = float(np.cov(rx, ry, ddof=1)[0, 1] / (srx * sry)) if srx > 0.0 and sry > 0.0 else 0.0
    rho = max(-1.0, min(1.0, rho))
    t_rho = rho * math.sqrt(df / max(1e-15, 1.0 - rho * rho)) if abs(rho) < 1.0 else float("inf")
    p_rho_t = student_t_two_sided_p(t_rho, df)
    p_rho_perm = exact_perm_corr_p(rx, ry)

    return {
        "n": int(n),
        "df": int(n - 2),
        "pearson_r": float(r),
        "r_squared": float(r * r),
        "t_stat": float(t_stat),
        "p_t_two_sided": float(p_t),
        "p_perm_exact": float(p_perm),
        "fisher_ci95": [ci_lo, ci_hi],
        "spearman_rho": float(rho),
        "spearman_p_t": float(p_rho_t),
        "spearman_p_perm": float(p_rho_perm),
        "r_crit_alpha05": float(critical_r_alpha(n, 0.05)),
        "significant_alpha05": bool(p_t < 0.05 and p_perm < 0.05),
    }


def analyze_drivers(json_path: Path = DEFAULT_JSON, max_lag: int = 2) -> dict:
    """Evaluate synchronous and lagged driver correlations with Central Valley subsidence."""
    with open(json_path, encoding="utf-8") as fh:
        data = json.load(fh)

    dates = [str(dt) for dt in data["dates"]]
    dt_objs = [datetime.strptime(dt, "%Y-%m-%d") for dt in dates]
    dt_days = [(dt_objs[i + 1] - dt_objs[i]).days for i in range(len(dt_objs) - 1)]

    sub_peak = np.asarray(data["subsidence_cm"], dtype=np.float64)
    sub_top5 = np.asarray(data["subsidence_top5_mean_cm"], dtype=np.float64)
    interval_rate = np.diff(sub_peak) / np.asarray(dt_days, dtype=np.float64)  # cm/day over each interval
    # Interval-level predictor: average driver value across the start and end of each interval
    targets = {
        "subsidence_cm": sub_peak,
        "subsidence_top5_mean_cm": sub_top5,
    }

    cumulative_results: dict[str, dict[str, dict[str, dict]]] = {}
    for target_name, y_full in targets.items():
        cumulative_results[target_name] = {}
        for key, _ in DRIVER_KEYS:
            x_full = np.asarray(data[key], dtype=np.float64)
            lag_map: dict[str, dict] = {}
            for lag in range(max_lag + 1):
                if lag == 0:
                    x_slice, y_slice = x_full, y_full
                else:
                    x_slice, y_slice = x_full[:-lag], y_full[lag:]
                lag_map[f"lag{lag}"] = corr_stats(x_slice, y_slice)
            cumulative_results[target_name][key] = lag_map

    # Detrended interval-rate correlations (predicting interval rate_t from antecedent driver)
    interval_results: dict[str, dict[str, dict]] = {}
    for key, _ in DRIVER_KEYS:
        x_full = np.asarray(data[key], dtype=np.float64)
        x_mid = 0.5 * (x_full[:-1] + x_full[1:])
        x_start = x_full[:-1]
        interval_results[key] = {
            "interval_midpoint_lag0": corr_stats(x_mid, interval_rate),
            "interval_start_lag0": corr_stats(x_start, interval_rate),
            "prior_epoch_lag1": corr_stats(x_full[:-2], interval_rate[1:]),
        }

    # Check minimum detectable |r| at 80% power for n=8 (df=6) using Fisher-z variance 1/(n-3)
    # 80% power two-sided at alpha=0.05 requires atanh(|r|) >= (1.96 + 0.8416) / sqrt(n-3)
    z_mde_n8 = (1.959963984540054 + 0.8416212335729143) / math.sqrt(8 - 3)
    r_mde_80pct_n8 = float(math.tanh(z_mde_n8))

    return {
        "site": "central_valley",
        "dates": dates,
        "n_epochs": len(dates),
        "interval_days": dt_days,
        "interval_dates": [f"{dates[i]}..{dates[i+1]}" for i in range(len(dt_days))],
        "interval_rate_cm_day": [float(v) for v in interval_rate],
        "reported_lag_corr_detail": data.get("lag_corr_detail", {}),
        "cumulative_correlations": cumulative_results,
        "detrended_interval_correlations": interval_results,
        "power_summary": {
            "n_epochs": len(dates),
            "r_crit_alpha05_lag0_n8": float(critical_r_alpha(8, 0.05)),
            "r_crit_alpha05_lag1_n7": float(critical_r_alpha(7, 0.05)),
            "r_crit_alpha05_lag2_n6": float(critical_r_alpha(6, 0.05)),
            "r_mde_80pct_power_n8": r_mde_80pct_n8,
        },
        "data_raw": data,
        "disclaimer": DISCLAIMER,
    }


def render_plot(report: dict, png_path: Path = DEFAULT_PNG) -> Path:
    """Create two-panel publication figure for Central Valley driver trajectories and lag CIs."""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.spines.top": False,
        }
    )

    data = report["data_raw"]
    dates = report["dates"]
    short_dates = [d[5:] for d in dates]
    x = np.arange(len(dates))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.6, 5.4), dpi=180)
    fig.subplots_adjust(wspace=0.33, top=0.81, bottom=0.18, left=0.06, right=0.94)
    fig.suptitle(
        "Central Valley Hydro-Agricultural Drivers vs. NISAR Subsidence (N = 8 Epochs)",
        fontsize=12.5,
        fontweight="bold",
        y=0.95,
    )

    # Panel A: Time series with 24-day gap highlights
    for idx_gap in (2, 6):
        ax1.axvspan(idx_gap, idx_gap + 1, color="#f1f5f9", alpha=0.9, zorder=0)
    ax1.text(2.5, 0.25, "24 d gap", ha="center", va="bottom", fontsize=7.5, color="#64748b")
    ax1.text(6.5, 0.25, "24 d gap", ha="center", va="bottom", fontsize=7.5, color="#64748b")

    sub = np.asarray(data["subsidence_cm"], dtype=np.float64)
    sm = np.asarray(data["soil_moisture"], dtype=np.float64)
    irr = np.asarray(data["irrigation_index"], dtype=np.float64)

    l1 = ax1.plot(x, -sub, "o-", color="#0f172a", linewidth=2.2, markersize=5, label="Peak 1 km subsidence |LOS| (cm)")
    ax1.set_ylabel("Cumulative Subsidence |LOS| (cm)", color="#0f172a")
    ax1.set_ylim(0, 9.2)
    ax1.set_xticks(x)
    ax1.set_xticklabels(short_dates, rotation=30, ha="right")
    ax1.set_title("A. Subsidence Trajectory vs. Soil Moisture & Irrigation Proxy")
    ax1.grid(axis="y", linestyle="--", alpha=0.3)

    ax1_r = ax1.twinx()
    ax1_r.spines["top"].set_visible(False)
    l2 = ax1_r.plot(x, sm, "s--", color="#2563eb", linewidth=1.8, markersize=5, label="SME2 soil moisture (m³/m³)")
    l3 = ax1_r.plot(x, irr * 0.25, "^:", color="#059669", linewidth=1.8, markersize=5, label="Irrigation index (scaled x0.25)")
    ax1_r.set_ylabel("Soil Moisture (m³/m³) / Scaled Index", color="#2563eb")
    ax1_r.set_ylim(0.02, 0.24)
    ax1_r.tick_params(axis="y", colors="#2563eb")

    lines = l1 + l2 + l3
    labels = [ln.get_label() for ln in lines]
    ax1.legend(lines, labels, loc="upper left", fontsize=8.0, frameon=True, framealpha=0.92)

    # Panel B: Pearson r with 95% Fisher-z CI across lags vs critical |r| thresholds
    cum_corr = report["cumulative_correlations"]["subsidence_cm"]
    plot_drivers = [
        ("irrigation_index", "Irrigation\nIndex"),
        ("soil_moisture", "Soil Moisture\n(Mean)"),
        ("soil_moisture_median", "Soil Moisture\n(Median)"),
        ("hv_backscatter_db", "HV Backscatter\n(dB)"),
    ]
    lags = [("lag0", "Lag 0 (0 d, n=8)", "#2563eb", -0.22), ("lag1", "Lag 1 (12-24 d, n=7)", "#d97706", 0.0), ("lag2", "Lag 2 (24-36 d, n=6)", "#dc2626", 0.22)]
    y_base = np.arange(len(plot_drivers))

    for lag_key, lag_label, color, offset in lags:
        r_vals = [cum_corr[d_key][lag_key]["pearson_r"] for d_key, _ in plot_drivers]
        err_lo = [r_vals[i] - cum_corr[plot_drivers[i][0]][lag_key]["fisher_ci95"][0] for i in range(len(plot_drivers))]
        err_hi = [cum_corr[plot_drivers[i][0]][lag_key]["fisher_ci95"][1] - r_vals[i] for i in range(len(plot_drivers))]
        ax2.errorbar(
            r_vals,
            y_base + offset,
            xerr=[err_lo, err_hi],
            fmt="o",
            color=color,
            ecolor=color,
            elinewidth=1.6,
            capsize=3.5,
            markersize=6,
            label=lag_label,
        )

    r_crit_8 = report["power_summary"]["r_crit_alpha05_lag0_n8"]
    r_crit_7 = report["power_summary"]["r_crit_alpha05_lag1_n7"]
    ax2.axvline(0.0, color="#64748b", linewidth=1.0)
    ax2.axvspan(-r_crit_8, r_crit_8, color="#e2e8f0", alpha=0.55, zorder=0, label=f"|r| < {r_crit_8:.2f} (p > 0.05 at n=8)")
    ax2.axvline(r_crit_7, color="#94a3b8", linewidth=1.1, linestyle="--", label=f"|r| crit (n=7): ±{r_crit_7:.2f}")
    ax2.axvline(-r_crit_7, color="#94a3b8", linewidth=1.1, linestyle="--")

    ax2.set_yticks(y_base)
    ax2.set_yticklabels([lbl for _, lbl in plot_drivers])
    ax2.set_xlim(-1.05, 1.05)
    ax2.set_ylim(-0.55, len(plot_drivers) + 0.72)
    ax2.set_xlabel("Pearson r with Cumulative LOS Subsidence (95% Fisher-z CI)")
    ax2.set_title("B. Lagged Correlations Remain Underpowered at N = 8")
    ax2.grid(axis="x", linestyle="--", alpha=0.3)
    ax2.legend(loc="upper left", fontsize=7.6, frameon=True, framealpha=0.94, ncol=2)

    fig.text(
        0.5,
        0.03,
        f"Data: NASA-ISRO NISAR L3 SME2 & L2 GUNW (provisional). {DISCLAIMER}",
        ha="center",
        fontsize=8.2,
        color="#475569",
    )
    fig.savefig(png_path, dpi=180)
    plt.close(fig)
    return png_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze lagged hydro-agricultural driver correlations.")
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--png", type=Path, default=DEFAULT_PNG)
    args = parser.parse_args()

    report = analyze_drivers(json_path=args.json)
    render_plot(report, png_path=args.png)
    out = {k: v for k, v in report.items() if k != "data_raw"}
    print(json.dumps(out, indent=2))
    print(f"Wrote {args.png}", file=sys.stderr)


if __name__ == "__main__":
    main()
