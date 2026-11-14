"""Run 5 diagnostic tests (a-e) explaining NISAR vs OPERA DISP-S1 correlation differences."""

from __future__ import annotations

import json
import pathlib
import sys

import h5py
import numpy as np
from pyproj import Transformer

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.insar import coh_to_float, deramp
from pipeline.pc2.opera_check import (
    DATA_GLOBAL,
    OPERA_DIR,
    _block_sample,
    _days_between,
    _load_nisar_chain,
    _re_ref_at_point,
    _sample_opera_to_grid,
    _stats,
)


def _mean_coherence(npz_paths: list[pathlib.Path]) -> np.ndarray:
    coh_sum = None
    for p in npz_paths:
        d = np.load(p)
        c = coh_to_float(d["coh"]).astype(np.float64)
        coh_sum = c if coh_sum is None else coh_sum + c
    return coh_sum / max(len(npz_paths), 1)


def _run_grid_5tests(
    name: str,
    nisar_rate_los: np.ndarray,
    opera_raw_cm: np.ndarray,
    opera_days: int,
    nx: np.ndarray,
    ny: np.ndarray,
    ref_x: float,
    ref_y: float,
    inc_deg: float,
    coh_mean: np.ndarray,
    nisar_period: tuple[str, str],
    opera_period: tuple[str, str],
) -> dict:
    # Baseline: deramp + re-ref + 1 km block
    op_deramped = deramp(opera_raw_cm, order=1).astype(np.float64)
    op_reref = _re_ref_at_point(op_deramped, nx, ny, ref_x, ref_y)
    op_rate_los = op_reref * (100.0 / opera_days)

    bx, by = _block_sample(nisar_rate_los, op_rate_los, block=12)
    base = _stats(bx, by)

    # (a) Temporal overlap
    n0, n1 = nisar_period
    o0, o1 = opera_period
    ov_days = max(0, (_days_between(max(n0, o0), min(n1, o1)) if max(n0, o0) <= min(n1, o1) else 0))

    # (b) Vertical conversion (cos theta)
    nisar_vert = nisar_rate_los / np.cos(np.deg2rad(inc_deg))
    opera_vert = op_rate_los / np.cos(np.deg2rad(39.0))
    bx_v, by_v = _block_sample(nisar_vert, opera_vert, block=12)
    test_b = _stats(bx_v, by_v)

    # (c) Reference point alignment (compare without re-referencing OPERA to NISAR ref)
    op_unaligned_rate = op_deramped * (100.0 / opera_days)
    bx_c, by_c = _block_sample(nisar_rate_los, op_unaligned_rate, block=12)
    test_c_unaligned = _stats(bx_c, by_c)

    # (d) Resolution / block averaging: 80m raw pixel (block=1), 1km (block=12), 2km (block=24)
    ok1 = np.isfinite(nisar_rate_los) & np.isfinite(op_rate_los)
    test_d_raw = _stats(nisar_rate_los[ok1][::4], op_rate_los[ok1][::4])
    bx_2k, by_2k = _block_sample(nisar_rate_los, op_rate_los, block=24)
    test_d_2km = _stats(bx_2k, by_2k)

    # (e) C-band vs L-band landcover split via NISAR coherence (urban/bare >=0.55 vs agri <0.55)
    high_coh = coh_mean >= 0.55
    low_coh = coh_mean < 0.55
    bx_hi, by_hi = _block_sample(np.where(high_coh, nisar_rate_los, np.nan), op_rate_los, block=12)
    bx_lo, by_lo = _block_sample(np.where(low_coh, nisar_rate_los, np.nan), op_rate_los, block=12)
    test_e_high = _stats(bx_hi, by_hi) if np.sum(np.isfinite(bx_hi) & np.isfinite(by_hi)) >= 10 else None
    test_e_low = _stats(bx_lo, by_lo) if np.sum(np.isfinite(bx_lo) & np.isfinite(by_lo)) >= 10 else None

    def _clean(st: dict | None) -> dict | None:
        if st is None:
            return None
        return {k: st[k] for k in ("r", "rmse", "slope", "n")}

    return {
        "id": name,
        "baseline": _clean(base),
        "test_a_overlap_days": ov_days,
        "test_b_vertical_cos_theta": _clean(test_b),
        "test_c_unaligned_ref": _clean(test_c_unaligned),
        "test_d_80m_raw": _clean(test_d_raw),
        "test_d_2km_block": _clean(test_d_2km),
        "test_e_high_coh_urban": _clean(test_e_high),
        "test_e_low_coh_agri": _clean(test_e_low),
        "opera_valid_frac": round(float(np.isfinite(opera_raw_cm).mean()), 3),
    }


