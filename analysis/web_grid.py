"""Light numeric grid for the website explorer: data/<site>/grid.json.

From analysis/out/<site>_cum_stack.npz (cumulative LOS cm per date, UTM grid) build a regular lon/lat grid of
~2 km cells (0.02 deg) over the site bbox. Each cell = median of the 80 m pixels inside it, kept only if >= 50 %
of them are valid in that date; otherwise null. This lets the page show "value at this date" and a time series
for any clicked spot without shipping the full 80 m grids. Values in cm, 1 decimal, line of sight.
Usage: python analysis/web_grid.py central_valley [step_deg]
"""
import json
import sys
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from cumulative import to_latlon_grid  # noqa: E402
from gunw_io import BBOX  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FINE = 0.001  # deg, same grid as the web PNGs


def main(site, step=0.02):
    st = np.load(ROOT / "analysis" / "out" / f"{site}_cum_stack.npz")
    meta = json.loads((ROOT / "data" / site / "meta.json").read_text(encoding="utf-8"))
    bbox = BBOX[site]
    k = int(round(step / FINE))
    cube = st["cum_stack_cm"].astype(np.float32)
    dates = [str(d) for d in st["dates"]]
    if dates != meta["dates"]:
        raise SystemExit("stack dates differ from data/<site>/meta.json; regenerate the cumulative first")
    vals = []
    for t in range(len(dates)):
        g = to_latlon_grid(cube[t], st["x"], st["y"], int(st["epsg"]), bbox, FINE)  # north-up
        H, W = (g.shape[0] // k) * k, (g.shape[1] // k) * k
        b = g[:H, :W].reshape(H // k, k, W // k, k)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            m = np.nanmedian(b, axis=(1, 3))
        m[np.isfinite(b).mean(axis=(1, 3)) < 0.5] = np.nan
        vals.append(m)
    nrow, ncol = vals[0].shape
    out = {
        "site": site, "bbox": list(bbox), "step_deg": step, "nrows": nrow, "ncols": ncol,
        "origin": "north-west corner; row 0 = north", "dates": dates, "units": "cm (line of sight, negative = sinking)",
        "values": [[None if not np.isfinite(v) else round(float(v), 1) for v in m.ravel()] for m in vals],
        "quality": meta.get("quality"), "quality_note": meta.get("quality_note"),
        "method": f"median of 80 m pixels in {step} deg cells, cell kept if >= 50 % valid (analysis/web_grid.py)",
    }
    dst = ROOT / "data" / site / "grid.json"
    dst.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(dst, nrow, ncol, len(dates), f"{dst.stat().st_size / 1e3:.0f} kB",
          "valid cells last date", int(np.isfinite(vals[-1]).sum()))


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.02)
