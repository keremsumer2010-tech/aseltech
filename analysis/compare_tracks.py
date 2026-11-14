"""Q21 · Independent check: track 34 (ascending) vs track 114 (descending) over the Central Valley.

Two different orbits look at the same ground from opposite sides. If the signal is real ground motion
(mostly vertical in pumping areas), both must show it; atmosphere and unwrapping errors are independent.

Method
1. Load both cumulative stacks (analysis/out/<site>_cum_stack.npz, LOS cm, each referenced to its own
   stable window) and incidence angles (analysis/out/<site>_cum.npz).
2. Interpolate track 114 linearly in time onto track 34's dates inside the common span and re-zero it at the
   first common date (both then measure motion since the same day).
3. Resample track 114 onto track 34's UTM grid (nearest pixel; same EPSG required).
4. Convert both to a vertical estimate, LOS / cos(incidence) (assumes purely vertical motion; horizontal
   motion would make the two disagree in opposite directions, which is itself informative: see Q22).
5. Average in ~1 km blocks (13 x 13 px, >= 50 % valid) and compare: Pearson r, RMSE, median difference,
   orthogonal-free least-squares slope. Scatter plot + difference map -> docs/cv_p34_vs_p114.png.
Usage: python analysis/compare_tracks.py
"""
from __future__ import annotations

import json
import sys
import warnings
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis" / "out"
BLOCK, MIN_VALID = 13, 0.5


def days(d):
    return np.array([(date.fromisoformat(str(x)) - date(2026, 1, 1)).days for x in d], float)


def interp_stack(stack, t_src, t_dst):
    """Linear interpolation in time, per pixel, of a (T, H, W) stack onto t_dst (must lie inside t_src)."""
    out = np.empty((len(t_dst),) + stack.shape[1:], np.float32)
    for k, t in enumerate(t_dst):
        j = int(np.clip(np.searchsorted(t_src, t) - 1, 0, len(t_src) - 2))
        w = (t - t_src[j]) / (t_src[j + 1] - t_src[j])
        out[k] = (1 - w) * stack[j] + w * stack[j + 1]
    return out


def resample_to(arr, xs, ys, xd, yd):
    ix = np.rint((xd - xs[0]) / (xs[1] - xs[0])).astype(int)
    iy = np.rint((yd - ys[0]) / (ys[1] - ys[0])).astype(int)
    okx = (ix >= 0) & (ix < len(xs))
    oky = (iy >= 0) & (iy < len(ys))
    out = np.full(arr.shape[:-2] + (len(yd), len(xd)), np.nan, np.float32)
    sub = arr[..., iy[oky][:, None], ix[okx][None, :]]
    out[..., np.where(oky)[0][:, None], np.where(okx)[0][None, :]] = sub
    return out


def blocks(a):
    H, W = a.shape
    Hp, Wp = H // BLOCK * BLOCK, W // BLOCK * BLOCK
    t = a[:Hp, :Wp].reshape(Hp // BLOCK, BLOCK, Wp // BLOCK, BLOCK)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        m = np.nanmean(t, axis=(1, 3))
    m[np.isfinite(t).mean(axis=(1, 3)) < MIN_VALID] = np.nan
    return m


def main(a_site="central_valley", b_site="central_valley_p114"):
    A = np.load(OUT / f"{a_site}_cum_stack.npz")
    B = np.load(OUT / f"{b_site}_cum_stack.npz")
    Ai = np.load(OUT / f"{a_site}_cum.npz")["incidence"].astype(np.float32)
    Bi = np.load(OUT / f"{b_site}_cum.npz")["incidence"].astype(np.float32)
    if int(A["epsg"]) != int(B["epsg"]):
        raise SystemExit("different EPSG; BLOCKED (reprojection not implemented)")
    ta, tb = days(A["dates"]), days(B["dates"])
    keep = (ta >= tb[0]) & (ta <= tb[-1])
    dates = [str(d) for d in np.array(A["dates"])[keep]]
    sa = A["cum_stack_cm"].astype(np.float32)[keep]
    sa = sa - sa[0]
    sb = interp_stack(B["cum_stack_cm"].astype(np.float32), tb, ta[keep])
    sb = sb - sb[0]
    sb = resample_to(sb, B["x"], B["y"], A["x"], A["y"])
    bi = resample_to(Bi, B["x"], B["y"], A["x"], A["y"])
    va = sa[-1] / np.cos(np.deg2rad(Ai))
    vb = sb[-1] / np.cos(np.deg2rad(bi))
    ba, bb = blocks(va), blocks(vb)
    ok = np.isfinite(ba) & np.isfinite(bb)
    x, y = ba[ok], bb[ok]
    r = float(np.corrcoef(x, y)[0, 1])
    rmse = float(np.sqrt(np.mean((x - y) ** 2)))
    slope = float(np.polyfit(x, y, 1)[0])
    stats = {
        "common_period": [dates[0], dates[-1]], "n_blocks_1km": int(ok.sum()),
        "pearson_r": round(r, 3), "rmse_cm": round(rmse, 2), "median_diff_cm": round(float(np.median(y - x)), 2),
        "slope_p114_vs_p34": round(slope, 3),
        "p34_vertical_p2_p50": [round(float(v), 2) for v in np.percentile(x, [2, 50])],
        "p114_vertical_p2_p50": [round(float(v), 2) for v in np.percentile(y, [2, 50])],
        "note": ("vertical estimate = LOS/cos(incidence) for each track; track 114 interpolated in time to "
                 "track 34 dates and re-zeroed at the first common date; ~1 km block means"),
    }
    (OUT / "cv_p34_vs_p114.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(1, 2, figsize=(12, 5.2))
    lim = float(np.ceil(np.nanpercentile(np.abs(np.r_[x, y]), 99.5)))
    ax[0].hexbin(x, y, gridsize=60, cmap="viridis", mincnt=1, extent=(-lim, lim, -lim, lim))
    ax[0].plot([-lim, lim], [-lim, lim], "w--", lw=1)
    ax[0].set_xlabel("Track 34 ascending — vertical estimate (cm)")
    ax[0].set_ylabel("Track 114 descending — vertical estimate (cm)")
    ax[0].set_title(f"{dates[0]} → {dates[-1]} · 1 km blocks · r = {r:.2f}, RMSE = {rmse:.1f} cm, n = {ok.sum()}", fontsize=9)
    d = bb - ba
    im = ax[1].imshow(d, cmap="PuOr", vmin=-4, vmax=4)
    fig.colorbar(im, ax=ax[1], shrink=0.8, label="Track 114 − Track 34 (cm, vertical estimate)")
    ax[1].set_title("Difference map (1 km blocks)", fontsize=9)
    ax[1].set_xticks([]); ax[1].set_yticks([])
    fig.suptitle("Central Valley · NISAR GUNW PROVISIONAL · two independent orbits", fontsize=11)
    fig.text(0.01, 0.01, "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
             "(NASA-JPL and ISRO), not by our team.", fontsize=7)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(ROOT / "docs" / "cv_p34_vs_p114.png", dpi=110)
    print(json.dumps(stats, indent=1))
    return stats


if __name__ == "__main__":
    main(*sys.argv[1:3])
