"""Generate docs/story/media/pc10_global.png: 4-region side-by-side comparison on one shared color scale."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]

PANELS = [
    {
        "title": "Central Valley, USA",
        "npz": ROOT / "analysis" / "out" / "central_valley_cum.npz",
        "summary": ROOT / "data" / "central_valley" / "summary.json",
        "meta": ROOT / "data" / "central_valley" / "meta.json",
    },
    {
        "title": "Mexico City, Mexico",
        "npz": ROOT / "analysis" / "out" / "global_mexico_city_cum.npz",
        "summary": ROOT / "data" / "global" / "mexico_city" / "summary.json",
        "meta": ROOT / "data" / "global" / "mexico_city" / "meta.json",
    },
    {
        "title": "Tehran, Iran",
        "npz": ROOT / "analysis" / "out" / "global_tehran_cum.npz",
        "summary": ROOT / "data" / "global" / "tehran" / "summary.json",
        "meta": ROOT / "data" / "global" / "tehran" / "meta.json",
    },
    {
        "title": "Jakarta, Indonesia",
        "npz": ROOT / "analysis" / "out" / "global_jakarta_cum.npz",
        "summary": ROOT / "data" / "global" / "jakarta" / "summary.json",
        "meta": ROOT / "data" / "global" / "jakarta" / "meta.json",
    },
]

VMIN, VMAX = -6.0, 6.0


def main() -> None:
    fig, axes = plt.subplots(1, 4, figsize=(18, 5.2), dpi=200, constrained_layout=False)
    fig.patch.set_facecolor("#ffffff")
    cmap = plt.get_cmap("RdBu").copy()
    cmap.set_bad("#eef1f5")

    im_ref = None
    for ax, p in zip(axes, PANELS):
        d = np.load(p["npz"], allow_pickle=False)
        summ = json.loads(p["summary"].read_text(encoding="utf-8"))
        meta = json.loads(p["meta"].read_text(encoding="utf-8"))

        cum = d["cum_cm"]
        x, y, epsg = d["x"], d["y"], int(d["epsg"])
        w, s, e, n = meta["bbox"]

        # Convert UTM extent to approximate km relative to bbox center or show lon/lat ticks
        tr = Transformer.from_crs(4326, epsg, always_xy=True)
        xmin, ymin = tr.transform(w, s)
        xmax, ymax = tr.transform(e, n)

        extent = [x[0] / 1000.0, x[-1] / 1000.0, y[-1] / 1000.0, y[0] / 1000.0]
        if y[0] < y[-1]:
            extent = [x[0] / 1000.0, x[-1] / 1000.0, y[0] / 1000.0, y[-1] / 1000.0]
            origin = "lower"
        else:
            origin = "upper"

        im = ax.imshow(
            np.ma.masked_invalid(cum),
            cmap=cmap,
            vmin=VMIN,
            vmax=VMAX,
            extent=extent,
            origin=origin,
            aspect="equal",
        )
        im_ref = im
        ax.set_xlim(xmin / 1000.0, xmax / 1000.0)
        ax.set_ylim(ymin / 1000.0, ymax / 1000.0)

        # Plot reference point (star) and max subsidence location (triangle)
        ref_x, ref_y = tr.transform(summ["reference_point"]["lon"], summ["reference_point"]["lat"])
        max_x, max_y = tr.transform(summ["max_subsidence_location"]["lon"], summ["max_subsidence_location"]["lat"])
        ax.plot(ref_x / 1000.0, ref_y / 1000.0, marker="*", color="#111111", markersize=9, markeredgecolor="white", markeredgewidth=0.6, label="Ref")
        ax.plot(max_x / 1000.0, max_y / 1000.0, marker="v", color="#7f0000", markersize=7, markeredgecolor="white", markeredgewidth=0.6, label="Max")

        t0, t1 = summ["period"]
        max_los = summ["max_subsidence_cm"]
        rate_los = summ["rate_cm_per_yr_estimate"]
        ax.set_title(
            f"{p['title']}\nMax: {max_los:.1f} cm LOS (~{rate_los:.1f} cm/yr est.)\n{t0} to {t1} ({summ['n_pairs']} pairs)",
            fontsize=10.5,
            fontweight="bold",
            pad=8,
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#cbd5e1")
            sp.set_linewidth(0.8)

    fig.subplots_adjust(left=0.02, right=0.92, top=0.80, bottom=0.14, wspace=0.08)
    cbar_ax = fig.add_axes([0.935, 0.16, 0.015, 0.62])
    cbar = fig.colorbar(im_ref, cax=cbar_ax, extend="both")
    cbar.set_label("Cumulative LOS displacement (cm)\n(negative = subsidence)", fontsize=9.5)

    fig.suptitle(
        "Same NISAR Engine, Four Sinking Regions (Provisional L2 GUNW, CRID P05023)",
        fontsize=13.5,
        fontweight="bold",
        y=0.96,
    )
    fig.text(
        0.5,
        0.04,
        "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team. "
        "Markers: black star = stable reference window; dark-red triangle = 1 km block peak subsidence.",
        ha="center",
        fontsize=8.5,
        color="#475569",
    )

    out_path = ROOT / "docs" / "story" / "media" / "pc10_global.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    print(f"Saved {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
