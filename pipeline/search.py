"""Search ASF for NISAR GUNW products over a project site and export CSV."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import asf_search as asf

SITES: dict[str, dict] = {
    "central_valley": {
        "bbox": (-120.2, 35.6, -119.0, 36.6),
        "path": 34,
        "frame": 20,
    },
    "karapinar": {
        "bbox": (33.3, 37.6, 33.8, 37.9),
        "path": 7,
        "frame": None,
    },
    "konya": {
        "bbox": (32.4, 37.4, 33.9, 38.1),
        "path": 7,
        "frame": None,
    },
    "fens": {
        "bbox": (-0.3, 52.4, 0.4, 52.9),
        "path": None,
        "frame": None,
    },
}

PROVISIONAL_CUTOFF = "2026-06-17"
DATE_RE = re.compile(
    r"_(\d{8})T\d{6}_\d{8}T\d{6}_(\d{8})T\d{6}_\d{8}T\d{6}_([A-Z]\d{5})_"
)


def bbox_to_wkt(bbox: tuple[float, float, float, float]) -> str:
    w, s, e, n = bbox
    return f"POLYGON(({w} {s}, {e} {s}, {e} {n}, {w} {n}, {w} {s}))"


def _fmt_date(yyyymmdd: str) -> str:
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"


def _extract_size_mb(props: dict, granule: str) -> float:
    b = props.get("bytes")
    if isinstance(b, dict):
        h5_key = f"{granule}.h5"
        if h5_key in b and isinstance(b[h5_key], dict):
            total_bytes = b[h5_key].get("bytes", 0)
        else:
            total_bytes = sum(
                v.get("bytes", 0) for v in b.values() if isinstance(v, dict)
            )
    elif isinstance(b, (int, float)):
        total_bytes = b
    else:
        total_bytes = 0
    return round(float(total_bytes) / (1024 * 1024), 2)


def search_site(
    site: str,
    level: str = "GUNW",
    all_frames: bool = False,
) -> list[dict]:
    if site not in SITES:
        raise ValueError(f"Unknown site '{site}'. Valid: {sorted(SITES)}")

    cfg = SITES[site]
    kwargs: dict = {
        "platform": "NISAR",
        "processingLevel": level,
        "intersectsWith": bbox_to_wkt(cfg["bbox"]),
    }
    if cfg["path"] is not None:
        kwargs["relativeOrbit"] = cfg["path"]
    if not all_frames and cfg["frame"] is not None:
        kwargs["frame"] = cfg["frame"]

    results = asf.search(**kwargs)

    rows: list[dict] = []
    seen: set[str] = set()
    for r in results:
        props = r.properties
        granule = props.get("fileID") or props.get("sceneName") or ""
        if not granule or granule in seen:
            continue
        seen.add(granule)

        if not all_frames and cfg["frame"] is not None:
            if props.get("frameNumber") != cfg["frame"]:
                continue

        m = DATE_RE.search(granule)
        if m:
            date1 = _fmt_date(m.group(1))
            date2 = _fmt_date(m.group(2))
            crid = props.get("crid") or m.group(3)
        else:
            start = (props.get("startTime") or "")[:10]
            stop = (props.get("stopTime") or "")[:10]
            date1, date2 = start, stop
            crid = props.get("crid") or ""

        quality = (
            "provisional"
            if (date1 >= PROVISIONAL_CUTOFF and date2 >= PROVISIONAL_CUTOFF)
            else "beta-precal"
        )

        rows.append(
            {
                "granule": granule,
                "date1": date1,
                "date2": date2,
                "crid": crid,
                "url": props.get("url", ""),
                "size_mb": _extract_size_mb(props, granule),
                "quality": quality,
            }
        )

    rows.sort(key=lambda x: (x["date1"], x["date2"], x["crid"], x["granule"]))
    return rows


def write_csv(rows: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["granule", "date1", "date2", "crid", "url", "size_mb", "quality"]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Search ASF for NISAR GUNW granules.")
    parser.add_argument(
        "site",
        nargs="?",
        default="central_valley",
        choices=sorted(SITES),
        help="Site name defined in VERI_SOZLESMESI.md",
    )
    parser.add_argument("--level", default="GUNW", help="ASF processingLevel")
    parser.add_argument(
        "--all-frames",
        action="store_true",
        help="Do not filter to primary frameNumber",
    )
    args = parser.parse_args()

    rows = search_site(args.site, level=args.level, all_frames=args.all_frames)
    out_path = Path(__file__).resolve().parent / f"{args.site}_{args.level.lower()}.csv"
    write_csv(rows, out_path)

    prov_count = sum(1 for r in rows if r["quality"] == "provisional" and r["crid"] == "P05023")
    print(f"Wrote {len(rows)} rows ({prov_count} provisional P05023) -> {out_path}")


if __name__ == "__main__":
    main()
