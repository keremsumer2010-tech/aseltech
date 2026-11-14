import numpy as np
import pytest

from insar import (
    choose_reference, coh_to_float, cycle_outliers, deramp, deramp_elevation, remove_islands, los_to_vertical, mask_coherence, mask_components, pair_to_cm,
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


def test_choose_reference_picks_most_coherent_valid_window():
    coh = np.full((40, 40), 0.5, np.float32)
    coh[10:17, 25:32] = 0.95
    valid = np.ones((40, 40), bool)
    r, c, m = choose_reference(coh, valid, radius=3, stride=1)
    assert (r, c) == (13, 28) and m == pytest.approx(0.95)
    valid[13, 28] = False  # invalid pixel in that window -> must move away
    r2, c2, _ = choose_reference(coh, valid, radius=3, stride=1)
    assert not (abs(r2 - 13) <= 3 and abs(c2 - 28) <= 3)
    excl = np.zeros((40, 40), bool)
    excl[:] = True
    with pytest.raises(ValueError):
        choose_reference(coh, None, exclude=excl)


def test_cycle_outliers():
    a = np.full((27, 27), -2.0, np.float32)
    a[10:13, 4] = -2.0 - 12.1  # one-cycle jump strip
    a[20, 20] = -3.0           # small real deviation stays
    out = cycle_outliers(a, thr_cm=6.0, block=9)
    assert np.isnan(out[11, 4]) and out[20, 20] == -3.0 and out[0, 0] == -2.0


def test_remove_islands():
    a = np.full((30, 30), np.nan, np.float32)
    a[0:20, 0:20] = 1.0      # big region (400 px) stays
    a[25:27, 25:27] = -10.0  # 4-px island goes
    out = remove_islands(a, min_px=50)
    assert np.isfinite(out[5, 5]) and np.isnan(out[25, 25])


def test_deramp_removes_plane_keeps_local_bowl():
    yy, xx = np.mgrid[0:100, 0:120].astype(np.float32)
    bowl = -4.0 * np.exp(-((yy - 50) ** 2 + (xx - 60) ** 2) / 50.0)
    ramp = 0.05 * xx - 0.03 * yy + 2.0
    a = bowl + ramp
    a[0:5, 0:5] = np.nan
    out = deramp(a, order=1, step=1)
    # after deramp, bowl depth relative to surroundings is preserved
    assert (np.nanmedian(out[:, :20]) - out[50, 60]) == pytest.approx(4.0, abs=0.1)
    assert abs(np.nanmedian(out[:, :20]) - np.nanmedian(out[:, -20:])) < 0.05
    assert np.isnan(out[0, 0])


def test_deramp_elevation_removes_height_term():
    rng = np.random.default_rng(1)
    yy, xx = np.mgrid[0:80, 0:90].astype(np.float32)
    h = np.where(xx > 60, (xx - 60) * 30.0, 80.0) + rng.normal(0, 5, xx.shape)  # flat floor + foothills
    bowl = -5.0 * np.exp(-((yy - 40) ** 2 + (xx - 30) ** 2) / 60.0)
    a = bowl + 0.02 * xx + 3.0 * h / 1000.0 + 1.0
    out, k = deramp_elevation(a, h, step=1)
    assert k == pytest.approx(3.0, abs=0.3)
    assert (np.median(out[:, :10]) - out[40, 30]) == pytest.approx(5.0, abs=0.3)
    assert np.std(out[:, 70:]) < 0.3  # foothill gradient gone


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


def test_two_geometry_inversion():
    from vertical_ew import solve_eu
    # asc LOS (to sensor) points west-up, desc points east-up (illustrative unit vectors)
    e1, u1 = np.array([-0.6]), np.array([0.78])
    e2, u2 = np.array([0.6]), np.array([0.78])
    E_true, U_true = 1.5, -8.0
    d1, d2 = E_true * e1 + U_true * u1, E_true * e2 + U_true * u2
    E, U = solve_eu(d1, d2, e1, u1, e2, u2)
    assert E[0] == pytest.approx(E_true, abs=1e-5) and U[0] == pytest.approx(U_true, abs=1e-5)
    E, U = solve_eu(d1, d2, e1, u1, e1, u1)  # identical geometry -> singular -> NaN
    assert np.isnan(E[0]) and np.isnan(U[0])