def main() -> None:
    results = []

    # 1. Central Valley
    d_cv = np.load(ROOT / "analysis" / "out" / "central_valley_p114_cum.npz")
    nx, ny = d_cv["x"], d_cv["y"]
    ref_r, ref_c = int(d_cv["reference_rc"][0]), int(d_cv["reference_rc"][1])
    inc = d_cv["incidence"]
    inc_deg = float(np.nanmedian(inc[np.isfinite(inc)]))
    dates = [str(x) for x in d_cv["dates"]]
    nisar_days = _days_between(dates[0], dates[-1])
    cv_npzs = sorted((ROOT / "pipeline" / "subset" / "central_valley_p114").glob("*.npz"))
    cv_coh = _mean_coherence(cv_npzs) if cv_npzs else np.ones_like(d_cv["cum_cm"])
    op_cv = _sample_opera_to_grid(OPERA_DIR / "cv_summer2025.nc", nx, ny)
    results.append(
        _run_grid_5tests(
            "central_valley",
            d_cv["cum_cm"].astype(np.float64) * (100.0 / nisar_days),
            op_cv,
            _days_between("2025-07-19", "2025-10-17"),
            nx,
            ny,
            float(nx[ref_c]),
            float(ny[ref_r]),
            inc_deg,
            cv_coh,
            (dates[0], dates[-1]),
            ("2025-07-19", "2025-10-17"),
        )
    )

    # 2. Eloy
    eloy_files = sorted((ROOT / "pipeline" / "subset" / "eloy").glob("*.npz"))
    nisar_eloy = _load_nisar_chain(eloy_files, bbox_wgs84=(-111.8, 32.5, -111.3, 33.0))
    eloy_coh = _mean_coherence(eloy_files)
    op_eloy = _sample_opera_to_grid(OPERA_DIR / "eloy.nc", nisar_eloy["x"], nisar_eloy["y"])
    results.append(
        _run_grid_5tests(
            "eloy",
            nisar_eloy["cum_cm"] * (100.0 / _days_between("2026-06-19", "2026-10-17")),
            op_eloy,
            _days_between("2026-01-24", "2026-04-30"),
            nisar_eloy["x"],
            nisar_eloy["y"],
            nisar_eloy["ref_x"],
            nisar_eloy["ref_y"],
            nisar_eloy["inc_deg"],
            eloy_coh,
            ("2026-06-19", "2026-10-17"),
            ("2026-01-24", "2026-04-30"),
        )
    )

    # 3. Mexico City (point-based: baseline vs vertical cos_theta vs unaligned ref)
    pts = json.loads((DATA_GLOBAL / "mexico_city" / "points.json").read_text(encoding="utf-8"))
    mc_meta = json.loads((DATA_GLOBAL / "mexico_city" / "summary.json").read_text(encoding="utf-8"))
    ref_pt = mc_meta.get("reference_point", {})
    inc_mc = float(mc_meta.get("incidence_deg_at_max", 38.0))
    nisar_days_mc = _days_between("2026-06-22", "2026-10-20")
    opera_days_mc = _days_between("2025-12-25", "2026-03-25")
    mc_nc = OPERA_DIR / ("mexico_city_f01088.nc" if (OPERA_DIR / "mexico_city_f01088.nc").exists() else "mexico_city.nc")
    tr = Transformer.from_crs(4326, 32614, always_xy=True)
    with h5py.File(mc_nc, "r") as f:
        ox, oy = f["x"][:], f["y"][:]
        disp, mask = f["displacement"], f["recommended_mask"]
        ref_offset = 0.0
        if "lon" in ref_pt and "lat" in ref_pt:
            rx, ry = tr.transform(ref_pt["lon"], ref_pt["lat"])
            rj, ri = int(np.abs(ox - rx).argmin()), int(np.abs(oy - ry).argmin())
            wd_r = disp[max(0, ri - 10):ri + 11, max(0, rj - 10):rj + 11].astype(np.float64) * 100.0
            wm_r = mask[max(0, ri - 10):ri + 11, max(0, rj - 10):rj + 11] == 1
            if (np.isfinite(wd_r) & wm_r).sum() >= 5:
                ref_offset = float(np.median(wd_r[np.isfinite(wd_r) & wm_r]))

        n_rates, o_rates_aligned, o_rates_raw = [], [], []
        for pt in pts:
            px, py = tr.transform(pt["lon"], pt["lat"])
            j, i = int(np.abs(ox - px).argmin()), int(np.abs(oy - py).argmin())
            win_d = disp[max(0, i - 5):i + 6, max(0, j - 5):j + 6].astype(np.float64) * 100.0
            win_m = mask[max(0, i - 5):i + 6, max(0, j - 5):j + 6] == 1
            ok = np.isfinite(win_d) & win_m
            if ok.sum() < 5:
                ok = np.isfinite(win_d)
            if ok.sum() < 3:
                continue
            raw_cm = float(np.median(win_d[ok]))
            n_rates.append(float(pt["disp_cm"][-1]) * (100.0 / nisar_days_mc))
            o_rates_aligned.append((raw_cm - ref_offset) * (100.0 / opera_days_mc))
            o_rates_raw.append(raw_cm * (100.0 / opera_days_mc))

    nx_mc = np.asarray(n_rates)
    oy_al = np.asarray(o_rates_aligned)
    oy_raw = np.asarray(o_rates_raw)
    st_mc_base = _stats(nx_mc, oy_al)
    st_mc_vert = _stats(nx_mc / np.cos(np.deg2rad(inc_mc)), oy_al / np.cos(np.deg2rad(39.0)))
    st_mc_unaligned = _stats(nx_mc, oy_raw)
    results.append(
        {
            "id": "mexico_city",
            "baseline": {k: st_mc_base[k] for k in ("r", "rmse", "slope", "n")},
            "test_a_overlap_days": 0,
            "test_b_vertical_cos_theta": {k: st_mc_vert[k] for k in ("r", "rmse", "slope", "n")},
            "test_c_unaligned_ref": {k: st_mc_unaligned[k] for k in ("r", "rmse", "slope", "n")},
        }
    )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
