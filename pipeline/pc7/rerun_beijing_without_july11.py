"""Rebuild Beijing from local subsets while bridging across 2026-07-11.

No network access is used. The two adjacent pair displacement grids around the
flagged acquisition are merged by the repository QC hook before accumulation.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import types
from pathlib import Path

import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.pc7.run_atlas_city import choose_reference_window, _write_quality_metrics

CITY = "beijing"
BBOX = (116.35, 39.70, 116.85, 40.20)
ANCHOR = (116.31061, 40.10068)
DROP_DATE = "2026-07-11"


def main() -> None:
    source = ROOT / "pipeline" / "subset" / "global_beijing"
    files = sorted(source.glob("*.npz"))
    if len(files) != 9:
        raise SystemExit(f"Expected 9 local Beijing pairs, found {len(files)}")
    row, col, coh, x, y, epsg = choose_reference_window(files, ANCHOR)
    lon, lat = Transformer.from_crs(epsg, 4326, always_xy=True).transform(float(x[col]), float(y[row]))
    fd, cum_copy_raw = tempfile.mkstemp(prefix="pc7_beijing_cum_", suffix=".npz")
    os.close(fd)
    cum_copy = Path(cum_copy_raw)

    with tempfile.TemporaryDirectory(prefix="pc7_beijing_bridge_") as temp:
        work = Path(temp)
        subset = work / "pipeline" / "subset" / CITY
        subset.mkdir(parents=True)
        for path in files:
            shutil.copy2(path, subset / path.name)
        (work / "analysis" / "out").mkdir(parents=True)
        sys.path.insert(0, str(ROOT / "analysis"))
        import cumulative  # type: ignore[import-not-found]
        import gunw_io  # type: ignore[import-not-found]
        import pipeline.nisarvision.qc as qc

        old_root, old_ref = cumulative.ROOT, cumulative.choose_reference
        old_bbox = gunw_io.BBOX.get(CITY)
        old_qc = qc.qc_stack
        old_argv = list(sys.argv)
        old_dem = sys.modules.get("dem")
        first_ref = True

        def choose_primary(coherence, valid=None, radius=3, stride=5, exclude=None):
            nonlocal first_ref
            if first_ref:
                first_ref = False
                return row, col, coh
            return old_ref(coherence, valid, radius, stride, exclude)

        def force_bridge(pair_cm, dates, conncomp_list=None, **kwargs):
            if DROP_DATE not in dates:
                raise ValueError(f"target date {DROP_DATE} missing from local chain")
            idx = dates.index(DROP_DATE)
            merged = np.asarray(pair_cm[idx - 1], dtype=np.float32) + np.asarray(pair_cm[idx], dtype=np.float32)
            rebuilt = list(pair_cm)
            rebuilt[idx - 1:idx + 1] = [merged]
            rebuilt_dates = list(dates)
            rebuilt_dates.pop(idx)
            rebuilt_cc = list(conncomp_list or [None] * len(pair_cm))
            if rebuilt_cc:
                a, b = rebuilt_cc[idx - 1], rebuilt_cc[idx]
                rebuilt_cc[idx - 1:idx + 1] = [a if a is not None else b]
            clean, clean_dates, report = old_qc(rebuilt, rebuilt_dates, rebuilt_cc, **kwargs)
            report["dropped_dates"].append({
                "date": DROP_DATE,
                "reason": "forced bridge per PC1 final handoff; adjacent pair grids summed",
                "merged_pair": [clean_dates[idx - 1], clean_dates[idx]],
            })
            return clean, clean_dates, report

        try:
            dummy_dem = types.ModuleType("dem")
            def no_dem_download(*_args, **_kwargs):
                raise RuntimeError("offline replay: DEM lookup/download disabled")
            dummy_dem.dem_on_grid = no_dem_download
            sys.modules["dem"] = dummy_dem
            cumulative.ROOT = work
            cumulative.choose_reference = choose_primary
            gunw_io.BBOX[CITY] = BBOX
            qc.qc_stack = force_bridge
            sys.argv = ["cumulative.py", CITY, "--data-dir", str(ROOT / "data" / "global" / CITY),
                        "--no-names", "--deramp", "1"]
            cumulative.main()
            shutil.copy2(work / "analysis" / "out" / f"{CITY}_cum.npz", cum_copy)
        finally:
            cumulative.ROOT = old_root
            cumulative.choose_reference = old_ref
            if old_bbox is None:
                gunw_io.BBOX.pop(CITY, None)
            else:
                gunw_io.BBOX[CITY] = old_bbox
            qc.qc_stack = old_qc
            sys.argv = old_argv
            if old_dem is None:
                sys.modules.pop("dem", None)
            else:
                sys.modules["dem"] = old_dem

    data = ROOT / "data" / "global" / CITY
    summary = _write_quality_metrics(data, cum_copy, BBOX,
                                     "PC1 handoff-supplied NW foothill reference; independent geology citation not verified",
                                     ANCHOR, (float(lon), float(lat)), coh, True)
    summary["n_pairs"] = 8
    summary["july_11_bridge"] = {"dropped_acquisition": DROP_DATE,
                                  "merged_pairs": ["2026-06-29_2026-07-11", "2026-07-11_2026-07-23"],
                                  "method": "sum adjacent, individually masked and deramped LOS grids; retain continuous 2026-06-29 to 2026-07-23 interval"}
    summary["confidence"] = "low"
    summary["confidence_note"] = "Indicative pending independent reference geology and PC5 review; bridge removes the flagged acquisition but does not establish a regional rate."
    (data / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")

    meta_path = data / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["dates"] = [d for d in meta["dates"] if d != DROP_DATE]
    meta["notes"] += f" Forced bridge: the 2026-06-29→2026-07-11 and 2026-07-11→2026-07-23 pair grids were individually masked/deramped, summed into one continuous 2026-06-29→2026-07-23 step, and the 2026-07-11 acquisition removed. Independent geology citation for the reference remains unverified."
    meta["quality"] = "provisional"
    meta["quality_note"] = summary["quality_note"]
    meta["confidence"] = "low"
    meta["confidence_note"] = summary["confidence_note"]
    meta_path.write_text(json.dumps(meta, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    coverage = json.loads((data / "coverage.json").read_text(encoding="utf-8")) if (data / "coverage.json").exists() else {}
    coverage.update({"site": CITY, "bbox": list(BBOX), "quality": "provisional", "coverage": "ok",
                     "chain_pairs": 8, "period": ["2026-06-17", "2026-10-15"], "gaps": [],
                     "raw_files_deleted_after_subsetting": True, "july_11_bridged": True})
    (data / "coverage.json").write_text(json.dumps(coverage, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (data / "disp" / f"{DROP_DATE}.png").unlink(missing_ok=True)
    cum_copy.unlink(missing_ok=True)
    print(json.dumps({"city": CITY, "summary": summary, "reference_point": [lon, lat],
                      "reference_mean_coherence": coh, "effective_pairs": 8}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
