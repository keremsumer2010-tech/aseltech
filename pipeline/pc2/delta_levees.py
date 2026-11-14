"""Fetch Sacramento-San Joaquin Delta levees from OSM Overpass and plot subsidence profile along levees."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import requests
from pyproj import Transformer

ROOT = Path(__file__).resolve().parent.parent.parent
BBOX = (-121.85, 37.95, -121.45, 38.20)  # w, s, e, n

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]


def fetch_levees(cache_path: Path) -> dict:
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    w, s, e, n = BBOX
    query = f"""
[out:json][timeout:60];
(
  way["man_made"~"^(dyke|embankment|levee)$"]({s},{w},{n},{e});
  way["flood_protection"="yes"]({s},{w},{n},{e});
);
out body geom;
"""
    last_err = None
    for url in OVERPASS_URLS:
        try:
            r = requests.post(url, data={"data": query}, timeout=70)
            r.raise_for_status()
            data = r.json()
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(data), encoding="utf-8")
            return data
        except Exception as exc:
            last_err = exc
    raise RuntimeError(f"Overpass failed: {last_err}")


def sample_along_way(
    coords: list[dict],
    cum: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    tr: Transformer,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    lons = np.array([c["lon"] for c in coords], dtype=np.float64)
    lats = np.array([c["lat"] for c in coords], dtype=np.float64)
    ux, uy = tr.transform(lons, lats)
    dx, dy = x[1] - x[0], y[1] - y[0]
    ix = np.rint((ux - x[0]) / dx).astype(int)
    iy = np.rint((uy - y[0]) / dy).astype(int)
    H, W = cum.shape
    vals = np.full(len(ux), np.nan, dtype=np.float32)
    for k in range(len(ux)):
        if 0 <= ix[k] < W and 0 <= iy[k] < H:
            # 3x3 window median around levee vertex to avoid single-pixel NaN over water edge
            r0, r1 = max(0, iy[k] - 1), min(H, iy[k] + 2)
            c0, c1 = max(0, ix[k] - 1), min(W, ix[k] + 2)
            patch = cum[r0:r1, c0:c1]
            if np.isfinite(patch).any():
                vals[k] = float(np.nanmedian(patch))
    dist_km = np.zeros(len(ux), dtype=np.float64)
    if len(ux) > 1:
        seg = np.hypot(np.diff(ux), np.diff(uy)) / 1000.0
        dist_km[1:] = np.cumsum(seg)
    return lons, lats, dist_km, vals


def main() -> None:
    cum_path = ROOT / "analysis" / "out" / "delta_cum.npz"
    if not cum_path.exists():
        raise SystemExit(f"Missing {cum_path}; run run_cumulative.py delta first.")
    d = np.load(cum_path, allow_pickle=False)
    cum = d["cum_cm"]
    x, y, epsg = d["x"], d["y"], int(d["epsg"])
    dates = [str(s) for s in d["dates"]]

    cache_path = ROOT / "pipeline" / "pc2" / "delta_levees_osm.json"
    osm = fetch_levees(cache_path)
    ways = [el for el in osm.get("elements", []) if el.get("type") == "way" and el.get("geometry")]
    print(f"OSM ways fetched: {len(ways)}")

    tr = Transformer.from_crs(4326, epsg, always_xy=True)
    tr_inv = Transformer.from_crs(epsg, 4326, always_xy=True)

    # Convert grid corners for plotting in lon/lat
    lon0, lat0 = tr_inv.transform(x[0], y[0])
    lon1, lat1 = tr_inv.transform(x[-1], y[-1])
    extent = [lon0, lon1, lat0, lat1] if y[1] > y[0] else [lon0, lon1, lat1, lat0]
    plot_cum = cum if y[1] > y[0] else cum[::-1, :]

    all_vals = []
    way_profiles = []
    for w in ways:
        lons, lats, dist_km, vals = sample_along_way(w["geometry"], cum, x, y, tr)
        n_ok = int(np.isfinite(vals).sum())
        if n_ok >= 5 and dist_km[-1] >= 0.5:
            all_vals.append(vals[np.isfinite(vals)])
            way_profiles.append(
                {
                    "id": w["id"],
                    "name": w.get("tags", {}).get("name", f"Levee #{w['id']}"),
                    "man_made": w.get("tags", {}).get("man_made", "levee"),
                    "length_km": float(dist_km[-1]),
                    "n_valid": n_ok,
                    "min_cm": float(np.nanmin(vals)),
                    "median_cm": float(np.nanmedian(vals)),
                    "lons": lons,
                    "lats": lats,
                    "dist_km": dist_km,
                    "vals": vals,
                }
            )

    if not way_profiles:
        raise SystemExit("No valid levee profiles found.")

    # Pick longest/most-subsiding significant levee (>= 2 km if available) for highlight profile
    long_ways = [wp for wp in way_profiles if wp["length_km"] >= 2.0 and wp["n_valid"] >= 10]
    pool = long_ways if long_ways else way_profiles
    best_way = min(pool, key=lambda wp: np.nanpercentile(wp["vals"], 10))
    cat_vals = np.concatenate(all_vals)

    print(
        f"Valid levee ways (>=0.5 km, >=5 pts): {len(way_profiles)} | "
        f"All levee samples: N={len(cat_vals)}, median={np.median(cat_vals):.2f} cm, "
        f"p10={np.percentile(cat_vals, 10):.2f} cm, min={np.min(cat_vals):.2f} cm"
    )
    print(
        f"Highlight levee: {best_way['name']} (id={best_way['id']}, "
        f"len={best_way['length_km']:.2f} km, min={best_way['min_cm']:.2f} cm, "
        f"median={best_way['median_cm']:.2f} cm)"
    )

    vlim = float(np.ceil(np.nanpercentile(np.abs(cum), 98)))
    vlim = max(vlim, 3.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.4), gridspec_kw={"width_ratios": [1.15, 1.0]})
    im = ax1.imshow(
        np.flipud(plot_cum),
        extent=extent,
        cmap="RdBu",
        vmin=-vlim,
        vmax=vlim,
        aspect="auto",
    )
    for wp in way_profiles:
        ax1.plot(wp["lons"], wp["lats"], color="#222222", lw=0.7, alpha=0.65)
    ax1.plot(best_way["lons"], best_way["lats"], color="#000000", lw=2.3, label=f"Profiled levee ({best_way['length_km']:.1f} km)")
    ax1.set_xlim(BBOX[0], BBOX[2])
    ax1.set_ylim(BBOX[1], BBOX[3])
    ax1.set_xlabel("Longitude (deg)")
    ax1.set_ylabel("Latitude (deg)")
    ax1.set_title(f"Sacramento-San Joaquin Delta LOS ({dates[0]} to {dates[-1]})")
    ax1.legend(loc="lower left", fontsize=8, framealpha=0.9)
    cb = fig.colorbar(im, ax=ax1, shrink=0.86)
    cb.set_label("Cumulative LOS displacement (cm)")

    ok = np.isfinite(best_way["vals"])
    ax2.axhline(0.0, color="#888888", lw=0.8, ls="--")
    ax2.plot(best_way["dist_km"][ok], best_way["vals"][ok], color="#b2182b", lw=1.6, marker="o", ms=2.5)
    ax2.fill_between(best_way["dist_km"][ok], best_way["vals"][ok], 0, where=(best_way["vals"][ok] < 0), color="#b2182b", alpha=0.15)
    ax2.set_xlabel("Distance along levee (km)")
    ax2.set_ylabel("Cumulative LOS displacement (cm)")
    ax2.set_title(f"Levee Subsidence Profile: {best_way['name']}\n(median {best_way['median_cm']:.2f} cm, min {best_way['min_cm']:.2f} cm)")
    ax2.grid(True, alpha=0.3)

    fig.suptitle("NISAR Handbook Fig. 2-4 Target: Delta Levees Measured with 2026 Provisional GUNW", fontsize=11, fontweight="bold")
    fig.tight_layout()
    out_png = ROOT / "docs" / "story" / "media" / "pc2_delta.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=180)
    plt.close(fig)
    print(f"Saved {out_png}")


if __name__ == "__main__":
    main()
