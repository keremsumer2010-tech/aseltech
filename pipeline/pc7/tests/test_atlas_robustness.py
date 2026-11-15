"""Network-free unit tests for the atlas robustness helpers."""
from __future__ import annotations

import numpy as np

from pipeline.pc7.atlas_robustness import block_headline, fast_deramp, kendall_tau_b, parse_subset_overrides


def test_fast_deramp_removes_plane_without_network() -> None:
    yy, xx = np.mgrid[0:64, 0:80]
    plane = (3.0 + xx * 0.2 - yy * 0.1).astype(np.float32)

    corrected = fast_deramp(plane, step=4)

    assert np.nanmax(np.abs(corrected)) < 1e-4


def test_block_headline_reports_min_eligible_median_and_p2() -> None:
    values = np.full((26, 26), -2.0, dtype=np.float32)
    values[:13, :13] = -5.0
    inside = np.ones(values.shape, dtype=bool)

    headline, p2 = block_headline(values, inside)

    assert headline == -5.0
    assert p2 == -5.0


def test_block_headline_rejects_no_data() -> None:
    values = np.full((26, 26), np.nan, dtype=np.float32)
    inside = np.ones(values.shape, dtype=bool)

    assert block_headline(values, inside) == (None, None)


def test_kendall_tau_detects_reversed_ranking() -> None:
    assert kendall_tau_b([1, 2, 3], [3, 2, 1]) == -1.0


def test_subset_override_parses_city_path_without_network() -> None:
    result = parse_subset_overrides([r"beijing=C:\scratch\global_beijing"])

    assert result["beijing"].as_posix() == "C:/scratch/global_beijing"


