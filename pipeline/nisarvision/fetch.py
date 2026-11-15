"""Authenticated one-by-one HDF5 download + subsetting wrapper."""

from __future__ import annotations

import shutil
from pathlib import Path

from pipeline.download import MIN_FREE_GB, download_file
from pipeline.search import SITES
from pipeline.subset import subset_gunw

ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = ROOT / "raw"


def fetch_subsets(
    name: str,
    bbox: tuple[float, float, float, float],
    chain: list[dict],
    out_dir: Path | None = None,
    resume: bool = True,
) -> list[Path]:
    """Download each granule in chain one-by-one, subset to .npz, and delete raw .h5."""
    subset_dir = out_dir or (ROOT / "pipeline" / "subset" / name)
    subset_dir.mkdir(parents=True, exist_ok=True)
    SITES[name] = {"bbox": bbox}
    saved: list[Path] = []

    for i, row in enumerate(chain, 1):
        out_npz = subset_dir / f"{row['date1']}_{row['date2']}.npz"
        if resume and out_npz.exists():
            print(f"[{i}/{len(chain)}] SKIP existing {out_npz.name}")
            saved.append(out_npz)
            continue

        free_gb = shutil.disk_usage(ROOT).free / 1e9
        if free_gb < MIN_FREE_GB:
            raise RuntimeError(
                f"Low disk space ({free_gb:.2f} GB < {MIN_FREE_GB:.1f} GB); stopping safely."
            )

        print(f"[{i}/{len(chain)}] Free={free_gb:.2f} GB | Downloading {row['granule']}...")
        h5_path, _ = download_file(row["url"], RAW_DIR / f"{row['granule']}.h5")
        try:
            res = subset_gunw(h5_path, name, subset_dir)
            saved.append(res["out_path"])
        finally:
            if h5_path.exists():
                h5_path.unlink()

    return saved
