"""Re-run Mexico City cumulative displacement with an off-basin stable volcanic-margin reference (KALITE STANDARDI §3)."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))

import cumulative as pc3_cum  # noqa: E402
import gunw_io  # noqa: E402
from insar import (  # noqa: E402
    choose_reference,
    cycle_outliers,
    deramp,
    mask_coherence,
    mask_components,
    phase_to_cm,
    reference,
)

SITE = "global_mexico_city"
BBOX = (-99.25, 19.25, -98.90, 19.60)
THR = 0.3
REF_RADIUS = 3


def main() -> None:
    gunw_io.BBOX[SITE] = BBOX
    _, files = pc3_cum.load_pairs(SITE)
    used, notes = pc3_cum.chain(files, ("provisional",))
    d0 = used[0][3]
    x, y, epsg = d0["x"], d0["y"], int(d0["epsg"])

    pair_cm, stats = [], []
    for d1, d2, f, d in used:
        unw = d["unw"] - d["ion"]
        cm = phase_to_cm(unw, float(d["wavelength"]))
        if "conncomp" in d and d["conncomp"].size:
            cm = mask_components(cm, d["conncomp"])
        cm = mask_coherence(cm, d["coh"], THR)
        cm = pc3_cum.remove_islands(cm, pc3_cum.ISLAND_MIN_PX)
        cm = deramp(cm, order=1)
        n_before = int(np.isfinite(cm).sum())
        cm = cycle_outliers(cm, thr_cm=float(d["wavelength"]) / 4 * 100)
        cycle_px = n_before - int(np.isfinite(cm).sum())
        pair_cm.append(cm)
        stats.append({
            "pair": [d1, d2],
            "file": str(f.relative_to(ROOT)).replace("\\", "/"),
            "lambda_m": float(d["wavelength"]),
            "ionosphere_applied": True,
            "cycle_outlier_px": cycle_px,
            "elev_coef_cm_per_km": None,
            "valid_frac_after_masks": float(np.isfinite(cm).mean()),
        })

    valid_all = np.logical_and.reduce([np.isfinite(c) for c in pair_cm])
    coh_mean = np.mean([np.load(f)["coh"].astype(np.float32) / 255 for _, _, f, _ in used], axis=0)
    XX, YY = np.meshgrid(x, y)
    LON, LAT = Transformer.from_crs(epsg, 4326, always_xy=True).transform(XX, YY)
    in_bbox = (LON >= BBOX[0]) & (LON <= BBOX[2]) & (LAT >= BBOX[1]) & (LAT <= BBOX[3])

    # Restrict primary reference to stable SW/W volcanic rock margin outside the lacustrine subsidence basin
    off_basin = in_bbox & (LON < -99.17) & (LAT < 19.45)
    r, c, mcoh = choose_reference(coh_mean, valid_all & off_basin, REF_RADIUS, stride=3)
    lon_r, lat_r = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c], y[r])
    print(f"Off-basin reference: row={r} col={c} lon={lon_r:.4f} lat={lat_r:.4f} mean_coh={mcoh:.2f}")

    dates = [used[0][0]] + [p[1] for p in used]
    cum = [np.zeros_like(pair_cm[0])]
    cum[0][~valid_all] = np.nan
    n_out = 0
    for i, cm in enumerate(pair_cm):
        cm = reference(cm, (r, c), REF_RADIUS)
        bad = np.abs(cm) > pc3_cum.PAIR_OUTLIER_CM
        n_out += int(bad.sum())
        cm[bad] = np.nan
        stats[i]["p2_p50_p98_cm"] = [round(float(v), 2) for v in np.nanpercentile(cm, [2, 50, 98])]
        cum.append(cum[-1] + cm)
    for k in range(len(cum)):
        cum[k][~valid_all] = np.nan
    final = cum[-1]
    valid = np.isfinite(final)

    sm = pc3_cum.block_median(np.where(in_bbox, final, np.nan), pc3_cum.BLOCK_PX, pc3_cum.BLOCK_MIN_VALID, pc3_cum.BLOCK_MAX_STD)
    rmin, cmin = np.unravel_index(np.nanargmin(sm), sm.shape)
    max_sub = float(sm[rmin, cmin])
    p2_cm = float(np.nanpercentile(final[in_bbox & valid], 2))

    # Alternative reference windows >= 30 km away
    def dist_mask(rr, cc):
        return np.hypot((np.arange(len(y))[:, None] - rr) * abs(y[1] - y[0]),
                        (np.arange(len(x))[None, :] - cc) * abs(x[1] - x[0])) < 30000

    used_refs, alts = [(r, c)], []
    for _ in range(2):
        excl = np.logical_or.reduce([dist_mask(rr, cc) for rr, cc in used_refs])
        try:
            r2, c2, _ = choose_reference(coh_mean, valid_all & in_bbox, REF_RADIUS, stride=3, exclude=excl)
        except ValueError:
            break
        used_refs.append((r2, c2))
        alt = np.zeros_like(final)
        for cm in pair_cm:
            q = reference(cm, (r2, c2), REF_RADIUS)
            q[np.abs(q) > pc3_cum.PAIR_OUTLIER_CM] = np.nan
            alt = alt + q
        alt[~valid_all] = np.nan
        sm_alt = pc3_cum.block_median(np.where(in_bbox, alt, np.nan), pc3_cum.BLOCK_PX, pc3_cum.BLOCK_MIN_VALID, pc3_cum.BLOCK_MAX_STD)
        alt_max = float(sm_alt[rmin, cmin]) if np.isfinite(sm_alt[rmin, cmin]) else float(np.nanmin(sm_alt))
        lon_r2, lat_r2 = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c2], y[r2])
        alts.append({
            "alt_reference": {"lon": round(lon_r2, 5), "lat": round(lat_r2, 5)},
            "max_subsidence_cm_at_same_location": round(alt_max, 1),
        })

    range_cm = sorted([round(max_sub, 1)] + [q["max_subsidence_cm_at_same_location"] for q in alts]) if alts else None
    inc = d0["incidence"] if "incidence" in d0 and d0["incidence"].size else None
    inc_at = float(inc[rmin, cmin]) if inc is not None else None
    days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
    lon_m, lat_m = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[cmin], y[rmin])
    vlim = float(np.ceil(np.nanpercentile(np.abs(sm), 99.5)))
    vmin, vmax = -vlim, vlim

    ddir = ROOT / "data" / "global" / "mexico_city"
    (ddir / "disp").mkdir(parents=True, exist_ok=True)
    for dt, g in zip(dates, cum):
        pc3_cum.save_png(pc3_cum.to_latlon_grid(g, x, y, epsg, BBOX), ddir / "disp" / f"{dt}.png", vmin, vmax)

    out = ROOT / "analysis" / "out"
    np.savez_compressed(
        out / f"{SITE}_cum.npz",
        cum_cm=final.astype(np.float32),
        x=x,
        y=y,
        epsg=np.int32(epsg),
        dates=np.array(dates),
        quality="provisional",
        incidence=(inc.astype(np.float16) if inc is not None else np.array([])),
        reference_rc=np.array([r, c]),
    )

    granules = [str(p[3]["granule"]) for p in used if "granule" in p[3]]
    pairs_txt = ", ".join(f"{p[0]}_{p[1]}" for p in used)
    meta = {
        "site": SITE,
        "bbox": list(BBOX),
        "dates": dates,
        "units": "cm",
        "vmin": vmin,
        "vmax": vmax,
        "component": "LOS (line of sight); negative = away from satellite = subsidence",
        "colormap": "RdBu (red = subsidence, blue = uplift/toward satellite)",
        "source": "NISAR L2 GUNW (PROVISIONAL, CRID P05023) via ASF DAAC, track 113 descending frame 79; https://nisar-docs.asf.alaska.edu/gunw",
        "granules": granules,
        "notes": (
            f"Cumulative LOS displacement relative to {dates[0]}, sum of {len(used)} consecutive pairs ({pairs_txt}). "
            f"Re-referenced to stable SW volcanic margin outside the lakebed subsidence basin at {lon_r:.4f}E {lat_r:.4f}N. "
            + " ".join(notes)
        ),
        "reference_point": {"lon": round(lon_r, 5), "lat": round(lat_r, 5)},
        "quality": "provisional",
        "quality_note": pc3_cum.DISCLAIMER,
    }
    (ddir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    pts = pc3_cum.pick_points(sm, np.isfinite(sm), (r, c), x, y, epsg)
    points = []
    for i, (kind, pr, pc, lon, lat) in enumerate(pts, 1):
        hb = pc3_cum.BLOCK_PX // 2
        win = np.stack(cum)[:, max(pr - hb, 0): pr + hb + 1, max(pc - hb, 0): pc + hb + 1]
        ts = np.nanmedian(win.reshape(len(dates), -1), axis=1)
        points.append({
            "id": f"p{i:02d}",
            "name": pc3_cum.place_label(lon, lat, []),
            "kind": kind,
            "lon": round(lon, 5),
            "lat": round(lat, 5),
            "dates": dates,
            "disp_cm": [None if not np.isfinite(v) else round(float(v), 2) for v in ts],
        })
    (ddir / "points.json").write_text(json.dumps(points, indent=2), encoding="utf-8")

    rate_yr = max_sub / days * 365.25
    rate_100d = max_sub / days * 100.0
    summary = {
        "max_subsidence_cm": round(max_sub, 1),
        "p2_cm": round(p2_cm, 1),
        "rate_cm_per_100d": round(rate_100d, 1),
        "max_subsidence_range_cm": [range_cm[0], range_cm[-1]] if range_cm else None,
        "range_cm": [range_cm[0], range_cm[-1]] if range_cm else None,
        "n_references": len(alts) + 1,
        "reference_sensitivity": alts[0] if alts else None,
        "reference_sensitivity_all": alts,
        "period": [dates[0], dates[-1]],
        "rate_cm_per_yr_estimate": round(rate_yr, 1),
        "reference_point": {"lon": round(lon_r, 5), "lat": round(lat_r, 5)},
        "quality": "provisional",
        "quality_note": pc3_cum.DISCLAIMER,
        "component": "LOS",
        "max_subsidence_location": {"lon": round(lon_m, 5), "lat": round(lat_m, 5)},
        "max_subsidence_vertical_cm_estimate": round(max_sub / np.cos(np.deg2rad(inc_at)), 1) if inc_at else None,
        "incidence_deg_at_max": round(inc_at, 1) if inc_at else None,
        "n_pairs": len(used),
        "valid_fraction": round(float(valid[in_bbox].mean()), 3),
        "method_note": (
            f"Re-referenced to SW volcanic margin outside the lakebed basin (previous in-basin reference at -99.0126E, 19.5872N gave -4.4 cm). "
            f"Headline value = most negative median of ~1 km blocks; p2_cm = {p2_cm:.1f} cm; rate_cm_per_100d = {rate_100d:.1f} cm/100d."
        ),
    }
    (ddir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / f"{SITE}_pair_stats.json").write_text(
        json.dumps({
            "pairs": stats,
            "notes": notes,
            "reference_mean_coh": mcoh,
            "valid_frac_full_chain": float(valid[in_bbox].mean()),
            "outlier_px_removed": n_out,
        }, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
