#!/usr/bin/env python3
"""Sync data/global/literature_rates.json and docs/story/literature_atlas.md
with the official data/global/atlas.json ordering and tiers (#1 Eloy, 15 reliable, 14 indicative).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def main():
    atlas_path = ROOT / "data/global/atlas.json"
    lit_path = ROOT / "data/global/literature_rates.json"
    doc_path = ROOT / "docs/story/literature_atlas.md"

    with open(atlas_path, "r", encoding="utf-8") as f:
        atlas = json.load(f)

    with open(lit_path, "r", encoding="utf-8") as f:
        lit = json.load(f)

    lit_map = {r["id"]: r for r in lit["regions"]}

    # Read existing literature_atlas.md to preserve existing source/DOI links and formatted notes
    rows_by_id = {}
    if doc_path.exists():
        with open(doc_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("| ") and line[2].isdigit():
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 9:
                        m = re.search(r"\(`([a-z0-9_]+)`\)", parts[2])
                        if m:
                            rid = m.group(1)
                            rows_by_id[rid] = {
                                "region_cell": parts[2],
                                "pub_rate": parts[6],
                                "source": parts[7],
                                "note": parts[8],
                            }

    new_lit_regions = []
    table_lines = []

    for ar in atlas["regions"]:
        rid = ar["id"]
        lr = dict(lit_map[rid])
        
        lr["rank"] = ar["rank"]
        lr["confidence"] = ar["confidence"]
        lr["indicative_only"] = ar["indicative_only"]
        lr["rate_cm_per_100d_common"] = ar["rate_cm_per_100d_common"]
        lr["rate_cm_per_100d"] = ar["rate_cm_per_100d"]
        lr["max_cm_los"] = ar["max_cm_los"]
        lr["period"] = ar["period"]
        new_lit_regions.append(lr)

        old_row = rows_by_id.get(rid, {})
        region_cell = old_row.get("region_cell", f"**{ar.get('name', rid)}** (`{rid}`)")
        pub_rate = old_row.get("pub_rate", lr.get("published_rate", "—"))
        source = old_row.get("source", lr.get("published_source", "—"))
        note = old_row.get("note", lr.get("agreement_note", "—"))

        tier = "indicative" if ar["indicative_only"] else "reliable"
        tier_conf = f"`{tier}` ({ar['confidence']})"
        rate_common = f"`{ar['rate_cm_per_100d_common']:.1f}`"
        peak_los = f"`{ar['max_cm_los']:.1f}`"

        row_line = f"| {ar['rank']} | {region_cell} | {rate_common} | {peak_los} | {tier_conf} | {pub_rate} | {source} | {note} |"
        table_lines.append(row_line)

    lit["regions"] = new_lit_regions

    with open(lit_path, "w", encoding="utf-8") as f:
        json.dump(lit, f, indent=2, ensure_ascii=False)
        f.write("\n")

    header = """# 2026 Global Subsidence Atlas — Literature & DOI Comparison (`docs/story/literature_atlas.md`)

> **Calibration Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

Standardized comparison of all **29** regions in `data/global/atlas.json` (v2, 93-day common window `2026-06-28` to `2026-09-29`) against peer-reviewed InSAR/GNSS literature (`data/global/*/validation_note.json`, `data/global/literature_rates.json`).

| Rank | Region | Common Rate (`cm/100d`) | Peak LOS (`cm`) | Tier / Conf. | Published Rate | Source / DOI | Agreement Note |
|---:|---|---:|---|---|---|---|---|
"""
    content = header + "\n".join(table_lines) + "\n"

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Synced {len(new_lit_regions)} regions in literature_rates.json and literature_atlas.md")

if __name__ == "__main__":
    main()
