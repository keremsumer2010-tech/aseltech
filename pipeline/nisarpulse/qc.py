"""Self-checking QC for NISAR Pulse cumulative displacement stacks."""

from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np

L_BAND_CYCLE_CM = 12.1


def _neighbor_median(stack: list[np.ndarray], idx: int) -> np.ndarray:
    """Pixel-wise median of other pair steps (requires >= 3 pairs to avoid blaming a clean neighbor)."""
    if len(stack) < 3:
        return np.full_like(stack[idx], np.nan, dtype=np.float32)
    neighbors = [stack[j] for j in range(len(stack)) if j != idx]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return np.nanmedian(np.stack(neighbors, axis=0), axis=0).astype(np.float32)


def qc_stack(
    pair_cm: list[np.ndarray],
    dates: list[str],
    conncomp_list: list[np.ndarray | None] | None = None,
    cycle_cm: float = L_BAND_CYCLE_CM,
    tol_cm: float = 2.0,
    min_comp_agree: float = 0.5,
    spike_thr_cm: float = 5.0,
    drop_frac: float = 0.30,
) -> tuple[list[np.ndarray], list[str], dict]:
    """Run pixel-level QC before cumulative summation.

    1. Compare each pair step against adjacent steps' median; if difference is
       within ``tol_cm`` of ``k * cycle_cm`` (k != 0) and > ``min_comp_agree`` of
       valid pixels in the same connected component agree on ``k``, subtract
       ``k * cycle_cm`` from that component in that pair.
    2. Detect interior dates where consecutive steps have opposite signs and both
       exceed ``spike_thr_cm`` on > ``drop_frac`` of jointly valid pixels; drop
       those dates by merging the two adjacent steps (cancelling the single-date error).
    """
    if len(dates) != len(pair_cm) + 1:
        raise ValueError(f"Expected {len(pair_cm) + 1} dates, got {len(dates)}")

    work = [np.array(arr, dtype=np.float32, copy=True) for arr in pair_cm]
    out_dates = list(dates)
    cc_list = list(conncomp_list) if conncomp_list is not None else [None] * len(work)

    corrected_pairs: list[dict] = []
    dropped_dates: list[dict] = []
    affected_mask = np.zeros(work[0].shape, dtype=bool) if work else np.zeros((0, 0), dtype=bool)

    i = 1
    while i < len(work):
        a = work[i - 1]
        b = work[i]
        both = np.isfinite(a) & np.isfinite(b)
        n_both = int(both.sum())
        if n_both > 0:
            opp = both & (np.abs(a) > spike_thr_cm) & (np.abs(b) > spike_thr_cm) & ((a * b) < 0)
            frac = float(opp.sum()) / n_both
            if frac > drop_frac:
                dropped_dates.append(
                    {
                        "date": out_dates[i],
                        "outlier_frac": round(frac, 3),
                        "merged_pair": [out_dates[i - 1], out_dates[i + 1]],
                    }
                )
                affected_mask |= opp
                merged = a + b
                work[i - 1 : i + 1] = [merged.astype(np.float32)]
                if i - 1 < len(cc_list) and i < len(cc_list):
                    cc_a, cc_b = cc_list[i - 1], cc_list[i]
                    cc_merged = cc_a if cc_a is not None else cc_b
                    cc_list[i - 1 : i + 1] = [cc_merged]
                out_dates.pop(i)
                continue
        i += 1

    if len(work) >= 3:
        for t in range(len(work)):
            med = _neighbor_median(work, t)
            valid = np.isfinite(work[t]) & np.isfinite(med)
            if not np.any(valid):
                continue

            diff = work[t] - med
            k_arr = np.round(diff / cycle_cm)
            is_jump = valid & (k_arr != 0) & (np.abs(k_arr) <= 5) & (np.abs(diff - k_arr * cycle_cm) <= tol_cm)

            cc = cc_list[t] if t < len(cc_list) and cc_list[t] is not None else np.ones_like(work[t], dtype=np.int32)
            labels = np.unique(cc[valid & (cc > 0)])
            for lbl in labels:
                comp_valid = valid & (cc == lbl)
                n_comp = int(comp_valid.sum())
                if n_comp == 0:
                    continue
                comp_jumps = k_arr[comp_valid & is_jump].astype(int)
                if comp_jumps.size == 0:
                    continue
                vals, counts = np.unique(comp_jumps, return_counts=True)
                best_idx = int(np.argmax(counts))
                k_mode = int(vals[best_idx])
                agree_frac = float(counts[best_idx]) / n_comp
                if agree_frac > min_comp_agree:
                    shift = np.float32(-k_mode * cycle_cm)
                    target = np.isfinite(work[t]) & (cc == lbl)
                    work[t][target] = work[t][target] + shift
                    affected_mask |= target
                    corrected_pairs.append(
                        {
                            "pair": [out_dates[t], out_dates[t + 1]],
                            "component": int(lbl),
                            "k": k_mode,
                            "shift_cm": round(float(shift), 2),
                            "affected_px": int(target.sum()),
                            "agree_frac": round(agree_frac, 3),
                        }
                    )

    if work:
        scene_valid = np.logical_or.reduce([np.isfinite(arr) for arr in work])
        n_scene = int(scene_valid.sum())
        affected_pct = round(100.0 * float((affected_mask & scene_valid).sum()) / n_scene, 2) if n_scene > 0 else 0.0
    else:
        affected_pct = 0.0

    report = {
        "qc_enabled": True,
        "corrected_pairs": corrected_pairs,
        "dropped_dates": dropped_dates,
        "affected_pixel_pct": affected_pct,
    }
    return work, out_dates, report


def write_qc_report(out_dir: Path, report: dict, quality: str = "provisional") -> Path:
    """Persist qc_report.json with explicit quality field."""
    payload = {"quality": quality, **report}
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "qc_report.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path
