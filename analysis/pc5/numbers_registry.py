"""Canonical Numbers Registry & Cross-Document Audit for NISAR Pulse.

Scans web/*.html, web/*.js, docs/story/*.md, docs/story/slides.html, and
docs/story/technical_note.html, maps headline numbers to their authoritative
JSON sources in data/, flags discrepancies, and writes:
  - data/numbers_registry.json
  - docs/story/numbers_registry.md

Usage:
    python analysis/pc5/numbers_registry.py
    python analysis/pc5/numbers_registry.py --update-qa
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DISCLAIMER = (
    "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
    "(NASA-JPL and ISRO), not by our team."
)

SCAN_GLOBS = [
    "web/*.html",
    "web/*.js",
    "docs/story/*.md",
    "docs/story/slides.html",
    "docs/story/technical_note.html",
]

# File ownership for discrepancy routing (docs/GOREV_DAGILIMI.md)
FILE_OWNERS = {
    "web/index.html": "PC9 / PC3",
    "web/science.html": "PC9 / PC3",
    "web/data.html": "PC9 / PC3",
    "web/faq.html": "PC9 / PC3",
    "web/explorer.html": "PC9 / PC3",
    "web/panel.html": "PC3",
    "web/app.js": "PC9 / PC3",
    "web/explorer.js": "PC9 / PC3",
    "web/docs.js": "PC9 / PC3",
    "docs/story/slides.html": "PC4",
    "docs/story/technical_note.html": "PC4",
    "docs/story/technical_note.md": "PC4",
    "docs/story/press_summary.md": "PC4",
    "docs/story/project_page.md": "PC4",
    "docs/story/judge_faq.md": "PC4",
    "docs/story/submission_form.md": "PC8 / PC4",
    "docs/story/exposure.md": "PC8",
    "docs/story/storage_loss.md": "PC7 / PC3",
    "docs/story/key_findings.md": "PC5",
    "docs/story/key_findings_public.md": "PC5 (Mehmet)",
    "docs/story/atlas_validation.md": "PC5",
    "docs/story/literature_comparison.md": "PC5",
    "docs/story/cross_sensor.md": "PC5",
    "docs/story/drivers_analysis.md": "PC5",
    "docs/story/sinkhole_stats.md": "PC5",
    "docs/story/global_atlas.md": "PC10",
}

UNIT_PATTERN = re.compile(
    r"(?P<num>[−\-+]?\d[\d,]*(?:\.\d+)?)\s*"
    r"(?P<unit>cm/100\s*d|cm/yr|cm/year|cm/yıl|km³/yr|km3/yr|km³|km3|km²|km2|mm/km|cm|%|people|persons)"
    r"|\b(?P<stat>RMSE|r)\s*[=:]\s*(?P<sval>[−\-+]?\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def _load_json(rel_path: str) -> Any:
    p = ROOT / rel_path
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def build_canonical_entries() -> list[dict[str, Any]]:
    """Build canonical metric entries directly from repository JSON files."""
    entries: list[dict[str, Any]] = []

    def add(
        eid: str,
        value: Any,
        unit: str,
        meaning: str,
        source_file: str,
        source_key: str,
        quality: str,
        verdict: str,
        patterns: list[str],
        note: str = "",
    ) -> None:
        entries.append(
            {
                "id": eid,
                "value": value,
                "unit": unit,
                "meaning": meaning,
                "source_file": source_file,
                "source_key": source_key,
                "quality": quality,
                "verdict": verdict,
                "used_in": [],
                "note": note,
                "_patterns": patterns,
            }
        )

    # 1. Central Valley (108-day provisional)
    cv_sum = _load_json("data/central_valley/summary.json")
    if cv_sum:
        add(
            "cv_max_los_cm",
            cv_sum["max_subsidence_cm"],
            "cm",
            "Central Valley peak 108-day LOS subsidence (2026-06-28 to 2026-10-14)",
            "data/central_valley/summary.json",
            "max_subsidence_cm",
            cv_sum.get("quality", "provisional"),
            "approved",
            [r"[−\-]?7\.8\s*cm"],
            f"Reference range: {cv_sum.get('range_cm')} cm.",
        )
        add(
            "cv_max_vert_cm_est",
            cv_sum["max_subsidence_vertical_cm_estimate"],
            "cm",
            "Central Valley peak 108-day vertical subsidence estimate (LOS / cos 39.1 deg)",
            "data/central_valley/summary.json",
            "max_subsidence_vertical_cm_estimate",
            cv_sum.get("quality", "provisional"),
            "approved",
            [r"[−\-]?10\.1\s*cm"],
            "Assumes purely vertical motion; label as estimate.",
        )
        add(
            "cv_rate_yr_est",
            cv_sum["rate_cm_per_yr_estimate"],
            "cm/yr",
            "Central Valley summer-extrapolated LOS rate estimate (108 d -> 365.25 d)",
            "data/central_valley/summary.json",
            "rate_cm_per_yr_estimate",
            cv_sum.get("quality", "provisional"),
            "preliminary",
            [r"[−\-]?26\.4\s*cm/(?:yr|year)"],
            "Summer-only extrapolation; overstates full-year permanent rate (-16.8 cm/yr). Must be labeled estimate.",
        )

    cv_area = _load_json("data/central_valley/area_stats.json")
    if cv_area:
        add(
            "cv_area_gt5cm_km2",
            cv_area["area_km2_lt_5cm"][-1],
            "km2",
            "Central Valley area with >5 cm LOS subsidence by 2026-10-14",
            "data/central_valley/area_stats.json",
            "area_km2_lt_5cm[-1]",
            cv_area.get("quality", "provisional"),
            "approved",
            [r"239\.5\s*km[²2]", r"240\s*km[²2]"],
            "Exact: 239.54 km2 (rounded to 240 km2 in public headlines).",
        )
        add(
            "cv_area_gt2cm_km2",
            cv_area["area_km2_lt_2cm"][-1],
            "km2",
            "Central Valley area with >2 cm LOS subsidence by 2026-10-14",
            "data/central_valley/area_stats.json",
            "area_km2_lt_2cm[-1]",
            cv_area.get("quality", "provisional"),
            "approved",
            [r"1,?578\.3\s*km[²2]", r"1,?579\.2\s*km[²2]"],
            "1578.3 km2 in area_stats.json; 1579.2 km2 on CDL grid in exposure.json.",
        )

    cv_unc = _load_json("data/central_valley/uncertainty/meta.json")
    if cv_unc:
        add(
            "cv_sigma_median_cm",
            cv_unc["median_sigma_cm"],
            "cm",
            "Central Valley median Cramér-Rao formal phase-noise uncertainty (L=208, 7 pairs)",
            "data/central_valley/uncertainty/meta.json",
            "median_sigma_cm",
            cv_unc.get("quality", "provisional"),
            "approved",
            [r"0\.294\s*cm", r"0\.29\s*cm"],
            "Short-scale phase noise lower bound only; excludes atmosphere.",
        )

    cv_val = _load_json("data/central_valley/validation.json")
    if cv_val and isinstance(cv_val, list):
        rmses = [float(s["rmse_cm"]) for s in cv_val if "rmse_cm" in s]
        med_rmse = round(float(np.median(rmses)), 3)
        add(
            "cv_gps_median_rmse_cm",
            med_rmse,
            "cm",
            "Median InSAR-vs-GPS RMSE across 10 NGL stations in Central Valley",
            "data/central_valley/validation.json",
            "median(rmse_cm)",
            "provisional",
            "approved",
            [r"1\.004\s*cm", r"1\.00?\s*cm"],
            "All 10 stations median 1.004 cm; 6 stations with r>=0.4 have median 0.8 cm.",
        )

    cv_assets = _load_json("data/central_valley/assets.json")
    if cv_assets:
        s_as = cv_assets.get("summary", {})
        add(
            "cv_high_risk_segments",
            s_as.get("high_risk_count"),
            "segments",
            "High-risk infrastructure segments in Central Valley (out of 645)",
            "data/central_valley/assets.json",
            "summary.high_risk_count",
            cv_assets.get("quality", "provisional"),
            "approved",
            [r"\b81\s*(?:/|of|out of)?\s*645\b", r"\b81\b[^\n]{0,30}high[- ]risk"],
            f"Evaluated segments: {s_as.get('evaluated_segments')}.",
        )

    cv_exp = _load_json("data/central_valley/exposure.json")
    if cv_exp:
        pop = cv_exp.get("population", {})
        lc = cv_exp.get("land_cover_and_crops", {})
        add(
            "cv_pop_gt2cm",
            pop.get("population_subsidence_gt_2cm_los_estimate"),
            "people",
            "Estimated population in Central Valley with >2 cm LOS subsidence (WorldPop 2020)",
            "data/central_valley/exposure.json",
            "population.population_subsidence_gt_2cm_los_estimate",
            cv_exp.get("quality", "provisional"),
            "approved",
            [r"71,?701"],
            "Combined with Karapinar (11,572) = 83,273.",
        )
        add(
            "cv_crop_share_gt2cm",
            lc.get("cultivated_cropland_gt_2cm_share_percent"),
            "%",
            "Share of >2 cm subsiding area in Central Valley that is cultivated cropland",
            "data/central_valley/exposure.json",
            "land_cover_and_crops.cultivated_cropland_gt_2cm_share_percent",
            cv_exp.get("quality", "provisional"),
            "approved",
            [r"79\.2\s*%"],
        )

    # 2. Central Valley Full-Year (mixed)
    fy_sum = _load_json("data/central_valley_fullyear/summary.json")
    if fy_sum:
        add(
            "cv_fy_max_los_cm",
            fy_sum["max_subsidence_cm"],
            "cm",
            "Central Valley 324-day cumulative LOS subsidence (2025-11-24 to 2026-10-14, mixed)",
            "data/central_valley_fullyear/summary.json",
            "max_subsidence_cm",
            fy_sum.get("quality", "mixed"),
            "approved",
            [r"[−\-]?20\.3\s*cm"],
            "Mixes beta-precal and provisional; label as mixed.",
        )

    fy_dec = _load_json("data/central_valley_fullyear/decomp.json")
    if fy_dec:
        pts = fy_dec.get("point_decompositions", [])
        p01 = next((p for p in pts if p.get("id") == "p01"), None)
        if p01:
            add(
                "cv_fy_perm_rate_p01",
                round(float(p01["permanent_cm_per_yr"]), 2),
                "cm/yr",
                "Permanent subsidence rate at peak station p01 (7 km W of Earlimart, 324 d)",
                "data/central_valley_fullyear/decomp.json",
                "point_decompositions[p01].permanent_cm_per_yr",
                fy_dec.get("quality", "mixed"),
                "approved",
                [r"[−\-]?16\.77\s*cm/yr", r"[−\-]?16\.8\s*cm/yr"],
            )
            add(
                "cv_fy_seasonal_p2p_p01",
                round(float(p01["seasonal_peak_to_peak_cm"]), 2),
                "cm",
                "Seasonal elastic peak-to-peak amplitude at p01 (324 d)",
                "data/central_valley_fullyear/decomp.json",
                "point_decompositions[p01].seasonal_peak_to_peak_cm",
                fy_dec.get("quality", "mixed"),
                "approved",
                [r"11\.67\s*cm", r"11\.7\s*cm"],
            )

    fy_vol = _load_json("data/central_valley_fullyear/storage_loss.json")
    if fy_vol:
        add(
            "cv_fy_storage_loss_km3",
            fy_vol["volume_km3_per_yr"],
            "km3/yr",
            "Central Valley permanent aquifer storage loss rate (>1 cm/yr mask, mixed)",
            "data/central_valley_fullyear/storage_loss.json",
            "volume_km3_per_yr",
            fy_vol.get("quality", "mixed"),
            "approved",
            [r"0\.3174?\s*km[³3]", r"0\.32\s*km[³3]"],
            f"Reference sensitivity range: {fy_vol.get('lower')} to {fy_vol.get('upper')} km3/yr.",
        )

    # 3. Karapinar & UK Clay
    kp_sum = _load_json("data/karapinar/summary.json")
    if kp_sum:
        add(
            "kp_max_los_cm",
            kp_sum["max_subsidence_cm"],
            "cm",
            "Karapinar peak 108-day LOS subsidence (2026-06-26 to 2026-10-12)",
            "data/karapinar/summary.json",
            "max_subsidence_cm",
            kp_sum.get("quality", "provisional"),
            "approved",
            [r"[−\-]?5\.9\s*cm", r"[−\-]?5\.93\s*cm"],
        )
        add(
            "kp_rate_yr_est",
            kp_sum["rate_cm_per_yr_estimate"],
            "cm/yr",
            "Karapinar summer-extrapolated LOS rate estimate (108 d -> 365.25 d)",
            "data/karapinar/summary.json",
            "rate_cm_per_yr_estimate",
            kp_sum.get("quality", "provisional"),
            "preliminary",
            [r"[−\-]?20\.0\s*cm/(?:yr|year)"],
            "Summer-only extrapolation; exclude from press headlines per atlas_validation.md.",
        )

    kp_unc = _load_json("data/karapinar/uncertainty/meta.json")
    if kp_unc:
        add(
            "kp_sigma_median_cm",
            kp_unc["median_sigma_cm"],
            "cm",
            "Karapinar median Cramér-Rao formal phase-noise uncertainty (L=208, 8 pairs)",
            "data/karapinar/uncertainty/meta.json",
            "median_sigma_cm",
            kp_unc.get("quality", "provisional"),
            "approved",
            [r"0\.326\s*cm", r"0\.33\s*cm"],
        )

    uk_det = _load_json("data/uk_clay/detection.json")
    if uk_det:
        add(
            "uk_clay_threshold_cm",
            uk_det["detection_threshold_cm"],
            "cm",
            "UK London Clay 3-sigma noise floor (below detection)",
            "data/uk_clay/detection.json",
            "detection_threshold_cm",
            uk_det.get("quality", "provisional"),
            "approved",
            [r"3\.62\s*cm", r"3\.6\s*cm"],
        )

    # 4. Global Atlas regions
    atlas = _load_json("data/global/atlas.json")
    if atlas:
        for r in atlas.get("regions", []):
            rid = r["id"]
            if rid in ("central_valley", "karapinar"):
                continue
            val = r.get("max_cm_los")
            rate100 = r.get("rate_cm_per_100d")
            conf = r.get("confidence", "low")
            verdict = "approved" if conf in ("high", "medium") else "preliminary"
            if val is not None:
                v_str = re.escape(f"{abs(float(val)):.1f}")
                add(
                    f"atlas_{rid}_los_cm",
                    val,
                    "cm",
                    f"{r['name']} peak LOS displacement ({r.get('days', '?')} d)",
                    f"data/global/atlas.json",
                    f"regions[{rid}].max_cm_los",
                    r.get("quality", "provisional"),
                    verdict,
                    [rf"[−\-]?{v_str}\s*cm"],
                    f"Confidence={conf}; rate_cm_per_100d={rate100}.",
                )

    return entries


def scan_documents(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Scan web and story files to populate used_in and detect discrepancies."""
    files: list[Path] = []
    for g in SCAN_GLOBS:
        files.extend(sorted(ROOT.glob(g)))
    seen: set[Path] = set()
    unique_files: list[Path] = []
    for f in files:
        if f not in seen and f.is_file():
            seen.add(f)
            unique_files.append(f)

    discrepancies: list[dict[str, str]] = []
    compiled = [
        (e, [re.compile(p, re.IGNORECASE) for p in e["_patterns"]])
        for e in entries
    ]

    for fpath in unique_files:
        rel = fpath.relative_to(ROOT).as_posix()
        if rel in ("docs/story/numbers_registry.md",):
            continue
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        owner = FILE_OWNERS.get(rel, "check docs/GOREV_DAGILIMI.md")
        for idx, line in enumerate(lines, start=1):
            loc = f"{rel}:{idx}"
            for e, pats in compiled:
                if any(p.search(line) for p in pats):
                    if loc not in e["used_in"]:
                        e["used_in"].append(loc)

            # Explicit discrepancy checks
            if re.search(r"−?6\.2\s*(?:and|to|–|-)\s*−?7\.8\s*cm", line, re.IGNORECASE):
                discrepancies.append(
                    {
                        "location": loc,
                        "written_value": "-6.2 to -7.8 cm (stale CV ref range)",
                        "data_value": "[-7.8, -4.7] cm (data/central_valley/summary.json:range_cm)",
                        "owner": owner,
                        "fix": "Update reference sensitivity range to -4.7 to -7.8 cm.",
                    }
                )
            if re.search(r"Consecutive\s+12[- ]day\s+pairs", line, re.IGNORECASE) and "central_valley" in rel + line.lower():
                discrepancies.append(
                    {
                        "location": loc,
                        "written_value": "Consecutive 12-day pairs",
                        "data_value": "12 to 24 day pairs (07-22->08-15 and 09-20->10-14 are 24 days)",
                        "owner": owner,
                        "fix": "Change to '12- to 24-day pairs'.",
                    }
                )
            if "mexico_city" in rel + line.lower() or "mexico city" in line.lower():
                if re.search(r"[−\-]4\.4\s*cm", line):
                    discrepancies.append(
                        {
                            "location": loc,
                            "written_value": "-4.4 cm (old Mexico City in-basin reference)",
                            "data_value": "-7.0 cm LOS (data/global/mexico_city/summary.json, SW volcanic ref)",
                            "owner": owner,
                            "fix": "Update Mexico City headline to -7.0 cm LOS (-5.8 cm/100 d).",
                        }
                    )

    for e in entries:
        e.pop("_patterns", None)
    return discrepancies


