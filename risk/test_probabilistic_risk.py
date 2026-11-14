import numpy as np

from risk.probabilistic_risk import beta_and_range, simulate_profile


def test_known_profile_has_expected_dimensionless_beta():
    beta, differential = beta_and_range(np.array([0.0, -20.0]), np.array([0.0, 100.0]))
    assert beta == 0.002
    assert differential == 20.0


def test_zero_sigma_produces_certain_exceedance_and_non_exceedance():
    distances = np.array([0.0, 100.0])
    sigma = np.zeros(2)
    over = simulate_profile(np.array([0.0, -21.0]), sigma, distances, trials=1000, seed=1)
    under = simulate_profile(np.array([0.0, -5.0]), sigma, distances, trials=1000, seed=1)
    assert over["p_beta_exceed"] == {"1/500": 1.0, "1/1000": 1.0}
    assert over["p_diff_gt_10cm"] == 1.0
    assert under["p_beta_exceed"] == {"1/500": 0.0, "1/1000": 0.0}
    assert under["p_diff_gt_10cm"] == 0.0

