"""Single source of numbers for the home page and the 3-minute jury path (PC1).

Reads atlas.json, vital_signs.json, opera_check.json, storage_loss.json, independent_validation.json,
qc_flags.json and atlas_changelog.json; writes data/global/home_summary.json.
Run after every atlas rebuild:  python tools/build_home_summary.py
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
J = lambda p: json.loads((ROOT / p).read_text(encoding="utf-8"))

atlas = J("data/global/atlas.json")
vital = J("data/global/vital_signs.json")
opera = {r["id"]: r for r in J("data/global/opera_check.json")}
storage = J("data/central_valley_fullyear/storage_loss.json")
indep = J("data/global/independent_validation.json")["regions"]
qc = J("data/global/qc_flags.json")["flags"]

regions = atlas["regions"]
reliable = [r for r in regions if r["confidence"] in ("high", "medium")]
cw = atlas.get("common_window") or regions[0].get("common_window")
gnss = indep["central_valley"]
mx = opera.get("mexico_city", {})

def region_card(r):
    return {"id": r["id"], "name": r["name"], "country": r.get("country", ""), "rank": r["rank"],
            "rate_cm_per_100d_common": r.get("rate_cm_per_100d_common"), "max_cm_los": r.get("max_cm_los"),
            "confidence": r["confidence"], "valid_fraction": r.get("valid_fraction"),
            "note": "low valid coverage (11.6 %); kept with caution" if r["id"] == "konya_plain" else ""}

out = {
    "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "one_liner": ("We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: "
                  f"{atlas['n_regions']} basins measured with one open pipeline on the same {(datetime.fromisoformat(cw[1]) - datetime.fromisoformat(cw[0])).days} days, "
                  "every number traceable to its file, and every headline checked against GPS, NASA's OPERA product and the literature."),
    "common_window": cw,
    "kpis": [
        {"key": "regions", "label": "basins in one atlas", "value": atlas["n_regions"], "unit": "",
         "detail": f"{atlas['n_reliable']} reliable, {atlas['n_indicative']} indicative", "source": "data/global/atlas.json"},
        {"key": "people", "label": "people living on ground sinking more than 5 cm", "value": vital["people_on_sinking_ground"], "unit": "",
         "detail": f"{vital['area_km2_lt_minus5cm']} km² in the measured basins (GHSL 2025 population)", "source": "data/global/vital_signs.json"},
        {"key": "gnss", "label": "agreement with 10 GPS stations (Central Valley)", "value": gnss["r"], "unit": "r",
         "detail": f"RMSE {gnss['rmse_cm']} cm at the final date", "source": gnss["source"]},
        {"key": "opera", "label": "agreement with NASA JPL OPERA (Mexico City)", "value": mx.get("r"), "unit": "r",
         "detail": "same summer season, OPERA one year earlier (2025 vs 2026)", "source": "data/global/opera_check.json"},
        {"key": "storage", "label": "permanent aquifer storage lost per year (Central Valley)", "value": storage["volume_km3_per_yr"], "unit": "km³/yr",
         "detail": "inelastic compaction ≈ storage that does not come back", "source": "data/central_valley_fullyear/storage_loss.json"},
    ],
    "top5": [region_card(r) for r in reliable[:5]],
    "qc_story": {
        "headline": "The atlas caught its own error",
        "semarang": {"before_cm": -12.1, "after_cm": -6.2,
                     "why": "the whole −12.1 cm came from one step of 11.2 cm, one full L-band phase cycle (12.1 cm): an unwrapping error; re-processed, the peak moved to the subsiding north coast"},
        # headline-point series before (recorded in the PC1 audit, 15 Nov) and after re-processing (current points.json)
        "series_before": {"dates": ["2026-06-25", "2026-07-07", "2026-07-19", "2026-08-12", "2026-08-24", "2026-09-05", "2026-09-17", "2026-09-29", "2026-10-11"],
                          "disp_cm": [0.0, -3.25, 0.25, -2.12, -2.26, -0.93, -1.57, -0.87, -12.05]},
        "series_after": next(({"dates": h["dates"], "disp_cm": h["disp_cm"]} for h in J("data/global/semarang/points.json") if h.get("kind") == "most_subsiding"), None),
        "fixed_reference": [{"id": "tehran", "before_cm": -3.5, "after_cm": -7.4}],
        "flagged": sorted(qc.keys()),
        "source": "docs/story/atlas_top5_check.md, data/global/qc_flags.json, data/global/atlas_changelog.json",
    },
    "calibration_note": "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.",
    "quality": "provisional",
}
(ROOT / "data/global/home_summary.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print("home_summary:", atlas["n_regions"], "regions;", [k["key"] + "=" + str(k["value"]) for k in out["kpis"]])
