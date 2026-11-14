"""Unit tests for analysis.pc5.detectability."""
from __future__ import annotations

import json
from pathlib import Path

from analysis.pc5.detectability import compute_city_detectability, run_detectability


def test_compute_city_detectability_threshold() -> None:
    sig = compute_city_detectability(
        "test_strong",
        {"max_subsidence_cm": -5.0, "period": ["2026-06-28", "2026-10-14"], "quality": "provisional"},
        {"median_sigma_cm": 0.3, "p90_sigma_cm": 0.5, "n_pairs": 7, "valid_pixel_fraction": 0.6},
    )
    assert sig["detectable"] is True
    assert sig["snr"] > 10.0

    weak = compute_city_detectability(
        "test_weak",
        {"max_subsidence_cm": -0.4, "period": ["2026-06-28", "2026-10-14"], "quality": "provisional"},
        {"median_sigma_cm": 0.3, "p90_sigma_cm": 0.5, "n_pairs": 7, "valid_pixel_fraction": 0.6},
    )
    assert weak["detectable"] is False
    assert weak["snr"] < 2.0


def test_run_detectability_outputs(tmp_path: Path) -> None:
    j_out = tmp_path / "detectability.json"
    m_out = tmp_path / "detectability.md"
    p_out = tmp_path / "pc5_detectability.png"
    res = run_detectability(json_out=j_out, md_out=m_out, png_out=p_out)
    assert j_out.exists() and m_out.exists() and p_out.exists()
    parsed = json.loads(j_out.read_text(encoding="utf-8"))
    assert parsed["n_cities"] >= 9
    assert parsed["overall_min_detectable_rate_cm_per_100d"]["median"] > 0
