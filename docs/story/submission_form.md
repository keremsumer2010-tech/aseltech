# NASA Space Apps 2026 — Copy-Paste Submission Form (`docs/story/submission_form.md`)

**Owner:** PC8 (`M3hmeT1888`) · **Challenge:** *Dancing with the SARs*  
**Compliance:** Every field below is written in plain English following [`docs/REVIEW_1500.md`](../REVIEW_1500.md) (zero banned buzzwords, zero emojis, zero exclamation marks, dated and unit-labelled measurements, explicit `provisional` / `preview` / `mixed` / `estimate` tags, and mandatory NISAR calibration notice). All numbers trace directly to committed repository files (`data/*/summary.json`, `data/central_valley/validation.json`, `data/*/assets.json`, `data/uk_clay/detection.json`, `data/central_valley_fullyear/decomp.json`, `data/fens/crops.json`). Character and word counts are provided for every portal box.

---

## 1. Project Title
*(Portal limit: typically ≤ 60–80 characters)*

- **Short Title (`48 chars` / `8 words`):**
```text
NISAR Pulse: Tracking Land Subsidence from Space
```

- **Full Descriptive Title (`76 chars` / `11 words`):**
```text
NISAR Pulse — Follow the Water: Tracking Silent Land Subsidence with L-Band SAR
```

---

## 2. High-Level Project Summary (Short Description)
*(Portal limit: 150-character ultra-short version and 480-character standard summary box)*

- **Ultra-Short Version (`146 chars` / `23 words` — fits 150-char limit):**
```text
Open web platform using provisional NASA-ISRO NISAR L-band radar to map centimeter-scale land subsidence, canal tilt, and groundwater risk in 2026.
```

- **Standard Portal Summary (`469 chars` / `70 words` — fits 500-char limit):**
```text
NASA's NISAR Land Subsidence StoryMap showed California's sinking valley with 2013-2017 airborne radar. We measured the same valley and aqueduct from space in 2026 with provisional NASA-ISRO NISAR L-band radar (24 cm wavelength), validated results against 10 GPS stations (1.00 cm median RMSE), ranked 645 canal and road segments by tilt, compared Karapinar sinkholes in Turkiye and UK peat/clay limits, and built a 24-month groundwater simulator in an open web app.
```

---

## 3. Link to Final Project & Repository
*(Must be public and require no login or permission)*

- **Live Interactive Application (`web/`, `game/`, `web3d/`):**
```text
https://keremsumer2010-tech.github.io/aseltech/web/index.html
```

- **Public GitHub Source Code & Data Repository:**
```text
https://github.com/keremsumer2010-tech/aseltech
```

---

## 4. Link to Project Demo
*(Strictly ONE public link: either a ≤ 30.0-second video with English subtitles OR a ≤ 7-slide presentation in English)*

- **Option A — 30-Second Video (with embedded English subtitles `docs/story/video_subtitles.srt`):**
```text
https://github.com/keremsumer2010-tech/aseltech/raw/main/docs/story/media/demo_30s.mp4
```

- **Option B — 7-Slide English Browser Deck (fallback / companion link):**
```text
https://keremsumer2010-tech.github.io/aseltech/docs/story/slides.html
```

---

## 5. Detailed Project Description (`2,384 chars` / `348 words`)

