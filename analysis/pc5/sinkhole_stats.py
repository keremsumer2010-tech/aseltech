#!/usr/bin/env python3
"""Permutation, block-bootstrap, and rigid-shift significance tests for Karapinar sinkholes.

Tests whether cumulative NISAR L-band LOS subsidence within 0-2 km of the 29
documented Karapinar sinkholes (data/karapinar/sinkholes.geojson) is statistically
distinguishable from >5 km background pixels in analysis/out/karapinar_cum.npz,
explicitly addressing spatial autocorrelation via:
  1. Pixel-level Monte Carlo permutation (B=10,000) and bootstrap 95% CI (naive baseline).
  2. Disjoint 1.04 km (13x13 px) and 2.08 km (26x26 px) spatial-block permutation and bootstrap.
  3. Rigid constellation spatial-shift null test translating all 29 sinkholes together
     across the observed Karapinar interferogram footprint.

Writes:
  - docs/story/media/pc5_sinkhole_perm.png

Usage:
    python analysis/pc5/sinkhole_stats.py
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.pc5.uncertainty_map import DISCLAIMER, lonlat_to_utm  # noqa: E402

DEFAULT_NPZ = ROOT / "analysis" / "out" / "karapinar_cum.npz"
DEFAULT_GEOJSON = ROOT / "data" / "karapinar" / "sinkholes.geojson"
DEFAULT_PNG = ROOT / "docs" / "story" / "media" / "pc5_sinkhole_perm.png"

RING_BOUNDS_KM: tuple[tuple[str, float, float | None], ...] = (
    ("0-1 km", 0.0, 1.0),
    ("1-2 km", 1.0, 2.0),
    ("0-2 km (combined)", 0.0, 2.0),
    ("2-5 km", 2.0, 5.0),
    (">5 km (background)", 5.0, None),
)


def _betacf(a: float, b: float, x: float) -> float:
    """Evaluates continued fraction for regularized incomplete beta I_x(a, b)."""
    max_iter = 200
    eps = 3.0e-14
    fpmin = 1.0e-300
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta function I_x(a, b) for 0 <= x <= 1."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def student_t_two_sided_p(t_stat: float, df: float) -> float:
    """Exact two-sided p-value from Student's t distribution."""
    if df <= 0.0 or not math.isfinite(t_stat):
        return float("nan")
    x = df / (df + t_stat * t_stat)
    return float(max(0.0, min(1.0, betainc(0.5 * df, 0.5, x))))


