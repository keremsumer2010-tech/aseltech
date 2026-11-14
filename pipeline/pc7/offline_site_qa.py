"""Offline source/data/text QA for the NISAR Pulse site."""
from __future__ import annotations

import argparse
import html.parser
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"
QA = ROOT / "docs" / "qa" / "PC7.md"
SITE_ROOT_DIRS = {"data", "game", "web3d", "docs"}
PATH_LITERAL = re.compile(r"[\"'`]((?:\./|\.\./)?(?:data|game|web3d|docs/story)/[^\"'`]+)[\"'`]")


class LocalAttributeParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[int, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line = self.getpos()[0]
        for key, value in attrs:
            if key.lower() in {"src", "href"} and value:
                self.refs.append((line, key.lower(), value.strip()))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def is_external(value: str) -> bool:
    value = value.strip()
    low = value.lower()
    return (
        not value
        or low.startswith(("http:", "https:", "//", "mailto:", "tel:", "data:", "blob:", "javascript:"))
        or value.startswith("#")
    )


def repo_target(value: str) -> tuple[Path, str, bool]:
    path = unquote(urlsplit(value).path).replace("\\", "/")
    dynamic = bool(re.search(r"\$\{[^}]*\}", path))
    path = re.sub(r"\$\{[^}]*\}", "*", path)
    while path.startswith("./"):
        path = path[2:]
    while path.startswith("../"):
        path = path[3:]
    parts = Path(path).parts
    if parts and parts[0] in SITE_ROOT_DIRS:
        target = ROOT.joinpath(*parts)
    else:
        target = WEB.joinpath(*parts)
    return target, target.relative_to(ROOT).as_posix(), dynamic


def target_exists(target: Path, dynamic: bool) -> bool:
    if dynamic:
        return any(target.parent.glob(target.name))
    return target.exists()


def path_report() -> str:
    sources = [WEB / name for name in ("index.html", "science.html", "data.html", "faq.html", "app.js", "docs.js")]
    records: set[tuple[str, int, str, str]] = set()
    for source in sources:
        text = source.read_text(encoding="utf-8")
        if source.suffix == ".html":
            parser = LocalAttributeParser()
            parser.feed(text)
            for line, attr, value in parser.refs:
                if not is_external(value):
                    records.add((source.relative_to(ROOT).as_posix(), line, f"{attr}={value}", value))
        for line, raw_line in enumerate(text.splitlines(), start=1):
            for match in PATH_LITERAL.finditer(raw_line):
                value = match.group(1)
                if not is_external(value):
                    records.add((source.relative_to(ROOT).as_posix(), line, "path literal", value))

    rows: list[tuple[str, int, str, str, str]] = []
    for source, line, kind, value in sorted(records):
        target, rel, dynamic = repo_target(value)
        exists = target_exists(target, dynamic)
        marker = "OK" if exists else "MISSING"
        if dynamic and exists:
            marker = "OK (dynamic pattern has matches)"
        rows.append((source, line, value, rel, marker))

    lines = [
        "## 1. Link ve dosya yolları (offline)",
        "",
        "Yayımlama eşlemesi: `web/` site kökü; `data/`, `game/`, `web3d/` ve `docs/story/` depo kökünden kopyalanıyor.",
        "",
        "| Kaynak | Satır | Göreli yol | Repo karşılığı | Kontrol |",
        "|---|---:|---|---|---|",
    ]
    lines.extend(f"| `{s}` | {n} | `{v}` | `{r}` | {ok} |" for s, n, v, r, ok in rows)
    missing = [(s, n, v, r) for s, n, v, r, ok in rows if ok == "MISSING"]
    lines.extend(["", f"Kontrol edilen yerel yol: {len(rows)}. Eksik: {len(missing)}."])
    if missing:
        lines.extend(["", "Eksik yollar:"])
        lines.extend(f"- `{s}:{n}` → `{v}` → `{r}`" for s, n, v, r in missing)
    else:
        lines.append("Eksik yerel yol bulunmadı.")
    return "\n".join(lines)


def walk_dates(value, prefix="$"):
    if isinstance(value, dict):
        for key, child in value.items():
            current = f"{prefix}.{key}"
            if key == "dates" and isinstance(child, list):
                yield current, child
            else:
                yield from walk_dates(child, current)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_dates(child, f"{prefix}[{index}]")


def quality_scope(value, key):
    if isinstance(value, dict) and key in value:
        return "root"
    if isinstance(value, list) and value and all(isinstance(item, dict) and key in item for item in value):
        return "records"
    if isinstance(value, dict) and isinstance(value.get("features"), list) and value["features"]:
        if all(isinstance(item, dict) and key in item.get("properties", {}) for item in value["features"]):
            return "feature properties"
    return "missing"


def required_fields(relpath, value):
    name = Path(relpath).name
    missing = []
    if relpath == "data/catalog.json":
        if not isinstance(value, list):
            missing.append("top-level array")
        else:
            for index, item in enumerate(value):
                if not isinstance(item, dict):
                    missing.append(f"[{index}] object")
                    continue
                for key in ("site", "title", "quality", "layers"):
                    if key not in item:
                        missing.append(f"[{index}].{key}")
    elif name == "meta.json" and relpath == "data/uk/meta.json":
        for key in ("date", "bbox", "optical_source_url", "optical_product", "radar_granule", "radar_browse_url", "quality", "note"):
            if not isinstance(value, dict) or key not in value:
                missing.append(key)
    elif name == "meta.json" and "/uncertainty/" not in relpath:
        for key in ("site", "bbox", "dates", "units", "vmin", "vmax", "source", "notes", "quality", "quality_note"):
            if not isinstance(value, dict) or key not in value:
                missing.append(key)
    elif name == "summary.json":
        for key in ("max_subsidence_cm", "period", "rate_cm_per_yr_estimate", "reference_point", "quality"):
            if not isinstance(value, dict) or key not in value:
                missing.append(key)
    elif name == "points.json":
        required = ("id", "name", "lon", "lat", "dates", "disp_cm")
        if not isinstance(value, list):
            missing.append("top-level array")
        else:
            for index, item in enumerate(value):
                if not isinstance(item, dict):
                    missing.append(f"[{index}] object")
                    continue
                for key in required:
                    if key not in item:
                        missing.append(f"[{index}].{key}")
    elif name == "drivers.json":
        for key in ("dates", "subsidence_cm", "soil_moisture", "irrigation_index", "lag_corr"):
            if not isinstance(value, dict) or key not in value:
                missing.append(key)
    elif name == "validation.json":
        required = ("station", "lon", "lat", "rmse_cm", "corr", "dates", "insar", "gnss")
        if not isinstance(value, list):
            missing.append("top-level array")
        else:
            for index, item in enumerate(value):
                if not isinstance(item, dict):
                    missing.append(f"[{index}] object")
                    continue
                for key in required:
                    if key not in item:
                        missing.append(f"[{index}].{key}")
    elif relpath.endswith(".geojson") or name == "assets.json":
        if not isinstance(value, dict) or value.get("type") != "FeatureCollection" or not isinstance(value.get("features"), list):
            missing.append("GeoJSON FeatureCollection")
        else:
            properties = ("name", "type", "risk", "gradient_mm_per_km", "max_cm") if name == "assets.json" else (("name", "year_formed", "source_title", "source_url", "coord_source") if name == "sinkholes.geojson" else ())
            for index, feature in enumerate(value["features"]):
                if not isinstance(feature, dict) or feature.get("type") != "Feature":
                    missing.append(f"features[{index}].type=Feature")
                    continue
                if not isinstance(feature.get("geometry"), dict):
                    missing.append(f"features[{index}].geometry")
                props = feature.get("properties") or {}
                for key in properties:
                    if key not in props:
                        missing.append(f"features[{index}].properties.{key}")
    return missing


def schema_label(relpath):
    name = Path(relpath).name
    if relpath == "data/catalog.json": return "catalog"
    if name == "meta.json" and relpath == "data/uk/meta.json": return "UK metadata"
    if name == "meta.json" and "/uncertainty/" not in relpath: return "site metadata"
    if name in {"summary.json", "points.json", "drivers.json", "validation.json"}: return name.removesuffix(".json")
    if name == "assets.json": return "assets GeoJSON features"
    if name == "sinkholes.geojson": return "sinkhole GeoJSON features"
    return "not specified in VERI_SOZLESMESI.md"


def data_report() -> str:
    files = sorted([* (ROOT / "data").rglob("*.json"), * (ROOT / "data").rglob("*.geojson")])
    results = []
    details = []
    parsed = {}
    date_sequence_count = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        try:
            value = json.loads(path.read_text(encoding="utf-8"), parse_constant=lambda token: (_ for _ in ()).throw(ValueError(f"non-finite {token}")))
            parsed[rel] = value
        except Exception as exc:
            results.append((rel, "PARSE ERROR", "—", "—", "—"))
            details.append(f"- `{rel}`: JSON parse error: {type(exc).__name__}: {exc}")
            continue
        q = quality_scope(value, "quality")
        qn = quality_scope(value, "quality_note")
        req = required_fields(rel, value)
        date_issues = []
        for location, values in walk_dates(value):
            date_sequence_count += 1
            strings = [item for item in values if isinstance(item, str)]
            bad_iso = [item for item in strings if not _valid_iso_date(item)]
            ordered = strings == sorted(strings)
            duplicate = len(strings) != len(set(strings))
            if bad_iso:
                date_issues.append(f"{location}: invalid date(s) {bad_iso}")
            if not ordered:
                date_issues.append(f"{location}: dates not ascending")
            if duplicate:
                date_issues.append(f"{location}: duplicate dates")
        if isinstance(value, dict) and isinstance(value.get("period"), list):
            period = value["period"]
            if any(not isinstance(item, str) or not _valid_iso_date(item) for item in period):
                date_issues.append("$.period: invalid ISO date")
            elif period != sorted(period):
                date_issues.append("$.period: dates not ascending")
        schema = schema_label(rel)
        schema_result = "not specified" if schema.startswith("not specified") else ("OK" if not req else "missing: " + ", ".join(req))
        results.append((rel, "OK", q, qn, schema_result))
        if req:
            details.append(f"- `{rel}`: contract fields missing: {', '.join(req)}")
        if q == "missing":
            details.append(f"- `{rel}`: dataset-level `quality` missing")
        if qn == "missing":
            details.append(f"- `{rel}`: dataset-level `quality_note` missing")
        details.extend(f"- `{rel}`: {issue}" for issue in date_issues)

    point_checks = []
    point_comparisons = 0
    for rel, points in parsed.items():
        if Path(rel).name != "points.json" or not isinstance(points, list):
            continue
        meta_rel = str(Path(rel).with_name("meta.json")).replace("\\", "/")
        meta = parsed.get(meta_rel)
        meta_dates = meta.get("dates") if isinstance(meta, dict) else None
        for index, point in enumerate(points):
            pdates = point.get("dates") if isinstance(point, dict) else None
            if meta_dates is not None and pdates is not None:
                point_comparisons += 1
                if pdates != meta_dates:
                    point_checks.append(f"`{rel}` point[{index}] dates != `{meta_rel}` dates")
    details.extend(f"- {item}" for item in point_checks)

    lines = [
        "## 2. Veri sözleşmesi (offline)",
        "",
        "| Dosya | Parse | quality alanı | quality_note alanı | Sözleşme şeması |",
        "|---|---|---|---|---|",
    ]
    lines.extend(f"| `{rel}` | {status} | {q} | {qn} | {schema} |" for rel, status, q, qn, schema in results)
    if details:
        lines.extend(["", "### Bulgular", *details])
    else:
        lines.extend(["", "Eksik alan veya tarih sırası sorunu bulunmadı."])
    lines.extend(["", f"JSON/GeoJSON dosyası: {len(files)}; parse hatası: {sum(1 for row in results if row[1] != 'OK')}; tarih dizisi: {date_sequence_count}; points/meta tarih karşılaştırması: {point_comparisons}, uyumsuzluk: {len(point_checks)}; bulgu satırı: {len(details)}."])
    return "\n".join(lines)


def _valid_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def write_section(section: str) -> None:
    QA.parent.mkdir(parents=True, exist_ok=True)
    old = QA.read_text(encoding="utf-8") if QA.exists() else "# PC7 QA notları\n"
    marker = section.splitlines()[0]
    if marker in old:
        before, rest = old.split(marker, 1)
        next_header = re.search(r"\n## \d+\.", rest)
        old = before + section + (rest[next_header.start():] if next_header else "")
    else:
        old = old.rstrip() + "\n\n" + section + "\n"
    QA.write_text(old, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("paths", "data"))
    args = parser.parse_args()
    result = path_report() if args.mode == "paths" else data_report()
    write_section(result)
    print(result)


if __name__ == "__main__":
    main()