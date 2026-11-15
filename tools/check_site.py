"""Check every local link and image on the published site (PC1).

Mirrors the folder layout that .github/workflows/pages.yml publishes:
  web/ -> site root, data/ -> data/, game/ -> game/, docs/story -> docs/story,
  docs/bulletins -> docs/bulletins and bulletins/.
Reports links whose target file does not exist. Usage: python tools/check_site.py
Exit code 1 if anything is broken.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
MOUNTS = [  # (site prefix, repo folder) longest prefix first
    ("docs/bulletins/", ROOT / "docs" / "bulletins"),
    ("docs/story/", ROOT / "docs" / "story"),
    ("bulletins/", ROOT / "docs" / "bulletins"),
    ("data/", ROOT / "data"),
    ("game/", ROOT / "game"),
    ("web3d/", ROOT / "web3d"),
    ("", ROOT / "web"),
]
GENERATED = {"data/global/atlas.geojson", "data/global/atlas.csv"}  # made by the deploy workflow


def site_to_repo(site_path: str) -> Path | None:
    for prefix, folder in MOUNTS:
        if site_path.startswith(prefix):
            return folder / site_path[len(prefix):]
    return None


def repo_to_site(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    for prefix, folder in MOUNTS:
        f = folder.relative_to(ROOT).as_posix() + "/"
        if rel.startswith(f):
            return prefix + rel[len(f):]
    return rel


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.found: list[tuple[str, str, bool]] = []  # (attr, value, root_relative)

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if not v:
                continue
            if k in ("href", "src", "poster"):
                self.found.append((k, v, False))
            elif k in ("data-rsrc", "data-rhref"):
                self.found.append((k, v, True))


def resolve(page_site: str, value: str, root_rel: bool) -> str | None:
    if re.match(r"^(https?:|mailto:|tel:|data:|javascript:|#|//)", value) or "${" in value:
        return None
    path = unquote(urlsplit(value).path)
    if not path:
        return None
    base = [] if root_rel else page_site.split("/")[:-1]
    parts = base + path.split("/")
    out: list[str] = []
    for p in parts:
        if p in ("", "."):
            continue
        if p == "..":
            if out:
                out.pop()
            continue
        out.append(p)
    target = "/".join(out)
    if path.endswith("/"):
        target += "/index.html"
    return target


def pages() -> list[Path]:
    files = list((ROOT / "web").glob("*.html")) + list((ROOT / "game").glob("*.html"))
    files += list((ROOT / "docs" / "bulletins").glob("*.html")) + list((ROOT / "docs" / "story").glob("*.html"))
    return sorted(files)


def check() -> list[str]:
    broken = []
    for page in pages():
        site = repo_to_site(page)
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for attr, value, root_rel in parser.found:
            target = resolve(site, value, root_rel)
            if target is None or target in GENERATED:
                continue
            repo = site_to_repo(target)
            if repo is None or not repo.exists():
                broken.append(f"{page.relative_to(ROOT).as_posix()}: {attr}=\"{value}\" -> {target}")
    return broken


if __name__ == "__main__":
    bad = check()
    print(f"{len(pages())} pages checked, {len(bad)} broken links")
    for b in bad:
        print("  " + b)
    sys.exit(1 if bad else 0)
