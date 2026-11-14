"""Q22 · Vertical + east-west motion from two NISAR geometries (track 34 ascending, track 114 descending).

Each track measures the projection of the 3-D ground motion D = (E, N, U) on its line of sight:
    d_k = E*e_k + N*n_k + U*u_k        (e, n, u = LOS unit vector from ground to sensor, GUNW metadata cube)
With two tracks we solve for E and U per pixel and neglect N: for near-polar orbits the north component of the
LOS vector is small, so north motion is poorly constrained by any SAR pair (standard 2-geometry approach, e.g.
Wright, Parsons & Lu 2004, GRL 31, L01607, https://doi.org/10.1029/2003GL018827).
Sign: our LOS convention is negative = away from the satellite (analysis/insar.py), consistent with D·los_unit.
Inputs: analysis/out/central_valley{,_p114}_cum_stack.npz (track 114 interpolated to track 34 dates as in
compare_tracks.py) + analysis/out/central_valley{,_p114}_geometry.npz.
Outputs: data/central_valley/vertical.json, data/central_valley/vertical_up.png, vertical_east.png.
Usage: python analysis/vertical_ew.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import compare_tracks as ct  # noqa: E402
from cumulative import block_median, save_png, to_latlon_grid  # noqa: E402
from gunw_io import BBOX  # noqa: E402
from pyproj import Transformer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis" / "out"
DISCLAIMER = ("NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
              "(NASA-JPL and ISRO), not by our team.")


def solve_eu(d1, d2, e1, u1, e2, u2):
    """Per-pixel 2x2 solve of [e1 u1; e2 u2] [E; U] = [d1; d2]. Returns E, U (NaN where ill-conditioned)."""
    det = e1 * u2 - e2 * u1
    bad = np.abs(det) < 0.05
    with np.errstate(divide="ignore", invalid="ignore"):
        E = (d1 * u2 - d2 * u1) / det
        U = (e1 * d2 - e2 * d1) / det
    E[bad] = np.nan
    U[bad] = np.nan
    return E.astype(np.float32), U.astype(np.float32)


def main():
    site = "central_valley"
    A = np.load(OUT / f"{site}_cum_stack.npz")
    B = np.load(OUT / f"{site}_p114_cum_stack.npz")
    gA = np.load(OUT / f"{site}_geometry.npz")
    gB = np.load(OUT / f"{site}_p114_geometry.npz")
    x, y, epsg = A["x"], A["y"], int(A["epsg"])
    ta, tb = ct.days(A["dates"]), ct.days(B["dates"])
    keep = (ta >= tb[0]) & (ta <= tb[-1])
    dates = [str(d) for d in np.array(A["dates"])[keep]]
    sa = A["cum_stack_cm"].astype(np.float32)[keep]
    sa = sa - sa[0]
    sb = ct.interp_stack(B["cum_stack_cm"].astype(np.float32), tb, ta[keep])
    sb = ct.resample_to(sb - sb[0], B["x"], B["y"], x, y)
    eA = ct.resample_to(gA["los_e"], gA["x"], gA["y"], x, y)
    uA = ct.resample_to(gA["los_u"], gA["x"], gA["y"], x, y)
    eB = ct.resample_to(gB["los_e"], gB["x"], gB["y"], x, y)
    uB = ct.resample_to(gB["los_u"], gB["x"], gB["y"], x, y)
    E, U = solve_eu(sa[-1], sb[-1], eA, uA, eB, uB)

    XX, YY = np.meshgrid(x, y)
    LON, LAT = Transformer.from_crs(epsg, 4326, always_xy=True).transform(XX, YY)
    bbox = BBOX[site]
    inb = (LON >= bbox[0]) & (LON <= bbox[2]) & (LAT >= bbox[1]) & (LAT <= bbox[3])
    U_b = block_median(np.where(inb, U, np.nan), 13, 0.5, 3.0)
    E_b = block_median(np.where(inb, E, np.nan), 13, 0.5, 3.0)
    r, c = np.unravel_index(np.nanargmin(U_b), U_b.shape)
    lon_m, lat_m = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c], y[r])
    okb = np.isfinite(U_b)
    # robust broad bowl (smooth, well-covered) reported next to the single most negative block
    named = []
    for nm, lo, la in (("Alpaugh / Earlimart west bowl", -119.45, 35.88),):
        X0, Y0 = Transformer.from_crs(4326, epsg, always_xy=True).transform(lo, la)
        rr, cc = int(np.argmin(np.abs(y - Y0))), int(np.argmin(np.abs(x - X0)))
        win = U_b[max(rr - 40, 0): rr + 41, max(cc - 40, 0): cc + 41]
        k = np.unravel_index(np.nanargmin(win), win.shape)
        r0, c0 = max(rr - 40, 0) + k[0], max(cc - 40, 0) + k[1]
        lon0, lat0 = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c0], y[r0])
        named.append({"name": nm, "lon": round(lon0, 4), "lat": round(lat0, 4), "up_cm": round(float(U_b[r0, c0]), 1),
                      "east_cm": round(float(E_b[r0, c0]), 1)})
    vlim = float(np.ceil(np.nanpercentile(np.abs(U_b[okb]), 99.5)))
    elim = float(np.ceil(np.nanpercentile(np.abs(E_b[np.isfinite(E_b)]), 99.5)))
    ddir = ROOT / "data" / site
    save_png(to_latlon_grid(U, x, y, epsg, bbox), ddir / "vertical_up.png", -vlim, vlim)
    save_png(to_latlon_grid(E, x, y, epsg, bbox), ddir / "vertical_east.png", -elim, elim)

    def pct(a):
        a = a[np.isfinite(a)]
        return {k: round(float(v), 2) for k, v in zip(("p2", "p50", "p98"), np.percentile(a, [2, 50, 98]))}

    doc = {
        "site": site, "period": [dates[0], dates[-1]], "units": "cm", "bbox": list(bbox),
        "method": ("Two-geometry inversion per pixel: track 34 ascending + track 114 descending cumulative LOS "
                   "(track 114 interpolated in time to track 34 dates, both re-zeroed at the first common date); "
                   "d_k = E*e_k + U*u_k with LOS unit vectors from the GUNW metadata cube; north motion neglected."),
        "up_cm": {"png": "vertical_up.png", "vmin": -vlim, "vmax": vlim, **pct(U_b)},
        "east_cm": {"png": "vertical_east.png", "vmin": -elim, "vmax": elim, **pct(E_b)},
        "max_subsidence_up_cm": round(float(U_b[r, c]), 1),
        "max_subsidence_location": {"lon": round(lon_m, 5), "lat": round(lat_m, 5)},
        "east_at_max_cm": round(float(E_b[r, c]), 1),
        "los_unit_vectors_median": {
            "track34_asc": {"e": round(float(np.nanmedian(eA)), 3), "u": round(float(np.nanmedian(uA)), 3)},
            "track114_desc": {"e": round(float(np.nanmedian(eB)), 3), "u": round(float(np.nanmedian(uB)), 3)},
        },
        "valid_fraction": round(float(np.isfinite(U).mean()), 3),
        "colormap": "RdBu for both: up map red = sinking, blue = rising; east map red = moving west, blue = moving east",
        "named_bowls": named,
        "quality": "provisional", "quality_note": DISCLAIMER,
        "notes": ("~1 km block medians (>= 50 % valid, within-block std <= 3 cm) for statistics. The single most negative block lies in the speckled south-east foothill/orchard edge (lower confidence); the Alpaugh bowl is the clearest broad feature. Each track carries "
                  "~2-3 cm of atmospheric noise per pair; east-west values are noisier than up because the two "
                  "LOS vectors differ mainly in their east component."),
    }
    (ddir / "vertical.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(json.dumps(doc, indent=1))
    return doc


if __name__ == "__main__":
    main()
