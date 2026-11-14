"""Karapınar second-orbit cross-check: Track 7 Descending (frame 69) vs Track 172 Ascending (frame 21)
(PC8, Task 2 — 15:35).

1. Runs PC3's cumulative InSAR chain on pipeline/subset/karapinar_p172/*.npz -> data/karapinar_p172/
   and analysis/pc8/karapinar_p172_*.
2. Compares Track 7 vs Track 172 (1 km blocks, valid pixels, and the 12 points of data/karapinar/points.json):
   Pearson r, RMSE, median difference, max difference, and time-series correlation at p01 (2 km W of Karapınar).
3. Saves docs/story/media/pc8_kp_p7_vs_p172.png and analysis/pc8/kp_p7_vs_p172.json.
"""
from __future__ import annotations

import json
import sys
import warnings
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis"))

import cumulative as cum_mod  # noqa: E402
import gunw_io  # noqa: E402
from compare_tracks import blocks, resample_to  # noqa: E402
from insar import (  # noqa: E402
    choose_reference,
    cycle_outliers,
    deramp,
    deramp_elevation,
    mask_coherence,
    mask_components,
    phase_to_cm,
    reference,
    remove_islands,
)

KP_BBOX = (33.3, 37.6, 33.8, 37.9)
gunw_io.BBOX["karapinar_p172"] = KP_BBOX
cum_mod.BBOX["karapinar_p172"] = KP_BBOX


