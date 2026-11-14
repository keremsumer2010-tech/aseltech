"""Unit tests for analysis.pc5.uncertainty_map."""
from __future__ import annotations

import math

import numpy as np
import pytest

from analysis.pc5.uncertainty_map import (
    compute_chain_sigma_cm,
    cramer_rao_phase_std,
    lonlat_to_utm,
    normalize_coherence,
    phase_std_to_los_cm,
    utm_to_lonlat,
)


def test_unit_coherence_gives_zero_uncertainty() -> None:
    assert cramer_rao_phase_std(1.0, looks=208.0) == 0.0
    arr = cramer_rao_phase_std(np.array([1.0, 1.0]), looks=25.0)
    np.testing.assert_allclose(arr, [0.0, 0.0], atol=1e-15)
    assert phase_std_to_los_cm(0.0, wavelength_m=0.242) == 0.0


def test_decreasing_coherence_strictly_increases_sigma() -> None:
    cohs = np.array([0.95, 0.80, 0.60, 0.40, 0.30])
    sig_phi = cramer_rao_phase_std(cohs, looks=208.0)
    sig_cm = phase_std_to_los_cm(sig_phi, wavelength_m=0.242)
    assert np.all(np.diff(sig_phi) > 0.0)
    assert np.all(np.diff(sig_cm) > 0.0)


def test_known_numerical_example() -> None:
    # gamma = 0.6, L = 25, lambda = 0.24 m:
    # sigma_phi = sqrt(1 - 0.36) / (0.6 * sqrt(50)) = 0.8 / (0.6 * sqrt(50))
    lam = 0.24
    expected_phi = 0.8 / (0.6 * math.sqrt(50.0))
    expected_cm = (lam / (4.0 * math.pi)) * expected_phi * 100.0

    got_phi = cramer_rao_phase_std(0.6, looks=25.0)
    got_cm = phase_std_to_los_cm(got_phi, wavelength_m=lam)
    assert got_phi == pytest.approx(expected_phi, rel=1e-12)
    assert got_cm == pytest.approx(expected_cm, rel=1e-12)


def test_chain_quadrature_and_uint8_coherence() -> None:
    # Two identical pairs with coh_uint8 = 153 (gamma = 153/255 = 0.6), L = 25, lam = 0.24
    c_u8 = np.full((3, 3), 153, dtype=np.uint8)
    c_u8[0, 0] = 51  # below mask
    m1 = normalize_coherence(c_u8) >= 0.3
    m2 = np.ones((3, 3), dtype=bool)
    m2[2, 2] = False  # invalid in second pair only

    sig_tot, valid = compute_chain_sigma_cm(
        [c_u8, c_u8],
        [0.24, 0.24],
        valid_masks=[m1, m2],
        looks=25.0,
    )
    single_cm = phase_std_to_los_cm(cramer_rao_phase_std(0.6, looks=25.0), 0.24)
    expected_two = math.sqrt(2.0) * single_cm

    assert not valid[0, 0] and np.isnan(sig_tot[0, 0])
    assert not valid[2, 2] and np.isnan(sig_tot[2, 2])
    assert valid[1, 1]
    assert sig_tot[1, 1] == pytest.approx(expected_two, rel=1e-6)


def test_utm_lonlat_roundtrip() -> None:
    lons = np.array([-119.5, -119.02173, 33.53056])
    lats = np.array([36.1, 36.01119, 37.71818])
    for epsg, lo, la in [(32611, lons[:2], lats[:2]), (32636, lons[2:], lats[2:])]:
        x, y = lonlat_to_utm(lo, la, epsg)
        lo2, la2 = utm_to_lonlat(x, y, epsg)
        np.testing.assert_allclose(lo2, lo, atol=1e-7)
        np.testing.assert_allclose(la2, la, atol=1e-7)
