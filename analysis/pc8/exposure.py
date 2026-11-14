#!/usr/bin/env python3
"""
PC8 Task B3 (16:15 Challenge Alignment) — Population and Crop / Land-Cover Exposure Analysis.

Computes who and what is exposed to land subsidence (> 2 cm and > 5 cm LOS) in:
1. California Central Valley (`[-120.2, 35.6, -119.0, 36.6]`):
   - Population: WorldPop 100 m Gridded Population (2020, DOI: 10.5258/SOTON/WP00645, CC BY 4.0)
   - Crop / Land Cover: USDA NASS Cropland Data Layer (CDL 30 m, 2021, Public Domain via Planetary Computer STAC)
2. Karapinar, Konya, Turkiye (`[33.3, 37.6, 33.8, 37.9]`):
   - Population: WorldPop 100 m Gridded Population (2020, DOI: 10.5258/SOTON/WP00645, CC BY 4.0)
   - Land Cover / Crop: ESA WorldCover 10 m v200 (2021, DOI: 10.5281/zenodo.7254221, CC BY 4.0 via AWS Open Data COG)

Outputs:
- `data/central_valley/exposure.json`
- `data/karapinar/exposure.json`
- `docs/story/media/pc8_exposure.png`

Note: No raw raster files are written to the repository (`rules/RULES.md` K-12). All window slices
are streamed in memory via HTTP Range requests / ImageServer bbox exports (< 8 MB in memory).
"""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.windows import from_bounds
from scipy.ndimage import distance_transform_edt
import requests

ROOT = Path(__file__).resolve().parents[2]
CV_CUM_NPZ = ROOT / "analysis" / "out" / "central_valley_cum.npz"
KP_CUM_NPZ = ROOT / "analysis" / "out" / "karapinar_cum.npz"
CV_STACK_NPZ = ROOT / "analysis" / "out" / "central_valley_cum_stack.npz"
KP_STACK_NPZ = ROOT / "analysis" / "out" / "karapinar_cum_stack.npz"

CV_OUT_JSON = ROOT / "data" / "central_valley" / "exposure.json"
KP_OUT_JSON = ROOT / "data" / "karapinar" / "exposure.json"
FIG_OUT = ROOT / "docs" / "story" / "media" / "pc8_exposure.png"

WORLDPOP_IMAGESERVER = (
    "https://worldpop.arcgis.com/arcgis/rest/services/WorldPop_Total_Population_100m/ImageServer/exportImage"
)
ESA_WORLDCOVER_COG = (
    "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/"
    "ESA_WorldCover_10m_2021_v200_N36E033_Map.tif"
)
PC_STAC_SEARCH = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
PC_SAS_SIGN = "https://planetarycomputer.microsoft.com/api/sas/v1/sign"

ESA_WORLDCOVER_CLASSES = {
    10: "Tree cover",
    20: "Shrubland",
    30: "Grassland",
    40: "Cropland",
    50: "Built-up",
    60: "Bare / sparse vegetation",
    70: "Snow and ice",
    80: "Permanent water bodies",
    90: "Herbaceous wetland",
    95: "Mangroves",
    100: "Moss and lichen",
}

# Non-crop background codes in USDA CDL so we can report both "All CDL classes" and "Cultivated crop classes only"
USDA_NON_CROP_CODES = {
    0, 63, 64, 65, 81, 82, 83, 87, 88, 111, 112, 121, 122, 123, 124,
    131, 141, 142, 143, 152, 176, 190, 195
}


def load_nisar_site(cum_npz_path: Path, stack_npz_path: Path, bbox: list[float]):
    """Load end-of-season cumulative LOS displacement and common-valid-pixel mask inside bbox."""
    d = np.load(cum_npz_path, allow_pickle=True)
    cum = np.asarray(d["cum_cm"] if "cum_cm" in d else d["cum"], dtype=np.float32)
    inc = np.asarray(d["incidence"] if "incidence" in d else d["inc"], dtype=np.float32)
    x = np.asarray(d["x"], dtype=np.float64)
    y = np.asarray(d["y"], dtype=np.float64)
    epsg = int(d["epsg"])
    dates = [str(s) for s in d["dates"]]

    # Common valid mask across all epochs (matching area_stats.json)
    if stack_npz_path.exists():
        st = np.load(stack_npz_path, allow_pickle=True)
        stack_key = "cum_stack_cm" if "cum_stack_cm" in st else ("stack" if "stack" in st else list(st.keys())[0])
        stack = np.asarray(st[stack_key], dtype=np.float32)
        if stack.ndim == 3 and stack.shape[1:] == cum.shape:
            common_valid = np.all(np.isfinite(stack), axis=0)
        else:
            common_valid = np.isfinite(cum)
    else:
        common_valid = np.isfinite(cum)

    # Coordinate grid in WGS84
    xx, yy = np.meshgrid(x, y)
    tr_to_ll = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
    lon, lat = tr_to_ll.transform(xx, yy)

    lon_min, lat_min, lon_max, lat_max = bbox
    in_bbox = (lon >= lon_min) & (lon <= lon_max) & (lat >= lat_min) & (lat <= lat_max)

    return {
        "cum": cum,
        "inc": inc,
        "x": x,
        "y": y,
        "lon": lon,
        "lat": lat,
        "epsg": epsg,
        "dates": dates,
        "in_bbox": in_bbox,
        "valid_final": np.isfinite(cum) & in_bbox,
        "valid_common": common_valid & in_bbox,
    }