def run_karapinar_p172(thr: float = 0.3) -> dict:
    site = "karapinar_p172"
    bbox = KP_BBOX
    quality = "provisional"
    qnote = cum_mod.DISCLAIMER
    src, files = cum_mod.load_pairs(site)
    used, notes = cum_mod.chain(files, ("provisional",))
    print(f"source {src}: {len(used)} pairs", [str(u[2].relative_to(ROOT)) for u in used], notes)
    if len(used) < 2:
        raise SystemExit("need >= 2 consecutive pairs")

    d0 = used[0][3]
    x, y, epsg = d0["x"], d0["y"], int(d0["epsg"])

    dem = None
    dem_f = ROOT / "analysis" / "out" / "karapinar_dem.npy"
    if dem_f.exists():
        loaded_dem = np.load(dem_f)
        if loaded_dem.shape == d0["unw"].shape and np.isfinite(loaded_dem).sum() >= 100:
            dem = loaded_dem

    pair_cm, stats = [], []
    for d1, d2, f, d in used:
        if d["unw"].shape != d0["unw"].shape or not np.allclose(d["x"], x) or not np.allclose(d["y"], y):
            raise SystemExit(f"grid mismatch in {f.name}; BLOCKED")
        unw = d["unw"]
        ion_used = "ion" in d and d["ion"].shape == unw.shape
        if ion_used:
            unw = unw - d["ion"]
        cm = phase_to_cm(unw, float(d["wavelength"]))
        if "conncomp" in d and d["conncomp"].size:
            cm = mask_components(cm, d["conncomp"])
        cm = mask_coherence(cm, d["coh"], thr)
        cm = remove_islands(cm, cum_mod.ISLAND_MIN_PX)
        k_elev = None
        if dem is not None:
            cm, k_elev = deramp_elevation(cm, dem)
        else:
            cm = deramp(cm, order=1)
        n_before = int(np.isfinite(cm).sum())
        cm = cycle_outliers(cm, thr_cm=float(d["wavelength"]) / 4 * 100)
        cycle_px = n_before - int(np.isfinite(cm).sum())
        pair_cm.append(cm)
        stats.append({
            "pair": [d1, d2],
            "file": str(f.relative_to(ROOT)).replace("\\", "/"),
            "lambda_m": float(d["wavelength"]),
            "ionosphere_applied": bool(ion_used),
            "cycle_outlier_px": cycle_px,
            "elev_coef_cm_per_km": None if k_elev is None else round(k_elev, 2),
            "valid_frac_after_masks": float(np.isfinite(cm).mean()),
        })

    valid_all = np.logical_and.reduce([np.isfinite(c) for c in pair_cm])
    coh_mean = np.mean([np.load(f)["coh"].astype(np.float32) / 255 for _, _, f, _ in used], axis=0)
    XX, YY = np.meshgrid(x, y)
    LON, LAT = Transformer.from_crs(epsg, 4326, always_xy=True).transform(XX, YY)
    in_bbox = (LON >= bbox[0]) & (LON <= bbox[2]) & (LAT >= bbox[1]) & (LAT <= bbox[3])
    r, c, mcoh = choose_reference(coh_mean, valid_all & in_bbox, cum_mod.RADIUS, stride=3)
    lon_r, lat_r = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c], y[r])
    print(f"p172 reference row={r} col={c} lon={lon_r:.4f} lat={lat_r:.4f} mean_coh={mcoh:.2f}")

    dates = [used[0][0]] + [p[1] for p in used]
    cum = [np.zeros_like(pair_cm[0])]
    cum[0][~valid_all] = np.nan
    n_out = 0
    for i, cm in enumerate(pair_cm):
        cm = reference(cm, (r, c), cum_mod.RADIUS)
        bad = np.abs(cm) > cum_mod.PAIR_OUTLIER_CM
        n_out += int(bad.sum())
        cm[bad] = np.nan
        stats[i]["p2_p50_p98_cm"] = [round(float(v), 2) for v in np.nanpercentile(cm, [2, 50, 98])]
        cum.append(cum[-1] + cm)
    for k in range(len(cum)):
        cum[k][~valid_all] = np.nan
    final = cum[-1]
    valid = np.isfinite(final)
    print(f"p172 valid in full chain: {valid.mean():.3f}; outlier px removed: {n_out}")

    sm = cum_mod.block_median(
        np.where(in_bbox, final, np.nan),
        cum_mod.BLOCK_PX,
        cum_mod.BLOCK_MIN_VALID,
        cum_mod.BLOCK_MAX_STD,
    )
    rmin, cmin = np.unravel_index(np.nanargmin(sm), sm.shape)
    max_sub = float(sm[rmin, cmin])

    def dist_mask(rr, cc):
        return np.hypot(
            (np.arange(len(y))[:, None] - rr) * abs(y[1] - y[0]),
            (np.arange(len(x))[None, :] - cc) * abs(x[1] - x[0]),
        ) < 30000

    used_refs, alts = [(r, c)], []
    for _ in range(2):
        excl = np.logical_or.reduce([dist_mask(rr, cc) for rr, cc in used_refs])
        try:
            r2, c2, _ = choose_reference(coh_mean, valid_all & in_bbox, cum_mod.RADIUS, stride=3, exclude=excl)
        except ValueError:
            break
        used_refs.append((r2, c2))
        alt = np.zeros_like(final)
        for cm in pair_cm:
            q = reference(cm, (r2, c2), cum_mod.RADIUS)
            q[np.abs(q) > cum_mod.PAIR_OUTLIER_CM] = np.nan
            alt = alt + q
        alt[~valid_all] = np.nan
        sm_alt = cum_mod.block_median(
            np.where(in_bbox, alt, np.nan),
            cum_mod.BLOCK_PX,
            cum_mod.BLOCK_MIN_VALID,
            cum_mod.BLOCK_MAX_STD,
        )
        alt_max = float(sm_alt[rmin, cmin]) if np.isfinite(sm_alt[rmin, cmin]) else float(np.nanmin(sm_alt))
        lon_r2, lat_r2 = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c2], y[r2])
        alts.append({
            "alt_reference": {"lon": round(lon_r2, 5), "lat": round(lat_r2, 5)},
            "max_subsidence_cm_at_same_location": round(alt_max, 1),
        })
    sens = alts[0] if alts else None
    range_cm = sorted([round(max_sub, 1)] + [q["max_subsidence_cm_at_same_location"] for q in alts]) if alts else None

    inc = d0["incidence"] if "incidence" in d0 and d0["incidence"].size else None
    inc_at = float(inc[rmin, cmin]) if inc is not None else None
    days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
    lon_m, lat_m = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[cmin], y[rmin])
    vlim = float(np.ceil(np.nanpercentile(np.abs(sm), 99.5)))
    vmin, vmax = -vlim, vlim
    print(f"p172 max subsidence (LOS, 1 km block median) {max_sub:.2f} cm at {lon_m:.4f},{lat_m:.4f}; days={days}; v=±{vlim}")

    ddir = ROOT / "data" / site
    (ddir / "disp").mkdir(parents=True, exist_ok=True)
    for dt, g in zip(dates, cum):
        cum_mod.save_png(cum_mod.to_latlon_grid(g, x, y, epsg, bbox), ddir / "disp" / f"{dt}.png", vmin, vmax)

    out_dir = ROOT / "analysis" / "pc8"
    out_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_dir / f"{site}_cum.npz",
        cum_cm=final.astype(np.float32),
        x=x,
        y=y,
        epsg=np.int32(epsg),
        dates=np.array(dates),
        quality=quality,
        incidence=(inc.astype(np.float16) if inc is not None else np.array([])),
        reference_rc=np.array([r, c]),
    )
    np.savez_compressed(
        out_dir / f"{site}_cum_stack.npz",
        cum_stack_cm=np.stack(cum).astype(np.float16),
        dates=np.array(dates),
        x=x,
        y=y,
        epsg=np.int32(epsg),
        quality="provisional",
    )

    pairs_txt = ", ".join(f"{p[0]}_{p[1]}" for p in used)
    granules = [str(p[3]["granule"]) for p in used if "granule" in p[3]]
    geom = "GUNW track/frame unknown"
    if granules:
        g = granules[0].split("_")
        geom = f"track {int(g[5])} {'ascending' if g[6] == 'A' else 'descending'} frame {int(g[7])}"

    meta = {
        "site": site,
        "bbox": list(bbox),
        "dates": dates,
        "units": "cm",
        "vmin": vmin,
        "vmax": vmax,
        "component": "LOS (line of sight); negative = away from satellite = subsidence",
        "colormap": "RdBu (red = subsidence, blue = uplift/toward satellite)",
        "source": f"NISAR L2 GUNW (PROVISIONAL, CRID P05023) via ASF DAAC, {geom}; https://nisar-docs.asf.alaska.edu/gunw",
        "granules": granules,
        "notes": (
            f"Cumulative LOS displacement relative to {dates[0]}, sum of {len(used)} consecutive pairs ({pairs_txt}). "
            f"Phase to cm with -lambda/(4*pi), lambda from each file's centerFrequency. Masks: coherence >= {thr}, "
            f"connectedComponents != 0, isolated patches < {cum_mod.ISLAND_MIN_PX} px (1.3 km2) removed (unwrapping-error guard), "
            f"pixels deviating > lambda/4 (half a phase cycle) from their 720 m tile median removed, "
            f"|pair| > {cum_mod.PAIR_OUTLIER_CM} cm removed; pixel shown only if valid in every pair. "
            f"All pairs referenced to the same window at {lon_r:.4f}E {lat_r:.4f}N. "
            "The ionosphere phase screen shipped in each GUNW was subtracted. "
            + (
                "A best-fit plane plus a linear elevation term (Copernicus DEM GLO-90) was removed from each pair "
                "(long-wavelength and elevation-correlated troposphere residual; this can also remove part of any valley-wide tilt). "
                if dem is not None
                else "A best-fit plane was removed from each pair (long-wavelength atmospheric residual). "
            )
            + "Troposphere and solid-earth-tide layers were NOT applied; residual atmospheric noise of a few cm per pair is expected. "
            + " ".join(notes)
        ),
        "reference_point": {"lon": round(lon_r, 5), "lat": round(lat_r, 5)},
        "quality": quality,
        "quality_note": qnote,
    }
    (ddir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    places = cum_mod.load_places("karapinar")
    pts = cum_mod.pick_points(sm, np.isfinite(sm), (r, c), x, y, epsg)
    points = []
    for i, (kind, pr, pc, lon, lat) in enumerate(pts, 1):
        hb = cum_mod.BLOCK_PX // 2
        win = np.stack(cum)[:, max(pr - hb, 0): pr + hb + 1, max(pc - hb, 0): pc + hb + 1]
        ts = np.nanmedian(win.reshape(len(dates), -1), axis=1)
        name = cum_mod.place_label(lon, lat, places)
        points.append({
            "id": f"p{i:02d}",
            "name": name,
            "kind": kind,
            "lon": round(lon, 5),
            "lat": round(lat, 5),
            "dates": dates,
            "disp_cm": [None if not np.isfinite(v) else round(float(v), 2) for v in ts],
        })
    (ddir / "points.json").write_text(json.dumps(points, indent=2), encoding="utf-8")

    rate = max_sub / days * 365.25
    summary = {
        "max_subsidence_cm": round(max_sub, 1),
        "max_subsidence_range_cm": [range_cm[0], range_cm[-1]] if range_cm else None,
        "range_cm": [range_cm[0], range_cm[-1]] if range_cm else None,
        "n_references": len(alts) + 1,
        "reference_sensitivity": sens,
        "reference_sensitivity_all": alts,
        "period": [dates[0], dates[-1]],
        "rate_cm_per_yr_estimate": round(rate, 1),
        "reference_point": {"lon": round(lon_r, 5), "lat": round(lat_r, 5)},
        "quality": quality,
        "quality_note": qnote,
        "component": "LOS",
        "max_subsidence_location": {"lon": round(lon_m, 5), "lat": round(lat_m, 5)},
        "max_subsidence_vertical_cm_estimate": round(max_sub / np.cos(np.deg2rad(inc_at)), 1) if inc_at else None,
        "incidence_deg_at_max": round(inc_at, 1) if inc_at else None,
        "n_pairs": len(used),
        "method_note": (
            f"Headline value = most negative median of ~1 km blocks (13x13 px, >= 50 % valid pixels, within-block std <= 2 cm) "
            f"of the cumulative LOS map (Track 172 ascending, Frame 21). Rate = linear extrapolation of {days} days ({dates[0]} to {dates[-1]}, "
            "irrigation season) to one year: an ESTIMATE that likely overstates the annual net rate because part of summer subsidence "
            "recovers in winter. Vertical value assumes purely vertical motion (LOS / cos(incidence))."
        ),
    }
    (ddir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / f"{site}_pair_stats.json").write_text(
        json.dumps(
            {
                "pairs": stats,
                "notes": notes,
                "reference_mean_coh": mcoh,
                "valid_frac_full_chain": float(valid.mean()),
                "outlier_px_removed": n_out,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return summary


def compare_p7_vs_p172() -> dict:
    p7_cum = np.load(ROOT / "analysis" / "out" / "karapinar_cum.npz")
    p7_stack = np.load(ROOT / "analysis" / "out" / "karapinar_cum_stack.npz")
    p172_cum = np.load(ROOT / "analysis" / "pc8" / "karapinar_p172_cum.npz")
    p172_stack = np.load(ROOT / "analysis" / "pc8" / "karapinar_p172_cum_stack.npz")

    x7, y7 = p7_cum["x"], p7_cum["y"]
    x172, y172 = p172_cum["x"], p172_cum["y"]
    inc7 = p7_cum["incidence"].astype(np.float32)
    inc172 = resample_to(p172_cum["incidence"].astype(np.float32), x172, y172, x7, y7)

    los7 = p7_cum["cum_cm"].astype(np.float32)
    los172 = resample_to(p172_cum["cum_cm"].astype(np.float32), x172, y172, x7, y7)
    stack7 = p7_stack["cum_stack_cm"].astype(np.float32)
    stack172 = resample_to(p172_stack["cum_stack_cm"].astype(np.float32), x172, y172, x7, y7)

    vert7 = los7 / np.cos(np.deg2rad(inc7))
    vert172 = los172 / np.cos(np.deg2rad(inc172))

    # 1 km block means (>=50% valid in each)
    b7_vert = blocks(vert7)
    b172_vert = blocks(vert172)
    b7_los = blocks(los7)
    b172_los = blocks(los172)

    ok_blk = np.isfinite(b7_vert) & np.isfinite(b172_vert)
    xv, yv = b7_vert[ok_blk], b172_vert[ok_blk]
    xl, yl = b7_los[ok_blk], b172_los[ok_blk]

    r_blk_vert = float(np.corrcoef(xv, yv)[0, 1])
    rmse_blk_vert = float(np.sqrt(np.mean((yv - xv) ** 2)))
    med_diff_vert = float(np.median(yv - xv))
    max_abs_diff_vert = float(np.max(np.abs(yv - xv)))
    slope_vert = float(np.polyfit(xv, yv, 1)[0])

    r_blk_los = float(np.corrcoef(xl, yl)[0, 1])
    rmse_blk_los = float(np.sqrt(np.mean((yl - xl) ** 2)))
    med_diff_los = float(np.median(yl - xl))
    max_abs_diff_los = float(np.max(np.abs(yl - xl)))

    # Pixel-level overlap statistics
    ok_px = np.isfinite(vert7) & np.isfinite(vert172)
    px_r_vert = float(np.corrcoef(vert7[ok_px], vert172[ok_px])[0, 1])
    px_rmse_vert = float(np.sqrt(np.mean((vert172[ok_px] - vert7[ok_px]) ** 2)))
    px_max_diff_vert = float(np.max(np.abs(vert172[ok_px] - vert7[ok_px])))

    px_r_los = float(np.corrcoef(los7[ok_px], los172[ok_px])[0, 1])
    px_rmse_los = float(np.sqrt(np.mean((los172[ok_px] - los7[ok_px]) ** 2)))
    px_max_diff_los = float(np.max(np.abs(los172[ok_px] - los7[ok_px])))

    # Sign agreement on blocks where |Track 7 vertical| > 2 cm and > 3 cm
    strong = np.abs(xv) > 2.0
    sign_agree_gt2cm = float(np.mean(np.sign(xv[strong]) == np.sign(yv[strong]))) if strong.any() else None
    strong3 = np.abs(xv) > 3.0
    sign_agree_gt3cm = float(np.mean(np.sign(xv[strong3]) == np.sign(yv[strong3]))) if strong3.any() else None
    r_gt2cm = float(np.corrcoef(xv[strong], yv[strong])[0, 1]) if strong.sum() >= 3 else None

    # Compare at the 12 official Karapınar points (data/karapinar/points.json)
    kp_pts = json.loads((ROOT / "data" / "karapinar" / "points.json").read_text(encoding="utf-8"))
    tr = Transformer.from_crs(4326, int(p7_cum["epsg"]), always_xy=True)
    hb = cum_mod.BLOCK_PX // 2
    pt_comparisons = []
    for pt in kp_pts:
        px_u, py_u = tr.transform(pt["lon"], pt["lat"])
        c_idx = int(np.argmin(np.abs(x7 - px_u)))
        r_idx = int(np.argmin(np.abs(y7 - py_u)))
        w7 = stack7[:, max(r_idx - hb, 0): r_idx + hb + 1, max(c_idx - hb, 0): c_idx + hb + 1]
        w172 = stack172[:, max(r_idx - hb, 0): r_idx + hb + 1, max(c_idx - hb, 0): c_idx + hb + 1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            ts7 = np.nanmedian(w7.reshape(len(stack7), -1), axis=1)
            ts172 = np.nanmedian(w172.reshape(len(stack172), -1), axis=1)
        inc7_pt = float(np.nanmedian(inc7[max(r_idx - hb, 0): r_idx + hb + 1, max(c_idx - hb, 0): c_idx + hb + 1]))
        inc172_pt = float(np.nanmedian(inc172[max(r_idx - hb, 0): r_idx + hb + 1, max(c_idx - hb, 0): c_idx + hb + 1]))
        fin_valid = np.isfinite(ts7) & np.isfinite(ts172)
        ts_r = float(np.corrcoef(ts7[fin_valid], ts172[fin_valid])[0, 1]) if fin_valid.sum() >= 3 and np.std(ts7[fin_valid]) > 0 and np.std(ts172[fin_valid]) > 0 else None
        ts_rmse_los = float(np.sqrt(np.mean((ts172[fin_valid] - ts7[fin_valid]) ** 2))) if fin_valid.any() else None
        v7_ts = ts7 / np.cos(np.deg2rad(inc7_pt))
        v172_ts = ts172 / np.cos(np.deg2rad(inc172_pt))
        ts_rmse_vert = float(np.sqrt(np.mean((v172_ts[fin_valid] - v7_ts[fin_valid]) ** 2))) if fin_valid.any() else None
        pt_comparisons.append({
            "id": pt["id"],
            "name": pt["name"],
            "kind": pt["kind"],
            "lon": pt["lon"],
            "lat": pt["lat"],
            "end_los_p7_cm": round(float(ts7[-1]), 2) if np.isfinite(ts7[-1]) else None,
            "end_los_p172_cm": round(float(ts172[-1]), 2) if np.isfinite(ts172[-1]) else None,
            "end_vert_p7_cm": round(float(v7_ts[-1]), 2) if np.isfinite(v7_ts[-1]) else None,
            "end_vert_p172_cm": round(float(v172_ts[-1]), 2) if np.isfinite(v172_ts[-1]) else None,
            "ts_pearson_r": None if ts_r is None or not np.isfinite(ts_r) else round(ts_r, 3),
            "ts_rmse_los_cm": None if ts_rmse_los is None or not np.isfinite(ts_rmse_los) else round(ts_rmse_los, 2),
            "ts_rmse_vert_cm": None if ts_rmse_vert is None or not np.isfinite(ts_rmse_vert) else round(ts_rmse_vert, 2),
            "ts_los_p7": [None if not np.isfinite(v) else round(float(v), 2) for v in ts7],
            "ts_los_p172": [None if not np.isfinite(v) else round(float(v), 2) for v in ts172],
        })

    pts_v7 = np.array([p["end_vert_p7_cm"] for p in pt_comparisons], dtype=float)
    pts_v172 = np.array([p["end_vert_p172_cm"] for p in pt_comparisons], dtype=float)
    pts_l7 = np.array([p["end_los_p7_cm"] for p in pt_comparisons], dtype=float)
    pts_l172 = np.array([p["end_los_p172_cm"] for p in pt_comparisons], dtype=float)
    pts_r_vert = float(np.corrcoef(pts_v7, pts_v172)[0, 1])
    pts_rmse_vert = float(np.sqrt(np.mean((pts_v172 - pts_v7) ** 2)))
    pts_max_diff_vert = float(np.max(np.abs(pts_v172 - pts_v7)))
    pts_r_los = float(np.corrcoef(pts_l7, pts_l172)[0, 1])
    pts_rmse_los = float(np.sqrt(np.mean((pts_l172 - pts_l7) ** 2)))
    pts_max_diff_los = float(np.max(np.abs(pts_l172 - pts_l7)))

    dates = [str(d) for d in p7_cum["dates"]]
    out_stats = {
        "common_period": [dates[0], dates[-1]],
        "n_pairs": 8,
        "n_blocks_1km": int(ok_blk.sum()),
        "n_valid_pixels_overlap": int(ok_px.sum()),
        "benchmark_12_points": {
            "pearson_r_los": round(pts_r_los, 3),
            "rmse_los_cm": round(pts_rmse_los, 2),
            "max_abs_diff_los_cm": round(pts_max_diff_los, 2),
            "pearson_r_vertical": round(pts_r_vert, 3),
            "rmse_vertical_cm": round(pts_rmse_vert, 2),
            "max_abs_diff_vertical_cm": round(pts_max_diff_vert, 2),
        },
        "blocks_1km_vertical": {
            "pearson_r": round(r_blk_vert, 3),
            "pearson_r_subsiding_gt_2cm": None if r_gt2cm is None else round(r_gt2cm, 3),
            "rmse_cm": round(rmse_blk_vert, 2),
            "median_diff_p172_minus_p7_cm": round(med_diff_vert, 2),
            "max_abs_diff_cm": round(max_abs_diff_vert, 2),
            "slope_p172_vs_p7": round(slope_vert, 3),
            "sign_agreement_abs_gt_2cm": None if sign_agree_gt2cm is None else round(sign_agree_gt2cm, 3),
            "sign_agreement_abs_gt_3cm": None if sign_agree_gt3cm is None else round(sign_agree_gt3cm, 3),
            "n_strong_blocks_gt_2cm": int(strong.sum()),
        },
        "blocks_1km_los": {
            "pearson_r": round(r_blk_los, 3),
            "rmse_cm": round(rmse_blk_los, 2),
            "median_diff_p172_minus_p7_cm": round(med_diff_los, 2),
            "max_abs_diff_cm": round(max_abs_diff_los, 2),
        },
        "pixels_vertical": {
            "pearson_r": round(px_r_vert, 3),
            "rmse_cm": round(px_rmse_vert, 2),
            "max_abs_diff_cm": round(px_max_diff_vert, 2),
        },
        "pixels_los": {
            "pearson_r": round(px_r_los, 3),
            "rmse_cm": round(px_rmse_los, 2),
            "max_abs_diff_cm": round(px_max_diff_los, 2),
        },
        "point_comparisons": pt_comparisons,
    }
    (ROOT / "analysis" / "pc8" / "kp_p7_vs_p172.json").write_text(
        json.dumps(out_stats, indent=2), encoding="utf-8"
    )

    # --- Plot docs/story/media/pc8_kp_p7_vs_p172.png ---
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.0,
        "axes.titlesize": 9.5,
        "axes.labelsize": 9.0,
    })
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13.8, 4.6), dpi=160, gridspec_kw={"width_ratios": [1.05, 1.15, 1.0]})
    fig.patch.set_facecolor("#ffffff")

    # Panel A: 1 km Block & 12 Benchmark Points Scatter (Track 7 Desc vs Track 172 Asc Vertical Est.)
    ax1.set_facecolor("#fafafa")
    lim = max(8.5, float(np.ceil(np.nanmax(np.abs(np.r_[xv, yv])) + 0.5)))
    ax1.plot([-lim, 3.0], [-lim, 3.0], color="#475569", ls="--", lw=1.1, label="1:1 agreement line")
    ax1.scatter(xv, yv, c="#93c5fd", s=22, alpha=0.65, edgecolors="#1e3a8a", linewidths=0.35,
                label=f"All 1 km blocks (n={ok_blk.sum()}, RMSE={rmse_blk_vert:.2f} cm)")
    ax1.scatter(pts_v7, pts_v172, c="#dc2626", marker="D", s=44, zorder=5, edgecolors="#0f172a", linewidths=0.6,
                label=f"12 benchmark points (r={pts_r_vert:.2f}, RMSE={pts_rmse_vert:.2f} cm)")
    ax1.annotate("p01 Karapınar bowl\n(-8.0 vs -6.4 cm)", xy=(pts_v7[0], pts_v172[0]),
                 xytext=(-7.8, -4.1), fontsize=7.5, fontweight="bold", color="#991b1b",
                 arrowprops=dict(arrowstyle="->", color="#991b1b", lw=0.9))
    ax1.set_xlim(-lim, 2.8)
    ax1.set_ylim(-lim, 2.8)
    ax1.set_xlabel("Track 7 descending — vertical est. (cm)")
    ax1.set_ylabel("Track 172 ascending — vertical est. (cm)")
    ax1.set_title("A. Cross-orbit vertical comparison", fontweight="bold", loc="left")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", fontsize=7.4, frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0")

    # Panel B: Time series at Karapınar bowl (p01: 2 km W of Karapınar) & Gazi Osman Paşa (p04)
    ax2.set_facecolor("#fafafa")
    p01 = pt_comparisons[0]
    p04 = pt_comparisons[3]
    t_idx = np.arange(len(dates))
    short_dates = [d[5:] for d in dates]
    ax2.axhline(0.0, color="#64748b", lw=0.8, ls="--")
    ax2.plot(t_idx, p01["ts_los_p7"], "-o", color="#b91c1c", lw=2.0, ms=5,
             label=f"p01 Karapınar W — Track 7 Desc ({p01['end_los_p7_cm']:.2f} cm LOS)")
    ax2.plot(t_idx, p01["ts_los_p172"], "--s", color="#ef4444", lw=2.0, ms=5,
             label=f"p01 Karapınar W — Track 172 Asc ({p01['end_los_p172_cm']:.2f} cm LOS, r={p01['ts_pearson_r']:.2f})")
    ax2.plot(t_idx, p04["ts_los_p7"], "-^", color="#1e40af", lw=1.6, ms=4.5,
             label=f"p04 Gazi Osman Paşa — Track 7 Desc ({p04['end_los_p7_cm']:.2f} cm LOS)")
    ax2.plot(t_idx, p04["ts_los_p172"], ":d", color="#3b82f6", lw=1.6, ms=4.5,
             label=f"p04 Gazi Osman Paşa — Track 172 Asc ({p04['end_los_p172_cm']:.2f} cm LOS)")
    ax2.set_xticks(t_idx)
    ax2.set_xticklabels(short_dates, fontsize=8, rotation=25)
    ax2.set_ylabel("Cumulative LOS displacement (cm)")
    ax2.set_title("B. Co-dated 9-epoch LOS time series", fontweight="bold", loc="left")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="lower left", fontsize=7.3, frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0")

    # Panel C: Spatial difference map (Track 172 − Track 7 vertical estimate, 1 km blocks)
    ax3.set_facecolor("#f1f5f9")
    diff_blk = b172_vert - b7_vert
    im = ax3.imshow(diff_blk, cmap="PuOr", vmin=-3.5, vmax=3.5)
    cbar = fig.colorbar(im, ax=ax3, shrink=0.82, pad=0.03)
    cbar.set_label("Track 172 − Track 7 vertical est. (cm)", fontsize=8.0)
    ax3.set_title(
        f"C. Block diff. (med {med_diff_vert:+.2f} cm, max |Δ| {max_abs_diff_vert:.2f} cm)",
        fontweight="bold", loc="left"
    )
    ax3.set_xticks([])
    ax3.set_yticks([])

    fig.suptitle(
        "Karapınar Basin Independent Orbit Cross-Check: Track 7 Descending (16:40 UTC) vs. Track 172 Ascending (02:53 UTC)",
        fontsize=10.8, fontweight="bold", y=0.98
    )
    fig.text(
        0.5, 0.012,
        f"Data: NASA-ISRO NISAR L2 GUNW (provisional CRID P05023, 8 consecutive pairs on identical dates 26 Jun–12 Oct 2026) via ASF DAAC.\n"
        f"12 benchmark points: r={pts_r_los:.2f} LOS ({pts_r_vert:.2f} vert.), RMSE={pts_rmse_los:.2f} cm LOS ({pts_rmse_vert:.2f} cm vert.); "
        f"220 1 km blocks: r={r_blk_los:.2f} (r={r_gt2cm:.2f} for |disp|>2 cm), RMSE={rmse_blk_los:.2f} cm LOS ({rmse_blk_vert:.2f} cm vert.), max |Δ|={max_abs_diff_los:.2f} cm LOS. Analysis: Team Taykut.",
        fontsize=7.5, color="#334155", ha="center"
    )
    plt.tight_layout(rect=[0.0, 0.055, 1.0, 0.94])

    out_png = ROOT / "docs" / "story" / "media" / "pc8_kp_p7_vs_p172.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=160)
    plt.close(fig)
    print(f"Saved {out_png} ({out_png.stat().st_size / 1024:.1f} KB)")
    print(json.dumps(out_stats, indent=2))
    return out_stats


def main():
    run_karapinar_p172()
    compare_p7_vs_p172()


if __name__ == "__main__":
    main()