```text
WHAT WE BUILT AND WHY IT MATTERS
When groundwater is pumped faster than rain refills it, or when organic peatlands are drained, deep clay and peat layers compact and the ground sinks by millimeters to centimeters per month. NASA's NISAR Land Subsidence StoryMap (Peacock et al., 2024) illustrated this hazard in California's Central Valley using 2013-2017 airborne UAVSAR radar. Our project, NISAR Pulse - Follow the Water, updates that story from space in 2026 using open NASA-ISRO NISAR L-band Synthetic Aperture Radar (24 cm wavelength) across three regions: California's Central Valley, Konya-Karapinar in Turkiye, and eastern England (the Fens and Greater London).

KEY QUANTITATIVE FINDINGS (ALL DATES AND UNITS EXPLICIT)
1. UK Fens All-Weather Imaging (20 Oct 2026, preview): A side-by-side comparison of VIIRS SNPP true-color optical imagery (over 98% cloud cover) and a same-day NISAR L2 GCOV radar preview resolves The Wash coastline and Fens drainage network through clouds, anchored by the Holme Fen iron post (~4 m peat loss since 1851; 1-2 cm/yr contemporary rate). Over 8 provisional GCOV epochs (28 Jul-20 Oct 2026), Fens cropland HV backscatter drops by -2.41 dB after late-summer harvest.
2. California Central Valley Subsidence (28 Jun-14 Oct 2026, 108 days, 7 provisional GUNW pairs): Cumulative line-of-sight (LOS) subsidence reaches -7.8 cm (range -4.7 to -7.8 cm across 3 reference windows; -10.1 cm vertical estimate at 39.1 deg incidence, 6 km N of Terra Bella). Across common valid pixels (7,704.68 km2), 1,578.27 km2 subsided more than 2 cm and 239.54 km2 subsided more than 5 cm. An experimental 11-month mixed chain (24 Nov 2025-14 Oct 2026, 18 beta-precal + 7 provisional pairs) separates -16.8 cm/yr LOS permanent compaction from an 11.7 cm peak-to-peak seasonal swing near Earlimart.
3. Karapinar Basin & Sinkholes, Turkiye (26 Jun-12 Oct 2026, 108 days, 8 provisional GUNW pairs): Cumulative subsidence reaches -5.9 cm LOS (-8.0 cm vertical estimate at 41.9 deg incidence, 2 km W of Karapinar), cross-checked against ascending Track 172 (-4.7 cm LOS at p01, 12-point r = 0.77, RMSE = 1.12 cm LOS). Valid pixels within 1 km of 29 field-verified sinkholes sink 6.4 times faster (-4.15 cm LOS) than background plateau areas beyond 5 km (-0.65 cm LOS).
4. UK London Clay Detection Limit (21 Jun-19 Oct 2026, 120 days, 9 provisional pairs): Expected seasonal clay shrink-swell (0.5-2.0 cm) lies below our measured single-season 1 km block noise floor (1.21 cm 1-sigma, 3.62 cm 3-sigma), demonstrating why multi-year NISAR time series are needed for sub-centimeter urban clay monitoring.

CALIBRATION NOTICE
NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.
```

---

## 6. How It Works (`1,492 chars` / `219 words`)

```text
1. HDF5 Subsetting & Phase-to-Centimeter Pipeline (Python):
We query the ASF Search API for NISAR Level-2 Geocoded Unwrapped Interferogram (GUNW) and Geocoded Polarimetric Covariance (GCOV) granules (CRID P05023). For each consecutive 12-to-24-day GUNW pair, our pipeline reads unwrappedPhase, coherenceMagnitude, connectedComponents, and the split-spectrum ionospheric phase screen on its native 80 m UTM grid. We convert unwrapped phase (radians) to line-of-sight displacement (cm) via dr_LOS = -(wavelength / 4*pi) * dphi using each granule's centerFrequency (1.229 GHz, wavelength = 24.39 cm), mask pixels where coherence < 0.30 or connectedComponents == 0, subtract the ionosphere screen and a planar/topographic ramp, reference each pair to a stable high-coherence bedrock window, and accumulate gap-free displacement chains.

2. Independent Validation (GNSS + Two-Orbit Cross-Check):
In California, we compare vertical estimates (LOS / cos(incidence)) against daily IGS20/NA positions at 10 Nevada Geodetic Laboratory GPS stations, achieving 1.00 cm median time-series RMSE (0.80 cm across 4 actively subsiding interior stations) and r = 0.924 cross-station agreement. We also cross-check ascending Track 34 against descending Track 114 across 6,719 1-km blocks (85% sign agreement for |d| > 3 cm) and decompose vertical (-7.2 cm at Alpaugh) versus east-west (-0.1 cm) motion.

3. Browser Story Map, 3D Surface Explorer & Policy Simulator:
Static JSON/PNG outputs power a MapLibre GL story map (web/), a Three.js 3D basin viewer (web3d/), and a 24-month Terzaghi aquifer compaction simulator (game/) running entirely in the browser.
```

---

## 7. Benefits & Impact (`1,068 chars` / `156 words`)

```text
- Water & Infrastructure Managers: Our OpenStreetMap differential tilt index evaluates 645 canal, road, and rail corridors in the Central Valley and identifies 81 high-risk segments (> 10 mm/km tilt), led by the Tulare Irrigation District Canal (57.01 mm/km) and a 102.8 km reach of the California Aqueduct (49.12 mm/km). A +/-25% threshold sensitivity test confirms the top-10 priority ranking is 100% invariant, helping engineers prioritize canal liner inspections before freeboard loss occurs.
- Agricultural Communities & Planners in Konya-Karapinar: Mapping regional groundwater subsidence bowls (-5.9 cm LOS in 108 days) alongside 29 verified karst sinkholes highlights where active drawdown and highway tilt (up to 19.74 mm/km along route 42-42) intersect, without falsely claiming to predict exact roof-collapse dates.
- Educators, Students & Citizens: Plain-English cards, coin-and-hand physical scale comparisons (>= 2.4 cm above noise), and the 24-month Valley Under Pressure simulator turn multi-gigabyte HDF5 radar files into an accessible tool for understanding irreversible clay compaction.
```

