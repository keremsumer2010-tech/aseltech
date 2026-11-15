"""Offline robustness sweep for the provisional global subsidence atlas.

Uses only local provisional GUNW subsets. Candidate reference windows are selected
from separated corners of the smallest test box using high coherence and low
relative motion; they are explicitly *not* claimed to be geologically verified.
Run from the repository root: ``python pipeline/pc7/atlas_robustness.py``.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
import math
from pathlib import Path
import sys
import argparse
from typing import Any
import warnings

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer
from numpy.lib.stride_tricks import sliding_window_view

from analysis.insar import cycle_outliers, mask_components, mask_coherence, phase_to_cm

HALF_WIDTHS = (0.20, 0.25, 0.30)
COHERENCE_THRESHOLDS = (0.3, 0.4, 0.5)
REF_RADIUS = 3
BLOCK_PX = 13
MIN_BLOCK_VALID = 0.5
MAX_BLOCK_STD_CM = 2.0
PROVISIONAL_START = "2026-06-17"


def kendall_tau_b(reference: list[float], variant: list[float]) -> float | None:
    """Kendall tau-b for short rank vectors, avoiding an optional SciPy import."""
    concordant = discordant = ties_ref = ties_var = 0
    for i in range(len(reference)):
        for j in range(i + 1, len(reference)):
            dx = np.sign(reference[i] - reference[j])
            dy = np.sign(variant[i] - variant[j])
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                ties_ref += 1
            elif dy == 0:
                ties_var += 1
            elif dx == dy:
                concordant += 1
            else:
                discordant += 1
    denom = math.sqrt((concordant + discordant + ties_ref) * (concordant + discordant + ties_var))
    return None if denom == 0 else (concordant - discordant) / denom


@dataclass
class Scene:
    city_id: str
    folder: Path
    pair_paths: list[Path]
    bbox: tuple[float, float, float, float]
    center: tuple[float, float]
    atlas_rate: float | None
    atlas_rank: int | None


def fast_deramp(values: np.ndarray, step: int = 8) -> np.ndarray:
    """Remove a least-squares plane using a sparse fit and broadcast evaluation."""
    a = np.asarray(values, dtype=np.float32)
    h, w = a.shape
    rows = np.arange(0, h, step)
    cols = np.arange(0, w, step)
    sample = a[np.ix_(rows, cols)]
    rr, cc = np.meshgrid(rows / max(h - 1, 1), cols / max(w - 1, 1), indexing="ij")
    ok = np.isfinite(sample)
    if int(ok.sum()) < 100:
        return a.copy()
    design = np.column_stack((np.ones(int(ok.sum())), cc[ok], rr[ok]))
    coef, *_ = np.linalg.lstsq(design, sample[ok].astype(np.float64), rcond=None)
    x = np.arange(w, dtype=np.float64) / max(w - 1, 1)
    y = np.arange(h, dtype=np.float64) / max(h - 1, 1)
    plane = coef[0] + coef[1] * x[None, :] + coef[2] * y[:, None]
    return (a - plane.astype(np.float32)).astype(np.float32)


def block_headline(values: np.ndarray, inside: np.ndarray) -> tuple[float | None, float | None]:
    """Return minimum eligible 13x13 block median and pixel p2 within a box."""
    a = np.where(inside, values, np.nan).astype(np.float32, copy=False)
    pix = a[np.isfinite(a)]
    if pix.size < BLOCK_PX * BLOCK_PX:
        return None, None
    p2 = float(np.percentile(pix, 2))
    h, w = a.shape
    hp = ((h + BLOCK_PX - 1) // BLOCK_PX) * BLOCK_PX
    wp = ((w + BLOCK_PX - 1) // BLOCK_PX) * BLOCK_PX
    pad = np.full((hp, wp), np.nan, np.float32)
    pad[:h, :w] = a
    tiles = pad.reshape(hp // BLOCK_PX, BLOCK_PX, wp // BLOCK_PX, BLOCK_PX).transpose(0, 2, 1, 3)
    flat = tiles.reshape(tiles.shape[0], tiles.shape[1], -1)
    count = np.isfinite(flat).sum(axis=2)
    fraction = count / float(BLOCK_PX * BLOCK_PX)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        med = np.nanmedian(flat, axis=2)
        std = np.nanstd(flat, axis=2)
    eligible = (fraction >= MIN_BLOCK_VALID) & (std <= MAX_BLOCK_STD_CM) & np.isfinite(med)
    headline = float(np.min(med[eligible])) if np.any(eligible) else None
    return headline, p2


def parse_subset_overrides(items: list[str]) -> dict[str, Path]:
    """Parse repeatable CITY=PATH overrides for freshly cut, non-shared inputs."""
    result: dict[str, Path] = {}
    for item in items:
        city, separator, path = item.partition("=")
        if not separator or not city.strip() or not path.strip():
            raise ValueError(f"invalid subset override {item!r}; expected CITY=PATH")
        result[city.strip()] = Path(path.strip())
    return result


def load_scene_inputs(subset_overrides: dict[str, Path] | None = None) -> tuple[list[Scene], dict[str, Any]]:
    subset_overrides = subset_overrides or {}
    atlas_path = ROOT / "data/global/atlas.json"
    atlas = json.loads(atlas_path.read_text(encoding="utf-8"))
    atlas_by_id = {r["id"]: r for r in atlas.get("regions", []) if isinstance(r, dict) and r.get("id")}
    ids = set(atlas_by_id)
    ids.update(p.parent.name for p in (ROOT / "data/global").glob("*/summary.json"))
    ids.update({"central_valley", "karapinar", "konya_plain", "delta"})
    scenes: list[Scene] = []
    for city_id in sorted(ids):
        global_dir = ROOT / "data/global" / city_id
        data_dir = global_dir if (global_dir / "summary.json").is_file() else ROOT / "data" / city_id
        meta_path, summary_path = data_dir / "meta.json", data_dir / "summary.json"
        subset_dir = subset_overrides.get(
            city_id,
            ROOT / "pipeline/subset" / (f"global_{city_id}" if city_id not in {"central_valley", "karapinar", "konya_plain", "delta"} else city_id),
        )
        if not meta_path.is_file() or not summary_path.is_file() or not subset_dir.is_dir():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        bbox_raw = meta.get("bbox")
        if not isinstance(bbox_raw, list) or len(bbox_raw) != 4:
            continue
        bbox = tuple(float(v) for v in bbox_raw)
        center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
        pairs = []
        for p in sorted(subset_dir.glob("*.npz")):
            try:
                with np.load(p, allow_pickle=False) as z:
                    quality = str(z["quality"].item())
                    d1 = str(z["date1"].item())
                    d2 = str(z["date2"].item())
                if quality == "provisional" and d1 >= PROVISIONAL_START and d2 >= PROVISIONAL_START:
                    pairs.append((d1, d2, p))
            except (OSError, KeyError, ValueError):
                continue
        pairs.sort(key=lambda v: (v[0], v[1]))
        chain: list[Path] = []
        previous_end = None
        for d1, d2, path in pairs:
            if previous_end is None:
                chain.append(path)
                previous_end = d2
            elif d1 == previous_end:
                chain.append(path)
                previous_end = d2
            elif d1 > previous_end:
                break
        if not chain:
            continue
        atlas_row = atlas_by_id.get(city_id, {})
        rate = summary.get("rate_cm_per_100d")
        if not isinstance(rate, (int, float)) or not math.isfinite(float(rate)):
            rate = atlas_row.get("rate_cm_per_100d")
        if not isinstance(rate, (int, float)) or not math.isfinite(float(rate)):
            period = summary.get("period", [])
            headline = summary.get("max_subsidence_cm")
            try:
                days = (date.fromisoformat(period[-1]) - date.fromisoformat(period[0])).days
                rate = float(headline) * 100.0 / days if days > 0 else None
            except (ValueError, TypeError, IndexError):
                rate = None
        scenes.append(Scene(city_id, subset_dir, chain, bbox, center,
                            None if rate is None else float(rate), atlas_row.get("rank")))
    return scenes, atlas


def lon_lat_axes(x: np.ndarray, y: np.ndarray, epsg: int) -> tuple[np.ndarray, np.ndarray]:
    transformer = Transformer.from_crs(epsg, 4326, always_xy=True)
    lon, _ = transformer.transform(x, np.full_like(x, float(np.median(y))))
    _, lat = transformer.transform(np.full_like(y, float(np.median(x))), y)
    return np.asarray(lon), np.asarray(lat)


def axis_coverage(lon_axis: np.ndarray, lat_axis: np.ndarray,
                  center: tuple[float, float], half_width: float) -> float:
    lon, lat = center
    lon_lo, lon_hi = float(np.nanmin(lon_axis)), float(np.nanmax(lon_axis))
    lat_lo, lat_hi = float(np.nanmin(lat_axis)), float(np.nanmax(lat_axis))
    span_lon = max(0.0, min(lon + half_width, lon_hi) - max(lon - half_width, lon_lo)) / (2 * half_width)
    span_lat = max(0.0, min(lat + half_width, lat_hi) - max(lat - half_width, lat_lo)) / (2 * half_width)
    return float(span_lon * span_lat)


def prepare_pair(path: Path, threshold: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int, float]:
    with np.load(path, allow_pickle=False) as z:
        unw = z["unw"].astype(np.float32, copy=True)
        coh = z["coh"].copy()
        conncomp = z["conncomp"].copy() if "conncomp" in z and z["conncomp"].size else None
        ion = z["ion"].copy() if "ion" in z and z["ion"].shape == unw.shape else None
        wavelength = float(z["wavelength"].item())
        x = z["x"].copy()
        y = z["y"].copy()
        epsg = int(z["epsg"].item())
        incidence = z["incidence"].copy() if "incidence" in z and z["incidence"].shape == unw.shape else None
    if ion is not None:
        unw -= ion
    cm = phase_to_cm(unw, wavelength)
    if conncomp is not None:
        cm = mask_components(cm, conncomp)
    cm = mask_coherence(cm, coh, threshold)
    cm = fast_deramp(cm)
    cm = cycle_outliers(cm, wavelength / 4.0 * 100.0)
    return cm, x, y, np.asarray(coh, dtype=np.float32) / (255.0 if np.issubdtype(np.asarray(coh).dtype, np.integer) else 1.0), epsg, wavelength


def choose_corner_references(scene: Scene) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Find three reproducible low-motion/high-coherence corner candidate windows."""
    unref_sum = None
    common = None
    coh_sum = None
    x = y = None
    epsg = None
    for path in scene.pair_paths:
        cm, px, py, coh, pair_epsg, _ = prepare_pair(path, 0.5)
        if unref_sum is None:
            x, y, epsg = px, py, pair_epsg
            unref_sum = np.zeros_like(cm, dtype=np.float32)
            common = np.ones(cm.shape, dtype=bool)
            coh_sum = np.zeros_like(cm, dtype=np.float32)
        if cm.shape != unref_sum.shape or pair_epsg != epsg or not np.array_equal(px, x) or not np.array_equal(py, y):
            raise ValueError(f"inconsistent grids in {scene.city_id}")
        ok = np.isfinite(cm)
        unref_sum[ok] += cm[ok]
        common &= ok
        coh_sum += coh
    if unref_sum is None or x is None or y is None or epsg is None:
        return [], {"reason": "no usable provisional chain"}
    lon_axis, lat_axis = lon_lat_axes(x, y, epsg)
    coverage = axis_coverage(lon_axis, lat_axis, scene.center, 0.20)
    if coverage < 0.98:
        return [], {"reason": "local subset does not cover the full +/-0.20 degree test box", "coverage_fraction": round(coverage, 4)}
    inside = (np.abs(lat_axis[:, None] - scene.center[1]) <= 0.20) & (np.abs(lon_axis[None, :] - scene.center[0]) <= 0.20)
    base_values = unref_sum[inside & common]
    if base_values.size == 0:
        return [], {"reason": "no pixels valid across provisional chain", "coverage_fraction": round(coverage, 4)}
    relative = unref_sum - float(np.median(base_values))
    common_window = np.zeros(common.shape, dtype=bool)
    windows = sliding_window_view(common, (2 * REF_RADIUS + 1, 2 * REF_RADIUS + 1))
    common_window[REF_RADIUS:-REF_RADIUS, REF_RADIUS:-REF_RADIUS] = windows.all(axis=(-1, -2))
    mean_coh = coh_sum / len(scene.pair_paths)
    # Quarter-box corner regions leave margin for a 7x7 reference window.
    corners = (
        ("northwest", lon_axis <= scene.center[0], lat_axis >= scene.center[1]),
        ("northeast", lon_axis >= scene.center[0], lat_axis >= scene.center[1]),
        ("southwest", lon_axis <= scene.center[0], lat_axis <= scene.center[1]),
    )
    transformer = Transformer.from_crs(epsg, 4326, always_xy=True)
    refs: list[dict[str, Any]] = []
    for name, col_side, row_side in corners:
        candidate = common_window & inside & col_side[None, :] & row_side[:, None]
        # Search the corner fringe and select a low-relative-motion, high-coherence window.
        fringe = (np.abs(lon_axis[None, :] - scene.center[0]) >= 0.10) & (np.abs(lat_axis[:, None] - scene.center[1]) >= 0.10)
        candidate &= fringe & (mean_coh >= 0.5)
        rr, cc = np.where(candidate)
        if rr.size == 0:
            continue
        # Sample candidates deterministically to limit large-scene sorting cost.
        sample = np.arange(0, rr.size, max(1, rr.size // 30000))
        rr, cc = rr[sample], cc[sample]
        score = np.abs(relative[rr, cc]) + (1.0 - mean_coh[rr, cc]) * 5.0
        order = np.argsort(score, kind="stable")
        chosen = None
        for idx in order[:1000]:
            r, c = int(rr[idx]), int(cc[idx])
            if all(math.hypot((r - int(q["row"])) * abs(float(y[1] - y[0])),
                              (c - int(q["col"])) * abs(float(x[1] - x[0]))) > 15000 for q in refs):
                chosen = (r, c, float(score[idx]))
                break
        if chosen is None:
            continue
        r, c, _ = chosen
        lon, lat = transformer.transform(float(x[c]), float(y[r]))
        window = relative[max(0, r - REF_RADIUS):r + REF_RADIUS + 1, max(0, c - REF_RADIUS):c + REF_RADIUS + 1]
        refs.append({"id": name, "lon": round(float(lon), 6), "lat": round(float(lat), 6),
                     "row": r, "col": c, "mean_coherence": round(float(mean_coh[r, c]), 4),
                     "relative_motion_cm": round(float(np.nanmedian(window)), 3),
                     "evidence": "corner low-motion proxy; geology/GNSS stability not independently verified"})
    return refs, {"coverage_fraction": round(coverage, 4), "reference_candidates_found": len(refs),
                  "reference_selection": "three separated corners in +/-0.20 degree box; highest coherence and lowest relative motion"}


def run_variants(scene: Scene, refs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(refs) != 3:
        return []
    results = []
    summary_path = (ROOT / "data/global" / scene.city_id / "summary.json")
    if not summary_path.is_file():
        summary_path = ROOT / "data" / scene.city_id / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    period = summary.get("period", [])
    days = (date.fromisoformat(period[-1]) - date.fromisoformat(period[0])).days if len(period) == 2 else 0
    if days <= 0:
        return []
    for threshold in COHERENCE_THRESHOLDS:
        accumulators: dict[str, np.ndarray] = {}
        validity: dict[str, np.ndarray] = {}
        grid = None
        for ref in refs:
            accumulators[ref["id"]] = None  # type: ignore[assignment]
            validity[ref["id"]] = None  # type: ignore[assignment]
        for path in scene.pair_paths:
            cm, x, y, _, epsg, wavelength = prepare_pair(path, threshold)
            if grid is None:
                grid = (x, y, epsg)
                for ref in refs:
                    accumulators[ref["id"]] = np.zeros_like(cm, dtype=np.float32)
                    validity[ref["id"]] = np.ones(cm.shape, dtype=bool)
            elif cm.shape != accumulators[refs[0]["id"]].shape or epsg != grid[2] or not np.array_equal(x, grid[0]) or not np.array_equal(y, grid[1]):
                raise ValueError(f"inconsistent grids in {scene.city_id}")
            for ref in refs:
                r, c = int(ref["row"]), int(ref["col"])
                window = cm[max(0, r - REF_RADIUS):r + REF_RADIUS + 1, max(0, c - REF_RADIUS):c + REF_RADIUS + 1]
                if not np.isfinite(window).any():
                    validity[ref["id"]][:] = False
                    continue
                referenced = cm - float(np.nanmedian(window))
                referenced = cycle_outliers(referenced, wavelength / 4.0 * 100.0)
                ok = np.isfinite(referenced)
                validity[ref["id"]] &= ok
                accumulators[ref["id"]][ok] += referenced[ok]
        if grid is None:
            continue
        x, y, epsg = grid
        lon_axis, lat_axis = lon_lat_axes(x, y, epsg)
        for ref in refs:
            ref_id = ref["id"]
            cum = accumulators[ref_id]
            cum[~validity[ref_id]] = np.nan
            for half_width in HALF_WIDTHS:
                coverage = axis_coverage(lon_axis, lat_axis, scene.center, half_width)
                if coverage < 0.98:
                    results.append({"reference_id": ref_id, "coherence_threshold": threshold,
                                    "box_half_width_deg": half_width, "valid": False,
                                    "coverage_fraction": round(coverage, 4),
                                    "reason": "local subset does not fully cover requested box"})
                    continue
                inside = ((np.abs(lat_axis[:, None] - scene.center[1]) <= half_width)
                          & (np.abs(lon_axis[None, :] - scene.center[0]) <= half_width))
                headline_cm, p2_cm = block_headline(cum, inside)
                if headline_cm is None or p2_cm is None:
                    results.append({"reference_id": ref_id, "coherence_threshold": threshold,
                                    "box_half_width_deg": half_width, "valid": False,
                                    "coverage_fraction": round(coverage, 4), "reason": "no eligible 1 km blocks"})
                    continue
                results.append({"reference_id": ref_id, "coherence_threshold": threshold,
                                "box_half_width_deg": half_width, "coverage_fraction": round(coverage, 4),
                                "valid": True, "headline_cm": round(headline_cm, 4),
                                "p2_cm": round(p2_cm, 4),
                                "rate_cm_per_100d": round(headline_cm * 100.0 / days, 5),
                                "period_days": days})
    return results


def build_report(subset_overrides: dict[str, Path] | None = None) -> dict[str, Any]:
    scenes, atlas = load_scene_inputs(subset_overrides)
    atlas_rows = {r["id"]: r for r in atlas.get("regions", []) if isinstance(r, dict) and r.get("id")}
    city_data: dict[str, dict[str, Any]] = {}
    variants_by_city: dict[str, list[dict[str, Any]]] = {}
    for scene in scenes:
        try:
            refs, selection = choose_corner_references(scene)
            variants = run_variants(scene, refs)
        except Exception as exc:
            refs, selection, variants = [], {"reason": f"processing error: {type(exc).__name__}: {exc}"}, []
        valid = [v for v in variants if v.get("valid")]
        base_rate = scene.atlas_rate
        rates = [float(v["rate_cm_per_100d"]) for v in valid]
        headline = [float(v["headline_cm"]) for v in valid]
        city_data[scene.city_id] = {
            "id": scene.city_id,
            "base_rate_cm_per_100d": base_rate,
            "min": round(min(headline), 4) if headline else None,
            "max": round(max(headline), 4) if headline else None,
            "spread_cm": round(max(headline) - min(headline), 4) if headline else None,
            "min_rate_cm_per_100d": round(min(rates), 5) if rates else None,
            "max_rate_cm_per_100d": round(max(rates), 5) if rates else None,
            "rank_min": None,
            "rank_max": None,
            "n_variants": len(valid),
            "n_variants_attempted": len(variants),
            "bbox_center_lonlat": [round(scene.center[0], 6), round(scene.center[1], 6)],
            "reference_candidates": [{k: v for k, v in r.items() if k not in {"row", "col"}} for r in refs],
            "reference_selection": selection,
            "variants": variants,
        }
        variants_by_city[scene.city_id] = valid

    # Rank cities independently for each matching (reference, threshold, box) combination.
    signatures = {(v.get("reference_id"), v.get("coherence_threshold"), v.get("box_half_width_deg"))
                  for values in variants_by_city.values() for v in values}
    rank_values: dict[str, list[int]] = {city_id: [] for city_id in city_data}
    tau_values: list[float] = []
    top3_sets: list[tuple[str, ...]] = []
    for sig in sorted(signatures, key=lambda s: (str(s[0]), float(s[1]), float(s[2]))):
        rows = []
        for city_id, values in variants_by_city.items():
            found = next((v for v in values if (v.get("reference_id"), v.get("coherence_threshold"), v.get("box_half_width_deg")) == sig), None)
            if found and city_data[city_id]["base_rate_cm_per_100d"] is not None:
                rows.append((city_id, float(found["rate_cm_per_100d"]), float(city_data[city_id]["base_rate_cm_per_100d"])))
        if len(rows) < 3:
            continue
        rows.sort(key=lambda row: row[1])
        for rank, (city_id, _, _) in enumerate(rows, 1):
            rank_values[city_id].append(rank)
        tau = kendall_tau_b([r[2] for r in rows], [r[1] for r in rows])
        if tau is not None and math.isfinite(float(tau)):
            tau_values.append(float(tau))
        top3_sets.append(tuple(row[0] for row in rows[:3]))
    for city_id, ranks in rank_values.items():
        if ranks:
            city_data[city_id]["rank_min"] = min(ranks)
            city_data[city_id]["rank_max"] = max(ranks)

    common_ids = [city_id for city_id, values in variants_by_city.items()
                  if len(values) == 27 and city_data[city_id]["base_rate_cm_per_100d"] is not None]
    common_top3_stable = None
    if len(common_ids) >= 3 and top3_sets:
        common_top3 = [tuple(city for city in row if city in common_ids) for row in top3_sets]
        common_top3_stable = all(row[:3] == common_top3[0][:3] for row in common_top3)

    top3_conclusion = (
        "stable across all tested variants" if common_top3_stable is True else
        "changes across tested variants" if common_top3_stable is False else
        "inconclusive: fewer than three cities have all 27 complete variants"
    )

    return {
        "quality": "provisional",
        "quality_note": "Robustness sweep of locally available provisional GUNW subsets; corner references are algorithmic low-motion proxies and are not independently confirmed stable ground.",
        "method": {
            "coherence_thresholds": list(COHERENCE_THRESHOLDS),
            "box_half_widths_deg": list(HALF_WIDTHS),
            "reference_candidates_per_city": 3,
            "headline": "Minimum eligible 13x13-pixel block median, at least 50% finite pixels, block standard deviation <= 2 cm; p2 is reported separately.",
            "preprocessing": "provisional adjacent pairs only; remove product ionosphere screen; mask connected-component zero and coherence; fit and remove a least-squares plane; remove half-cycle local outliers; reference every pair to a 7x7-pixel candidate window.",
            "box_coverage_rule": "A requested box is only scored when the local subset covers at least 98% of its lon/lat extent; incomplete boxes remain explicit invalid variants.",
            "reference_limit": "Corner candidates are selected from high-coherence, low-relative-motion windows. No geological basin polygon or independent GNSS/stable-ground evidence is available to prove they lie outside each basin.",
        },
        "n_cities": len(city_data),
        "n_common_cities_with_27_variants": len(common_ids),
        "top3_all_variants_stable": common_top3_stable,
        "top3_conclusion": top3_conclusion,
        "top3_stability_scope": common_ids,
        "kendall_tau_base_vs_variants": {
            "n_variant_rankings": len(tau_values),
            "mean": round(float(np.mean(tau_values)), 4) if tau_values else None,
            "min": round(float(np.min(tau_values)), 4) if tau_values else None,
            "max": round(float(np.max(tau_values)), 4) if tau_values else None,
        },
        "cities": list(city_data.values()),
    }


def write_outputs(report: dict[str, Any]) -> None:
    out_json = ROOT / "data/global/robustness.json"
    out_png = ROOT / "docs/story/media/pc7_atlas_robustness.png"
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    rows = list(report["cities"])
    rows.sort(key=lambda c: float(c["base_rate_cm_per_100d"]) if c.get("base_rate_cm_per_100d") is not None else 0.0)
    fig_h = max(4.0, 0.42 * len(rows) + 1.5)
    fig, ax = plt.subplots(figsize=(10, fig_h), constrained_layout=True)
    if rows:
        y = np.arange(len(rows))
        for yi, row in zip(y, rows):
            base = row.get("base_rate_cm_per_100d")
            if row.get("min_rate_cm_per_100d") is not None and row.get("max_rate_cm_per_100d") is not None:
                lo, hi = float(row["min_rate_cm_per_100d"]), float(row["max_rate_cm_per_100d"])
                ax.plot([lo, hi], [yi, yi], color="#2563eb", linewidth=2.2, solid_capstyle="round")
                if base is not None:
                    ax.scatter([float(base)], [yi], color="#b91c1c", s=26, zorder=3)
            else:
                if base is not None:
                    ax.scatter([float(base)], [yi], color="#8b949e", marker="x", s=30, zorder=3)
                ax.annotate("incomplete local coverage/reference set", (0.01, yi), xycoords=("axes fraction", "data"),
                            xytext=(2, 0), textcoords="offset points", color="#6b7280", fontsize=7, va="center")
        ax.set_yticks(y, [r["id"].replace("_", " ") for r in rows])
        ax.invert_yaxis()
        ax.set_xlabel("LOS subsidence rate (cm per 100 days; more negative = faster)")
        ax.set_title("Atlas rate range across reference, coherence and box variants")
        ax.grid(axis="x", alpha=0.25)
        ax.plot([], [], color="#2563eb", linewidth=2.2, label="variant min–max")
        ax.scatter([], [], color="#b91c1c", s=26, label="city summary rate")
        ax.legend(loc="best")
    else:
        ax.text(0.5, 0.5, "No city had enough complete local variants", ha="center", va="center")
        ax.set_axis_off()
    fig.savefig(out_png, dpi=180)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subset-dir", action="append", default=[], metavar="CITY=PATH",
                        help="Use fresh local subsets for a city (repeatable), without writing to shared pipeline/subset")
    args = parser.parse_args()
    try:
        overrides = parse_subset_overrides(args.subset_dir)
    except ValueError as exc:
        parser.error(str(exc))
    report = build_report(overrides)
    write_outputs(report)
    print(json.dumps({"cities": report["n_cities"], "common_27": report["n_common_cities_with_27_variants"],
                      "top3_stable": report["top3_all_variants_stable"],
                      "kendall_tau": report["kendall_tau_base_vs_variants"],
                      "files": ["data/global/robustness.json", "docs/story/media/pc7_atlas_robustness.png"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
