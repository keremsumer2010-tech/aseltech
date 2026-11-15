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

# Fixed release values (PC1). People = reliable basins only, from data/global/vital_signs.json.
EXPECTED = {
    "regions": 29,
    "reliable": 15,
    "gnss_r": "0.924",
    "opera_r": "0.912",
    "storage_km3_yr": "0.3174",
    "people": 1_167_429,
    "konya_cm_per_100d": "-11.0",
}


def _same(actual: str, wanted: str) -> bool:
    """Equal, or equal after rounding the canonical value to the decimals shown in the document."""
    if actual == wanted:
        return True
    try:
        a, w = float(actual), float(wanted)
    except ValueError:
        return False
    dec = len(actual.split(".")[1]) if "." in actual else 0
    return round(w, dec) == a


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
        "konya_cm_per_100d": "-11.0",  # Konya keeps its rate but is indicative since the review (PC1)
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
        "gnss_r": [re.compile(r"cross.station[^=]{0,40}?\br\s*=\s*(0\.\d+)", re.I),
                   re.compile(r"(?:GPS|stations)[^=]{0,80}?\br\s*=\s*(0\.\d+)", re.I)],
        "opera_r": [re.compile(r"OPERA[^=]{0,90}?\br\s*=\s*(0\.\d+)", re.I)],
        "storage_km3_yr": [re.compile(r"([\d.]+)\s*km[³3]/yr", re.I)],
        "people": [re.compile(r"(\d{1,3}(?:,\d{3}){2,})\s+(?:estimated\s+)?residents?", re.I)],
        "konya_cm_per_100d": [re.compile(r"Konya[^()\n]{0,40}\(([−-][\d.]+)\s*cm/100d", re.I)],
    }
    for path in DOCS:
        content = path.read_text(encoding="utf-8")
        for key, patterns in checks.items():
            for line, raw in _line_numbers(content, patterns):
                # Restrict correlation checks to the named sensor and population/rate checks to context.
                original_line = content.splitlines()[line - 1]
                if "→" in original_line:  # revision history rows list superseded values on purpose
                    continue
                if key == "regions" and re.search(r"draft|was\s+\d+|flagged|indicative", original_line, re.I):
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
                if not _same(actual, wanted):
                    errors.append(f"{path.relative_to(ROOT).as_posix()}:{line}: {key} is {raw!r}, expected {wanted!r}")

    assert not errors, "Headline number mismatches (file:line):\n" + "\n".join(errors)
