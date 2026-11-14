"""Offline source/data/text QA for the NISAR Pulse site."""
from __future__ import annotations

import argparse
import html.parser
import json
import re
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
    elif parts and parts[0] == "web":
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


def write_section(section: str) -> None:
    QA.parent.mkdir(parents=True, exist_ok=True)
    old = QA.read_text(encoding="utf-8") if QA.exists() else "# PC7 QA notları\n"
    marker = section.splitlines()[0]
    if marker in old:
        before, rest = old.split(marker, 1)
        next_header = re.search(r"\n## \d+\.", rest)
        if next_header:
            old = before + section + rest[next_header.start():]
        else:
            old = before + section
    else:
        old = old.rstrip() + "\n\n" + section + "\n"
    QA.write_text(old, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("paths",))
    args = parser.parse_args()
    if args.mode == "paths":
        result = path_report()
        write_section(result)
        print(result)


if __name__ == "__main__":
    main()