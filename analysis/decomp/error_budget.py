"""Empirical uncertainty budget, chain noise propagation, and GNSS validation stats (PC5).

Computes per-pair InSAR noise (``sigma_pair``), N-pair cumulative chain noise
(``sigma_total = sqrt(sum(sigma_pair_i^2)) ~= sigma_pair * sqrt(N)``), NISAR
GUNW split-spectrum ionosphere phase screen bounds (p1-p99 in LOS cm), and
GNSS-vs-InSAR summary statistics across ``provisional`` Central Valley datasets.

Assumptions & Scientific Conventions:
    1. Only ``quality == "provisional"`` pairs are included; ``beta-precal``
       scenes are strictly excluded (never mixed in one calculation).
    2. Phase-to-LOS displacement follows ISCE3/MintPy/NISAR ATBD sign:
       ``disp_los_cm = -(phase_rad * wavelength_m * 100.0) / (4.0 * pi)``,
       where negative means motion away from the satellite (subsidence).
    3. ``propagate_chain_std`` uses standard quadrature error propagation
       assuming pairwise-independent errors (decorrelation, unwrapping, soil
       moisture closure, residual atmosphere). Strictly speaking, in a daisy
       chain of consecutive unwrapped pairs (0-1, 1-2, ..., (N-1)-N), shared
       interior-epoch atmospheric delays partially cancel at intermediate dates,
       so sqrt(N) represents a conservative upper-bound model for independent
       per-pair error accumulation alongside epoch-1/epoch-N end-member screens.
"""

from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


def phase_to_los_cm(phase_rad: np.ndarray, wavelength_m: float) -> np.ndarray:
    """Convert unwrapped or ionospheric phase [rad] to LOS displacement [cm].

    Negative values correspond to motion away from the radar (subsidence).
    """
    if not np.isfinite(wavelength_m) or wavelength_m <= 0:
        raise ValueError(f"wavelength_m must be finite and positive, got {wavelength_m}")
    arr = np.asarray(phase_rad, dtype=np.float64)
    return (-float(wavelength_m) / (4.0 * math.pi) * arr) * 100.0


def _coh_to_float(coh: np.ndarray) -> np.ndarray:
    arr = np.asarray(coh)
    if np.issubdtype(arr.dtype, np.integer):
        return arr.astype(np.float64) / 255.0
    return arr.astype(np.float64)


def _reference_subtract(
    arr: np.ndarray,
    ref_rc: tuple[int, int],
    radius: int = 3,
) -> tuple[np.ndarray, float]:
    r, c = int(ref_rc[0]), int(ref_rc[1])
    h, w = arr.shape
    if not (0 <= r < h and 0 <= c < w):
        raise ValueError(f"ref_rc={ref_rc} out of bounds for shape {(h, w)}")
    win = arr[max(r - radius, 0) : r + radius + 1, max(c - radius, 0) : c + radius + 1]
    finite_win = win[np.isfinite(win)]
    if finite_win.size == 0:
        raise ValueError(f"reference window around {ref_rc} contains no finite pixels")
    ref_val = float(np.median(finite_win))
    return arr - ref_val, ref_val


def ionosphere_stats_cm(
    ion_rad: np.ndarray,
    wavelength_m: float,
    valid_mask: np.ndarray | None = None,
    ref_rc: tuple[int, int] | None = None,
    ref_radius: int = 3,
) -> dict[str, Any]:
    """Compute p1, p50, p99, and p1-p99 spread [LOS cm] of a GUNW ionosphere screen.

    Both absolute (unreferenced) scene statistics and optional reference-window-
    subtracted statistics (representing differential ionosphere across the subset
    relative to ``ref_rc``) are returned.
    """
    ion_cm = phase_to_los_cm(np.asarray(ion_rad, dtype=np.float64), float(wavelength_m))
    finite = np.isfinite(ion_cm)
    if valid_mask is not None:
        finite = finite & np.asarray(valid_mask, dtype=bool)
    vals = ion_cm[finite]
    if vals.size == 0:
        raise ValueError("No valid finite ionosphere pixels available")

    p1, p50, p99 = [float(v) for v in np.percentile(vals, [1.0, 50.0, 99.0])]
    out: dict[str, Any] = {
        "n_valid": int(vals.size),
        "p1_cm": p1,
        "p50_cm": p50,
        "p99_cm": p99,
        "p1_p99_range_cm": float(p99 - p1),
        "std_cm": float(np.std(vals)),
    }
    if ref_rc is not None:
        masked = np.where(finite, ion_cm, np.nan)
        ion_ref, ref_offset = _reference_subtract(masked, ref_rc, radius=ref_radius)
        ref_vals = ion_ref[finite]
        rp1, rp50, rp99 = [float(v) for v in np.percentile(ref_vals, [1.0, 50.0, 99.0])]
        out.update(
            {
                "ref_offset_cm": ref_offset,
                "ref_p1_cm": rp1,
                "ref_p50_cm": rp50,
                "ref_p99_cm": rp99,
                "ref_p1_p99_range_cm": float(rp99 - rp1),
            }
        )
    return out


