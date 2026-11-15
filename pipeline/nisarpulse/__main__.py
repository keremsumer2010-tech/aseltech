"""CLI entrypoint for `python -m pipeline.nisarpulse`."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from pipeline.nisarpulse.catalog import upsert_catalog
from pipeline.nisarpulse.search import bbox_from_center, parse_bbox, search_granules

ROOT = Path(__file__).resolve().parent.parent.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pipeline.nisarpulse",
        description="NISAR Pulse: single-command InSAR subsidence pipeline.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run_p = sub.add_parser("run", help="Search, download, subset, process, and register a site.")
    run_p.add_argument("--name", required=True, help="Site identifier (e.g. delta).")
    run_p.add_argument("--bbox", default=None, help="Bounding box as w,s,e,n.")
    run_p.add_argument("--center", default=None, help="Center lon,lat (used with --box-deg).")
    run_p.add_argument("--box-deg", type=float, default=0.25, help="Half-box size in deg (default 0.25).")
    run_p.add_argument("--ref-lonlat", default=None, help="Out-of-basin reference lon,lat.")
    run_p.add_argument("--start", required=True, help="Start date YYYY-MM-DD.")
    run_p.add_argument("--end", required=True, help="End date YYYY-MM-DD.")
    run_p.add_argument("--track", type=int, default=None, help="Optional relative orbit / path.")
    run_p.add_argument(
        "--quality",
        choices=("provisional", "mixed"),
        default="provisional",
        help="Quality filter: provisional (>=2026-06-17) or mixed (beta-precal+provisional).",
    )
    run_p.add_argument("--dry-run", action="store_true", help="Plan only; do not download.")
    run_p.add_argument("--resume", action="store_true", help="Reuse existing .npz subsets.")
    run_p.add_argument("--data-dir", type=Path, default=None, help="Output data dir (default: data/<name>).")
    run_p.add_argument("--title", default=None, help="Optional human title for catalog.json.")
    run_p.add_argument("--no-catalog", action="store_true", help="Skip updating data/catalog.json.")
    run_p.add_argument("--qc", dest="qc", action="store_true", default=True, help="Enable pixel-level QC (default).")
    run_p.add_argument("--no-qc", dest="qc", action="store_false", help="Disable pixel-level QC.")

    rep_p = sub.add_parser("reproduce", help="Reproduce a region's summary from its meta.json granule list.")
    rep_p.add_argument("region", help="Region id (e.g. konya_plain, mashhad).")
    rep_p.add_argument("--out-dir", type=Path, default=None, help="Output directory (default: analysis/out/repro_<id>).")
    rep_p.add_argument("--dry-run", action="store_true", help="Print reproduction plan without running cumulative.")
    rep_p.add_argument("--qc", dest="qc", action="store_true", default=True, help="Enable pixel-level QC (default).")
    rep_p.add_argument("--no-qc", dest="qc", action="store_false", help="Disable pixel-level QC.")
    return parser


def write_coverage_report(
    out_path: Path,
    name: str,
    bbox: tuple[float, float, float, float],
    quality: str,
    rows: list[dict],
    chain: list[dict],
    gaps: list[tuple[str, str]],
    total_mb: float,
    error: str | None = None,
) -> dict:
    """Write coverage.json summarizing ASF granule availability and chain gaps."""
    status = "none" if not chain else ("partial" if gaps else "ok")
    report = {
        "site": name,
        "bbox": list(bbox),
        "quality": quality,
        "coverage": status,
        "granules": len(rows),
        "chain_pairs": len(chain),
        "path": chain[0]["path"] if chain else None,
        "frame": chain[0]["frame"] if chain else None,
        "period": [chain[0]["date1"], chain[-1]["date2"]] if chain else None,
        "gaps": [[a, b] for a, b in gaps],
        "total_raw_mb": round(total_mb, 1),
        "error": error,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    raw = list(argv) if argv is not None else sys.argv[1:]
    normalized: list[str] = []
    i = 0
    while i < len(raw):
        if raw[i] in ("--bbox", "--center", "--ref-lonlat") and i + 1 < len(raw) and raw[i + 1].startswith("-"):
            normalized.append(f"{raw[i]}={raw[i + 1]}")
            i += 2
        else:
            normalized.append(raw[i])
            i += 1
    return build_parser().parse_args(normalized)


def parse_ref_lonlat(raw: str | None) -> tuple[float, float] | None:
    if not raw:
        return None
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 2:
        raise ValueError(f"Expected 'lon,lat' for --ref-lonlat, got: {raw!r}")
    return (float(parts[0]), float(parts[1]))


def main(argv: list[str] | None = None) -> int:
    args = parse_cli_args(argv)
    if args.command == "reproduce":
        from pipeline.nisarpulse.reproduce import reproduce_region

        res = reproduce_region(args.region, out_dir=args.out_dir, qc=args.qc, dry_run=args.dry_run)
        print(json.dumps(res, indent=2))
        return 0
    if args.command != "run":
        return 1

    t0 = time.monotonic()
    if args.bbox:
        bbox = parse_bbox(args.bbox)
    elif args.center:
        bbox = bbox_from_center(args.center, box_deg=args.box_deg)
    else:
        raise SystemExit("Provide either --bbox w,s,e,n or --center lon,lat")
    ref_lonlat = parse_ref_lonlat(args.ref_lonlat)
    target_data_dir = args.data_dir or (ROOT / "data" / args.name)
    rows, chain, gaps, total_mb = search_granules(
        bbox, args.start, args.end, track=args.track, quality_mode=args.quality
    )
    print(
        f"NISAR Pulse [{args.name}] bbox={bbox} quality={args.quality} | "
        f"granules={len(rows)} chain_pairs={len(chain)} total_raw={total_mb:.1f} MB gaps={len(gaps)}"
    )
    for g0, g1 in gaps:
        print(f"  GAP: {g0} -> {g1}")
    for r in chain:
        print(
            f"  {r['date1']} -> {r['date2']} ({r['quality']}, {r['size_mb']:.1f} MB) "
            f"P{r['path']:03d} F{r['frame']:03d} {r['granule']}"
        )

    if args.dry_run:
        print(f"Dry-run complete in {time.monotonic() - t0:.2f}s (no files downloaded).")
        return 0

    if not chain:
        write_coverage_report(
            target_data_dir / "coverage.json",
            args.name,
            bbox,
            args.quality,
            rows,
            chain,
            gaps,
            total_mb,
            error="No interferometric pairs found.",
        )
        print(f"No coverage for [{args.name}]; wrote {target_data_dir / 'coverage.json'}.")
        return 0

    from pipeline.nisarpulse.fetch import fetch_subsets
    from pipeline.nisarpulse.process import run_cumulative

    try:
        fetch_subsets(args.name, bbox, chain, resume=args.resume)
        data_dir, meta, summary = run_cumulative(
            args.name, bbox, data_dir=target_data_dir, quality_mode=args.quality, ref_lonlat=ref_lonlat, qc=args.qc
        )
        write_coverage_report(
            data_dir / "coverage.json", args.name, bbox, args.quality, rows, chain, gaps, total_mb
        )
        if not args.no_catalog:
            upsert_catalog(ROOT / "data" / "catalog.json", args.name, bbox, meta, title=args.title)
    except Exception as exc:
        write_coverage_report(
            target_data_dir / "coverage.json",
            args.name,
            bbox,
            args.quality,
            rows,
            chain,
            gaps,
            total_mb,
            error=str(exc),
        )
        raise

    print(
        f"Done [{args.name}] -> {data_dir} | max_subsidence_cm={summary.get('max_subsidence_cm')} "
        f"| elapsed={time.monotonic() - t0:.1f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
