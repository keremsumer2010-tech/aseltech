import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))
from decompose import decimal_year, fit  # noqa: E402

# 12-day sampling over one year (Nov 2025 -> Oct 2026), like the full NISAR chain
T = np.array([decimal_year("2025-11-24") + k * 12 / 365.25 for k in range(28)])


def synth(v, C, low_month, a=0.0, noise=0.0, seed=0, shape=(5, 4)):
    rng = np.random.default_rng(seed)
    t_low = (low_month - 0.5) / 12            # middle of that month
    phi = 2 * np.pi * (t_low - 0.5)            # peak half a year before the low
    A, B = C * np.sin(phi), C * np.cos(phi)
    d = a + v * (T - T.mean()) + A * np.sin(2 * np.pi * T) + B * np.cos(2 * np.pi * T)
    stack = np.repeat(d[:, None, None], np.prod(shape), axis=1).reshape(len(T), *shape)
    return stack + rng.normal(0, noise, stack.shape)


def test_decimal_year():
    assert decimal_year("2026-01-01") == 2026.0
    assert decimal_year("2026-07-02") == pytest.approx(2026 + 182 / 365)


def test_recovers_exact_parameters():
    out = fit(T, synth(-20.0, 4.0, 9))
    assert np.allclose(out["v_cm_per_yr"], -20.0, atol=1e-4)
    assert np.allclose(out["amp_cm"], 4.0, atol=1e-4)
    assert np.all(out["low_month"] == 9)
    assert np.all(out["reason"] == 0) and np.allclose(out["r2"], 1.0)


def test_recovers_with_noise_within_tolerance():
    out = fit(T, synth(-15.0, 3.0, 8, noise=0.5, shape=(40, 40)))
    assert np.nanmedian(out["v_cm_per_yr"]) == pytest.approx(-15.0, abs=0.3)
    assert np.nanmedian(out["amp_cm"]) == pytest.approx(3.0, abs=0.2)
    assert np.nanmedian(np.abs(out["low_month"] - 8)) <= 1
    # reported standard error should be of the same size as the actual scatter
    assert 0.5 < np.nanstd(out["v_cm_per_yr"]) / np.nanmedian(out["v_se"]) < 2.0


def test_nan_epochs_are_ignored():
    d = synth(-10.0, 2.0, 7)
    d[[3, 9, 17], 0, 0] = np.nan
    out = fit(T, d)
    assert out["n_valid"][0, 0] == len(T) - 3
    assert out["v_cm_per_yr"][0, 0] == pytest.approx(-10.0, abs=1e-4)


def test_too_few_points_and_short_span_give_nan_and_reason():
    d = synth(-10.0, 2.0, 7)
    d[7:, 0, 0] = np.nan          # 7 points -> reason 1
    d[10:, 0, 1] = np.nan         # 10 points over ~0.3 yr -> reason 2
    d[:, 0, 2] = np.nan           # empty -> reason 1
    out = fit(T, d)
    assert out["reason"][0, 0] == 1 and np.isnan(out["v_cm_per_yr"][0, 0])
    assert out["reason"][0, 1] == 2 and np.isnan(out["amp_cm"][0, 1])
    assert out["reason"][0, 2] == 1
    assert out["reason"][1, 1] == 0


def test_shape_mismatch_raises():
    with pytest.raises(ValueError):
        fit(T[:-1], synth(-1.0, 1.0, 1))


def test_chunked_equals_unchunked():
    d = synth(-12.0, 2.5, 6, noise=0.3, shape=(30, 25))
    a = fit(T, d)
    b = fit(T, d, chunk=97)
    for k in ("v_cm_per_yr", "amp_cm", "r2", "reason"):
        assert np.allclose(a[k], b[k], equal_nan=True)
