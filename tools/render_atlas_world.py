"""Render the home-page world map from data/global/atlas.json on NASA Blue Marble (PC1).

Filled circle = reliable, ring = indicative; the five fastest reliable basins are labelled.
Writes docs/story/media/pc1_atlas_world.png and web/assets/atlas_world.{webp,jpg}.
Usage: python tools/render_atlas_world.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
atlas = json.loads((ROOT / "data/global/atlas.json").read_text(encoding="utf-8"))
bm = Image.open(ROOT / "web/assets/bluemarble_2k.jpg")

W, H = 1800, 650
LAT0, LAT1 = -45, 62
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(bm, extent=[-180, 180, -90, 90], aspect="auto")
ax.imshow([[0]], extent=[-180, 180, -90, 90], cmap="gray", alpha=0.25, aspect="auto")
ax.set_xlim(-130, 150)
ax.set_ylim(LAT0, LAT1)
ax.axis("off")


def colour(rate):
    if rate is None:
        return "#9aa3b0"
    if rate <= -6:
        return "#c8321f"
    if rate <= -4:
        return "#e8572e"
    if rate <= -2:
        return "#f39c3d"
    return "#f6d28a"


top = [r for r in atlas["regions"] if not r.get("indicative_only")][:5]
for r in atlas["regions"]:
    if r.get("lon") is None:
        continue
    rate = r.get("rate_cm_per_100d_common")
    size = 40 + 18 * min(abs(rate or 0), 12)
    if r.get("indicative_only"):
        ax.scatter(r["lon"], r["lat"], s=size, facecolors="none", edgecolors="#ffffff", linewidths=1.6, zorder=3)
    else:
        ax.scatter(r["lon"], r["lat"], s=size, c=colour(rate), edgecolors="#ffffff", linewidths=1.4, zorder=4)

offsets = [(-60, 28), (-40, -38), (14, 30), (16, -34), (30, 22)]
for i, r in enumerate(top):
    dx, dy = offsets[i % len(offsets)]
    ax.annotate(f"#{i + 1} {r['name'].split(' (')[0]}  {r['rate_cm_per_100d_common']:.1f}",
                (r["lon"], r["lat"]), xytext=(dx, dy), textcoords="offset points",
                fontsize=11, fontweight="bold", color="#0d1524",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.92),
                arrowprops=dict(arrowstyle="-", color="white", lw=1.2), zorder=6)

n, nr = atlas["n_regions"], atlas["n_reliable"]
ax.text(-128, LAT0 + 2, f"{n} basins · filled = reliable ({nr}), ring = indicative · cm per 100 days, common window · provisional NISAR data",
        fontsize=9, color="white", zorder=6)

out = ROOT / "docs/story/media/pc1_atlas_world.png"
fig.savefig(out, dpi=100)
im = Image.open(out).convert("RGB")
im.save(ROOT / "web/assets/atlas_world.webp", quality=84, method=6)
im.save(ROOT / "web/assets/atlas_world.jpg", quality=84, optimize=True, progressive=True)
print("wrote", out, [r["id"] for r in top])
