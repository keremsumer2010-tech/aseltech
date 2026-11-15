"""Generate shared-scale thumbnail maps (±10 cm LOS, 400px) and common colorbar.

Outputs:
- data/konya_plain/thumb.png
- data/central_valley/thumb.png
- data/global/eloy/thumb.png
- data/global/kashmar/thumb.png
- data/global/mashhad/thumb.png
- data/global/semarang/thumb.png
- docs/story/media/pc10_colorbar.png

Scale: [-10.0, +10.0] cm LOS (RdBu colormap: red = subsidence, blue = uplift/toward satellite).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]

TARGETS = [
    {
        "id": "konya_plain",
        "disp_png": ROOT / "data" / "konya_plain" / "disp" / "2026-09-30.png",
        "meta": ROOT / "data" / "konya_plain" / "meta.json",
        "out_thumb": ROOT / "data" / "konya_plain" / "thumb.png",
    },
    {
        "id": "central_valley",
        "disp_png": ROOT / "data" / "central_valley" / "disp" / "2026-09-20.png",
        "meta": ROOT / "data" / "central_valley" / "meta.json",
        "out_thumb": ROOT / "data" / "central_valley" / "thumb.png",
    },
    {
        "id": "eloy",
        "disp_png": ROOT / "data" / "global" / "eloy" / "disp" / "2026-09-23.png",
        "meta": ROOT / "data" / "global" / "eloy" / "meta.json",
        "out_thumb": ROOT / "data" / "global" / "eloy" / "thumb.png",
    },
    {
        "id": "kashmar",
        "disp_png": ROOT / "data" / "global" / "kashmar" / "disp" / "2026-09-23.png",
        "meta": ROOT / "data" / "global" / "kashmar" / "meta.json",
        "out_thumb": ROOT / "data" / "global" / "kashmar" / "thumb.png",
    },
    {
        "id": "mashhad",
        "disp_png": ROOT / "data" / "global" / "mashhad" / "disp" / "2026-09-23.png",
        "meta": ROOT / "data" / "global" / "mashhad" / "meta.json",
        "out_thumb": ROOT / "data" / "global" / "mashhad" / "thumb.png",
    },
    {
        "id": "semarang",
        "disp_png": ROOT / "data" / "global" / "semarang" / "disp" / "2026-09-29.png",
        "meta": ROOT / "data" / "global" / "semarang" / "meta.json",
        "out_thumb": ROOT / "data" / "global" / "semarang" / "thumb.png",
    },
]

VMIN, VMAX = -10.0, 10.0


def make_colorbar(out_path: Path) -> None:
    """Generate shared horizontal colorbar for ±10 cm LOS scale."""
    fig = plt.figure(figsize=(7.0, 1.3), dpi=200)
    fig.patch.set_facecolor("#ffffff")
    ax = fig.add_axes([0.08, 0.45, 0.84, 0.22])

    cmap = plt.get_cmap("RdBu")
    norm = Normalize(vmin=VMIN, vmax=VMAX)

    cb = ColorbarBase(ax, cmap=cmap, norm=norm, orientation="horizontal")
    cb.set_label("LOS Cumulative Displacement (cm) [Shared ±10 cm scale]", fontsize=10, weight="bold", labelpad=8)
    cb.set_ticks([-10, -5, 0, 5, 10])
    cb.set_ticklabels(["-10 (subsidence)", "-5", "0", "+5", "+10 (uplift)"])
    cb.ax.tick_params(labelsize=8)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"Saved colorbar: {out_path}")


def rescale_and_crop(disp_png_path: Path, meta_path: Path, out_path: Path, target_size: int = 400) -> None:
    """Read original disp PNG, remap from [orig_vmin, orig_vmax] to [-10, +10], and save square thumbnail."""
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    orig_vmin = float(meta.get("vmin", -8.0))
    orig_vmax = float(meta.get("vmax", 8.0))

    img = Image.open(disp_png_path).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    valid_mask = alpha > 0

    cmap = plt.get_cmap("RdBu")
    table_t = np.linspace(0, 1, 1000)
    table_rgb = (cmap(table_t)[:, :3] * 255).astype(np.int32)

    rgb_pixels = arr[valid_mask, :3].astype(np.int32)
    recovered_t = np.empty(len(rgb_pixels), dtype=np.float32)

    # Chunked lookup to find original normalized value t in [0, 1]
    for i in range(0, len(rgb_pixels), 50000):
        chunk = rgb_pixels[i:i + 50000]
        dists = np.sum((chunk[:, None, :] - table_rgb[None, :, :]) ** 2, axis=-1)
        best = np.argmin(dists, axis=-1)
        recovered_t[i:i + 50000] = table_t[best]

    # Map recovered t to physical displacement (cm)
    disp_cm = orig_vmin + recovered_t * (orig_vmax - orig_vmin)

    # Map displacement to new shared scale [-10, +10]
    new_norm = np.clip((disp_cm - VMIN) / (VMAX - VMIN), 0.0, 1.0)
    new_rgba = (cmap(new_norm) * 255).astype(np.uint8)

    rescaled_arr = np.zeros_like(arr)
    rescaled_arr[valid_mask, :3] = new_rgba[:, :3]
    rescaled_arr[valid_mask, 3] = alpha[valid_mask]

    rescaled_img = Image.fromarray(rescaled_arr, "RGBA")

    # Center crop / fit to square with transparent background
    w, h = rescaled_img.size
    max_dim = max(w, h)
    square_img = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
    offset = ((max_dim - w) // 2, (max_dim - h) // 2)
    square_img.paste(rescaled_img, offset)

    thumb = square_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    thumb.save(out_path, "PNG")
    print(f"Saved {out_path.name} for {meta.get('site', disp_png_path.parent.parent.name)}: {thumb.size}")


def main() -> None:
    print("Generating shared-scale thumbnails...")
    for t in TARGETS:
        rescale_and_crop(t["disp_png"], t["meta"], t["out_thumb"], target_size=400)

    colorbar_path = ROOT / "docs" / "story" / "media" / "pc10_colorbar.png"
    make_colorbar(colorbar_path)
    print("Done generating thumbnails and colorbar.")


if __name__ == "__main__":
    main()
