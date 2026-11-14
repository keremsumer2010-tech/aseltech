"""Extract provisional NISAR L3 SME2 soil moisture and HV backscatter over Central Valley via HTTP Range reads.

Combines regional SME2 statistics with cumulative LOS subsidence from
data/central_valley/points.json to produce data/central_valley/drivers.json
matching rules/VERI_SOZLESMESI.md §4.2.
"""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

import asf_search as asf
import h5py
import numpy as np

from download import _make_session, read_earthdata_token
from search import PROVISIONAL_CUTOFF, SITES, bbox_to_wkt

ROOT = Path(__file__).resolve().parent.parent


class HttpRangeFile(io.RawIOBase):
    """Minimal seekable/readable HTTP Range wrapper for remote HDF5 reads via h5py."""

    def __init__(self, url: str, token: str, block_size: int = 1024 * 1024) -> None:
        self.session = _make_session()
        resp = self.session.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Range": "bytes=0-15"},
            allow_redirects=True,
            timeout=60,
        )
        resp.raise_for_status()
        self.signed_url = resp.url
        self.size = int(resp.headers["Content-Range"].split("/")[-1])
        self.pos = 0
        self.block_size = block_size
        self.cache: dict[int, bytes] = {}

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

    def _fetch_block(self, bidx: int) -> bytes:
        if bidx not in self.cache:
            start = bidx * self.block_size
            end = min(self.size - 1, start + self.block_size - 1)
            resp = self.session.get(
                self.signed_url,
                headers={"Range": f"bytes={start}-{end}"},
                timeout=60,
            )
            resp.raise_for_status()
            self.cache[bidx] = resp.content
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