def propagate_chain_std(
    sigma_pairs: float | Sequence[float] | np.ndarray,
    n_pairs: int | None = None,
    incidence_deg: float = 39.1,
) -> dict[str, Any]:
    """Propagate per-pair uncertainty across an N-pair cumulative interferogram chain.

    Formula:
        ``sigma_total = sqrt(sum_{i=1..N} sigma_pair_i^2) = sigma_rms * sqrt(N)``

    Assumes pairwise-independent random errors across the ``N`` chained pairs.
    Converts LOS uncertainty to vertical uncertainty estimate via ``/ cos(incidence_deg)``.
    """
    cos_inc = math.cos(math.radians(float(incidence_deg)))
    if cos_inc <= 0:
        raise ValueError(f"Invalid incidence angle: {incidence_deg}")

    if np.ndim(sigma_pairs) == 0:
        sig = float(sigma_pairs)
        if n_pairs is None or n_pairs <= 0:
            raise ValueError("n_pairs must be a positive integer when sigma_pairs is scalar")
        if sig < 0 or not math.isfinite(sig):
            raise ValueError(f"sigma_pairs must be finite and non-negative, got {sig}")
        n = int(n_pairs)
        rms = sig
        total_los = sig * math.sqrt(n)
    else:
        arr = np.asarray(sigma_pairs, dtype=np.float64)
        if arr.ndim != 1 or arr.size == 0:
            raise ValueError("sigma_pairs sequence must be non-empty 1-D")
        if not np.all(np.isfinite(arr)) or np.any(arr < 0):
            raise ValueError("All per-pair sigmas must be finite and non-negative")
        n = int(arr.size if n_pairs is None else n_pairs)
        if n <= 0:
            raise ValueError("n_pairs must be positive")
        rms = float(np.sqrt(np.mean(arr ** 2)))
        total_los = float(np.sqrt(np.sum(arr ** 2))) if n == arr.size else rms * math.sqrt(n)

    return {
        "n_pairs": n,
        "sigma_pair_rms_los_cm": float(rms),
        "sigma_total_los_cm": float(total_los),
        "sigma_total_vertical_cm_estimate": float(total_los / cos_inc),
        "incidence_deg": float(incidence_deg),
        "assumption": "independent pair noise: sigma_total = sigma_pair * sqrt(N)",
    }


def _scalar_str(val: np.ndarray) -> str:
    if isinstance(val, np.ndarray):
        return str(val.item() if val.ndim == 0 else val.ravel()[0])
    return str(val)


