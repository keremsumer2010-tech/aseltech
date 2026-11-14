"""CLI entrypoint for `python -m pipeline.nisarpulse`."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from pipeline.nisarpulse.catalog import upsert_catalog
from pipeline.nisarpulse.search import parse_bbox, search_granules

ROOT = Path(__file__).resolve().parent.parent.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pipeline.nisarpulse",
        description="NISAR Pulse: single-command InSAR subsidence pipeline.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run_p = sub.add_parser("run", help="Search, download, subset, process, and register a site.")
    run_p.add_argument("--name", required=True, help="Site identifier (e.g. delta).")
    run_p.add_argument("--bbox", required=True, help="Bounding box as w,s,e,n.")
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
    run_p.add_argument("--title", default=None, help="Optional human title for catalog.json.")
    run_p.add_argument("--no-catalog", action="store_true", help="Skip updating data/catalog.json.")
    return parser


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    raw = list(argv) if argv is not None else sys.argv[1:]
    normalized: list[str] = []
    i = 0
    while i < len(raw):
        if raw[i] == "--bbox" and i + 1 < len(raw) and raw[i + 1].startswith("-"):
            normalized.append(f"--bbox={raw[i + 1]}")
            i += 2
        else:
            normalized.append(raw[i])
            i += 1
    return build_parser().parse_args(normalized)


def main(argv: list[str] | None = None) -> int:
    args = parse_cli_args(argv)
    if args.command != "run":
        return 1

    t0 = time.monotonic()
    bbox = parse_bbox(args.bbox)
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
        raise RuntimeError("No interferometric pairs found for the requested parameters.")

    from pipeline.nisarpulse.fetch import fetch_subsets
    from pipeline.nisarpulse.process import run_cumulative

    fetch_subsets(args.name, bbox, chain, resume=args.resume)
    data_dir, meta, summary = run_cumulative(
        args.name, bbox, quality_mode=args.quality
    )
    if not args.no_catalog:
        upsert_catalog(ROOT / "data" / "catalog.json", args.name, bbox, meta, title=args.title)

    print(
        f"Done [{args.name}] -> {data_dir} | max_subsidence_cm={summary.get('max_subsidence_cm')} "
        f"| elapsed={time.monotonic() - t0:.1f}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
