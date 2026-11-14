"""Tests for Central Valley hydro-agricultural driver correlation and power analysis."""
from __future__ import annotations

import numpy as np

from analysis.pc5.drivers_analysis import analyze_drivers, corr_stats, critical_r_alpha, exact_perm_corr_p


def test_exact_permutation_and_critical_r() -> None:
    # Monotonic series of length 7 should have r=1.0 and tiny p
    x = np.arange(7, dtype=np.float64)
    y = 2.0 * x + 1.0
    stats = corr_stats(x, y)
    assert np.isclose(stats["pearson_r"], 1.0)
    assert np.isclose(stats["spearman_rho"], 1.0)
    assert stats["p_perm_exact"] <= 2.0 / 5040.0 + 1e-9

    # Orthogonal/zero-corr synthetic vector gives high p
    xo = np.array([-2.0, -1.0, 0.0, 1.0, 2.0, 0.0])
    yo = np.array([1.0, -1.0, -2.0, -1.0, 1.0, 2.0])
    p_zero = exact_perm_corr_p(xo, yo)
    assert p_zero > 0.5

    # Standard statistical critical thresholds for Pearson r
    assert np.isclose(critical_r_alpha(8, 0.05), 0.7067, atol=1e-3)
    assert np.isclose(critical_r_alpha(7, 0.05), 0.7545, atol=1e-3)
    assert np.isclose(critical_r_alpha(6, 0.05), 0.8114, atol=1e-3)


def test_real_drivers_reproduce_json_values_and_show_n8_limits() -> None:
    report = analyze_drivers()
    assert report["n_epochs"] == 8
    assert report["interval_days"] == [12, 12, 24, 12, 12, 12, 24]

    cum = report["cumulative_correlations"]["subsidence_cm"]
    sm_l0 = cum["soil_moisture"]["lag0"]["pearson_r"]
    irr_l0 = cum["irrigation_index"]["lag0"]["pearson_r"]
    sm_l1 = cum["soil_moisture"]["lag1"]["pearson_r"]
    rep = report["reported_lag_corr_detail"]

    assert np.isclose(sm_l0, rep["corr_soil_moisture_vs_subsidence"], atol=1e-3)
    assert np.isclose(irr_l0, rep["corr_irrigation_index_vs_subsidence"], atol=1e-3)
    assert np.isclose(sm_l1, rep["lag1_12d_soil_moisture_vs_subsidence"], atol=1e-3)

    # None of the N=8 cumulative correlations reach alpha=0.05 two-sided significance
    for drv in cum.values():
        for lag in drv.values():
            assert not lag["significant_alpha05"]
