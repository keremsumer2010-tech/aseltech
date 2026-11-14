"""Cumulative LOS displacement from a chain of consecutive GUNW pairs (PC3, Task 2).

Usage: python analysis/cumulative.py central_valley [--thr 0.3]

Input (first non-empty wins): pipeline/subset/<site>/*.npz (PC2)  ->  analysis/out/subset/<site>/*.npz (PC3 backup)
Steps per pair (analysis/insar.py): phase -> cm (-lambda/4pi, lambda from file) -> connComp/coherence mask
-> outlier mask -> referenced to ONE common window -> summed along the chain.
Only `provisional` pairs, only a gap-free chain (rules/VERI_SOZLESMESI.md section 3).
Outputs follow rules/VERI_SOZLESMESI.md section 4 (data/<site>/..., analysis/out/<site>_cum.npz).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer

sys.path.insert(0, str(Path(__file__).parent))
from gunw_io import BBOX  # noqa: E402
from insar import choose_reference, cycle_outliers, deramp, deramp_elevation, remove_islands, mask_coherence, mask_components, phase_to_cm, reference  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RADIUS = 3
BLOCK_PX, BLOCK_MIN_VALID, BLOCK_MAX_STD = 13, 0.5, 2.0  # ~1 km blocks for headline numbers and points
ISLAND_MIN_PX = 200  # 200 px * 80 m * 80 m = 1.28 km^2
PAIR_OUTLIER_CM = 15.0  # |per-pair LOS| above this in a 12-24 day pair = unwrapping error (documented)
CMAP = "RdBu"
DISCLAIMER = ("NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
              "(NASA-JPL and ISRO), not by our team.")


def iso(d):
    return str(d)


def block_median(arr, block, min_valid, max_std=None):
    """NaN-median over block x block tiles (tiles with < min_valid valid fraction -> NaN), expanded to full size."""
    import warnings
    H, W = arr.shape
    Hp, Wp = -(-H // block) * block, -(-W // block) * block
    pad = np.full((Hp, Wp), np.nan, np.float32)
    pad[:H, :W] = arr
    t = pad.reshape(Hp // block, block, Wp // block, block)
    frac = np.isfinite(t).mean(axis=(1, 3))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        med = np.nanmedian(t, axis=(1, 3))
    med[frac < min_valid] = np.nan
    if max_std is not None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            sd = np.nanstd(t, axis=(1, 3))
        med[~(sd <= max_std)] = np.nan  # speckled (noisy) blocks are not eligible
    full = np.repeat(np.repeat(med, block, 0), block, 1)[:H, :W]
    centre = np.zeros((H, W), bool)
    centre[block // 2::block, block // 2::block] = True  # one representative pixel per block
    return np.where(centre & np.isfinite(arr), full, np.nan).astype(np.float32)


def load_pairs(site):
    """Union of PC2 (pipeline/subset) and PC3 backup (analysis/out/subset) npz files, one per pair.
    Same pair in both: prefer the file that carries the ionosphere screen (`ion`), else PC2's."""
    best = {}
    for rank, src in enumerate((ROOT / "pipeline" / "subset" / site, ROOT / "analysis" / "out" / "subset" / site)):
        for f in sorted(src.glob("*.npz")):
            d = np.load(f, allow_pickle=False)
            key = (str(d["date1"]), str(d["date2"])) if "date1" in d else tuple(f.stem.split("_"))
            has_ion = "ion" in d and d["ion"].size > 0
            score = (has_ion, -rank)
            if key not in best or score > best[key][0]:
                best[key] = (score, f)
    files = [v[1] for _, v in sorted(best.items())]
    if not files:
        raise SystemExit(f"no npz for {site}")
    return "pipeline+analysis/out", files


def chain(files):
    pairs, notes = [], []
    for f in files:
        d = np.load(f, allow_pickle=False)
        q = str(d["quality"])
        d1, d2 = (str(d["date1"]), str(d["date2"])) if "date1" in d else tuple(f.stem.split("_"))
        if q != "provisional":
            notes.append(f"skipped {f.name}: quality={q}")
            continue
        pairs.append((d1, d2, f, d))
    pairs.sort(key=lambda p: p[0])
    used = [pairs[0]]
    for p in pairs[1:]:
        if p[0] == used[-1][1]:
            used.append(p)
        elif p[0] > used[-1][1]:
            notes.append(f"chain gap {used[-1][1]} -> {p[0]}: stopped at {used[-1][1]}")
            break
        else:
            notes.append(f"skipped overlapping pair {p[0]}_{p[1]}")
    return used, notes


