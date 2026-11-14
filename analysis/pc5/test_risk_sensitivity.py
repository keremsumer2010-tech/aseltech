"""Unit tests for analysis.pc5.risk_sensitivity."""
from __future__ import annotations

import json
from pathlib import Path

from analysis.pc5.risk_sensitivity import (
    DEFAULT_ASSETS,
    DEFAULT_INFRA,
    DEFAULT_NPZ,
    classify_with_thresholds,
    evaluate_all_segments,
    rank_top_n,
    sweep_thresholds,
)


def _make_feat(osm_id: int, grad: float, max_cm: float) -> dict:
    return {
        "type": "Feature",
        "properties": {
            "osm_id": osm_id,
            "name": f"seg-{osm_id}",
            "type": "canal",
            "gradient_mm_per_km": grad,
            "max_cm": max_cm,
            "length_km": 2.0,
        },
    }


def test_classify_with_thresholds_boundaries() -> None:
    assert classify_with_thresholds(10.0, -2.0, high_grad=10.0, high_sub=10.0) == "high"
    assert classify_with_thresholds(9.9, -2.0, high_grad=10.0, high_sub=10.0) == "medium"
    assert classify_with_thresholds(10.0, -1.99, high_grad=10.0, high_sub=10.0) == "medium"
    assert classify_with_thresholds(2.0, -10.0, high_grad=10.0, high_sub=10.0) == "high"
    assert classify_with_thresholds(2.0, -7.5, high_grad=10.0, high_sub=7.5) == "high"
    assert classify_with_thresholds(10.0, -2.0, high_grad=12.5, high_sub=12.5) == "medium"
    assert classify_with_thresholds(4.0, -2.0, high_grad=10.0, high_sub=10.0) == "low"


def test_sweep_monotonicity_and_top10_stability_synthetic() -> None:
    feats = [
        _make_feat(100 + i, grad=50.0 - i * 2.0, max_cm=-6.0) for i in range(10)
    ] + [
        _make_feat(200, grad=8.5, max_cm=-3.5),
        _make_feat(201, grad=11.0, max_cm=-2.5),
        _make_feat(202, grad=3.0, max_cm=-8.0),
    ]
    rows = sweep_thresholds(feats)
    assert len(rows) == 9
    # Looser thresholds must yield >= as many high-risk segments as tighter thresholds
    by_key = {(r["high_grad"], r["high_sub"]): r["high"] for r in rows}
    assert by_key[(7.5, 7.5)] >= by_key[(10.0, 10.0)] >= by_key[(12.5, 12.5)]
    assert all(r["top10_all_same_order"] for r in rows)
    assert all(r["top10_high_same_order"] for r in rows)


def test_real_central_valley_baseline_matches_assets_json() -> None:
    if not (DEFAULT_INFRA.exists() and DEFAULT_NPZ.exists() and DEFAULT_ASSETS.exists()):
        return
    evaluated, _ = evaluate_all_segments(DEFAULT_INFRA, DEFAULT_NPZ)
    assets = json.loads(DEFAULT_ASSETS.read_text(encoding="utf-8"))
    summary = assets["summary"]
    rows = sweep_thresholds(evaluated)
    base = next(r for r in rows if r["high_grad"] == 10.0 and r["high_sub"] == 10.0)

    assert base["total"] == summary["evaluated_segments"] == 645
    assert base["high"] == summary["high_risk_count"] == 81
    assert base["medium"] == summary["medium_risk_count"] == 131
    assert base["low"] == summary["low_risk_count"] == 433

    asset_top10_ids = [f["properties"]["osm_id"] for f in assets["features"][:10]]
    eval_top10_ids = [f["properties"]["osm_id"] for f in rank_top_n(evaluated, 10)]
    assert eval_top10_ids == asset_top10_ids
    assert all(r["top10_high_same_order"] for r in rows)
