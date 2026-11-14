# NASA Space Apps Project Page Draft (`Q11`)

> **Status:** Ready-to-paste English draft aligned with the official Space Apps project submission form fields. Quantitative Central Valley, Karapınar, and UK Fens metrics come directly from repository data files (`data/central_valley/summary.json`, `web3d/surfaces.json`, `data/uk/meta.json`); bracketed URLs (`{...}`) mark public deployment and demo links to populate after final publishing.

---

## Project Title

**Under the Cloud, Beneath the Crops: Tracking Silent Land Subsidence with NASA–ISRO NISAR**

---

## High-Level Project Summary

Over-pumped aquifers, draining lowland peats, shrinking clays, and dissolving karst bedrock cause the ground to sink quietly beneath cities, aqueducts, levees, and farms—often under persistent cloud cover that blinds optical satellites. Our team pairs NASA–ISRO **NISAR L-band Synthetic Aperture Radar (24 cm wavelength)** imagery and Level-2 interferometric displacement (**GUNW**) with peer-reviewed geological benchmarks and an interactive web explorer + educational simulation to turn millimeter-to-centimeter radar phase shifts into actionable local hazard awareness across three flagship regions: the **UK Fens**, **California's Central Valley & Delta**, and **Konya–Karapınar, Türkiye**.

---

## Link to Final Project

- **Source Code & Data Repository:** https://github.com/keremsumer2010-tech/aseltech  
- **Live Interactive Web App / 3D Viewer:** `{PUBLIC_GITHUB_PAGES_URL}` *(verify incognito/unauthenticated public access before submission)*

---

## Link to Project "Demo"

`{PUBLIC_DEMO_LINK_30S_VIDEO_OR_7_SLIDES}`  
*(Must not exceed 30 seconds video or 7 slides.)*

---

## Detailed Project Description

