"""Build 3D terrain (Copernicus DEM GLO-30) and atlas/epoch metadata for demo_30s_v2.mp4."""
from __future__ import annotations

import json
import pathlib
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import from_bounds

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT_PATH = pathlib.Path(__file__).resolve().parent / "demo_v2_data.json"

COPERNICUS_BASE = "https://copernicus-dem-30m.s3.amazonaws.com"


def tile_name(lat_floor: int, lon_floor: int) -> str:
    ns = "N" if lat_floor >= 0 else "S"
    ew = "E" if lon_floor >= 0 else "W"
    return f"Copernicus_DSM_COG_10_{ns}{abs(lat_floor):02d}_00_{ew}{abs(lon_floor):03d}_00_DEM"


def fetch_dem_grid(bbox: list[float], width: int, height: int) -> dict:
    """Read Copernicus DEM GLO-30 over bbox=[w, s, e, n] via /vsicurl/ without downloading full tiles."""
    w, s, e, n = bbox
    lon_tiles = range(int(np.floor(w)), int(np.floor(e - 1e-9)) + 1)
    lat_tiles = range(int(np.floor(s)), int(np.floor(n - 1e-9)) + 1)

    grid = np.full((height, width), np.nan, dtype=np.float32)
    xs = np.linspace(w, e, width, endpoint=False) + (e - w) / (2 * width)
    ys = np.linspace(n, s, height, endpoint=False) - (n - s) / (2 * height)

    for lt in lat_tiles:
        for ln in lon_tiles:
            tw = max(w, float(ln))
            te = min(e, float(ln + 1))
            ts = max(s, float(lt))
            tn = min(n, float(lt + 1))
            if tw >= te or ts >= tn:
                continue

            col0 = int(np.searchsorted(xs, tw, side="left"))
            col1 = int(np.searchsorted(xs, te, side="right"))
            # ys is descending (north to south)
            row0 = int(np.sum(ys > tn))
            row1 = int(np.sum(ys >= ts))
            sub_h = max(1, row1 - row0)
            sub_w = max(1, col1 - col0)

            name = tile_name(lt, ln)
            url = f"/vsicurl/{COPERNICUS_BASE}/{name}/{name}.tif"
            try:
                with rasterio.open(url) as src:
                    win = from_bounds(tw, ts, te, tn, transform=src.transform)
                    arr = src.read(
                        1,
                        window=win,
                        out_shape=(sub_h, sub_w),
                        resampling=Resampling.bilinear,
                        boundless=True,
                        fill_value=np.nan,
                    )
                    grid[row0:row1, col0:col1] = arr
            except Exception as exc:
                print(f"Warning: failed reading {name}: {exc}")

    valid = np.isfinite(grid)
    min_elev = float(np.nanmin(grid)) if valid.any() else 0.0
    max_elev = float(np.nanmax(grid)) if valid.any() else 100.0
    grid_clean = np.where(valid, grid, min_elev)

    return {
        "bbox": bbox,
        "width": width,
        "height": height,
        "min_m": round(min_elev, 1),
        "max_m": round(max_elev, 1),
        "elev_m": np.round(grid_clean, 1).flatten().tolist(),
        "source": "Copernicus DEM GLO-30 (AWS Open Data, ESA/Airbus)",
    }


def collect_atlas_points() -> list[dict]:
    """Collect all available measured NISAR sites for the 3D globe scene."""
    points = []
    candidates = [
        ("central_valley", "Tulare Basin, USA", ROOT / "data/central_valley/summary.json"),
        ("karapinar", "Karapinar, Türkiye", ROOT / "data/karapinar/summary.json"),
        ("konya_plain", "Konya Plain, Türkiye", ROOT / "data/konya_plain/summary.json"),
        ("delta", "Sacramento-San Joaquin Delta, USA", ROOT / "data/delta/summary.json"),
    ]
    for gdir in sorted((ROOT / "data/global").iterdir()):
        if gdir.is_dir() and (gdir / "summary.json").exists():
            candidates.append((gdir.name, gdir.name.replace("_", " ").title(), gdir / "summary.json"))

    for sid, label, spath in candidates:
        if not spath.exists():
            continue
        s = json.loads(spath.read_text(encoding="utf-8"))
        loc = s.get("max_subsidence_location") or {}
        lon = loc.get("lon")
        lat = loc.get("lat")
        if lon is None or lat is None:
            meta_p = spath.parent / "meta.json"
            if meta_p.exists():
                b = json.loads(meta_p.read_text(encoding="utf-8")).get("bbox")
                if b:
                    lon = 0.5 * (b[0] + b[2])
                    lat = 0.5 * (b[1] + b[3])
        if lon is None or lat is None:
            continue
        vert = s.get("max_subsidence_vertical_est_cm")
        if vert is None and s.get("max_subsidence_cm") is not None:
            vert = round(float(s["max_subsidence_cm"]) / 0.776, 1)
        points.append({
            "id": sid,
            "name": label,
            "lon": round(float(lon), 4),
            "lat": round(float(lat), 4),
            "vert_cm": round(float(vert or 0.0), 1),
            "quality": s.get("quality", "provisional"),
        })
    return points


def main() -> None:
    print("Fetching Central Valley Copernicus DEM GLO-30 (180x150)...")
    cv_dem = fetch_dem_grid([-120.2, 35.6, -119.0, 36.6], 180, 150)
    print(f"  CV DEM: {cv_dem['min_m']} m .. {cv_dem['max_m']} m")

    print("Fetching Karapinar Copernicus DEM GLO-30 (160x120)...")
    kp_dem = fetch_dem_grid([33.3, 37.6, 33.8, 37.9], 160, 120)
    print(f"  KP DEM: {kp_dem['min_m']} m .. {kp_dem['max_m']} m")

    cv_fy_meta = json.loads((ROOT / "data/central_valley_fullyear/meta.json").read_text(encoding="utf-8"))
    cv_fy_pts = json.loads((ROOT / "data/central_valley_fullyear/points.json").read_text(encoding="utf-8"))
    earlimart = next((p for p in cv_fy_pts if p.get("id") == "p01"), cv_fy_pts[0])

    kp_meta = json.loads((ROOT / "data/karapinar/meta.json").read_text(encoding="utf-8"))
    kp_sinkholes = json.loads((ROOT / "data/karapinar/sinkholes.geojson").read_text(encoding="utf-8"))
    sink_coords = [
        f["geometry"]["coordinates"][:2]
        for f in kp_sinkholes.get("features", [])
        if f.get("geometry", {}).get("type") == "Point"
    ]

    atlas = collect_atlas_points()
    print(f"Collected {len(atlas)} global atlas points.")

    payload = {
        "cv_dem": cv_dem,
        "kp_dem": kp_dem,
        "cv_fullyear": {
            "dates": cv_fy_meta["dates"],
            "quality": cv_fy_meta.get("quality", "mixed"),
            "earlimart_los_cm": earlimart["disp_cm"],
            "disp_dir": "../../data/central_valley_fullyear/disp",
        },
        "karapinar": {
            "dates": kp_meta["dates"],
            "quality": kp_meta.get("quality", "provisional"),
            "disp_dir": "../../data/karapinar/disp",
            "sinkholes": sink_coords,
        },
        "atlas": atlas,
    }
    OUT_PATH.write_text(json.dumps(payload), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
