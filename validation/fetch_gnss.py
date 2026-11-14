#!/usr/bin/env python3
"""Fetch Central Valley continuous GNSS station metadata and vertical (Up) time series
from Nevada Geodetic Laboratory (NGL, University of Nevada, Reno).

Data source:
  - Station catalog: https://geodesy.unr.edu/NGLStationPages/DataHoldings.txt
  - Time series format: IGS20 North America plate-fixed (.NA.tenv3)
  - Format documentation: https://geodesy.unr.edu/gps_timeseries/readmes/README_tenv3.txt

Owner: PC6
"""
from __future__ import annotations

import csv
import datetime as dt
import os
import time
import urllib.request
from pathlib import Path

# Central Valley bbox [lon_min, lat_min, lon_max, lat_max] per rules/VERI_SOZLESMESI.md
BBOX = (-120.2, 35.6, -119.0, 36.6)

# Minimum required coverage: NISAR provisional period (2026-06-28 -> 2026-09-20)
REQ_START = "2026-06-28"
REQ_END = "2026-09-20"

# Export daily time series starting from this date (covers full-year 2025-11-24 -> 2026-10-14 + baseline)
SERIES_FROM_DATE = "2025-01-01"

# 10 stations spanning subsiding agricultural basins (Tulare Basin, Hanford, Five Points,
# Corcoran/Tipton/Delano corridor) and stable basin margin reference (P566)
SELECTED_STATIONS = [
    "TLBN",
    "QCAP",
    "CAHA",
    "HANF",
    "CAFP",
    "P056",
    "CAD1",
    "P565",
    "P564",
    "P566",
]

DATA_HOLDINGS_URL = "https://geodesy.unr.edu/NGLStationPages/DataHoldings.txt"
STA_PAGE_TMPL = "https://geodesy.unr.edu/NGLStationPages/stations/{sta}.sta"
TENV3_URL_TMPL = "https://geodesy.unr.edu/gps_timeseries/IGS20/tenv3/NA/{sta}.NA.tenv3"

ROOT_DIR = Path(__file__).resolve().parent
GNSS_DIR = ROOT_DIR / "gnss"
STATIONS_CSV = ROOT_DIR / "gnss_stations.csv"


def fetch_text(url: str, timeout: int = 30, retries: int = 3) -> str:
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; aseltech-nisar-pulse/1.0)"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:
            last_err = exc
            if attempt < retries - 1:
                time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def parse_holdings(text: str) -> list[dict[str, str]]:
    w, s, e, n = BBOX
    rows: list[dict[str, str]] = []
    lines = text.splitlines()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 11:
            continue
        sta = parts[0].strip()
        lat = float(parts[1])
        lon = float(parts[2])
        if lon > 180.0:
            lon -= 360.0
        beg = parts[7].strip()
        end = parts[8].strip()
        if w <= lon <= e and s <= lat <= n and beg <= REQ_START and end >= REQ_END:
            rows.append(
                {
                    "station": sta,
                    "lon": f"{lon:.4f}",
                    "lat": f"{lat:.4f}",
                    "source_url": STA_PAGE_TMPL.format(sta=sta),
                    "series_url": TENV3_URL_TMPL.format(sta=sta),
                    "first_date": beg,
                    "last_date": end,
                }
            )
    rows.sort(key=lambda r: r["station"])
    return rows


def parse_tenv3(text: str, start_date: str = SERIES_FROM_DATE) -> list[tuple[str, float]]:
    """Parse NGL .tenv3 vertical coordinates (m -> cm).

    Columns (0-indexed) per README_tenv3.txt:
      1: YYMMMDD date
      11: u0(m) vertical integer portion
      12: ____up(m) vertical fractional portion
    Returns list of (YYYY-MM-DD, up_cm) sorted by date.
    """
    records: list[tuple[str, float]] = []
    u0_ref: float | None = None
    for line in text.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 13:
            continue
        date_iso = dt.datetime.strptime(parts[1], "%y%b%d").strftime("%Y-%m-%d")
        if date_iso < start_date:
            continue
        u0_m = float(parts[11])
        up_frac_m = float(parts[12])
        if u0_ref is None:
            u0_ref = u0_m
        # Preserve continuity if integer portion u0(m) re-initializes across 10m boundary
        up_cm = ((u0_m - u0_ref) + up_frac_m) * 100.0
        records.append((date_iso, round(up_cm, 4)))
    records.sort(key=lambda x: x[0])
    return records


def summarize_window(records: list[tuple[str, float]], t0: str, t1: str) -> tuple[float | None, int]:
    """Compute change in cm between 7-day windows centered on t0 and t1."""
    d0 = dt.date.fromisoformat(t0)
    d1 = dt.date.fromisoformat(t1)
    w0 = [v for s, v in records if abs((dt.date.fromisoformat(s) - d0).days) <= 3]
    w1 = [v for s, v in records if abs((dt.date.fromisoformat(s) - d1).days) <= 3]
    if not w0 or not w1:
        return None, len(records)
    return round(sum(w1) / len(w1) - sum(w0) / len(w0), 2), len(records)


def main() -> None:
    os.makedirs(GNSS_DIR, exist_ok=True)
    print(f"Fetching NGL station holdings from {DATA_HOLDINGS_URL} ...")
    holdings_text = fetch_text(DATA_HOLDINGS_URL)
    stations = parse_holdings(holdings_text)
    print(f"Found {len(stations)} stations inside bbox {BBOX} covering {REQ_START} -> {REQ_END}")

    with STATIONS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["station", "lon", "lat", "source_url", "series_url", "first_date", "last_date"],
        )
        writer.writeheader()
        writer.writerows(stations)
    print(f"Wrote {STATIONS_CSV} ({len(stations)} rows)")

    station_map = {r["station"]: r for r in stations}
    print("\nDownloading vertical (Up) time series for selected stations:")
    print(f"{'STA':5s} {'Lon':>9s} {'Lat':>8s} {'Rows':>5s} {'First':>10s} {'Last':>10s} {'d_Prov(cm)':>10s} {'d_Year(cm)':>10s}")
    for sta in SELECTED_STATIONS:
        if sta not in station_map:
            raise RuntimeError(f"Selected station {sta} not found in filtered DataHoldings!")
        url = station_map[sta]["series_url"]
        time.sleep(0.5)
        text = fetch_text(url)
        records = parse_tenv3(text, start_date=SERIES_FROM_DATE)
        if not records:
            raise RuntimeError(f"No records parsed for {sta} from {url}")
        out_csv = GNSS_DIR / f"{sta}.csv"
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "up_cm"])
            writer.writerows(records)

        d_prov, n_rows = summarize_window(records, REQ_START, REQ_END)
        d_year, _ = summarize_window(records, "2025-11-24", "2026-10-14")
        prov_str = f"{d_prov:+.2f}" if d_prov is not None else "n/a"
        year_str = f"{d_year:+.2f}" if d_year is not None else "n/a"
        print(
            f"{sta:5s} {station_map[sta]['lon']:>9s} {station_map[sta]['lat']:>8s} "
            f"{n_rows:5d} {records[0][0]:>10s} {records[-1][0]:>10s} {prov_str:>10s} {year_str:>10s}"
        )


if __name__ == "__main__":
    main()
