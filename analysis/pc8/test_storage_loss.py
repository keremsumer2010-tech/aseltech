"""Unit tests for permanent aquifer storage loss integration (O1, PC8)."""
from __future__ import annotations

import numpy as np
import pytest

from analysis.pc8.storage_loss import compute_storage_loss_metrics


def test_constant_velocity_known_area() -> None:
    """Constant -5.0 cm/yr over 100x100 pixels (80 m x 80 m) -> exact 0.0032 km3/yr."""
    shape = (104, 104)
    v_vert = np.full(shape, -5.0, dtype=np.float64)
    se_vert = np.full(shape, 0.5, dtype=np.float64)
    ok = np.zeros(shape, dtype=bool)
    ok[2:102, 2:102] = True  # exact 10,000 pixels = 64.0 km2
    px_area_m2 = 80.0 * 80.0

    out = compute_storage_loss_metrics(v_vert, se_vert, ok, px_area_m2, subsidence_threshold_cm_yr=1.0)
    active = out["active_subsiding_gt_threshold"]
    net = out["net_all_valid_in_bbox"]

    assert active["n_pixels"] == 10000
    assert active["area_km2"] == pytest.approx(64.0, rel=1e-6)
    assert active["volume_km3_per_yr"] == pytest.approx(0.0032, rel=1e-6)
    assert active["volume_million_m3_per_yr"] == pytest.approx(3.2, rel=1e-6)
    assert net["volume_km3_per_yr"] == pytest.approx(0.0032, rel=1e-6)
    assert active["se_block_km3_per_yr"] > active["se_independent_km3_per_yr"]
