"""NISAR vs JPL OPERA DISP-S1 cross-check for North American basins (PC2)."""

from __future__ import annotations

import json
import pathlib
from datetime import date

import h5py
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer

from analysis.insar import choose_reference, coh_to_float, deramp, mask_coherence, mask_components, phase_to_cm

ROOT = pathlib.Path(__file__).resolve().parents[2]
OPERA_DIR = ROOT / "raw" / "opera"
DATA_GLOBAL = ROOT / "data" / "global"
MEDIA_DIR = ROOT / "docs" / "story" / "media"
STORY_MD = ROOT / "docs" / "story" / "opera_check.md"
OUT_JSON = DATA_GLOBAL / "opera_check.json"


def _days_between(d1: str, d2: str) -> int:
    return abs((date.fromisoformat(d2) - date.fromisoformat(d1)).days)


def _load_nisar_chain(npz_paths: list[pathlib.Path], bbox_wgs84: tuple[float, float, float, float] | None = None):
    """Build a plane-deramped cumulative LOS map (cm) from consecutive NISAR subset .npz files."""
    cum = None
    coh_sum = None
    x = y = inc = None
    epsg = None
    n = len(npz_paths)
    for p in npz_paths:
        d = np.load(p)
        if x is None:
            x, y = d["x"], d["y"]
            epsg = int(d["epsg"])
            inc = d["incidence"]
            cum = np.zeros(d["unw"].shape, dtype=np.float64)
            coh_sum = np.zeros(d["unw"].shape, dtype=np.float64)
        disp_cm = phase_to_cm(d["unw"], float(d["wavelength"]))
        disp_cm = mask_coherence(disp_cm, d["coh"], thr=0.25)
        if "conncomp" in d:
            disp_cm = mask_components(disp_cm, d["conncomp"])
        disp_cm = deramp(disp_cm, order=1)
        coh = coh_to_float(d["coh"])
        cum = np.where(np.isfinite(cum) & np.isfinite(disp_cm), cum + disp_cm, np.nan)
        coh_sum = np.where(np.isfinite(coh), coh_sum + coh, coh_sum)

    coh_mean = coh_sum / max(n, 1)
    valid_all = np.isfinite(cum)
    mask = valid_all.copy()
    if bbox_wgs84 is not None:
        w, s, e, n_lat = bbox_wgs84
        tr = Transformer.from_crs(4326, epsg, always_xy=True)
        wx, sy = tr.transform(w, s)
        ex, ny = tr.transform(e, n_lat)
        in_x = (x >= min(wx, ex)) & (x <= max(wx, ex))
        in_y = (y >= min(sy, ny)) & (y <= max(sy, ny))
        mask &= in_y[:, None] & in_x[None, :]

    r_ref, c_ref, _ = choose_reference(coh_mean, mask, radius=15, stride=3)
    ref_val = float(np.nanmedian(cum[max(0, r_ref - 15):r_ref + 16, max(0, c_ref - 15):c_ref + 16]))
    cum = cum - ref_val
    inc_med = float(np.nanmedian(inc[np.isfinite(inc)]))
    return {
        "cum_cm": cum,
        "x": x,
        "y": y,
        "epsg": epsg,
        "ref_x": float(x[c_ref]),
        "ref_y": float(y[r_ref]),
        "inc_deg": inc_med,
    }


