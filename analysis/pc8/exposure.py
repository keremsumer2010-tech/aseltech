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
import sys
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from analysis import insar, cumulative

CV_CUM_NPZ = ROOT / "analysis" / "out" / "central_valley_cum.npz"
KP_CUM_NPZ = ROOT / "analysis" / "out" / "karapinar_cum.npz"
CV_STACK_NPZ = ROOT / "analysis" / "out" / "central_valley_cum_stack.npz"
KP_STACK_NPZ = ROOT / "analysis" / "out" / "karapinar_cum_stack.npz"
KONYA_SUBSET_DIR = ROOT / "pipeline" / "subset" / "konya_plain"

CV_OUT_JSON = ROOT / "data" / "central_valley" / "exposure.json"
KP_OUT_JSON = ROOT / "data" / "karapinar" / "exposure.json"
KONYA_OUT_JSON = ROOT / "data" / "konya_plain" / "exposure.json"
FIG_OUT = ROOT / "docs" / "story" / "media" / "pc8_exposure.png"

WORLDPOP_IMAGESERVER = (
    "https://worldpop.arcgis.com/arcgis/rest/services/WorldPop_Total_Population_100m/ImageServer/exportImage"
)
ESA_WORLDCOVER_COG_TILES = [
    "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N36E030_Map.tif",
    "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N36E033_Map.tif",
]
ESA_WORLDCOVER_COG = ESA_WORLDCOVER_COG_TILES[1]
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


def load_konya_plain_from_subsets(subset_dir: Path, bbox: list[float]) -> dict:
    """
    Build cumulative LOS displacement grid for Konya Plain (`[32.4, 37.4, 33.9, 38.1]`)
    from `pipeline/subset/konya_plain/*.npz` using the reference window in `data/konya_plain/meta.json`.
    """
    meta = json.loads((ROOT / "data" / "konya_plain" / "meta.json").read_text(encoding="utf-8"))
    ref_lon = float(meta["reference_point"]["lon"])
    ref_lat = float(meta["reference_point"]["lat"])

    npz_files = sorted(subset_dir.glob("*.npz"))
    if not npz_files:
        raise FileNotFoundError(f"No NPZ files found in {subset_dir}")

    d0 = np.load(npz_files[0], allow_pickle=True)
    x = np.asarray(d0["x"], dtype=np.float64)
    y = np.asarray(d0["y"], dtype=np.float64)
    epsg = int(d0["epsg"])
    inc = np.asarray(d0["incidence"], dtype=np.float32)

    tr_to_utm = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    rx, ry = tr_to_utm.transform(ref_lon, ref_lat)
    ref_c = int(np.argmin(np.abs(x - rx)))
    ref_r = int(np.argmin(np.abs(y - ry)))

    stack = []
    dates = []
    cum = np.zeros(inc.shape, dtype=np.float32)
    common_valid = np.ones(inc.shape, dtype=bool)

    for idx, f in enumerate(npz_files):
        d = np.load(f, allow_pickle=True)
        if idx == 0:
            dates.append(str(d["date1"]))
            stack.append(np.zeros(inc.shape, dtype=np.float32))
        dates.append(str(d["date2"]))

        unw = np.asarray(d["unw"], dtype=np.float32)
        coh = np.asarray(d["coh"], dtype=np.float32)
        cc = np.asarray(d["conncomp"], dtype=np.float32)
        ion = np.asarray(d["ion"], dtype=np.float32)
        wl = float(d["wavelength"])

        cm = insar.phase_to_cm(unw, wl)
        if np.isfinite(ion).any():
            ion_cm = insar.phase_to_cm(ion, wl)
            cm = np.where(np.isfinite(ion_cm), cm - ion_cm, cm)
        cm = insar.mask_coherence(cm, coh, thr=0.30)
        cm = np.where(cc != 0, cm, np.nan)
        cm = cumulative.deramp(cm)
        cm = insar.reference(cm, (ref_r, ref_c), radius=3)
        cm = np.where(np.abs(cm) <= 15.0, cm, np.nan)

        common_valid &= np.isfinite(cm)
        cum = np.where(common_valid, cum + cm, np.nan)
        stack.append(cum.copy())

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