---

## 8. Space Agency Data Used (`1,089 chars` / `155 words`)

```text
1. NASA-ISRO NISAR Level-2 Geocoded Unwrapped Interferogram (GUNW, Provisional CRID P05023, accessed via NASA Earthdata / ASF DAAC):
- California Central Valley: 7 provisional pairs on Track 34 Ascending (2026-06-28 to 2026-10-14), 6 provisional pairs on Track 114 Descending (2026-06-21 to 2026-10-19), plus 18 pre-calibration beta pairs (2025-11-24 to 2026-06-28, stored separately as quality: mixed in data/central_valley_fullyear/).
- Karapinar, Konya, Turkiye: 8 provisional pairs on Track 7 Descending and 8 provisional pairs on Track 172 Ascending (2026-06-26 to 2026-10-12).
- Greater London, UK: 9 provisional pairs on Track 101 Ascending (2026-06-21 to 2026-10-19).

2. NASA-ISRO NISAR Level-2 Geocoded Polarimetric Covariance (GCOV, Provisional CRID P05023, ASF DAAC):
- Eastern England / UK Fens: 2026-10-20 all-weather radar browse preview (data/uk/) and 8-epoch dual-polarization (HHHH, HVHV) agricultural time series (2026-07-28 to 2026-10-20, data/fens/crops.json).

3. NASA GIBS / Worldview Snapshots API:
- VIIRS SNPP Corrected Reflectance True Color (2026-10-20 over the UK Fens, data/uk/optical.png).

4. NASA NISAR Level-2 Soil Moisture (SME2, Provisional, Central Valley driver comparison).
```

---

## 9. Other Non-Space-Agency Data Used (`748 chars` / `107 words`)

```text
- Nevada Geodetic Laboratory (NGL, University of Nevada, Reno): Daily continuous GPS vertical time series (IGS20/NA reference frame) at 10 stations in the San Joaquin Valley (CAHA, CAFP, HANF, P566, P056, P564, P565, CAD1, QCAP, TLBN).
- OpenStreetMap (ODbL): Canal, aqueduct, highway, and railway vector geometries in California (645 evaluated segments) and Karapinar, Turkiye (77 evaluated segments), plus settlement names for benchmark point labelling.
- Copernicus DEM GLO-90 (ESA): 90 m digital elevation model used for topographic phase ramp checks.
- WorldPop Open Population Data (100 m gridded population, CC BY 4.0), USDA NASS Cropland Data Layer (CropScape, public domain), and ESA WorldCover 10 m (CC BY 4.0) for population and crop exposure analysis.
- Published Karapinar sinkhole coordinates (29 verified collapses, Tapur & Bozyigit 2015, 2016; Orhan et al. 2021) and UK Holme Fen peat loss records (Great Fen Project / UKCEH).
```

---

## 10. Tools, Coding Languages, Hardware & Software (`634 chars` / `91 words`)

```text
- Languages: Python 3.11, JavaScript (ES6+), HTML5, CSS3.
- Scientific Python Stack: NumPy, SciPy, h5py, Matplotlib, Pillow, PyProj, Rasterio, Requests, asf_search, pytest (automated unit tests for phase-to-cm conversion, coherence masking, reference subtraction, and seasonal decomposition).
- Web & 3D Visualization: MapLibre GL JS (2D interactive displacement maps and GeoJSON overlays), Three.js v0.160.0 (web3d/ interactive 3D displacement mesh and sinkhole depth columns), HTML5 Canvas (charts and 24-month aquifer simulator).
- Workflow & Hosting: Git, GitHub, GitHub Pages (static zero-backend deployment).
```

---

## 11. Project Development & Technical Challenges (`962 chars` / `141 words`)