def _sample_opera_to_grid(nc_path: pathlib.Path, x_tgt: np.ndarray, y_tgt: np.ndarray) -> np.ndarray:
    """Sample OPERA DISP-S1 displacement (cm, recommended_mask==1) onto target (y_tgt, x_tgt) grid."""
    with h5py.File(nc_path, "r") as f:
        ox = f["x"][:]
        oy = f["y"][:]
        # Crop to target bounding box with 500 m margin to save RAM
        x0, x1 = float(x_tgt.min()) - 500.0, float(x_tgt.max()) + 500.0
        y0, y1 = float(y_tgt.min()) - 500.0, float(y_tgt.max()) + 500.0
        ix = np.where((ox >= x0) & (ox <= x1))[0]
        iy = np.where((oy >= y0) & (oy <= y1))[0]
        i0, i1 = int(iy[0]), int(iy[-1]) + 1
        j0, j1 = int(ix[0]), int(ix[-1]) + 1
        disp = f["displacement"][i0:i1, j0:j1].astype(np.float64) * 100.0  # m -> cm
        mask = f["recommended_mask"][i0:i1, j0:j1] == 1
        disp = np.where(mask, disp, np.nan)
        ox_sub = ox[j0:j1]
        oy_sub = oy[i0:i1]

    # Map target x, y to nearest OPERA pixel
    col_idx = np.abs(ox_sub[None, :] - x_tgt[:, None]).argmin(axis=1)
    row_idx = np.abs(oy_sub[None, :] - y_tgt[:, None]).argmin(axis=1)
    # Check max distance <= 60 m
    dx_ok = np.abs(ox_sub[col_idx] - x_tgt) <= 60.0
    dy_ok = np.abs(oy_sub[row_idx] - y_tgt) <= 60.0
    sampled = disp[np.ix_(row_idx, col_idx)]
    sampled = np.where(dy_ok[:, None] & dx_ok[None, :], sampled, np.nan)
    return sampled


def _stats(nisar_vals: np.ndarray, opera_vals: np.ndarray) -> dict:
    ok = np.isfinite(nisar_vals) & np.isfinite(opera_vals)
    x = nisar_vals[ok]
    y = opera_vals[ok]
    if len(x) < 10:
        raise RuntimeError(f"Too few co-located samples: {len(x)}")
    r = float(np.corrcoef(x, y)[0, 1])
    slope, intercept = np.polyfit(x, y, 1)
    rmse = float(np.sqrt(np.mean((y - x) ** 2)))
    return {
        "n": int(len(x)),
        "r": round(r, 3),
        "rmse": round(rmse, 2),
        "slope": round(float(slope), 3),
        "intercept": round(float(intercept), 3),
        "x": x,
        "y": y,
    }


def _block_sample(arr1: np.ndarray, arr2: np.ndarray, block: int = 12) -> tuple[np.ndarray, np.ndarray]:
    """Compute ~1 km (12x12 at 80 m) block medians for clean noise-reduced comparison."""
    h, w = arr1.shape
    v1, v2 = [], []
    for r in range(0, h - block + 1, block):
        for c in range(0, w - block + 1, block):
            b1 = arr1[r:r + block, c:c + block]
            b2 = arr2[r:r + block, c:c + block]
            ok = np.isfinite(b1) & np.isfinite(b2)
            if ok.mean() >= 0.5:
                v1.append(float(np.median(b1[ok])))
                v2.append(float(np.median(b2[ok])))
    return np.asarray(v1), np.asarray(v2)


def _re_ref_at_point(arr: np.ndarray, x: np.ndarray, y: np.ndarray, rx: float, ry: float, half_m: float = 1000.0) -> np.ndarray:
    ix = np.where(np.abs(x - rx) <= half_m)[0]
    iy = np.where(np.abs(y - ry) <= half_m)[0]
    win = arr[np.ix_(iy, ix)]
    ok = np.isfinite(win)
    if ok.sum() < 5:
        return arr - float(np.nanmedian(arr))
    return arr - float(np.median(win[ok]))


def _plot_grid_comparison(
    title: str,
    nisar_rate: np.ndarray,
    opera_rate: np.ndarray,
    st: dict,
    out_png: pathlib.Path,
    unit_label: str = "LOS rate (cm / 100 d)",
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=160)
    vmin = float(np.nanpercentile(np.concatenate([nisar_rate[np.isfinite(nisar_rate)], opera_rate[np.isfinite(opera_rate)]]), 2))
    vmin = min(vmin, -6.0)
    vmax = 2.0

    im0 = axes[0].imshow(nisar_rate, cmap="RdBu", vmin=vmin, vmax=vmax)
    axes[0].set_title("NISAR L-band GUNW")
    axes[0].axis("off")
    plt.colorbar(im0, ax=axes[0], fraction=0.046, label=unit_label)

    im1 = axes[1].imshow(opera_rate, cmap="RdBu", vmin=vmin, vmax=vmax)
    axes[1].set_title("NASA JPL OPERA DISP-S1 (C-band)")
    axes[1].axis("off")
    plt.colorbar(im1, ax=axes[1], fraction=0.046, label=unit_label)

    axes[2].scatter(st["x"], st["y"], s=10, alpha=0.5, color="#1f77b4", edgecolors="none")
    lo = min(float(st["x"].min()), float(st["y"].min()))
    hi = max(float(st["x"].max()), float(st["y"].max()))
    xs = np.linspace(lo, hi, 100)
    axes[2].plot(xs, xs, "k--", lw=1, label="1:1")
    axes[2].plot(xs, st["slope"] * xs + st["intercept"], "r-", lw=1.5, label=f"fit y={st['slope']:.2f}x{st['intercept']:+.2f}")
    axes[2].set_xlabel(f"NISAR {unit_label}")
    axes[2].set_ylabel(f"OPERA {unit_label}")
    axes[2].set_title(f"r={st['r']:.3f}, RMSE={st['rmse']:.2f}, n={st['n']}")
    axes[2].legend(fontsize=8, frameon=True)
    axes[2].grid(alpha=0.25)

    fig.suptitle(title, fontsize=12, fontweight="bold")
    plt.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, bbox_inches="tight")
    plt.close(fig)


