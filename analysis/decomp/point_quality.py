"""Per-point time-series regression and phase-unwrapping jump diagnostics (PC5, Q26).

Evaluates each representative point in ``data/<site>/points.json`` using an
ordinary least-squares linear trend model ``d(t) = a + v * t`` and inspects
consecutive epoch-to-epoch increments for sudden jumps relative to NISAR L-band
two-way phase ambiguity scales (with ``lambda ~= 0.242 m``):
    * One full 2*pi phase ambiguity cycle: ``lambda / 2 ~= 12.10 cm`` LOS.
    * Half an ambiguity cycle (pi rad): ``lambda / 4 ~= 6.05 cm`` LOS
      (``UNWRAP_SUSPECT``, matching ``analysis/insar.py`` ``cycle_outliers``).
    * Quarter cycle (pi/2 rad): ``lambda / 8 ~= 3.02 cm`` LOS
      (``ELEVATED_JUMP``, single-pair step worth manual atmospheric/unwrapping check).
"""

from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

DEFAULT_L_BAND_WAVELENGTH_M = 0.2419632429378531


def analyze_point_series(
    point: dict[str, Any],
    wavelength_m: float = DEFAULT_L_BAND_WAVELENGTH_M,
    watch_jump_cm: float = 2.0,
) -> dict[str, Any]:
    """Fit linear trend, residual std, and max epoch-to-epoch jump for one point.

    Flag rules relative to L-band ambiguity thresholds:
        - ``"UNWRAP_SUSPECT"`` if ``max_abs_jump_cm > lambda/4*100`` (~6.05 cm, pi rad)
        - ``"ELEVATED_JUMP"`` if ``max_abs_jump_cm > lambda/8*100`` (~3.02 cm, pi/2 rad)
        - ``"WATCH"`` if ``watch_jump_cm < max_abs_jump_cm <= lambda/8*100``
        - ``"OK"`` otherwise.
    """
    dates = list(point["dates"])
    disp = np.asarray([np.nan if v is None else float(v) for v in point["disp_cm"]], dtype=np.float64)
    if len(dates) != disp.size:
        raise ValueError(f"Point {point.get('id')} dates/disp length mismatch")

    t0 = date.fromisoformat(dates[0])
    t_days = np.array([(date.fromisoformat(s) - t0).days for s in dates], dtype=np.float64)
    t_yr = t_days / 365.25
    span_days = float(t_days[-1] - t_days[0])

    valid = np.isfinite(disp)
    n_valid = int(valid.sum())
    if n_valid < 3:
        return {
            "id": point.get("id"),
            "name": point.get("name"),
            "kind": point.get("kind"),
            "n_valid": n_valid,
            "rate_cm_per_yr": math.nan,
            "fit_total_cm": math.nan,
            "r2": math.nan,
            "residual_std_cm": math.nan,
            "max_jump_cm": math.nan,
            "max_abs_jump_cm": math.nan,
            "max_jump_pair": None,
            "unwrapping_flag": "INSUFFICIENT_DATA",
        }

    g_mat = np.column_stack([np.ones(n_valid, dtype=np.float64), t_yr[valid]])
    y = disp[valid]
    coef, *_ = np.linalg.lstsq(g_mat, y, rcond=None)
    yhat = g_mat @ coef
    resid = y - yhat
    resid_std = float(np.std(resid, ddof=2))
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0.0 else 1.0

    # Pairwise jumps along consecutive valid timestamps
    valid_idx = np.flatnonzero(valid)
    diffs = np.diff(disp[valid_idx])
    abs_diffs = np.abs(diffs)
    imax = int(np.argmax(abs_diffs))
    max_jump = float(diffs[imax])
    max_abs = float(abs_diffs[imax])
    i0, i1 = int(valid_idx[imax]), int(valid_idx[imax + 1])
    jump_pair = f"{dates[i0]}->{dates[i1]}"

    half_cycle_cm = (float(wavelength_m) / 4.0) * 100.0     # pi rad (~6.05 cm)
    quarter_cycle_cm = (float(wavelength_m) / 8.0) * 100.0  # pi/2 rad (~3.02 cm)
    if max_abs > half_cycle_cm:
        flag = "UNWRAP_SUSPECT"
    elif max_abs > quarter_cycle_cm:
        flag = "ELEVATED_JUMP"
    elif max_abs > watch_jump_cm:
        flag = "WATCH"
    else:
        flag = "OK"

    rate_cm_yr = float(coef[1])
    return {
        "id": point.get("id"),
        "name": point.get("name"),
        "kind": point.get("kind"),
        "lon": point.get("lon"),
        "lat": point.get("lat"),
        "n_valid": n_valid,
        "span_days": span_days,
        "end_disp_cm": float(disp[valid_idx[-1]]),
        "rate_cm_per_yr": rate_cm_yr,
        "fit_total_cm": rate_cm_yr * (span_days / 365.25),
        "r2": r2,
        "residual_std_cm": resid_std,
        "max_jump_cm": max_jump,
        "max_abs_jump_cm": max_abs,
        "max_jump_pair": jump_pair,
        "half_cycle_cm": half_cycle_cm,
        "quarter_cycle_cm": quarter_cycle_cm,
        "unwrapping_flag": flag,
    }


def analyze_points_file(
    points_path: str | Path,
    wavelength_m: float = DEFAULT_L_BAND_WAVELENGTH_M,
) -> dict[str, Any]:
    """Evaluate all point time series in ``points.json`` and return summary diagnostics."""
    path = Path(points_path)
    pts = json.loads(path.read_text(encoding="utf-8"))
    results = [analyze_point_series(p, wavelength_m=wavelength_m) for p in pts]
    suspects = [r["id"] for r in results if r["unwrapping_flag"] == "UNWRAP_SUSPECT"]
    elevated = [r["id"] for r in results if r["unwrapping_flag"] == "ELEVATED_JUMP"]
    watches = [r["id"] for r in results if r["unwrapping_flag"] == "WATCH"]
    return {
        "file": str(path),
        "n_points": len(results),
        "half_cycle_threshold_cm": (float(wavelength_m) / 4.0) * 100.0,
        "quarter_cycle_threshold_cm": (float(wavelength_m) / 8.0) * 100.0,
        "suspect_ids": suspects,
        "elevated_ids": elevated,
        "watch_ids": watches,
        "points": results,
    }


if __name__ == "__main__":
    print(json.dumps(analyze_points_file("data/central_valley/points.json"), indent=2))