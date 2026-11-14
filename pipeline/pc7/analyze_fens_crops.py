"""Build repeatable Fens GCOV sample-window summaries from PC2's local subsets."""

from __future__ import annotations

import json
from datetime import date as date_type
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "pipeline" / "subset" / "fens_gcov"
OUTPUT = ROOT / "data" / "fens"
POLARIZATION_PLOT = ROOT / "docs" / "story" / "media" / "pc7_polarization.png"
WINDOW_PIXELS = 12
PIXEL_SIZE_M = 40
WINDOW_SIZE_M = WINDOW_PIXELS * PIXEL_SIZE_M
FIELD_CENTRES_UTM = [
    ("f01", "Fens field-like sample 1", 690000.0, 5851000.0),
    ("f02", "Fens field-like sample 2", 703000.0, 5843000.0),
    ("f03", "Fens field-like sample 3", 716000.0, 5832000.0),
    ("f04", "Fens field-like sample 4", 727000.0, 5819000.0),
]
REQUIRED_KEYS = {"hh_db", "hv_db", "x", "y", "epsg", "date", "quality", "granule"}


def load_inputs():
    paths = sorted(INPUT.glob("*.npz"))
    if not paths:
        raise FileNotFoundError(f"No local Fens GCOV subsets found in {INPUT}")

    records = []
    reference_x = reference_y = None
    reference_epsg = None
    for path in paths:
        with np.load(path, allow_pickle=False) as data:
            missing = REQUIRED_KEYS - set(data.files)
            if missing:
                raise ValueError(f"{path.name} is missing keys: {sorted(missing)}")
            record = {key: data[key].copy() for key in REQUIRED_KEYS}

        date = str(record["date"].item())
        quality = str(record["quality"].item())
        epsg = int(record["epsg"].item())
        if path.stem != date:
            raise ValueError(f"Filename/date mismatch: {path.name} contains {date}")
        if quality != "provisional":
            raise ValueError(f"Refusing non-provisional subset {path.name}: {quality}")
        if reference_epsg is None:
            reference_epsg = epsg
            reference_x = record["x"]
            reference_y = record["y"]
        elif epsg != reference_epsg or not np.array_equal(record["x"], reference_x) or not np.array_equal(record["y"], reference_y):
            raise ValueError(f"Grid mismatch in {path.name}")

        expected_shape = (record["y"].size, record["x"].size)
        for key in ("hh_db", "hv_db"):
            if record[key].shape != expected_shape:
                raise ValueError(f"{path.name} {key} shape does not match x/y axes")
        record["path"] = path
        record["date_text"] = date
        records.append(record)

    dates = [record["date_text"] for record in records]
    if dates != sorted(set(dates)):
        raise ValueError(f"Dates must be unique and sorted: {dates}")
    return records, reference_x, reference_y, reference_epsg


