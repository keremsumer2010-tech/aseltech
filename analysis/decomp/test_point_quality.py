"""Unit and integration tests for analysis.decomp.point_quality."""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from analysis.decomp.point_quality import analyze_point_series, analyze_points_file


def test_analyze_point_series_clean_linear():
    pt = {
        "id": "p_clean",
        "name": "Synthetic Clean",
        "kind": "most_subsiding",
        "dates": ["2026-01-01", "2026-04-02", "2026-07-02", "2026-10-01", "2027-01-01"],
        "disp_cm": [0.0, -1.5, -3.0, -4.5, -6.0],
    }
    res = analyze_point_series(pt)
    assert res["n_valid"] == 5
    assert abs(res["rate_cm_per_yr"] - (-6.0)) < 0.05
    assert res["r2"] > 0.999
    assert res["residual_std_cm"] < 0.05
    assert res["unwrapping_flag"] == "OK"


def test_analyze_point_series_elevated_and_unwrap_suspect_jumps():
    # +4.5 cm exceeds pi/2 (~3.02 cm) -> ELEVATED_JUMP
    pt_elev = {
        "id": "p_elev",
        "name": "Synthetic Elevated",
        "kind": "median",
        "dates": ["2026-06-28", "2026-07-10", "2026-07-22", "2026-08-15"],
        "disp_cm": [0.0, -0.2, 4.3, 4.2],
    }
    res_elev = analyze_point_series(pt_elev)
    assert res_elev["unwrapping_flag"] == "ELEVATED_JUMP"
    assert abs(res_elev["max_jump_cm"] - 4.5) < 1e-9
    assert res_elev["max_jump_pair"] == "2026-07-10->2026-07-22"

    # +8.0 cm exceeds pi (~6.05 cm, lambda/4) -> UNWRAP_SUSPECT
    pt_susp = {
        "id": "p_susp",
        "name": "Synthetic Suspect",
        "kind": "median",
        "dates": ["2026-06-28", "2026-07-10", "2026-07-22", "2026-08-15"],
        "disp_cm": [0.0, -0.2, 7.8, 0.1],
    }
    assert analyze_point_series(pt_susp)["unwrapping_flag"] == "UNWRAP_SUSPECT"


def test_analyze_point_series_insufficient_and_nan():
    pt = {
        "id": "p_few",
        "name": "Missing",
        "kind": "median",
        "dates": ["2026-06-28", "2026-07-10", "2026-07-22"],
        "disp_cm": [0.0, None, -0.5],
    }
    res = analyze_point_series(pt)
    assert res["n_valid"] == 2
    assert res["unwrapping_flag"] == "INSUFFICIENT_DATA"
    assert math.isnan(res["rate_cm_per_yr"])


def test_analyze_points_file_central_valley():
    cv_pts = Path("data/central_valley/points.json")
    if not cv_pts.exists():
        pytest.skip("central_valley points.json not present")
    report = analyze_points_file(cv_pts)
    assert report["n_points"] == 12
    assert report["suspect_ids"] == []  # none exceed pi rad (lambda/4 = 6.05 cm)
    assert set(report["elevated_ids"]) == {"p03", "p08"}
    by_id = {p["id"]: p for p in report["points"]}
    assert abs(by_id["p01"]["end_disp_cm"] - (-7.8)) < 1e-6