```text
We organized our team into parallel tracks governed by a strict JSON/PNG data contract (rules/VERI_SOZLESMESI.md): HDF5 subsetting, InSAR phase inversion, GPS/literature validation, infrastructure risk and game simulation, frontend integration, and continuous QA.

Three technical challenges shaped our design:
1. Product Maturity Separation: NISAR scenes acquired before 17 June 2026 belong to the pre-calibration beta phase (beta-precal) and carry known radiometric and mask caveats. We isolated all headline summer metrics to post-17 June 2026 provisional scenes (CRID P05023) and placed the 11-month beta+provisional decomposition in a separate mixed dataset with explicit visual warnings.
2. Atmospheric Noise vs. Real Deformation: Over Greater London, single-pair tropospheric delay (0.31-0.47 cm 1-km block std per pair; 1.21 cm cumulative 1-sigma across 9 pairs) exceeded expected 0.5-2.0 cm clay motion. Reporting a rigorous "below single-season detection limit" result strengthened our scientific credibility.
3. Multi-Geometry Verification: Comparing ascending and descending tracks in both California and Karapinar allowed us to separate vertical subsidence from orbital edge gradients.
```

---

## 12. AI Usage Disclosure (`692 chars` / `102 words`)

```text
- Data Maps, Charts & Simulator: Zero generative AI images are used in our scientific maps, charts, or active Site v2 interface. Every displacement raster, GPS trace, infrastructure profile, and 3D surface is rendered directly from measured NISAR, NGL GPS, OpenStreetMap, and survey data. (Earlier illustrative concept graphics archived in web/assets/ carry explicit "AI-generated illustration" labels per project rules.)
- Code & Documentation Assistance: Team members used Claude Code and Google Gemini / Antigravity to assist with Python InSAR script scaffolding, unit test generation, frontend layout refactoring, and English copy editing. Every formula, coordinate, numerical claim, and citation URL was verified against primary HDF5 granules, JSON outputs, and HTTP-200 source documents.
```

---

## 13. References (Copy-Paste List for Portal References Box)

```text
1. NASA-ISRO NISAR Mission & Applications White Papers: https://science.nasa.gov/mission/nisar/ and https://science.nasa.gov/mission/nisar/societal-benefits/
2. Peacock, A., An, K., Pinto, N., & Lou, Y. (2024). NISAR ArcGIS StoryMaps (Land Subsidence): https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828 (https://doi.org/10.5281/zenodo.10818833)
3. NISAR Data User Guide & GUNW/GCOV Product Specifications (ASF DAAC): https://nisar-docs.asf.alaska.edu/gunw and https://nisar-docs.asf.alaska.edu/provisional-known-issues/
4. Neely, W. R., Borsa, A. A., Burney, J. A., Levy, M. C., Silverii, F., & Sneed, M. (2021). Characterization of groundwater recharge and flow in California's San Joaquin Valley from InSAR and GPS. Water Resources Research, 57(4), e2020WR028451: https://pmc.ncbi.nlm.nih.gov/articles/PMC8047915/
5. Ojha, C., Werth, S., & Shirzaei, M. (2019). Groundwater loss and aquifer systemetic compaction in San Joaquin Valley during 2012-2015 drought. JGR Solid Earth, 124, 3127-3143: https://pmc.ncbi.nlm.nih.gov/articles/PMC6559157/
6. USGS Scientific Investigations Report 2018-5144 (Land Subsidence Along the California Aqueduct): https://pubs.usgs.gov/publication/sir20185144
7. USGS Fact Sheet 005-00 (Land Subsidence in the Sacramento-San Joaquin Delta): https://pubs.usgs.gov/publication/fs00500
8. Orhan, O., Oliver-Cabrera, T., Wdowinski, S., Yalvac, S., & Yakar, M. (2021). Land subsidence and its relations with sinkhole activity in Karapinar region, Turkey. Sensors, 21(3), 774: https://pmc.ncbi.nlm.nih.gov/articles/PMC7865528/
9. Tapur, T., & Bozyigit, R. (2015). Current sinkhole formations in Konya Province. Marmara Coğrafya Dergisi, 31, 415-441: https://dergipark.org.tr/tr/download/article-file/3454
10. Great Fen Project — Holme Fen Posts & UKCEH Lowland Peatlands WP2 Briefing: https://www.greatfen.org.uk/about-great-fen/heritage/holme-fen-posts and https://lowlandpeat.ceh.ac.uk/sites/default/files/2022-07/Policy-brief-note-WP2.pdf
11. British Geological Survey — Swelling and Shrinking Soils (London Clay): https://www.bgs.ac.uk/geology-projects/shallow-geohazards/clay-shrink-swell/
12. Nevada Geodetic Laboratory (NGL) GPS Networks, OpenStreetMap Contributors (ODbL), WorldPop (CC BY 4.0), USDA NASS Cropland Data Layer, and ESA WorldCover 10 m (CC BY 4.0).
```