def to_latlon_grid(arr, x, y, epsg, bbox, step=0.001):
    """Nearest-neighbour resample a UTM grid onto a regular lon/lat grid covering bbox (north-up)."""
    w, s, e, n = bbox
    lons = np.arange(w + step / 2, e, step)
    lats = np.arange(n - step / 2, s, -step)
    LON, LAT = np.meshgrid(lons, lats)
    X, Y = Transformer.from_crs(4326, epsg, always_xy=True).transform(LON, LAT)
    dx, dy = x[1] - x[0], y[1] - y[0]
    ix = np.rint((X - x[0]) / dx).astype(int)
    iy = np.rint((Y - y[0]) / dy).astype(int)
    ok = (ix >= 0) & (ix < len(x)) & (iy >= 0) & (iy < len(y))
    out = np.full(LON.shape, np.nan, np.float32)
    out[ok] = arr[iy[ok], ix[ok]]
    return out


def save_png(grid, path, vmin, vmax):
    cmap = plt.get_cmap(CMAP).copy()
    cmap.set_bad((0, 0, 0, 0))
    plt.imsave(path, np.ma.masked_invalid(grid), cmap=cmap, vmin=vmin, vmax=vmax)


def load_places(site):
    """OSM place=city|town|village nodes for the site (Overpass export, ODbL, (c) OpenStreetMap contributors)."""
    f = ROOT / "analysis" / "out" / f"{site}_places_osm.json"
    if not f.exists():
        return []
    e = json.loads(f.read_text(encoding="utf-8"))["elements"]
    return [(x["tags"]["name"], x["lon"], x["lat"]) for x in e if "name" in x["tags"]]


