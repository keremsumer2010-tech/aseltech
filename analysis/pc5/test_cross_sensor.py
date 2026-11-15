"""Unit tests for B1 multi-frequency cross-sensor analysis (analysis/pc5/cross_sensor.py)."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

from analysis.pc5.cross_sensor import (
    NISAR_LAMBDA_CM,
    S1_LAMBDA_CM,
    analyze_lband_coherence_series,
    evaluate_nisar_vs_gnss,
    evaluate_phase_ambiguity_margins,
    regression_metrics,
    run_cross_sensor_analysis,
)

ROOT = Path(__file__).resolve().parents[2]
# Raw NISAR subsets (*.npz) live outside the repository since 2026-11-15; skip the tests that read them.
HAS_RAW = any((ROOT / "pipeline" / "subset" / "central_valley").glob("*.npz"))
needs_raw = pytest.mark.skipif(not HAS_RAW, reason="raw NISAR .npz subsets are kept outside the repository")


def test_regression_metrics_exact() -> None:
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y = 2.0 * x - 1.0
    m = regression_metrics(x, y)
    assert m["n"] == 4
    assert math.isclose(m["r"], 1.0, abs_tol=1e-6)
    assert math.isclose(m["slope"], 2.0, abs_tol=1e-6)
    assert math.isclose(m["intercept_cm"], -1.0, abs_tol=1e-6)


@needs_raw
def test_nisar_vs_gnss_and_coherence_outputs() -> None:
    gps = json.loads((ROOT / "data" / "central_valley" / "validation.json").read_text(encoding="utf-8"))
    gnss_eval = evaluate_nisar_vs_gnss(gps)
    assert gnss_eval["n_stations"] == 10
    tm = gnss_eval["terminal_vertical_metrics"]
    assert tm["r"] > 0.85
    assert 0.5 < tm["rmse_cm"] < 2.0

    coh = analyze_lband_coherence_series()
    assert coh["n_pairs_total"] == 25
    assert coh["seasonal_summary"]["summer_jun_oct"]["mean_ag_core_valid_frac"] > 0.70

    cv_pts = json.loads((ROOT / "data" / "central_valley" / "points.json").read_text(encoding="utf-8"))
    fy_pts = json.loads((ROOT / "data" / "central_valley_fullyear" / "points.json").read_text(encoding="utf-8"))
    amb = evaluate_phase_ambiguity_margins(cv_pts, fy_pts)
    assert math.isclose(amb["wavelength_ratio_L_over_C"], NISAR_LAMBDA_CM / S1_LAMBDA_CM, abs_tol=0.01)
    assert amb["cv_108d_top5"][0]["intervals_exceeding_c_band_half_fringe_1_39cm"] >= 1
    assert amb["cv_108d_top5"][0]["intervals_exceeding_l_band_half_fringe_6_05cm"] == 0


@needs_raw
def test_offline_cross_sensor_pipeline_clean_artifacts(tmp_path: Path) -> None:
    opera_dir = tmp_path / "opera"
    s1_dir = tmp_path / "s1"
    fig_path = tmp_path / "pc5_cross_sensor.png"
    out = run_cross_sensor_analysis(
        offline=True,
        opera_dir=opera_dir,
        s1_out_dir=s1_dir,
        fig_out=fig_path,
    )
    assert out["cmr_opera_disp_s1"]["opera_summer_2026_hits"] == 0
    assert out["cmr_opera_disp_s1"]["sentinel1c_slc_summer_2026_hits"] == 55
    assert (opera_dir / "opera_disp_cv_coverage.json").exists()
    assert (s1_dir / "cross_sensor.json").exists()
    assert fig_path.exists()
    # Verify checked-in artifacts exist and no raw NetCDF-4 or temp files remain in repo
    assert (ROOT / "pipeline" / "subset" / "opera_disp" / "opera_disp_cv_coverage.json").exists()
    assert (ROOT / "data" / "central_valley_s1" / "cross_sensor.json").exists()
    assert (ROOT / "docs" / "story" / "media" / "pc5_cross_sensor.png").exists()
    leftovers = list((ROOT / "pipeline" / "subset" / "opera_disp").glob("*.nc*"))
    assert leftovers == []
