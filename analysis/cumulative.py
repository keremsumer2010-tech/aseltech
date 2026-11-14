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
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer
from scipy.ndimage import median_filter, minimum_filter

sys.path.insert(0, str(Path(__file__).parent))
from gunw_io import BBOX  # noqa: E402
from insar import choose_reference, mask_coherence, mask_components, phase_to_cm, reference  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RADIUS = 3
PAIR_OUTLIER_CM = 15.0  # |per-pair LOS| above this in a 12-24 day pair = unwrapping error (documented)
CMAP = "RdBu"
DISCLAIMER = ("NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
              "(NASA-JPL and ISRO), not by our team.")


def iso(d):
    return str(d)


def load_pairs(site):
    for src in (ROOT / "pipeline" / "subset" / site, ROOT / "analysis" / "out" / "subset" / site):
        files = sorted(src.glob("*.npz"))
        if files:
            return src, files
    raise SystemExit(f"no npz for {site}")


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


def reverse_name(lon, lat, cache):
    key = f"{lon:.2f},{lat:.2f}"
    if key in cache:
        return cache[key]
    q = urllib.parse.urlencode({"lat": f"{lat:.4f}", "lon": f"{lon:.4f}", "format": "jsonv2", "zoom": 12})
    req = urllib.request.Request(f"https://nominatim.openstreetmap.org/reverse?{q}",
                                 headers={"User-Agent": "aseltech-space-apps-hackathon/1.0"})
    name = None
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            a = json.load(r).get("address", {})
        name = next((a[k] for k in ("city", "town", "village", "hamlet", "suburb", "county") if k in a), None)
    except Exception as ex:  # network failure -> coordinate label, never an invented name
        print("nominatim failed", ex)
    time.sleep(1.1)  # Nominatim usage policy: max 1 request / second
    cache[key] = name
    return name


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
    for dr, dc in ((-12, 0), (0, 12)):
        r, c = rr + dr, rc + dc
        if 0 <= r < valid.shape[0] and 0 <= c < valid.shape[1] and valid[r, c]:
            pts.append(("near_reference", r, c))
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
    a = ap.parse_args()
    site, bbox = a.site, BBOX[a.site]
    src, files = load_pairs(site)
    used, notes = chain(files)
    print(f"source {src.relative_to(ROOT)}: {len(used)} pairs", notes)
    if len(used) < 2:
        raise SystemExit("need >= 2 consecutive pairs")

    d0 = used[0][3]
    x, y, epsg = d0["x"], d0["y"], int(d0["epsg"])
    pair_cm, stats = [], []
    for d1, d2, f, d in used:
        if d["unw"].shape != d0["unw"].shape or not np.allclose(d["x"], x) or not np.allclose(d["y"], y):
            raise SystemExit(f"grid mismatch in {f.name}; BLOCKED (pairs must share one grid)")
        cm = phase_to_cm(d["unw"], float(d["wavelength"]))
        if "conncomp" in d and d["conncomp"].size:
            cm = mask_components(cm, d["conncomp"])
        cm = mask_coherence(cm, d["coh"], a.thr)
        pair_cm.append(cm)
        stats.append({"pair": [d1, d2], "lambda_m": float(d["wavelength"]),
                      "valid_frac_after_masks": float(np.isfinite(cm).mean())})

    valid_all = np.logical_and.reduce([np.isfinite(c) for c in pair_cm])
    coh_mean = np.mean([np.load(f)["coh"].astype(np.float32) / 255 for _, _, f, _ in used], axis=0)
    r, c, mcoh = choose_reference(coh_mean, valid_all, RADIUS, stride=3)
    lon_r, lat_r = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[c], y[r])
    print(f"reference row={r} col={c} lon={lon_r:.4f} lat={lat_r:.4f} mean_coh={mcoh:.2f}")

    dates = [used[0][0]] + [p[1] for p in used]
    cum = [np.zeros_like(pair_cm[0])]
    cum[0][~valid_all] = np.nan
    n_out = 0
    for i, cm in enumerate(pair_cm):
        cm = reference(cm, (r, c), RADIUS)
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

    # robust extremes: 5x5 (400 m) median smoothing, so single pixels never set the headline number
    sm = median_filter(np.where(valid, final, np.nan), size=5, mode="nearest")
    sm = np.where(valid & np.isfinite(sm), sm, np.nan)
    rmin, cmin = np.unravel_index(np.nanargmin(sm), sm.shape)
    max_sub = float(sm[rmin, cmin])
    inc = d0["incidence"] if "incidence" in d0 and d0["incidence"].size else None
    inc_at = float(inc[rmin, cmin]) if inc is not None else None
    days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
    lon_m, lat_m = Transformer.from_crs(epsg, 4326, always_xy=True).transform(x[cmin], y[rmin])
    vlim = float(np.ceil(np.nanpercentile(np.abs(sm), 99.5)))
    vmin, vmax = -vlim, vlim
    print(f"max subsidence (LOS, 400 m median) {max_sub:.2f} cm at {lon_m:.4f},{lat_m:.4f}; days={days}; v=±{vlim}")

    # ---- outputs -------------------------------------------------------------------------------
    ddir = ROOT / "data" / site
    (ddir / "disp").mkdir(parents=True, exist_ok=True)
    for dt, g in zip(dates, cum):
        save_png(to_latlon_grid(g, x, y, epsg, bbox), ddir / "disp" / f"{dt}.png", vmin, vmax)

    out = ROOT / "analysis" / "out"
    np.savez_compressed(out / f"{site}_cum.npz", cum_cm=final.astype(np.float32), x=x, y=y, epsg=np.int32(epsg),
                        dates=np.array(dates), quality="provisional",
                        cum_stack_cm=np.stack(cum).astype(np.float32),
                        incidence=inc if inc is not None else np.array([]),
                        reference_rc=np.array([r, c]))

    pairs_txt = ", ".join(f"{p[0]}_{p[1]}" for p in used)
    granules = [str(p[3]["granule"]) for p in used if "granule" in p[3]]
    meta = {
        "site": site, "bbox": list(bbox), "dates": dates, "units": "cm", "vmin": vmin, "vmax": vmax,
        "component": "LOS (line of sight); negative = away from satellite = subsidence",
        "colormap": "RdBu (red = subsidence, blue = uplift/toward satellite)",
        "source": "NISAR L2 GUNW (PROVISIONAL, CRID P05023) via ASF DAAC, track 34 ascending frame 20; "
                  "https://nisar-docs.asf.alaska.edu/gunw",
        "granules": granules,
        "notes": (f"Cumulative LOS displacement relative to {dates[0]}, sum of {len(used)} consecutive pairs ({pairs_txt}). "
                  f"Phase to cm with -lambda/(4*pi), lambda from each file's centerFrequency. Masks: coherence >= {a.thr}, "
                  f"connectedComponents != 0, |pair| > {PAIR_OUTLIER_CM} cm removed; pixel shown only if valid in every pair. "
                  f"All pairs referenced to the same window at {lon_r:.4f}E {lat_r:.4f}N. Ionosphere, troposphere and solid-earth-tide "
                  "layers shipped in the product were NOT applied (product default). " + " ".join(notes)),
        "reference_point": {"lon": round(lon_r, 5), "lat": round(lat_r, 5)},
        "quality": "provisional",
        "quality_note": DISCLAIMER,
    }
    (ddir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    cache = {}
    pts = pick_points(sm, valid & np.isfinite(sm), (r, c), x, y, epsg)
    points = []
    for i, (kind, pr, pc, lon, lat) in enumerate(pts, 1):
        win = np.stack(cum)[:, max(pr - 1, 0): pr + 2, max(pc - 1, 0): pc + 2]
        ts = np.nanmedian(win.reshape(len(dates), -1), axis=1)
        place = None if a.no_names else reverse_name(lon, lat, cache)
        name = f"near {place}" if place else f"{lat:.3f}N {abs(lon):.3f}W"
        points.append({"id": f"p{i:02d}", "name": name, "kind": kind, "lon": round(lon, 5), "lat": round(lat, 5),
                       "dates": dates, "disp_cm": [None if not np.isfinite(v) else round(float(v), 2) for v in ts]})
    (ddir / "points.json").write_text(json.dumps(points, indent=2), encoding="utf-8")

    rate = max_sub / days * 365.25
    summary = {
        "max_subsidence_cm": round(max_sub, 1),
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
        "method_note": (f"Headline value = minimum of 400 m (5x5 px) median-smoothed cumulative LOS map. Rate = linear "
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
