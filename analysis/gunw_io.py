"""Read a NISAR L2 GUNW .h5 and cut a lon/lat bbox into the npz layout of the data contract
(rules/VERI_SOZLESMESI.md 4.1): unw (rad), coh (uint8 0-255), x, y, epsg, wavelength, incidence, quality.
Extra fields we keep: conncomp (uint16), ion (rad, NOT applied), date1, date2, granule.

HDF5 paths: docs/qa/PC1.md and the GUNW product spec (JPL D-102272 Rev E).
Usage: python analysis/gunw_io.py <file.h5> <site> <out.npz>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import h5py
import numpy as np
from pyproj import Transformer
from scipy.interpolate import RegularGridInterpolator

from insar import wavelength_from_frequency

BBOX = {  # [w, s, e, n]  rules/VERI_SOZLESMESI.md section 1
    "central_valley": (-120.2, 35.6, -119.0, 36.6),
    "konya": (32.4, 37.4, 33.9, 38.1),
    "karapinar": (33.3, 37.6, 33.8, 37.9),
    # second geometry over the same box (Q21: track 114 descending vs track 34 ascending); outputs kept separate
    "central_valley_p114": (-120.2, 35.6, -119.0, 36.6),
}
G = "science/LSAR/GUNW"
PROVISIONAL_START = "2026-06-17"


def dates_from_name(name: str):
    ts = re.findall(r"_(\d{8})T\d{6}", name)
    d = sorted(set(ts))
    if len(d) < 2:
        raise ValueError(f"cannot parse dates from {name}")
    iso = [f"{s[:4]}-{s[4:6]}-{s[6:]}" for s in d]
    return iso[0], iso[-1]


def quality_for(d1: str, d2: str, crid: str) -> str:
    if crid == "P05023" and d1 >= PROVISIONAL_START and d2 >= PROVISIONAL_START:
        return "provisional"
    return "beta-precal"


def _crop_slices(xs, ys, epsg, bbox, pad_m=2000.0):
    tr = Transformer.from_crs(4326, epsg, always_xy=True)
    w, s, e, n = bbox
    lon = np.array([w, e, e, w, (w + e) / 2, (w + e) / 2])
    lat = np.array([s, s, n, n, s, n])
    X, Y = tr.transform(lon, lat)
    x0, x1, y0, y1 = X.min() - pad_m, X.max() + pad_m, Y.min() - pad_m, Y.max() + pad_m
    ix = np.where((xs >= x0) & (xs <= x1))[0]
    iy = np.where((ys >= y0) & (ys <= y1))[0]
    if ix.size == 0 or iy.size == 0:
        raise ValueError("bbox does not intersect this GUNW")
    return slice(iy[0], iy[-1] + 1), slice(ix[0], ix[-1] + 1)


def _incidence(f, x, y, ref_height_m=None):
    """Interpolate the incidence cube (heights, y, x) onto the subset grid at one height."""
    rg = f[f"{G}/metadata/radarGrid"]
    cube = rg["incidenceAngle"][()]
    cx, cy = rg["xCoordinates"][()], rg["yCoordinates"][()]
    hts = rg["heightAboveEllipsoid"][()] if "heightAboveEllipsoid" in rg else np.arange(cube.shape[0])
    k = int(np.argmin(np.abs(hts - ref_height_m))) if ref_height_m is not None else cube.shape[0] // 2
    lay = cube[k]
    if cy[0] > cy[-1]:
        cy, lay = cy[::-1], lay[::-1]
    if cx[0] > cx[-1]:
        cx, lay = cx[::-1], lay[:, ::-1]
    itp = RegularGridInterpolator((cy, cx), lay, bounds_error=False, fill_value=np.nan)
    YY, XX = np.meshgrid(y, x, indexing="ij")
    return itp((YY, XX)).astype(np.float32), float(hts[k])


def subset(h5path, site, pol="HH", ref_height_m=None):
    h5path = Path(h5path)
    with h5py.File(h5path, "r") as f:
        ident = f["science/LSAR/identification"]
        t_ref = ident["referenceZeroDopplerStartTime"][()].decode()[:10]
        t_sec = ident["secondaryZeroDopplerStartTime"][()].decode()[:10]
        if not t_ref < t_sec:  # our sign test assumes reference = earlier date
            raise ValueError(f"reference {t_ref} is not earlier than secondary {t_sec}")
        granule = h5path.stem
        try:
            gname = ident["granuleId"][()].decode() if "granuleId" in ident else granule
        except Exception:
            gname = granule
        crid = ident["compositeReleaseId"][()].decode() if "compositeReleaseId" in ident else ""
        fa = f[f"{G}/grids/frequencyA"]
        unw_g = fa[f"unwrappedInterferogram/{pol}"]
        xs, ys = unw_g["xCoordinates"][()], unw_g["yCoordinates"][()]
        epsg = int(unw_g["projection"].attrs.get("epsg_code", unw_g["projection"][()]))
        sy, sx = _crop_slices(xs, ys, epsg, BBOX[site])
        out = dict(
            unw=unw_g["unwrappedPhase"][sy, sx].astype(np.float32),
            coh=np.clip(np.nan_to_num(unw_g["coherenceMagnitude"][sy, sx], nan=0.0) * 255.0 + 0.5, 0, 255).astype(np.uint8),
            conncomp=unw_g["connectedComponents"][sy, sx].astype(np.uint16),
            ion=unw_g["ionospherePhaseScreen"][sy, sx].astype(np.float32) if "ionospherePhaseScreen" in unw_g else np.array([]),
            x=xs[sx].astype(np.float64), y=ys[sy].astype(np.float64), epsg=np.int32(epsg),
            wavelength=np.float64(wavelength_from_frequency(fa["centerFrequency"][()])),
        )
        out["incidence"], h_used = _incidence(f, out["x"], out["y"], ref_height_m)
    d1, d2 = dates_from_name(gname if "_P0" in gname else granule)
    out.update(date1=d1, date2=d2, granule=gname, crid=crid, quality=quality_for(d1, d2, crid),
               incidence_height_m=np.float64(h_used))
    return out


if __name__ == "__main__":
    h5, site, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    o = subset(h5, site)
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(dst, **o)
    print(dst, o["unw"].shape, o["epsg"], o["wavelength"], o["date1"], o["date2"], o["quality"],
          f"{Path(dst).stat().st_size/1e6:.1f} MB")