def pair_noise_from_npz(
    npz_path: str | Path,
    ref_rc: tuple[int, int],
    stable_scene_mask: np.ndarray | None = None,
    local_stable_mask: np.ndarray | None = None,
    coh_thr: float = 0.3,
    hi_coh_thr: float = 0.85,
    ref_radius: int = 3,
) -> dict[str, Any] | None:
    """Extract empirical per-pair noise and ionosphere bounds from one GUNW ``.npz``.

    Returns ``None`` if the file's ``quality`` is not ``"provisional"`` so that
    ``beta-precal`` scenes are never mixed into provisional estimates.
    """
    path = Path(npz_path)
    with np.load(path, allow_pickle=False) as d:
        quality = _scalar_str(d["quality"])
        if quality != "provisional":
            return None

        wavelength = float(d["wavelength"].item() if d["wavelength"].ndim == 0 else d["wavelength"])
        unw = d["unw"].astype(np.float64)
        coh = _coh_to_float(d["coh"])
        conn = d["conncomp"] if "conncomp" in d and d["conncomp"].size else None
        date1 = _scalar_str(d["date1"]) if "date1" in d else path.stem.split("_")[0]
        date2 = _scalar_str(d["date2"]) if "date2" in d else path.stem.split("_")[1]

        valid = np.isfinite(unw) & np.isfinite(coh) & (coh >= coh_thr)
        if conn is not None:
            valid = valid & (conn != 0)

        disp_raw_cm = phase_to_los_cm(unw, wavelength)
        disp_raw_ref, _ = _reference_subtract(np.where(valid, disp_raw_cm, np.nan), ref_rc, radius=ref_radius)

        hi_mask = valid & (coh >= hi_coh_thr)
        if stable_scene_mask is not None:
            scene_eval_mask = hi_mask & stable_scene_mask
        else:
            scene_eval_mask = hi_mask

        result: dict[str, Any] = {
            "pair": [date1, date2],
            "file": str(path.name),
            "quality": quality,
            "wavelength_m": wavelength,
            "sigma_raw_stable_scene_cm": float(np.nanstd(disp_raw_ref[scene_eval_mask])),
            "n_stable_scene": int(scene_eval_mask.sum()),
        }

        if local_stable_mask is not None:
            local_eval = hi_mask & local_stable_mask
            result["sigma_raw_local_cm"] = float(np.nanstd(disp_raw_ref[local_eval]))
            result["n_local"] = int(local_eval.sum())

        if "ion" in d and d["ion"].shape == unw.shape:
            ion = d["ion"].astype(np.float64)
            valid_ion = valid & np.isfinite(ion)
            result["ionosphere"] = ionosphere_stats_cm(
                ion, wavelength, valid_mask=valid_ion, ref_rc=ref_rc, ref_radius=ref_radius
            )
            disp_deion_cm = phase_to_los_cm(unw - ion, wavelength)
            disp_deion_ref, _ = _reference_subtract(
                np.where(valid_ion, disp_deion_cm, np.nan), ref_rc, radius=ref_radius
            )
            scene_deion = scene_eval_mask & np.isfinite(ion)
            result["sigma_deion_stable_scene_cm"] = float(np.nanstd(disp_deion_ref[scene_deion]))
            if local_stable_mask is not None:
                local_deion = hi_mask & local_stable_mask & np.isfinite(ion)
                result["sigma_deion_local_cm"] = float(np.nanstd(disp_deion_ref[local_deion]))

    return result


def summarize_gnss_validation(validation_path: str | Path) -> dict[str, Any]:
    """Compute per-station and aggregate statistical metrics for ``validation.json`` (Q27).

    Returns RMSE, Pearson r, endpoint difference, and OLS linear velocity trends
    (``cm/yr`` and equivalent over the 108-day campaign) for both InSAR and GNSS.
    """
    records = json.loads(Path(validation_path).read_text(encoding="utf-8"))
    if not records:
        raise ValueError(f"Empty validation file: {validation_path}")

    per_station: list[dict[str, Any]] = []
    for rec in records:
        dates = rec["dates"]
        t0 = date.fromisoformat(dates[0])
        t_days = np.array([(date.fromisoformat(s) - t0).days for s in dates], dtype=np.float64)
        span_days = float(t_days[-1] - t_days[0])
        t_yr = t_days / 365.25
        g_mat = np.column_stack([np.ones_like(t_yr), t_yr])

        insar = np.asarray(rec["insar"], dtype=np.float64)
        gnss = np.asarray(rec["gnss"], dtype=np.float64)
        ok = np.isfinite(insar) & np.isfinite(gnss)
        c_insar, *_ = np.linalg.lstsq(g_mat[ok], insar[ok], rcond=None)
        c_gnss, *_ = np.linalg.lstsq(g_mat[ok], gnss[ok], rcond=None)

        rate_insar = float(c_insar[1])
        rate_gnss = float(c_gnss[1])
        trend_diff_yr = rate_insar - rate_gnss
        per_station.append(
            {
                "station": rec["station"],
                "lon": float(rec["lon"]),
                "lat": float(rec["lat"]),
                "incidence_deg": float(rec["incidence_deg"]),
                "rmse_cm": float(rec["rmse_cm"]),
                "corr": float(rec["corr"]),
                "insar_end_cm": float(insar[-1]),
                "gnss_end_cm": float(gnss[-1]),
                "rate_insar_cm_per_yr": rate_insar,
                "rate_gnss_cm_per_yr": rate_gnss,
                "trend_diff_cm_per_yr": trend_diff_yr,
                "trend_diff_span_cm": trend_diff_yr * span_days / 365.25,
                "span_days": span_days,
            }
        )

    rmses = np.array([s["rmse_cm"] for s in per_station], dtype=np.float64)
    corrs = np.array([s["corr"] for s in per_station], dtype=np.float64)
    abs_rate_diffs = np.array([abs(s["trend_diff_cm_per_yr"]) for s in per_station], dtype=np.float64)

    active_basin = [s for s in per_station if s["corr"] >= 0.6]
    active_rmses = np.array([s["rmse_cm"] for s in active_basin], dtype=np.float64)
    active_corrs = np.array([s["corr"] for s in active_basin], dtype=np.float64)
    active_diffs = np.array([s["trend_diff_cm_per_yr"] for s in active_basin], dtype=np.float64)

    return {
        "n_stations": len(per_station),
        "all_stations": {
            "mean_rmse_cm": float(np.mean(rmses)),
            "median_rmse_cm": float(np.median(rmses)),
            "min_rmse_cm": float(np.min(rmses)),
            "max_rmse_cm": float(np.max(rmses)),
            "median_corr": float(np.median(corrs)),
            "mean_abs_trend_diff_cm_per_yr": float(np.mean(abs_rate_diffs)),
        },
        "subsiding_basin_subset": {
            "stations": [s["station"] for s in active_basin],
            "criterion": "Pearson r >= 0.60 (active subsidence stations inside basin)",
            "n_stations": len(active_basin),
            "mean_rmse_cm": float(np.mean(active_rmses)) if active_basin else math.nan,
            "max_rmse_cm": float(np.max(active_rmses)) if active_basin else math.nan,
            "mean_corr": float(np.mean(active_corrs)) if active_basin else math.nan,
            "mean_trend_diff_cm_per_yr": float(np.mean(active_diffs)) if active_basin else math.nan,
            "mean_abs_trend_diff_cm_per_yr": float(np.mean(np.abs(active_diffs))) if active_basin else math.nan,
        },
        "per_station": per_station,
    }


