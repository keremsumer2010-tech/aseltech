"""Extract and render provisional NISAR L2 GCOV HV backscatter (gamma0_HV in dB) for Central Valley (Q03).

Produces north-up RGBA PNG overlays aligned to the site bbox [-120.2, 35.6, -119.0, 36.6]
and writes data/central_valley/gcov/meta.json matching rules/VERI_SOZLESMESI.md.
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import asf_search as asf
import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import requests
from requests.adapters import HTTPAdapter

from download import read_earthdata_token
from search import PROVISIONAL_CUTOFF, SITES, bbox_to_wkt
from subset import bbox_to_utm_bounds

ROOT = Path(__file__).resolve().parent.parent
VMIN_DB = -28.0
VMAX_DB = -10.0
CMAP = "viridis"


class FastHttpRangeFile(io.RawIOBase):
    """Seekable HTTP Range reader with 16-thread sequential read-ahead for large GCOV HDF5s."""

    def __init__(self, url: str, token: str, block_size: int = 4 * 1024 * 1024, prefetch: int = 16) -> None:
        self.s = requests.Session()
        adapter = HTTPAdapter(pool_connections=32, pool_maxsize=32, max_retries=5)
        self.s.mount("https://", adapter)
        r = self.s.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Range": "bytes=0-15"},
            allow_redirects=True,
            timeout=60,
        )
        r.raise_for_status()
        self.signed_url = r.url
        self.size = int(r.headers["Content-Range"].split("/")[-1])
        self.pos = 0
        self.block_size = block_size
        self.prefetch = prefetch
        self.cache: dict[int, bytes] = {}
        self.pool = ThreadPoolExecutor(max_workers=16)

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        elif whence == io.SEEK_END:
            self.pos = self.size + offset
        return self.pos

    def _get_one(self, bidx: int) -> tuple[int, bytes]:
        start = bidx * self.block_size
        if start >= self.size:
            return bidx, b""
        end = min(self.size - 1, start + self.block_size - 1)
        r = self.s.get(self.signed_url, headers={"Range": f"bytes={start}-{end}"}, timeout=60)
        r.raise_for_status()
        return bidx, r.content

    def _fetch_block(self, bidx: int) -> bytes:
        if bidx not in self.cache:
            if (bidx - 1) in self.cache:
                todo = [
                    k
                    for k in range(bidx, bidx + self.prefetch)
                    if k not in self.cache and k * self.block_size < self.size
                ]
            else:
                todo = [bidx]
            for k, data in self.pool.map(self._get_one, todo):
                self.cache[k] = data
        return self.cache[bidx]

    def read(self, size: int = -1) -> bytes:
        if self.pos >= self.size:
            return b""
        if size < 0 or self.pos + size > self.size:
            size = self.size - self.pos
        out = bytearray()
        rem = size
        while rem > 0 and self.pos < self.size:
            bidx = self.pos // self.block_size
            boff = self.pos % self.block_size
            blk = self._fetch_block(bidx)
            take = min(rem, len(blk) - boff)
            out.extend(blk[boff : boff + take])
            self.pos += take
            rem -= take
        return bytes(out)

    def readinto(self, b) -> int:
        data = self.read(len(b))
        n = len(data)
        b[:n] = data
        return n


def _lonlat_to_utm_vec(lon_grid: np.ndarray, lat_grid: np.ndarray, epsg: int) -> tuple[np.ndarray, np.ndarray]:
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

    lon0 = np.radians((zone - 1) * 6 - 180 + 3)
    lat_r = np.radians(lat_grid)
    lon_r = np.radians(lon_grid)
    dlon = lon_r - lon0

    sin_lat = np.sin(lat_r)
    cos_lat = np.cos(lat_r)
    tan_lat = np.tan(lat_r)

    n_rad = a / np.sqrt(1.0 - e2 * sin_lat**2)
    t_val = tan_lat**2
    c_val = ep2 * cos_lat**2
    a_val = cos_lat * dlon
    m_val = a * (
        (1.0 - e2 / 4.0 - 3.0 * e2**2 / 64.0 - 5.0 * e2**3 / 256.0) * lat_r
        - (3.0 * e2 / 8.0 + 3.0 * e2**2 / 32.0 + 45.0 * e2**3 / 1024.0) * np.sin(2.0 * lat_r)
        + (15.0 * e2**2 / 256.0 + 45.0 * e2**3 / 1024.0) * np.sin(4.0 * lat_r)
        - (35.0 * e2**3 / 3072.0) * np.sin(6.0 * lat_r)
    )

    x = (
        k0
        * n_rad
        * (
            a_val
            + (1.0 - t_val + c_val) * a_val**3 / 6.0
            + (5.0 - 18.0 * t_val + t_val**2 + 72.0 * c_val - 58.0 * ep2) * a_val**5 / 120.0
        )
        + 500000.0
    )
    y = k0 * (
        m_val
        + n_rad
        * tan_lat
        * (
            a_val**2 / 2.0
            + (5.0 - t_val + 9.0 * c_val + 4.0 * c_val**2) * a_val**4 / 24.0
            + (61.0 - 58.0 * t_val + t_val**2 + 600.0 * c_val - 330.0 * ep2) * a_val**6 / 720.0
        )
    )
    if south:
        y += 10000000.0
    return x, y


def to_latlon_grid(
    arr: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    epsg: int,
    bbox: tuple[float, float, float, float],
    step: float = 0.001,
) -> np.ndarray:
    w, s, e, n = bbox
    lons = np.arange(w + step / 2, e, step)
    lats = np.arange(n - step / 2, s, -step)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    utmx, utmy = _lonlat_to_utm_vec(lon_grid, lat_grid, epsg)
    dx, dy = x[1] - x[0], y[1] - y[0]
    ix = np.rint((utmx - x[0]) / dx).astype(int)
    iy = np.rint((utmy - y[0]) / dy).astype(int)
    ok = (ix >= 0) & (ix < len(x)) & (iy >= 0) & (iy < len(y))
    out = np.full(lon_grid.shape, np.nan, np.float32)
    out[ok] = arr[iy[ok], ix[ok]]
    return out


def save_png(grid: np.ndarray, path: Path, vmin: float = VMIN_DB, vmax: float = VMAX_DB) -> None:
    cmap = plt.get_cmap(CMAP).copy()
    cmap.set_bad((0, 0, 0, 0))
    plt.imsave(path, np.ma.masked_invalid(grid), cmap=cmap, vmin=vmin, vmax=vmax)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Central Valley GCOV HV dB PNGs + meta.json.")
    parser.add_argument("--site", default="central_valley", choices=["central_valley"])
    parser.add_argument("--cache-dir", type=Path, default=ROOT / "raw" / "gcov_cache")
    args = parser.parse_args()

    cfg = SITES[args.site]
    bbox = cfg["bbox"]
    out_dir = ROOT / "data" / args.site / "gcov"
    out_dir.mkdir(parents=True, exist_ok=True)

    cached = sorted(args.cache_dir.glob("*.npz")) if args.cache_dir.exists() else []
    if not cached:
        res = asf.search(
            platform="NISAR",
            processingLevel="GCOV",
            relativeOrbit=cfg["path"],
            frame=cfg["frame"],
            intersectsWith=bbox_to_wkt(bbox),
        )
        prov = sorted(
            [
                r
                for r in res
                if "P05023" in r.properties.get("fileID", "")
                and r.properties.get("startTime", "")[:10] >= PROVISIONAL_CUTOFF
            ],
            key=lambda x: x.properties["startTime"],
        )
        args.cache_dir.mkdir(parents=True, exist_ok=True)
        token = read_earthdata_token()
        xmin, ymin, xmax, ymax = bbox_to_utm_bounds(bbox, 32611, pad_m=0.0)
        for r in prov:
            dt = r.properties["startTime"][:10]
            dst = args.cache_dir / f"{dt}.npz"
            rf = FastHttpRangeFile(r.properties["url"], token)
            with h5py.File(rf, "r") as f:
                fa = f["science/LSAR/GCOV/grids/frequencyA"]
                x, y = fa["xCoordinates"][:], fa["yCoordinates"][:]
                ix = np.where((x >= xmin) & (x <= xmax))[0]
                iy = np.where((y >= ymin) & (y <= ymax))[0]
                xs = slice(int(ix[0]), int(ix[-1]) + 1, 8)
                ys = slice(int(iy[0]), int(iy[-1]) + 1, 8)
                hv = fa["HVHV"][ys, xs].astype(np.float32)
                hv_db = np.where(
                    (hv > 0) & np.isfinite(hv),
                    10.0 * np.log10(np.maximum(hv, 1e-10)),
                    np.nan,
                ).astype(np.float32)
                np.savez_compressed(
                    dst,
                    hv_db=hv_db,
                    x=x[xs],
                    y=y[ys],
                    epsg=np.int32(32611),
                    date=dt,
                    granule=r.properties["fileID"],
                )
        cached = sorted(args.cache_dir.glob("*.npz"))

    dates: list[str] = []
    granules: list[str] = []
    mean_dbs: list[float] = []
    for fpath in cached:
        with np.load(fpath, allow_pickle=False) as d:
            dt = str(d["date"])
            granule = str(d["granule"])
            hv_db = d["hv_db"].astype(np.float32)
            x = d["x"].astype(np.float64)
            y = d["y"].astype(np.float64)
            epsg = int(d["epsg"])
        grid = to_latlon_grid(hv_db, x, y, epsg, bbox, step=0.001)
        png_path = out_dir / f"{dt}.png"
        save_png(grid, png_path, vmin=VMIN_DB, vmax=VMAX_DB)
        dates.append(dt)
        granules.append(granule)
        mean_dbs.append(round(float(np.nanmean(hv_db)), 2))
        print(f"Wrote {png_path.name} ({png_path.stat().st_size / 1e6:.2f} MB) | mean={mean_dbs[-1]} dB")

    meta = {
        "site": args.site,
        "bbox": list(bbox),
        "dates": dates,
        "units": "dB",
        "vmin": VMIN_DB,
        "vmax": VMAX_DB,
        "mean_hv_db": mean_dbs,
        "component": "L-band cross-pol radar backscatter gamma0_HV (10*log10(HVHV), frequencyA)",
        "colormap": "viridis (dark = bare/dry soil or open water, bright = irrigated crop canopy / vegetation volume)",
        "source": (
            f"NISAR L2 GCOV (PROVISIONAL, CRID P05023) via ASF DAAC, track {cfg['path']} ascending "
            f"frame {cfg['frame']}; https://nisar-docs.asf.alaska.edu/gcov"
        ),
        "granules": granules,
        "notes": (
            "Geocoded terrain-corrected cross-polarisation backscatter gamma0_HV in dB "
            "(10*log10(science/LSAR/GCOV/grids/frequencyA/HVHV)) resampled from UTM Zone 11N (EPSG:32611, "
            "160 m stride) onto a regular 0.001 deg lon/lat grid covering [-120.2, 35.6, -119.0, 36.6]. "
            "All 8 provisional dates share a fixed colour scale [-28, -10] dB."
        ),
        "quality": "provisional",
        "quality_note": (
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
            "(NASA-JPL and ISRO), not by our team."
        ),
    }
    meta_path = out_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {meta_path} ({len(dates)} dates)")

    if args.cache_dir.exists():
        shutil.rmtree(args.cache_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
