"""Unit tests for tools/bulletin.py (PC8, ATLAS_PLANI.md)."""
from __future__ import annotations

import json
from pathlib import Path

from tools.bulletin import ATLAS_PATH, CALIBRATION_NOTICE, render_index, render_region_bulletin


def test_bulletin_renders_all_seeded_atlas_regions(tmp_path: Path) -> None:
    atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    regions = atlas["regions"]
    generated = []
    for reg in regions:
        out = render_region_bulletin(reg, out_dir=tmp_path)
        if out is not None:
            generated.append((reg, out))
            txt = out.read_text(encoding="utf-8")
            assert "NISAR Pulse Bulletin" in txt
            assert CALIBRATION_NOTICE in txt
            assert "cm/100d" in txt
            assert "CONFIDENCE:" in txt
            if reg["id"] == "central_valley":
                assert "O2 probabilistic infrastructure risk (assets_prob.json)" in txt
                assert "Beta Max" in txt

    idx = render_index(regions, generated, out_dir=tmp_path)
    assert idx.exists()
    idx_txt = idx.read_text(encoding="utf-8")
    assert "Rate (cm/100d)" in idx_txt
    assert "Confidence" in idx_txt
    assert len(generated) >= 8
