"""Wrapper for PC10 global cities: download one .h5 at a time, subset with PC2's subset.py, delete .h5, run PC3's cumulative.py."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))

from pipeline import download as pc2_download
from pipeline import search as pc2_search
from pipeline import subset as pc2_subset
from pipeline.pc10.search_global import CITIES, find_longest_chain

CITY_CONFIG: dict[str, dict] = {
    "mexico_city": {
        "site_key": "global_mexico_city",
        "bbox": CITIES["mexico_city"]["bbox"],
        "path": 113,
    },
    "tehran": {
        "site_key": "global_tehran",
        "bbox": CITIES["tehran"]["bbox"],
        "path": 56,
    },
    "jakarta": {
        "site_key": "global_jakarta",
        "bbox": CITIES["jakarta"]["bbox"],
        "path": 18,
    },
}


def load_chain_from_csv(city: str, path: int) -> list[dict]:
    csv_path = Path(__file__).resolve().parent / f"{city}_p{path}_gunw.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing {csv_path}; run search_global.py first")
    with csv_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return find_longest_chain(rows)


def process_city(city: str, pol: str = "HH", thr: float = 0.3, skip_download: bool = False) -> None:
    cfg = CITY_CONFIG[city]
    site_key = cfg["site_key"]
    bbox = cfg["bbox"]
    path = cfg["path"]

    # Register in-memory without modifying PC2/PC3 files
    pc2_search.SITES[site_key] = {"bbox": bbox, "path": path, "frame": None}

    out_subset_dir = ROOT / "pipeline" / "subset" / site_key
    out_subset_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = ROOT / "raw" / "pc10"
    raw_dir.mkdir(parents=True, exist_ok=True)

    if not skip_download:
        chain = load_chain_from_csv(city, path)
        print(f"[{city}] Processing {len(chain)} consecutive provisional pairs (path {path})")
        for idx, row in enumerate(chain, 1):
            t1, t2 = row["date1"], row["date2"]
            npz_path = out_subset_dir / f"{t1}_{t2}.npz"
            if npz_path.exists():
                print(f"[{city}] ({idx}/{len(chain)}) {npz_path.name} already exists, skipping download")
                continue

            free_gb = pc2_download.check_disk_space(raw_dir)
            print(f"[{city}] ({idx}/{len(chain)}) Free disk: {free_gb:.2f} GB | Downloading {row['granule']}...")
            h5_path = raw_dir / f"{row['granule']}.h5"
            try:
                _, speed = pc2_download.download_file(row["url"], h5_path)
                print(f"[{city}] Downloaded at {speed:.2f} MB/s -> subsetting...")
                info = pc2_subset.subset_gunw(h5_path, site_key, out_subset_dir, pol=pol)
                print(
                    f"[{city}] Saved {info['out_path'].name} | shape={info['shape']} | "
                    f"size={info['size_mb']:.2f} MB | NaN={info['nan_pct']:.2f}% | "
                    f"epsg={info['epsg']} | lambda={info['wavelength']:.5f} m"
                )
            finally:
                if h5_path.exists():
                    h5_path.unlink()
                    print(f"[{city}] Deleted raw {h5_path.name}")
                part_path = h5_path.with_suffix(".h5.part")
                if part_path.exists():
                    part_path.unlink()

    # Run PC3 cumulative.py unmodified via in-memory BBOX registration
    import gunw_io
    import cumulative

    gunw_io.BBOX[site_key] = bbox
    data_dir = ROOT / "data" / "global" / city
    data_dir.mkdir(parents=True, exist_ok=True)

    sys.argv = [
        "cumulative.py",
        site_key,
        "--thr",
        str(thr),
        "--no-names",
        "--data-dir",
        str(data_dir),
    ]
    print(f"[{city}] Running analysis/cumulative.py -> {data_dir}")
    cumulative.main()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("city", choices=sorted(CITY_CONFIG))
    ap.add_argument("--pol", default="HH")
    ap.add_argument("--thr", type=float, default=0.3)
    ap.add_argument("--skip-download", action="store_true")
    args = ap.parse_args()
    process_city(args.city, pol=args.pol, thr=args.thr, skip_download=args.skip_download)
