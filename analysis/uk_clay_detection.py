"""Q09 · London clay: is there a subsidence signal above the noise? (run after `cumulative.py uk_clay`)

Test (all on ~1 km block medians of the cumulative LOS map, analysis/cumulative.block_median):
  1. noise: per-pair block-median std of the pair increments; chain sigma = sqrt(sum sigma_k^2)
     (independent-pair assumption, as in docs/story/uncertainty.md).
  2. remove a quadratic surface from the final map as well (residual long-wavelength atmosphere: the raw
     extremes sit at the scene edges and appear as steps in the pairs whose whole-scene median also shifts).
  3. detection threshold = 3 * chain sigma. A block counts as a detection only if it is below -threshold
     after step 2 AND at least 10 km from the scene edge.
Writes data/uk_clay/detection.json and adds `detection_status` to data/uk_clay/summary.json.
Usage: python analysis/uk_clay_detection.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent))
from cumulative import block_median  # noqa: E402
from insar import deramp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = "uk_clay"
EDGE_KM = 10.0


def main():
    d = np.load(ROOT / "analysis" / "out" / f"{SITE}_cum.npz")
    st = np.load(ROOT / "analysis" / "out" / f"{SITE}_cum_stack.npz")["cum_stack_cm"].astype(np.float32)
    x, y, epsg = d["x"], d["y"], int(d["epsg"])
    inc = np.diff(st, axis=0)
    sig_k = [float(np.nanstd(block_median(i, 13, 0.5, None))) for i in inc]
    sigma = float(np.sqrt(np.sum(np.square(sig_k))))
    thr = 3 * sigma

    def blocks(a):
        b = block_median(a, 13, 0.5, 2.0)
        return b

    raw = blocks(d["cum_cm"])
    quad = blocks(deramp(d["cum_cm"], 2, 1))
    H, W = quad.shape
    rr, cc = np.mgrid[0:H, 0:W]
    edge_km = np.minimum.reduce([rr, cc, H - 1 - rr, W - 1 - cc]) * abs(x[1] - x[0]) / 1000
    det = np.isfinite(quad) & (quad < -thr) & (edge_km >= EDGE_KM)
    tr = Transformer.from_crs(epsg, 4326, always_xy=True)

    def extreme(b):
        r, c = np.unravel_index(np.nanargmin(b), b.shape)
        lon, lat = tr.transform(x[c], y[r])
        return {"cm": round(float(b[r, c]), 2), "lon": round(lon, 4), "lat": round(lat, 4),
                "km_from_edge": round(float(edge_km[r, c]), 1)}

    v = quad[np.isfinite(quad)]
    status = "detected" if det.any() else "below_detection"
    out = {
        "site": SITE, "status": status,
        "chain_sigma_cm": round(sigma, 2), "per_pair_block_std_cm": [round(s, 2) for s in sig_k],
        "detection_threshold_cm": round(thr, 2),
        "extreme_plane_elevation_corrected": extreme(raw),
        "extreme_after_quadratic": extreme(quad),
        "after_quadratic_block_p2_p50_p98_cm": [round(float(q), 2) for q in np.percentile(v, [2, 50, 98])],
        "fraction_blocks_within_1p5cm": round(float((np.abs(v) <= 1.5).mean()), 3),
        "n_detected_blocks": int(det.sum()),
        "statement": (
            "No ground motion above the noise was detected over London in this one-season provisional NISAR chain "
            f"(21 Jun - 19 Oct 2026, 9 pairs): after removing residual long-wavelength atmosphere, "
            f"{(np.abs(v) <= 1.5).mean() * 100:.0f} % of 1 km areas lie within +/-1.5 cm and no area away from the "
            f"scene edge exceeds the 3-sigma threshold of {thr:.1f} cm. Seasonal clay shrinkage of about a centimetre "
            "or less would be below what this chain can resolve."
            if status == "below_detection" else
            f"{int(det.sum())} 1 km areas exceed the 3-sigma threshold of {thr:.1f} cm away from the scene edge."),
        "quality": "provisional",
        "quality_note": ("NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
                         "(NASA-JPL and ISRO), not by our team."),
        "notes": ("Study box (-0.5, 51.3, 0.2, 51.7) as defined by PC2 in pipeline/search.py; track 101 ascending "
                  "frame 28. Maps in data/uk_clay/disp/ are real data but should be labelled 'below detection'."),
    }
    (ROOT / "data" / SITE / "detection.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    sp = ROOT / "data" / SITE / "summary.json"
    s = json.loads(sp.read_text(encoding="utf-8"))
    s["detection_status"] = status
    s["detection_threshold_cm"] = round(thr, 2)
    s["detection_note"] = out["statement"]
    sp.write_text(json.dumps(s, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