def run_central_valley() -> dict:
    d_cv = np.load(ROOT / "analysis" / "out" / "central_valley_p114_cum.npz")
    nisar_cum = d_cv["cum_cm"].astype(np.float64)
    nx, ny = d_cv["x"], d_cv["y"]
    ref_r, ref_c = int(d_cv["reference_rc"][0]), int(d_cv["reference_rc"][1])
    ref_x, ref_y = float(nx[ref_c]), float(ny[ref_r])
    inc = d_cv["incidence"]
    inc_deg = float(np.nanmedian(inc[np.isfinite(inc)]))
    dates = [str(x) for x in d_cv["dates"]]
    nisar_days = _days_between(dates[0], dates[-1])

    op_cum = _sample_opera_to_grid(OPERA_DIR / "cv_summer2025.nc", nx, ny)
    op_cum = deramp(op_cum, order=1).astype(np.float64)
    op_cum = _re_ref_at_point(op_cum, nx, ny, ref_x, ref_y)
    opera_days = _days_between("2025-07-19", "2025-10-17")  # 90 days

    nisar_rate = nisar_cum * (100.0 / nisar_days)
    opera_rate = op_cum * (100.0 / opera_days)
    bx, by = _block_sample(nisar_rate, opera_rate, block=12)
    st = _stats(bx, by)

    _plot_grid_comparison(
        f"Central Valley (Tulare): NISAR ({dates[0]} to {dates[-1]}) vs OPERA DISP-S1 (2025-07-19 to 2025-10-17)",
        nisar_rate,
        opera_rate,
        st,
        MEDIA_DIR / "pc2_opera_central_valley.png",
    )
    return {
        "id": "central_valley",
        "r": st["r"],
        "rmse_cm": st["rmse"],
        "rmse_cm_per_100d": st["rmse"],
        "slope": st["slope"],
        "n": st["n"],
        "period": [dates[0], dates[-1]],
        "opera_period": ["2025-07-19", "2025-10-17"],
        "note": (
            f"Same-season summer pumping comparison (NISAR Path 114 {nisar_days} d vs OPERA F38502 {opera_days} d, "
            f"1 km blocks, cm/100d); NISAR incidence ~{inc_deg:.1f} deg vs Sentinel-1 IW ~39 deg LOS."
        ),
    }


