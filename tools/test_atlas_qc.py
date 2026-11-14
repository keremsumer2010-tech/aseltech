"""Tests for tools/atlas_qc.py (no network, no data files)."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("atlas_qc", Path(__file__).with_name("atlas_qc.py"))
qc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qc)

DATES = [f"2026-07-{d:02d}" for d in range(1, 10)]


def series(disp):
    return {"dates": DATES[:len(disp)], "disp_cm": disp, "lon": 0, "lat": 0}


def test_steady_subsidence_not_flagged():
    flags, steps, _, kept = qc.check(series([0, -1, -2, -3.1, -4, -5.2, -6, -7, -7.8]))
    assert flags == []
    assert abs(kept - (-7.8)) < 1e-6


def test_one_cycle_jump_flagged_and_removed():
    flags, _, detail, kept = qc.check(series([0, -3.25, 0.25, -2.12, -2.26, -0.93, -1.57, -0.87, -12.05]))
    assert "phase_cycle_jump" in flags
    assert abs(kept - (-0.87)) < 0.01
    assert "one phase cycle" in detail


def test_single_date_outlier_flagged():
    flags, _, _, kept = qc.check(series([0, -1.4, 0.48, 0.65, -9.36, -1.3, -3.25, -4.75, -4.32]))
    assert flags == ["single_date_outlier"]
    # steps -1.4, +1.88, +0.17, -10.01, +8.06, -1.95, -1.5, +0.43 -> the -10.01/+8.06 pair is dropped
    assert abs(kept - (-2.37)) < 0.01


def test_large_real_step_not_called_a_cycle():
    flags, _, _, _ = qc.check(series([0, -0.2, -5.3, -6.1, -6.5]))   # 5 cm step: real seasonal pumping signal
    assert flags == []


def test_cycle_constant_matches_l_band():
    assert abs(qc.CYCLE_CM - 12.098) < 0.01
