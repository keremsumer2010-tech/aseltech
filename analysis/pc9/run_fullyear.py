"""PC9 wrapper for Q08 full-year Central Valley cumulative & seasonal decomposition.

Runs PC3's `analysis/cumulative.py` (--mixed) and `analysis/decomp/run_decomp.py`
without modifying any PC3 file, handling missing local Copernicus DEM tiles cleanly
via cumulative.py's built-in plane-only deramp fallback when raw/dem/ has no .tif
files, and enriching the `mixed` provenance notes in meta.json, summary.json, and
decomp.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
ANALYSIS_DIR = ROOT / "analysis"
DECOMP_DIR = ANALYSIS_DIR / "decomp"
DATA_DIR = ROOT / "data" / "central_valley_fullyear"
STACK_PATH = ANALYSIS_DIR / "out" / "central_valley_fullyear_cum_stack.npz"

MIXED_QUALITY_NOTE = (
    "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
    "(NASA-JPL and ISRO), not by our team. This series MIXES provisional products with pre-calibration "
    "BETA products (dates before 2026-06-17); treat amplitudes before that date with extra caution."
)


def _ensure_valid_local_dem(dem_path: Path) -> None:
    """Remove an empty/all-NaN cached DEM so cumulative.py uses its plane-only fallback."""
    if not dem_path.exists():
        return
    try:
        arr = np.load(dem_path)
        if arr.size == 0 or not np.isfinite(arr).any():
            dem_path.unlink()
    except Exception:
        dem_path.unlink(missing_ok=True)


def _has_dem_tiles() -> bool:
    dem_dir = ROOT / "raw" / "dem"
    return dem_dir.exists() and any(dem_dir.glob("*.tif"))


def _pair_quality_lists() -> tuple[list[str], list[str]]:
    """Read pair provenance directly from the pair_stats.json and source .npz files."""
    stats_path = ANALYSIS_DIR / "out" / "central_valley_fullyear_pair_stats.json"
    beta_pairs, prov_pairs = [], []
    if stats_path.exists():
        pair_stats = json.loads(stats_path.read_text(encoding="utf-8"))
        for row in pair_stats.get("pairs", []):
            rel = row.get("file", "")
            npz_path = ROOT / rel
            q = "unknown"
            if npz_path.exists():
                with np.load(npz_path, allow_pickle=False) as d:
                    q = str(d["quality"])
            pair_label = f"{row['pair'][0]}_{row['pair'][1]}"
            if q == "beta-precal":
                beta_pairs.append(pair_label)
            else:
                prov_pairs.append(pair_label)
    return beta_pairs, prov_pairs


def _provenance_sentence(beta_pairs: list[str], prov_pairs: list[str]) -> str:
    beta_range = f"{beta_pairs[0].split('_')[0]} to {beta_pairs[-1].split('_')[1]}" if beta_pairs else "none"
    prov_range = f"{prov_pairs[0].split('_')[0]} to {prov_pairs[-1].split('_')[1]}" if prov_pairs else "none"
    return (
        f"Quality class provenance (quality=mixed): {len(beta_pairs)} beta-precal pairs "
        f"({beta_range}: {', '.join(beta_pairs)}) from pipeline/subset/central_valley_beta/ and "
        f"{len(prov_pairs)} provisional pairs ({prov_range}: {', '.join(prov_pairs)}) from "
        f"pipeline/subset/central_valley/."
    )


def run_cumulative(site: str = "central_valley") -> None:
    if str(ANALYSIS_DIR) not in sys.path:
        sys.path.insert(0, str(ANALYSIS_DIR))

    dem_cache = ANALYSIS_DIR / "out" / f"{site}_dem.npy"
    _ensure_valid_local_dem(dem_cache)
    if not _has_dem_tiles() and not dem_cache.exists():
        # Trigger cumulative.py's built-in `except Exception` plane-only fallback cleanly.
        sys.modules["dem"] = None  # type: ignore[assignment]

    import cumulative  # noqa: WPS433

    orig_argv = sys.argv
    try:
        sys.argv = [
            str(ANALYSIS_DIR / "cumulative.py"),
            site,
            "--mixed",
            "--data-dir",
            str(DATA_DIR),
        ]
        cumulative.main()
    finally:
        sys.argv = orig_argv
        if "dem" in sys.modules and sys.modules["dem"] is None:
            del sys.modules["dem"]

    postprocess_cumulative(site)


def postprocess_cumulative(site: str = "central_valley") -> None:
    beta_pairs, prov_pairs = _pair_quality_lists()
    prov_note = _provenance_sentence(beta_pairs, prov_pairs)

    meta_path = DATA_DIR / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["quality"] = "mixed"
    meta["quality_note"] = MIXED_QUALITY_NOTE
    if "beta-precal pairs" not in meta.get("notes", ""):
        meta["notes"] = meta.get("notes", "").rstrip() + " " + prov_note
    meta["beta_precal_pairs"] = beta_pairs
    meta["provisional_pairs"] = prov_pairs
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    summary_path = DATA_DIR / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["quality"] = "mixed"
    summary["quality_note"] = MIXED_QUALITY_NOTE
    days = None
    if len(summary.get("period", [])) == 2:
        from datetime import date
        days = (date.fromisoformat(summary["period"][1]) - date.fromisoformat(summary["period"][0])).days
    mn = summary.get("method_note", "")
    mn = mn.replace("summer season", "mixed full-year series (beta-precal winter/spring + provisional summer)")
    if "beta-precal" not in mn:
        mn = mn.rstrip() + (
            f" Chain combines {len(beta_pairs)} beta-precal pairs ({beta_pairs[0].split('_')[0]} to "
            f"{beta_pairs[-1].split('_')[1]}) and {len(prov_pairs)} provisional pairs ({prov_pairs[0].split('_')[0]} "
            f"to {prov_pairs[-1].split('_')[1]}) over {days} days."
        )
    summary["method_note"] = mn
    summary["n_beta_pairs"] = len(beta_pairs)
    summary["n_provisional_pairs"] = len(prov_pairs)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def run_decomp(site: str = "central_valley") -> None:
    if str(ANALYSIS_DIR) not in sys.path:
        sys.path.insert(0, str(ANALYSIS_DIR))
    if str(DECOMP_DIR) not in sys.path:
        sys.path.insert(0, str(DECOMP_DIR))

    import run_decomp as pc3_run_decomp  # noqa: WPS433
    import decompose  # noqa: WPS433

    doc = pc3_run_decomp.run(
        site,
        stack_path=str(STACK_PATH),
        out_dir=str(DATA_DIR),
        quality="mixed",
    )

    beta_pairs, prov_pairs = _pair_quality_lists()
    prov_note = _provenance_sentence(beta_pairs, prov_pairs)
    decomp_path = DATA_DIR / "decomp.json"
    doc = json.loads(decomp_path.read_text(encoding="utf-8"))
    doc["quality"] = "mixed"
    doc["quality_note"] = MIXED_QUALITY_NOTE
    if "beta-precal pairs" not in doc.get("notes", ""):
        doc["notes"] = doc.get("notes", "").rstrip() + " " + prov_note
    doc["beta_precal_pairs"] = beta_pairs
    doc["provisional_pairs"] = prov_pairs

    points_path = DATA_DIR / "points.json"
    if points_path.exists():
        pts = json.loads(points_path.read_text(encoding="utf-8"))
        point_decomp = []
        for p in pts:
            t_pts = np.array([decompose.decimal_year(d) for d in p["dates"]], dtype=np.float64)
            y_pts = np.array([np.nan if v is None else float(v) for v in p["disp_cm"]], dtype=np.float64)
            res = decompose.fit(t_pts, y_pts[:, None])
            v = float(res["v_cm_per_yr"][0])
            amp = float(res["amp_cm"][0])
            lm = None if not np.isfinite(res["low_month"][0]) else int(res["low_month"][0])
            r2 = None if not np.isfinite(res["r2"][0]) else round(float(res["r2"][0]), 3)
            v_se = None if not np.isfinite(res["v_se"][0]) else round(float(res["v_se"][0]), 2)
            amp_se = None if not np.isfinite(res["amp_se"][0]) else round(float(res["amp_se"][0]), 2)
            point_decomp.append({
                "id": p["id"],
                "name": p["name"],
                "kind": p["kind"],
                "lon": p["lon"],
                "lat": p["lat"],
                "end_disp_cm": p["disp_cm"][-1],
                "permanent_cm_per_yr": None if not np.isfinite(v) else round(v, 2),
                "permanent_se_cm_per_yr": v_se,
                "seasonal_amp_cm": None if not np.isfinite(amp) else round(amp, 2),
                "seasonal_amp_se_cm": amp_se,
                "seasonal_peak_to_peak_cm": None if not np.isfinite(amp) else round(2.0 * amp, 2),
                "low_month": lm,
                "r2": r2,
            })
        doc["point_decompositions"] = point_decomp

    decomp_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", choices=["cumulative", "decomp", "all"], default="all")
    ap.add_argument("--site", default="central_valley")
    args = ap.parse_args()
    if args.step in ("cumulative", "all"):
        run_cumulative(args.site)
    if args.step in ("decomp", "all"):
        run_decomp(args.site)


if __name__ == "__main__":
    main()
