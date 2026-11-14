#!/usr/bin/env python3
"""Compute differential subsidence risk index along Central Valley linear infrastructure.

Reads:
  - risk/central_valley_infra.geojson (OSM canals, highways, railways)
  - analysis/out/central_valley_cum.npz (PC3 cumulative LOS displacement grid)

Writes:
  - data/central_valley/assets.json (GeoJSON FeatureCollection of top 10 highest-risk segments)

Usage:
  python risk/compute_risk.py
  python risk/compute_risk.py --self-test

Owner: PC6
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "validation"))
from compare import DISCLAIMER, project_to_crs  # noqa: E402

DEFAULT_INFRA = ROOT / "risk" / "central_valley_infra.geojson"
DEFAULT_NPZ = ROOT / "analysis" / "out" / "central_valley_cum.npz"
DEFAULT_OUT = ROOT / "data" / "central_valley" / "assets.json"

STEP_M = 200.0
MIN_SPAN_M = 1000.0
BLOCK_RADIUS_M = 480.0
MAX_SAMPLES_PER_FEATURE = 400


def classify_risk(gradient_mm_per_km: float, max_cm: float) -> str:
    if (gradient_mm_per_km >= 10.0 and max_cm <= -2.0) or max_cm <= -10.0:
        return "high"
    if (gradient_mm_per_km >= 5.0 and max_cm <= -1.0) or max_cm <= -5.0:
        return "medium"
    return "low"


def densify_utm_line(pts_x: np.ndarray, pts_y: np.ndarray, step_m: float = STEP_M) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Densify a polyline in projected meters and return (xs, ys, cum_dist_m)."""
    dx = np.diff(pts_x)
    dy = np.diff(pts_y)
    seg_len = np.hypot(dx, dy)
    total_len = float(seg_len.sum())
    eff_step = max(step_m, total_len / MAX_SAMPLES_PER_FEATURE) if total_len > 0 else step_m

    out_x: list[float] = [float(pts_x[0])]
    out_y: list[float] = [float(pts_y[0])]
    out_d: list[float] = [0.0]
    cum_d = 0.0

    for i, slen in enumerate(seg_len):
        if slen <= 0.0:
            continue
        n_sub = max(1, int(math.ceil(slen / eff_step)))
        for k in range(1, n_sub + 1):
            frac = k / n_sub
            out_x.append(float(pts_x[i] + frac * dx[i]))
            out_y.append(float(pts_y[i] + frac * dy[i]))
            out_d.append(cum_d + frac * float(slen))
        cum_d += float(slen)

    return np.asarray(out_x), np.asarray(out_y), np.asarray(out_d)


