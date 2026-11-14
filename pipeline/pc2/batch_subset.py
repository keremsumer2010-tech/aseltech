"""Search, download one-by-one, subset, and immediately delete raw GUNW HDF5s for PC2 sites."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

from download import check_disk_space, download_file  # noqa: E402
from search import PROVISIONAL_CUTOFF, SITES, search_site, write_csv  # noqa: E402
from subset import subset_gunw  # noqa: E402

EXTRA_SITES: dict[str, dict] = {
    "delta": {
        "bbox": (-121.85, 37.95, -121.45, 38.20),
        "path": 42,
        "frame": 69,
    },
    "delta_p135": {
        "bbox": (-121.85, 37.95, -121.45, 38.20),
        "path": 135,
        "frame": 21,
    },
    "konya_plain": {
        "bbox": (32.4, 37.4, 33.9, 38.1),
        "path": 7,
        "frame": 69,
    },
    "karapinar_fullyear": {
        "bbox": (33.3, 37.6, 33.8, 37.9),
        "path": 7,
        "frame": 69,
    },
}


def build_consecutive_chain(
    rows: list[dict],
    include_beta: bool = False,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict]:
    """Filter rows and pick the longest consecutive pair chain (preferring P05023 and shortest step)."""
    filtered = []
    for r in rows:
        if r["crid"] != "P05023":
            continue
        if not include_beta and (
            r["quality"] != "provisional"
            or r["date1"] < PROVISIONAL_CUTOFF
            or r["date2"] < PROVISIONAL_CUTOFF
        ):
            continue
        if start_date and r["date1"] < start_date:
            continue
        if end_date and r["date2"] > end_date:
            continue
        filtered.append(r)

    # Deduplicate by (date1, date2), keeping latest granule name
    by_pair: dict[tuple[str, str], dict] = {}
    for r in filtered:
        key = (r["date1"], r["date2"])
        if key not in by_pair or r["granule"] > by_pair[key]["granule"]:
            by_pair[key] = r

    # Group by date1, sort candidates by date2 ascending (prefer 12-day over 24-day)
    by_d1: dict[str, list[dict]] = {}
    for r in by_pair.values():
        by_d1.setdefault(r["date1"], []).append(r)
    for d1 in by_d1:
        by_d1[d1].sort(key=lambda x: x["date2"])

    if not by_d1:
        return []

    # Try starting from each available date1 and pick the chain with maximum total span / pairs
    best_chain: list[dict] = []
    for s_d1 in sorted(by_d1):
        chain: list[dict] = []
        cur = s_d1
        while cur in by_d1:
            nxt = by_d1[cur][0]
            chain.append(nxt)
            cur = nxt["date2"]
        if len(chain) > len(best_chain):
            best_chain = chain
    return best_chain


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    SITES.update(EXTRA_SITES)

    ap = argparse.ArgumentParser()
    ap.add_argument("site", choices=sorted(SITES))
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--csv-path", type=Path, default=None)
    ap.add_argument("--include-beta", action="store_true")
    ap.add_argument("--start-date", default=None)
    ap.add_argument("--end-date", default=None)
    ap.add_argument("--all-frames", action="store_true")
    ap.add_argument("--max-pairs", type=int, default=0, help="0 = all pairs in chain")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out_dir = args.out_dir or (ROOT / "pipeline" / "subset" / args.site)
    csv_path = args.csv_path or (ROOT / "pipeline" / f"{args.site}_gunw.csv")
    raw_dir = ROOT / "raw"

    rows = search_site(args.site, level="GUNW", all_frames=args.all_frames)
    write_csv(rows, csv_path)
    print(f"CSV: {len(rows)} rows -> {csv_path}")

    chain = build_consecutive_chain(
        rows,
        include_beta=args.include_beta,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    if args.max_pairs > 0:
        chain = chain[: args.max_pairs]

    print(f"Selected chain ({len(chain)} pairs):")
    for r in chain:
        print(f"  {r['date1']} -> {r['date2']} ({r['quality']}, {r['size_mb']} MB) {r['granule']}")

    if args.dry_run:
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    for i, r in enumerate(chain, 1):
        npz_path = out_dir / f"{r['date1']}_{r['date2']}.npz"
        if npz_path.exists():
            print(f"[{i}/{len(chain)}] SKIP existing {npz_path.name}")
            continue

        free_gb = check_disk_space(raw_dir, min_free_gb=20.0)
        print(f"[{i}/{len(chain)}] Free disk: {free_gb:.2f} GB | Downloading {r['granule']}...")
        h5_path = raw_dir / f"{r['granule']}.h5"
        part_path = h5_path.with_suffix(".h5.part")
        try:
            _, speed = download_file(r["url"], h5_path, timeout=60, max_attempts=6)
            info = subset_gunw(h5_path, args.site, out_dir)
            print(
                f"[{i}/{len(chain)}] OK {info['out_path'].name} | speed={speed:.2f} MB/s | "
                f"shape={info['shape']} | size={info['size_mb']:.2f} MB | NaN={info['nan_pct']:.2f}% | "
                f"quality={info['quality']} | ion={info['ion_bits']}"
            )
        finally:
            h5_path.unlink(missing_ok=True)
            part_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
