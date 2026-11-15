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

# Shared ±10 cm scale bounds
VMIN, VMAX = -10.0, 10.0


def discover_all_targets() -> list[dict]:
    """Discover all sites with meta.json and disp/*.png in data/global, konya_plain, central_valley, karapinar."""
    targets = []
    candidate_dirs = [
        ROOT / "data" / "konya_plain",
        ROOT / "data" / "central_valley",
        ROOT / "data" / "karapinar",
    ]
    global_dir = ROOT / "data" / "global"
    if global_dir.is_dir():
        candidate_dirs.extend(sorted(global_dir.iterdir()))

    seen = set()
    for d in candidate_dirs:
        if not d.is_dir():
            continue
        meta_p = d / "meta.json"
        disp_dir = d / "disp"
        if not (meta_p.exists() and disp_dir.is_dir()):
            continue
        disp_pngs = sorted([p for p in disp_dir.glob("*.png") if not p.name.startswith(".")])
        if not disp_pngs:
            continue
        site_id = d.name
        if site_id in seen:
            continue
        seen.add(site_id)
        targets.append({
            "id": site_id,
            "disp_png": disp_pngs[-1],
            "meta": meta_p,
            "out_thumb": d / "thumb.png",
        })
    return targets


def update_meta_json(meta_path: Path) -> None:
    """Ensure thumb and thumb_scale fields are present in meta.json."""
    try:
        content = meta_path.read_text(encoding="utf-8")
        data = json.loads(content)
        changed = False
        if data.get("thumb") != "thumb.png":
            data["thumb"] = "thumb.png"
            changed = True
        if data.get("thumb_scale") != [VMIN, VMAX]:
            data["thumb_scale"] = [VMIN, VMAX]
            changed = True
        if changed:
            meta_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"Updated meta.json for {meta_path.parent.name}")
    except Exception as e:
        print(f"Warning: could not update meta {meta_path}: {e}")


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
    targets = discover_all_targets()
    print(f"Discovered {len(targets)} targets with displacement maps.")
    for t in targets:
        rescale_and_crop(t["disp_png"], t["meta"], t["out_thumb"], target_size=400)
        update_meta_json(t["meta"])

    colorbar_path = ROOT / "docs" / "story" / "media" / "pc10_colorbar.png"
    make_colorbar(colorbar_path)
    print(f"Done generating thumbnails for {len(targets)} targets and colorbar.")
    print("Done generating thumbnails and colorbar.")


if __name__ == "__main__":
    main()
