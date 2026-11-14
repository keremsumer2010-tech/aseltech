"""Verification tests for PC9 full-year Q08 outputs (`data/central_valley_fullyear/`)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "central_valley_fullyear"
STORY_MD = ROOT / "docs" / "story" / "fullyear.md"
PLOT_PNG = ROOT / "docs" / "story" / "media" / "pc9_fullyear_point.png"
PLOT_12D_PNG = ROOT / "docs" / "story" / "media" / "pc9_fullyear_12day_steps.png"
PLOT_MONTHLY_PNG = ROOT / "docs" / "story" / "media" / "pc9_fullyear_monthly_steps.png"


def test_mixed_quality_labels_and_provenance():
    meta = json.loads((DATA_DIR / "meta.json").read_text(encoding="utf-8"))
    summary = json.loads((DATA_DIR / "summary.json").read_text(encoding="utf-8"))
    decomp = json.loads((DATA_DIR / "decomp.json").read_text(encoding="utf-8"))

    for doc in (meta, summary, decomp):
        assert doc["quality"] == "mixed"
        assert "BETA" in doc["quality_note"] or "beta" in doc["quality_note"].lower()
        assert "NISAR" in doc["quality_note"]

    assert len(meta["beta_precal_pairs"]) == 18
    assert len(meta["provisional_pairs"]) == 7
    assert "beta-precal" in meta["notes"]
    assert "beta-precal" in decomp["notes"]
    assert summary["n_pairs"] == 25
    assert summary["n_beta_pairs"] == 18
    assert summary["n_provisional_pairs"] == 7
    assert summary["period"] == ["2025-11-24", "2026-10-14"]


def test_dates_points_and_pngs_match_contract():
    meta = json.loads((DATA_DIR / "meta.json").read_text(encoding="utf-8"))
    points = json.loads((DATA_DIR / "points.json").read_text(encoding="utf-8"))
    decomp = json.loads((DATA_DIR / "decomp.json").read_text(encoding="utf-8"))

    assert len(meta["dates"]) == 26
    assert decomp["dates"] == meta["dates"]
    assert decomp["status"] == "ok"
    assert decomp["valid_fraction"] > 0.30
    assert len(points) == 12
    for pt in points:
        assert pt["dates"] == meta["dates"]
        assert len(pt["disp_cm"]) == 26
        assert all(v is None or np.isfinite(v) for v in pt["disp_cm"])

    disp_pngs = sorted((DATA_DIR / "disp").glob("*.png"))
    assert len(disp_pngs) == 26
    for p in disp_pngs:
        assert p.stat().st_size <= 20_000_000

    for key, fname in (("permanent_cm_per_yr", "decomp_permanent.png"), ("seasonal_amp_cm", "decomp_seasonal.png")):
        assert decomp[key]["png"] == fname
        img_path = DATA_DIR / fname
        assert img_path.exists()
        assert img_path.stat().st_size <= 20_000_000
        im = Image.open(img_path)
        assert im.mode == "RGBA"
        assert im.size == (1200, 1000)


def test_story_and_figure_exist_and_no_exclamations():
    assert PLOT_PNG.exists()
    assert PLOT_PNG.stat().st_size > 50_000
    assert PLOT_PNG.stat().st_size <= 20_000_000
    text = STORY_MD.read_text(encoding="utf-8")
    prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    assert "!" not in prose
    assert "beta-precal" in text
    assert "provisional" in text
    assert "-20.3 cm" in text
    assert "-16.8" in text or "-16.77" in text


def test_timestep_charts_and_a6_section():
    import sys

    pc9_dir = str(Path(__file__).resolve().parent)
    if pc9_dir not in sys.path:
        sys.path.insert(0, pc9_dir)
    from plot_fullyear_timesteps import compute_monthly_bins, compute_pair_steps

    for img_path in (PLOT_12D_PNG, PLOT_MONTHLY_PNG):
        assert img_path.exists()
        assert 50_000 < img_path.stat().st_size <= 20_000_000
        with Image.open(img_path) as im:
            assert im.format == "PNG"
            assert im.mode == "RGBA"
            im.load()

    text = STORY_MD.read_text(encoding="utf-8")
    assert "pc9_fullyear_12day_steps.png" in text
    assert "pc9_fullyear_monthly_steps.png" in text
    assert "patterns and rhythms at different time steps" in text.lower()

    points = {p["id"]: p for p in json.loads((DATA_DIR / "points.json").read_text(encoding="utf-8"))}
    for pid in ("p01", "p06", "p11"):
        pt = points[pid]
        steps = compute_pair_steps(pt)
        assert len(steps) == 25
        assert abs(sum(s["dv_cm"] for s in steps) - pt["disp_cm"][-1]) < 1e-9

        bins = compute_monthly_bins(pt)
        assert len(bins) == 11
        assert bins[0]["ym"] == "2025-12"
        assert bins[-1]["ym"] == "2026-10"
        assert abs(sum(b["dv_cm"] for b in bins) - pt["disp_cm"][-1]) < 1e-9

    p01_bins = {b["ym"]: b for b in compute_monthly_bins(points["p01"])}
    assert round(p01_bins["2026-03"]["dv_cm"], 2) == 2.63
    assert round(p01_bins["2026-04"]["dv_cm"], 2) == -9.51
