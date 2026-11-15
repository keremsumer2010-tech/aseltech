"""Build data/global/home_summary.json: the ONLY file the home page reads numbers from (PC10).

Every value is read from a source file at build time; nothing is typed in by hand except
fixed wording. Run after every `build_atlas.py` (build_atlas.py calls this automatically).

    python pipeline/pc10/build_home_summary.py
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = ROOT / "data" / "global"

CALIBRATION_NOTE = (
    "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
    "(NASA-JPL and ISRO), not by our team."
)
ONE_LINER = (
    "We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: "
    "{n} basins measured with one open pipeline on the same {days} days, every number traceable to its file, "
    "and every headline checked against GPS, NASA's OPERA product and the literature."
)
SEMARANG_ID = "semarang"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _gnss_from_report() -> tuple[float, float]:
    """Cross-station Pearson r and final-epoch RMSE (cm) of the 10 Central Valley GPS stations."""
    text = (ROOT / "docs" / "story" / "validation_report.md").read_text(encoding="utf-8")
    m = re.search(r"All 10 stations.*?`r = ([0-9.]+)`.*?`RMSE = ([0-9.]+) cm`", text, re.S)
    if not m:
        raise ValueError("GPS r/RMSE not found in docs/story/validation_report.md")
    return float(m.group(1)), float(m.group(2))


def _top5(atlas: dict) -> list[dict]:
    out = []
    for r in atlas["reliable"][:5]:
        note = (r.get("note") or "").strip()
        if not note and r.get("valid_fraction") is None:
            note = "valid-pixel fraction not recorded for this region; kept with caution"
        out.append(
            {
                "id": r["id"],
                "name": r["name"],
                "country": r["country"],
                "rank": r["rank_reliable"],
                "rate_cm_per_100d_common": r.get("rate_cm_per_100d_common"),
                "max_cm_los": r["max_cm_los"],
                "confidence": r["confidence"],
                "valid_fraction": r.get("valid_fraction"),
                "note": note,
            }
        )
    return out


def _qc_story(atlas: dict) -> dict:
    qc = _load(G / "qc_flags.json")
    before = _load(G / SEMARANG_ID / "qc_before.json")
    pts = _load(G / SEMARANG_ID / "points.json")
    pt = next(p for p in pts if p.get("kind") == "most_subsiding")
    sem = next(r for r in atlas["regions"] if r["id"] == SEMARANG_ID)

    b_cm = before["disp_cm"]
    jump = round(b_cm[-1] - b_cm[-2], 1)
    cycle = qc.get("cycle_cm", 12.1)
    changelog = _load(G / "atlas_changelog.json")
    fixed_ref = []
    for e in changelog.get("entries", []):
        for v in e.get("value_changes", []):
            if "reference" in v.get("reason", "").lower():
                fixed_ref.append({"id": v["id"], "before_cm": v["old_cm"], "after_cm": v["new_cm"]})
    return {
        "headline": "The atlas caught its own error",
        "semarang": {
            "before_cm": round(b_cm[-1], 1),
            "after_cm": sem["max_cm_los"],
            "why": (
                f"the whole {round(b_cm[-1], 1)} cm came from one step of {abs(jump)} cm, "
                f"one full L-band phase cycle ({cycle} cm): an unwrapping error; "
                "re-processed, the peak moved to the subsiding north coast"
            ),
        },
        "series_before": {"dates": before["dates"], "disp_cm": b_cm},
        "series_after": {"dates": pt["dates"], "disp_cm": [round(v, 2) for v in pt["disp_cm"]]},
        "fixed_reference": fixed_ref,
        "flagged": sorted(k for k in qc.get("flags", {}) if k in {r["id"] for r in atlas["regions"]}),  # atlas regions only (PC1)
        "source": "docs/story/atlas_top5_check.md, data/global/qc_flags.json, data/global/atlas_changelog.json",
    }


def build() -> dict:
    atlas = _load(G / "atlas.json")
    vital = _load(G / "vital_signs.json")
    storage = _load(ROOT / "data" / "central_valley_fullyear" / "storage_loss.json")
    opera = next(x for x in _load(G / "opera_check.json") if x["id"] == "mexico_city")
    gnss_r, gnss_rmse = _gnss_from_report()
    n, n_rel, n_ind = atlas["n_regions"], atlas["n_reliable"], atlas["n_indicative"]
    days = atlas["common_window_days"]

    kpis = [
        {
            "key": "regions",
            "label": "basins in one atlas",
            "value": n,
            "unit": "",
            "detail": f"{n_rel} reliable, {n_ind} indicative",
            "source": "data/global/atlas.json",
        },
        {
            "key": "people",
            "label": "people living on ground sinking more than 5 cm",
            "value": vital["people_on_sinking_ground"],
            "unit": "",
            "detail": f"{vital['area_km2_lt_minus5cm']} km\u00b2 in the measured basins (GHSL 2025 population)",
            "source": "data/global/vital_signs.json",
        },
        {
            "key": "gnss",
            "label": "agreement with 10 GPS stations (Central Valley)",
            "value": gnss_r,
            "unit": "r",
            "detail": f"RMSE {gnss_rmse} cm at the final date",
            "source": "docs/story/validation_report.md",
        },
        {
            "key": "opera",
            "label": "agreement with NASA JPL OPERA (Mexico City)",
            "value": opera["r"],
            "unit": "r",
            "detail": (
                f"OPERA {opera['opera_period'][0]} to {opera['opera_period'][1]} vs NISAR "
                f"{opera['period'][0]} to {opera['period'][1]}; different seasons, so a shape check, not a same-day match"
            ),
            "source": "data/global/opera_check.json",
        },
        {
            "key": "storage",
            "label": "permanent aquifer storage lost per year (Central Valley)",
            "value": storage["volume_km3_per_yr"],
            "unit": "km\u00b3/yr",
            "detail": "inelastic compaction \u2248 storage that does not come back",
            "source": "data/central_valley_fullyear/storage_loss.json",
        },
    ]

    return {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "one_liner": ONE_LINER.format(n=n, days=days),
        "common_window": atlas["common_window"],
        "kpis": kpis,
        "top5": _top5(atlas),
        "qc_story": _qc_story(atlas),
        "calibration_note": CALIBRATION_NOTE,
        "quality": "provisional",
    }


def main() -> None:
    summary = build()
    out = G / "home_summary.json"
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(summary['kpis'])} KPIs, top5={[t['id'] for t in summary['top5']]})")


if __name__ == "__main__":
    main()