def _control_point_stats(points_path: Path, dates: Sequence[str]) -> list[dict[str, Any]]:
    if not points_path.exists():
        return []
    pts = json.loads(points_path.read_text(encoding="utf-8"))
    out: list[dict[str, Any]] = []
    for p in pts:
        if p.get("kind") != "near_reference":
            continue
        vals = np.asarray(p["disp_cm"], dtype=np.float64)
        increments = np.diff(vals)
        out.append(
            {
                "id": p["id"],
                "name": p["name"],
                "pair_increments_cm": [float(v) for v in increments],
                "sigma_pair_rms_cm": float(np.sqrt(np.mean(increments ** 2))),
                "sigma_pair_std_cm": float(np.std(increments, ddof=1)) if len(increments) > 1 else 0.0,
                "cum_end_cm": float(vals[-1]),
                "dates": dates,
            }
        )
    return out


def compute_error_budget(
    subset_dir: str | Path = "pipeline/subset/central_valley",
    cum_path: str | Path = "analysis/out/central_valley_cum.npz",
    cum_stack_path: str | Path = "analysis/out/central_valley_cum_stack.npz",
    points_path: str | Path = "data/central_valley/points.json",
    validation_path: str | Path = "data/central_valley/validation.json",
    summary_path: str | Path = "data/central_valley/summary.json",
    local_radius_km: float = 10.0,
    stable_cum_thr_cm: float = 0.5,
    hi_coh_thr: float = 0.85,
) -> dict[str, Any]:
    """Compute the full provisional Central Valley uncertainty budget and GNSS synthesis."""
    subset_dir = Path(subset_dir)
    cum = np.load(cum_path, allow_pickle=False)
    cum_cm = cum["cum_cm"].astype(np.float64)
    ref_rc = (int(cum["reference_rc"][0]), int(cum["reference_rc"][1]))
    pixel_spacing_km = 0.080  # 80 m NISAR GUNW posting

    summary = json.loads(Path(summary_path).read_text(encoding="utf-8")) if Path(summary_path).exists() else {}
    inc_deg = float(summary.get("incidence_deg_at_max", 39.1))

    rr, cc = np.ogrid[: cum_cm.shape[0], : cum_cm.shape[1]]
    dist_km = np.hypot(rr - ref_rc[0], cc - ref_rc[1]) * pixel_spacing_km
    stable_scene_mask = np.isfinite(cum_cm) & (np.abs(cum_cm) < stable_cum_thr_cm)
    local_stable_mask = stable_scene_mask & (dist_km <= local_radius_km)

    npz_files = sorted(subset_dir.glob("*.npz"))
    pair_records: list[dict[str, Any]] = []
    skipped_files: list[dict[str, str]] = []
    coh_sum = np.zeros_like(cum_cm, dtype=np.float64)
    coh_count = 0

    for f in npz_files:
        rec = pair_noise_from_npz(
            f,
            ref_rc=ref_rc,
            stable_scene_mask=stable_scene_mask,
            local_stable_mask=local_stable_mask,
            hi_coh_thr=hi_coh_thr,
        )
        if rec is None:
            with np.load(f, allow_pickle=False) as d:
                skipped_files.append({"file": f.name, "quality": _scalar_str(d["quality"])})
            continue
        pair_records.append(rec)
        with np.load(f, allow_pickle=False) as d:
            coh_sum += _coh_to_float(d["coh"])
            coh_count += 1

    if not pair_records:
        raise ValueError(f"No provisional .npz pairs found in {subset_dir}")

    coh_mean = coh_sum / max(coh_count, 1)

    # Post-deramp cumulative stack pair increments (matches the published cumulative product)
    stack_npz = np.load(cum_stack_path, allow_pickle=False)
    stack = stack_npz["cum_stack_cm"].astype(np.float64)
    stack_dates = [str(d) for d in stack_npz["dates"]]
    diffs = np.diff(stack, axis=0)
    post_local_mask = np.isfinite(stack[-1]) & (coh_mean >= hi_coh_thr) & local_stable_mask
    post_scene_mask = np.isfinite(stack[-1]) & (coh_mean >= hi_coh_thr) & stable_scene_mask

    for idx, rec in enumerate(pair_records):
        if idx < diffs.shape[0]:
            rec["sigma_post_deramp_local_cm"] = float(np.nanstd(diffs[idx][post_local_mask]))
            rec["sigma_post_deramp_stable_scene_cm"] = float(np.nanstd(diffs[idx][post_scene_mask]))

    n_pairs = len(pair_records)
    raw_local_sigs = [r["sigma_raw_local_cm"] for r in pair_records]
    post_local_sigs = [r["sigma_post_deramp_local_cm"] for r in pair_records]
    post_scene_sigs = [r["sigma_post_deramp_stable_scene_cm"] for r in pair_records]
    iono_ranges = [r["ionosphere"]["p1_p99_range_cm"] for r in pair_records if "ionosphere" in r]

    max_sub_cm = float(summary.get("max_subsidence_cm", -7.8))
    max_sub_vert_cm = float(summary.get("max_subsidence_vertical_cm_estimate", -10.1))

    chain_raw_local = propagate_chain_std(raw_local_sigs, incidence_deg=inc_deg)
    chain_post_local = propagate_chain_std(post_local_sigs, incidence_deg=inc_deg)
    chain_post_scene = propagate_chain_std(post_scene_sigs, incidence_deg=inc_deg)

    ref_range = summary.get("max_subsidence_range_cm")
    ref_spread_cm = (
        abs(float(ref_range[1]) - float(ref_range[0])) if isinstance(ref_range, list) and len(ref_range) == 2 else None
    )

    gnss_summary = summarize_gnss_validation(validation_path) if Path(validation_path).exists() else None
    ctrl_points = _control_point_stats(Path(points_path), stack_dates)

    return {
        "quality": "provisional",
        "reference_rc": list(ref_rc),
        "n_pairs": n_pairs,
        "skipped_files": skipped_files,
        "pairs": pair_records,
        "chain_noise": {
            "raw_local_high_coh": chain_raw_local,
            "post_deramp_local_high_coh": chain_post_local,
            "post_deramp_stable_scene_high_coh": chain_post_scene,
        },
        "ionosphere_summary_cm": {
            "min_p1_p99_range_cm": float(min(iono_ranges)),
            "median_p1_p99_range_cm": float(np.median(iono_ranges)),
            "max_p1_p99_range_cm": float(max(iono_ranges)),
            "mean_p1_p99_range_cm": float(np.mean(iono_ranges)),
        },
        "near_reference_control_points": ctrl_points,
        "signal_to_noise": {
            "max_subsidence_los_cm": max_sub_cm,
            "max_subsidence_vertical_cm_estimate": max_sub_vert_cm,
            "snr_vs_post_local_chain": abs(max_sub_cm) / chain_post_local["sigma_total_los_cm"],
            "snr_vs_post_scene_chain": abs(max_sub_cm) / chain_post_scene["sigma_total_los_cm"],
            "reference_sensitivity_spread_los_cm": ref_spread_cm,
        },
        "gnss_validation_summary": gnss_summary,
    }


if __name__ == "__main__":
    print(json.dumps(compute_error_budget(), indent=2))
