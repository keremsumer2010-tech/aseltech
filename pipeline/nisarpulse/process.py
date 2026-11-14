"""Wrapper around analysis/cumulative.py without modifying upstream analysis code."""

from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent


def compute_quality_metrics(
    cum_grid: np.ndarray,
    max_sub_cm: float,
    period: list[str],
    range_cm: list[float] | None,
) -> dict:
    """Compute p2_cm, rate_cm_per_100d, valid_fraction, and confidence per ATLAS_PLANI §1-§4."""
    finite = cum_grid[np.isfinite(cum_grid)]
    p2_cm = round(float(np.percentile(finite, 2)), 2) if finite.size else None
    valid_fraction = round(float(np.isfinite(cum_grid).mean()), 3) if cum_grid.size else 0.0

    d0 = date.fromisoformat(period[0])
    d1 = date.fromisoformat(period[1])
    days = max(1, (d1 - d0).days)
    rate_100d = round(float(max_sub_cm) / days * 100.0, 2)

    spread_ok = False
    if range_cm and len(range_cm) >= 2 and abs(max_sub_cm) > 1e-6:
        spread_ok = (abs(max(range_cm) - min(range_cm)) / abs(max_sub_cm)) < 0.30

    if valid_fraction >= 0.40 and spread_ok:
        confidence = "high"
    elif valid_fraction >= 0.25:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "p2_cm": p2_cm,
        "rate_cm_per_100d": rate_100d,
        "valid_fraction": valid_fraction,
        "confidence": confidence,
    }


def _apply_ref_lonlat(
    out_dir: Path,
    cum_npz_path: Path,
    ref_lonlat: tuple[float, float],
) -> np.ndarray:
    """Shift cumulative grid, summary.json, and points.json to an out-of-basin reference."""
    from pyproj import Transformer

    with np.load(cum_npz_path) as d:
        cum = np.array(d["cum_cm"], dtype=np.float32)
        x = d["x"]
        y = d["y"]
        epsg = int(d["epsg"])

    tr = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    rx, ry = tr.transform(ref_lonlat[0], ref_lonlat[1])
    c = int(np.argmin(np.abs(x - rx)))
    r = int(np.argmin(np.abs(y - ry)))
    win = cum[max(0, r - 6) : r + 7, max(0, c - 6) : c + 7]
    finite = win[np.isfinite(win)]
    if finite.size == 0:
        raise ValueError(f"No valid pixels near --ref-lonlat {ref_lonlat}")
    offset = float(np.median(finite))
    cum_shifted = cum - offset

    summary_path = out_dir / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["max_subsidence_cm"] = round(float(summary["max_subsidence_cm"]) - offset, 1)
    inc_deg = summary.get("incidence_deg_at_max")
    if inc_deg is not None:
        summary["max_subsidence_vertical_cm_estimate"] = round(
            summary["max_subsidence_cm"] / math.cos(math.radians(float(inc_deg))), 1
        )
    summary["reference_point"] = {
        "lon": ref_lonlat[0],
        "lat": ref_lonlat[1],
        "source": "ref_lonlat",
    }
    summary_path.write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")

    points_path = out_dir / "points.json"
    if points_path.exists():
        pts = json.loads(points_path.read_text(encoding="utf-8"))
        for pt in pts:
            vals = pt.get("disp_cm", [])
            if vals:
                n = max(1, len(vals) - 1)
                pt["disp_cm"] = [
                    round(float(v) - offset * (i / n), 2) if v is not None else None
                    for i, v in enumerate(vals)
                ]
        points_path.write_text(json.dumps(pts, indent=1) + "\n", encoding="utf-8")

    return cum_shifted


def run_cumulative(
    name: str,
    bbox: tuple[float, float, float, float],
    data_dir: Path | None = None,
    quality_mode: str = "provisional",
    ref_lonlat: tuple[float, float] | None = None,
) -> tuple[Path, dict, dict]:
    """Register site bbox at runtime, invoke analysis/cumulative.py, and add quality metrics."""
    analysis_dir = str(ROOT / "analysis")
    if analysis_dir not in sys.path:
        sys.path.insert(0, analysis_dir)

    import cumulative  # noqa: E402
    import gunw_io  # noqa: E402

    gunw_io.BBOX[name] = bbox
    out_dir = data_dir or (ROOT / "data" / name)
    argv_backup = list(sys.argv)
    try:
        sys.argv = ["cumulative.py", name, "--data-dir", str(out_dir)]
        if quality_mode == "mixed":
            sys.argv.append("--mixed")
        cumulative.main()
    finally:
        sys.argv = argv_backup

    tag = f"{name}_fullyear" if quality_mode == "mixed" else name
    cum_npz = ROOT / "analysis" / "out" / f"{tag}_cum.npz"
    if ref_lonlat is not None and cum_npz.exists():
        cum_grid = _apply_ref_lonlat(out_dir, cum_npz, ref_lonlat)
    elif cum_npz.exists():
        with np.load(cum_npz) as d:
            cum_grid = np.array(d["cum_cm"], dtype=np.float32)
    else:
        cum_grid = np.array([], dtype=np.float32)

    meta = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))
    summary_path = out_dir / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    metrics = compute_quality_metrics(
        cum_grid,
        float(summary["max_subsidence_cm"]),
        summary["period"],
        summary.get("range_cm"),
    )
    summary.update(metrics)
    summary_path.write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    return out_dir, meta, summary
