"""Search ASF for NISAR L2 GUNW provisional (P05023, >= 2026-06-17) pairs for PC10 global cities."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import asf_search as asf

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipeline.search import DATE_RE, PROVISIONAL_CUTOFF, _extract_size_mb, _fmt_date, bbox_to_wkt

CITIES: dict[str, dict] = {
    "mexico_city": {
        "bbox": (-99.25, 19.25, -98.90, 19.60),
        "paths": [113, 19],
    },
    "tehran": {
        "bbox": (51.10, 35.45, 51.65, 35.85),
        "paths": [56],
    },
    "jakarta": {
        "bbox": (106.65, -6.38, 107.02, -6.08),
        "paths": [18],
    },
    "beijing": {
        "bbox": (116.25, 39.75, 116.85, 40.15),
        "paths": [47],
    },
}


def search_city(city: str, path: int) -> list[dict]:
    cfg = CITIES[city]
    results = asf.search(
        platform="NISAR",
        processingLevel="GUNW",
        intersectsWith=bbox_to_wkt(cfg["bbox"]),
        relativeOrbit=path,
    )
    rows: list[dict] = []
    seen: set[str] = set()
    for r in results:
        props = r.properties
        granule = props.get("fileID") or props.get("sceneName") or ""
        if not granule or granule in seen:
            continue
        seen.add(granule)

        m = DATE_RE.search(granule)
        if m:
            date1 = _fmt_date(m.group(1))
            date2 = _fmt_date(m.group(2))
            crid = props.get("crid") or m.group(3)
        else:
            date1 = (props.get("startTime") or "")[:10]
            date2 = (props.get("stopTime") or "")[:10]
            crid = props.get("crid") or ""

        quality = (
            "provisional"
            if (crid == "P05023" and date1 >= PROVISIONAL_CUTOFF and date2 >= PROVISIONAL_CUTOFF)
            else "beta-precal"
        )
        rows.append(
            {
                "granule": granule,
                "path": props.get("pathNumber"),
                "frame": props.get("frameNumber"),
                "direction": props.get("flightDirection"),
                "date1": date1,
                "date2": date2,
                "crid": crid,
                "url": props.get("url", ""),
                "size_mb": _extract_size_mb(props, granule),
                "quality": quality,
            }
        )
    rows.sort(key=lambda x: (str(x["frame"]), x["date1"], x["date2"], x["crid"]))
    return rows


def find_longest_chain(rows: list[dict]) -> list[dict]:
    """Find longest consecutive gap-free provisional chain within a single frame."""
    prov = [r for r in rows if r["quality"] == "provisional"]
    by_frame: dict = {}
    for r in prov:
        by_frame.setdefault(r["frame"], []).append(r)

    best_chain: list[dict] = []
    for frame, fr_rows in by_frame.items():
        # Group by (date1, date2) keeping one per pair
        pairs = {}
        for r in fr_rows:
            k = (r["date1"], r["date2"])
            if k not in pairs:
                pairs[k] = r
        sorted_pairs = [pairs[k] for k in sorted(pairs)]
        # Build all chains
        by_d1: dict[str, list[dict]] = {}
        for r in sorted_pairs:
            by_d1.setdefault(r["date1"], []).append(r)

        def dfs(curr: dict) -> list[dict]:
            best_sub: list[dict] = []
            for nxt in by_d1.get(curr["date2"], []):
                cand = dfs(nxt)
                if len(cand) > len(best_sub):
                    best_sub = cand
            return [curr] + best_sub

        for start in sorted_pairs:
            ch = dfs(start)
            if len(ch) > len(best_chain):
                best_chain = ch
    return best_chain


if __name__ == "__main__":
    city_arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    targets = list(CITIES) if city_arg == "all" else [city_arg]
    out_dir = Path(__file__).resolve().parent
    for c in targets:
        for p in CITIES[c]["paths"]:
            rows = search_city(c, p)
            csv_path = out_dir / f"{c}_p{p}_gunw.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as f:
                if rows:
                    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                    w.writeheader()
                    w.writerows(rows)
            prov = [r for r in rows if r["quality"] == "provisional"]
            chain = find_longest_chain(rows)
            print(f"=== {c} path {p}: total={len(rows)}, provisional={len(prov)}, longest_chain={len(chain)} ===")
            for r in chain:
                print(f"  frame={r['frame']} {r['date1']} -> {r['date2']} ({r['size_mb']} MB) {r['granule']}")