def fetch_esa_worldcover_site(site_data: dict, bbox: list[float], tile_urls: list[str]) -> dict:
    """
    Stream ESA WorldCover 10 m v200 (2021) COG windows across one or more 3x3-deg tiles
    covering `bbox` and tabulate area (km^2) per land-cover class in subsiding areas.
    """
    lon_min, lat_min, lon_max, lat_max = bbox
    lon = site_data["lon"]
    lat = site_data["lat"]
    wc_on_nisar = np.zeros(lon.shape, dtype=np.uint8)

    for url in tile_urls:
        with rasterio.open(url) as src:
            left, bottom, right, top = src.bounds
            in_tile = (lon >= left) & (lon < right) & (lat >= bottom) & (lat < top)
            if not np.any(in_tile):
                continue
            l_b = max(left + 1e-4, float(lon[in_tile].min()) - 0.002)
            r_b = min(right - 1e-4, float(lon[in_tile].max()) + 0.002)
            b_b = max(bottom + 1e-4, float(lat[in_tile].min()) - 0.002)
            t_b = min(top - 1e-4, float(lat[in_tile].max()) + 0.002)
            win = from_bounds(l_b, b_b, r_b, t_b, src.transform)
            win = win.round_offsets().round_lengths()
            wc_arr = src.read(1, window=win)
            wt = src.window_transform(win)

            cols = np.floor((lon[in_tile] - wt.c) / wt.a).astype(np.int32)
            rows = np.floor((lat[in_tile] - wt.f) / wt.e).astype(np.int32)
            cols = np.clip(cols, 0, wc_arr.shape[1] - 1)
            rows = np.clip(rows, 0, wc_arr.shape[0] - 1)
            wc_on_nisar[in_tile] = wc_arr[rows, cols]

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
        "tile_urls": tile_urls,
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