### The Problem
Ground subsidence rarely arrives like an earthquake, yet its cumulative toll rivals major rapid disasters:
- **Agricultural Peat Drainage (UK Fens & Sacramento Delta):** Draining organic peatlands exposes ancient carbon to oxygen, shrinking the land surface over decades. At **Holme Fen (Cambridgeshire)**, an iron gauge driven in **1851** now stands **approximately 4 metres** above ground, leaving the reserve **2.75 metres below sea level** (Britain's lowest land point), while contemporary arable fenland sinks **1–2 cm/yr**. In California's **Sacramento–San Joaquin Delta**, peat oxidation at **1–3 inches/yr** has dropped central islands **10 to nearly 25 feet** below sea level behind **more than 1,100 miles** of levees—triggering roughly **100 levee failures** since the **1890s** and threatening freshwater exports serving **over 20 million** residents.
- **Groundwater Over-Draft (California San Joaquin Valley):** Pumping from aquifers below confining clay beds caused up to **8.5 meters (28 feet)** of compaction since the **1920s**, up to **0.6 meters (2 feet) per year** during drought peaks near Chowchilla and Corcoran, and reduced freeboard and flow capacity along a **145-kilometer** stretch of the California Aqueduct.
- **Sudden Karst Collapse (Konya–Karapınar, Türkiye):** Groundwater decline in soluble carbonate strata has accelerated catastrophic sinkhole (*obruk*) formation—with **104** sinkholes documented across Konya Province (**86** in Karapınar district, **43** recent collapses during **1972–2014**), reaching **80 m** deep (**Akviran Obruğu**) and **76 m** deep (**Yarımoğlu Obruğu**).
- **Urban Soil Shrink–Swell (Great Britain):** Moisture-driven clay shrinkage and swelling in the **upper two metres** of soil is Britain's most damaging geohazard, costing **£540 million** after the **1991** drought and spiking **350%** to **£64 million** across **>10,000** household insurance claims in a single dry quarter (**July–September 2018**).

### What Our Solution Does
Our web experience guides decision-makers and citizens through four synchronized interactive scenes plus a serious game:
1. **Seeing Through Clouds (UK Fens Comparison):** A side-by-side interactive swipe comparing an optical **VIIRS SNPP** true-color capture on **2026-10-20** (almost completely obscured by cloud cover) against a **same-day NISAR L-band GCOV radar preview**, proving all-weather imaging of The Wash coastline and Fens drainage geometry.
2. **Reading Millimeter-Scale Ground Motion (California Central Valley):** An interactive MapLibre time-series map showing cumulative NISAR Level-2 **GUNW** Line-of-Sight (LOS) displacement across irrigated agricultural bowls, paired with borehole-style location hydrographs.
3. **Infrastructure Under Quiet Strain (Aqueducts, Levees & Shrink–Swell):** Contextualizes millimeter-to-centimeter radar deformation gradients against aqueduct freeboard limits, Delta levee stability, and urban shallow-foundation risk.
4. **Mapping Active Sinkhole Clusters (Karapınar, Konya):** Overlays **29 field-verified sinkhole coordinates** (from peer-reviewed Turkish geographical surveys strictly within the regional radar swath) onto NISAR InSAR displacement tiles, with clickable depth, diameter, formation year, and source links.
5. **Interactive Simulator Mini-Game:** Translates physical aquifer drawdown, peat oxidation, and infrastructure strain into an accessible resource-management game grounded in measured Central Valley subsidence metrics.
6. **3D "Breathing Earth" Surface Explorer (`web3d/`):** Renders time-interpolated Three.js 3D displacement surfaces with interactive vertical exaggeration (`10,000×–150,000×`), epoch animation across the summer 2026 San Joaquin Valley stack, and 3D depth columns (`0.5–80 m`) for the 29 mapped Karapınar sinkholes.

### Quantitative Results & Calibration Transparency
*(All quantitative InSAR numbers come strictly from NISAR **Provisional** Level-2 `GUNW` collections acquired on or after **2026-06-17**, while same-day UK Fens GCOV browse imagery is strictly labeled **`preview`**).*

| Site / Metric | Value | Period / Maturity | Source |
|---|---|---|---|
| **Central Valley 7-Pair Cumulative Stack (`summary.json` & `web3d/surfaces.json`)** | Peak 1 km block median `−7.8 cm` LOS (`−10.1 cm` vert. est. at `39.1°` inc., `6 km N of Terra Bella`); linear irrigation-season estimate `−26.4 cm/yr` *(overstates net annual rate)*; stack percentiles p2 `−5.83`, p50 `−0.51`, p98 `+3.26` cm LOS (`62.9%` valid) | `2026-06-28` to `2026-10-14` (`108` days, `7` pairs, `provisional`, `P05023`, iono + plane + DEM deramp) | `data/central_valley/summary.json`, `web3d/surfaces.json` |
| **Karapınar 12-Day Checkpoint (`λ = 0.24393 m`)** | With iono screen + deramp: p2 `−2.12`, median `−0.78`, p98 `+0.79` cm LOS (`41.3%` valid); unscreened check: p2 `−2.81`, median `−0.67`, p98 `+2.43` cm | `2026-09-18` to `2026-09-30` (`provisional`, `P05023`) | `web3d/surfaces.json`, `status/PC3.md` |
| **UK Fens All-Weather Optical vs. Radar Pair** | 98%+ cloud optical vs. 100% valid radar preview (`700×500`) | `2026-10-20` (`preview`, `P05023`) | `data/uk/meta.json` |
| **Verified Karapınar Sinkhole Inventory** | 29 mapped inside `[33.3, 37.6, 33.8, 37.9]` (from 104 regional inventory) | Field surveys (`1972–2014`) | `data/karapinar/sinkholes.geojson` |

### How We Built It
- **Data Acquisition & Processing (Python):** Queried ASF Search API & NASA Earthdata (`earthaccess` / `.netrc`) for NISAR L2 GUNW (`unwrappedPhase`, `coherenceMagnitude`, `connectedComponents`, ionosphere screen, per-granule `centerFrequency`) and GCOV browse imagery; converted phase to LOS displacement via $\Delta r_{\text{LOS}} = -\frac{\lambda}{4\pi}\Delta\phi$ with `RdBu` symmetric color ramps and `connectedComponents != 0` masking (`analysis/insar.py`, `cumulative.py`).
- **Front-End & 3D Visualization:** Lightweight static HTML/CSS/JavaScript with **MapLibre GL**, synchronized optical-vs-radar split slider, **Three.js (`0.160.0`)** 3D surface explorer (`web3d/`), GeoJSON sinkhole popups, and responsive educational game canvas.
- **Verification & Data Contracts:** Cross-team JSON/GeoJSON/PNG contracts (`rules/VERI_SOZLESMESI.md`), automated pytest checks on phase-conversion physics, visual shoreline registration verification, and programmatic HTTP-200 link verification on all cited literature and API endpoints.

---

## Space Agency Data

- **NASA–ISRO NISAR Level-2 Geocoded Unwrapped Interferogram (`GUNW`, Provisional `CRID P05023`):** Used for L-band interferometric displacement time series and spatial uncertainty masking ([ASF GUNW User Guide](https://nisar-docs.asf.alaska.edu/gunw)).
- **NASA–ISRO NISAR Level-2 Geocoded Polarimetric Covariance (`GCOV`, Provisional `CRID P05023` browse preview):** Used for same-day cloud-penetrating radar preview in eastern England ([ASF Products Overview](https://nisar-docs.asf.alaska.edu/products-overview/)).
- **NASA GIBS / Worldview Snapshots API (`VIIRS_SNPP_CorrectedReflectance_TrueColor`):** Used for unauthenticated true-color optical comparison over the UK Fens on `2026-10-20`.
- **Mandatory Attribution & Limitations:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.* Because GUNW `unwrappedPhase` files do not subtract ionospheric, tropospheric, or solid-Earth-tide correction layers by default, single 12-day interferograms retain broad atmospheric/ionospheric ramps and unwrapping edge artifacts, mitigated via temporal stacking and spatial deramping where multi-pair stacks exist.

---

## Hackathon Journey

Working as a coordinated multi-workstation team, we split ownership cleanly into orbital search & HDF5 subsetting, InSAR phase inversion & testing, literature & ground-truth curation, frontend storytelling, and quality assurance. One key challenge was handling early NISAR product maturity differences safely: pre-`2026-06-17` BETA acquisitions carry mask-offset and radiometric-banding caveats, so we strictly excluded `beta-precal` scenes from quantitative claims and anchored every quantitative chart to uniform `2026-06-17+` Provisional collections while communicating NISAR project provenance clearly.

---

## AI & Tool Disclosure

In line with open scientific transparency and competition integrity rules:
- **Visual Media:** Seven illustrative scene graphics/banners in `web/assets/` (`hero.jpg`, `fens_ai.jpg`, `holme_ai.jpg`, `canal_ai.jpg`, `sinkhole_aerial_ai.jpg`, `obruk_ai.jpg`, `game_valley_ai.jpg`) and `hero.mp4` were created using **Higgsfield AI** and are explicitly labeled `"AI-generated illustration"` in the interface—never represented as real NASA imagery or measurements. No official NASA/ISRO logos are used in application UI.
- **Software & Documentation Support:** AI coding and research assistants (Claude Code, Codex, and Antigravity) assisted with Python InSAR utility scaffolding, unit tests, coordinate extraction verification from published tables, and documentation drafting. Every numerical claim, URL, coordinate, and unit conversion was independently verified by team members against primary source PDFs, ASF API responses, and automated tests.

---

## References

- **NISAR Mission Overview (NASA Science):** https://science.nasa.gov/mission/nisar/
- **NISAR Products Overview (ASF Data User Guide):** https://nisar-docs.asf.alaska.edu/products-overview/
- **NISAR Provisional Known Issues (ASF):** https://nisar-docs.asf.alaska.edu/provisional-known-issues/
- **NISAR Pre-Calibration Known Issues (ASF):** https://nisar-docs.asf.alaska.edu/product-known-issues/
- **NISAR L2 GUNW Product Documentation (ASF):** https://nisar-docs.asf.alaska.edu/gunw
- **Holme Fen Posts (The Great Fen):** https://www.greatfen.org.uk/about-great-fen/heritage/holme-fen-posts
- **Holme Fen (Wikipedia):** https://en.wikipedia.org/wiki/Holme_Fen
- **Lowland Peatlands Policy Briefing Note WP2 (CEH / Defra SP1218):** https://lowlandpeat.ceh.ac.uk/sites/default/files/2022-07/Policy-brief-note-WP2.pdf
- **San Joaquin Valley is Still Sinking (NASA Earth Observatory):** https://earthobservatory.nasa.gov/images/89761/san-joaquin-valley-is-still-sinking
- **USGS SIR 2018-5144 (California Aqueduct Subsidence):** https://pubs.usgs.gov/publication/sir20185144
- **USGS Fact Sheet 005-00 (Sacramento–San Joaquin Delta Subsidence):** https://pubs.usgs.gov/publication/fs00500
- **Tapur & Bozyiğit (2015), Current Sinkholes Formations in Konya Province:** https://dergipark.org.tr/tr/download/article-file/3454
- **Tapur & Bozyiğit (2016), Tourism Potential of Sinkholes in Konya Province:** https://dergipark.org.tr/tr/download/article-file/227372
- **Swelling and Shrinking Soils (British Geological Survey):** https://www.bgs.ac.uk/geology-projects/shallow-geohazards/clay-shrink-swell/
- **BGS GeoSure Shrink–Swell Dataset:** https://www.bgs.ac.uk/datasets/bgs-geosure-shrink-swell/
