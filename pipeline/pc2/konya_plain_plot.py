"""Plot Konya Plain cumulative LOS subsidence map with major towns and sinkhole markers."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parent.parent.parent
BBOX = (32.4, 37.4, 33.9, 38.1)  # w, s, e, n

TOWNS = [
    ("Konya", 32.4846, 37.8714),
    ("Çumra", 32.7764, 37.5732),
    ("Karapınar", 33.5522, 37.7160),
    ("Ereğli (W edge)", 33.85, 37.55),
]


def main() -> None:
    cum_path = ROOT / "analysis" / "out" / "konya_plain_cum.npz"
    if not cum_path.exists():
        raise SystemExit(f"Missing {cum_path}; run run_cumulative.py konya_plain first.")
    d = np.load(cum_path, allow_pickle=False)
    cum = d["cum_cm"]
    x, y, epsg = d["x"], d["y"], int(d["epsg"])
    dates = [str(s) for s in d["dates"]]

    tr_inv = Transformer.from_crs(epsg, 4326, always_xy=True)
    lon0, lat0 = tr_inv.transform(x[0], y[0])
    lon1, lat1 = tr_inv.transform(x[-1], y[-1])
    extent = [lon0, lon1, lat0, lat1] if y[1] > y[0] else [lon0, lon1, lat1, lat0]
    plot_cum = cum if y[1] > y[0] else cum[::-1, :]

    sinkholes_path = ROOT / "risk" / "sinkholes.geojson"
    sh_lons, sh_lats = [], []
    if sinkholes_path.exists():
        gj = json.loads(sinkholes_path.read_text(encoding="utf-8"))
        for feat in gj.get("features", []):
            coords = feat.get("geometry", {}).get("coordinates", [])
            if len(coords) >= 2:
                lon, lat = coords[0], coords[1]
                if BBOX[0] <= lon <= BBOX[2] and BBOX[1] <= lat <= BBOX[3]:
                    sh_lons.append(lon)
                    sh_lats.append(lat)

    sum_path = ROOT / "data" / "konya_plain" / "summary.json"
    summary = json.loads(sum_path.read_text(encoding="utf-8")) if sum_path.exists() else {}
    max_sub = summary.get("max_subsidence_cm", float(np.nanmin(cum)))
    loc = summary.get("max_subsidence_location", {})

    vlim = float(np.ceil(np.nanpercentile(np.abs(cum), 98)))
    vlim = max(vlim, 5.0)

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    im = ax.imshow(
        np.flipud(plot_cum),
        extent=extent,
        cmap="RdBu",
        vmin=-vlim,
        vmax=vlim,
        aspect="auto",
    )
    if sh_lons:
        ax.scatter(sh_lons, sh_lats, s=28, facecolors="none", edgecolors="#111111", linewidths=1.1, label=f"Documented sinkholes (n={len(sh_lons)})", zorder=5)

    for name, lon, lat in TOWNS:
        if BBOX[0] <= lon <= BBOX[2] and BBOX[1] <= lat <= BBOX[3]:
            ax.plot(lon, lat, marker="^", color="#111111", ms=6, zorder=6)
            ax.text(lon + 0.015, lat + 0.01, name, fontsize=9, fontweight="bold", color="#111111",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75), zorder=7)

    if loc:
        ax.plot(loc["lon"], loc["lat"], marker="*", color="#ffdd00", markeredgecolor="#111111", ms=12, zorder=8,
                label=f"Peak 1 km subsidence ({max_sub} cm LOS)")

    ax.set_xlim(BBOX[0], BBOX[2])
    ax.set_ylim(BBOX[1], BBOX[3])
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    ax.set_title(f"Konya Closed Basin Cumulative LOS Displacement ({dates[0]} to {dates[-1]}, NISAR Path 7 Frame 69)")
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.9)
    cb = fig.colorbar(im, ax=ax, shrink=0.88)
    cb.set_label("Cumulative LOS displacement (cm)")

    fig.tight_layout()
    out_png = ROOT / "docs" / "story" / "media" / "pc2_konya_plain.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=180)
    plt.close(fig)
    print(f"Saved {out_png}")


if __name__ == "__main__":
    main()
