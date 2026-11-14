# Peer-Reviewed Literature Comparison — Central Valley & Karapınar

> **Calibration Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

This document compares our provisional 108-day L-band NISAR cumulative displacement and linearized annual-rate estimates (`data/central_valley/summary.json`, `data/karapinar/summary.json`) and our 11-month full-year chain (`data/central_valley_fullyear/summary.json`, `decomp.json`) against peer-reviewed geodetic (InSAR, GNSS, and extensometer) studies for both study areas. Every URL below was opened directly during verification (HTTP 200) and all quoted rates appear verbatim in the linked documents.

---

## 1. California Central Valley (Tulare Basin / San Joaquin Valley)

| Source | Year | Method | Period | Subsidence Rate (cm/yr) | Link |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **NASA NISAR StoryMap (*Land Subsidence*, Peacock et al.) / JPL UAVSAR (Miller et al.; Jones et al.)** | 2024 / 2020 | Airborne L-band UAVSAR InSAR | `2013–2017` | Cumulative subsidence bowl **> 100 cm** (`> 40 in`) along the California Aqueduct corridor (`Peacock et al. 2024`, `doi:10.5281/zenodo.10818833`) | https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828 |
| **NASA NISAR Applications White Paper (*Subsidence*)** | 2024 | L-band SAR / InSAR mission synthesis | Multi-year | Documents spatially gradual aquifer compaction undetected at street level until canal, bridge, and well damage accumulates | https://assets.science.nasa.gov/content/dam/science/missions/nisar/nisar-jpl/pdf/NISAR_Applications_Subsidence.pdf |
| **Neely et al. (*Water Resources Research*)** | 2021 | Sentinel-1 InSAR + cGPS | Oct 2015 – Sep 2017 (`WY2016–WY2017`) | Dry `WY2016`: mean **-4.20 cm/yr** (`-42.0 mm/yr`), peak **-34.5 cm/yr** (`-345 mm/yr`); Wet `WY2017`: mean **-2.04 cm/yr** (`-20.4 mm/yr`), peak **-17.7 cm/yr** (`-177 mm/yr`); `Apr 2015–Oct 2017` peak **-27.0 cm/yr** (`-270 mm/yr`) | https://pmc.ncbi.nlm.nih.gov/articles/PMC8047915/ |
| **Ojha, Werth & Shirzaei (*JGR Solid Earth*)** | 2019 | ALOS / Sentinel-1 InSAR + GPS + GRACE | `2007–2009` & `Jan 2015–Sep 2016` | Up to **-25.0 cm/yr** (`250 mm/yr`) in Tule/Kaweah subbasins (`~ -15.0 cm/yr` Chowchilla); **~ -30.0 cm/yr** (`2007–2009`) and **> -30.0 cm/yr** (`Jan 2015–Sep 2016`) in southern Central Valley | https://pmc.ncbi.nlm.nih.gov/articles/PMC6559157/ |
| **NASA Earth Observatory / JPL (Farr & Jones)** | 2017 | Satellite InSAR (NASA JPL for CA DWR) | `May 2015 – Sep 2016` | Up to **-60.0 cm/yr** (`0.6 m / 2 ft per yr`) near Chowchilla and Corcoran; up to **-51 cm** (`20 in`) over 16 months near Tranquility | https://earthobservatory.nasa.gov/images/89761/san-joaquin-valley-is-still-sinking |
| **Sneed, Brandt & Solt (*USGS SIR 2018-5144*)** | 2018 | InSAR + GPS + extensometers | `1926–1970` & `2003–2010` | Historical cumulative **> 8.5 m** (`1926–1970`); renewed drought compaction beneath Corcoran Clay (`2007–2010`) along a `145 km` reach of the California Aqueduct | https://pubs.usgs.gov/publication/sir20185144 |

> **Continuity with NASA's Land Subsidence Narrative:** NASA's NISAR StoryMap documented the Central Valley subsidence bowl and California Aqueduct corridor with airborne L-band UAVSAR radar during `2013–2017`. In `2025–2026`, we measured the same valley and aqueduct corridor from space with NISAR L-band interferometry, checked those measurements against continuous GPS stations, and ranked canal and road segments exposed to differential sinking.

---

## 2. Karapınar / Konya Closed Basin (Central Anatolia, Türkiye)