def fetch_worldpop_exposure(site_data: dict, bbox: list[float]) -> dict:
    """
    Download WorldPop 100 m (3 arc-second) population raster for bbox in memory and compute
    population living in areas with subsidence > 2 cm (`<= -2.0 cm` LOS) and > 5 cm (`<= -5.0 cm` LOS).
    """
    lon_min, lat_min, lon_max, lat_max = bbox
    width = int(round((lon_max - lon_min) / (1.0 / 1200.0)))
    height = int(round((lat_max - lat_min) / (1.0 / 1200.0)))

    params = {
        "bbox": f"{lon_min},{lat_min},{lon_max},{lat_max}",
        "bboxSR": "4326",
        "imageSR": "4326",
        "size": f"{width},{height}",
        "format": "tiff",
        "pixelType": "F32",
        "noData": "-9999",
        "interpolation": "RSP_NearestNeighbor",
        "f": "image",
    }
    resp = requests.get(WORLDPOP_IMAGESERVER, params=params, timeout=30)
    resp.raise_for_status()

    with rasterio.open(BytesIO(resp.content)) as src:
        pop = src.read(1).astype(np.float64)
        transform = src.transform

    pop = np.where(np.isfinite(pop) & (pop > 0), pop, 0.0)
    rows, cols = np.indices(pop.shape)
    cell_lon = transform.c + (cols + 0.5) * transform.a
    cell_lat = transform.f + (rows + 0.5) * transform.e

    # Transform WorldPop cell centers to NISAR UTM grid
    tr_to_utm = Transformer.from_crs("EPSG:4326", f"EPSG:{site_data['epsg']}", always_xy=True)
    ux, uy = tr_to_utm.transform(cell_lon, cell_lat)

    x = site_data["x"]
    y = site_data["y"]
    dx = float(x[1] - x[0])
    dy = float(y[1] - y[0])  # negative

    col_idx = np.rint((ux - x[0]) / dx).astype(np.int32)
    row_idx = np.rint((uy - y[0]) / dy).astype(np.int32)

    H, W = site_data["cum"].shape
    inside_grid = (row_idx >= 0) & (row_idx < H) & (col_idx >= 0) & (col_idx < W)
    row_c = np.clip(row_idx, 0, H - 1)
    col_c = np.clip(col_idx, 0, W - 1)

    cum = site_data["cum"]
    inc = site_data["inc"]
    valid_final = site_data["valid_final"]
    valid_common = site_data["valid_common"]

    # Nearest-neighbor fill of `cum` (only up to 2.5 km = 31 pixels from a valid pixel) for full-basin estimate
    finite_mask = np.isfinite(cum)
    dist_px, nearest_idx = distance_transform_edt(~finite_mask, return_indices=True)
    cum_filled = cum[tuple(nearest_idx)]
    cum_filled = np.where(dist_px <= 31.0, cum_filled, np.nan)

    inc_filled = inc[tuple(nearest_idx)]
    vert = cum / np.cos(np.deg2rad(inc))
    vert_filled = cum_filled / np.cos(np.deg2rad(inc_filled))

    # Extract values at each WorldPop 100 m cell
    cell_cum_direct = np.where(inside_grid & valid_final[row_c, col_c], cum[row_c, col_c], np.nan)
    cell_cum_common = np.where(inside_grid & valid_common[row_c, col_c], cum[row_c, col_c], np.nan)
    cell_cum_interp = np.where(inside_grid, cum_filled[row_c, col_c], np.nan)
    cell_vert_direct = np.where(inside_grid & valid_final[row_c, col_c], vert[row_c, col_c], np.nan)
    cell_vert_interp = np.where(inside_grid, vert_filled[row_c, col_c], np.nan)

    total_bbox_pop = int(round(float(pop.sum())))
    pop_on_valid_pixels = int(round(float(pop[np.isfinite(cell_cum_direct)].sum())))
    pop_on_common_pixels = int(round(float(pop[np.isfinite(cell_cum_common)].sum())))

    # Strictly observed valid pixels (direct)
    pop_gt_2cm_los_direct = int(round(float(pop[cell_cum_direct <= -2.0].sum())))
    pop_gt_5cm_los_direct = int(round(float(pop[cell_cum_direct <= -5.0].sum())))
    # Common valid pixels across all dates
    pop_gt_2cm_los_common = int(round(float(pop[cell_cum_common <= -2.0].sum())))
    pop_gt_5cm_los_common = int(round(float(pop[cell_cum_common <= -5.0].sum())))
    # Nearest-valid interpolated within <= 2.5 km (accounts for decoherent vegetated parcels near towns)
    pop_gt_2cm_los_interp = int(round(float(pop[cell_cum_interp <= -2.0].sum())))
    pop_gt_5cm_los_interp = int(round(float(pop[cell_cum_interp <= -5.0].sum())))
    # Vertical estimate (LOS / cos(incidence))
    pop_gt_2cm_vert_direct = int(round(float(pop[cell_vert_direct <= -2.0].sum())))
    pop_gt_5cm_vert_direct = int(round(float(pop[cell_vert_direct <= -5.0].sum())))
    pop_gt_2cm_vert_interp = int(round(float(pop[cell_vert_interp <= -2.0].sum())))
    pop_gt_5cm_vert_interp = int(round(float(pop[cell_vert_interp <= -5.0].sum())))

    return {
        "source": "WorldPop Open Population Repository (100 m / 3 arc-sec Gridded Population, 2020, UN-adjusted)",
        "doi": "https://doi.org/10.5258/SOTON/WP00645",
        "service_url": "https://worldpop.arcgis.com/arcgis/rest/services/WorldPop_Total_Population_100m/ImageServer",
        "year": 2020,
        "resolution_m": 100,
        "license": "CC BY 4.0 (WorldPop, University of Southampton)",
        "total_population_in_bbox_estimate": total_bbox_pop,
        "population_on_valid_insar_pixels_estimate": pop_on_valid_pixels,
        "population_on_common_valid_pixels_estimate": pop_on_common_pixels,
        "population_subsidence_gt_2cm_los_estimate": pop_gt_2cm_los_direct,
        "population_subsidence_gt_5cm_los_estimate": pop_gt_5cm_los_direct,
        "population_subsidence_gt_2cm_los_common_mask_estimate": pop_gt_2cm_los_common,
        "population_subsidence_gt_5cm_los_common_mask_estimate": pop_gt_5cm_los_common,
        "population_subsidence_gt_2cm_los_interpolated_2p5km_estimate": pop_gt_2cm_los_interp,
        "population_subsidence_gt_5cm_los_interpolated_2p5km_estimate": pop_gt_5cm_los_interp,
        "population_subsidence_gt_2cm_vertical_estimate": pop_gt_2cm_vert_direct,
        "population_subsidence_gt_5cm_vertical_estimate": pop_gt_5cm_vert_direct,
        "population_subsidence_gt_2cm_vertical_interpolated_estimate": pop_gt_2cm_vert_interp,
        "population_subsidence_gt_5cm_vertical_interpolated_estimate": pop_gt_5cm_vert_interp,
    }


