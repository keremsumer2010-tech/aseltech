"""Extract provisional NISAR L3 SME2 soil moisture and HV backscatter for Karapinar via HTTP Range reads.

Produces data/karapinar/drivers.json matching the Central Valley drivers.json schema.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import asf_search as asf
import h5py
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))

from download import read_earthdata_token  # noqa: E402
from search import PROVISIONAL_CUTOFF, SITES, bbox_to_wkt  # noqa: E402
from sme2_drivers import HttpRangeFile  # noqa: E402


def build_karapinar_drivers() -> dict:
    site = "karapinar"
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
    print(f"Found {len(prov)} provisional SME2 granules for Karapinar")

    token = read_earthdata_token()
    sm_by_date: dict[str, dict] = {}
    for r in prov:
        dt = r.properties["startTime"][:10]
        granule = r.properties["fileID"]
        print(f"  Reading SME2 {dt}: {granule}")
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
    dates = [d for d in pts[0]["dates"] if d in sm_by_date]
    idx = [i for i, d in enumerate(pts[0]["dates"]) if d in sm_by_date]

    p01 = next((p for p in pts if p.get("id") == "p01"), pts[0])
    sub = np.array([p01["disp_cm"][i] for i in idx], dtype=float)
    top5_subs = [[p["disp_cm"][i] for i in idx] for p in pts if p.get("kind") == "most_subsiding"]
    sub5 = np.mean(top5_subs, axis=0) if top5_subs else sub

    sm_arr = np.array([sm_by_date[d]["sm_mean"] for d in dates], dtype=float)
    sm_med_arr = [sm_by_date[d]["sm_median"] for d in dates]
    hv_arr = np.array([sm_by_date[d]["hv_db"] for d in dates], dtype=float)
    granules = [sm_by_date[d]["granule"] for d in dates]

    sm_norm = (sm_arr - sm_arr.min()) / max(float(sm_arr.max() - sm_arr.min()), 1e-9)
    hv_norm = (hv_arr - hv_arr.min()) / max(float(hv_arr.max() - hv_arr.min()), 1e-9)
    irr = np.round(0.5 * sm_norm + 0.5 * hv_norm, 3)

    corr_sm = round(float(np.corrcoef(sm_arr, sub)[0, 1]), 3)
    corr_irr = round(float(np.corrcoef(irr, sub)[0, 1]), 3)
    lag1_sm = round(float(np.corrcoef(sm_arr[:-1], sub[1:])[0, 1]), 3) if len(dates) > 2 else None

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
            "subsidence_cm": f"cm (LOS, negative = subsidence, from {p01.get('id')} {p01.get('name')} in points.json)",
            "soil_moisture": "m^3/m^3 (volumetric soil moisture, Karapinar bbox mean from NISAR L3 SME2)",
            "hv_backscatter_db": "dB (10*log10(sigma0_HV) from NISAR L3 SME2 frequencyA)",
            "irrigation_index": "0-1 normalized composite of volumetric soil moisture and HV crop canopy backscatter",
        },
        "granules": granules,
        "source": (
            f"NISAR L3 SME2 (PROVISIONAL, CRID P05023, track {cfg['path']} descending frame {cfg['frame']}, "
            "200 m EASE-Grid 2.0) + NISAR L2 GUNW cumulative subsidence (data/karapinar/points.json)"
        ),
        "notes": (
            f"Bbox [{w}, {s}, {e}, {n}] mean volumetric soil moisture (grids/soilMoisture, 0 < sm <= 0.6 m^3/m^3) "
            "and L-band HV radar backscatter (grids/radarData/frequencyA/sigma0HV in dB) extracted over Karapinar "
            "and paired with cumulative LOS subsidence."
        ),
        "quality": "provisional",
        "quality_note": (
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
            "(NASA-JPL and ISRO), not by our team."
        ),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    out_path = ROOT / "data" / "karapinar" / "drivers.json"
    payload = build_karapinar_drivers()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({len(payload['dates'])} dates, lag_corr={payload['lag_corr']})")


if __name__ == "__main__":
    main()