def write_registry_outputs(
    entries: list[dict[str, Any]],
    discrepancies: list[dict[str, str]],
    json_out: Path | None = None,
    md_out: Path | None = None,
) -> dict[str, Any]:
    """Write data/numbers_registry.json and docs/story/numbers_registry.md."""
    jp = json_out or (ROOT / "data" / "numbers_registry.json")
    mp = md_out or (ROOT / "docs" / "story" / "numbers_registry.md")
    jp.parent.mkdir(parents=True, exist_ok=True)
    mp.parent.mkdir(parents=True, exist_ok=True)

    counts = {
        "total": len(entries),
        "approved": sum(1 for e in entries if e["verdict"] == "approved"),
        "preliminary": sum(1 for e in entries if e["verdict"] == "preliminary"),
        "rejected": sum(1 for e in entries if e["verdict"] == "rejected"),
        "discrepancies": len(discrepancies),
    }
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "quality_notice": DISCLAIMER,
        "summary": counts,
        "entries": entries,
        "discrepancies": discrepancies,
    }
    jp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Numbers Registry — Authoritative Source Mapping",
        "",
        f"> **Calibration Notice:** {DISCLAIMER}",
        "",
        f"Every headline number in the web portal and story documents is traced to its authoritative JSON source (`{counts['total']}` metrics: `{counts['approved']}` approved, `{counts['preliminary']}` preliminary, `{counts['rejected']}` rejected; `{counts['discrepancies']}` open discrepancies).",
        "",
        "| ID | Value | Unit | Quality | Verdict | Source (`file:key`) | Used In (count) |",
        "|---|---:|---|---|---|---|---:|",
    ]
    for e in entries:
        lines.append(
            f"| `{e['id']}` | `{e['value']}` | {e['unit']} | `{e['quality']}` | **{e['verdict']}** | `{e['source_file']}` (`{e['source_key']}`) | {len(e['used_in'])} |"
        )
    if discrepancies:
        lines.extend(["", "## Open Discrepancies", "", "| Location | Written | Authoritative Data | Owner | Fix |", "|---|---|---|---|---|"])
        for d in discrepancies:
            lines.append(
                f"| `{d['location']}` | {d['written_value']} | {d['data_value']} | {d['owner']} | {d['fix']} |"
            )
    mp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    ap = argparse.ArgumentParser(description="Build canonical numbers registry and audit documents.")
    ap.add_argument("--json-out", type=Path, default=None)
    ap.add_argument("--md-out", type=Path, default=None)
    args = ap.parse_args()

    entries = build_canonical_entries()
    discrepancies = scan_documents(entries)
    payload = write_registry_outputs(entries, discrepancies, json_out=args.json_out, md_out=args.md_out)
    s = payload["summary"]
    print(
        f"[numbers_registry] total={s['total']} approved={s['approved']} "
        f"preliminary={s['preliminary']} rejected={s['rejected']} discrepancies={s['discrepancies']}"
    )


if __name__ == "__main__":
    main()
