"""Bbox parsing, quality classification, ASF search, and chain-gap detection."""

from __future__ import annotations

import re
from typing import Iterable

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

CMR_URL = "https://cmr.earthdata.nasa.gov/search/granules.json"
PROVISIONAL_CUTOFF = "2026-06-17"
_UR_RE = re.compile(
    r"NISAR_L2_PR_GUNW_\d+_(\d+)_([AD])_(\d+)_\d+_\d+_[A-Z]+_"
    r"(\d{8})T\d+_(\d{8})T\d+_(\d{8})T\d+_\d{8}T\d+_([PX]\d+)"
)


def parse_bbox(raw: str) -> tuple[float, float, float, float]:
    """Parse 'w,s,e,n' string into validated (west, south, east, north) tuple."""
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 4:
        raise ValueError(f"Expected 4 comma-separated floats w,s,e,n, got: {raw!r}")
    w, s, e, n = (float(x) for x in parts)
    if not (-180.0 <= w < e <= 180.0):
        raise ValueError(f"Invalid longitude bounds: w={w}, e={e}")
    if not (-90.0 <= s < n <= 90.0):
        raise ValueError(f"Invalid latitude bounds: s={s}, n={n}")
    return (w, s, e, n)


def classify_quality(date1: str, date2: str, crid: str = "") -> str:
    """Return 'provisional' if >= 2026-06-17 (and not X-CRID), else 'beta-precal'."""
    if crid.startswith("X"):
        return "beta-precal"
    if min(date1, date2) >= PROVISIONAL_CUTOFF:
        return "provisional"
    return "beta-precal"


def _fmt_date(yyyymmdd: str) -> str:
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"


def build_chain(
    rows: Iterable[dict], quality_mode: str = "provisional"
) -> tuple[list[dict], list[tuple[str, str]]]:
    """Build a non-overlapping temporal chain and report any gaps [(d_end, d_next)]."""
    if quality_mode not in ("provisional", "mixed"):
        raise ValueError(f"Unsupported quality_mode: {quality_mode!r}")
    filtered = [
        r for r in rows if quality_mode == "mixed" or r.get("quality") == "provisional"
    ]
    # Prefer provisional over beta-precal for identical (date1, date2), shortest span first
    best: dict[tuple[str, str], dict] = {}
    for r in filtered:
        key = (r["date1"], r["date2"])
        cur = best.get(key)
        if cur is None or (cur.get("quality") != "provisional" and r.get("quality") == "provisional"):
            best[key] = r

    ordered = sorted(best.values(), key=lambda r: (r["date1"], r["date2"]))
    chain: list[dict] = []
    gaps: list[tuple[str, str]] = []
    for r in ordered:
        if not chain:
            chain.append(r)
            continue
        prev_end = chain[-1]["date2"]
        if r["date1"] == prev_end:
            chain.append(r)
        elif r["date1"] > prev_end:
            gaps.append((prev_end, r["date1"]))
            chain.append(r)
    return chain, gaps


def search_granules(
    bbox: tuple[float, float, float, float],
    start: str,
    end: str,
    track: int | None = None,
    quality_mode: str = "provisional",
) -> tuple[list[dict], list[dict], list[tuple[str, str]], float]:
    """Search NASA CMR for NISAR GUNW granules and build the interferometric chain."""
    collections = ["NISAR_L2_GUNW_PROVISIONAL_V1"]
    if quality_mode == "mixed":
        collections.append("NISAR_L2_GUNW_BETA_V1")

    bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
    temporal = f"{start}T00:00:00Z,{end}T23:59:59Z"
    rows: list[dict] = []
    seen_ur: set[str] = set()

    session = requests.Session()
    session.mount(
        "https://",
        HTTPAdapter(max_retries=Retry(total=5, backoff_factor=1.0, status_forcelist=(500, 502, 503, 504))),
    )

    for short_name in collections:
        resp = session.get(
            CMR_URL,
            params={
                "short_name": short_name,
                "bounding_box": bbox_str,
                "temporal": temporal,
                "page_size": 500,
            },
            timeout=30,
        )
        resp.raise_for_status()
        for entry in resp.json().get("feed", {}).get("entry", []):
            ur = entry.get("title", "")
            if ur in seen_ur:
                continue
            m = _UR_RE.search(ur)
            if not m:
                continue
            path_num = int(m.group(1))
            if track is not None and path_num != track:
                continue
            d1, d2 = _fmt_date(m.group(4)), _fmt_date(m.group(6))
            crid = m.group(7)
            if d1 < start or d2 > end:
                continue
            h5_url = next(
                (lk["href"] for lk in entry.get("links", []) if lk.get("href", "").endswith(".h5")),
                "",
            )
            if not h5_url:
                continue
            seen_ur.add(ur)
            rows.append(
                {
                    "granule": ur,
                    "path": path_num,
                    "direction": m.group(2),
                    "frame": int(m.group(3)),
                    "date1": d1,
                    "date2": d2,
                    "crid": crid,
                    "url": h5_url,
                    "size_mb": float(entry.get("granule_size") or 0.0),
                    "quality": classify_quality(d1, d2, crid),
                }
            )

    # Pick dominant track/frame if track not specified
    if track is None and rows:
        counts: dict[tuple[int, int], int] = {}
        for r in rows:
            pf = (r["path"], r["frame"])
            counts[pf] = counts.get(pf, 0) + 1
        dom_pf = max(counts, key=lambda k: counts[k])
        rows = [r for r in rows if (r["path"], r["frame"]) == dom_pf]

    chain, gaps = build_chain(rows, quality_mode=quality_mode)
    total_mb = sum(r["size_mb"] for r in chain)
    return rows, chain, gaps, total_mb
