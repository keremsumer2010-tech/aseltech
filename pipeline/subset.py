"""Subset NISAR L2 GUNW HDF5 products to site bounding boxes and save compressed .npz."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import h5py
import numpy as np

try:
    from pipeline.search import SITES
except ImportError:
    from search import SITES

C_LIGHT_M_S = 299792458.0
PROVISIONAL_CUTOFF = "2026-06-17"
MAX_NPZ_MB = 19.5
DATE_RE = re.compile(
    r"_(\d{8})T\d{6}_\d{8}T\d{6}_(\d{8})T\d{6}_\d{8}T\d{6}_([A-Z]\d{5})_"
)


def lonlat_to_utm(lon: float, lat: float, epsg: int) -> tuple[float, float]:
    """Convert WGS84 (lon, lat) in degrees to UTM (easting, northing) for EPSG 326xx/327xx."""
    if 32601 <= epsg <= 32660:
        zone = epsg - 32600
        south = False
    elif 32701 <= epsg <= 32760:
        zone = epsg - 32700
        south = True
    else:
        raise ValueError(f"Unsupported UTM EPSG code: {epsg}")

    a = 6378137.0
    f = 1.0 / 298.257223563
    k0 = 0.9996
    e2 = f * (2.0 - f)
    ep2 = e2 / (1.0 - e2)

    lon0 = math.radians((zone - 1) * 6 - 180 + 3)
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)
    dlon = lon_r - lon0

    sin_lat = math.sin(lat_r)
    cos_lat = math.cos(lat_r)
    tan_lat = math.tan(lat_r)

    N = a / math.sqrt(1.0 - e2 * sin_lat**2)
    T = tan_lat**2
    C = ep2 * cos_lat**2
    A = cos_lat * dlon
    M = a * (
        (1.0 - e2 / 4.0 - 3.0 * e2**2 / 64.0 - 5.0 * e2**3 / 256.0) * lat_r
        - (3.0 * e2 / 8.0 + 3.0 * e2**2 / 32.0 + 45.0 * e2**3 / 1024.0)
        * math.sin(2.0 * lat_r)
        + (15.0 * e2**2 / 256.0 + 45.0 * e2**3 / 1024.0) * math.sin(4.0 * lat_r)
        - (35.0 * e2**3 / 3072.0) * math.sin(6.0 * lat_r)
    )

    x = (
        k0
        * N
        * (
            A
            + (1.0 - T + C) * A**3 / 6.0
            + (5.0 - 18.0 * T + T**2 + 72.0 * C - 58.0 * ep2) * A**5 / 120.0
        )
        + 500000.0
    )
    y = k0 * (
        M
        + N
        * tan_lat
        * (
            A**2 / 2.0
            + (5.0 - T + 9.0 * C + 4.0 * C**2) * A**4 / 24.0
            + (61.0 - 58.0 * T + T**2 + 600.0 * C - 330.0 * ep2) * A**6 / 720.0
        )
    )
    if south:
        y += 10000000.0
    return x, y


def bbox_to_utm_bounds(
    bbox: tuple[float, float, float, float], epsg: int, pad_m: float = 2000.0
) -> tuple[float, float, float, float]:
    w, s, e, n = bbox
    corners = [
        (w, s),
        (e, s),
        (w, n),
        (e, n),
        ((w + e) / 2.0, s),
        ((w + e) / 2.0, n),
    ]
    pts = [lonlat_to_utm(lon, lat, epsg) for lon, lat in corners]
    xs, ys = zip(*pts)
    return min(xs) - pad_m, min(ys) - pad_m, max(xs) + pad_m, max(ys) + pad_m


def bilinear_interp_2d(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    grid_z: np.ndarray,
    target_x: np.ndarray,
    target_y: np.ndarray,
) -> np.ndarray:
    """Bilinear interpolation from coarse 2D grid (grid_y, grid_x) onto (target_y, target_x)."""
    gx = np.asarray(grid_x, dtype=np.float64)
    gy = np.asarray(grid_y, dtype=np.float64)
    gz = np.asarray(grid_z, dtype=np.float64)

    if gx[0] > gx[-1]:
        gx = gx[::-1]
        gz = gz[:, ::-1]
    if gy[0] > gy[-1]:
        gy = gy[::-1]
        gz = gz[::-1, :]

    tx = np.clip(np.asarray(target_x, dtype=np.float64), gx[0], gx[-1])
    ty = np.clip(np.asarray(target_y, dtype=np.float64), gy[0], gy[-1])

    ix = np.clip(np.searchsorted(gx, tx, side="right") - 1, 0, len(gx) - 2)
    iy = np.clip(np.searchsorted(gy, ty, side="right") - 1, 0, len(gy) - 2)

    wx = (tx - gx[ix]) / np.where(gx[ix + 1] != gx[ix], gx[ix + 1] - gx[ix], 1.0)
    wy = (ty - gy[iy]) / np.where(gy[iy + 1] != gy[iy], gy[iy + 1] - gy[iy], 1.0)

    iy2 = iy[:, None]
    ix2 = ix[None, :]
    wy2 = wy[:, None]
    wx2 = wx[None, :]

    z00 = gz[iy2, ix2]
    z01 = gz[iy2, ix2 + 1]
    z10 = gz[iy2 + 1, ix2]
    z11 = gz[iy2 + 1, ix2 + 1]

    out = (
        z00 * (1.0 - wy2) * (1.0 - wx2)
        + z01 * (1.0 - wy2) * wx2
        + z10 * wy2 * (1.0 - wx2)
        + z11 * wy2 * wx2
    )
    return out.astype(np.float32)


def _bitround_f32(arr: np.ndarray, keep_mantissa_bits: int = 12) -> np.ndarray:
    """Zero low mantissa bits of finite float32 values to improve deflate compression."""
    a = np.ascontiguousarray(arr, dtype=np.float32)
    shift = 23 - keep_mantissa_bits
    if shift <= 0:
        return a
    u = a.view(np.uint32)
    rounded = ((u >> shift) << shift).view(np.float32)
    return np.where(np.isfinite(a), rounded, a).astype(np.float32)


def _read_epsg(proj_ds: h5py.Dataset) -> int:
    for key in ("epsg_code", "EPSG_code", "epsg"):
        if key in proj_ds.attrs:
            return int(proj_ds.attrs[key])
    val = proj_ds[()]
    if isinstance(val, (bytes, np.bytes_)):
        val = val.decode("utf-8")
    if isinstance(val, (int, np.integer)):
        return int(val)
    m = re.search(r"(\d{5})", str(val))
    if m:
        return int(m.group(1))
    raise ValueError(f"Could not parse EPSG from projection dataset: {val!r}")


def _decode_str(val) -> str:
    if isinstance(val, (bytes, np.bytes_)):
        return val.decode("utf-8", errors="replace")
    return str(val)


def _infer_metadata(h5: h5py.File, h5_path: Path) -> tuple[str, str, str, str, str]:
    ident = h5["/science/LSAR/identification"]
    crid = _decode_str(ident["compositeReleaseId"][()]) if "compositeReleaseId" in ident else ""
    granule = (
        _decode_str(ident["granuleId"][()])
        if "granuleId" in ident
        else h5_path.stem
    )
    m = DATE_RE.search(h5_path.name)
    if m:
        d1, d2 = m.group(1), m.group(2)
        t1 = f"{d1[:4]}-{d1[4:6]}-{d1[6:8]}"
        t2 = f"{d2[:4]}-{d2[4:6]}-{d2[6:8]}"
        if not crid:
            crid = m.group(3)
    else:
        t1 = _decode_str(ident["referenceZeroDopplerStartTime"][()])[:10]
        t2 = _decode_str(ident["secondaryZeroDopplerStartTime"][()])[:10]

    quality = (
        "provisional"
        if (crid == "P05023" and t1 >= PROVISIONAL_CUTOFF and t2 >= PROVISIONAL_CUTOFF)
        else "beta-precal"
    )
    return t1, t2, crid, granule, quality


def subset_gunw(
    h5_path: Path,
    site: str,
    out_dir: Path,
    pol: str = "HH",
    pad_m: float = 2000.0,
) -> dict:
    if site not in SITES:
        raise ValueError(f"Unknown site '{site}'. Valid: {sorted(SITES)}")

    bbox = SITES[site]["bbox"]

    with h5py.File(h5_path, "r") as h5:
        t1, t2, crid, granule, quality = _infer_metadata(h5, h5_path)
        freq_grp = h5["/science/LSAR/GUNW/grids/frequencyA"]
        center_freq = float(freq_grp["centerFrequency"][()])
        wavelength = np.float64(C_LIGHT_M_S / center_freq)

        pol_grp = freq_grp[f"unwrappedInterferogram/{pol}"]
        x = pol_grp["xCoordinates"][:].astype(np.float64)
        y = pol_grp["yCoordinates"][:].astype(np.float64)
        epsg = _read_epsg(pol_grp["projection"])

        xmin, ymin, xmax, ymax = bbox_to_utm_bounds(bbox, epsg, pad_m=pad_m)
        x_idx = np.where((x >= xmin) & (x <= xmax))[0]
        y_idx = np.where((y >= ymin) & (y <= ymax))[0]

        if len(x_idx) == 0 or len(y_idx) == 0:
            raise ValueError(
                f"Site '{site}' bbox UTM ({xmin:.0f}..{xmax:.0f}, {ymin:.0f}..{ymax:.0f}) "
                f"does not intersect granule grid ({x.min():.0f}..{x.max():.0f}, {y.min():.0f}..{y.max():.0f})"
            )

        xs = slice(int(x_idx[0]), int(x_idx[-1]) + 1)
        ys = slice(int(y_idx[0]), int(y_idx[-1]) + 1)

        x_sub = x[xs]
        y_sub = y[ys]

        unw = pol_grp["unwrappedPhase"][ys, xs].astype(np.float32)
        coh_f = pol_grp["coherenceMagnitude"][ys, xs].astype(np.float32)
        if "connectedComponents" in pol_grp:
            conn = pol_grp["connectedComponents"][ys, xs].astype(np.uint16)
            unw = np.where((conn == 0) | (conn == 65535), np.nan, unw)
        else:
            conn = np.ones(unw.shape, dtype=np.uint16)

        ion = (
            pol_grp["ionospherePhaseScreen"][ys, xs].astype(np.float32)
            if "ionospherePhaseScreen" in pol_grp
            else np.array([], dtype=np.float32)
        )

        coh_u8 = (
            np.clip(np.nan_to_num(coh_f, nan=0.0) * 255.0 + 0.5, 0.0, 255.0)
            .astype(np.uint8)
        )

        radar_grid = h5["/science/LSAR/GUNW/metadata/radarGrid"]
        if "incidenceAngle" in radar_grid:
            height_key = (
                "heightAboveEllipsoid"
                if "heightAboveEllipsoid" in radar_grid
                else "heights"
            )
            heights = radar_grid[height_key][:]
            z_idx = int(np.argmin(np.abs(heights)))
            h_used = float(heights[z_idx])
            rg_x = radar_grid["xCoordinates"][:]
            rg_y = radar_grid["yCoordinates"][:]
            inc_slice = radar_grid["incidenceAngle"][z_idx, :, :]
            inc_sub = _bitround_f32(
                bilinear_interp_2d(rg_x, rg_y, inc_slice, x_sub, y_sub),
                keep_mantissa_bits=12,
            )
        else:
            h_used = 0.0
            inc_sub = np.full(unw.shape, np.nan, dtype=np.float32)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{t1}_{t2}.npz"

    payload = {
        "unw": unw,
        "coh": coh_u8,
        "conncomp": conn,
        "ion": ion,
        "x": x_sub,
        "y": y_sub,
        "epsg": np.int32(epsg),
        "wavelength": wavelength,
        "incidence": inc_sub,
        "incidence_height_m": np.float64(h_used),
        "date1": np.array(t1),
        "date2": np.array(t2),
        "granule": np.array(granule),
        "crid": np.array(crid),
        "quality": np.array(quality),
    }

    np.savez_compressed(out_path, **payload)
    size_mb = out_path.stat().st_size / (1024 * 1024)
    ion_bits = "full"
    for keep_bits in (14, 12):
        if size_mb <= MAX_NPZ_MB or payload["ion"].size == 0:
            break
        payload["ion"] = _bitround_f32(ion, keep_mantissa_bits=keep_bits)
        np.savez_compressed(out_path, **payload)
        size_mb = out_path.stat().st_size / (1024 * 1024)
        ion_bits = f"{keep_bits}b"

    if size_mb > 20.0:
        raise ValueError(f"Output {out_path} is {size_mb:.2f} MB (> 20 MB limit)")

    with np.load(out_path) as data:
        assert data["unw"].shape == data["coh"].shape == data["incidence"].shape == data["ion"].shape
        assert data["unw"].dtype == np.float32
        assert data["coh"].dtype == np.uint8
        assert data["ion"].dtype == np.float32
        nan_pct = float(100.0 * np.isnan(data["unw"]).mean())
        shape = data["unw"].shape

    return {
        "out_path": out_path,
        "t1": t1,
        "t2": t2,
        "shape": shape,
        "size_mb": round(size_mb, 2),
        "nan_pct": round(nan_pct, 2),
        "epsg": epsg,
        "wavelength": float(wavelength),
        "quality": quality,
        "ion_bits": ion_bits,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Subset NISAR GUNW .h5 to .npz.")
    parser.add_argument("h5_path", type=Path)
    parser.add_argument("site", choices=sorted(SITES))
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (defaults to pipeline/subset/<site>)",
    )
    parser.add_argument("--pol", default="HH")
    args = parser.parse_args()

    out_dir = (
        args.out_dir
        if args.out_dir is not None
        else Path(__file__).resolve().parent / "subset" / args.site
    )
    info = subset_gunw(args.h5_path, args.site, out_dir, pol=args.pol)
    print(
        f"Saved {info['out_path']} | shape={info['shape']} | "
        f"size={info['size_mb']:.2f} MB | NaN={info['nan_pct']:.2f}% | "
        f"epsg={info['epsg']} | lambda={info['wavelength']:.5f} m | "
        f"quality={info['quality']} | ion_bits={info['ion_bits']}"
    )


if __name__ == "__main__":
    main()
