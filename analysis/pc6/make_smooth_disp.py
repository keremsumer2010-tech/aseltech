#!/usr/bin/env python3
"""Generate NaN-aware smoothed cumulative LOS displacement PNGs (7x7 mean + light Gaussian).

Writes:
  - data/central_valley/disp_smooth/<date>.png
  - data/karapinar/disp_smooth/<date>.png

Owner: PC6 (B23 / S-17)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter, uniform_filter

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis"))
from cumulative import save_png, to_latlon_grid  # noqa: E402


def nan_aware_smooth(arr: np.ndarray, box_size: int = 7, min_frac: float = 0.1, gauss_sigma: float = 1.0) -> np.ndarray:
    """7x7 NaN-aware box mean followed by light NaN-aware Gaussian smoothing."""
    valid = np.isfinite(arr)
    vals = np.where(valid, arr.astype(np.float32), 0.0)
    w = valid.astype(np.float32)

    mean_v = uniform_filter(vals, size=box_size, mode="constant", cval=0.0)
    mean_w = uniform_filter(w, size=box_size, mode="constant", cval=0.0)
    ok_box = mean_w >= min_frac
    box = np.where(ok_box, mean_v / np.where(ok_box, mean_w, 1.0), np.nan)

    valid2 = np.isfinite(box)
    vals2 = np.where(valid2, box, 0.0)
    w2 = valid2.astype(np.float32)
    g_v = gaussian_filter(vals2, sigma=gauss_sigma, mode="constant", cval=0.0)
    g_w = gaussian_filter(w2, sigma=gauss_sigma, mode="constant", cval=0.0)
    out = np.where(valid2 & (g_w > 0), g_v / np.where(g_w > 0, g_w, 1.0), np.nan)
    return out.astype(np.float32)


def build_site(site: str) -> int:
    meta = json.loads((ROOT / "data" / site / "meta.json").read_text(encoding="utf-8"))
    st = np.load(ROOT / "analysis" / "out" / f"{site}_cum_stack.npz")
    cube = st["cum_stack_cm"].astype(np.float32)
    x = st["x"]
    y = st["y"]
    epsg = int(st["epsg"])
    dates = [str(d) for d in st["dates"]]
    bbox = meta["bbox"]
    vmin = float(meta["vmin"])
    vmax = float(meta["vmax"])

    out_dir = ROOT / "data" / site / "disp_smooth"
    out_dir.mkdir(parents=True, exist_ok=True)
    for dt, g in zip(dates, cube):
        sm = nan_aware_smooth(g)
        ll = to_latlon_grid(sm, x, y, epsg, bbox)
        save_png(ll, out_dir / f"{dt}.png", vmin, vmax)
    print(f"{site}: wrote {len(dates)} smoothed PNGs to {out_dir}")
    return len(dates)


def main() -> None:
    for site in ("central_valley", "karapinar"):
        build_site(site)


if __name__ == "__main__":
    main()
