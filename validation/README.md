# Central Valley GNSS Validation Dataset

Independent ground-truth vertical displacement time series from continuous GNSS stations inside the Central Valley study area (`bbox: [-120.2, 35.6, -119.0, 36.6]`).

## Data Source & Reference Frame

- **Provider:** Nevada Geodetic Laboratory (NGL), University of Nevada, Reno ([geodesy.unr.edu](https://geodesy.unr.edu/))
- **Station holdings catalog:** [DataHoldings.txt](https://geodesy.unr.edu/NGLStationPages/DataHoldings.txt)
- **Format specification:** [README_tenv3.txt](https://geodesy.unr.edu/gps_timeseries/readmes/README_tenv3.txt)
- **Reference frame:** `IGS20` fixed to the North American plate (`NA` solution: `.../IGS20/tenv3/NA/<STA>.NA.tenv3`). Using the plate-fixed `NA` frame suppresses rigid North American plate motion while preserving local vertical (`Up`) ground motion.
- **Units & conversion:** NGL `.tenv3` provides vertical coordinates in meters (`u0(m)` integer part + `____up(m)` fractional part, columns 12 and 13). `validation/fetch_gnss.py` preserves continuity across `u0(m)` and converts to centimeters (`up_cm`). Relative displacement between two dates is computed by subtracting the baseline epoch (e.g., 7-day median around the initial NISAR acquisition); **negative `Δup_cm` = subsidence**.
- **Owner:** PC6 (`validation/fetch_gnss.py`)

## Station Catalog (`validation/gnss_stations.csv`)

23 continuous GNSS stations inside `[-120.2, 35.6, -119.0, 36.6]` cover at least the NISAR provisional window (`2026-06-28` → `2026-09-20`). All station `.sta` pages and `.NA.tenv3` links were verified HTTP 200 on `2026-11-14`.

## Downloaded Time Series (`validation/gnss/<STA>.csv`, `2025-01-01` → `2026-10-31`)

10 stations were downloaded to span both the active Tulare Basin / Hanford / Five Points / Corcoran–Delano subsidence bowls and stable basin-margin bedrock/edge reference points (`P566`).

| Station | Lon (°) | Lat (°) | Rows (2025–2026) | Exported Span | ΔUp Provisional (`2026-06-28` → `2026-09-20`) | ΔUp Full-Year (`2025-11-24` → `2026-10-14`) | Role / Notes | Source |
|---|---:|---:|---:|---|---:|---:|---|---|
| **TLBN** | -119.4071 | 35.9347 | 647 | `2025-01-01` → `2026-10-31` | **-3.90 cm** | **-10.77 cm** | Tulare Lake Basin peak subsidence | [TLBN.sta](https://geodesy.unr.edu/NGLStationPages/stations/TLBN.sta) |
| **QCAP** | -119.6322 | 36.3136 | 655 | `2025-01-01` → `2026-10-31` | **-3.59 cm** | **-7.79 cm** | Hanford / Kings County agricultural bowl | [QCAP.sta](https://geodesy.unr.edu/NGLStationPages/stations/QCAP.sta) |
| **CAHA** | -119.6228 | 36.3234 | 515 | `2025-05-08` → `2026-10-17` | **-3.38 cm** | *gap ~Nov 17–28* | Caltrans Hanford (co-located cross-check near QCAP) | [CAHA.sta](https://geodesy.unr.edu/NGLStationPages/stations/CAHA.sta) |
| **HANF** | -119.6591 | 36.2152 | 585 | `2025-03-06` → `2026-10-31` | **-2.54 cm** | **-6.61 cm** | South of Hanford / Lemoore agricultural corridor | [HANF.sta](https://geodesy.unr.edu/NGLStationPages/stations/HANF.sta) |
| **CAFP** | -120.1020 | 36.4240 | 516 | `2025-05-08` → `2026-10-17` | **-2.40 cm** | *gap ~Nov 17–28* | Five Points (west-side Westlands irrigation area) | [CAFP.sta](https://geodesy.unr.edu/NGLStationPages/stations/CAFP.sta) |
| **P056** | -119.0629 | 36.0274 | 634 | `2025-01-01` → `2026-10-31` | **-1.65 cm** | **-3.01 cm** | Porterville / east-side Friant-Kern Canal corridor | [P056.sta](https://geodesy.unr.edu/NGLStationPages/stations/P056.sta) |
| **CAD1** | -119.2438 | 35.7594 | 515 | `2025-05-03` → `2026-10-31` | **-1.03 cm** | *gap ~Nov 17–29* | Delano (southern San Joaquin agricultural corridor) | [CAD1.sta](https://geodesy.unr.edu/NGLStationPages/stations/CAD1.sta) |
| **P565** | -119.2367 | 35.7439 | 657 | `2025-01-01` → `2026-10-31` | **-0.77 cm** | **-0.94 cm** | Earlimart / Delano NOTA station | [P565.sta](https://geodesy.unr.edu/NGLStationPages/stations/P565.sta) |
| **P564** | -119.3494 | 35.6229 | 656 | `2025-01-01` → `2026-10-31` | **-0.47 cm** | **-1.75 cm** | Wasco / Kern-Tulare border | [P564.sta](https://geodesy.unr.edu/NGLStationPages/stations/P564.sta) |
| **P566** | -119.2293 | 36.3245 | 658 | `2025-01-01` → `2026-10-31` | **-0.02 cm** | **-0.93 cm** | Visalia / northeast basin edge (near-stable baseline) | [P566.sta](https://geodesy.unr.edu/NGLStationPages/stations/P566.sta) |

*Note: Provisional/full-year ΔUp values above are computed from 7-day windows (`±3 days`) centered on the start and end dates to suppress daily GNSS scatter.*