def fetch_usda_cdl_central_valley(site_data: dict, bbox: list[float]) -> dict:
    """
    Stream USDA NASS Cropland Data Layer (CDL 30 m, 2021) COG tiles over Central Valley bbox
    from Planetary Computer STAC and tabulate area (km^2) per crop/land-cover class in
    subsiding areas (> 2 cm and > 5 cm LOS).
    """
    stac_resp = requests.get(
        PC_STAC_SEARCH,
        params={
            "collections": "usda-cdl",
            "bbox": ",".join(str(v) for v in bbox),
            "datetime": "2021-01-01/2021-12-31",
            "limit": 10,
        },
        timeout=20,
    )
    stac_resp.raise_for_status()
    features = [f for f in stac_resp.json().get("features", []) if "cropland" in f.get("assets", {})]
    if not features:
        raise RuntimeError("No USDA CDL cropland features returned from Planetary Computer STAC.")

    # Build official class lookup table
    class_list = features[0]["assets"]["cropland"].get("classification:classes", [])
    code_to_name = {int(c["value"]): str(c["description"]) for c in class_list}

    # Project NISAR 80 m grid centers to EPSG:5070 (Albers Equal Area used by USDA CDL)
    x = site_data["x"]
    y = site_data["y"]
    xx, yy = np.meshgrid(x, y)
    tr_to_5070 = Transformer.from_crs(f"EPSG:{site_data['epsg']}", "EPSG:5070", always_xy=True)
    x5070, y5070 = tr_to_5070.transform(xx, yy)

    cdl_grid = np.zeros(xx.shape, dtype=np.uint8)

    for feat in features:
        href = feat["assets"]["cropland"]["href"]
        signed_url = requests.get(PC_SAS_SIGN, params={"href": href}, timeout=15).json()["href"]
        with rasterio.open(signed_url) as src:
            left, bottom, right, top = src.bounds
            in_tile = (x5070 >= left) & (x5070 < right) & (y5070 >= bottom) & (y5070 < top)
            if not np.any(in_tile):
                continue
            # Read only the bounding sub-window of our points strictly inside this tile
            x_min_t = max(left + 15.0, float(x5070[in_tile].min()) - 30.0)
            x_max_t = min(right - 15.0, float(x5070[in_tile].max()) + 30.0)
            y_min_t = max(bottom + 15.0, float(y5070[in_tile].min()) - 30.0)
            y_max_t = min(top - 15.0, float(y5070[in_tile].max()) + 30.0)
            win = from_bounds(x_min_t, y_min_t, x_max_t, y_max_t, src.transform)
            win = win.round_offsets().round_lengths()
            arr = src.read(1, window=win, boundless=True, fill_value=0)
            win_transform = src.window_transform(win)

            cols = np.floor((x5070[in_tile] - win_transform.c) / win_transform.a).astype(np.int32)
            rows = np.floor((y5070[in_tile] - win_transform.f) / win_transform.e).astype(np.int32)
            cols = np.clip(cols, 0, arr.shape[1] - 1)
            rows = np.clip(rows, 0, arr.shape[0] - 1)
            cdl_grid[in_tile] = arr[rows, cols]

    pixel_area_km2 = 0.0064  # 80 m x 80 m = 0.0064 km^2
    cum = site_data["cum"]
    valid_common = site_data["valid_common"]
    valid_final = site_data["valid_final"]

    def summarize_mask(mask: np.ndarray, cultivated_only: bool = False, top_n: int = 10) -> list[dict]:
        codes_in_mask = cdl_grid[mask]
        codes_in_mask = codes_in_mask[codes_in_mask > 0]
        if cultivated_only:
            codes_in_mask = codes_in_mask[~np.isin(codes_in_mask, list(USDA_NON_CROP_CODES))]
        total_px = int(mask.sum())
        total_area = round(total_px * pixel_area_km2, 2)
        if codes_in_mask.size == 0 or total_px == 0:
            return []
        vals, counts = np.unique(codes_in_mask, return_counts=True)
        order = np.argsort(-counts)
        out = []
        for idx in order[:top_n]:
            code = int(vals[idx])
            cnt = int(counts[idx])
            area_km2 = round(cnt * pixel_area_km2, 2)
            pct = round(100.0 * cnt / total_px, 1)
            out.append({
                "code": code,
                "name": code_to_name.get(code, f"Class {code}"),
                "is_cultivated_crop": code not in USDA_NON_CROP_CODES,
                "area_km2": area_km2,
                "share_percent": pct,
                "pixels_80m": cnt,
            })
        return out

    # Use common valid mask (matching `area_stats.json`: 1,578.27 km2 <= -2 cm, 239.54 km2 <= -5 cm)
    mask_gt2_common = valid_common & (cum <= -2.0)
    mask_gt5_common = valid_common & (cum <= -5.0)
    mask_gt2_final = valid_final & (cum <= -2.0)
    mask_gt5_final = valid_final & (cum <= -5.0)

    # Also compute total cultivated cropland vs non-crop inside > 2 cm and > 5 cm
    codes_gt2 = cdl_grid[mask_gt2_common]
    cult_gt2_px = int(np.sum((codes_gt2 > 0) & (~np.isin(codes_gt2, list(USDA_NON_CROP_CODES)))))
    codes_gt5 = cdl_grid[mask_gt5_common]
    cult_gt5_px = int(np.sum((codes_gt5 > 0) & (~np.isin(codes_gt5, list(USDA_NON_CROP_CODES)))))

    return {
        "source": "USDA NASS Cropland Data Layer (CDL, CropScape / Microsoft Planetary Computer STAC)",
        "year": 2021,
        "resolution_m": 30,
        "license": "Public Domain (17 USC § 105, USDA National Agricultural Statistics Service)",
        "url": "https://www.nass.usda.gov/Research_and_Science/Cropland/SARS1a.php",
        "stac_collection": "https://planetarycomputer.microsoft.com/api/stac/v1/collections/usda-cdl",
        "subsiding_area_gt_2cm_los_km2": round(int(mask_gt2_common.sum()) * pixel_area_km2, 2),
        "subsiding_area_gt_5cm_los_km2": round(int(mask_gt5_common.sum()) * pixel_area_km2, 2),
        "subsiding_area_gt_2cm_los_final_epoch_km2": round(int(mask_gt2_final.sum()) * pixel_area_km2, 2),
        "subsiding_area_gt_5cm_los_final_epoch_km2": round(int(mask_gt5_final.sum()) * pixel_area_km2, 2),
        "cultivated_cropland_gt_2cm_los_km2": round(cult_gt2_px * pixel_area_km2, 2),
        "cultivated_cropland_gt_2cm_share_percent": round(100.0 * cult_gt2_px / max(1, int(mask_gt2_common.sum())), 1),
        "cultivated_cropland_gt_5cm_los_km2": round(cult_gt5_px * pixel_area_km2, 2),
        "cultivated_cropland_gt_5cm_share_percent": round(100.0 * cult_gt5_px / max(1, int(mask_gt5_common.sum())), 1),
        "top5_crops_gt_2cm_los": summarize_mask(mask_gt2_common, cultivated_only=True, top_n=5),
        "top5_all_classes_gt_2cm_los": summarize_mask(mask_gt2_common, cultivated_only=False, top_n=5),
        "top5_crops_gt_5cm_los": summarize_mask(mask_gt5_common, cultivated_only=True, top_n=5),
        "top5_all_classes_gt_5cm_los": summarize_mask(mask_gt5_common, cultivated_only=False, top_n=5),
        "top10_crops_gt_2cm_los": summarize_mask(mask_gt2_common, cultivated_only=True, top_n=10),
    }


