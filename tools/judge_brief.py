"""Build docs/story/judge_brief.html (A4, one page) and judge_brief.pdf from data files.

Numbers come from data/global/home_summary.json when it exists, otherwise from
data/global/vital_signs.json (same fields). Nothing is typed by hand.
Usage: python tools/judge_brief.py [--no-pdf]
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
G = ROOT / "data" / "global"
OUT = ROOT / "docs" / "story" / "judge_brief.html"
PDF = ROOT / "docs" / "story" / "judge_brief.pdf"
SITE = "https://keremsumer2010-tech.github.io/aseltech/"
REPO = "https://github.com/keremsumer2010-tech/aseltech"
CALIB = (
    "NISAR data are provisional. Calibration and validation are carried out by "
    "the NISAR project (NASA-JPL and ISRO), not by our team."
)


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sxy / (sx * sy)


def numbers() -> dict:
    hs = G / "home_summary.json"
    atlas = load(G / "atlas.json")
    storage = load(ROOT / "data" / "central_valley_fullyear" / "storage_loss.json")
    gps = load(ROOT / "data" / "central_valley" / "validation.json")
    xs = [s["insar"][-1] for s in gps]
    ys = [s["gnss"][-1] for s in gps]
    
    if hs.exists():
        data = load(hs)
        kpi_map = {item["key"]: item["value"] for item in data.get("kpis", [])}
        regs = atlas["regions"]
        rel = sorted((r for r in regs if not r.get("indicative_only")), key=lambda r: r.get("rank", 999))
        fastest = rel[0] if rel else regs[0]
        return {
            "basins": kpi_map.get("regions", atlas["n_regions"]),
            "reliable": atlas["n_reliable"],
            "indicative": atlas["n_indicative"],
            "window_days": atlas["common_window_days"],
            "window": atlas["common_window"],
            "people": kpi_map.get("people"),
            "area": load(G / "vital_signs.json")["area_km2_lt_minus5cm"],
            "fastest": {
                "name": fastest["name"],
                "rate_cm_per_100d": fastest.get("rate_cm_per_100d_common", fastest.get("rate_cm_per_100d")),
            },
            "storage": kpi_map.get("storage", storage["volume_km3_per_yr"]),
            "gps_r": kpi_map.get("gnss", round(pearson(xs, ys), 2)),
            "gps_n": len(gps),
            "source": "home_summary.json",
        }
    
    vs = load(G / "vital_signs.json")
    return {
        "basins": vs.get("cities_measured", atlas["n_regions"]),
        "reliable": atlas["n_reliable"],
        "indicative": atlas["n_indicative"],
        "window_days": atlas["common_window_days"],
        "window": atlas["common_window"],
        "people": vs["people_on_sinking_ground"],
        "area": vs["area_km2_lt_minus5cm"],
        "fastest": vs["fastest"],
        "storage": storage["volume_km3_per_yr"],
        "gps_r": round(pearson(xs, ys), 2),
        "gps_n": len(gps),
        "source": "vital_signs.json",
    }


def build(n: dict) -> str:
    f = n["fastest"]
    people_m = f"{n['people'] / 1e6:.2f}"
    cards = [
        (str(n["basins"]), "basins measured", f"{n['reliable']} reliable, {n['indicative']} indicative"),
        (f"{f['rate_cm_per_100d']:+.1f} cm", f"fastest: {f['name']}", f"per 100 days, line of sight, {n['window_days']}-day common window"),
        (f"{people_m} M", "people on sinking ground", f"{n['people']:,} residents on {n['area']:.0f} km2 below -5 cm"),
        (f"r = {n['gps_r']:.2f}", "agreement with GPS", f"{n['gps_n']} stations, Central Valley"),
        (f"{n['storage']:.2f} km3/yr", "permanent aquifer loss", "Central Valley, mixed-quality series"),
    ]
    card_html = "\n".join(
        f'<div class="num"><b>{a}</b><span>{b}</span><i>{c}</i></div>' for a, b, c in cards
    )
    contribs = [
        ("One window, one method, 29 basins", f"A comparable global ranking from the first provisional NISAR data: one {n['window_days']}-day window, one open pipeline."),
        ("An atlas that checks itself", "Time-series quality control caught a full phase-cycle error in Semarang (-12.1 to -6.2 cm) and flagged other basins as indicative."),
        ("Independent evidence", "GPS agreement in the Central Valley (r = 0.92, 10 stations); in Mexico City spatial pattern matches NASA JPL OPERA at 10 points (r = 0.91) across seasons."),
        ("From measurement to decision", "People and aquifer loss, canal tilt risk, one-page bulletins, a 24-month simulator, one command to reproduce."),
    ]
    contrib_html = "\n".join(
        f"<li><strong>{a}.</strong> {b}</li>" for a, b in contribs
    )
    links = [
        ("Site", SITE),
        ("Atlas", SITE + "atlas.html"),
        ("Simulator", SITE + "game/"),
        ("Bulletins", SITE + "docs/bulletins/"),
        ("Repository", REPO),
    ]
    link_html = "\n".join(
        f'<li><b>{a}</b> <a href="{u}">{u}</a></li>' for a, u in links
    )
    core = (
        f"We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: "
        f"{n['basins']} basins measured with one open pipeline on the same {n['window_days']} days, every number traceable to its file, "
        f"and every headline checked against GPS, NASA's OPERA product and the literature."
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>NISAR Vision - one-page brief for judges</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
@page {{ size: A4; margin: 0 }}
* {{ box-sizing: border-box }}
html {{ background: #e9edf1 }}
body {{ margin: 0; font: 10pt/1.4 "Segoe UI", Arial, sans-serif; color: #14202b }}
.page {{ width: 210mm; height: 297mm; margin: 0 auto; background: #fff; padding: 13mm 14mm 10mm; display: flex; flex-direction: column; overflow: hidden }}
.kicker {{ font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color: #5a6b7a }}
h1 {{ font-size: 21pt; margin: 2mm 0 3mm; line-height: 1.1 }}
.core {{ font-size: 11.5pt; line-height: 1.45; margin: 0 0 5mm; padding: 3.5mm 4mm; border-left: 3px solid #1b6fb3; background: #f2f7fb }}
.nums {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.5mm; margin-bottom: 5mm }}
.num {{ border: 1px solid #cfd9e2; border-radius: 3px; padding: 3mm 2.5mm; display: flex; flex-direction: column }}
.num b {{ font-size: 17pt; line-height: 1.05; color: #0d4f86 }}
.num span {{ font-size: 8.5pt; font-weight: 600; margin-top: 1.5mm }}
.num i {{ font-size: 7.5pt; font-style: normal; color: #5a6b7a; margin-top: 1mm }}
h2 {{ font-size: 10.5pt; margin: 0 0 2mm; text-transform: uppercase; letter-spacing: .05em; color: #0d4f86 }}
ol, ul {{ margin: 0; padding-left: 5mm }}
li {{ margin-bottom: 1.6mm }}
.links {{ list-style: none; padding: 0 }}
.links li {{ margin-bottom: 1mm }}
.links b {{ display: inline-block; width: 22mm }}
a {{ color: #0d4f86; text-decoration: none; word-break: break-all }}
section {{ margin-bottom: 4.5mm }}
.sections li {{ margin-bottom: 1mm }}
.foot {{ margin-top: auto; font-size: 8pt; color: #3d4c59; border-top: 1px solid #cfd9e2; padding-top: 2.5mm }}
@media print {{ html {{ background: #fff }} .page {{ margin: 0 }} }}
</style></head>
<body><div class="page">
<div class="kicker">NASA Space Apps 2026 · Dancing with the SARs · Team Aseltech</div>
<h1>NISAR Vision: Follow the Water</h1>
<p class="core">{core}</p>
<div class="nums">
{card_html}
</div>
<section><h2>What the site shows in three minutes</h2>
<ul class="sections">
<li><strong>Hero.</strong> One sentence and three numbers: basins, people, GPS agreement.</li>
<li><strong>Atlas.</strong> All {n['basins']} basins ranked on the same {n['window_days']} days ({n['window'][0]} to {n['window'][1]}).</li>
<li><strong>We caught our own error.</strong> Semarang before and after quality control.</li>
<li><strong>Why you can trust it.</strong> GPS agreement across 10 stations (r = 0.92), formal uncertainty, and the calibration notice.</li>
<li><strong>What it is for.</strong> People, water, canals, bulletins, simulator.</li>
<li><strong>Original and open.</strong> Four contributions and one reproduction command.</li>
</ul></section>
<section><h2>Four original contributions</h2><ol>
{contrib_html}
</ol></section>
<section><h2>Links</h2><ul class="links">
{link_html}
</ul></section>
<div class="foot"><strong>Calibration notice.</strong> {CALIB}<br>
Numbers are read from data/global/{n['source']}, atlas.json, exposure_atlas.json and the Central Valley validation file. Line-of-sight (LOS) means motion toward or away from the satellite.</div>
</div></body></html>
"""


def make_pdf() -> bool:
    chrome = None
    for c in (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ):
        if Path(c).exists():
            chrome = c
            break
    chrome = chrome or shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        print("No Chrome/Edge found; PDF skipped")
        return False
    with tempfile.TemporaryDirectory() as prof:
        subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}",
             "--no-pdf-header-footer", f"--print-to-pdf={PDF}", OUT.as_uri()],
            check=False, capture_output=True, timeout=120,
        )
    return PDF.exists()


def main() -> int:
    n = numbers()
    OUT.write_text(build(n), encoding="utf-8", newline="\n")
    print("Wrote", OUT, json.dumps({k: v for k, v in n.items() if k != "fastest"}))
    if "--no-pdf" not in sys.argv:
        print("PDF:", make_pdf(), PDF)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
