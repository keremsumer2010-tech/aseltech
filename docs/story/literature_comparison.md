# Peer-Reviewed Literature Comparison — Central Valley & Karapınar

> **Calibration Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

This document compares our provisional 108-day L-band NISAR cumulative displacement and linearized annual-rate estimates (`data/central_valley/summary.json`, `data/karapinar/summary.json`) against peer-reviewed geodetic (InSAR, GNSS, and extensometer) studies for both study areas. Every URL below was opened directly during verification (HTTP 200) and all quoted rates appear verbatim in the linked documents.

---

## 1. California Central Valley (Tulare Basin / San Joaquin Valley)

| Source | Year | Method | Period | Subsidence Rate (cm/yr) | Link |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Neely et al. (*Water Resources Research*)** | 2021 | Sentinel-1 InSAR + cGPS | Oct 2015 – Sep 2017 (`WY2016–WY2017`) | Dry `WY2016`: mean **-4.20 cm/yr** (`-42.0 mm/yr`), peak **-34.5 cm/yr** (`-345 mm/yr`); Wet `WY2017`: mean **-2.04 cm/yr** (`-20.4 mm/yr`), peak **-17.7 cm/yr** (`-177 mm/yr`); `Apr 2015–Oct 2017` peak **-27.0 cm/yr** (`-270 mm/yr`) | https://pmc.ncbi.nlm.nih.gov/articles/PMC8047915/ |
| **Ojha, Werth & Shirzaei (*JGR Solid Earth*)** | 2019 | ALOS / Sentinel-1 InSAR + GPS + GRACE | `2007–2009` & `Jan 2015–Sep 2016` | Up to **-25.0 cm/yr** (`250 mm/yr`) in Tule/Kaweah subbasins (`~ -15.0 cm/yr` Chowchilla); **~ -30.0 cm/yr** (`2007–2009`) and **> -30.0 cm/yr** (`Jan 2015–Sep 2016`) in southern Central Valley | https://pmc.ncbi.nlm.nih.gov/articles/PMC6559157/ |
| **NASA Earth Observatory / JPL (Farr & Jones)** | 2017 | Satellite InSAR (NASA JPL for CA DWR) | `May 2015 – Sep 2016` | Up to **-60.0 cm/yr** (`0.6 m / 2 ft per yr`) near Chowchilla and Corcoran; up to **-51 cm** (`20 in`) over 16 months near Tranquility | https://earthobservatory.nasa.gov/images/89761/san-joaquin-valley-is-still-sinking |
| **Sneed, Brandt & Solt (*USGS SIR 2018-5144*)** | 2018 | InSAR + GPS + extensometers | `1926–1970` & `2003–2010` | Historical cumulative **> 8.5 m** (`1926–1970`); renewed drought compaction beneath Corcoran Clay (`2007–2010`) along a `145 km` reach of the California Aqueduct | https://pubs.usgs.gov/publication/sir20185144 |

---

## 2. Karapınar / Konya Closed Basin (Central Anatolia, Türkiye)

| Source | Year | Method | Period | Subsidence Rate (cm/yr) | Link |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Orhan et al. (*Sensors* 21(3):774)** | 2021 | Sentinel-1 (`2014–2018`) & COSMO-SkyMed (`2016–2017`) SBAS-InSAR + cGNSS | `2014 – 2018` | **> -7.0 cm/yr** (`> 70 mm/yr`) across broad agricultural parts of Karapınar Basin (`> 80%` cross-correlation with groundwater decline) | https://pmc.ncbi.nlm.nih.gov/articles/PMC7865528/ |
| **Üstün, Tuşat & Yalvaç (*NHESS* 10:1151–1164)** | 2010 | GNSS monitoring network | `2006 – 2009` | **-1.2 to -5.2 cm/yr** (`-12 to -52 mm/yr`) vertical displacement across the Konya Closed Basin | https://nhess.copernicus.org/articles/10/1151/2010/ |
| **Canaslan Çomut et al. (*ISPRS Archives* XL-1/W5:115–119)** | 2015 | Multi-band InSAR (ERS-1/2, Envisat, ALOS L-band) | `1992 – 2010` | **-1.3 to -1.7 cm/yr** (`-13 to -17 mm/yr`) regional multi-decadal trend (faster locally north of Karaman / agricultural bowls) | https://isprs-archives.copernicus.org/articles/XL-1-W5/115/2015/ |

---

## 3. Comparison with Provisional 108-Day NISAR Estimates

| Site | Repo Source | Observation Window (108 days) | Peak Cumulative LOS (`cm`) | Peak Vertical Estimate (`cm`) | Linearized Annual Rate Estimate (`cm/yr`) | Literature Multi-Year Range (`cm/yr`) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Central Valley** (Tulare / Corcoran) | `data/central_valley/summary.json` | `2026-06-28` to `2026-10-14` (`7` pairs) | **-7.8** (`[-7.8, -6.2]` ref sensitivity) | **-10.1** ($\theta = 39.1^\circ$) | **-26.4** (LOS) / **-34.1** (vertical)* | `-17.7` to `-34.5` peak (up to `-60.0` in 2015–2016 drought) |
| **Karapınar** (Konya Closed Basin) | `data/karapinar/summary.json` | `2026-06-26` to `2026-10-12` (`8` pairs) | **-5.9** | **-8.0** ($\theta = 42.0^\circ$) | **-20.0** (LOS) / **-27.0** (vertical)* | `-1.2` to `-5.2` (2006–2009 GNSS); `> -7.0` (`2014–2018` InSAR) |

\*Note: Linearized annual rates (`108-day cumulative * 365.25 / 108`) are explicitly flagged as provisional summer-window **estimates** in `data/*/summary.json`.

### Why 108-Day Summer Extrapolations Exceed Multi-Year Annual Rates

Our annualized NISAR estimates (`-26.4 cm/yr` LOS / `-34.1 cm/yr` vertical in Central Valley; `-20.0 cm/yr` LOS / `-27.0 cm/yr` vertical in Karapınar) fall inside drought-peak Central Valley measurements (`-25` to `-60 cm/yr`) but sit substantially above multi-year annual averages in Karapınar (`-1.2` to `> -7.0 cm/yr`). This contrast reflects the strong seasonal asymmetry of irrigated aquifer systems: our 108-day observation period (`June 26/28` to `October 12/14, 2026`) captures solely the peak summer pumping season, when evapotranspiration demand is highest and hydraulic head drops most steeply. Because a full hydrologic year includes autumn–spring groundwater recovery and partial poroelastic rebound (`S_ke`), multiplying a pure summer drawdown segment by `365.25 / 108` systematically overstates the net annual compaction rate. Once full-year NISAR acquisitions arrive, direct 12-month differencing will separate reversible seasonal elastic motion from permanent inelastic aquitard compaction.