def sample_block_median(
    grid: np.ndarray,
    x_axis: np.ndarray,
    y_axis: np.ndarray,
    sx: np.ndarray,
    sy: np.ndarray,
    radius_m: float = BLOCK_RADIUS_M,
) -> np.ndarray:
    """Sample ~1 km NaN-median block around each coordinate to suppress InSAR pixel speckle."""
    dx = float(x_axis[1] - x_axis[0])
    dy = float(y_axis[1] - y_axis[0])
    half_win = max(1, int(round(radius_m / max(abs(dx), 1.0))))
    min_valid = max(4, ((2 * half_win + 1) ** 2) // 4)
    h, w = grid.shape
    cols = np.rint((sx - float(x_axis[0])) / dx).astype(int)
    rows = np.rint((sy - float(y_axis[0])) / dy).astype(int)

    vals = np.full(len(sx), np.nan, dtype=np.float64)
    for i, (r, c) in enumerate(zip(rows, cols)):
        if 0 <= r < h and 0 <= c < w:
            win = grid[max(r - half_win, 0) : min(r + half_win + 1, h), max(c - half_win, 0) : min(c + half_win + 1, w)]
            finite = win[np.isfinite(win)]
            if finite.size >= min_valid:
                vals[i] = float(np.median(finite))
    return vals


def evaluate_feature(
    feat: dict,
    grid: np.ndarray,
    x_axis: np.ndarray,
    y_axis: np.ndarray,
    epsg: int,
    proj_fn=project_to_crs,
) -> dict | None:
    geom = feat.get("geometry") or {}
    if geom.get("type") != "LineString":
        return None
    coords = geom.get("coordinates") or []
    if len(coords) < 2:
        return None

    lons = np.array([c[0] for c in coords], dtype=np.float64)
    lats = np.array([c[1] for c in coords], dtype=np.float64)
    px, py = proj_fn(lons, lats, epsg)
    sx, sy, sd = densify_utm_line(np.asarray(px, dtype=np.float64), np.asarray(py, dtype=np.float64))
    if len(sd) < 2 or sd[-1] < MIN_SPAN_M:
        return None

    vals = sample_block_median(grid, x_axis, y_axis, sx, sy)
    ok = np.isfinite(vals)
    if int(ok.sum()) < 2:
        return None

    vd = sd[ok]
    vv = vals[ok]
    if float(vd[-1] - vd[0]) < MIN_SPAN_M:
        return None

    # Pairwise differential subsidence gradient across spans >= MIN_SPAN_M (200 m)
    dd_km = (vd[None, :] - vd[:, None]) / 1000.0
    dv_mm = np.abs(vv[None, :] - vv[:, None]) * 10.0  # cm -> mm
    valid_pairs = dd_km >= (MIN_SPAN_M / 1000.0)
    if not valid_pairs.any():
        return None
    gradient_mm_per_km = float(np.max(dv_mm[valid_pairs] / dd_km[valid_pairs]))

    # Peak subsidence (most negative value if subsiding, else largest magnitude)
    min_v = float(np.min(vv))
    max_cm = min_v if min_v < 0.0 else float(vv[np.argmax(np.abs(vv))])
    risk = classify_risk(gradient_mm_per_km, max_cm)

    props = feat.get("properties") or {}
    infra_type = str(props.get("type") or "other")
    osm_id = props.get("osm_id")
    raw_name = str(props.get("name") or "").strip()
    display_name = raw_name if raw_name else f"Unnamed {infra_type} (osm:{osm_id})"

    return {
        "type": "Feature",
        "geometry": geom,
        "properties": {
            "name": display_name,
            "type": infra_type,
            "osm_id": osm_id,
            "risk": risk,
            "gradient_mm_per_km": round(gradient_mm_per_km, 2),
            "max_cm": round(max_cm, 2),
            "length_km": round(float(sd[-1]) / 1000.0, 2),
        },
    }


def make_batch_projector(epsg: int):
    try:
        from pyproj import Transformer

        tr = Transformer.from_crs(4326, epsg, always_xy=True)

        def _proj(lons, lats, _epsg):
            return tr.transform(lons, lats)

        return _proj
    except ImportError:

        def _proj(lons, lats, _epsg):
            out = [project_to_crs(float(lo), float(la), _epsg) for lo, la in zip(lons, lats)]
            return np.array([p[0] for p in out]), np.array([p[1] for p in out])

        return _proj


def compute_assets(infra_path: Path, npz_path: Path, top_n: int = 10) -> dict:
    if not infra_path.exists():
        raise FileNotFoundError(f"Infrastructure GeoJSON not found: {infra_path}")
    if not npz_path.exists():
        raise FileNotFoundError(f"NPZ file not found: {npz_path}")

    gj = json.loads(infra_path.read_text(encoding="utf-8"))
    d = np.load(npz_path, allow_pickle=False)
    cum_cm = np.asarray(d["cum_cm"], dtype=np.float64)
    x_axis = np.asarray(d["x"], dtype=np.float64)
    y_axis = np.asarray(d["y"], dtype=np.float64)
    epsg = int(d["epsg"])
    dates = [str(s) for s in d["dates"]] if "dates" in d else []
    quality = str(d["quality"]) if "quality" in d else "provisional"

    proj_fn = make_batch_projector(epsg)
    evaluated: list[dict] = []
    for feat in gj.get("features", []):
        res = evaluate_feature(feat, cum_cm, x_axis, y_axis, epsg, proj_fn=proj_fn)
        if res is not None:
            evaluated.append(res)

    counts = Counter(f["properties"]["risk"] for f in evaluated)
    evaluated.sort(
        key=lambda f: (
            f["properties"]["gradient_mm_per_km"],
            abs(f["properties"]["max_cm"]),
        ),
        reverse=True,
    )

    return {
        "type": "FeatureCollection",
        "quality": quality,
        "quality_note": DISCLAIMER,
        "license": "© OpenStreetMap contributors, ODbL",
        "summary": {
            "total_features_in_geojson": len(gj.get("features", [])),
            "evaluated_segments": len(evaluated),
            "high_risk_count": counts.get("high", 0),
            "medium_risk_count": counts.get("medium", 0),
            "low_risk_count": counts.get("low", 0),
            "period": [dates[0], dates[-1]] if len(dates) >= 2 else dates,
            "thresholds": {
                "high_gradient_mm_per_km": 10.0,
                "high_subsidence_cm": 10.0,
                "medium_gradient_mm_per_km": 5.0,
                "medium_subsidence_cm": 5.0,
                "min_span_m": MIN_SPAN_M,
            },
        },
        "features": evaluated[:top_n],
    }


def self_test() -> None:
    print("Running risk/compute_risk.py --self-test ...")
    # Build synthetic subsidence bowl centered near Tulare Basin / California Aqueduct / Friant-Kern
    xs = np.arange(200000.0, 330000.0, 160.0, dtype=np.float64)
    ys = np.arange(4060000.0, 3940000.0, -160.0, dtype=np.float64)
    XX, YY = np.meshgrid(xs, ys)
    # Two Gaussian subsidence bowls: Tulare Basin (-12 cm, sigma=5 km) & Friant-Kern edge (-9 cm, sigma=4 km)
    bx1, by1 = project_to_crs(-119.50, 36.00, 32611)
    bx2, by2 = project_to_crs(-119.15, 36.15, 32611)
    cum = (
        -12.0 * np.exp(-((XX - bx1) ** 2 + (YY - by1) ** 2) / (2.0 * 5000.0**2))
        - 9.0 * np.exp(-((XX - bx2) ** 2 + (YY - by2) ** 2) / (2.0 * 4000.0**2))
    ).astype(np.float32)

    with tempfile.TemporaryDirectory() as tmp:
        npz_path = Path(tmp) / "synthetic_cum.npz"
        np.savez_compressed(
            npz_path,
            cum_cm=cum,
            x=xs,
            y=ys,
            epsg=np.int32(32611),
            dates=np.array(["2026-06-28", "2026-09-20"]),
            quality="provisional",
        )
        out = compute_assets(DEFAULT_INFRA, npz_path, top_n=10)

    s = out["summary"]
    print(
        f"  Evaluated {s['evaluated_segments']}/{s['total_features_in_geojson']} segments: "
        f"high={s['high_risk_count']}, medium={s['medium_risk_count']}, low={s['low_risk_count']}"
    )
    assert s["evaluated_segments"] > 500, "Expected >500 segments inside synthetic grid"
    assert s["high_risk_count"] > 0, "Expected high-risk segments near synthetic bowl"
    assert len(out["features"]) == 10, "Expected top 10 segments"
    for rank, feat in enumerate(out["features"], 1):
        p = feat["properties"]
        assert {"name", "type", "risk", "gradient_mm_per_km", "max_cm"}.issubset(p.keys())
        print(
            f"  #{rank:2d} [{p['risk']:6s}] {p['type']:8s} grad={p['gradient_mm_per_km']:6.2f} mm/km "
            f"max={p['max_cm']:6.2f} cm len={p['length_km']:5.2f} km | {p['name']}"
        )

    dumped = json.dumps(out, allow_nan=False)
    assert "NaN" not in dumped
    print("Self-test passed (top 10 segments valid GeoJSON, zero NaNs).")


def main() -> None:
    ap = argparse.ArgumentParser(description="Compute infrastructure subsidence risk GeoJSON.")
    ap.add_argument("--infra", type=Path, default=DEFAULT_INFRA)
    ap.add_argument("--npz", type=Path, default=DEFAULT_NPZ)
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Explicit output assets.json path (overrides --data-dir).",
    )
    ap.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Target output directory where assets.json is written if --out is omitted.",
    )
    ap.add_argument(
        "--quality",
        type=str,
        default=None,
        help="Optional quality label override (e.g. 'mixed' for full-year beta+provisional runs).",
    )
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return

    out_path = args.out or ((args.data_dir / "assets.json") if args.data_dir else DEFAULT_OUT)
    out = compute_assets(args.infra, args.npz, top_n=args.top)
    if args.quality:
        out["quality"] = args.quality
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(out, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    s = out["summary"]
    print(
        f"Wrote {out_path}: evaluated={s['evaluated_segments']}, "
        f"high={s['high_risk_count']}, medium={s['medium_risk_count']}, low={s['low_risk_count']}"
    )
    for rank, feat in enumerate(out["features"], 1):
        p = feat["properties"]
        print(
            f"  #{rank:2d} [{p['risk']:6s}] {p['type']:8s} grad={p['gradient_mm_per_km']:6.2f} mm/km "
            f"max={p['max_cm']:6.2f} cm len={p['length_km']:5.2f} km | {p['name']}"
        )


if __name__ == "__main__":
    main()