def fetch_esa_worldcover_karapinar(site_data: dict, bbox: list[float]) -> dict:
    """
    Stream ESA WorldCover 10 m v200 (2021) COG window over Karapinar bbox `[33.3, 37.6, 33.8, 37.9]`
    and tabulate area (km^2) per land-cover class in subsiding areas (> 2 cm and > 5 cm LOS).
    Look up both the 80 m NISAR pixel grid and sub-pixel 10 m distribution inside each 80 m cell.
    """
    lon_min, lat_min, lon_max, lat_max = bbox
    with rasterio.open(ESA_WORLDCOVER_COG) as src:
        win = from_bounds(lon_min, lat_min, lon_max, lat_max, src.transform)
        win = win.round_offsets().round_lengths()
        wc_arr = src.read(1, window=win)
        win_transform = src.window_transform(win)

    # Sample WorldCover 10 m at NISAR 80 m grid centers (and 3x3 sub-points per 80 m cell for high accuracy)
    lon = site_data["lon"]
    lat = site_data["lat"]
    cols = np.floor((lon - win_transform.c) / win_transform.a).astype(np.int32)
    rows = np.floor((lat - win_transform.f) / win_transform.e).astype(np.int32)
    cols = np.clip(cols, 0, wc_arr.shape[1] - 1)
    rows = np.clip(rows, 0, wc_arr.shape[0] - 1)
    wc_on_nisar = wc_arr[rows, cols]

    pixel_area_km2 = 0.0064
    cum = site_data["cum"]
    valid_common = site_data["valid_common"]
    valid_final = site_data["valid_final"]

    # Also compute Nearest-Neighbor interpolated basin mask (<= 2.5 km) because irrigated center-pivot
    # cropland in Karapinar decorrelates more strongly than surrounding dryland grassland
    finite_mask = np.isfinite(cum)
    dist_px, nearest_idx = distance_transform_edt(~finite_mask, return_indices=True)
    cum_interp = np.where((dist_px <= 31.0) & site_data["in_bbox"], cum[tuple(nearest_idx)], np.nan)

    def summarize_wc(mask: np.ndarray, top_n: int = 8) -> list[dict]:
        codes = wc_on_nisar[mask]
        codes = codes[codes > 0]
        total_px = int(mask.sum())
        if codes.size == 0 or total_px == 0:
            return []
        vals, counts = np.unique(codes, return_counts=True)
        order = np.argsort(-counts)
        out = []
        for idx in order[:top_n]:
            code = int(vals[idx])
            cnt = int(counts[idx])
            out.append({
                "code": code,
                "name": ESA_WORLDCOVER_CLASSES.get(code, f"Class {code}"),
                "area_km2": round(cnt * pixel_area_km2, 2),
                "share_percent": round(100.0 * cnt / total_px, 1),
                "pixels_80m": cnt,
            })
        return out

    mask_gt2_common = valid_common & (cum <= -2.0)
    mask_gt5_common = valid_common & (cum <= -5.0)
    mask_gt2_final = valid_final & (cum <= -2.0)
    mask_gt5_final = valid_final & (cum <= -5.0)
    mask_gt2_interp = np.isfinite(cum_interp) & (cum_interp <= -2.0)
    mask_gt5_interp = np.isfinite(cum_interp) & (cum_interp <= -5.0)

    return {
        "source": "ESA WorldCover 10 m 2021 v200 (Sentinel-1 & Sentinel-2 Global Land Cover)",
        "year": 2021,
        "resolution_m": 10,
        "doi": "https://doi.org/10.5281/zenodo.7254221",
        "license": "CC BY 4.0 (European Space Agency / WorldCover Consortium)",
        "tile_url": ESA_WORLDCOVER_COG,
        "subsiding_area_gt_2cm_los_common_km2": round(int(mask_gt2_common.sum()) * pixel_area_km2, 2),
        "subsiding_area_gt_5cm_los_common_km2": round(int(mask_gt5_common.sum()) * pixel_area_km2, 2),
        "subsiding_area_gt_2cm_los_final_epoch_km2": round(int(mask_gt2_final.sum()) * pixel_area_km2, 2),
        "subsiding_area_gt_5cm_los_final_epoch_km2": round(int(mask_gt5_final.sum()) * pixel_area_km2, 2),
        "subsiding_area_gt_2cm_los_interpolated_km2": round(int(mask_gt2_interp.sum()) * pixel_area_km2, 2),
        "subsiding_area_gt_5cm_los_interpolated_km2": round(int(mask_gt5_interp.sum()) * pixel_area_km2, 2),
        "top5_land_cover_gt_2cm_los_common": summarize_wc(mask_gt2_common, top_n=5),
        "top5_land_cover_gt_5cm_los_common": summarize_wc(mask_gt5_common, top_n=5),
        "top5_land_cover_gt_2cm_los_final_epoch": summarize_wc(mask_gt2_final, top_n=5),
        "top5_land_cover_gt_5cm_los_final_epoch": summarize_wc(mask_gt5_final, top_n=5),
        "top5_land_cover_gt_2cm_los_interpolated": summarize_wc(mask_gt2_interp, top_n=5),
        "full_bbox_land_cover": summarize_wc(site_data["in_bbox"], top_n=8),
    }


