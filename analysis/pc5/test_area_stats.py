"""Unit tests for analysis.pc5.area_stats."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from analysis.pc5.area_stats import compute_site_area_stats
from analysis.pc5.uncertainty_map import SITE_BBOX


def test_area_stats_synthetic_stack(tmp_path: Path) -> None:
    # Build synthetic UTM 11N grid fully inside central_valley bbox (-120.2, 35.6, -119.0, 36.6)
    nx, ny = 30, 30
    x = np.arange(260000.0, 260000.0 + nx * 80.0, 80.0, dtype=np.float64)
    y = np.arange(4000000.0, 4000000.0 - ny * 80.0, -80.0, dtype=np.float64)

    stack = np.zeros((3, ny, nx), dtype=np.float16)
    # Date 1: 100 pixels at -3.0 cm (< -2 cm only -> 100 * 0.0064 = 0.64 km2)
    stack[1, :10, :10] = -3.0
    # Date 2: 200 pixels < -2 cm (1.28 km2), 169 pixels at -6.0 cm (< -5 cm -> 1.0816 -> 1.08 km2)
    stack[2, :13, :13] = -6.0
    stack[2, 13:16, :10] = -2.5  # 30 extra -> 169 + 30 = 199 pixels -> 1.2736 -> 1.27 km2
    stack[2, 20, 20] = np.nan

    f = tmp_path / "synthetic_stack.npz"
    np.savez_compressed(
        f,
        cum_stack_cm=stack,
        dates=np.array(["2026-06-28", "2026-07-10", "2026-07-22"]),
        x=x,
        y=y,
        epsg=np.int32(32611),
        quality="provisional",
    )

    st = compute_site_area_stats("central_valley", stack_path=f, bbox=SITE_BBOX["central_valley"])
    assert st["dates"] == ["2026-06-28", "2026-07-10", "2026-07-22"]
    assert st["area_km2_lt_2cm"] == [0.0, 0.64, 1.27]
    assert st["area_km2_lt_5cm"] == [0.0, 0.0, 1.08]
    assert st["max_subsidence_cm"] == [0.0, -3.0, -6.0]
    assert st["valid_pixels"] == nx * ny - 1


def test_real_sites_area_stats_monotonic_and_consistent() -> None:
    cv_stack = Path("analysis/out/central_valley_cum_stack.npz")
    kp_stack = Path("analysis/out/karapinar_cum_stack.npz")
    if not (cv_stack.exists() and kp_stack.exists()):
        return

    cv = compute_site_area_stats("central_valley")
    assert len(cv["dates"]) == 8
    assert cv["area_km2_lt_2cm"][0] == 0.0
    assert cv["area_km2_lt_5cm"][0] == 0.0
    assert cv["area_km2_lt_2cm"][-1] > cv["area_km2_lt_5cm"][-1] > 200.0
    assert abs(cv["max_subsidence_cm"][-1] - (-7.8)) <= 0.15

    kp = compute_site_area_stats("karapinar")
    assert len(kp["dates"]) == 9
    assert kp["area_km2_lt_2cm"][0] == 0.0
    assert kp["area_km2_lt_2cm"][-1] > kp["area_km2_lt_5cm"][-1] > 2.0
    assert abs(kp["max_subsidence_cm"][-1] - (-5.9)) <= 0.15
