"""Unit and integration tests for analysis.decomp.error_budget."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from analysis.decomp.error_budget import (
    compute_error_budget,
    ionosphere_stats_cm,
    pair_noise_from_npz,
    phase_to_los_cm,
    propagate_chain_std,
)


def test_phase_to_los_cm_sign_and_validation():
    wl = 0.24196324
    # Positive phase corresponds to negative LOS displacement (moving away = subsidence)
    disp = phase_to_los_cm(np.array([0.0, 2.0 * math.pi, -math.pi]), wl)
    assert np.isclose(disp[0], 0.0)
    assert np.isclose(disp[1], -(wl / 2.0) * 100.0, atol=1e-6)
    assert np.isclose(disp[2], (wl / 4.0) * 100.0, atol=1e-6)

    with pytest.raises(ValueError):
        phase_to_los_cm(np.array([1.0]), 0.0)


def test_propagate_chain_std_scalar_and_vector():
    res_scalar = propagate_chain_std(0.5, n_pairs=4, incidence_deg=39.1)
    assert res_scalar["n_pairs"] == 4
    assert np.isclose(res_scalar["sigma_pair_rms_los_cm"], 0.5)
    assert np.isclose(res_scalar["sigma_total_los_cm"], 1.0)
    assert np.isclose(
        res_scalar["sigma_total_vertical_cm_estimate"],
        1.0 / math.cos(math.radians(39.1)),
    )
    assert "independent" in res_scalar["assumption"].lower()

    res_vec = propagate_chain_std([0.3, 0.4], incidence_deg=0.0)
    assert res_vec["n_pairs"] == 2
    assert np.isclose(res_vec["sigma_total_los_cm"], 0.5)
    assert np.isclose(res_vec["sigma_total_vertical_cm_estimate"], 0.5)

    with pytest.raises(ValueError):
        propagate_chain_std(0.5)  # missing n_pairs for scalar
    with pytest.raises(ValueError):
        propagate_chain_std(-0.1, n_pairs=3)


def test_ionosphere_stats_cm_ramp_and_reference():
    wl = 0.24196324
    # Construct ion screen spanning [0, 4*pi] rad -> [0, -lambda] * 100 cm LOS
    ramp_1d = np.linspace(0.0, 4.0 * math.pi, 101)
    ion_rad = np.broadcast_to(ramp_1d, (15, 101)).copy()
    stats = ionosphere_stats_cm(ion_rad, wl, ref_rc=(7, 50), ref_radius=2)

    expected_span = 0.98 * wl * 100.0  # p99 - p1 across uniform [0, lambda*100]
    assert np.isclose(stats["p1_p99_range_cm"], expected_span, atol=0.15)
    assert np.isclose(stats["ref_p1_p99_range_cm"], stats["p1_p99_range_cm"], atol=1e-9)
    assert abs(stats["ref_p50_cm"]) < 0.2


def test_pair_noise_excludes_beta_precal(tmp_path: Path):
    shape = (30, 30)
    rng = np.random.default_rng(7)
    base_kwargs = dict(
        unw=rng.normal(0.0, 0.2, size=shape).astype(np.float32),
        coh=np.full(shape, 240, dtype=np.uint8),
        conncomp=np.ones(shape, dtype=np.uint8),
        ion=np.zeros(shape, dtype=np.float32),
        wavelength=np.array(0.242),
        date1=np.array("2026-06-16"),
        date2=np.array("2026-06-28"),
    )

    beta_path = tmp_path / "beta.npz"
    np.savez(beta_path, quality=np.array("beta-precal"), **base_kwargs)
    assert pair_noise_from_npz(beta_path, ref_rc=(15, 15)) is None

    prov_path = tmp_path / "prov.npz"
    np.savez(prov_path, quality=np.array("provisional"), **base_kwargs)
    out = pair_noise_from_npz(prov_path, ref_rc=(15, 15))
    assert out is not None
    assert out["quality"] == "provisional"
    expected_cm = (0.242 / (4.0 * math.pi) * 0.2) * 100.0
    assert abs(out["sigma_raw_stable_scene_cm"] - expected_cm) < 0.08


def test_compute_error_budget_workspace():
    subset_dir = Path("pipeline/subset/central_valley")
    if not subset_dir.exists():
        pytest.skip("central_valley subset not present")
    res = compute_error_budget()
    assert res["quality"] == "provisional"
    assert res["n_pairs"] == 7
    assert res["chain_noise"]["post_deramp_local_high_coh"]["n_pairs"] == 7
    assert math.isfinite(res["chain_noise"]["post_deramp_local_high_coh"]["sigma_total_los_cm"])
    assert math.isfinite(res["ionosphere_summary_cm"]["max_p1_p99_range_cm"])
    assert res["gnss_validation_summary"]["n_stations"] == 10
