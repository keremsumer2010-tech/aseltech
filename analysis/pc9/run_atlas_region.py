"""PC9 wrapper for `pipeline.nisarpulse` that guards against all-NaN DEM caches.

Without modifying PC3's `analysis/cumulative.py` or `pipeline/nisarpulse/`,
this wrapper removes any cached `analysis/out/<site>_dem.npy` with zero finite
pixels and ensures `dem.dem_on_grid` raises `RuntimeError` instead of returning
an all-NaN array so `cumulative.py` falls back cleanly to plane-only deramp.
"""
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
ANALYSIS_DIR = ROOT / "analysis"
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

import dem as _dem  # noqa: E402
from pipeline.nisarpulse.__main__ import main as _nisarpulse_main  # noqa: E402


def _clean_nan_dem_caches() -> None:
    out_dir = ROOT / "analysis" / "out"
    if not out_dir.exists():
        return
    for npy in out_dir.glob("*_dem.npy"):
        try:
            arr = np.load(npy)
            if int(np.isfinite(arr).sum()) < 100:
                npy.unlink()
        except Exception:
            pass


def main(argv: list[str] | None = None) -> int:
    _clean_nan_dem_caches()
    orig_dem_on_grid = _dem.dem_on_grid

    def _safe_dem_on_grid(x, y, epsg):
        arr = orig_dem_on_grid(x, y, epsg)
        if arr is None or int(np.isfinite(arr).sum()) < 100:
            raise RuntimeError("DEM has <100 finite pixels; using plane-only deramp")
        return arr

    _dem.dem_on_grid = _safe_dem_on_grid
    rc = _nisarpulse_main(argv)
    if rc == 0:
        _enrich_summary(argv if argv is not None else sys.argv[1:])
    return rc


def _enrich_summary(args: list[str]) -> None:
    import json
    from datetime import date

    if "--dry-run" in args:
        return
    name = None
    data_dir = None
    for i, tok in enumerate(args):
        if tok == "--name" and i + 1 < len(args):
            name = args[i + 1]
        elif tok == "--data-dir" and i + 1 < len(args):
            data_dir = Path(args[i + 1])
    if not name:
        return
    if data_dir is None:
        data_dir = ROOT / "data" / name
    elif not data_dir.is_absolute():
        data_dir = ROOT / data_dir
    summary_p = data_dir / "summary.json"
    cum_p = ROOT / "analysis" / "out" / f"{name}_cum.npz"
    if not summary_p.exists() or not cum_p.exists():
        return
    s = json.loads(summary_p.read_text(encoding="utf-8"))
    with np.load(cum_p) as d:
        arr = d["cum_cm"] if "cum_cm" in d.files else d[d.files[0]]
        valid = arr[np.isfinite(arr)]
        s["p2_cm"] = round(float(np.nanpercentile(valid, 2)), 1) if valid.size else None
        s["valid_fraction"] = round(float(np.isfinite(arr).mean()), 3)
    nd = (date.fromisoformat(s["period"][1]) - date.fromisoformat(s["period"][0])).days
    if nd > 0:
        s["rate_cm_per_100d"] = round(float(s["max_subsidence_cm"]) / nd * 100.0, 2)
    summary_p.write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
