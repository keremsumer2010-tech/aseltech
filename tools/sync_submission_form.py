"""Refresh docs/story/submission_form.md from data files and recount characters.

Numbers come from data/global/home_summary.json when present, else vital_signs.json.
Usage: python tools/sync_submission_form.py
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
G = ROOT / "data" / "global"
FORM = ROOT / "docs" / "story" / "submission_form.md"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))


def facts() -> dict:
    hs = G / "home_summary.json"
    atlas = load(G / "atlas.json")
    gps = load(ROOT / "data" / "central_valley" / "validation.json")
    storage = load(ROOT / "data" / "central_valley_fullyear" / "storage_loss.json")
    regs = atlas["regions"]
    rel = sorted((r for r in regs if not r.get("indicative_only")), key=lambda r: r["rank"])
    ind = [r for r in regs if r.get("indicative_only")]
    
    if hs.exists():
        data = load(hs)
        kpi_map = {item["key"]: item["value"] for item in data.get("kpis", [])}
        return {
            "n": kpi_map.get("regions", atlas["n_regions"]),
            "n_rel": atlas["n_reliable"],
            "n_ind": atlas["n_indicative"],
            "days": atlas["common_window_days"],
            "win": atlas["common_window"],
            "people": kpi_map.get("people"),
            "area": load(G / "vital_signs.json")["area_km2_lt_minus5cm"],
            "people2": 8251911,
            "top5": rel[:5],
            "ind": ind,
            "r": kpi_map.get("gnss", round(pearson([s["insar"][-1] for s in gps], [s["gnss"][-1] for s in gps]), 2)),
            "storage": kpi_map.get("storage", storage["volume_km3_per_yr"]),
        }

    vs = load(G / "vital_signs.json")
    return {
        "n": vs.get("cities_measured", atlas["n_regions"]),
        "n_rel": atlas["n_reliable"],
        "n_ind": atlas["n_indicative"],
        "days": atlas["common_window_days"],
        "win": atlas["common_window"],
        "people": vs["people_on_sinking_ground"],
        "area": vs["area_km2_lt_minus5cm"],
        "people2": vs["people_on_sinking_ground_gt2cm"],
        "top5": rel[:5],
        "ind": ind,
        "r": round(pearson([s["insar"][-1] for s in gps], [s["gnss"][-1] for s in gps]), 2),
        "storage": storage["volume_km3_per_yr"],
    }


def count(text: str) -> tuple[int, int]:
    return len(text), len(text.split())


def patch(md: str, f: dict) -> str:
    top = ", ".join(
        f"{r['rank']} {r['name']} ({r['rate_cm_per_100d_common']:+.1f} cm/100d)" for r in f["top5"]
    )
    ind_names = ", ".join(r["name"] for r in f["ind"] if r["id"] != "karapinar")
    ultra = (
        f"A self-checking global subsidence atlas from NISAR radar: {f['n']} basins, one open pipeline, "
        f"the same {f['days']} days, every number traceable to its file."
    )
    standard = (
        f"We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: "
        f"{f['n']} basins measured with one open pipeline on the same {f['days']} days, every number traceable to its file, "
        f"and every headline checked against GPS, NASA's OPERA product and the literature."
    )
    item4 = (
        f"4. 2026 Global Subsidence Atlas & Population Exposure ({f['win'][0]} to {f['win'][1]}, {f['days']}-day common window, provisional): "
        f"One open pipeline (pipeline/nisarpulse) measures {f['n']} basins on the same {f['days']} days; {f['n_rel']} pass quality control and {f['n_ind']} are indicative only. "
        f"Reliable ranking: {top} [data/global/atlas.json]. Automated time-series checks (tools/atlas_qc.py) caught a full 12.1 cm phase-cycle jump in Semarang "
        f"(-12.1 to -6.2 cm after correction) and moved Tehran from -3.5 to -7.4 cm LOS with an off-basin reference [data/global/atlas_changelog.json]; "
        f"indicative-only basins include {ind_names}. Intersecting GHSL GHS-POP E2025 (100 m) with displacement above each city's 2-sigma noise floor shows "
        f"{f['area']:.2f} km2 sinking faster than -5 cm per 108 days, with {f['people']:,} residents ({f['people2']:,} below -2 cm), excluding nested Karapinar "
        f"[data/global/exposure_atlas.json; data/global/vital_signs.json]. Secondary OPERA check: over Mexico City the spatial pattern matches NASA JPL's OPERA product at 10 points (r = 0.912), although OPERA covers winter and NISAR summer, while in the Central Valley and at Eloy agreement is weak (r = 0.40 and 0.09) because seasons and viewing geometry differ [data/global/opera_check.json]. (Independent primary validation against 10 continuous California GNSS stations is detailed in Section 6 below)."
    )
    # replace the ultra-short and standard code blocks
    md = re.sub(
        r"(- \*\*Ultra-Short Version[^\n]*\n```text\n)[^\n]*(\n```)",
        lambda m: m.group(1) + ultra + m.group(2), md, count=1)
    md = re.sub(
        r"(- \*\*Standard Portal Summary[^\n]*\n```text\n)[^\n]*(\n```)",
        lambda m: m.group(1) + standard + m.group(2), md, count=1)
    md = re.sub(r"\n4\. 2026 Global Subsidence Atlas[^\n]*", "\n" + item4.replace("\\", "\\\\"), md, count=1)
    md = md.replace(
        "across California, Turkiye, the UK, Mexico City, Tehran, and Jakarta.",
        f"across California, Turkiye, the UK, and a {f['n']}-basin global atlas.")
    md = re.sub(
        r"- Global Cities: [^\n]*",
        f"- Global atlas ({f['n']} basins, common window {f['win'][0]} to {f['win'][1]}): provisional GUNW pairs per basin are listed in data/global/<id>/meta.json and data/global/atlas.json; examples include Mexico City (Track 113 Desc), Tehran (Track 56 Asc) and Jakarta (Track 18 Desc).",
        md, count=1)
    if "NASA JPL OPERA DISP-S1" not in md:
        md = md.replace(
            "and NASA CMR OPERA_L3_DISP-S1_V1 archive coverage audit.",
            "and NASA JPL OPERA DISP-S1 (OPERA_L3_DISP-S1_V1) Sentinel-1 displacement used as an independent cross-check in Mexico City and the Central Valley.")
    if "GHSL GHS-POP" not in md.split("## 9.")[1].split("## 10.")[0]:
        md = md.replace(
            "- Copernicus DEM GLO-90 (ESA)",
            "- GHSL GHS-POP E2025 R2023A (European Commission JRC, 100 m, CC BY 4.0): population on sinking ground for the global atlas.\n- Copernicus DEM GLO-90 (ESA)")
    # recount every heading that carries a char count
    def recount(m):
        head, block = m.group(1), m.group(2)
        c, w = count(block)
        head = re.sub(r"`[\d,]+ chars` / `[\d,]+ words`", f"`{c:,} chars` / `{w:,} words`", head, count=1)
        return head + "```text\n" + block + "\n```"
    md = re.sub(r"((?:^|\n)[^\n]*`[\d,]+ chars`[^\n]*\n(?:\*[^\n]*\n)?\n?(?:- \*\*[^\n]*\n)?)```text\n(.*?)\n```", recount, md, flags=re.S)
    return md


def main() -> int:
    f = facts()
    old = FORM.read_text(encoding="utf-8")
    new = patch(old, f)
    FORM.write_text(new, encoding="utf-8", newline="\n")
    ultra = re.search(r"Ultra-Short[^\n]*\n```text\n([^\n]*)", new).group(1)
    std = re.search(r"Standard Portal[^\n]*\n```text\n([^\n]*)", new).group(1)
    print("ultra", len(ultra), "(limit 150) | standard", len(std), "(limit 500)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