def place_label(lon, lat, places):
    """'7 km SW of Corcoran' from the nearest OSM place; coordinates if no place list."""
    if not places:
        return f"{lat:.3f}N {abs(lon):.3f}{'W' if lon < 0 else 'E'}"
    kx = 111.32 * np.cos(np.deg2rad(lat))
    best = min(places, key=lambda p: ((p[1] - lon) * kx) ** 2 + ((p[2] - lat) * 110.57) ** 2)
    dx, dy = (lon - best[1]) * kx, (lat - best[2]) * 110.57
    km = float(np.hypot(dx, dy))
    if km < 1.5:
        return best[0]
    ang = (np.degrees(np.arctan2(dx, dy)) + 360) % 360
    d = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][int((ang + 22.5) // 45) % 8]
    return f"{km:.0f} km {d} of {best[0]}"


def pick_points(cum_s, valid, ref_rc, x, y, epsg, min_sep_px=60):
    """5 most subsiding (separated local minima), 5 around the median, 2 near the reference."""
    tr = Transformer.from_crs(epsg, 4326, always_xy=True)
    pts = []
    work = np.where(valid, cum_s, np.inf)
    for _ in range(5):
        r, c = np.unravel_index(np.argmin(work), work.shape)
        if not np.isfinite(work[r, c]):
            break
        pts.append(("most_subsiding", r, c))
        work[max(r - min_sep_px, 0): r + min_sep_px, max(c - min_sep_px, 0): c + min_sep_px] = np.inf
    med = np.nanmedian(cum_s[valid])
    cand = np.argwhere(valid & (np.abs(cum_s - med) < 0.25))
    rng = np.random.default_rng(42)
    rng.shuffle(cand)
    for r, c in cand:
        if len([p for p in pts if p[0] == "median"]) >= 5:
            break
        if all(abs(r - p[1]) > min_sep_px or abs(c - p[2]) > min_sep_px for p in pts):
            pts.append(("median", int(r), int(c)))
    rr, rc = ref_rc
    cand = np.argwhere(valid)
    dist = (cand[:, 0] - rr) ** 2 + (cand[:, 1] - rc) ** 2
    for r, c in cand[np.argsort(dist)[1:3]]:  # 2nd and 3rd nearest valid blocks (1st holds the reference)
        pts.append(("near_reference", int(r), int(c)))
    out = []
    for k, r, c in pts:
        lon, lat = tr.transform(x[c], y[r])
        out.append((k, int(r), int(c), float(lon), float(lat)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--thr", type=float, default=0.3)
    ap.add_argument("--no-names", action="store_true")
    ap.add_argument("--data-dir", help="write meta/points/summary/disp here instead of data/<site>/ (QA runs)")
    ap.add_argument("--ref-radius", type=int, default=RADIUS, help="reference window half-size in px")
    ap.add_argument("--deramp", type=int, default=1, choices=[0, 1, 2],
                    help="per-pair ramp removal: 0 none, 1 plane (default), 2 quadratic")
    ap.add_argument("--no-ion", dest="ion", action="store_false", help="do not subtract the product ionosphere screen")
    a = ap.parse_args()
    site, bbox = a.site, BBOX[a.site]
    src, files = load_pairs(site)
    used, notes = chain(files)
    print(f"source {src}: {len(used)} pairs", [str(u[2].relative_to(ROOT)) for u in used], notes)
    if len(used) < 2:
        raise SystemExit("need >= 2 consecutive pairs")

    d0 = used[0][3]
    x, y, epsg = d0["x"], d0["y"], int(d0["epsg"])
    dem = None
    if a.deramp:
        dem_f = ROOT / "analysis" / "out" / f"{site}_dem.npy"
        if not dem_f.exists():
            try:
                from dem import dem_on_grid
                np.save(dem_f, dem_on_grid(x, y, epsg))
            except Exception as ex:
                print("DEM unavailable, plane-only deramp:", ex)
        if dem_f.exists():
            dem = np.load(dem_f)
            if dem.shape != d0["unw"].shape:
                dem = None
    pair_cm, stats = [], []
    for d1, d2, f, d in used:
        if d["unw"].shape != d0["unw"].shape or not np.allclose(d["x"], x) or not np.allclose(d["y"], y):
            raise SystemExit(f"grid mismatch in {f.name}; BLOCKED (pairs must share one grid)")
        unw = d["unw"]
        ion_used = a.ion and "ion" in d and d["ion"].shape == unw.shape
        if ion_used:
            # Product ionosphere phase screen (shipped in GUNW, not applied by default:
            # https://nisar-docs.asf.alaska.edu/gunw). Subtracting it lowered the scatter in every
            # pair we tested (status/PC3.md), which also confirms the sign.
            unw = unw - d["ion"]
        cm = phase_to_cm(unw, float(d["wavelength"]))
        if "conncomp" in d and d["conncomp"].size:
            cm = mask_components(cm, d["conncomp"])
        cm = mask_coherence(cm, d["coh"], a.thr)
        cm = remove_islands(cm, ISLAND_MIN_PX)
        k_elev = None
        if a.deramp and dem is not None:
            cm, k_elev = deramp_elevation(cm, dem)
        elif a.deramp:
            cm = deramp(cm, order=a.deramp)
        n_before = int(np.isfinite(cm).sum())
        cm = cycle_outliers(cm, thr_cm=float(d["wavelength"]) / 4 * 100)
        cycle_px = n_before - int(np.isfinite(cm).sum())
        pair_cm.append(cm)
        stats.append({"pair": [d1, d2], "file": str(f.relative_to(ROOT)).replace("\\", "/"), "lambda_m": float(d["wavelength"]), "ionosphere_applied": bool(ion_used), "cycle_outlier_px": cycle_px, "elev_coef_cm_per_km": None if k_elev is None else round(k_elev, 2),
                      "valid_frac_after_masks": float(np.isfinite(cm).mean())})

    valid_all = np.logical_and.reduce([np.isfinite(c) for c in pair_cm])
    coh_mean = np.mean([np.load(f)["coh"].astype(np.float32) / 255 for _, _, f, _ in used], axis=0)
    XX, YY = np.meshgrid(x, y)
    LON, LAT = Transformer.from_crs(epsg, 4326, always_xy=True).transform(XX, YY)
    in_bbox = (LON >= bbox[0]) & (LON <= bbox[2]) & (LAT >= bbox[1]) & (LAT <= bbox[3])
    r, c, mcoh = choose_reference(coh_mean, valid_all & in_bbox, a.ref_radius, stride=3)
    lon_r, lat_r = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c], y[r])
    print(f"reference row={r} col={c} lon={lon_r:.4f} lat={lat_r:.4f} mean_coh={mcoh:.2f}")

    dates = [used[0][0]] + [p[1] for p in used]
    cum = [np.zeros_like(pair_cm[0])]
    cum[0][~valid_all] = np.nan
    n_out = 0
    for i, cm in enumerate(pair_cm):
        cm = reference(cm, (r, c), a.ref_radius)
        bad = np.abs(cm) > PAIR_OUTLIER_CM
        n_out += int(bad.sum())
        cm[bad] = np.nan
        stats[i]["p2_p50_p98_cm"] = [round(float(v), 2) for v in np.nanpercentile(cm, [2, 50, 98])]
        cum.append(cum[-1] + cm)
    for k in range(len(cum)):
        cum[k][~valid_all] = np.nan
    final = cum[-1]
    valid = np.isfinite(final)
    print(f"valid in full chain: {valid.mean():.3f}; outlier px removed: {n_out}")

    # robust extremes: ~1 km blocks (13x13 px), block median, only blocks with >= 50 % valid pixels,
    # so small artefacts (rivers, canals, single fields) never set the headline number
    sm = block_median(np.where(in_bbox, final, np.nan), BLOCK_PX, BLOCK_MIN_VALID, BLOCK_MAX_STD)
    rmin, cmin = np.unravel_index(np.nanargmin(sm), sm.shape)
    max_sub = float(sm[rmin, cmin])

    # reference sensitivity: redo the sum with the best window >= 30 km from the primary reference
    far = np.hypot((np.arange(len(y))[:, None] - r) * abs(y[1] - y[0]), (np.arange(len(x))[None, :] - c) * abs(x[1] - x[0])) < 30000
    try:
        r2, c2, _ = choose_reference(coh_mean, valid_all & in_bbox, a.ref_radius, stride=3, exclude=far)
        alt = np.zeros_like(final)
        for cm in pair_cm:
            q = reference(cm, (r2, c2), a.ref_radius)
            q[np.abs(q) > PAIR_OUTLIER_CM] = np.nan
            alt = alt + q
        alt[~valid_all] = np.nan
        sm_alt = block_median(np.where(in_bbox, alt, np.nan), BLOCK_PX, BLOCK_MIN_VALID, BLOCK_MAX_STD)
        alt_max = float(sm_alt[rmin, cmin]) if np.isfinite(sm_alt[rmin, cmin]) else float(np.nanmin(sm_alt))
        lon_r2, lat_r2 = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c2], y[r2])
        sens = {"alt_reference": {"lon": round(lon_r2, 5), "lat": round(lat_r2, 5)},
                "max_subsidence_cm_at_same_location": round(alt_max, 1)}
    except ValueError:
        sens = None
    print("reference sensitivity:", sens)
    inc = d0["incidence"] if "incidence" in d0 and d0["incidence"].size else None
    inc_at = float(inc[rmin, cmin]) if inc is not None else None
    days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
    lon_m, lat_m = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[cmin], y[rmin])
    vlim = float(np.ceil(np.nanpercentile(np.abs(sm), 99.5)))
    vmin, vmax = -vlim, vlim
    print(f"max subsidence (LOS, 1 km block median) {max_sub:.2f} cm at {lon_m:.4f},{lat_m:.4f}; days={days}; v=±{vlim}")

    # ---- outputs -------------------------------------------------------------------------------
    ddir = Path(a.data_dir) if a.data_dir else ROOT / "data" / site
    (ddir / "disp").mkdir(parents=True, exist_ok=True)
    for dt, g in zip(dates, cum):
        save_png(to_latlon_grid(g, x, y, epsg, bbox), ddir / "disp" / f"{dt}.png", vmin, vmax)

    out = ROOT / "analysis" / "out"
    # data contract 4.1 fields (PC6 reads cum_cm); extras kept small (K-12: every repo file <= 20 MB)
    np.savez_compressed(out / f"{site}_cum.npz", cum_cm=final.astype(np.float32), x=x, y=y, epsg=np.int32(epsg),
                        dates=np.array(dates), quality="provisional",
                        incidence=(inc.astype(np.float16) if inc is not None else np.array([])),
                        reference_rc=np.array([r, c]))
    # per-date cumulative stack for GNSS comparison (Q05), float16 cm (step <= 0.008 cm below 16 cm)
    np.savez_compressed(out / f"{site}_cum_stack.npz", cum_stack_cm=np.stack(cum).astype(np.float16),
                        dates=np.array(dates), x=x, y=y, epsg=np.int32(epsg), quality="provisional")
    for fn in (f"{site}_cum.npz", f"{site}_cum_stack.npz"):
        mb = (out / fn).stat().st_size / 1e6
        print(f"{fn}: {mb:.1f} MB")
        if mb > 20:
            print(f"WARNING {fn} > 20 MB: do not commit (K-12)")

    pairs_txt = ", ".join(f"{p[0]}_{p[1]}" for p in used)
    granules = [str(p[3]["granule"]) for p in used if "granule" in p[3]]
    geom = "GUNW track/frame unknown"
    if granules:
        g = granules[0].split("_")  # NISAR_L2_PR_GUNW_<cycle>_<track>_<A|D>_<frame>_...
        geom = f"track {int(g[5])} {'ascending' if g[6] == 'A' else 'descending'} frame {int(g[7])}"
    meta = {
        "site": site, "bbox": list(bbox), "dates": dates, "units": "cm", "vmin": vmin, "vmax": vmax,
        "component": "LOS (line of sight); negative = away from satellite = subsidence",
        "colormap": "RdBu (red = subsidence, blue = uplift/toward satellite)",
        "source": f"NISAR L2 GUNW (PROVISIONAL, CRID P05023) via ASF DAAC, {geom}; "
                  "https://nisar-docs.asf.alaska.edu/gunw",
        "granules": granules,
        "notes": (f"Cumulative LOS displacement relative to {dates[0]}, sum of {len(used)} consecutive pairs ({pairs_txt}). "
                  f"Phase to cm with -lambda/(4*pi), lambda from each file's centerFrequency. Masks: coherence >= {a.thr}, "
                  f"connectedComponents != 0, isolated patches < {ISLAND_MIN_PX} px (1.3 km2) removed (unwrapping-error guard), pixels deviating > lambda/4 (half a phase cycle) from their 720 m "
                  f"tile median removed, "
                  f"|pair| > {PAIR_OUTLIER_CM} cm removed; pixel shown only if valid in every pair. "
                  f"All pairs referenced to the same window at {lon_r:.4f}E {lat_r:.4f}N. "
                  + ("The ionosphere phase screen shipped in each GUNW was subtracted. " if a.ion else
                     "The ionosphere phase screen was NOT applied. ")
                  + ({1: ("A best-fit plane plus a linear elevation term (Copernicus DEM GLO-90) was removed from each pair "
                          "(long-wavelength and elevation-correlated troposphere residual; this can also remove part of any "
                          "valley-wide tilt). " if dem is not None else
                          "A best-fit plane was removed from each pair (long-wavelength atmospheric residual; this can also "
                          "remove part of any valley-wide tilt). "),
                      2: "A best-fit quadratic surface was removed from each pair. "}.get(a.deramp, ""))
                  + "Troposphere and solid-earth-tide layers were NOT applied; residual atmospheric noise of a few cm "
                  "per pair is expected. " + " ".join(notes)),
        "reference_point": {"lon": round(lon_r, 5), "lat": round(lat_r, 5)},
        "quality": "provisional",
        "quality_note": DISCLAIMER,
    }
    (ddir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    places = [] if a.no_names else load_places(site)
    pts = pick_points(sm, np.isfinite(sm), (r, c), x, y, epsg)
    points = []
    for i, (kind, pr, pc, lon, lat) in enumerate(pts, 1):
        hb = BLOCK_PX // 2
        win = np.stack(cum)[:, max(pr - hb, 0): pr + hb + 1, max(pc - hb, 0): pc + hb + 1]
        ts = np.nanmedian(win.reshape(len(dates), -1), axis=1)
        name = place_label(lon, lat, places)
        points.append({"id": f"p{i:02d}", "name": name, "kind": kind, "lon": round(lon, 5), "lat": round(lat, 5),
                       "dates": dates, "disp_cm": [None if not np.isfinite(v) else round(float(v), 2) for v in ts]})
    (ddir / "points.json").write_text(json.dumps(points, indent=2), encoding="utf-8")

    rate = max_sub / days * 365.25
    summary = {
        "max_subsidence_cm": round(max_sub, 1),
        "max_subsidence_range_cm": (sorted([round(max_sub, 1), sens["max_subsidence_cm_at_same_location"]])
                                    if sens else None),
        "reference_sensitivity": sens,
        "period": [dates[0], dates[-1]],
        "rate_cm_per_yr_estimate": round(rate, 1),
        "reference_point": {"lon": round(lon_r, 5), "lat": round(lat_r, 5)},
        "quality": "provisional",
        "quality_note": DISCLAIMER,
        "component": "LOS",
        "max_subsidence_location": {"lon": round(lon_m, 5), "lat": round(lat_m, 5)},
        "max_subsidence_vertical_cm_estimate": round(max_sub / np.cos(np.deg2rad(inc_at)), 1) if inc_at else None,
        "incidence_deg_at_max": round(inc_at, 1) if inc_at else None,
        "n_pairs": len(used),
        "method_note": (f"Headline value = most negative median of ~1 km blocks (13x13 px, >= 50 % valid pixels, within-block std <= 2 cm) of the cumulative LOS map. Rate = linear "
                        f"extrapolation of {days} days ({dates[0]} to {dates[-1]}, irrigation season) to one year: an ESTIMATE "
                        "that likely overstates the annual net rate because part of summer subsidence recovers in winter. "
                        "Vertical value assumes purely vertical motion (LOS / cos(incidence))."),
    }
    (ddir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / f"{site}_pair_stats.json").write_text(json.dumps({"pairs": stats, "notes": notes,
                                                              "reference_mean_coh": mcoh,
                                                              "valid_frac_full_chain": float(valid.mean()),
                                                              "outlier_px_removed": n_out}, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