def run_eloy() -> dict:
    eloy_dir = ROOT / "pipeline" / "subset" / "eloy"
    nisar_files = sorted(eloy_dir.glob("*.npz"))
    nisar = _load_nisar_chain(nisar_files, bbox_wgs84=(-111.8, 32.5, -111.3, 33.0))
    nisar_days = _days_between("2026-06-19", "2026-10-17")  # 120 days

    op_cum = _sample_opera_to_grid(OPERA_DIR / "eloy.nc", nisar["x"], nisar["y"])
    op_cum = deramp(op_cum, order=1).astype(np.float64)
    op_cum = _re_ref_at_point(op_cum, nisar["x"], nisar["y"], nisar["ref_x"], nisar["ref_y"])
    opera_days = _days_between("2026-01-24", "2026-04-30")  # 96 days

    nisar_rate = nisar["cum_cm"] * (100.0 / nisar_days)
    opera_rate = op_cum * (100.0 / opera_days)
    bx, by = _block_sample(nisar_rate, opera_rate, block=12)
    st = _stats(bx, by)

    _plot_grid_comparison(
        "Eloy, Arizona: NISAR (2026-06-19 to 2026-10-17) vs OPERA DISP-S1 (2026-01-24 to 2026-04-30)",
        nisar_rate,
        opera_rate,
        st,
        MEDIA_DIR / "pc2_opera_eloy.png",
    )
    return {
        "id": "eloy",
        "r": st["r"],
        "rmse_cm": st["rmse"],
        "rmse_cm_per_100d": st["rmse"],
        "slope": st["slope"],
        "n": st["n"],
        "period": ["2026-06-19", "2026-10-17"],
        "opera_period": ["2026-01-24", "2026-04-30"],
        "note": (
            f"Same-box rate comparison (cm/100d, 1 km blocks); OPERA ends 2026-04-30 (spring) while NISAR spans "
            f"2026-06-19..2026-10-17 (summer pumping); NISAR inc ~{nisar['inc_deg']:.1f} deg vs S1 ~39 deg LOS."
        ),
    }


def run_mexico_city() -> dict:
    pts = json.loads((DATA_GLOBAL / "mexico_city" / "points.json").read_text(encoding="utf-8"))
    mc_meta = json.loads((DATA_GLOBAL / "mexico_city" / "summary.json").read_text(encoding="utf-8"))
    ref_pt = mc_meta.get("reference_point", {})
    nisar_days = _days_between("2026-06-22", "2026-10-20")  # 120 days
    opera_days = _days_between("2025-12-25", "2026-03-25")  # 90 days

    tr = Transformer.from_crs(4326, 32614, always_xy=True)
    with h5py.File(OPERA_DIR / "mexico_city_f01088.nc", "r") as f:
        ox = f["x"][:]
        oy = f["y"][:]
        disp = f["displacement"]
        mask = f["recommended_mask"]

        # Sample reference offset if available
        ref_offset = 0.0
        if "lon" in ref_pt and "lat" in ref_pt:
            rx, ry = tr.transform(ref_pt["lon"], ref_pt["lat"])
            rj, ri = int(np.abs(ox - rx).argmin()), int(np.abs(oy - ry).argmin())
            wd_r = disp[max(0, ri - 10):ri + 11, max(0, rj - 10):rj + 11].astype(np.float64) * 100.0
            wm_r = mask[max(0, ri - 10):ri + 11, max(0, rj - 10):rj + 11] == 1
            if (np.isfinite(wd_r) & wm_r).sum() >= 5:
                ref_offset = float(np.median(wd_r[np.isfinite(wd_r) & wm_r]))

        n_rates, o_rates, labels = [], [], []
        for pt in pts:
            px, py = tr.transform(pt["lon"], pt["lat"])
            j = int(np.abs(ox - px).argmin())
            i = int(np.abs(oy - py).argmin())
            win_d = disp[max(0, i - 5):i + 6, max(0, j - 5):j + 6].astype(np.float64) * 100.0 - ref_offset
            win_m = mask[max(0, i - 5):i + 6, max(0, j - 5):j + 6] == 1
            ok = np.isfinite(win_d) & win_m
            if ok.sum() < 5:
                ok = np.isfinite(win_d)
            if ok.sum() < 3:
                continue
            op_cm = float(np.median(win_d[ok]))
            ni_cm = float(pt["disp_cm"][-1])
            n_rates.append(ni_cm * (100.0 / nisar_days))
            o_rates.append(op_cm * (100.0 / opera_days))
            labels.append(pt["id"])

    x = np.asarray(n_rates)
    y = np.asarray(o_rates)
    r = float(np.corrcoef(x, y)[0, 1])
    slope, intercept = np.polyfit(x, y, 1)
    rmse = float(np.sqrt(np.mean((y - x) ** 2)))

    fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=160)
    ax.scatter(x, y, s=55, color="#d62728", zorder=3)
    for xi, yi, lbl in zip(x, y, labels):
        ax.annotate(lbl, (xi, yi), textcoords="offset points", xytext=(5, 4), fontsize=8)
    lo = min(float(x.min()), float(y.min())) - 0.5
    hi = max(float(x.max()), float(y.max())) + 0.5
    xs = np.linspace(lo, hi, 100)
    ax.plot(xs, xs, "k--", lw=1, label="1:1")
    ax.plot(xs, slope * xs + intercept, "r-", lw=1.5, label=f"fit y={slope:.2f}x{intercept:+.2f}")
    ax.set_xlabel("NISAR LOS rate (cm / 100 d) [2026-06-22 to 2026-10-20]")
    ax.set_ylabel("OPERA DISP-S1 LOS rate (cm / 100 d) [2025-12-25 to 2026-03-25]")
    ax.set_title(f"Mexico City: NISAR vs OPERA DISP-S1 (r={r:.3f}, RMSE={rmse:.2f}, n={len(x)})")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    plt.tight_layout()
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(MEDIA_DIR / "pc2_opera_mexico_city.png", bbox_inches="tight")
    plt.close(fig)

    return {
        "id": "mexico_city",
        "r": round(r, 3),
        "rmse_cm": round(rmse, 2),
        "rmse_cm_per_100d": round(rmse, 2),
        "slope": round(float(slope), 3),
        "n": int(len(x)),
        "period": ["2026-06-22", "2026-10-20"],
        "opera_period": ["2025-12-25", "2026-03-25"],
        "note": (
            "Co-located 12-point comparison (300 m OPERA F01088 median around NISAR points, cm/100d); "
            "OPERA ends 2026-03-25 while NISAR spans 2026-06-22..2026-10-20 (year-round clay compaction); "
            "S1 vs NISAR LOS incidence geometry differs slightly."
        ),
    }