def make_exposure_figure(cv_data: dict, kp_data: dict, konya_data: dict, out_path: Path):
    """Create a 3-panel NASA Earth Observatory style chart of crop/land-cover and population exposure."""
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.0,
        "axes.titlesize": 10.0,
        "axes.labelsize": 9.0,
    })

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16.5, 5.4), dpi=180)
    fig.patch.set_facecolor("#ffffff")

    # Panel A: Central Valley Top 5 Cultivated Crops in > 2 cm and > 5 cm LOS Subsidence
    cv_crops_2 = cv_data["land_cover_and_crops"]["top5_crops_gt_2cm_los"]
    top5_5_lookup = {c["code"]: c["area_km2"] for c in cv_data["land_cover_and_crops"]["top5_crops_gt_5cm_los"]}

    names_cv = [c["name"] for c in cv_crops_2][::-1]
    areas_2_cv = [c["area_km2"] for c in cv_crops_2][::-1]
    shares_2_cv = [c["share_percent"] for c in cv_crops_2][::-1]
    areas_5_cv = [top5_5_lookup.get(c["code"], 0.0) for c in cv_crops_2][::-1]

    y_pos = np.arange(len(names_cv))
    ax1.barh(y_pos + 0.17, areas_2_cv, height=0.33, color="#2b6cb0", label="> 2 cm LOS (1,579.2 km²)")
    ax1.barh(y_pos - 0.17, areas_5_cv, height=0.33, color="#c53030", label="> 5 cm LOS (239.8 km²)")
    for i, (a2, s2, a5) in enumerate(zip(areas_2_cv, shares_2_cv, areas_5_cv)):
        ax1.text(a2 + 4.5, i + 0.17, f"{a2:.1f} km² ({s2:.1f}%)", va="center", fontsize=7.9, color="#1a365d", fontweight="bold")
        if a5 > 0:
            ax1.text(a5 + 4.5, i - 0.17, f"{a5:.1f} km²", va="center", fontsize=7.6, color="#9b2c2c")

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names_cv, fontweight="bold")
    ax1.set_xlabel("Exposed Crop Area (km², 80 m NISAR)")
    ax1.set_title("A. Central Valley Top 5 Crops\n(USDA CDL 30 m · 28 Jun–14 Oct 2026)", fontweight="bold", pad=8)
    ax1.set_xlim(0, max(areas_2_cv) * 1.54)
    ax1.set_ylim(-0.65, len(names_cv) - 0.35)
    ax1.grid(axis="x", linestyle="--", alpha=0.35)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="lower right", frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e0", fontsize=7.6)

    pop_cv = cv_data["population"]
    ax1.text(
        0.98, 0.21,
        f"WorldPop 100 m (2020):\n"
        f"• > 2 cm: {pop_cv['population_subsidence_gt_2cm_los_estimate']:,} (valid)\n"
        f"  [{pop_cv['population_subsidence_gt_2cm_los_interpolated_2p5km_estimate']:,} interp.]\n"
        f"• > 5 cm: {pop_cv['population_subsidence_gt_5cm_los_estimate']:,} (valid)\n"
        f"  [{pop_cv['population_subsidence_gt_5cm_los_interpolated_2p5km_estimate']:,} interp.]",
        transform=ax1.transAxes, ha="right", va="bottom", fontsize=7.4,
        bbox=dict(boxstyle="round,pad=0.38", facecolor="#edf2f7", edgecolor="#cbd5e0"),
    )

    def plot_wc_panel(ax, site_data_json: dict, title: str, color2: str, color5: str):
        lc = site_data_json["land_cover_and_crops"]
        wc2 = lc["top5_land_cover_gt_2cm_los_common"]
        wc5_map = {c["code"]: c["area_km2"] for c in lc["top5_land_cover_gt_5cm_los_common"]}
        names = [c["name"] for c in wc2][::-1]
        a2_list = [c["area_km2"] for c in wc2][::-1]
        s2_list = [c["share_percent"] for c in wc2][::-1]
        a5_list = [wc5_map.get(c["code"], 0.0) for c in wc2][::-1]

        yp = np.arange(len(names))
        tot2 = lc["subsiding_area_gt_2cm_los_common_km2"]
        tot5 = lc["subsiding_area_gt_5cm_los_common_km2"]
        ax.barh(yp + 0.17, a2_list, height=0.33, color=color2, label=f"> 2 cm LOS ({tot2:.1f} km²)")
        ax.barh(yp - 0.17, a5_list, height=0.33, color=color5, label=f"> 5 cm LOS ({tot5:.1f} km²)")
        pad_x = max(a2_list) * 0.025
        for i, (a2, s2, a5) in enumerate(zip(a2_list, s2_list, a5_list)):
            ax.text(a2 + pad_x, i + 0.17, f"{a2:.2f} km² ({s2:.1f}%)", va="center", fontsize=7.9, color="#1a202c", fontweight="bold")
            if a5 > 0:
                ax.text(a5 + pad_x, i - 0.17, f"{a5:.2f} km²", va="center", fontsize=7.6, color="#9c4221")

        ax.set_yticks(yp)
        ax.set_yticklabels(names, fontweight="bold")
        ax.set_xlabel("Exposed Land Cover (km², ESA WorldCover 10 m)")
        ax.set_title(title, fontweight="bold", pad=8)
        ax.set_xlim(0, max(a2_list) * 1.56)
        ax.set_ylim(-0.65, len(names) - 0.35)
        ax.grid(axis="x", linestyle="--", alpha=0.35)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(loc="lower right", frameon=True, facecolor="#f8fafc", edgecolor="#cbd5e0", fontsize=7.6)

        pop = site_data_json["population"]
        ax.text(
            0.98, 0.21,
            f"WorldPop 100 m (2020):\n"
            f"• > 2 cm: {pop['population_subsidence_gt_2cm_los_estimate']:,} (valid)\n"
            f"  [{pop['population_subsidence_gt_2cm_los_interpolated_2p5km_estimate']:,} interp.]\n"
            f"• > 5 cm: {pop['population_subsidence_gt_5cm_los_estimate']:,} (valid)\n"
            f"  [{pop['population_subsidence_gt_5cm_los_interpolated_2p5km_estimate']:,} interp.]",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.4,
            bbox=dict(boxstyle="round,pad=0.38", facecolor="#edf2f7", edgecolor="#cbd5e0"),
        )

    plot_wc_panel(
        ax2, kp_data,
        "B. Karapınar Land Cover\n(ESA WorldCover 10 m · 26 Jun–12 Oct 2026)",
        "#2f855a", "#dd6b20",
    )
    plot_wc_panel(
        ax3, konya_data,
        "C. Konya Closed Basin Land Cover\n(ESA WorldCover 10 m · 26 Jun–12 Oct 2026)",
        "#2c7a7b", "#b83280",
    )

    fig.text(
        0.5, 0.008,
        "Data: NASA-ISRO NISAR L2 GUNW (provisional, CRID P05023), WorldPop 100 m (CC BY 4.0), USDA CDL 30 m (Public Domain), ESA WorldCover 10 m (CC BY 4.0). "
        "Calibration by NASA-JPL/ISRO.",
        ha="center", fontsize=8.0, color="#4a5568"
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
    kp_wc = fetch_esa_worldcover_site(kp_site, [33.3, 37.6, 33.8, 37.9], [ESA_WORLDCOVER_COG_TILES[1]])

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
            "ESA WorldCover 10 m v200 (2021) across the 80 m NISAR grid (0.0064 km^2/pixel)."
        ),
    }
    KP_OUT_JSON.write_text(json.dumps(kp_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {KP_OUT_JSON}")

    print("Building Konya Plain cumulative grid from NPZ subsets...")
    konya_bbox = [32.4, 37.4, 33.9, 38.1]
    konya_site = load_konya_plain_from_subsets(KONYA_SUBSET_DIR, konya_bbox)
    print("Fetching Konya Plain WorldPop 100 m population...")
    konya_pop = fetch_worldpop_exposure(konya_site, konya_bbox)
    print("Fetching Konya Plain ESA WorldCover 10 m land-cover exposure (N36E030 + N36E033)...")
    konya_wc = fetch_esa_worldcover_site(konya_site, konya_bbox, ESA_WORLDCOVER_COG_TILES)

    konya_json = {
        "site": "konya_plain",
        "period": ["2026-06-26", "2026-10-12"],
        "bbox": konya_bbox,
        "quality": "provisional",
        "quality_note": (
            "NISAR data are provisional. Calibration and validation are carried out by the NISAR project "
            "(NASA-JPL and ISRO), not by our team."
        ),
        "population": konya_pop,
        "land_cover_and_crops": konya_wc,
        "method_note": (
            "Population exposure is estimated by projecting WorldPop 100 m (3 arc-sec, 2020, UN-adjusted) grid cell "
            "centers onto the 80 m NISAR UTM grid (EPSG:32636) built from the 8 consecutive Track 7 GUNW pairs "
            "referenced to 32.91943E, 37.93711N. Land-cover exposure samples ESA WorldCover 10 m v200 (2021) "
            "tiles N36E030 and N36E033 across the 80 m NISAR grid (0.0064 km^2/pixel)."
        ),
    }
    KONYA_OUT_JSON.write_text(json.dumps(konya_json, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {KONYA_OUT_JSON}")

    make_exposure_figure(cv_json, kp_json, konya_json, FIG_OUT)
    print(f"Saved {FIG_OUT}")


if __name__ == "__main__":
    main()
