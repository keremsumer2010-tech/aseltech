#!/usr/bin/env python3
"""Compare NISAR cumulative InSAR displacement against continuous GNSS vertical time series.

Reads:
  - validation/gnss_stations.csv and validation/gnss/<STA>.csv (NGL IGS20/NA, cm)
  - analysis/out/central_valley_cum.npz (produced by PC3 analysis/cumulative.py)

Writes:
  - data/central_valley/validation.json (per rules/VERI_SOZLESMESI.md section 4.2)

Usage:
  python validation/compare.py
  python validation/compare.py --npz analysis/out/central_valley_cum.npz --out data/central_valley/validation.json
  python validation/compare.py --self-test

Owner: PC6
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATIONS_CSV = ROOT / "validation" / "gnss_stations.csv"
DEFAULT_GNSS_DIR = ROOT / "validation" / "gnss"
DEFAULT_NPZ = ROOT / "analysis" / "out" / "central_valley_cum.npz"
DEFAULT_OUT = ROOT / "data" / "central_valley" / "validation.json"

DISCLAIMER = (
    "NISAR data are provisional. Calibration and validation are carried out by the "
    "NISAR project (NASA-JPL and ISRO), not by our team."
)


def lonlat_to_utm_math(lon: float, lat: float, epsg: int) -> tuple[float, float]:
    """WGS84 geographic (lon, lat) -> UTM Easting, Northing (m) without external dependencies."""
    if 32601 <= epsg <= 32660:
        zone = epsg - 32600
        north = True
    elif 32701 <= epsg <= 32760:
        zone = epsg - 32700
        north = False
    else:
        raise ValueError(f"Unsupported EPSG without pyproj: {epsg}")

    a = 6378137.0
    f = 1.0 / 298.257223563
    e2 = f * (2.0 - f)
    ep2 = e2 / (1.0 - e2)
    k0 = 0.9996

    lat_r = math.radians(lat)
    lon0_r = math.radians((zone - 1) * 6 - 180 + 3)
    dlon = math.radians(lon) - lon0_r

    sin_l = math.sin(lat_r)
    cos_l = math.cos(lat_r)
    tan_l = math.tan(lat_r)

    n_val = a / math.sqrt(1.0 - e2 * sin_l * sin_l)
    t_val = tan_l * tan_l
    c_val = ep2 * cos_l * cos_l
    a_val = cos_l * dlon

    m_val = a * (
        (1.0 - e2 / 4.0 - 3.0 * e2**2 / 64.0 - 5.0 * e2**3 / 256.0) * lat_r
        - (3.0 * e2 / 8.0 + 3.0 * e2**2 / 32.0 + 45.0 * e2**3 / 1024.0) * math.sin(2.0 * lat_r)
        + (15.0 * e2**2 / 256.0 + 45.0 * e2**3 / 1024.0) * math.sin(4.0 * lat_r)
        - (35.0 * e2**3 / 3072.0) * math.sin(6.0 * lat_r)
    )

    easting = k0 * n_val * (
        a_val
        + (1.0 - t_val + c_val) * a_val**3 / 6.0
        + (5.0 - 18.0 * t_val + t_val**2 + 72.0 * c_val - 58.0 * ep2) * a_val**5 / 120.0
    ) + 500000.0

    northing = k0 * (
        m_val
        + n_val
        * tan_l
        * (
            a_val**2 / 2.0
            + (5.0 - t_val + 9.0 * c_val + 4.0 * c_val**2) * a_val**4 / 24.0
            + (61.0 - 58.0 * t_val + t_val**2 + 600.0 * c_val - 330.0 * ep2) * a_val**6 / 720.0
        )
    )
    if not north:
        northing += 10000000.0
    return easting, northing


def project_to_crs(lon: float, lat: float, epsg: int) -> tuple[float, float]:
    try:
        from pyproj import Transformer

        tr = Transformer.from_crs(4326, epsg, always_xy=True)
        x, y = tr.transform(lon, lat)
        return float(x), float(y)
    except ImportError:
        return lonlat_to_utm_math(lon, lat, epsg)


def load_station_catalog(stations_csv: Path, gnss_dir: Path) -> list[dict]:
    stations: list[dict] = []
    with stations_csv.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sta = row["station"].strip()
            ts_path = gnss_dir / f"{sta}.csv"
            if ts_path.exists():
                stations.append(
                    {
                        "station": sta,
                        "lon": float(row["lon"]),
                        "lat": float(row["lat"]),
                        "ts_path": ts_path,
                    }
                )
    return stations


def load_gnss_series(csv_path: Path) -> list[tuple[dt.date, float]]:
    series: list[tuple[dt.date, float]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            series.append((dt.date.fromisoformat(row["date"]), float(row["up_cm"])))
    series.sort(key=lambda x: x[0])
    return series


def gnss_window_median(series: list[tuple[dt.date, float]], target_iso: str, half_window_days: int = 3) -> float | None:
    target = dt.date.fromisoformat(target_iso)
    vals = [val for d, val in series if abs((d - target).days) <= half_window_days]
    if not vals:
        return None
    return float(np.median(vals))


def extract_3x3_incidence(inc: np.ndarray | None, row: int, col: int) -> float | None:
    if inc is None or inc.size == 0:
        return None
    if inc.ndim == 0 or inc.size == 1:
        val = float(np.ravel(inc)[0])
        return val if math.isfinite(val) else None
    if inc.ndim == 2:
        h, w = inc.shape
        win = inc[max(row - 1, 0) : min(row + 2, h), max(col - 1, 0) : min(col + 2, w)]
        finite = win[np.isfinite(win)]
        if finite.size == 0:
            return None
        return float(np.median(finite))
    return None


def compute_metrics(insar_vals: list[float | None], gnss_vals: list[float | None]) -> tuple[float | None, float | None]:
    pairs = [(a, b) for a, b in zip(insar_vals, gnss_vals) if a is not None and b is not None]
    if len(pairs) < 2:
        return None, None
    arr_i = np.array([p[0] for p in pairs], dtype=np.float64)
    arr_g = np.array([p[1] for p in pairs], dtype=np.float64)
    rmse = float(np.sqrt(np.mean((arr_i - arr_g) ** 2)))
    std_i = float(np.std(arr_i))
    std_g = float(np.std(arr_g))
    if std_i < 1e-12 or std_g < 1e-12:
        corr = None
    else:
        c = float(np.corrcoef(arr_i, arr_g)[0, 1])
        corr = round(c, 4) if math.isfinite(c) else None
    return round(rmse, 3), corr


def run_comparison(
    npz_path: Path,
    stations_csv: Path = DEFAULT_STATIONS_CSV,
    gnss_dir: Path = DEFAULT_GNSS_DIR,
) -> list[dict]:
    if not npz_path.exists():
        raise FileNotFoundError(f"NPZ file not found: {npz_path}")

    d = np.load(npz_path, allow_pickle=False)
    x = np.asarray(d["x"], dtype=np.float64)
    y = np.asarray(d["y"], dtype=np.float64)
    epsg = int(d["epsg"])
    dates = [str(s) for s in d["dates"]]
    quality = str(d["quality"]) if "quality" in d else "provisional"
    inc = np.asarray(d["incidence"], dtype=np.float64) if "incidence" in d else None

    stack_path = npz_path.with_name(npz_path.stem + "_stack.npz")
    if "cum_stack_cm" in d and d["cum_stack_cm"].ndim == 3:
        stack = np.asarray(d["cum_stack_cm"], dtype=np.float64)
    elif stack_path.exists():
        ds = np.load(stack_path, allow_pickle=False)
        stack = np.asarray(ds["cum_stack_cm"], dtype=np.float64)
        if "dates" in ds and len(ds["dates"]) == stack.shape[0]:
            dates = [str(s) for s in ds["dates"]]
    else:
        cum_cm = np.asarray(d["cum_cm"], dtype=np.float64)
        zeros = np.where(np.isfinite(cum_cm), 0.0, np.nan)
        stack = np.stack([zeros, cum_cm], axis=0)
        if len(dates) >= 2:
            dates = [dates[0], dates[-1]]

    if len(x) < 2 or len(y) < 2:
        raise ValueError("Grid axes x/y must have length >= 2")

    dx = float(x[1] - x[0])
    dy = float(y[1] - y[0])
    _, h, w = stack.shape

    stations = load_station_catalog(stations_csv, gnss_dir)
    results: list[dict] = []

    for st in stations:
        sta = st["station"]
        lon, lat = st["lon"], st["lat"]
        gnss_raw = load_gnss_series(st["ts_path"])
        gnss_at_dates = [gnss_window_median(gnss_raw, dt_str, half_window_days=3) for dt_str in dates]

        sx, sy = project_to_crs(lon, lat, epsg)
        col = int(round((sx - float(x[0])) / dx))
        row = int(round((sy - float(y[0])) / dy))

        in_bounds = 0 <= row < h and 0 <= col < w
        inc_deg = extract_3x3_incidence(inc, row, col) if in_bounds else None

        if in_bounds:
            r0, r1 = max(row - 1, 0), min(row + 2, h)
            c0, c1 = max(col - 1, 0), min(col + 2, w)
            los_series: list[float | None] = []
            for k in range(len(dates)):
                win = stack[k, r0:r1, c0:c1]
                finite = win[np.isfinite(win)]
                los_series.append(float(np.median(finite)) if finite.size > 0 else None)
        else:
            los_series = [None] * len(dates)

        # Project LOS -> approximate vertical assuming purely vertical subsidence
        if inc_deg is not None and 0.0 <= inc_deg < 85.0:
            cos_inc = math.cos(math.radians(inc_deg))
            insar_series = [v / cos_inc if v is not None else None for v in los_series]
            comp_label = "vertical_estimate (LOS / cos(incidence))"
            los_note = (
                f"InSAR LOS converted to vertical via LOS / cos({inc_deg:.1f} deg), "
                "assuming negligible horizontal motion."
            )
        else:
            insar_series = los_series
            comp_label = "LOS (no incidence grid)"
            los_note = (
                "InSAR kept as Line-of-Sight (LOS) because no per-pixel incidence angle was supplied; "
                "LOS = vertical * cos(incidence) typically underestimates pure vertical motion by ~15-35%."
            )

        # Align both series to the first mutually valid epoch (typically dates[0])
        base_idx = next(
            (i for i in range(len(dates)) if insar_series[i] is not None and gnss_at_dates[i] is not None),
            None,
        )
        if base_idx is not None:
            i0 = insar_series[base_idx]
            g0 = gnss_at_dates[base_idx]
            insar_rel = [round(v - i0, 3) if v is not None else None for v in insar_series]
            gnss_rel = [round(v - g0, 3) if v is not None else None for v in gnss_at_dates]
        else:
            # Keep GNSS relative to first available GNSS date even if InSAR pixel was masked
            g_first = next((v for v in gnss_at_dates if v is not None), None)
            insar_rel = [None] * len(dates)
            gnss_rel = [
                round(v - g_first, 3) if (v is not None and g_first is not None) else None
                for v in gnss_at_dates
            ]

        rmse_cm, corr = compute_metrics(insar_rel, gnss_rel)

        if not in_bounds:
            status_note = f"Station ({lon:.4f}, {lat:.4f}) is outside the InSAR grid bounds."
        elif base_idx is None:
            status_note = "3x3 window around station had no valid InSAR pixels (masked or outside swath)."
        else:
            status_note = (
                f"3x3 median at grid pixel (row={row}, col={col}) zero-referenced to {dates[base_idx]}; "
                "GNSS is 7-day median (+/-3d) of NGL IGS20/NA Up series."
            )

        results.append(
            {
                "station": sta,
                "lon": round(lon, 4),
                "lat": round(lat, 4),
                "rmse_cm": rmse_cm,
                "corr": corr,
                "dates": dates,
                "insar": insar_rel,
                "gnss": gnss_rel,
                "component": comp_label,
                "incidence_deg": round(inc_deg, 2) if inc_deg is not None else None,
                "quality": quality,
                "quality_note": DISCLAIMER,
                "notes": f"{status_note} {los_note}",
            }
        )

    return results


def self_test() -> None:
    print("Running validation/compare.py --self-test ...")
    # 1. Verify pure-math UTM matches pyproj (if installed) to < 1 cm across Central Valley
    test_lon, test_lat = -119.4071, 35.9347  # TLBN
    xm, ym = lonlat_to_utm_math(test_lon, test_lat, 32611)
    xp, yp = project_to_crs(test_lon, test_lat, 32611)
    err_m = math.hypot(xm - xp, ym - yp)
    print(f"  UTM parity check (TLBN EPSG:32611): math=({xm:.3f}, {ym:.3f}) diff={err_m*100:.4f} cm")
    assert err_m < 0.01, f"UTM projection discrepancy too high: {err_m} m"

    # 2. Build synthetic NPZ matching cumulative.py schema around TLBN, QCAP, P566
    dates = ["2026-06-28", "2026-07-22", "2026-08-15", "2026-09-20"]
    xs = np.arange(220000.0, 320000.0, 80.0, dtype=np.float64)
    ys = np.arange(4040000.0, 3930000.0, -80.0, dtype=np.float64)
    h, w = len(ys), len(xs)
    inc_deg = 38.0
    cos_inc = math.cos(math.radians(inc_deg))

    stack = np.zeros((len(dates), h, w), dtype=np.float32)
    inc_grid = np.full((h, w), inc_deg, dtype=np.float32)

    # Plant actual GNSS vertical trajectories * cos(inc) into 5x5 patches around TLBN, QCAP, P566
    dx, dy = xs[1] - xs[0], ys[1] - ys[0]
    planted: dict[str, list[float]] = {}
    for sta, lon, lat in [("TLBN", -119.4071, 35.9347), ("QCAP", -119.6322, 36.3136), ("P566", -119.2293, 36.3245)]:
        series = load_gnss_series(DEFAULT_GNSS_DIR / f"{sta}.csv")
        g_vals = [gnss_window_median(series, dt_s) for dt_s in dates]
        assert all(v is not None for v in g_vals)
        rel_vert = [v - g_vals[0] for v in g_vals]
        planted[sta] = rel_vert
        sx, sy = project_to_crs(lon, lat, 32611)
        col = int(round((sx - xs[0]) / dx))
        row = int(round((sy - ys[0]) / dy))
        assert 2 <= row < h - 2 and 2 <= col < w - 2, f"{sta} outside synthetic test grid"
        for k, v_vert in enumerate(rel_vert):
            stack[k, row - 2 : row + 3, col - 2 : col + 3] = float(v_vert * cos_inc)

    with tempfile.TemporaryDirectory() as tmp:
        npz_path = Path(tmp) / "synthetic_cum.npz"
        np.savez_compressed(
            npz_path,
            cum_cm=stack[-1],
            x=xs,
            y=ys,
            epsg=np.int32(32611),
            dates=np.array(dates),
            quality="provisional",
            cum_stack_cm=stack,
            incidence=inc_grid,
        )
        out = run_comparison(npz_path)

    by_sta = {r["station"]: r for r in out}
    for sta in ("TLBN", "QCAP", "P566"):
        r = by_sta[sta]
        print(f"  {sta}: rmse={r['rmse_cm']} cm, corr={r['corr']}, gnss={r['gnss']}, insar={r['insar']}")
        assert r["rmse_cm"] is not None and r["rmse_cm"] < 0.01, f"Unexpected RMSE for {sta}: {r['rmse_cm']}"
        assert r["corr"] is not None and r["corr"] > 0.999, f"Unexpected corr for {sta}: {r['corr']}"
        assert r["quality"] == "provisional"
        assert "calibration" in r["quality_note"].lower()

    # Check JSON serialization produces zero NaN tokens
    dumped = json.dumps(out, allow_nan=False)
    assert "NaN" not in dumped
    print(f"Self-test passed ({len(out)} stations evaluated, JSON clean).")


def main() -> None:
    ap = argparse.ArgumentParser(description="Compare NISAR cumulative InSAR vs. GNSS time series.")
    ap.add_argument("--npz", type=Path, default=DEFAULT_NPZ)
    ap.add_argument("--stations", type=Path, default=DEFAULT_STATIONS_CSV)
    ap.add_argument("--gnss-dir", type=Path, default=DEFAULT_GNSS_DIR)
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Explicit output validation.json path (overrides --data-dir).",
    )
    ap.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Target output directory where validation.json is written if --out is omitted.",
    )
    ap.add_argument(
        "--quality",
        type=str,
        default=None,
        help="Optional quality label override (e.g. 'mixed' for full-year beta+provisional runs).",
    )
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return

    out_path = args.out or ((args.data_dir / "validation.json") if args.data_dir else DEFAULT_OUT)
    results = run_comparison(args.npz, args.stations, args.gnss_dir)
    if args.quality:
        for row in results:
            row["quality"] = args.quality
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(results, indent=2, allow_nan=False) + "\n")
    valid_stations = [r for r in results if r["rmse_cm"] is not None]
    print(f"Wrote {out_path} ({len(results)} stations, {len(valid_stations)} inside valid InSAR footprint)")
    for r in valid_stations:
        print(f"  {r['station']:5s} rmse={r['rmse_cm']} cm  corr={r['corr']}  insar_end={r['insar'][-1]} cm  gnss_end={r['gnss'][-1]} cm")


if __name__ == "__main__":
    main()
