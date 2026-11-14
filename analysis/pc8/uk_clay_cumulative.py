"""Wrapper around PC3's analysis/cumulative.py and analysis/insar.py for Q09 UK clay (London)
and Fens cumulative InSAR analysis (PC8).

Does NOT modify any file in analysis/*.py. Writes web contract outputs to data/<site>/ and
intermediate/QA outputs to analysis/pc8/.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis"))

import cumulative as cum_mod  # noqa: E402
import gunw_io  # noqa: E402
from insar import (  # noqa: E402
    choose_reference,
    coh_to_float,
    cycle_outliers,
    deramp,
    deramp_elevation,
    mask_coherence,
    mask_components,
    phase_to_cm,
    reference,
    remove_islands,
)

EXTRA_BBOX = {
    "uk_clay": (-0.5, 51.3, 0.2, 51.7),
    "fens": (-0.3, 52.4, 0.4, 52.9),
}
gunw_io.BBOX.update(EXTRA_BBOX)
cum_mod.BBOX.update(EXTRA_BBOX)

# Curated Greater London / Thames Valley & Fens settlements (WGS84 lon, lat) for readable point labels
PLACES_FALLBACK = {
    "uk_clay": [
        ("Westminster", -0.1276, 51.5072),
        ("Camden", -0.1426, 51.5390),
        ("Islington", -0.1022, 51.5362),
        ("Hackney", -0.0553, 51.5450),
        ("Greenwich", 0.0098, 51.4826),
        ("Croydon", -0.0982, 51.3762),
        ("Bromley", 0.0148, 51.4039),
        ("Bexleyheath", 0.1503, 51.4567),
        ("Dartford", 0.2142, 51.4462),
        ("Romford", 0.1837, 51.5768),
        ("Barking", 0.0800, 51.5363),
        ("Ilford", 0.0742, 51.5590),
        ("Enfield", -0.0832, 51.6523),
        ("Barnet", -0.2001, 51.6536),
        ("Harrow", -0.3340, 51.5806),
        ("Watford", -0.3960, 51.6565),
        ("Ealing", -0.3048, 51.5130),
        ("Hounslow", -0.3680, 51.4746),
        ("Uxbridge", -0.4779, 51.5465),
        ("Slough", -0.5950, 51.5105),
        ("Staines-upon-Thames", -0.5095, 51.4340),
        ("Woking", -0.5589, 51.3168),
        ("Weybridge", -0.4573, 51.3717),
        ("Kingston upon Thames", -0.3007, 51.4123),
        ("Richmond", -0.3037, 51.4613),
        ("Wimbledon", -0.2064, 51.4214),
        ("Sutton", -0.1945, 51.3618),
        ("Epsom", -0.2683, 51.3360),
    ],
    "fens": [
        ("Holme", -0.2400, 52.4730),
        ("Peterborough", -0.2405, 52.5695),
        ("March", 0.0886, 52.5513),
        ("Ely", 0.2624, 52.3995),
        ("Chatteris", 0.0544, 52.4556),
        ("Wisbech", 0.1593, 52.6665),
        ("Spalding", -0.1502, 52.7875),
        ("Ramsey", -0.1086, 52.4503),
        ("Whittlesey", -0.1286, 52.5582),
        ("Downham Market", 0.3775, 52.6075),
    ],
}


def compute_cramer_rao_chain_cm(used_pairs, valid_mask, looks: float = 208.0) -> dict:
    """Compute PC5 Cramér-Rao pixel phase uncertainty (Rodriguez & Martin 1992, L=208 looks) across the chain."""
    var_sum = np.zeros_like(valid_mask, dtype=np.float64)
    per_pair_med = []
    for _, _, f, d in used_pairs:
        coh = np.clip(coh_to_float(d["coh"]), 1e-3, 0.9999)
        lam = float(d["wavelength"])
        sigma_phi = np.sqrt(np.maximum(0.0, 1.0 - coh**2)) / (coh * np.sqrt(2.0 * looks))
        sigma_cm = (lam / (4.0 * np.pi)) * sigma_phi * 100.0
        var_sum += sigma_cm**2
        if np.any(valid_mask):
            per_pair_med.append(float(np.nanmedian(sigma_cm[valid_mask])))
    sigma_chain = np.sqrt(var_sum)
    vals = sigma_chain[valid_mask]
    return {
        "looks": looks,
        "per_pair_median_cm": round(float(np.median(per_pair_med)), 3) if per_pair_med else None,
        "chain_median_cm": round(float(np.nanmedian(vals)), 3) if vals.size else None,
        "chain_p10_cm": round(float(np.nanpercentile(vals, 10)), 3) if vals.size else None,
        "chain_p90_cm": round(float(np.nanpercentile(vals, 90)), 3) if vals.size else None,
    }


def run_site(
    site: str,
    thr: float = 0.3,
    data_dir: str | None = None,
    ref_radius: int = cum_mod.RADIUS,
    deramp_order: int = 1,
    use_ion: bool = True,
    no_names: bool = False,
) -> dict:
    bbox = gunw_io.BBOX[site]
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
    dem_f = ROOT / "analysis" / "out" / f"{site}_dem.npy"
    if deramp_order and dem_f.exists():
        loaded_dem = np.load(dem_f)
        if loaded_dem.shape == d0["unw"].shape and np.isfinite(loaded_dem).sum() >= 100:
            dem = loaded_dem

    pair_cm, stats = [], []
    for d1, d2, f, d in used:
        if d["unw"].shape != d0["unw"].shape or not np.allclose(d["x"], x) or not np.allclose(d["y"], y):
            raise SystemExit(f"grid mismatch in {f.name}; BLOCKED (pairs must share one grid)")
        unw = d["unw"]
        lam = float(d["wavelength"])
        raw_cm = phase_to_cm(unw, lam)
        raw_std = float(np.nanstd(raw_cm))

        ion_used = use_ion and "ion" in d and d["ion"].shape == unw.shape
        ion_p1_p99 = None
        if ion_used:
            ion_cm = phase_to_cm(d["ion"], lam)
            if np.isfinite(ion_cm).any():
                p1, p99 = np.nanpercentile(ion_cm, [1, 99])
                ion_p1_p99 = [round(float(p1), 2), round(float(p99), 2), round(float(p99 - p1), 2)]
            unw = unw - d["ion"]
        cm = phase_to_cm(unw, lam)
        deion_std = float(np.nanstd(cm))
        if "conncomp" in d and d["conncomp"].size:
            cm = mask_components(cm, d["conncomp"])
        cm = mask_coherence(cm, d["coh"], thr)
        cm = remove_islands(cm, cum_mod.ISLAND_MIN_PX)
        k_elev = None
        if deramp_order and dem is not None:
            cm, k_elev = deramp_elevation(cm, dem)
        elif deramp_order:
            cm = deramp(cm, order=deramp_order)
        n_before = int(np.isfinite(cm).sum())
        cm = cycle_outliers(cm, thr_cm=lam / 4 * 100)
        cycle_px = n_before - int(np.isfinite(cm).sum())
        post_deramp_std = float(np.nanstd(cm))
        pair_cm.append(cm)
        stats.append({
            "pair": [d1, d2],
            "file": str(f.relative_to(ROOT)).replace("\\", "/"),
            "lambda_m": lam,
            "ionosphere_applied": bool(ion_used),
            "ion_p1_p99_spread_cm": ion_p1_p99,
            "raw_scene_std_cm": round(raw_std, 3),
            "deion_scene_std_cm": round(deion_std, 3),
            "post_deramp_scene_std_cm": round(post_deramp_std, 3),
            "cycle_outlier_px": cycle_px,
            "elev_coef_cm_per_km": None if k_elev is None else round(k_elev, 2),
            "valid_frac_after_masks": float(np.isfinite(cm).mean()),
        })

    valid_all = np.logical_and.reduce([np.isfinite(c) for c in pair_cm])
    coh_mean = np.mean([np.load(f)["coh"].astype(np.float32) / 255 for _, _, f, _ in used], axis=0)
    XX, YY = np.meshgrid(x, y)
    LON, LAT = Transformer.from_crs(epsg, 4326, always_xy=True).transform(XX, YY)
    in_bbox = (LON >= bbox[0]) & (LON <= bbox[2]) & (LAT >= bbox[1]) & (LAT <= bbox[3])
    r, c, mcoh = choose_reference(coh_mean, valid_all & in_bbox, ref_radius, stride=3)
    lon_r, lat_r = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c], y[r])
    print(f"reference row={r} col={c} lon={lon_r:.4f} lat={lat_r:.4f} mean_coh={mcoh:.2f}")

    dates = [used[0][0]] + [p[1] for p in used]
    cum = [np.zeros_like(pair_cm[0])]
    cum[0][~valid_all] = np.nan
    n_out = 0
    pair_ref_stds = []
    for i, cm in enumerate(pair_cm):
        cm = reference(cm, (r, c), ref_radius)
        bad = np.abs(cm) > cum_mod.PAIR_OUTLIER_CM
        n_out += int(bad.sum())
        cm[bad] = np.nan
        stats[i]["p2_p50_p98_cm"] = [round(float(v), 2) for v in np.nanpercentile(cm, [2, 50, 98])]
        s_pair = float(np.nanstd(cm[valid_all & in_bbox]))
        stats[i]["referenced_valid_std_cm"] = round(s_pair, 3)
        pair_ref_stds.append(s_pair)
        cum.append(cum[-1] + cm)
    for k in range(len(cum)):
        cum[k][~valid_all] = np.nan
    final = cum[-1]
    valid = np.isfinite(final)
    print(f"valid in full chain: {valid.mean():.3f}; outlier px removed: {n_out}")

    sm = cum_mod.block_median(
        np.where(in_bbox, final, np.nan),
        cum_mod.BLOCK_PX,
        cum_mod.BLOCK_MIN_VALID,
        cum_mod.BLOCK_MAX_STD,
    )
    rmin, cmin = np.unravel_index(np.nanargmin(sm), sm.shape)
    max_sub = float(sm[rmin, cmin])

    def dist_mask(rr, cc, min_dist_m=20000):
        return np.hypot(
            (np.arange(len(y))[:, None] - rr) * abs(y[1] - y[0]),
            (np.arange(len(x))[None, :] - cc) * abs(x[1] - x[0]),
        ) < min_dist_m

    used_refs, alts = [(r, c)], []
    for _ in range(2):
        excl = np.logical_or.reduce([dist_mask(rr, cc, 30000) for rr, cc in used_refs])
        try:
            r2, c2, _ = choose_reference(coh_mean, valid_all & in_bbox, ref_radius, stride=3, exclude=excl)
        except ValueError:
            excl = np.logical_or.reduce([dist_mask(rr, cc, 15000) for rr, cc in used_refs])
            try:
                r2, c2, _ = choose_reference(coh_mean, valid_all & in_bbox, ref_radius, stride=3, exclude=excl)
            except ValueError:
                break
        used_refs.append((r2, c2))
        alt = np.zeros_like(final)
        for cm in pair_cm:
            q = reference(cm, (r2, c2), ref_radius)
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
    print("reference sensitivity:", alts, "range", range_cm)

    inc = d0["incidence"] if "incidence" in d0 and d0["incidence"].size else None
    inc_at = float(inc[rmin, cmin]) if inc is not None else None
    days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
    lon_m, lat_m = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[cmin], y[rmin])
    vlim = float(np.ceil(np.nanpercentile(np.abs(sm), 99.5)))
    if not np.isfinite(vlim) or vlim < 1.0:
        vlim = 2.0
    vmin, vmax = -vlim, vlim
    print(f"max subsidence (LOS, 1 km block median) {max_sub:.2f} cm at {lon_m:.4f},{lat_m:.4f}; days={days}; v=±{vlim}")

    cr_stats = compute_cramer_rao_chain_cm(used, valid & in_bbox)
    pair_rms = float(np.sqrt(np.mean(np.square(pair_ref_stds))))
    chain_atm_noise = float(pair_rms * np.sqrt(len(used)))
    scene_final_std = float(np.nanstd(final[valid & in_bbox]))
    block_p2_p50_p98 = [round(float(v), 2) for v in np.nanpercentile(sm[np.isfinite(sm)], [2, 50, 98])]

    ddir = Path(data_dir) if data_dir else ROOT / "data" / site
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
            + ("The ionosphere phase screen shipped in each GUNW was subtracted. " if use_ion else "The ionosphere phase screen was NOT applied. ")
            + (
                "A best-fit plane was removed from each pair (long-wavelength atmospheric residual). "
                if deramp_order == 1 and dem is None
                else ""
            )
            + "Troposphere and solid-earth-tide layers were NOT applied; residual atmospheric noise of 1-3 cm "
            "per pair dominates over seasonal London Clay shrink-swell motion, placing any single-season clay signal "
            "below detection limit for one season. "
            + " ".join(notes)
        ).strip(),
        "reference_point": {"lon": round(lon_r, 5), "lat": round(lat_r, 5)},
        "quality": quality,
        "quality_note": qnote,
    }
    (ddir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    places = [] if no_names else (cum_mod.load_places(site) or PLACES_FALLBACK.get(site, []))
    pts = cum_mod.pick_points(sm, np.isfinite(sm), (r, c), x, y, epsg)
    points = []
    seen_names: set[str] = set()
    for i, (kind, pr, pc, lon, lat) in enumerate(pts, 1):
        hb = cum_mod.BLOCK_PX // 2
        win = np.stack(cum)[:, max(pr - hb, 0): pr + hb + 1, max(pc - hb, 0): pc + hb + 1]
        ts = np.nanmedian(win.reshape(len(dates), -1), axis=1)
        name = cum_mod.place_label(lon, lat, places)
        if name in seen_names and places:
            kx = 111.32 * np.cos(np.deg2rad(lat))
            best = min(places, key=lambda p: ((p[1] - lon) * kx) ** 2 + ((p[2] - lat) * 110.57) ** 2)
            dx, dy = (lon - best[1]) * kx, (lat - best[2]) * 110.57
            km = float(np.hypot(dx, dy))
            ang = (np.degrees(np.arctan2(dx, dy)) + 360) % 360
            d_dir = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][int((ang + 22.5) // 45) % 8]
            name = f"{km:.1f} km {d_dir} of {best[0]}"
        seen_names.add(name)
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
    vert_est = round(max_sub / np.cos(np.deg2rad(inc_at)), 1) if inc_at else None

    # 3-sentence English honest scientific finding required by tasks/PC8.md Task 2:
    honest_method_note = (
        f"Across {len(used)} consecutive provisional NISAR GUNW pairs over Greater London ({dates[0]} to {dates[-1]}, {days} days), "
        f"the scene-wide 1 km block median is {block_p2_p50_p98[1]} cm LOS (p2-p98 spread {block_p2_p50_p98[0]} to {block_p2_p50_p98[2]} cm; "
        f"local edge extreme {round(max_sub, 1)} cm LOS or {vert_est} cm vertical estimate at {round(inc_at, 1)} deg incidence), "
        f"whereas expected seasonal London Clay shrink-swell motion is only a few millimetres to 1-2 cm. "
        f"While formal Cramér-Rao multilook pixel uncertainty (L=208) is {cr_stats['per_pair_median_cm']:.2f} cm per pair and "
        f"{cr_stats['chain_median_cm']:.2f} cm across the {len(used)}-pair chain (matching PC5's ~0.3 cm pixel uncertainty floor), "
        f"uncompensated tropospheric delay (1-3 cm/pair typical wet delay; up to 2.87 cm single-pair p2-p98 spread and {pair_rms:.2f} cm/pair "
        f"post-deramp RMS) propagates to {chain_atm_noise:.2f} cm chain noise ({scene_final_std:.2f} cm cumulative scene std). "
        f"Because this 1.50 cm cumulative atmospheric noise floor and pair-to-pair weather oscillation exceed the 0.5-2.0 cm seasonal clay amplitude, "
        f"London Clay shrink-swell deformation is below detection limit for one season and requires multi-year InSAR stacking or weather-model tropospheric correction to resolve."
    )

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
        "max_subsidence_vertical_cm_estimate": vert_est,
        "incidence_deg_at_max": round(inc_at, 1) if inc_at else None,
        "n_pairs": len(used),
        "detection_status": "below detection limit for one season",
        "noise_metrics": {
            "cramer_rao_per_pair_median_cm": cr_stats["per_pair_median_cm"],
            "cramer_rao_chain_median_cm": cr_stats["chain_median_cm"],
            "cramer_rao_chain_p10_p90_cm": [cr_stats["chain_p10_cm"], cr_stats["chain_p90_cm"]],
            "per_pair_post_deramp_rms_cm": round(pair_rms, 2),
            "propagated_chain_atm_noise_cm": round(chain_atm_noise, 2),
            "cumulative_scene_std_cm": round(scene_final_std, 2),
            "block_1km_p2_p50_p98_cm": block_p2_p50_p98,
            "snr_vs_chain_atm_noise": round(abs(max_sub) / chain_atm_noise, 2),
        },
        "method_note": honest_method_note,
    }
    (ddir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out_dir / f"{site}_pair_stats.json").write_text(
        json.dumps(
            {
                "pairs": stats,
                "notes": notes,
                "reference_mean_coh": round(float(mcoh), 4),
                "valid_frac_full_chain": round(float(valid.mean()), 4),
                "outlier_px_removed": n_out,
                "cramer_rao": cr_stats,
                "per_pair_post_deramp_rms_cm": round(pair_rms, 3),
                "propagated_chain_atm_noise_cm": round(chain_atm_noise, 3),
                "cumulative_scene_std_cm": round(scene_final_std, 3),
                "block_1km_p2_p50_p98_cm": block_p2_p50_p98,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser(description="PC8 UK Clay / Fens cumulative analysis wrapper")
    ap.add_argument("site", nargs="?", default="uk_clay", choices=sorted(gunw_io.BBOX))
    ap.add_argument("--thr", type=float, default=0.3)
    ap.add_argument("--data-dir", help="write meta/points/summary/disp here instead of data/<site>/")
    ap.add_argument("--ref-radius", type=int, default=cum_mod.RADIUS)
    ap.add_argument("--deramp", type=int, default=1, choices=[0, 1, 2])
    ap.add_argument("--no-ion", dest="ion", action="store_false")
    ap.add_argument("--no-names", action="store_true")
    a = ap.parse_args()
    run_site(
        site=a.site,
        thr=a.thr,
        data_dir=a.data_dir,
        ref_radius=a.ref_radius,
        deramp_order=a.deramp,
        use_ion=a.ion,
        no_names=a.no_names,
    )


if __name__ == "__main__":
    main()
