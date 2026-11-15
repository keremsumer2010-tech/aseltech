"""Reprocess an already-clipped city's provisional NPZ chain without network access."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import types
from datetime import date
from pathlib import Path

import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.pc7.run_atlas_city import choose_reference_window, _write_quality_metrics, core_bbox


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--name", required=True)
    ap.add_argument("--center", required=True, help="lon,lat")
    ap.add_argument("--reference", required=True, help="candidate anchor lon,lat")
    ap.add_argument("--reference-source", required=True)
    ap.add_argument("--reference-outside-basin", choices=("yes", "no"), required=True)
    ap.add_argument("--search-radius-m", type=float, default=3000)
    args = ap.parse_args()
    name = args.name
    center = tuple(float(x) for x in args.center.split(","))
    anchor = tuple(float(x) for x in args.reference.split(","))
    bbox = core_bbox(center)
    src = ROOT / "pipeline" / "subset" / f"global_{name}"
    files = sorted(src.glob("*.npz"))
    if not files:
        raise SystemExit(f"no local subset files for {name}")
    ref_row, ref_col, ref_coh, x, y, epsg = choose_reference_window(
        files, anchor, search_radius_m=args.search_radius_m)
    tx = Transformer.from_crs(epsg, 4326, always_xy=True)
    ref_lon, ref_lat = tx.transform(float(x[ref_col]), float(y[ref_row]))
    with np.load(files[0], allow_pickle=False) as d:
        xx, yy = np.meshgrid([d["x"].min(), d["x"].max()], [d["y"].min(), d["y"].max()])
        lons, lats = tx.transform(xx, yy)
        coverage_bbox = [float(np.min(lons)), float(np.min(lats)), float(np.max(lons)), float(np.max(lats))]
        q = str(d["quality"].item())
    if q != "provisional":
        raise SystemExit(f"non-provisional local chain: {q}")
    with tempfile.TemporaryDirectory(prefix=f"pc7_{name}_offline_") as t:
        work = Path(t)
        dest = work / "pipeline" / "subset" / name
        dest.mkdir(parents=True)
        for f in files:
            shutil.copy2(f, dest / f.name)
        (work / "analysis" / "out").mkdir(parents=True)
        fd, copied = tempfile.mkstemp(prefix=f"pc7_{name}_", suffix=".npz")
        os.close(fd)
        cum_copy = Path(copied)
        sys.path.insert(0, str(ROOT / "analysis"))
        import cumulative  # type: ignore[import-not-found]
        import gunw_io  # type: ignore[import-not-found]
        old_root, old_ref, old_bbox, old_argv = cumulative.ROOT, cumulative.choose_reference, gunw_io.BBOX.get(name), list(sys.argv)
        old_dem = sys.modules.get("dem")
        first = True
        def select_reference(coherence, valid=None, radius=3, stride=5, exclude=None):
            nonlocal first
            if first:
                first = False
                return ref_row, ref_col, ref_coh
            return old_ref(coherence, valid, radius, stride, exclude)
        try:
            dummy_dem = types.ModuleType("dem")
            def no_download(*_args, **_kwargs):
                raise RuntimeError("offline replay: DEM lookup/download disabled")
            dummy_dem.dem_on_grid = no_download
            sys.modules["dem"] = dummy_dem
            cumulative.ROOT = work
            cumulative.choose_reference = select_reference
            gunw_io.BBOX[name] = bbox
            sys.argv = ["cumulative.py", name, "--data-dir", str(ROOT / "data" / "global" / name), "--no-names", "--deramp", "1"]
            cumulative.main()
            shutil.copy2(work / "analysis" / "out" / f"{name}_cum.npz", cum_copy)
        finally:
            cumulative.ROOT = old_root
            cumulative.choose_reference = old_ref
            if old_bbox is None:
                gunw_io.BBOX.pop(name, None)
            else:
                gunw_io.BBOX[name] = old_bbox
            sys.argv = old_argv
            if old_dem is None:
                sys.modules.pop("dem", None)
            else:
                sys.modules["dem"] = old_dem

    data = ROOT / "data" / "global" / name
    period_days = (date(2026, 10, 15) - date(2026, 6, 17)).days
    summary = _write_quality_metrics(data, cum_copy, bbox, args.reference_source, anchor,
                                     (float(ref_lon), float(ref_lat)), ref_coh,
                                     args.reference_outside_basin == "yes")
    summary["confidence"] = "low"
    summary["confidence_note"] = "Indicative only: reference geology/out-of-basin status and independent validation are not established by this local replay."
    summary["local_subset_coverage_bbox"] = coverage_bbox
    (data / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8")
    meta_path = data / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update({"bbox": list(bbox), "quality": "provisional", "reference_outside_basin": args.reference_outside_basin == "yes",
                 "confidence": "low", "confidence_note": summary["confidence_note"],
                 "local_subset_coverage_bbox": coverage_bbox})
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8")
    dates = sorted({str(np.load(f, allow_pickle=False)["date2"].item()) for f in files} |
                   {str(np.load(f, allow_pickle=False)["date1"].item()) for f in files})
    coverage = {"site": name, "bbox": list(bbox), "subset_bbox": coverage_bbox, "quality": "provisional",
                "coverage": "ok" if all(coverage_bbox[i] <= bbox[i] for i in (0,1)) and coverage_bbox[2] >= bbox[2] and coverage_bbox[3] >= bbox[3] else "partial",
                "granules": len(files), "chain_pairs": len(files), "period": [dates[0], dates[-1]], "gaps": [],
                "raw_files_deleted_after_subsetting": True, "network_used": False}
    (data / "coverage.json").write_text(json.dumps(coverage, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8")
    cum_copy.unlink(missing_ok=True)
    print(json.dumps({"city": name, "bbox": bbox, "local_subset_coverage_bbox": coverage_bbox,
                      "reference_point": [ref_lon, ref_lat], "reference_mean_coherence": ref_coh,
                      "summary": summary, "coverage": coverage}, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