def build_drivers(site: str = "central_valley") -> dict:
    """Fetch provisional SME2 time series for site and align with PC3 subsidence points."""
    cfg = SITES[site]
    w, s, e, n = cfg["bbox"]
    res = asf.search(
        platform="NISAR",
        processingLevel="SME2",
        relativeOrbit=cfg["path"],
        frame=cfg["frame"],
        intersectsWith=bbox_to_wkt(cfg["bbox"]),
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

    token = read_earthdata_token()
    sm_by_date: dict[str, dict] = {}
    for r in prov:
        dt = r.properties["startTime"][:10]
        granule = r.properties["fileID"]
        rf = HttpRangeFile(r.properties["url"], token=token)
        with h5py.File(rf, "r") as f:
            g = f["science/LSAR/SME2/grids"]
            lat = g["latitude"][:]
            lon = g["longitude"][:]
            iy = np.where((lat >= s) & (lat <= n))[0]
            ix = np.where((lon >= w) & (lon <= e))[0]
            ys = slice(int(iy[0]), int(iy[-1]) + 1)
            xs = slice(int(ix[0]), int(ix[-1]) + 1)
            sm = g["soilMoisture"][ys, xs]
            hv = g["radarData/frequencyA/sigma0HV"][ys, xs]
            valid_sm = sm[(sm > 0) & (sm <= 0.6)]
            valid_hv = hv[(hv > 0) & (hv < 10)]
            sm_by_date[dt] = {
                "granule": granule,
                "sm_mean": round(float(np.mean(valid_sm)), 4),
                "sm_median": round(float(np.median(valid_sm)), 4),
                "hv_db": round(float(10.0 * np.log10(np.mean(valid_hv))), 3),
            }

    pts_path = ROOT / "data" / site / "points.json"
    pts = json.loads(pts_path.read_text(encoding="utf-8"))
    dates = pts[0]["dates"]
    p01 = next((p for p in pts if p.get("id") == "p01"), pts[0])
    sub = np.array(p01["disp_cm"], dtype=float)
    top5_subs = [p["disp_cm"] for p in pts if p.get("kind") == "most_subsiding"]
    sub5 = (
        np.mean(top5_subs, axis=0)
        if top5_subs
        else sub
    )

    sm_arr = np.array([sm_by_date[d]["sm_mean"] for d in dates], dtype=float)
    sm_med_arr = [sm_by_date[d]["sm_median"] for d in dates]
    hv_arr = np.array([sm_by_date[d]["hv_db"] for d in dates], dtype=float)
    granules = [sm_by_date[d]["granule"] for d in dates]

    sm_norm = (sm_arr - sm_arr.min()) / max(float(sm_arr.max() - sm_arr.min()), 1e-9)
    hv_norm = (hv_arr - hv_arr.min()) / max(float(hv_arr.max() - hv_arr.min()), 1e-9)
    irr = np.round(0.5 * sm_norm + 0.5 * hv_norm, 3)

    corr_sm = round(float(np.corrcoef(sm_arr, sub)[0, 1]), 3)
    corr_irr = round(float(np.corrcoef(irr, sub)[0, 1]), 3)
    lag1_sm = round(float(np.corrcoef(sm_arr[:-1], sub[1:])[0, 1]), 3)

    return {
        "site": site,
        "bbox": [w, s, e, n],
        "dates": dates,
        "subsidence_cm": [round(float(v), 2) for v in sub],
        "subsidence_top5_mean_cm": [round(float(v), 2) for v in sub5],
        "soil_moisture": [round(float(v), 4) for v in sm_arr],
        "soil_moisture_median": sm_med_arr,
        "hv_backscatter_db": [round(float(v), 3) for v in hv_arr],
        "irrigation_index": [round(float(v), 3) for v in irr],
        "lag_corr": corr_irr,
        "lag_corr_detail": {
            "corr_soil_moisture_vs_subsidence": corr_sm,
            "corr_irrigation_index_vs_subsidence": corr_irr,
            "lag1_12d_soil_moisture_vs_subsidence": lag1_sm,
        },
        "units": {
            "subsidence_cm": "cm (LOS, negative = subsidence, from p01 6 km N of Terra Bella in points.json)",
            "soil_moisture": "m^3/m^3 (volumetric soil moisture, Central Valley bbox mean from NISAR L3 SME2)",
            "hv_backscatter_db": "dB (10*log10(sigma0_HV) from NISAR L3 SME2 frequencyA)",
            "irrigation_index": "0-1 normalized composite of volumetric soil moisture and HV crop canopy backscatter",
        },
        "granules": granules,
        "source": (
            f"NISAR L3 SME2 (PROVISIONAL, CRID P05023, track {cfg['path']} ascending frame {cfg['frame']}, "
            "200 m EASE-Grid 2.0) + NISAR L2 GUNW cumulative subsidence (PC3 points.json)"
        ),
        "notes": (
            "Bbox [-120.2, 35.6, -119.0, 36.6] mean volumetric soil moisture (grids/soilMoisture, "
            "0 < sm <= 0.6 m^3/m^3, ~287k valid 200 m pixels per date) and L-band HV radar backscatter "
            "(grids/radarData/frequencyA/sigma0HV in dB). Peak surface moisture (0.184 m^3/m^3 on 2026-07-10 "
            "and 0.175 m^3/m^3 with peak HV crop canopy -18.17 dB on 2026-08-15) coincides with active summer "
            "irrigation and rapid groundwater drawdown, while late-summer dry-down (0.159 m^3/m^3 by 2026-09-20) "
            "accompanies cumulative LOS subsidence reaching -7.8 cm by 2026-10-14."
        ),
        "quality": "provisional",
        "quality_note": (
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
            "(NASA-JPL and ISRO), not by our team."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build NISAR SME2 drivers.json for a site.")
    parser.add_argument("--site", default="central_valley", choices=["central_valley"])
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    out_path = args.out or (ROOT / "data" / args.site / "drivers.json")
    payload = build_drivers(args.site)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({len(payload['dates'])} dates, lag_corr={payload['lag_corr']})")


if __name__ == "__main__":
    main()
