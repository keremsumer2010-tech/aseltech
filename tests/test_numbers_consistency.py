"""Guard the final package's repeated atlas headline figures against drift."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "data/global/home_summary.json"
DOCS = [
    ROOT / "docs/qa/SCIENCE_SIGNOFF.md",
    ROOT / "docs/story/slides.html",
    ROOT / "docs/story/technical_note.md",
    ROOT / "docs/story/press_summary.md",
    ROOT / "docs/story/submission_form.md",
]

EXPECTED = {
    "regions": 29,
    "reliable": 16,
    "gnss_r": "0.924",
    "opera_r": "0.912",
    "storage_km3_yr": "0.3174",
    "people": 1_479_844,
    "konya_cm_per_100d": "-11.0",
}


def _line_numbers(text: str, patterns: list[re.Pattern[str]]) -> list[tuple[int, str]]:
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        for pattern in patterns:
            match = pattern.search(line)
            if match:
                found.append((number, match.group(1).replace(",", "")))
                break
    return found


def test_headline_numbers_match_home_summary() -> None:
    home_text = HOME.read_text(encoding="utf-8")
    home = json.loads(home_text)
    kpis = {item["key"]: item for item in home["kpis"]}
    expected_home = {
        "regions": kpis["regions"]["value"],
        "reliable": int(re.search(r"(\d+) reliable", kpis["regions"]["detail"]).group(1)),
        "gnss_r": f"{kpis['gnss']['value']:.3f}",
        "opera_r": f"{kpis['opera']['value']:.3f}",
        "storage_km3_yr": f"{kpis['storage']['value']:.4f}",
        "people": kpis["people"]["value"],
        "konya_cm_per_100d": f"{home['top5'][0]['rate_cm_per_100d_common']:.1f}",
    }
    errors: list[str] = []
    for key, expected in EXPECTED.items():
        if expected_home[key] != expected:
            line = next((i for i, value in enumerate(home_text.splitlines(), 1)
                         if f'"{key}"' in value), 1)
            errors.append(f"{HOME.relative_to(ROOT).as_posix()}:{line}: canonical {key} is {expected_home[key]!r}, expected {expected!r}")

    checks: dict[str, list[re.Pattern[str]]] = {
        "regions": [re.compile(r"(\d+)\s+(?:basins|regions)\b", re.I),
                    re.compile(r"(\d+)\s+standardized\b[^\n]{0,100}\bregions\b", re.I)],
        "reliable": [re.compile(r"(\d+)\s+reliable\s*(?:/|[,;])", re.I),
                     re.compile(r"(\d+)\s+pass quality control", re.I)],
        "gnss_r": [re.compile(r"r\s*=\s*(0\.\d+)", re.I)],
        "opera_r": [re.compile(r"r\s*=\s*(0\.\d+)", re.I)],
        "storage_km3_yr": [re.compile(r"([\d.]+)\s*km[³3]/yr", re.I)],
        "people": [re.compile(r"(\d{1,3}(?:,\d{3}){2,})\s+(?:estimated\s+)?residents?", re.I)],
        "konya_cm_per_100d": [re.compile(r"([−-][\d.]+)\s*cm/100d", re.I)],
    }
    for path in DOCS:
        content = path.read_text(encoding="utf-8")
        for key, patterns in checks.items():
            for line, raw in _line_numbers(content, patterns):
                # Restrict correlation checks to the named sensor and population/rate checks to context.
                original_line = content.splitlines()[line - 1]
                if key == "regions" and re.search(r"draft|was\s+\d+", original_line, re.I):
                    continue
                if key == "reliable" and re.search(r"top[- ]?5|#\d+\s+reliable", original_line, re.I):
                    continue
                if key == "gnss_r" and not re.search(r"cross.station|10.{0,12}stations|GPS\s+r\s*=", original_line, re.I):
                    continue
                if key == "opera_r" and not re.search(r"OPERA.{0,60}Mexico City|Mexico City.{0,60}OPERA", original_line, re.I):
                    continue
                if key == "storage_km3_yr" and not re.search(r"storage|aquifer|compaction", original_line, re.I):
                    continue
                if key == "konya_cm_per_100d" and not re.search(r"Konya", original_line, re.I):
                    continue
                if key == "people" and not re.search(r"GHSL|global|sinking ground", original_line, re.I):
                    continue
                actual = raw.replace("−", "-")
                wanted = str(EXPECTED[key])
                if actual != wanted:
                    errors.append(f"{path.relative_to(ROOT).as_posix()}:{line}: {key} is {raw!r}, expected {wanted!r}")

    assert not errors, "Headline number mismatches (file:line):\n" + "\n".join(errors)
