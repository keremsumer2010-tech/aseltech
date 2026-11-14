"""Probabilistic vertical-settlement screening for the current Central Valley top ten.

This is an offline, provisional screening calculation. It reuses the local PC5
formal phase-noise model and never downloads data or writes into PC5's outputs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer
from scipy.ndimage import map_coordinates

ROOT = Path(__file__).resolve().parents[1]
N_TRIALS = 1000
SEED = 7102026
SPACING_M = 100.0
BASELINES_M = (100.0, 500.0, 1000.0)
BETA_THRESHOLDS = {"1/500": 1.0 / 500.0, "1/1000": 1.0 / 1000.0}


def beta_and_range(displacement_cm: np.ndarray, distances_m: np.ndarray) -> tuple[float, float]:
    """Return maximum absolute angular distortion and profile range."""
    d = np.asarray(displacement_cm, dtype=float)
    s = np.asarray(distances_m, dtype=float)
    if d.ndim != 1 or s.shape != d.shape or d.size == 0:
        raise ValueError("displacement and distance must be non-empty matching vectors")
    best = 0.0
    for baseline in BASELINES_M:
        for i in range(d.size):
            j = int(np.searchsorted(s, s[i] + baseline))
            if j < d.size and abs((s[j] - s[i]) - baseline) <= 1e-6:
                best = max(best, abs(d[j] - d[i]) / (baseline * 100.0))
    return float(best), float(np.max(d) - np.min(d))


def simulate_profile(
    displacement_cm: np.ndarray,
    sigma_cm: np.ndarray,
    distances_m: np.ndarray,
    trials: int = N_TRIALS,
    seed: int = SEED,
) -> dict:
    """Propagate independent per-sample Gaussian sigma through profile metrics."""
    mean = np.asarray(displacement_cm, dtype=float)
    sigma = np.asarray(sigma_cm, dtype=float)
    dist = np.asarray(distances_m, dtype=float)
    if mean.ndim != 1 or sigma.shape != mean.shape or dist.shape != mean.shape:
        raise ValueError("profile, sigma and distance vectors must have equal shape")
    if mean.size == 0 or not np.all(np.isfinite(mean)) or not np.all(np.isfinite(sigma)):
        raise ValueError("profile and sigma must contain finite values")
    if np.any(sigma < 0) or trials <= 0:
        raise ValueError("sigma must be non-negative and trials positive")

    beta_mean, range_mean = beta_and_range(mean, dist)
    rng = np.random.default_rng(seed)
    draws = rng.normal(mean, sigma, size=(trials, mean.size))
    beta_draws = np.zeros(trials, dtype=float)
    for baseline in BASELINES_M:
        for i in range(mean.size):
            j = int(np.searchsorted(dist, dist[i] + baseline))
            if j < mean.size and abs((dist[j] - dist[i]) - baseline) <= 1e-6:
                beta_draws = np.maximum(beta_draws, np.abs(draws[:, j] - draws[:, i]) / (baseline * 100.0))
    range_draws = np.ptp(draws, axis=1)
    return {
        "beta_max": beta_mean,
        "max_differential_cm": range_mean,
        "p_beta_exceed": {
            label: float(np.mean(beta_draws > threshold))
            for label, threshold in BETA_THRESHOLDS.items()
        },
        "p_diff_gt_10cm": float(np.mean(range_draws > 10.0)),
        "ci90": {
            "beta_max": [float(v) for v in np.percentile(beta_draws, [5, 95])],
            "max_differential_cm": [float(v) for v in np.percentile(range_draws, [5, 95])],
        },
        "_beta_draws": beta_draws,
        "_range_draws": range_draws,
    }


def _load_sigma() -> tuple[np.ndarray, dict]:
    """Recompute numeric PC5 LOS sigma from local provisional subset files."""
    sys.path.insert(0, str(ROOT))
    from analysis.pc5.uncertainty_map import (  # local code; no output generation
        compute_chain_sigma_cm,
        load_site_provisional_chain,
        normalize_coherence,
        utm_to_lonlat,
    )

    pairs, notes = load_site_provisional_chain("central_valley", ROOT / "pipeline/subset/central_valley")
    coherences, wavelengths, masks = [], [], []
    for _, _, _, data in pairs:
        coherence = normalize_coherence(data["coh"])
        mask = np.isfinite(data["unw"]) & (coherence >= 0.3)
        if "conncomp" in data:
            mask &= data["conncomp"] != 0
        coherences.append(coherence)
        wavelengths.append(float(data["wavelength"]))
        masks.append(mask)
    sigma, valid = compute_chain_sigma_cm(coherences, wavelengths, masks, looks=208.0)
    meta = json.loads((ROOT / "data/central_valley/uncertainty/meta.json").read_text(encoding="utf-8"))
    with np.load(ROOT / "analysis/out/central_valley_cum.npz", allow_pickle=False) as raster:
        x, y, epsg = raster["x"].astype(float), raster["y"].astype(float), int(raster["epsg"])
    xx, yy = np.meshgrid(x, y)
    lon, lat = utm_to_lonlat(xx, yy, epsg)
    west, south, east, north = (float(v) for v in meta["bbox"])
    in_bbox = (lon >= west) & (lon <= east) & (lat >= south) & (lat <= north)
    observed = float(np.nanmedian(sigma[valid & in_bbox]))
    if abs(observed - float(meta["median_sigma_cm"])) > 0.002:
        raise ValueError(f"Recomputed sigma median {observed:.4f} cm differs from PC5 metadata")
    return np.where(valid, sigma, np.nan), {
        "pairs": len(pairs),
        "period": meta.get("period"),
        "median_sigma_cm_recomputed": round(observed, 4),
        "median_sigma_cm_metadata": meta.get("median_sigma_cm"),
        "p90_sigma_cm_metadata": meta.get("p90_sigma_cm"),
        "model": "PC5 Cramér-Rao formal phase-noise lower bound; excludes atmospheric, ramp and unwrapping errors",
        "chain_notes": notes,
    }


def _sample_line(coords: list[list[float]], transformer: Transformer) -> tuple[np.ndarray, np.ndarray]:
    xy = np.column_stack(transformer.transform(
        np.asarray(coords, dtype=float)[:, 0], np.asarray(coords, dtype=float)[:, 1]
    ))
    lengths = np.hypot(np.diff(xy[:, 0]), np.diff(xy[:, 1]))
    cumulative = np.concatenate(([0.0], np.cumsum(lengths)))
    total = float(cumulative[-1])
    if total <= 0:
        return np.array([], dtype=float), np.empty((0, 2), dtype=float)
    distances = np.arange(0.0, total + 1e-6, SPACING_M)
    # Include the final endpoint for the full-segment differential metric. It is
    # not used for angular distortion unless it falls exactly on a 100 m grid.
    if total - distances[-1] > 1e-6:
        distances = np.append(distances, total)
    seg = np.minimum(np.searchsorted(cumulative, distances, side="right") - 1, len(lengths) - 1)
    seg = np.maximum(seg, 0)
    frac = (distances - cumulative[seg]) / np.maximum(lengths[seg], 1e-9)
    points = xy[seg] + frac[:, None] * (xy[seg + 1] - xy[seg])
    return distances, points


def _interp(grid: np.ndarray, rows: np.ndarray, cols: np.ndarray) -> np.ndarray:
    return map_coordinates(grid, np.vstack((rows, cols)), order=1, mode="constant", cval=np.nan)


def _analyze_feature(feature: dict, cum: np.ndarray, sigma_los: np.ndarray, x: np.ndarray, y: np.ndarray, incidence: np.ndarray, transformer: Transformer, seed: int) -> dict | None:
    geometry = feature.get("geometry") or {}
    if geometry.get("type") != "LineString":
        return None
    distances, points = _sample_line(geometry.get("coordinates", []), transformer)
    if distances.size < 2:
        return None
    cols = (points[:, 0] - x[0]) / (x[1] - x[0])
    rows = (points[:, 1] - y[0]) / (y[1] - y[0])
    los = _interp(cum, rows, cols)
    sigma = _interp(sigma_los, rows, cols)
    theta = _interp(incidence.astype(float), rows, cols)
    valid = np.isfinite(los) & np.isfinite(sigma) & np.isfinite(theta) & (theta > 0) & (theta < 90)
    # Retain the continuous segment spacing: never bridge a masked-data gap.
    runs: list[np.ndarray] = []
    starts = np.flatnonzero(valid & np.r_[True, ~valid[:-1]])
    ends = np.flatnonzero(valid & np.r_[~valid[1:], True]) + 1
    for start, end in zip(starts, ends):
        if end - start >= 2:
            runs.append(np.arange(start, end))
    if not runs:
        return None

    # Preserve line order and evaluate each valid run independently.
    vertical_runs, sigma_runs, distance_runs = [], [], []
    for idx in runs:
        cosine = np.cos(np.deg2rad(theta[idx]))
        vertical_runs.append(los[idx] / cosine)
        sigma_runs.append(sigma[idx] / cosine)
        distance_runs.append(distances[idx] - distances[idx[0]])

    # Aggregate beta and segment-wide differential over valid profile runs.
    deterministic_beta = 0.0
    deterministic_range = 0.0
    simulations = []
    for run_i, (mu, sd, ds) in enumerate(zip(vertical_runs, sigma_runs, distance_runs)):
        deterministic_beta = max(deterministic_beta, beta_and_range(mu, ds)[0])
        deterministic_range = max(deterministic_range, beta_and_range(mu, ds)[1])
        simulations.append(simulate_profile(mu, sd, ds, seed=seed + run_i))
    # Combine valid continuous runs by taking the per-trial segment maximum.
    beta_draws = np.maximum.reduce([item["_beta_draws"] for item in simulations])
    differential_draws = np.maximum.reduce([item["_range_draws"] for item in simulations])
    beta_probs = {label: float(np.mean(beta_draws > threshold)) for label, threshold in BETA_THRESHOLDS.items()}
    p_diff = float(np.mean(differential_draws > 10.0))
    beta_ci = [float(v) for v in np.percentile(beta_draws, [5, 95])]
    differential_ci = [float(v) for v in np.percentile(differential_draws, [5, 95])]
    props = feature.get("properties", {})
    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": {
            "name": props.get("name") or f"Unnamed {props.get('type', 'asset')} (OSM {props.get('osm_id')})",
            "type": props.get("type"),
            "osm_id": props.get("osm_id"),
            "beta_max": deterministic_beta,
            "p_beta_exceed": beta_probs,
            "max_differential_cm": deterministic_range,
            "p_diff_gt_10cm": p_diff,
            "ci90": {"beta_max": beta_ci, "max_differential_cm": differential_ci},
        },
    }


def run(output_path: Path | None = None, chart_path: Path | None = None) -> dict:
    cum_path = ROOT / "analysis/out/central_valley_cum.npz"
    with np.load(cum_path, allow_pickle=False) as data:
        cum = data["cum_cm"].astype(float)
        x, y = data["x"].astype(float), data["y"].astype(float)
        incidence = data["incidence"]
        epsg = int(data["epsg"])
        quality = str(data["quality"])
    if quality != "provisional":
        raise ValueError(f"Expected provisional raster, got {quality}")
    sigma_los, sigma_meta = _load_sigma()
    infra = json.loads((ROOT / "risk/central_valley_infra.geojson").read_text(encoding="utf-8"))
    current = json.loads((ROOT / "data/central_valley/assets.json").read_text(encoding="utf-8"))
    by_id = {f.get("properties", {}).get("osm_id"): f for f in infra.get("features", [])}
    transformer = Transformer.from_crs(4326, epsg, always_xy=True)
    results = []
    for i, asset in enumerate(current.get("features", [])):
        osm_id = asset.get("properties", {}).get("osm_id")
        source = by_id.get(osm_id)
        if source is None:
            continue
        analyzed = _analyze_feature(source, cum, sigma_los, x, y, incidence, transformer, SEED + i * N_TRIALS)
        if analyzed:
            results.append(analyzed)
    if not results:
        raise ValueError("No current indexed asset had a valid sampled raster profile")

    deterministic = sorted(current["features"], key=lambda f: f.get("properties", {}).get("gradient_mm_per_km", -np.inf), reverse=True)
    probabilistic = sorted(results, key=lambda f: (f["properties"]["p_beta_exceed"]["1/500"], f["properties"]["beta_max"]), reverse=True)
    old_top = [f["properties"].get("osm_id") for f in deterministic[:10]]
    new_top = [f["properties"].get("osm_id") for f in probabilistic[:10]]
    output = {
        "type": "FeatureCollection",
        "quality": "provisional",
        "quality_note": "Probability screening on the ten existing deterministic assets only; not a design or safety assessment.",
        "license": current.get("license", "© OpenStreetMap contributors, ODbL"),
        "method": {
            "source_raster": "analysis/out/central_valley_cum.npz",
            "uncertainty": sigma_meta,
            "vertical_assumption": "vertical displacement = LOS / cos(local incidence); horizontal motion is assumed negligible",
            "spacing_m": SPACING_M,
            "beta_baselines_m": list(BASELINES_M),
            "beta_thresholds": BETA_THRESHOLDS,
            "trials": N_TRIALS,
            "seed": SEED,
            "sample_sigma_assumption": "independent Gaussian formal phase-noise samples; spatial covariance and atmospheric/unwrapping errors are not modeled",
            "scope": "The ten IDs in data/central_valley/assets.json, matched to risk/central_valley_infra.geojson; 3,238-source corridor file is not exhaustively scored.",
        },
        "summary": {
            "analyzed_assets": len(results),
            "deterministic_top10_osm_ids": old_top,
            "probabilistic_top10_osm_ids": new_top,
            "top10_overlap_count": len(set(old_top) & set(new_top)),
            "top10_order_changed": old_top != new_top,
        },
        "features": results,
    }
    out_file = output_path or ROOT / "data/central_valley/assets_prob.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    chart_file = chart_path or ROOT / "docs/story/media/pc7_risk_prob.png"
    _plot(results, chart_file)
    return output


def _plot(features: list[dict], path: Path) -> None:
    ranked = sorted(features, key=lambda f: (f["properties"]["p_beta_exceed"]["1/500"], f["properties"]["beta_max"]), reverse=True)[:10]
    labels = [textwrap.fill(f["properties"]["name"], width=24) for f in ranked][::-1]
    probs = [f["properties"]["p_diff_gt_10cm"] for f in ranked][::-1]
    beta = [f["properties"]["beta_max"] for f in ranked][::-1]
    fig, ax = plt.subplots(figsize=(11, 7.2))
    yloc = np.arange(len(labels))
    ax.barh(yloc, probs, color="#286f8e", alpha=0.86, label="P(segment differential > 10 cm)")
    ax.set_yticks(yloc, labels)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Monte Carlo exceedance probability", labelpad=12)
    ax.set_title("Central Valley infrastructure: provisional probabilistic screen")
    ax.grid(axis="x", alpha=0.22)
    ax2 = ax.twiny()
    ax2.scatter(beta, yloc, marker="|", s=130, color="#d17c26", label="deterministic β max")
    ax2.set_xlabel("Maximum angular distortion β (dimensionless)")
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, loc="lower right", fontsize=8)
    fig.subplots_adjust(left=0.32, right=0.95, bottom=0.18, top=0.87)
    fig.text(0.32, 0.025, "P(β > 1/500) = 0/1,000 for all ten assets. Formal phase-noise lower bound only; not a safety rating.", fontsize=8)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "data/central_valley/assets_prob.json")
    parser.add_argument("--chart", type=Path, default=ROOT / "docs/story/media/pc7_risk_prob.png")
    args = parser.parse_args()
    result = run(args.output, args.chart)
    print(json.dumps(result["summary"], indent=2))
