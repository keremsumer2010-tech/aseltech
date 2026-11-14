"""Q28: Karapinar sinkhole ring subsidence & OSM infrastructure proximity analysis.

Quantifies:
1. Cumulative NISAR LOS subsidence (`analysis/out/karapinar_cum.npz`) inside radial
   rings (0-1 km, 1-2 km, 2-5 km, >5 km background) around the 29 sourced sinkholes
   in `data/karapinar/sinkholes.geojson`.
2. Minimum distance (m) from each OSM corridor in `risk/karapinar_infra.geojson`
   to the nearest sinkhole, alongside block-median differential gradient (mm/km)
   reusing helpers from `risk/compute_risk.py`.

Outputs: `data/karapinar/assets.json` (zero NaNs, LF newlines, provisional metadata).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute_risk as cr  # noqa: E402

DEFAULT_SINKHOLES = ROOT / "data" / "karapinar" / "sinkholes.geojson"
DEFAULT_INFRA = ROOT / "risk" / "karapinar_infra.geojson"
DEFAULT_NPZ = ROOT / "analysis" / "out" / "karapinar_cum.npz"
DEFAULT_OUT = ROOT / "data" / "karapinar" / "assets.json"


def _clean_float(val: float | None, decimals: int = 3) -> float | None:
    if val is None or not math.isfinite(val):
        return None
    return round(float(val), decimals)


def point_to_polyline_distance_m(px: float, py: float, line_xy: np.ndarray) -> float:
    """Return exact minimum Euclidean distance (m) from point (px, py) to 2D polyline."""
    if len(line_xy) == 0:
        return math.inf
    if len(line_xy) == 1:
        return float(math.hypot(px - line_xy[0, 0], py - line_xy[0, 1]))
    ax = line_xy[:-1, 0]
    ay = line_xy[:-1, 1]
    bx = line_xy[1:, 0]
    by = line_xy[1:, 1]
    dx = bx - ax
    dy = by - ay
    seg_len2 = dx * dx + dy * dy
    t = np.where(seg_len2 > 1e-9, ((px - ax) * dx + (py - ay) * dy) / np.maximum(seg_len2, 1e-9), 0.0)
    t = np.clip(t, 0.0, 1.0)
    proj_x = ax + t * dx
    proj_y = ay + t * dy
    dists = np.hypot(px - proj_x, py - proj_y)
    return float(np.min(dists))


def analyze_sinkhole_rings(
    cum_cm: np.ndarray,
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    epsg: int,
    sinkhole_features: list[dict],
    project_fn,
) -> dict:
    """Compute subsidence statistics across radial rings around sinkhole points."""
    gx, gy = np.meshgrid(x_grid, y_grid)
    valid_mask = np.isfinite(cum_cm)
    vx = gx[valid_mask]
    vy = gy[valid_mask]
    vz = cum_cm[valid_mask].astype(float)

    sh_coords_ll = []
    sh_meta = []
    for feat in sinkhole_features:
        coords = feat.get("geometry", {}).get("coordinates", [])
        if len(coords) >= 2:
            sh_coords_ll.append((float(coords[0]), float(coords[1])))
            sh_meta.append(feat.get("properties", {}))

    sh_px, sh_py = project_fn(
        np.array([c[0] for c in sh_coords_ll], dtype=float),
        np.array([c[1] for c in sh_coords_ll], dtype=float),
        epsg,
    )
    sh_xy = np.column_stack([np.asarray(sh_px, dtype=float), np.asarray(sh_py, dtype=float)])

    # Distance from each valid radar pixel to nearest sinkhole (m)
    dx = vx[:, None] - sh_xy[:, 0][None, :]
    dy = vy[:, None] - sh_xy[:, 1][None, :]
    min_dist_m = np.min(np.hypot(dx, dy), axis=1)

    region_mean = float(np.mean(vz)) if len(vz) else 0.0
    region_median = float(np.median(vz)) if len(vz) else 0.0

    def _band_stats(mask: np.ndarray, label: str) -> dict:
        cnt = int(np.sum(mask))
        if cnt == 0:
            return {
                "band": label,
                "pixel_count": 0,
                "mean_cm": None,
                "median_cm": None,
                "min_cm": None,
                "delta_vs_region_mean_cm": None,
                "pct_subsiding_over_2cm": None,
            }
        vals = vz[mask]
        mean_v = float(np.mean(vals))
        return {
            "band": label,
            "pixel_count": cnt,
            "mean_cm": _clean_float(mean_v),
            "median_cm": _clean_float(float(np.median(vals))),
            "min_cm": _clean_float(float(np.min(vals))),
            "delta_vs_region_mean_cm": _clean_float(mean_v - region_mean),
            "pct_subsiding_over_2cm": _clean_float(float(np.mean(vals <= -2.0) * 100.0), 1),
        }

    disjoint_bands = [
        _band_stats(min_dist_m <= 1000.0, "0-1 km"),
        _band_stats((min_dist_m > 1000.0) & (min_dist_m <= 2000.0), "1-2 km"),
        _band_stats((min_dist_m > 2000.0) & (min_dist_m <= 5000.0), "2-5 km"),
        _band_stats(min_dist_m > 5000.0, ">5 km (background)"),
    ]
    cumulative_disks = [
        _band_stats(min_dist_m <= 1000.0, "<=1 km"),
        _band_stats(min_dist_m <= 2000.0, "<=2 km"),
        _band_stats(min_dist_m <= 5000.0, "<=5 km"),
    ]

    # Per-sinkhole 1 km disk local subsidence check
    per_sinkhole = []
    for idx, meta in enumerate(sh_meta):
        sx, sy = sh_xy[idx, 0], sh_xy[idx, 1]
        d_px = np.hypot(vx - sx, vy - sy)
        m1 = d_px <= 1000.0
        m2 = d_px <= 2000.0
        per_sinkhole.append({
            "name": meta.get("name", f"Sinkhole {idx + 1}"),
            "year_formed": meta.get("year_formed"),
            "pixels_within_1km": int(np.sum(m1)),
            "mean_cm_within_1km": _clean_float(float(np.mean(vz[m1]))) if np.any(m1) else None,
            "min_cm_within_1km": _clean_float(float(np.min(vz[m1]))) if np.any(m1) else None,
            "mean_cm_within_2km": _clean_float(float(np.mean(vz[m2]))) if np.any(m2) else None,
        })

    in_footprint = [s for s in per_sinkhole if s["pixels_within_1km"] > 0]
    in_footprint.sort(key=lambda s: s["mean_cm_within_1km"] if s["mean_cm_within_1km"] is not None else 999.0)

    return {
        "sinkhole_count": len(sh_meta),
        "sinkholes_inside_1km_footprint": len(in_footprint),
        "region_valid_pixels": int(len(vz)),
        "region_mean_cm": _clean_float(region_mean),
        "region_median_cm": _clean_float(region_median),
        "region_std_cm": _clean_float(float(np.std(vz))) if len(vz) else None,
        "region_min_cm": _clean_float(float(np.min(vz))) if len(vz) else None,
        "disjoint_rings": disjoint_bands,
        "cumulative_disks": cumulative_disks,
        "most_subsiding_sinkholes_1km": in_footprint[:10],
        "sh_xy": sh_xy,
        "sh_meta": sh_meta,
    }


def compute_karapinar_assets(
    sinkholes_path: Path = DEFAULT_SINKHOLES,
    infra_path: Path = DEFAULT_INFRA,
    npz_path: Path = DEFAULT_NPZ,
    out_path: Path = DEFAULT_OUT,
    quality_override: str | None = None,
) -> dict:
    """Run sinkhole ring + OSM proximity/gradient risk analysis and save JSON."""
    with open(sinkholes_path, "r", encoding="utf-8") as f:
        sh_gj = json.load(f)
    with open(infra_path, "r", encoding="utf-8") as f:
        infra_gj = json.load(f)

    with np.load(npz_path, allow_pickle=True) as z:
        cum_cm = z["cum_cm"]
        x_grid = z["x"]
        y_grid = z["y"]
        epsg = int(z["epsg"])
        dates = [str(d) for d in z["dates"]]
        quality = quality_override or (str(z["quality"]) if "quality" in z else "provisional")
    project_fn = cr.make_batch_projector(epsg)

    ring_info = analyze_sinkhole_rings(cum_cm, x_grid, y_grid, epsg, sh_gj["features"], project_fn)
    sh_xy = ring_info.pop("sh_xy")
    sh_meta = ring_info.pop("sh_meta")

    evaluated_features = []
    within_1km_count = 0
    within_2km_count = 0
    within_5km_count = 0
    risk_counts = {"high": 0, "medium": 0, "low": 0, "outside_or_short": 0}

    for feat in infra_gj.get("features", []):
        props = dict(feat.get("properties", {}))
        geom = feat.get("geometry", {})
        if geom.get("type") != "LineString" or len(geom.get("coordinates", [])) < 2:
            continue
        coords = np.asarray(geom["coordinates"], dtype=float)
        lx, ly = project_fn(coords[:, 0], coords[:, 1], epsg)
        line_xy = np.column_stack([np.asarray(lx, dtype=float), np.asarray(ly, dtype=float)])

        # Exact shortest distance to any sourced sinkhole (m)
        best_dist = math.inf
        best_idx = 0
        for i in range(len(sh_xy)):
            d_m = point_to_polyline_distance_m(float(sh_xy[i, 0]), float(sh_xy[i, 1]), line_xy)
            if d_m < best_dist:
                best_dist = d_m
                best_idx = i

        best_meta = sh_meta[best_idx]
        if best_dist <= 1000.0:
            within_1km_count += 1
        if best_dist <= 2000.0:
            within_2km_count += 1
        if best_dist <= 5000.0:
            within_5km_count += 1

        # Also evaluate InSAR subsidence gradient reusing compute_risk.py
        grad_res = cr.evaluate_feature(feat, cum_cm, x_grid, y_grid, epsg, project_fn)
        if grad_res is not None:
            grad_props = grad_res["properties"]
            risk_cls = grad_props["risk"]
            risk_counts[risk_cls] = risk_counts.get(risk_cls, 0) + 1
            out_props = {
                **grad_props,
                "nearest_sinkhole_m": round(best_dist, 1),
                "nearest_sinkhole_name": best_meta.get("name"),
                "nearest_sinkhole_year": best_meta.get("year_formed"),
            }
        else:
            # Segment outside radar footprint or shorter than MIN_SPAN_M; keep proximity data
            seg_len_m = float(np.sum(np.hypot(np.diff(line_xy[:, 0]), np.diff(line_xy[:, 1]))))
            risk_counts["outside_or_short"] += 1
            out_props = {
                "name": props.get("name") or f"Unnamed {props.get('type', 'road')} (osm:{props.get('osm_id', '')})",
                "type": props.get("type", "unknown"),
                "osm_id": props.get("osm_id"),
                "risk": "low" if best_dist > 2000.0 else ("high" if best_dist <= 1000.0 else "medium"),
                "gradient_mm_per_km": None,
                "max_cm": None,
                "length_km": round(seg_len_m / 1000.0, 2),
                "nearest_sinkhole_m": round(best_dist, 1),
                "nearest_sinkhole_name": best_meta.get("name"),
                "nearest_sinkhole_year": best_meta.get("year_formed"),
            }

        evaluated_features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": out_props,
        })

    # Rank segments closest to sinkholes and highest subsidence gradient first
    evaluated_features.sort(
        key=lambda f: (
            f["properties"]["nearest_sinkhole_m"],
            -(f["properties"]["gradient_mm_per_km"] or 0.0),
        )
    )

    payload = {
        "type": "FeatureCollection",
        "site": "karapinar",
        "quality": quality,
        "quality_note": cr.DISCLAIMER,
        "license": "OSM infrastructure © OpenStreetMap contributors (ODbL); Sinkholes compiled from peer-reviewed literature (data/karapinar/sinkholes.geojson)",
        "summary": {
            "period": [dates[0], dates[-1]],
            "total_infra_segments": len(evaluated_features),
            "segments_within_1km_of_sinkhole": within_1km_count,
            "segments_within_2km_of_sinkhole": within_2km_count,
            "segments_within_5km_of_sinkhole": within_5km_count,
            "risk_counts": risk_counts,
            "sinkhole_ring_analysis": ring_info,
        },
        "features": evaluated_features,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return payload


def self_test() -> None:
    """Verify ring bullseye detection, zero-distance polyline hit, and zero NaN emission."""
    print("Running karapinar_risk.py self-test...")
    x = np.arange(520000.0, 535000.0, 100.0)
    y = np.arange(4170000.0, 4185000.0, 100.0)
    gx, gy = np.meshgrid(x, y)
    cx, cy = 527500.0, 4177500.0
    dist = np.hypot(gx - cx, gy - cy)
    # Synthetic subsidence bowl: -8 cm inside 1 km fading toward 0 cm outside 3 km
    cum = -8.0 * np.exp(-0.5 * (dist / 1100.0) ** 2)

    from pyproj import Transformer
    to_ll = Transformer.from_crs("EPSG:32636", "EPSG:4326", always_xy=True)
    slon, slat = to_ll.transform(cx, cy)
    p1 = to_ll.transform(cx - 1000.0, cy)
    p2 = to_ll.transform(cx + 1000.0, cy)

    with tempfile.TemporaryDirectory() as tmp:
        tp = Path(tmp)
        npz_p = tp / "test_cum.npz"
        np.savez(npz_p, cum_cm=cum, x=x, y=y, epsg=np.int32(32636), dates=np.array(["2026-06-26", "2026-10-12"]), quality="provisional")
        sh_p = tp / "sh.geojson"
        sh_p.write_text(json.dumps({
            "type": "FeatureCollection",
            "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [slon, slat]}, "properties": {"name": "Synth Obruk", "year_formed": 2021}}],
        }), encoding="utf-8")
        inf_p = tp / "inf.geojson"
        inf_p.write_text(json.dumps({
            "type": "FeatureCollection",
            "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [list(p1), list(p2)]}, "properties": {"name": "Synth Canal Road", "type": "trunk", "osm_id": 1}}],
        }), encoding="utf-8")
        out_p = tp / "assets.json"
        res = compute_karapinar_assets(sh_p, inf_p, npz_p, out_p)

        raw = out_p.read_text(encoding="utf-8")
        assert "NaN" not in raw and "Infinity" not in raw
        bands = {b["band"]: b for b in res["summary"]["sinkhole_ring_analysis"]["disjoint_rings"]}
        assert bands["0-1 km"]["mean_cm"] < bands["1-2 km"]["mean_cm"] < bands["2-5 km"]["mean_cm"]
        seg_dist = res["features"][0]["properties"]["nearest_sinkhole_m"]
        assert seg_dist < 1.0, f"Expected ~0 m distance when line crosses sinkhole, got {seg_dist}"
        print(
            f"PASS self-test: 0-1km={bands['0-1 km']['mean_cm']} cm < "
            f"1-2km={bands['1-2 km']['mean_cm']} cm < 2-5km={bands['2-5 km']['mean_cm']} cm | "
            f"line dist={seg_dist} m"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Karapinar sinkhole ring subsidence and OSM proximity risk.")
    parser.add_argument("--sinkholes", type=Path, default=DEFAULT_SINKHOLES)
    parser.add_argument("--infra", type=Path, default=DEFAULT_INFRA)
    parser.add_argument("--npz", type=Path, default=DEFAULT_NPZ)
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Explicit output assets.json path (overrides --data-dir).",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Target output directory where assets.json is written if --out is omitted.",
    )
    parser.add_argument(
        "--quality",
        type=str,
        default=None,
        help="Optional quality label override (e.g. 'mixed' for full-year beta+provisional runs).",
    )
    parser.add_argument("--self-test", action="store_true", help="Run synthetic unit check")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    out_path = args.out or ((args.data_dir / "assets.json") if args.data_dir else DEFAULT_OUT)
    res = compute_karapinar_assets(
        sinkholes_path=args.sinkholes,
        infra_path=args.infra,
        npz_path=args.npz,
        out_path=out_path,
        quality_override=args.quality,
    )
    s = res["summary"]
    print(f"Wrote {out_path} ({s['total_infra_segments']} segments, 0 NaNs verified)")
    print("Disjoint rings:", s["sinkhole_ring_analysis"]["disjoint_rings"])
    print("Within 1/2/5 km infra count:", s["segments_within_1km_of_sinkhole"], s["segments_within_2km_of_sinkhole"], s["segments_within_5km_of_sinkhole"])
    print("Top 5 nearest infra segments:", [(f["properties"]["name"], f["properties"]["type"], f["properties"]["nearest_sinkhole_m"], f["properties"]["gradient_mm_per_km"]) for f in res["features"][:5]])


if __name__ == "__main__":
    main()