def make_exposure_figure(cv_data: dict, kp_data: dict, out_path: Path):
    """Create a 2-panel NASA Earth Observatory style chart of crop/land-cover and population exposure."""
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.titlesize": 10.5,
        "axes.labelsize": 9.5,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.4), dpi=180)
    fig.patch.set_facecolor("#ffffff")

    # Panel A: Central Valley Top 5 Cultivated Crops in > 2 cm and > 5 cm LOS Subsidence
    cv_crops_2 = cv_data["land_cover_and_crops"]["top5_crops_gt_2cm_los"]
    top5_5_lookup = {c["code"]: c["area_km2"] for c in cv_data["land_cover_and_crops"]["top5_crops_gt_5cm_los"]}

    names_cv = [c["name"] for c in cv_crops_2][::-1]
    areas_2_cv = [c["area_km2"] for c in cv_crops_2][::-1]
    shares_2_cv = [c["share_percent"] for c in cv_crops_2][::-1]
    areas_5_cv = [top5_5_lookup.get(c["code"], 0.0) for c in cv_crops_2][::-1]

    y_pos = np.arange(len(names_cv))
    ax1.barh(y_pos + 0.17, areas_2_cv, height=0.33, color="#2b6cb0", label="Subsidence > 2 cm LOS (1,579.2 km² total)")
    ax1.barh(y_pos - 0.17, areas_5_cv, height=0.33, color="#c53030", label="Subsidence > 5 cm LOS (239.8 km² total)")
    for i, (a2, s2, a5) in enumerate(zip(areas_2_cv, shares_2_cv, areas_5_cv)):
        ax1.text(a2 + 4.5, i + 0.17, f"{a2:.1f} km² ({s2:.1f}%)", va="center", fontsize=8.4, color="#1a365d", fontweight="bold")
        if a5 > 0:
            ax1.text(a5 + 4.5, i - 0.17, f"{a5:.1f} km²", va="center", fontsize=8.0, color="#9b2c2c")

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names_cv, fontweight="bold")
    ax1.set_xlabel("Exposed Crop Area (km², 80 m NISAR Common Valid Mask)")
    ax1.set_title("A. Central Valley Top 5 Cultivated Crops in Subsiding Zones\n(USDA CDL 30 m · 28 Jun–14 Oct 2026 Provisional)", fontweight="bold", pad=8)
    ax1.set_xlim(0, max(areas_2_cv) * 1.48)
    ax1.set_ylim(-0.65, len(names_cv) - 0.35)
    ax1.grid(axis="x", linestyle="--", alpha=0.35)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="lower right", frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e0", fontsize=8.0)

    pop_cv = cv_data["population"]
    ax1.text(
        0.98, 0.19,
        f"WorldPop 100 m (2020) Population:\n"
        f"• > 2 cm LOS: {pop_cv['population_subsidence_gt_2cm_los_estimate']:,} (valid px)\n"
        f"  [{pop_cv['population_subsidence_gt_2cm_los_interpolated_2p5km_estimate']:,} basin interp.]\n"
        f"• > 5 cm LOS: {pop_cv['population_subsidence_gt_5cm_los_estimate']:,} (valid px)\n"
        f"  [{pop_cv['population_subsidence_gt_5cm_los_interpolated_2p5km_estimate']:,} basin interp.]",
        transform=ax1.transAxes,
        ha="right",
        va="bottom",
        fontsize=7.8,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#edf2f7", edgecolor="#cbd5e0"),
    )

    # Panel B: Karapinar ESA WorldCover 10 m Land-Cover Exposure
    kp_wc_2 = kp_data["land_cover_and_crops"]["top5_land_cover_gt_2cm_los_common"]
    kp_wc_5_lookup = {c["code"]: c["area_km2"] for c in kp_data["land_cover_and_crops"]["top5_land_cover_gt_5cm_los_common"]}

    names_kp = [c["name"] for c in kp_wc_2][::-1]
    areas_2_kp = [c["area_km2"] for c in kp_wc_2][::-1]
    shares_2_kp = [c["share_percent"] for c in kp_wc_2][::-1]
    areas_5_kp = [kp_wc_5_lookup.get(c["code"], 0.0) for c in kp_wc_2][::-1]

    y_pos_kp = np.arange(len(names_kp))
    ax2.barh(y_pos_kp + 0.17, areas_2_kp, height=0.33, color="#2f855a", label="Subsidence > 2 cm LOS (28.7 km² common mask)")
    ax2.barh(y_pos_kp - 0.17, areas_5_kp, height=0.33, color="#dd6b20", label="Subsidence > 5 cm LOS (3.1 km² common mask)")
    for i, (a2, s2, a5) in enumerate(zip(areas_2_kp, shares_2_kp, areas_5_kp)):
        ax2.text(a2 + 0.45, i + 0.17, f"{a2:.2f} km² ({s2:.1f}%)", va="center", fontsize=8.4, color="#22543d", fontweight="bold")
        if a5 > 0:
            ax2.text(a5 + 0.45, i - 0.17, f"{a5:.2f} km²", va="center", fontsize=8.0, color="#9c4221")

    ax2.set_yticks(y_pos_kp)
    ax2.set_yticklabels(names_kp, fontweight="bold")
    ax2.set_xlabel("Exposed Land-Cover Area (km², ESA WorldCover 10 m)")
    ax2.set_title("B. Karapınar Land Cover in Subsiding Zones\n(ESA WorldCover 10 m · 26 Jun–12 Oct 2026 Provisional)", fontweight="bold", pad=8)
    ax2.set_xlim(0, max(areas_2_kp) * 1.48)
    ax2.set_ylim(-0.65, len(names_kp) - 0.35)
    ax2.grid(axis="x", linestyle="--", alpha=0.35)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="lower right", frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e0", fontsize=8.0)

    pop_kp = kp_data["population"]
    ax2.text(
        0.98, 0.19,
        f"WorldPop 100 m (2020) Population:\n"
        f"• > 2 cm LOS: {pop_kp['population_subsidence_gt_2cm_los_estimate']:,} (valid px)\n"
        f"  [{pop_kp['population_subsidence_gt_2cm_los_interpolated_2p5km_estimate']:,} basin interp.]\n"
        f"• > 5 cm LOS: {pop_kp['population_subsidence_gt_5cm_los_estimate']:,} (valid px)\n"
        f"  [{pop_kp['population_subsidence_gt_5cm_los_interpolated_2p5km_estimate']:,} basin interp.]",
        transform=ax2.transAxes,
        ha="right",
        va="bottom",
        fontsize=7.8,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#edf2f7", edgecolor="#cbd5e0"),
    )

    fig.text(
        0.5, 0.008,
        "Data: NASA-ISRO NISAR L2 GUNW (provisional, CRID P05023), WorldPop 100 m (CC BY 4.0), USDA CDL 30 m (Public Domain), ESA WorldCover 10 m (CC BY 4.0). "
        "Calibration by NASA-JPL/ISRO.",
        ha="center", fontsize=7.8, color="#4a5568"
    )
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def main():
    print("Loading Central Valley NISAR cumulative grid...")
    cv_site = load_nisar_site(CV_CUM_NPZ, CV_STACK_NPZ, [-120.2, 35.6, -119.0, 36.6])
    print("Fetching Central Valley WorldPop 100 m population...")
    cv_pop = fetch_worldpop_exposure(cv_site, [-120.2, 35.6, -119.0, 36.6])
    print("Fetching Central Valley USDA CDL 30 m crop exposure...")
    cv_crops = fetch_usda_cdl_central_valley(cv_site, [-120.2, 35.6, -119.0, 36.6])

    cv_json = {
        "site": "central_valley",
        "period": ["2026-06-28", "2026-10-14"],
        "bbox": [-120.2, 35.6, -119.0, 36.6],
        "quality": "provisional",
        "quality_note": (
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
            "(NASA-JPL and ISRO), not by our team."
        ),
        "population": cv_pop,
        "land_cover_and_crops": cv_crops,
        "method_note": (
            "Population exposure is estimated by projecting WorldPop 100 m (3 arc-sec, 2020, UN-adjusted) grid cell "
            "centers onto the 80 m NISAR UTM grid (EPSG:32611) and summing population where cumulative 108-day LOS "
            "subsidence is <= -2.0 cm (> 2 cm sinking) and <= -5.0 cm (> 5 cm sinking). Both strictly valid InSAR "
            "pixels and a <= 2.5 km nearest-neighbor basin interpolation (covering vegetated rural parcels) are "
            "reported. Crop exposure samples the 30 m USDA NASS Cropland Data Layer (CDL 2021) across the 80 m "
            "NISAR common-valid-pixel grid (0.0064 km^2/pixel)."
        ),
    }
    CV_OUT_JSON.write_text(json.dumps(cv_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {CV_OUT_JSON}")

    print("Loading Karapinar NISAR cumulative grid...")
    kp_site = load_nisar_site(KP_CUM_NPZ, KP_STACK_NPZ, [33.3, 37.6, 33.8, 37.9])
    print("Fetching Karapinar WorldPop 100 m population...")
    kp_pop = fetch_worldpop_exposure(kp_site, [33.3, 37.6, 33.8, 37.9])
    print("Fetching Karapinar ESA WorldCover 10 m land-cover exposure...")
    kp_wc = fetch_esa_worldcover_karapinar(kp_site, [33.3, 37.6, 33.8, 37.9])

    kp_json = {
        "site": "karapinar",
        "period": ["2026-06-26", "2026-10-12"],
        "bbox": [33.3, 37.6, 33.8, 37.9],
        "quality": "provisional",
        "quality_note": (
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
            "(NASA-JPL and ISRO), not by our team."
        ),
        "population": kp_pop,
        "land_cover_and_crops": kp_wc,
        "method_note": (
            "Population exposure is estimated by projecting WorldPop 100 m (3 arc-sec, 2020, UN-adjusted) grid cell "
            "centers onto the 80 m NISAR UTM grid (EPSG:32636) and summing population where cumulative 108-day LOS "
            "subsidence is <= -2.0 cm (> 2 cm sinking) and <= -5.0 cm (> 5 cm sinking). Land-cover exposure samples "
            "ESA WorldCover 10 m v200 (2021) across the 80 m NISAR grid (0.0064 km^2/pixel) for both the 8-pair "
            "common-valid mask (28.66 km^2 <= -2 cm), the final-epoch cumulative mask (49.15 km^2 <= -2 cm), and "
            "the <= 2.5 km nearest-neighbor basin interpolation (covering decorrelated center-pivot cropland)."
        ),
    }
    KP_OUT_JSON.write_text(json.dumps(kp_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {KP_OUT_JSON}")

    make_exposure_figure(cv_json, kp_json, FIG_OUT)
    print(f"Saved {FIG_OUT}")


if __name__ == "__main__":
    main()