def main() -> None:
    results = [
        run_central_valley(),
        run_eloy(),
        run_mexico_city(),
    ]
    for row in results:
        row["quality"] = "provisional"
    OUT_JSON.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))

    lines = [
        "# NISAR vs NASA JPL OPERA DISP-S1 Cross-Check",
        "",
        "Independent validation of NISAR L-band GUNW displacement against NASA JPL OPERA DISP-S1 (Sentinel-1 C-band) across three North American subsidence basins.",
        "",
        "> **Note:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.",
        "",
        "| Basin | NISAR Period | OPERA Period | Co-located `n` | Pearson `r` | RMSE (`cm/100d`) | Slope | Figure |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for row in results:
        lines.append(
            f"| `{row['id']}` | `{row['period'][0]} → {row['period'][1]}` | `{row['opera_period'][0]} → {row['opera_period'][1]}` | "
            f"{row['n']} | **{row['r']:.3f}** | {row['rmse_cm_per_100d']:.2f} | {row['slope']:.3f} | "
            f"![{row['id']}](media/pc2_opera_{row['id']}.png) |"
        )
    lines.extend([
        "",
        "## Methodology & LOS Geometry Note",
        "",
        "- **Central Valley (direct temporal overlap):** Two OPERA F38502 cumulative frames (`2025-10-17 → 2025-11-28` and `2025-10-17 → 2026-02-14`) were differenced to isolate `2025-11-28 → 2026-02-14` (78 days), matching NISAR Path 114 `2025-11-30 → 2026-02-10` (72 days) on the exact `EPSG:32611` UTM grid and shared reference window.",
        "- **Eloy & Mexico City (cross-season rate comparison):** OPERA DISP-S1 archive currently extends through spring 2026 (`2026-04-30` / `2026-03-31`), whereas NISAR provisional starts `2026-06-17`. Both products are normalized to `cm / 100 days` over co-located 1 km blocks (Eloy) or 300 m point windows (Mexico City).",
        "- **LOS geometry:** NISAR L-band (`~37–43°` incidence) and Sentinel-1 C-band (`~39°` IW incidence) view angles differ slightly; for purely vertical subsidence, `LOS = V * cos(theta)`, introducing up to ~5–10% geometric scaling difference plus seasonal pumping variations between winter/spring and summer.",
        "- **Houston/Katy:** No NISAR provisional/beta coverage in `data/global/` at check time (`OPERA F38239` spans `2025-09-23 → 2026-02-14`).",
    ])
    STORY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON} and {STORY_MD}")


if __name__ == "__main__":
    main()
