"""Tests for Karapinar sinkhole statistical permutation, block, and shift suite."""
from __future__ import annotations

import numpy as np

from analysis.pc5.sinkhole_stats import (
    analyze_karapinar_sinkholes,
    bootstrap_diff_ci,
    extract_disjoint_block_groups,
    mann_whitney_u_test,
    permutation_diff_means,
    welch_t_test,
)


def test_permutation_and_bootstrap_separated_vs_null() -> None:
    rng = np.random.default_rng(123)
    near_sep = rng.normal(-4.0, 0.6, size=40)
    bg_sep = rng.normal(-0.5, 0.6, size=120)
    perm_sep = permutation_diff_means(near_sep, bg_sep, n_perm=1000, seed=1)
    lo_s, hi_s, _, _ = bootstrap_diff_ci(near_sep, bg_sep, n_boot=1000, seed=1)
    _, _, p_t = welch_t_test(near_sep, bg_sep)
    _, _, p_u = mann_whitney_u_test(near_sep, bg_sep)

    assert perm_sep["obs_diff_cm"] < -2.5
    assert perm_sep["p_two_sided"] < 0.01
    assert lo_s < hi_s < 0.0
    assert p_t < 1e-6
    assert p_u < 1e-6

    near_null = rng.normal(-1.0, 0.5, size=35)
    bg_null = rng.normal(-1.0, 0.5, size=100)
    perm_null = permutation_diff_means(near_null, bg_null, n_perm=1000, seed=2)
    lo_n, hi_n, _, _ = bootstrap_diff_ci(near_null, bg_null, n_boot=1000, seed=2)
    assert perm_null["p_two_sided"] > 0.05
    assert lo_n < 0.0 < hi_n


def test_disjoint_blocks_exclude_border_bleed() -> None:
    # Construct 26x26 pixels partitioned into two 13x13 blocks cleanly separated in x
    vx = np.array([100.0, 200.0, 300.0, 1200.0, 1300.0, 3000.0, 3100.0])
    vy = np.zeros_like(vx)
    vc = np.array([-4.0, -4.2, -1.0, -0.5, -0.6, -0.4, -0.5])
    # Pixel at x=300 is 3km (mixed with block 0 near pixels); x=1200/1300 in block 1 has pixel at 4.9km (<5km) so excluded!
    pdist_km = np.array([0.5, 1.5, 3.0, 4.9, 5.5, 6.0, 6.5])
    near_b, bg_b = extract_disjoint_block_groups(
        vx, vy, vc, pdist_km, x0=0.0, y0=-520.0, dx_m=80.0, dy_m=80.0, block_px=13
    )
    assert len(near_b) == 1
    assert np.isclose(near_b[0], -4.1)
    assert len(bg_b) == 1
    assert np.isclose(bg_b[0], -0.45)


def test_karapinar_real_counts_and_significance() -> None:
    report, arrays = analyze_karapinar_sinkholes(n_perm=1000, n_boot=1000, n_shifts=600, seed=42)
    assert report["n_valid_pixels"] == 40194
    assert report["rings"]["0-1 km"]["n_pixels"] == 60
    assert report["rings"]["1-2 km"]["n_pixels"] == 176
    assert report["rings"]["0-2 km (combined)"]["n_pixels"] == 236
    assert report["rings"]["2-5 km"]["n_pixels"] == 985
    assert report["rings"][">5 km (background)"]["n_pixels"] == 38973

    assert report["pixel_test"]["diff_mean_cm"] < -3.0
    assert report["block_1km_test"]["n_near"] >= 10
    assert report["block_1km_test"]["diff_mean_cm"] < -2.5
    assert report["block_1km_test"]["perm_p_two_sided"] < 0.01
    assert len(arrays["shift_null"]) >= 200
