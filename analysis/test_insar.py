import numpy as np
import pytest

from insar import (
    coh_to_float, los_to_vertical, mask_coherence, mask_components, pair_to_cm,
    phase_to_cm, reference, wavelength_from_frequency,
)

LAM = wavelength_from_frequency(1.239e9)  # Central Valley GUNW centerFrequency (docs/qa/PC1.md)


def test_wavelength():
    assert LAM == pytest.approx(0.24196, abs=1e-5)


def test_two_pi_is_half_wavelength():
    # 2*pi phase = lambda/2 of LOS change = 12.098 cm for lambda = 0.24196 m
    assert abs(phase_to_cm(np.array([2 * np.pi]), LAM)[0]) == pytest.approx(LAM / 2 * 100, rel=1e-5)
    assert abs(phase_to_cm(np.array([2 * np.pi]), LAM)[0]) == pytest.approx(12.098, abs=1e-3)


def test_sign_positive_phase_is_subsidence():
    # MintPy convention: positive phase = away from satellite -> negative displacement
    assert phase_to_cm(np.array([1.0]), LAM)[0] < 0
    assert phase_to_cm(np.array([-1.0]), LAM)[0] > 0


def test_coherence_mask_uint8_and_float():
    a = np.ones((2, 2), np.float32)
    coh8 = np.array([[255, 0], [77, 76]], np.uint8)  # 77/255=0.302, 76/255=0.298
    m = mask_coherence(a, coh8, 0.3)
    assert np.isfinite(m[0, 0]) and np.isnan(m[0, 1]) and np.isfinite(m[1, 0]) and np.isnan(m[1, 1])
    m2 = mask_coherence(a, np.array([[0.9, np.nan], [0.1, 0.5]]), 0.3)
    assert np.isnan(m2).tolist() == [[False, True], [True, False]]
    assert coh_to_float(np.uint8(255)) == pytest.approx(1.0)


def test_conncomp_mask():
    m = mask_components(np.ones((1, 3)), np.array([[0, 1, 2]], np.uint16))
    assert np.isnan(m[0, 0]) and np.isfinite(m[0, 1:]).all()


def test_reference_zeroes_reference_pixel():
    rng = np.random.default_rng(0)
    a = rng.normal(5, 1, (50, 50)).astype(np.float32)
    a[20:27, 30:37] = 7.0
    out = reference(a, (23, 33), radius=3)
    assert out[23, 33] == pytest.approx(0.0, abs=1e-6)
    assert np.allclose(out + 7.0, a)


def test_reference_ignores_nan_and_raises_when_empty():
    a = np.full((10, 10), 2.0, np.float32)
    a[5, 5] = np.nan
    assert reference(a, (5, 5), 1)[4, 4] == 0.0
    with pytest.raises(ValueError):
        reference(np.full((10, 10), np.nan), (5, 5), 1)


def test_los_to_vertical():
    assert los_to_vertical(np.array([-10.0]), 60.0)[0] == pytest.approx(-20.0, rel=1e-6)
    assert los_to_vertical(np.array([-10.0]), 0.0)[0] == pytest.approx(-10.0)


def test_pair_chain_synthetic_bowl():
    # Synthetic subsidence bowl of -3 cm LOS at centre, stable edges, reference at corner
    yy, xx = np.mgrid[0:60, 0:60]
    true_cm = -3.0 * np.exp(-((yy - 30) ** 2 + (xx - 30) ** 2) / 100.0)
    unw = -true_cm / 100.0 * 4 * np.pi / LAM + 1.234  # arbitrary constant phase offset
    coh = np.full(unw.shape, 200, np.uint8)
    coh[0:3, 50:60] = 10
    out = pair_to_cm(unw, coh, LAM, ref_rc=(5, 5), radius=3)
    assert out[30, 30] == pytest.approx(-3.0, abs=0.01)
    assert abs(out[5, 5]) < 1e-4
    assert np.isnan(out[0, 55])
