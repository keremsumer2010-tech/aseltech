"""Copernicus DEM GLO-90 heights sampled onto a GUNW UTM grid (nearest neighbour).

DEM: Copernicus DEM GLO-90, open data on AWS (no login):
https://copernicus-dem-90m.s3.amazonaws.com/  (c) DLR e.V. 2010-2014 and (c) Airbus Defence and Space GmbH
2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved.
Tiles live in raw/dem/ (git-ignored). Used only for the elevation-correlated troposphere regression.
"""
from pathlib import Path

import numpy as np
import rasterio
from pyproj import Transformer

ROOT = Path(__file__).resolve().parent.parent


def dem_on_grid(x, y, epsg, tile_dir=ROOT / "raw" / "dem"):
    X, Y = np.meshgrid(x, y)
    lon, lat = Transformer.from_crs(int(epsg), 4326, always_xy=True).transform(X, Y)
    out = np.full(X.shape, np.nan, np.float32)
    for t in sorted(Path(tile_dir).glob("*.tif")):
        with rasterio.open(t) as src:
            b = src.bounds
            m = (lon >= b.left) & (lon < b.right) & (lat > b.bottom) & (lat <= b.top) & np.isnan(out)
            if not m.any():
                continue
            band = src.read(1).astype(np.float32)
            inv = ~src.transform
            cols, rows = inv * (lon[m], lat[m])
            rows = np.clip(np.floor(rows).astype(int), 0, band.shape[0] - 1)
            cols = np.clip(np.floor(cols).astype(int), 0, band.shape[1] - 1)
            out[m] = band[rows, cols]
    return out
