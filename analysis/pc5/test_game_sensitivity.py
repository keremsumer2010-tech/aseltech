"""Unit tests for analysis.pc5.game_sensitivity."""
from __future__ import annotations

import numpy as np

from analysis.pc5.game_sensitivity import (
    TARGET_VERT_108D_CM,
    compute_calibrated_demand_multiplier,
    run_monte_carlo,
    simulate_108d_calibration,
    simulate_24_months,
)


def test_calibrated_108d_reproduces_nisar_target() -> None:
    k = compute_calibrated_demand_multiplier(TARGET_VERT_108D_CM)
    sim_108d = simulate_108d_calibration(calibration_factor=k)
    assert np.isclose(sim_108d, TARGET_VERT_108D_CM, atol=0.05)


def test_subsidence_monotonic_in_clay_thickness_and_skv() -> None:
    d_thin = simulate_24_months(b0=30.0)[0]
    d_thick = simulate_24_months(b0=90.0)[0]
    # More negative displacement means stronger subsidence
    assert d_thick < d_thin < 0.0

    d_soft = simulate_24_months(skv=5.0e-4)[0]
    d_stiff = simulate_24_months(skv=1.5e-4)[0]
    assert d_soft < d_stiff < 0.0


def test_inelastic_subsidence_does_not_rebound_under_wet_year() -> None:
    tot_wet_y2, el_w, inel_w = simulate_24_months(year1_wy="Critical", year2_wy="Wet", pumping_pct=50.0, surface_alloc_pct=100.0)
    assert inel_w <= 0.0
    assert abs(tot_wet_y2 - (el_w + inel_w)) < 1e-9


def test_monte_carlo_ensemble_statistics() -> None:
    res = run_monte_carlo(n_trials=200, seed=12345)
    s24 = res["summary"]["sub_24m_fixed"]
    assert s24["p10_severe"] < s24["p50_median"] < s24["p90_mild"] < 0.0
    assert 0.0 < res["summary"]["within_10pct_fraction"] < 1.0