def analyze():
    records, x, y, epsg = load_inputs()
    if not np.allclose(np.diff(x), PIXEL_SIZE_M) or not np.allclose(np.diff(y), -PIXEL_SIZE_M):
        raise ValueError("Expected 40 m eastward x spacing and north-up 40 m y spacing")

    to_wgs84 = Transformer.from_crs(epsg, 4326, always_xy=True)
    dates = [record["date_text"] for record in records]
    plot_dates = [date_type.fromisoformat(value) for value in dates]
    fields = []
    plot_series = []
    half = WINDOW_PIXELS // 2

    for field_id, name, target_x, target_y in FIELD_CENTRES_UTM:
        col = int(np.argmin(np.abs(x - target_x)))
        row = int(np.argmin(np.abs(y - target_y)))
        row0, row1 = row - half, row + half
        col0, col1 = col - half, col + half
        if row0 < 0 or col0 < 0 or row1 > len(y) or col1 > len(x):
            raise ValueError(f"Window for {field_id} falls outside the raster")

        hv_values = []
        hh_values = []
        ratio_values = []
        ratio_db_values = []
        for record in records:
            hv = record["hv_db"][row0:row1, col0:col1]
            hh = record["hh_db"][row0:row1, col0:col1]
            common_valid = np.isfinite(hv) & np.isfinite(hh)
            if common_valid.sum() != WINDOW_PIXELS * WINDOW_PIXELS:
                raise ValueError(f"Incomplete HH/HV coverage for {field_id} on {record['date_text']}")
            hv_values.append(round(float(np.mean(hv[common_valid], dtype=np.float64)), 2))
            hh_values.append(round(float(np.mean(hh[common_valid], dtype=np.float64)), 2))
            pixel_ratios = np.power(10.0, (hv[common_valid] - hh[common_valid]) / 10.0)
            mean_ratio = float(np.mean(pixel_ratios, dtype=np.float64))
            ratio_values.append(round(mean_ratio, 5))
            ratio_db_values.append(round(10.0 * float(np.log10(mean_ratio)), 2))

        west = float(x[col0] - PIXEL_SIZE_M / 2)
        east = float(x[col1 - 1] + PIXEL_SIZE_M / 2)
        north = float(y[row0] + PIXEL_SIZE_M / 2)
        south = float(y[row1 - 1] - PIXEL_SIZE_M / 2)
        center_x = (west + east) / 2
        center_y = (south + north) / 2
        lon, lat = to_wgs84.transform(center_x, center_y)

        fields.append(
            {
                "id": field_id,
                "name": name,
                "lon": round(lon, 5),
                "lat": round(lat, 5),
                "hv_db": hv_values,
                "hh_db": hh_values,
                "hv_hh_ratio": ratio_values,
                "hv_hh_ratio_db": ratio_db_values,
                "sample_window": {
                    "epsg": epsg,
                    "bounds_m": [round(west, 1), round(south, 1), round(east, 1), round(north, 1)],
                },
            }
        )
        plot_series.append({
            "hh_db": hh_values,
            "hv_db": hv_values,
            "hv_hh_ratio": ratio_values,
            "hv_hh_ratio_db": ratio_db_values,
        })

    granules = [str(record["granule"].item()) for record in records]
    first_date, last_date = dates[0], dates[-1]
    mean_hh_range = float(np.mean([np.ptp(series["hh_db"]) for series in plot_series]))
    mean_hv_range = float(np.mean([np.ptp(series["hv_db"]) for series in plot_series]))
    mean_ratio_range = float(np.mean([np.ptp(series["hv_hh_ratio_db"]) for series in plot_series]))
    method = (
        f"Eight provisional NISAR GCOV acquisitions (CRID P05023; {first_date} to {last_date}) were averaged in four separated 480 m by 480 m windows (12 by 12 40 m pixels) selected from field-like patterns in the local median-HV image; window centers are WGS84 and bounds are EPSG:32630. "
        f"Mean per-window temporal ranges were {mean_hh_range:.2f} dB for HH, {mean_hv_range:.2f} dB for HV, and {mean_ratio_range:.2f} dB for 10 log10(HV/HH); these differences do not identify a crop event. "
        "The observations do not establish a harvest or tillage effect, and the windows are sampling rectangles rather than verified cadastral field polygons."
    )
    result = {
        "dates": dates,
        "fields": fields,
        "quality": "provisional",
        "quality_note": f"{len(dates)} local NISAR GCOV P05023 provisional acquisitions from {first_date} through {last_date}. The 480 m sample windows are field-like sampling areas, not verified parcel boundaries; sparse dates limit crop-phenology interpretation.",
        "source": "NASA-ISRO NISAR Level-2 PR GCOV Provisional (CRID P05023), local PC2 subsets under pipeline/subset/fens_gcov/.",
        "granules": granules,
        "method": method,
    }

    OUTPUT.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT / "crops.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for field, values in zip(fields, plot_series):
        ax.plot(plot_dates, values["hv_db"], marker="o", linewidth=1.8, label=field["id"])
    ax.set_title("Fens sample-window mean HV backscatter")
    ax.set_ylabel("Mean HV backscatter (dB)")
    ax.set_xlabel("NISAR acquisition date")
    ax.grid(True, alpha=0.25)
    ax.legend(title="Sample window", ncol=2)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    fig.tight_layout()
    fig.savefig(OUTPUT / "hv_timeseries.png", dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    channels = [
        ("hh_db", "HH backscatter (dB)"),
        ("hv_db", "HV backscatter (dB)"),
        ("hv_hh_ratio_db", "10 log10(HV/HH) (dB)"),
    ]
    for ax, (key, ylabel) in zip(axes, channels):
        for field, series in zip(fields, plot_series):
            ax.plot(plot_dates, series[key], marker="o", linewidth=1.5, label=field["id"])
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.25)
    axes[0].set_title("Fens polarization comparison across four sample windows")
    axes[0].legend(title="Window", ncol=4)
    axes[-1].set_xlabel("NISAR acquisition date")
    axes[-1].xaxis.set_major_locator(mdates.AutoDateLocator())
    axes[-1].xaxis.set_major_formatter(mdates.ConciseDateFormatter(axes[-1].xaxis.get_major_locator()))
    fig.tight_layout()
    POLARIZATION_PLOT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(POLARIZATION_PLOT, dpi=180)
    plt.close(fig)

    print(json.dumps({"dates": dates, "fields": fields, "outputs": [str(json_path), str(OUTPUT / 'hv_timeseries.png'), str(POLARIZATION_PLOT)]}, indent=2))


if __name__ == "__main__":
    analyze()
