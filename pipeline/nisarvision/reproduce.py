"""Reproduce any atlas region's summary from its meta.json granule list."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GRANULE_DATE_RE = re.compile(r"_(\d{8})T\d{6}_\d{8}T\d{6}_(\d{8})T\d{6}_")


def find_region_dir(region_id: str, root: Path = ROOT) -> Path:
    """Locate data/global/<id> or data/<id> containing meta.json."""
    for cand in (root / "data" / "global" / region_id, root / "data" / region_id):
        if (cand / "meta.json").exists():
            return cand
    raise FileNotFoundError(f"No meta.json found for region '{region_id}'")


def parse_granule_pair(granule: str) -> tuple[str, str]:
    """Extract (YYYY-MM-DD, YYYY-MM-DD) pair dates from a NISAR GUNW granule ID."""
    m = GRANULE_DATE_RE.search(granule)
    if not m:
        raise ValueError(f"Could not parse dates from granule: {granule!r}")
    d1, d2 = m.group(1), m.group(2)
    return f"{d1[:4]}-{d1[4:6]}-{d1[6:8]}", f"{d2[:4]}-{d2[4:6]}-{d2[6:8]}"


def find_cached_subsets(
    region_id: str,
    granules: list[str],
    root: Path = ROOT,
) -> tuple[list[Path], list[str]]:
    """Check local subset caches for .npz files matching each granule's date pair."""
    search_dirs = [
        root / "pipeline" / "subset" / region_id,
        root / "pipeline" / "subset" / f"global_{region_id}",
        root / "analysis" / "out" / "subset" / region_id,
    ]
    found: list[Path] = []
    missing: list[str] = []
    for gran in granules:
        d1, d2 = parse_granule_pair(gran)
        fname = f"{d1}_{d2}.npz"
        hit = next((d / fname for d in search_dirs if (d / fname).exists()), None)
        if hit is not None:
            found.append(hit)
        else:
            missing.append(gran)
    return found, missing


def reproduce_region(
    region_id: str,
    out_dir: Path | None = None,
    qc: bool = True,
    dry_run: bool = False,
    root: Path = ROOT,
) -> dict:
    """Reproduce a region from its meta.json granule list using cached subsets, or emit a dry-run plan."""
    t0 = time.monotonic()
    region_dir = find_region_dir(region_id, root=root)
    meta = json.loads((region_dir / "meta.json").read_text(encoding="utf-8"))
    summary_path = region_dir / "summary.json"
    orig_summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}

    bbox = tuple(float(v) for v in meta["bbox"])
    granules = list(meta.get("granules", []))
    found, missing = find_cached_subsets(region_id, granules, root=root)

    if dry_run or missing:
        return {
            "mode": "dry-run",
            "region": region_id,
            "region_dir": str(region_dir),
            "bbox": list(bbox),
            "granules": len(granules),
            "cached": len(found),
            "missing": missing,
            "quality": orig_summary.get("quality", "provisional"),
            "elapsed_s": round(time.monotonic() - t0, 3),
        }

    from pipeline.nisarvision.process import run_cumulative

    target_out = out_dir or (root / "analysis" / "out" / f"repro_{region_id}")
    quality_mode = "mixed" if orig_summary.get("quality") == "mixed" else "provisional"
    _, _, repro_summary = run_cumulative(
        region_id,
        bbox,  # type: ignore[arg-type]
        data_dir=target_out,
        quality_mode=quality_mode,
        qc=qc,
    )
    diff_max = None
    if "max_subsidence_cm" in orig_summary and "max_subsidence_cm" in repro_summary:
        diff_max = round(
            float(repro_summary["max_subsidence_cm"]) - float(orig_summary["max_subsidence_cm"]),
            3,
        )
    return {
        "mode": "reproduced",
        "region": region_id,
        "region_dir": str(region_dir),
        "out_dir": str(target_out),
        "granules": len(granules),
        "cached": len(found),
        "original": {
            "max_subsidence_cm": orig_summary.get("max_subsidence_cm"),
            "range_cm": orig_summary.get("range_cm"),
            "rate_cm_per_yr_estimate": orig_summary.get("rate_cm_per_yr_estimate"),
            "period": orig_summary.get("period"),
            "n_pairs": orig_summary.get("n_pairs"),
        },
        "reproduced": {
            "max_subsidence_cm": repro_summary.get("max_subsidence_cm"),
            "range_cm": repro_summary.get("range_cm"),
            "rate_cm_per_yr_estimate": repro_summary.get("rate_cm_per_yr_estimate"),
            "period": repro_summary.get("period"),
            "n_pairs": repro_summary.get("n_pairs"),
        },
        "diff_max_cm": diff_max,
        "elapsed_s": round(time.monotonic() - t0, 3),
    }
