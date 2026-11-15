"""Automated consistency checks between site HTML/JSON and data/global/atlas.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "data" / "global" / "atlas.json"
EXPOSURE_PATH = ROOT / "data" / "global" / "exposure_atlas.json"
VITAL_PATH = ROOT / "data" / "global" / "vital_signs.json"
CV_SUMMARY_PATH = ROOT / "data" / "central_valley" / "summary.json"
STORAGE_PATH = ROOT / "data" / "central_valley_fullyear" / "storage_loss.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_vital_signs_matches_atlas_and_exposure() -> None:
    atlas = _load(ATLAS_PATH)
    exposure = _load(EXPOSURE_PATH)
    vital = _load(VITAL_PATH)

    regions = atlas["regions"]
    reliable = [r for r in regions if not r.get("indicative_only")]
    reliable.sort(
        key=lambda r: (
            r.get("rate_cm_per_100d_common")
            if r.get("rate_cm_per_100d_common") is not None
            else r.get("rate_cm_per_100d", 999.0)
        )
    )
    assert reliable, "Expected at least one reliable region in atlas.json"
    top = reliable[0]
    top_rate = (
        top["rate_cm_per_100d_common"]
        if top.get("rate_cm_per_100d_common") is not None
        else top["rate_cm_per_100d"]
    )

    assert vital["cities_measured"] == atlas["n_regions"] == len(regions)
    assert vital["fastest"]["id"] == top["id"]
    assert not top.get("indicative_only"), "vital_signs.fastest must be a reliable region"
    assert vital["fastest"]["rate_cm_per_100d"] == top_rate

    totals = exposure["totals_excluding_nested_karapinar"]
    assert vital["people_on_sinking_ground"] == totals["people_lt_minus5cm"]
    assert vital["people_on_sinking_ground_gt2cm"] == totals["people_lt_minus2cm"]
    assert vital["area_km2_lt_minus5cm"] == totals["area_km2_lt_minus5cm"]


def test_web_pages_match_atlas_counts_and_headline_numbers() -> None:
    atlas = _load(ATLAS_PATH)
    cv = _load(CV_SUMMARY_PATH)
    storage = _load(STORAGE_PATH)
    reliable = [r for r in atlas["regions"] if not r.get("indicative_only")]
    top = min(
        reliable,
        key=lambda r: r.get("rate_cm_per_100d_common", r.get("rate_cm_per_100d", 999.0)),
    )

    n_reg = str(atlas["n_regions"])
    n_rel = str(atlas["n_reliable"])
    n_ind = str(atlas["n_indicative"])
    cv_peak = f"{abs(cv['max_subsidence_cm']):.1f}"
    storage_vol = f"{storage['volume_km3_per_yr']:.4f}"

    for rel_path in ("web/index.html", "web/atlas.html"):
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        assert "NISAR data are provisional." in text, f"Missing calibration notice in {rel_path}"
        assert n_reg in text, f"Expected n_regions={n_reg} in {rel_path}"

    atlas_html = (ROOT / "web" / "atlas.html").read_text(encoding="utf-8")
    assert n_rel in atlas_html and n_ind in atlas_html, "web/atlas.html meta/stats must match reliable/indicative counts"
    assert "ranked by common 93-day window" in atlas_html.lower()

    index_html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert n_rel in index_html and n_ind in index_html, "web/index.html must match reliable/indicative counts"
    assert "home3.js" in index_html
    assert f"{storage['volume_km3_per_yr']:.2f}" in index_html or str(storage['volume_km3_per_yr']) in index_html
