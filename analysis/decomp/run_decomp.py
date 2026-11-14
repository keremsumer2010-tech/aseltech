"""Run the permanent / seasonal decomposition on a cumulative stack and write web outputs.

Usage:
  python analysis/decomp/run_decomp.py central_valley                       # reads analysis/out/central_valley_cum_stack.npz
  python analysis/decomp/run_decomp.py central_valley --stack <npz> --out data/central_valley_fullyear --quality mixed

Writes (rules/VERI_SOZLESMESI.md 4.2, decomp.json):
  <out>/decomp.json            permanent_cm_per_yr / seasonal_amp_cm statistics + PNG paths + coverage + reasons
  <out>/decomp_permanent.png   v (cm/yr), RdBu, transparent NaN, fitted to the site bbox (lat/lon grid)
  <out>/decomp_seasonal.png    amplitude (cm), magma, transparent NaN
When too few valid pixels exist (e.g. one summer only: span < 9 months), decomp.json is still written with
"status": "insufficient_data" and the reason counts; PNGs are skipped. Nothing else is touched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from decompose import MIN_POINTS, MIN_SPAN_YR, REASON, decimal_year, fit  # noqa: E402

DISCLAIMER = ("NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
              "(NASA-JPL and ISRO), not by our team.")


def run(site, stack_path=None, out_dir=None, quality=None):
    from cumulative import save_png, to_latlon_grid  # analysis/cumulative.py (PC3)
    from gunw_io import BBOX

    stack_path = Path(stack_path or ROOT / "analysis" / "out" / f"{site}_cum_stack.npz")
    out_dir = Path(out_dir or ROOT / "data" / f"{site}_fullyear")
    d = np.load(stack_path)
    dates = [str(x) for x in d["dates"]]
    q = quality or str(d["quality"])
    t = np.array([decimal_year(x) for x in dates])
    res = fit(t, d["cum_stack_cm"].astype(np.float32))
    ok = res["reason"] == 0
    reasons = {REASON[int(k)]: int((res["reason"] == k).sum()) for k in np.unique(res["reason"])}
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = {
        "site": site, "dates": dates, "quality": q, "quality_note": DISCLAIMER,
        "model": "d(t) = a + v*(t - t0) + A*sin(2*pi*t) + B*cos(2*pi*t); t in decimal years (analysis/decomp/decompose.py)",
        "min_points": MIN_POINTS, "min_span_years": MIN_SPAN_YR,
        "valid_fraction": round(float(ok.mean()), 4), "reason_counts": reasons,
        "notes": ("Standard errors assume independent epochs; cumulative InSAR epochs are correlated, so they are "
                  "optimistic. Values are line of sight."),
    }
    if ok.sum() < 100:
        doc["status"] = "insufficient_data"
        doc["permanent_cm_per_yr"] = None
        doc["seasonal_amp_cm"] = None
    else:
        v, amp = res["v_cm_per_yr"], res["amp_cm"]

        def stats(a):
            a = a[ok]
            return {k: round(float(x), 2) for k, x in zip(("p2", "p50", "p98"), np.percentile(a, [2, 50, 98]))}

        vlim = float(np.ceil(np.percentile(np.abs(v[ok]), 99)))
        alim = float(np.ceil(np.percentile(amp[ok], 99)))
        x, y, epsg, bbox = d["x"], d["y"], int(d["epsg"]), BBOX[site]
        save_png(to_latlon_grid(np.where(ok, v, np.nan), x, y, epsg, bbox), out_dir / "decomp_permanent.png", -vlim, vlim)
        import matplotlib.pyplot as plt
        cm = plt.get_cmap("magma").with_extremes(bad=(0, 0, 0, 0))
        plt.imsave(out_dir / "decomp_seasonal.png",
                   np.ma.masked_invalid(to_latlon_grid(np.where(ok, amp, np.nan), x, y, epsg, bbox)),
                   cmap=cm, vmin=0, vmax=alim)
        doc.update({
            "status": "ok", "bbox": list(bbox),
            "permanent_cm_per_yr": {"png": "decomp_permanent.png", "vmin": -vlim, "vmax": vlim, **stats(v)},
            "seasonal_amp_cm": {"png": "decomp_seasonal.png", "vmin": 0.0, "vmax": alim, **stats(amp)},
            "low_month_mode": int(np.bincount(res["low_month"][ok].astype(int)).argmax()),
        })
    (out_dir / "decomp.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(json.dumps({k: doc[k] for k in ("status", "valid_fraction", "reason_counts")}))
    return doc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--stack")
    ap.add_argument("--out")
    ap.add_argument("--quality", help="override quality label (full-year runs with beta pairs: mixed)")
    a = ap.parse_args()
    run(a.site, a.stack, a.out, a.quality)