| Source | Year | Method | Period | Subsidence Rate (cm/yr) | Link |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Orhan et al. (*Sensors* 21(3):774)** | 2021 | Sentinel-1 (`2014–2018`) & COSMO-SkyMed (`2016–2017`) SBAS-InSAR + cGNSS | `2014 – 2018` | **> -7.0 cm/yr** (`> 70 mm/yr`) across broad agricultural parts of Karapınar Basin (`> 80%` cross-correlation with groundwater decline) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7865528/ |
| **Üstün, Tuşat & Yalvaç (*NHESS* 10:1151–1164)** | 2010 | GNSS monitoring network | `2006 – 2009` | **-1.2 to -5.2 cm/yr** (`-12 to -52 mm/yr`) vertical displacement across the Konya Closed Basin | https://nhess.copernicus.org/articles/10/1151/2010/ |
| **Canaslan Çomut et al. (*ISPRS Archives* XL-1/W5:115–119)** | 2015 | Multi-band InSAR (ERS-1/2, Envisat, ALOS L-band) | `1992 – 2010` | **-1.3 to -1.7 cm/yr** (`-13 to -17 mm/yr`) regional multi-decadal trend (faster locally north of Karaman / agricultural bowls) | https://isprs-archives.copernicus.org/articles/XL-1-W5/115/2015/ |

---

## 3. Comparison with Provisional 108-Day and 11-Month NISAR Estimates

| Site | Repo Source | Observation Window | Peak Cumulative LOS (`cm`) | Peak Vertical Estimate (`cm`) | Linearized Annual Rate Estimate (`cm/yr`) | Decomposed Permanent / Seasonal LOS | Literature Multi-Year Range (`cm/yr`) |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Central Valley** (Tulare / Corcoran, Summer 2026) | `data/central_valley/summary.json` | `2026-06-28` to `2026-10-14` (`108 d`, `7` pairs) | **-7.8** (`[-7.8, -4.7]` across `3` refs) | **-10.1** ($\theta = 39.1^\circ$) | **-26.4** (LOS) / **-34.1** (vertical)* | Not separable on `108 d` window | `-17.7` to `-34.5` peak (`Neely et al. 2021`; up to `-60.0` in 2015–2016 drought; `> 100 cm` UAVSAR 2013–2017 cumulative bowl) |
| **Central Valley Full-Year** (Earlimart / Tulare, 11-Month `mixed`) | `data/central_valley_fullyear/summary.json`, `decomp.json` | `2025-11-24` to `2026-10-14` (`324 d`, `25` pairs: `18` `beta-precal` + `7` `provisional`) | **-20.3** (`[-20.3, -11.7]` across `3` refs) | **-26.9** ($\theta = 40.9^\circ$) | **-22.9** (LOS) / **-30.3** (vertical) | **-16.8 ± 2.2 cm/yr** permanent at Earlimart (`p01`, $R^2 = 0.972$); seasonal amplitude **5.8 ± 0.8 cm** (`11.7 cm` peak-to-peak, low in August); basin median permanent **-3.74 cm/yr** (`p2 = -12.64 cm/yr`) | `-17.7` to `-34.5` peak (`Neely et al. 2021`); `-25.0` to `-30.0` (`Ojha et al. 2019`) |
| **Karapınar** (Konya Closed Basin) | `data/karapinar/summary.json` | `2026-06-26` to `2026-10-12` (`108 d`, `8` pairs) | **-5.9** | **-8.0** ($\theta = 42.0^\circ$) | **-20.0** (LOS) / **-27.0** (vertical)* | Seasonal cycle pending full-year archive | `-1.2` to `-5.2` (2006–2009 GNSS); `> -7.0` (`2014–2018` InSAR) |

\*Note: Linearized annual rates (`108-day cumulative * 365.25 / 108`) are explicitly flagged as provisional summer-window **estimates** in `data/*/summary.json`.

### Why 108-Day Summer Extrapolations Exceed Multi-Year Annual Rates — Confirmed by the 11-Month Decomposition

Our 108-day summer NISAR extrapolations (`-26.4 cm/yr` LOS / `-34.1 cm/yr` vertical in Central Valley; `-20.0 cm/yr` LOS / `-27.0 cm/yr` vertical in Karapınar) sit substantially above regional multi-year rates in Karapınar (`-1.2` to `> -7.0 cm/yr`) and at the upper drought end in the San Joaquin Valley (`-17.7` to `-34.5 cm/yr`). The newly completed 11-month (`324-day`, `2025-11-24 → 2026-10-14`, `mixed` quality) Central Valley chain in `data/central_valley_fullyear/` directly confirms why: at Earlimart (`p01`), seasonal + linear decomposition ($R^2 = 0.972$) separates a **permanent inelastic trend of `-16.8 ± 2.2 cm/yr` LOS** from a **reversible seasonal oscillation of `5.8 ± 0.8 cm` amplitude** (`11.7 cm` peak-to-peak, deepest low in August). Winter groundwater recovery and poroelastic rebound (`S_ke`) partially offset summer pumping drawdown, so multiplying a late-summer window by `365.25 / 108` overstates the long-term permanent rate (`-26.4` vs `-16.8 cm/yr`).
