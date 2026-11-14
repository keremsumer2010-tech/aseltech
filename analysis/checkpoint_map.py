"""Single-pair checkpoint map: GUNW subset npz -> referenced LOS cm PNG.

Usage: python analysis/checkpoint_map.py analysis/out/karapinar_20260918_20260930.npz docs/karapinar_checkpoint_cm.png
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent))
from insar import choose_reference, mask_coherence, mask_components, phase_to_cm, reference  # noqa: E402

THR, RADIUS = 0.3, 3


def run(src, dst):
    d = np.load(src)
    unw, coh, cc = d["unw"], d["coh"], d["conncomp"]
    lam = float(d["wavelength"])
    cm = mask_coherence(mask_components(phase_to_cm(unw, lam), cc), coh, THR)
    r, c, mcoh = choose_reference(coh, np.isfinite(cm), RADIUS, stride=3)
    cm = reference(cm, (r, c), RADIUS)
    x, y = d["x"], d["y"]
    lon, lat = Transformer.from_crs(int(d["epsg"]), 4326, always_xy=True).transform(x[c], y[r])
    v = np.nanpercentile(np.abs(cm), 98)
    v = float(np.ceil(v * 2) / 2)
    ext = [x[0] / 1e3, x[-1] / 1e3, y[-1] / 1e3, y[0] / 1e3]
    fig, ax = plt.subplots(figsize=(8, 6.4), dpi=130)
    im = ax.imshow(cm, cmap="RdBu", vmin=-v, vmax=v, extent=ext, interpolation="nearest")
    ax.plot(x[c] / 1e3, y[r] / 1e3, "k^", ms=8, label=f"reference ({lon:.3f}E, {lat:.3f}N)")
    ax.set_xlabel(f"Easting (km, EPSG:{int(d['epsg'])})")
    ax.set_ylabel("Northing (km)")
    ax.legend(loc="lower right", fontsize=8)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.set_label("LOS displacement (cm)  — negative = away from satellite (subsidence)")
    ax.set_title(f"Karapinar · NISAR GUNW path 7 · {d['date1']} → {d['date2']} · PROVISIONAL\n"
                 f"LOS cm, coherence ≥ {THR}, referenced; ionosphere/troposphere not applied", fontsize=10)
    fig.text(0.01, 0.005, "NISAR data are provisional. Calibration and validation are carried out by the NISAR "
             "project (NASA-JPL and ISRO), not by our team.", fontsize=6.5)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dst)
    st = {
        "pair": [str(d["date1"]), str(d["date2"])], "granule": str(d["granule"]),
        "wavelength_m": lam, "valid_fraction": float(np.isfinite(cm).mean()),
        "p2_p50_p98_cm": [float(q) for q in np.nanpercentile(cm, [2, 50, 98])],
        "min_cm": float(np.nanmin(cm)), "max_cm": float(np.nanmax(cm)),
        "reference": {"row": r, "col": c, "lon": lon, "lat": lat, "mean_coh": mcoh},
        "color_limit_cm": v,
    }
    print(json.dumps(st, indent=1))
    return st


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