def welch_t_test(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Return (t_stat, df, two_sided_p) for Welch's unequal-variance t-test."""
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan"), float("nan"), float("nan")
    v1 = float(np.var(a, ddof=1))
    v2 = float(np.var(b, ddof=1))
    se2 = v1 / n1 + v2 / n2
    if se2 <= 0.0:
        return 0.0, float(n1 + n2 - 2), 1.0
    t_stat = float((np.mean(a) - np.mean(b)) / math.sqrt(se2))
    num = se2 * se2
    den = ((v1 / n1) ** 2) / (n1 - 1) + ((v2 / n2) ** 2) / (n2 - 1)
    df = num / den if den > 0.0 else float(n1 + n2 - 2)
    return t_stat, df, student_t_two_sided_p(t_stat, df)


def mann_whitney_u_test(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Return (u_stat, z_stat, two_sided_p) using average ranks and tie correction."""
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return float("nan"), float("nan"), float("nan")
    pooled = np.concatenate([a, b])
    order = np.argsort(pooled, kind="mergesort")
    sorted_vals = pooled[order]
    n_tot = len(pooled)
    ranks = np.empty(n_tot, dtype=np.float64)
    tie_corr = 0.0
    i = 0
    while i < n_tot:
        j = i + 1
        while j < n_tot and sorted_vals[j] == sorted_vals[i]:
            j += 1
        avg_rank = 0.5 * (i + j - 1) + 1.0
        ranks[order[i:j]] = avg_rank
        t = j - i
        if t > 1:
            tie_corr += t * (t * t - 1.0)
        i = j
    r1 = float(ranks[:n1].sum())
    u1 = r1 - n1 * (n1 + 1) / 2.0
    mu = n1 * n2 / 2.0
    var = (n1 * n2 / 12.0) * ((n_tot + 1.0) - tie_corr / (n_tot * (n_tot - 1.0))) if n_tot > 1 else 0.0
    if var <= 0.0:
        return u1, 0.0, 1.0
    z = (u1 - mu) / math.sqrt(var)
    p = math.erfc(abs(z) / math.sqrt(2.0))
    return float(u1), float(z), float(p)


def permutation_diff_means(
    near_vals: np.ndarray,
    bg_vals: np.ndarray,
    n_perm: int = 10_000,
    seed: int = 42,
) -> dict:
    """Two-group Monte Carlo permutation test on difference in means (near - bg)."""
    near = np.asarray(near_vals, dtype=np.float64)
    bg = np.asarray(bg_vals, dtype=np.float64)
    n_near, n_bg = len(near), len(bg)
    obs_diff = float(near.mean() - bg.mean())
    pool = np.concatenate([near, bg])
    pool_sum = float(pool.sum())
    n_pool = len(pool)

    # Exact algebraic identity: sum_bg = pool_sum - sum_near
    py_rng = random.Random(seed)
    indices_range = range(n_pool)
    null_diffs = np.empty(n_perm, dtype=np.float64)
    inv_near = 1.0 / n_near
    inv_bg = 1.0 / n_bg
    for i in range(n_perm):
        picked = py_rng.sample(indices_range, n_near)
        s_near = float(pool[picked].sum())
        null_diffs[i] = s_near * inv_near - (pool_sum - s_near) * inv_bg

    # Phipson & Smyth (2010) pseudocount estimator avoids uncalibrated exact zero
    p_one_sided = float((np.sum(null_diffs <= obs_diff) + 1) / (n_perm + 1))
    p_two_sided = float((np.sum(np.abs(null_diffs) >= abs(obs_diff)) + 1) / (n_perm + 1))
    return {
        "obs_diff_cm": obs_diff,
        "p_one_sided": p_one_sided,
        "p_two_sided": p_two_sided,
        "null_diffs_cm": null_diffs,
        "null_q025_cm": float(np.quantile(null_diffs, 0.025)),
        "null_q50_cm": float(np.quantile(null_diffs, 0.50)),
        "null_q975_cm": float(np.quantile(null_diffs, 0.975)),
    }


def bootstrap_diff_ci(
    near_vals: np.ndarray,
    bg_vals: np.ndarray,
    n_boot: int = 10_000,
    seed: int = 42,
    alpha: float = 0.05,
    chunk_size: int = 500,
) -> tuple[float, float, float, np.ndarray]:
    """Stratified non-parametric bootstrap CI for (mean(near) - mean(bg))."""
    near = np.asarray(near_vals, dtype=np.float64)
    bg = np.asarray(bg_vals, dtype=np.float64)
    n_near, n_bg = len(near), len(bg)
    rng = np.random.default_rng(seed)
    boot_diffs = np.empty(n_boot, dtype=np.float64)
    done = 0
    while done < n_boot:
        k = min(chunk_size, n_boot - done)
        i_near = rng.integers(0, n_near, size=(k, n_near))
        i_bg = rng.integers(0, n_bg, size=(k, n_bg))
        m_near = near[i_near].mean(axis=1)
        m_bg = bg[i_bg].mean(axis=1)
        boot_diffs[done : done + k] = m_near - m_bg
        done += k
    lo = float(np.quantile(boot_diffs, alpha / 2.0))
    hi = float(np.quantile(boot_diffs, 1.0 - alpha / 2.0))
    return lo, hi, float(boot_diffs.std(ddof=1)), boot_diffs


def summarize_group(
    near_vals: np.ndarray,
    bg_vals: np.ndarray,
    label: str,
    n_perm: int = 10_000,
    n_boot: int = 10_000,
    seed: int = 42,
) -> tuple[dict, np.ndarray]:
    """Run full comparison suite (permutation, bootstrap CI, Welch t, Mann-Whitney U)."""
    perm = permutation_diff_means(near_vals, bg_vals, n_perm=n_perm, seed=seed)
    ci_lo, ci_hi, boot_se, _ = bootstrap_diff_ci(near_vals, bg_vals, n_boot=n_boot, seed=seed)
    t_stat, t_df, t_p = welch_t_test(near_vals, bg_vals)
    u_stat, u_z, u_p = mann_whitney_u_test(near_vals, bg_vals)
    summary = {
        "level": label,
        "n_near": int(len(near_vals)),
        "n_bg": int(len(bg_vals)),
        "near_mean_cm": float(np.mean(near_vals)),
        "near_median_cm": float(np.median(near_vals)),
        "near_std_cm": float(np.std(near_vals, ddof=1)),
        "bg_mean_cm": float(np.mean(bg_vals)),
        "bg_median_cm": float(np.median(bg_vals)),
        "bg_std_cm": float(np.std(bg_vals, ddof=1)),
        "diff_mean_cm": float(perm["obs_diff_cm"]),
        "diff_median_cm": float(np.median(near_vals) - np.median(bg_vals)),
        "boot_ci95_cm": [ci_lo, ci_hi],
        "boot_se_cm": boot_se,
        "perm_n": int(n_perm),
        "perm_p_one_sided": float(perm["p_one_sided"]),
        "perm_p_two_sided": float(perm["p_two_sided"]),
        "welch_t": float(t_stat),
        "welch_df": float(t_df),
        "welch_p_two_sided": float(t_p),
        "mann_whitney_u": float(u_stat),
        "mann_whitney_z": float(u_z),
        "mann_whitney_p_two_sided": float(u_p),
    }
    return summary, perm["null_diffs_cm"]


def extract_disjoint_block_groups(
    vx: np.ndarray,
    vy: np.ndarray,
    vc: np.ndarray,
    pdist_km: np.ndarray,
    x0: float,
    y0: float,
    dx_m: float,
    dy_m: float,
    block_px: int,
    near_km: float = 2.0,
    bg_km: float = 5.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Aggregate finite pixels onto disjoint spatial blocks without near/bg bleed.

    Any block containing at least one pixel closer than ``bg_km`` is excluded from
    the ``>5 km`` background block sample so near-sinkhole and background blocks stay
    strictly spatially separated.
    """
    bw = abs(dx_m) * block_px
    bh = abs(dy_m) * block_px
    ix = np.floor((vx - x0) / bw).astype(np.int64)
    iy = np.floor((vy - y0) / bh).astype(np.int64)
    span = int(ix.max() - ix.min()) + 16
    cell_ids = (iy - iy.min()) * span + (ix - ix.min())

    near_mask = pdist_km < near_km
    _, inv_n = np.unique(cell_ids[near_mask], return_inverse=True)
    near_block_means = np.bincount(inv_n, weights=vc[near_mask]) / np.bincount(inv_n)

    interior_cells = np.unique(cell_ids[pdist_km < bg_km])
    bg_pure = (pdist_km >= bg_km) & (~np.isin(cell_ids, interior_cells))
    _, inv_b = np.unique(cell_ids[bg_pure], return_inverse=True)
    bg_block_means = np.bincount(inv_b, weights=vc[bg_pure]) / np.bincount(inv_b)
    return near_block_means.astype(np.float64), bg_block_means.astype(np.float64)


def rigid_spatial_shift_test(
    cum_cm: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    sx: np.ndarray,
    sy: np.ndarray,
    obs_diff_cm: float,
    n_attempts: int = 5_000,
    seed: int = 42,
    min_near_coverage: float = 0.5,
    min_near_valid_px: int = 50,
    min_bg_valid_px: int = 1_000,
) -> tuple[dict, np.ndarray]:
    """Translate the entire 29-sinkhole constellation rigidly across the valid scene.

    Preserves both internal sinkhole spacing and kilometer-scale SAR spatial
    autocorrelation while asking whether the observed sinkhole belt sits over
    exceptionally deep subsidence compared with random placements across Karapinar.
    """
    gx, gy = np.meshgrid(x.astype(np.float64), y.astype(np.float64))
    gdist_km = np.sqrt(
        (gx[:, :, None] - sx[None, None, :]) ** 2 + (gy[:, :, None] - sy[None, None, :]) ** 2
    ).min(axis=2) / 1000.0
    m2_full = gdist_km < 2.0
    m5_full = gdist_km < 5.0
    r2, c2 = np.where(m2_full)
    r5, c5 = np.where(m5_full)
    r_mid = int((r2.min() + r2.max()) // 2)
    c_mid = int((c2.min() + c2.max()) // 2)
    dr2, dc2 = r2 - r_mid, c2 - c_mid
    dr5, dc5 = r5 - r_mid, c5 - c_mid

    finite = np.isfinite(cum_cm)
    cum_zero = np.where(finite, cum_cm, 0.0).astype(np.float64)
    cnt_valid = finite.astype(np.int32)
    total_sum = float(cum_zero.sum())
    total_cnt = int(cnt_valid.sum())
    h, w = cum_cm.shape

    rng = np.random.default_rng(seed)
    dr_draws = rng.integers(-r_mid, h - r_mid, size=n_attempts)
    dc_draws = rng.integers(-c_mid, w - c_mid, size=n_attempts)
    min_footprint_px = len(dr2) * min_near_coverage

    shift_diffs: list[float] = []
    for dr, dc in zip(dr_draws, dc_draws):
        rr2 = dr2 + int(dr) + r_mid
        cc2 = dc2 + int(dc) + c_mid
        in2 = (rr2 >= 0) & (rr2 < h) & (cc2 >= 0) & (cc2 < w)
        if int(in2.sum()) < min_footprint_px:
            continue
        rr2_v, cc2_v = rr2[in2], cc2[in2]
        n2 = int(cnt_valid[rr2_v, cc2_v].sum())
        if n2 < min_near_valid_px:
            continue
        s2 = float(cum_zero[rr2_v, cc2_v].sum())

        rr5 = dr5 + int(dr) + r_mid
        cc5 = dc5 + int(dc) + c_mid
        in5 = (rr5 >= 0) & (rr5 < h) & (cc5 >= 0) & (cc5 < w)
        rr5_v, cc5_v = rr5[in5], cc5[in5]
        n5 = int(cnt_valid[rr5_v, cc5_v].sum())
        s5 = float(cum_zero[rr5_v, cc5_v].sum())
        nbg = total_cnt - n5
        if nbg < min_bg_valid_px:
            continue
        sbg = total_sum - s5
        shift_diffs.append((s2 / n2) - (sbg / nbg))

    arr = np.asarray(shift_diffs, dtype=np.float64)
    n_valid = len(arr)
    if n_valid == 0:
        raise RuntimeError("No valid rigid shifts produced inside Karapinar footprint.")
    p_one = float((np.sum(arr <= obs_diff_cm) + 1) / (n_valid + 1))
    p_two = float((np.sum(np.abs(arr) >= abs(obs_diff_cm)) + 1) / (n_valid + 1))
    summary = {
        "n_attempts": int(n_attempts),
        "n_valid_shifts": int(n_valid),
        "obs_diff_cm": float(obs_diff_cm),
        "p_one_sided": p_one,
        "p_two_sided": p_two,
        "null_mean_cm": float(arr.mean()),
        "null_median_cm": float(np.median(arr)),
        "null_q025_cm": float(np.quantile(arr, 0.025)),
        "null_q05_cm": float(np.quantile(arr, 0.05)),
        "null_q95_cm": float(np.quantile(arr, 0.95)),
        "null_q975_cm": float(np.quantile(arr, 0.975)),
    }
    return summary, arr


def analyze_karapinar_sinkholes(
    npz_path: Path = DEFAULT_NPZ,
    geojson_path: Path = DEFAULT_GEOJSON,
    n_perm: int = 10_000,
    n_boot: int = 10_000,
    n_shifts: int = 5_000,
    seed: int = 42,
) -> tuple[dict, dict[str, np.ndarray]]:
    """Run pixel, 1 km block, 2 km block, and rigid-shift statistics on Karapinar."""
    d = np.load(npz_path, allow_pickle=False)
    cum = np.asarray(d["cum_cm"], dtype=np.float32)
    x = np.asarray(d["x"], dtype=np.float64)
    y = np.asarray(d["y"], dtype=np.float64)
    epsg = int(d["epsg"])
    dates = [str(dt) for dt in d["dates"]]

    with open(geojson_path, encoding="utf-8") as fh:
        gj = json.load(fh)
    pts = np.asarray([feat["geometry"]["coordinates"][:2] for feat in gj["features"]], dtype=np.float64)
    sx, sy = lonlat_to_utm(pts[:, 0], pts[:, 1], epsg)

    xx, yy = np.meshgrid(x, y)
    valid = np.isfinite(cum)
    vx, vy, vc = xx[valid], yy[valid], cum[valid].astype(np.float64)
    pdist_km = np.sqrt((vx[:, None] - sx[None, :]) ** 2 + (vy[:, None] - sy[None, :]) ** 2).min(axis=1) / 1000.0

    # Sinkhole coverage check
    min_px_per_sinkhole_km = (
        np.sqrt((vx[:, None] - sx[None, :]) ** 2 + (vy[:, None] - sy[None, :]) ** 2).min(axis=0) / 1000.0
    )
    n_sinkholes_with_px_2km = int((min_px_per_sinkhole_km < 2.0).sum())

    rings: dict[str, dict] = {}
    for label, rmin, rmax in RING_BOUNDS_KM:
        mask = (pdist_km >= rmin) & (pdist_km < rmax if rmax is not None else True)
        vals = vc[mask]
        rings[label] = {
            "n_pixels": int(mask.sum()),
            "mean_cm": float(vals.mean()),
            "median_cm": float(np.median(vals)),
            "std_cm": float(vals.std(ddof=1)),
        }

    near_px = vc[pdist_km < 2.0]
    bg_px = vc[pdist_km >= 5.0]
    pixel_res, pixel_null = summarize_group(near_px, bg_px, "pixel_80m", n_perm=n_perm, n_boot=n_boot, seed=seed)

    dx_m = float(abs(x[1] - x[0]))
    dy_m = float(abs(y[1] - y[0]))
    near_1km, bg_1km = extract_disjoint_block_groups(
        vx, vy, vc, pdist_km, float(x.min()), float(y.min()), dx_m, dy_m, block_px=13
    )
    block1_res, block1_null = summarize_group(
        near_1km, bg_1km, "disjoint_1km_block", n_perm=n_perm, n_boot=n_boot, seed=seed + 1
    )

    near_2km, bg_2km = extract_disjoint_block_groups(
        vx, vy, vc, pdist_km, float(x.min()), float(y.min()), dx_m, dy_m, block_px=26
    )
    block2_res, block2_null = summarize_group(
        near_2km, bg_2km, "disjoint_2km_block", n_perm=n_perm, n_boot=n_boot, seed=seed + 2
    )

    shift_res, shift_null = rigid_spatial_shift_test(
        cum, x, y, sx, sy, obs_diff_cm=pixel_res["diff_mean_cm"], n_attempts=n_shifts, seed=seed
    )

    report = {
        "site": "karapinar",
        "epsg": epsg,
        "dates": dates,
        "n_valid_pixels": int(valid.sum()),
        "n_sinkholes_total": int(len(pts)),
        "n_sinkholes_with_valid_px_2km": n_sinkholes_with_px_2km,
        "rings": rings,
        "pixel_test": pixel_res,
        "block_1km_test": block1_res,
        "block_2km_test": block2_res,
        "rigid_shift_test": shift_res,
        "disclaimer": DISCLAIMER,
    }
    arrays = {
        "pixel_null": pixel_null,
        "block1_null": block1_null,
        "block2_null": block2_null,
        "shift_null": shift_null,
        "near_1km": near_1km,
        "bg_1km": bg_1km,
    }
    return report, arrays


def render_plot(report: dict, arrays: dict[str, np.ndarray], png_path: Path = DEFAULT_PNG) -> Path:
    """Create two-panel publication figure summarizing permutation, block, and shift tests."""
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
            "axes.spines.right": False,
        }
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.2), dpi=180)
    fig.subplots_adjust(wspace=0.28, top=0.80, bottom=0.17, left=0.07, right=0.97)
    fig.suptitle(
        "Karapınar Sinkhole Belt vs. Regional Background (>5 km): Autocorrelation-Aware Significance",
        fontsize=12.5,
        fontweight="bold",
        y=0.95,
    )

    # Panel A: Rigid cluster shift null vs naive 1 km block null
    shift_null = arrays["shift_null"]
    block1_null = arrays["block1_null"]
    obs_px = report["pixel_test"]["diff_mean_cm"]
    obs_1km = report["block_1km_test"]["diff_mean_cm"]
    ci_px = report["pixel_test"]["boot_ci95_cm"]
    ci_1km = report["block_1km_test"]["boot_ci95_cm"]
    p_shift = report["rigid_shift_test"]["p_one_sided"]
    p_1km = report["block_1km_test"]["perm_p_two_sided"]

    ax1.hist(
        shift_null,
        bins=36,
        density=True,
        color="#64748b",
        alpha=0.52,
        edgecolor="#334155",
        linewidth=0.5,
        label=f"Rigid 29-sinkhole shift null (n={report['rigid_shift_test']['n_valid_shifts']})",
    )
    ax1.hist(
        block1_null,
        bins=30,
        density=True,
        histtype="step",
        linewidth=1.8,
        color="#2563eb",
        label=f"1.04 km block permutation null (n={report['block_1km_test']['perm_n']:,})",
    )
    ax1.axvline(obs_px, color="#dc2626", linewidth=2.2, label=f"Observed 0-2 km diff: {obs_px:.2f} cm (shift p={p_shift:.3f})")
    ax1.axvline(
        obs_1km,
        color="#0f766e",
        linewidth=2.0,
        linestyle="--",
        label=f"Observed 1 km block diff: {obs_1km:.2f} cm (perm p={p_1km:.4f})",
    )
    ax1.axvline(
        report["rigid_shift_test"]["null_q05_cm"],
        color="#475569",
        linewidth=1.2,
        linestyle=":",
        label=f"Rigid-shift 5th pct: {report['rigid_shift_test']['null_q05_cm']:.2f} cm",
    )
    ax1.set_title("A. Null Distributions for Mean Difference (0-2 km minus >5 km)")
    ax1.set_xlabel("Mean LOS Difference (cm; negative = deeper near sinkholes)")
    ax1.set_ylabel("Probability Density")
    ax1.set_xlim(min(obs_px, float(shift_null.min())) - 0.8, max(3.6, float(shift_null.max()) + 0.6))
    y_max = ax1.get_ylim()[1]
    ax1.set_ylim(0, y_max * 1.48)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.legend(loc="upper right", fontsize=8.0, frameon=True, framealpha=0.92)

    # Panel B: 1.04 km disjoint block distribution + bootstrap 95% CIs
    near_1km = arrays["near_1km"]
    bg_1km = arrays["bg_1km"]
    rng = np.random.default_rng(7)
    x_pos = [0, 1]
    bp = ax2.boxplot(
        [near_1km, bg_1km],
        positions=x_pos,
        widths=0.38,
        showfliers=False,
        patch_artist=True,
        medianprops={"color": "#0f172a", "linewidth": 2.0},
        whiskerprops={"color": "#475569"},
        capprops={"color": "#475569"},
    )
    for patch, color in zip(bp["boxes"], ["#fca5a5", "#93c5fd"]):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)

    jitter_n = rng.normal(0.0, 0.055, size=len(near_1km))
    jitter_b = rng.normal(1.0, 0.065, size=len(bg_1km))
    ax2.scatter(jitter_b, bg_1km, s=11, color="#2563eb", alpha=0.25, zorder=2, label=f">5 km blocks (n={len(bg_1km)})")
    ax2.scatter(jitter_n, near_1km, s=28, color="#dc2626", alpha=0.85, zorder=3, label=f"0-2 km blocks (n={len(near_1km)})")

    # Mean markers
    ax2.scatter(
        [0, 1],
        [float(near_1km.mean()), float(bg_1km.mean())],
        marker="D",
        s=55,
        color="#0f172a",
        zorder=4,
        label=f"Block means: {near_1km.mean():.2f} vs {bg_1km.mean():.2f} cm",
    )
    ax2.axhline(0.0, color="#94a3b8", linewidth=1.0, linestyle=":")
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(["0-2 km Sinkhole Belt\n(1.04 km disjoint blocks)", ">5 km Background\n(1.04 km disjoint blocks)"])
    ax2.set_ylabel("Cumulative LOS Displacement (cm, 26 Jun-12 Oct 2026)")
    ax2.set_title("B. Spatial-Block Subsidence Contrast & 95% CIs")
    ymin = min(float(near_1km.min()), float(bg_1km.min())) - 0.6
    ymax = max(float(near_1km.max()), float(bg_1km.max())) + 2.0
    ax2.set_ylim(ymin, ymax)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    ax2.text(
        0.03,
        0.96,
        (
            f"Pixel 0-2 km vs >5 km: {obs_px:.2f} cm\n"
            f"  95% boot CI: [{ci_px[0]:.2f}, {ci_px[1]:.2f}] cm\n"
            f"1 km block diff: {obs_1km:.2f} cm\n"
            f"  95% boot CI: [{ci_1km[0]:.2f}, {ci_1km[1]:.2f}] cm"
        ),
        transform=ax2.transAxes,
        fontsize=8.2,
        va="top",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#f8fafc", "edgecolor": "#cbd5e1"},
    )
    ax2.legend(loc="upper right", fontsize=8.0, frameon=True, framealpha=0.92)

    fig.text(
        0.5,
        0.03,
        f"Data: NASA-ISRO NISAR L2 GUNW (provisional) & Tapur & Bozyigit (2015) sinkhole inventory. {DISCLAIMER}",
        ha="center",
        fontsize=8.2,
        color="#475569",
    )
    fig.savefig(png_path, dpi=180)
    plt.close(fig)
    return png_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Statistical significance tests for Karapinar sinkhole subsidence.")
    parser.add_argument("--npz", type=Path, default=DEFAULT_NPZ)
    parser.add_argument("--geojson", type=Path, default=DEFAULT_GEOJSON)
    parser.add_argument("--png", type=Path, default=DEFAULT_PNG)
    parser.add_argument("--n-perm", type=int, default=10_000)
    parser.add_argument("--n-boot", type=int, default=10_000)
    parser.add_argument("--n-shifts", type=int, default=5_000)
    args = parser.parse_args()

    report, arrays = analyze_karapinar_sinkholes(
        npz_path=args.npz,
        geojson_path=args.geojson,
        n_perm=args.n_perm,
        n_boot=args.n_boot,
        n_shifts=args.n_shifts,
    )
    render_plot(report, arrays, png_path=args.png)
    print(json.dumps(report, indent=2))
    print(f"Wrote {args.png}", file=sys.stderr)


if __name__ == "__main__":
    main()
