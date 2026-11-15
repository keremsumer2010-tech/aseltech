# NASA Space Apps 2026 — Copy-Paste Submission Form (`docs/story/submission_form.md`)

**Owner:** PC8 (`M3hmeT1888`) · **Challenge:** *Dancing with the SARs* · **Local event:** Cambridge, MA (virtual) · **Submission deadline:** 15 Nov 2026, 23:59 EST  
**Compliance:** Every field below is written in plain English following [`docs/REVIEW_1500.md`](../REVIEW_1500.md) (zero banned buzzwords, zero emojis, zero exclamation marks, dated and unit-labelled measurements, explicit `provisional` / `preview` / `mixed` / `estimate` tags, and mandatory NISAR calibration notice). Every number cites its exact repository source file (`data/*/summary.json`, `validation.json`, `assets.json`, `exposure.json`, `detection.json`, `decomp.json`, `cross_sensor.json`, `polarizations.json`, `drivers.json`).

---

## 1. Project Title
*(Portal limit: typically ≤ 60–80 characters)*

- **Short Title (`49 chars` / `7 words`):**
```text
NISAR Vision: Tracking Land Subsidence from Space
```

- **Full Descriptive Title (`80 chars` / `13 words`):**
```text
NISAR Vision — Follow the Water: Tracking Silent Land Subsidence with L-Band SAR
```

---

## 2. High-Level Project Summary (Short Description)
*(Portal limit: 150-character ultra-short version and 500-character standard summary box)*

- **Ultra-Short Version (`141 chars` / `23 words` — fits 150-char limit):**
```text
A self-checking global subsidence atlas from NISAR radar: 20 basins, one open pipeline, the same 93 days, every number traceable to its file.
```

- **Standard Portal Summary (`282 chars` / `46 words` — fits 500-char limit, verbatim One-Sentence Core):**
```text
We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: 20 basins measured with one open pipeline on the same 93 days, every number traceable to its file, and every headline checked against GPS, NASA's OPERA product and the literature.
```

---

## 3. Link to Final Project & Repository
*(Must be public and require no login or permission)*

- **Live Interactive Application (`web/`, `web/explorer.html`, `game/`, `web3d/`):**
```text
https://keremsumer2010-tech.github.io/aseltech/
```

- **Public GitHub Source Code & Data Repository:**
```text
https://github.com/keremsumer2010-tech/aseltech
```

---

## 4. Link to Project "Demo"
*(Strictly ONE public link: ≤ 7-slide English presentation OR ≤ 30.0-second video with English subtitles. See [`docs/story/slides_notes.md`](slides_notes.md) for slide-by-slide presenter notes and captions.)*

- **Primary Demo Link — 7-Slide English Browser Deck (`≤ 7 slides`, printable to PDF):**
```text
https://keremsumer2010-tech.github.io/aseltech/docs/story/slides.html
```

- **Overview Video (Cambridge, MA Virtual Judges — `≤ 3 min`, 1080p MP4 with English subtitles):**
```text
https://keremsumer2010-tech.github.io/aseltech/docs/story/media/nisar_vision_overview.mp4
```

---

## 5. Detailed Project Description (`6,774 chars` / `983 words` — Source-Tagged)

```text
WHAT WE BUILT AND WHY IT MATTERS
We used NASA-ISRO's new NISAR radar satellite to measure where the ground is sinking in 29 places, and built checks that catch our own mistakes. Local event: Cambridge, MA (virtual). Across the United States and worldwide, when groundwater is pumped faster than rain refills it or organic peatlands are drained, deep clay and peat layers compact and the ground sinks silently by inches per season (1 in = 2.54 cm). In our 2026 global NISAR radar atlas, the fastest reliable basin is #1 Eloy, Arizona at -8.6 cm/100d (-3.4 in/100d), and 4 of our 15 reliable basins are in the United States: Eloy (Arizona), Central Valley (California, -7.3 cm/100d / -2.9 in/100d), Houston (Texas), and Sacramento-San Joaquin Delta (California). NASA's NISAR Land Subsidence StoryMap (Peacock et al., 2024) illustrated this hazard in California using 2013-2017 airborne UAVSAR radar. Our project, NISAR Vision - Follow the Water, updates that story from space in 2026 using open NASA-ISRO NISAR L-band Synthetic Aperture Radar (24 cm / 9.4 in wavelength) across the US, Turkiye, the UK, and a 29-basin global atlas.

KEY QUANTITATIVE FINDINGS (DATES, UNITS & REPO SOURCES)
1. UK Fens All-Weather & Polarization (28 Jul-20 Oct 2026, preview & provisional): A swipe comparison of cloudy VIIRS SNPP optical imagery (over 98% cloud on 20 Oct 2026) against a same-day NISAR L2 GCOV radar preview resolves The Wash coastline and Fens drainage [data/uk/meta.json], anchored by the Holme Fen iron post (~4 m peat loss since 1851; 1-2 cm/yr modern rate [docs/story/holme_fen.md]). Across 8 provisional GCOV epochs and 4 sample windows, mean temporal range is 4.27 dB in HH, 3.49 dB in HV, and 1.36 dB in HV/HH ratio, showing HV is the clearest vegetation-structure indicator [data/fens/polarizations.json; docs/story/polarization.md].
2. California Central Valley & Delta (28 Jun-14 Oct 2026, 7 provisional pairs, 108 days): Peak 1-km block-median subsidence reaches -7.8 cm (-3.1 in) LOS (3-reference spread -7.8 to -4.7 cm; -10.1 cm / -4.0 in vertical estimate at 39.1 deg, 6 km N of Terra Bella) [data/central_valley/summary.json], with 1,578.27 km2 sinking > 2 cm (> 0.8 in) LOS and 239.54 km2 > 5 cm (> 2.0 in) LOS [data/central_valley/area_stats.json]. An experimental 11-month mixed chain (24 Nov 2025-14 Oct 2026, 18 beta-precal + 7 provisional pairs) separates -16.77 +/- 2.24 cm/yr (-6.6 in/yr) LOS permanent compaction from an 11.67 cm (4.6 in) peak-to-peak seasonal rebound near Earlimart [data/central_valley_fullyear/decomp.json]. Integrating permanent vertical compaction across 4,508.3 km2 (> 1 cm/yr) yields an estimated 0.3174 km3/yr permanent aquifer storage-capacity loss (0.066-0.320 km3/yr 3-ref range; ~0.49x Millerton Lake) [data/central_valley_fullyear/storage_loss.json]. In the Sacramento-San Joaquin Delta (17 Jun-15 Oct 2026, 9 pairs), basin peak is -1.3 cm (-0.5 in) LOS (-1.6 cm vertical est.), while levee alignments reach -3.48 cm (-1.4 in) at the 10th percentile and -11.36 cm (-4.5 in) locally [data/delta/summary.json; docs/story/delta.md].
3. Konya Closed Basin & Karapinar, Turkiye (26 Jun-12 Oct 2026, 8 provisional pairs, 108 days): Across the full Konya Plain, subsidence peaks at -9.6 cm (-3.8 in) LOS (-14.0 to -9.6 cm across 3 references; -12.1 cm / -4.8 in vertical estimate at 37.6 deg) south of Konya city [data/konya_plain/summary.json]. In Karapinar, Track 7 peaks at -5.9 cm (-2.3 in) LOS (-8.0 cm vertical est.) [data/karapinar/summary.json], cross-checked by ascending Track 172 (-4.73 cm LOS at p01; 12-point r = 0.767, RMSE = 1.12 cm LOS) [analysis/pc8/kp_p7_vs_p172.json]. Valid pixels within 1 km of 29 verified sinkholes sink 6.4x faster (-4.15 cm LOS) than background plateau (> 5 km: -0.65 cm LOS) [data/karapinar/assets.json].
4. 2026 Global Subsidence Atlas & Population Exposure (2026-06-28 to 2026-09-29, 93-day common window, provisional): One open pipeline (pipeline/nisarvision) measures 20 basins on the same 93 days; 9 pass quality control and 11 are indicative only. Reliable ranking: 1 Eloy (-8.6 cm/100d), 2 Central Valley (Tulare Basin) (-7.3 cm/100d), 3 Mexico City (-6.3 cm/100d), 4 Semarang (-6.1 cm/100d), 5 Houston (-4.9 cm/100d) [data/global/atlas.json]. Automated time-series checks (tools/atlas_qc.py) caught a full 12.1 cm phase-cycle jump in Semarang (-12.1 to -6.2 cm after correction) and moved Tehran from -3.5 to -7.4 cm LOS with an off-basin reference [data/global/atlas_changelog.json]; indicative-only basins include Delhi, Beijing, Bangkok, Pekalongan, Konya Plain, Tehran, Jakarta, Yunlin, Hanoi, Ho Chi Minh City. Intersecting GHSL GHS-POP E2025 (100 m) with displacement above each city's 2-sigma noise floor shows 348.96 km2 sinking faster than -5 cm per 108 days, with 369,770 residents (4,652,365 below -2 cm), excluding nested Karapinar [data/global/exposure_atlas.json; data/global/vital_signs.json]. Secondary OPERA check: over Mexico City the spatial pattern matches NASA JPL's OPERA product at 10 points (r = 0.912), although OPERA covers winter and NISAR summer, while in the Central Valley and at Eloy agreement is weak (r = 0.40 and 0.09) because seasons and viewing geometry differ [data/global/opera_check.json]. (Independent primary validation against 10 continuous California GNSS stations is detailed in Section 6 below).
5. UK London Clay Detection Limit (21 Jun-19 Oct 2026, 9 provisional pairs, 120 days): Single-season 1-km block noise (1.21 cm 1-sigma, 3.62 cm 3-sigma) exceeds expected 0.5-2.0 cm seasonal clay motion, placing London below single-season detection limit [data/uk_clay/detection.json; docs/story/uk_findings.md].
6. Human & Crop Exposure: Using WorldPop 100 m (2020), an estimated 71,701 Central Valley residents and 69,854 Konya Closed Basin residents (including 11,572 in Karapinar) live on pixels subsiding > 2 cm LOS (3,407 and 16,822 on > 5 cm LOS) [data/*/exposure.json]. USDA CDL 30 m shows 79.2% (1,251.4 km2) of California's > 2 cm LOS zone is cultivated cropland, led by citrus (355.6 km2) and pistachios (230.9 km2); ESA WorldCover 10 m maps Konya Closed Basin's exposed grassland (284.9 km2), cropland (173.1 km2 coherent; 1,167.7 km2 interpolated), and built-up fabric (40.7 km2) [docs/story/exposure.md].
7. Operational Early-Warning Bulletins (v2.0): `tools/bulletin.py` generates A4-printable NASA Disasters-style HTML monitoring packages (`docs/bulletins/<region>.html` and `docs/bulletins/index.html`) directly from `data/global/atlas.json` and `data/global/exposure_atlas.json`, reporting Product ID, UTC issue time, `cm/100d` rate, top 3 subsiding areas, GHSL affected population, infrastructure tilt risk, GNSS comparison, 3 "What This Means" bullets, and mandatory calibration notices.

CALIBRATION NOTICE
NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.
```

---

## 6. How It Works (`1,956 chars` / `256 words`)

```text
1. HDF5 Subsetting & Phase-to-Centimeter Pipeline (Python):
We query the ASF Search API for NISAR Level-2 Geocoded Unwrapped Interferogram (GUNW) and Geocoded Polarimetric Covariance (GCOV) granules (CRID P05023). For each consecutive 12-to-24-day GUNW pair, our pipeline reads unwrappedPhase, coherenceMagnitude, connectedComponents, and the split-spectrum ionospheric phase screen on its native 80 m UTM grid. We convert unwrapped phase (radians) to line-of-sight displacement (cm) via dr_LOS = -(wavelength / 4*pi) * dphi using each granule's centerFrequency (1.229 GHz, wavelength = 24.39 cm), mask pixels where coherence < 0.30 or connectedComponents == 0, subtract the ionosphere screen and a planar/topographic ramp, reference each pair to a stable high-coherence bedrock window, and accumulate gap-free displacement chains.

2. Independent Validation (GNSS, Dual-Orbit & Multi-Sensor):
In California, vertical estimates (LOS / cos(incidence)) match 10 Nevada Geodetic Laboratory GPS stations at r = 0.924 cross-station agreement and 1.00 cm median RMSE (0.82 cm across 5 central Tulare stations) [data/central_valley/validation.json; data/central_valley_s1/cross_sensor.json]. Dual-orbit cross-checks compare Track 34 vs. Track 114 in California (6,719 1-km blocks, 85% sign agreement for |d| > 3 cm; -7.2 cm vertical at Alpaugh [data/central_valley/vertical.json]) and Track 7 vs. Track 172 in Karapinar. Across 25 Central Valley pairs, L-band NISAR retains 80.4% valid summer cropland coherence where shorter 5.55 cm C-band Sentinel-1 waves wrap > 2.77 cm in single 12-24 day steps [docs/story/cross_sensor.md].

3. Interactive Web Platform & Operational Bulletins:
Static JSON/PNG outputs drive a MapLibre GL story map (web/), multi-region explorer (web/explorer.html), Three.js 3D surface viewer (web3d/), 24-month Terzaghi aquifer simulator (game/), and printable regional monitoring bulletins (`tools/bulletin.py` -> `docs/bulletins/*.html`).
```

---

## 7. Benefits & Impact (`1,243 chars` / `164 words`)

```text
- Water & Infrastructure Managers: Our OpenStreetMap differential tilt index evaluates 645 canal, road, and rail corridors in the Central Valley and flags 81 high-risk segments (> 10 mm/km tilt), led by the Tulare Irrigation District Canal (57.01 mm/km) and a 102.8 km reach of the California Aqueduct (49.12 mm/km) [data/central_valley/assets.json]. A +/-25% threshold sensitivity test confirms the top-10 priority ranking is 100% invariant [docs/story/risk_sensitivity.md]. In the Sacramento-San Joaquin Delta, levee-aligned sampling prioritizes embankment segments up to -11.36 cm LOS for inspection [docs/story/delta.md].
- Agricultural Communities & Planners in Konya-Karapinar: Mapping basin-wide drawdown (-9.6 cm LOS south of Konya; -5.9 cm LOS in Karapinar) alongside 29 verified karst sinkholes highlights highway corridors up to 19.74 mm/km tilt (route 42-42) [data/karapinar/assets.json], without falsely claiming to predict sudden roof-collapse dates.
- Educators, Students & Citizens: Plain-English cards, physical scale rulers (>= 2.4 cm above noise), a classroom lesson plan [docs/story/lesson_plan.md], and the 24-month Valley Under Pressure simulator turn multi-gigabyte HDF5 radar files into accessible groundwater literacy.
```

---

## 8. Space Agency Data Used (`1,559 chars` / `216 words`)

```text
1. NASA-ISRO NISAR Level-2 Geocoded Unwrapped Interferogram (GUNW, Provisional CRID P05023, NASA Earthdata / ASF DAAC):
- California Central Valley: 7 provisional pairs Track 34 Asc (2026-06-28 to 2026-10-14), 6 provisional pairs Track 114 Desc (2026-06-21 to 2026-10-19), and 18 pre-calibration beta pairs (2025-11-24 to 2026-06-28, stored separately as quality: mixed in data/central_valley_fullyear/).
- Sacramento-San Joaquin Delta: 9 provisional pairs Track 42 Desc (2026-06-17 to 2026-10-15).
- Konya Basin & Karapinar, Turkiye: 8 provisional pairs Track 7 Desc and 8 provisional pairs Track 172 Asc (2026-06-26 to 2026-10-12).
- Greater London, UK: 9 provisional pairs Track 101 Asc (2026-06-21 to 2026-10-19).
- Global atlas (20 basins, common window 2026-06-28 to 2026-09-29): provisional GUNW pairs per basin are listed in data/global/<id>/meta.json and data/global/atlas.json; examples include Mexico City (Track 113 Desc), Tehran (Track 56 Asc) and Jakarta (Track 18 Desc).

2. NASA-ISRO NISAR Level-2 Geocoded Polarimetric Covariance (GCOV, Provisional CRID P05023, ASF DAAC):
- Eastern England / UK Fens: 2026-10-20 radar preview (data/uk/) and 8-epoch HH/HV agricultural time series (2026-07-28 to 2026-10-20, data/fens/polarizations.json).

3. NASA GIBS / Worldview Snapshots API (VIIRS SNPP True Color, 2026-10-20 UK Fens), NASA NISAR L3 Soil Moisture (SME2, Central Valley & Karapinar drivers), and NASA JPL OPERA DISP-S1 (OPERA_L3_DISP-S1_V1) Sentinel-1 displacement used as an independent cross-check in Mexico City and the Central Valley.
```

---

## 9. Other Non-Space-Agency Data Used (`1,091 chars` / `171 words`)

```text
- Nevada Geodetic Laboratory (NGL, University of Nevada, Reno): Daily continuous GPS vertical time series (IGS20/NA reference frame) at 10 stations in the San Joaquin Valley (CAHA, CAFP, HANF, P566, P056, P564, P565, CAD1, QCAP, TLBN).
- OpenStreetMap (ODbL): Canal, aqueduct, levee, highway, and railway vector geometries in California (645 evaluated segments), the Delta (87 levee points), and Karapinar, Turkiye (77 evaluated segments), plus settlement names.
- GHSL GHS-POP E2025 R2023A (European Commission JRC, 100 m, CC BY 4.0): population on sinking ground for the global atlas.
- Copernicus DEM GLO-90 (ESA): 90 m digital elevation model used for topographic phase ramp checks.
- WorldPop Open Population Data (100 m gridded population, 2020, CC BY 4.0), USDA NASS Cropland Data Layer (30 m, 2021, Public Domain), and ESA WorldCover 10 m v200 (2021, CC BY 4.0) for population and crop exposure analysis.
- Published Karapinar sinkhole coordinates (29 verified collapses, Tapur & Bozyigit 2015, 2016; Orhan et al. 2021) and UK Holme Fen peat loss records (Great Fen Project / UKCEH).
```

---

## 10. Tools, Coding Languages, Hardware & Software (`660 chars` / `83 words`)

```text
- Languages: Python 3.11, JavaScript (ES6+), HTML5, CSS3.
- Scientific Python Stack: NumPy, SciPy, h5py, Matplotlib, Pillow, PyProj, Rasterio, Requests, asf_search, pytest (automated unit tests for phase-to-cm conversion, coherence masking, reference subtraction, cross-sensor metrics, and seasonal decomposition).
- Web & 3D Visualization: MapLibre GL JS (2D interactive displacement maps, multi-region explorer, and GeoJSON overlays), Three.js v0.160.0 (web3d/ interactive 3D displacement mesh and sinkhole depth columns), HTML5 Canvas (charts and 24-month aquifer simulator).
- Workflow & Hosting: Git, GitHub, GitHub Pages (static zero-backend deployment).
```

---

## 11. Project Development & Technical Challenges (`1,198 chars` / `159 words`)

```text
We organized our team into parallel tracks governed by a strict JSON/PNG data contract (rules/VERI_SOZLESMESI.md): HDF5 subsetting, InSAR phase inversion, GPS/literature validation, infrastructure risk and game simulation, frontend integration, and continuous QA.

Three technical challenges shaped our design:
1. Product Maturity Separation: NISAR scenes acquired before 17 June 2026 belong to the pre-calibration beta phase (beta-precal) and carry known radiometric and mask caveats. We isolated all headline summer metrics to post-17 June 2026 provisional scenes (CRID P05023) and placed the 11-month beta+provisional decomposition in a separate mixed dataset with explicit visual warnings.
2. Atmospheric Noise vs. Real Deformation: Over Greater London, single-pair tropospheric delay (0.31-0.47 cm 1-km block std per pair; 1.21 cm cumulative 1-sigma across 9 pairs) exceeded expected 0.5-2.0 cm clay motion. Reporting a rigorous "below single-season detection limit" result strengthened our scientific credibility.
3. Multi-Geometry Verification: Comparing ascending and descending tracks in both California and Karapinar allowed us to separate vertical subsidence from orbital edge gradients.
```

---

## 12. AI Usage Disclosure (`669 chars` / `98 words`)

```text
- Visuals, Maps & Charts: Zero AI-generated images are used in our website or interactive game (early draft Higgsfield visuals were removed). Every displacement map, chart, GPS comparison, and infrastructure risk profile is rendered strictly from real satellite, GNSS, and open geospatial data.
- Code & Writing Assistance: Code, analysis scripts, and documentation drafts were written with assistance from Anthropic Claude (Claude Code), Google Gemini (Antigravity, Gemini CLI), and OpenAI Codex, and reviewed and verified by the team. Every reported number comes directly from checked repository data files, and every scientific claim is linked to its primary source.
```

---

## 13. References (`2,607 chars` / `268 words` — Copy-Paste List for Portal References Box)

```text
1. NASA-ISRO NISAR Mission & Applications White Papers: https://science.nasa.gov/mission/nisar/ and https://science.nasa.gov/mission/nisar/societal-benefits/
2. Peacock, A., An, K., Pinto, N., & Lou, Y. (2024). NISAR ArcGIS StoryMaps (Land Subsidence): https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828 (https://doi.org/10.5281/zenodo.10818833)
3. NISAR Data User Guide & GUNW/GCOV Product Specifications (ASF DAAC): https://nisar-docs.asf.alaska.edu/gunw and https://nisar-docs.asf.alaska.edu/provisional-known-issues/
4. Neely, W. R., Borsa, A. A., Burney, J. A., Levy, M. C., Silverii, F., & Sneed, M. (2021). Characterization of groundwater recharge and flow in California's San Joaquin Valley from InSAR and GPS. Water Resources Research, 57(4), e2020WR028451: https://pmc.ncbi.nlm.nih.gov/articles/PMC8047915/
5. Ojha, C., Werth, S., & Shirzaei, M. (2019). Groundwater loss and aquifer system compaction in San Joaquin Valley during 2012-2015 drought. JGR Solid Earth, 124, 3127-3143: https://pmc.ncbi.nlm.nih.gov/articles/PMC6559157/
6. USGS Scientific Investigations Report 2018-5144 (Land Subsidence Along the California Aqueduct) and Fact Sheet 005-00 (Sacramento-San Joaquin Delta): https://pubs.usgs.gov/publication/sir20185144 and https://pubs.usgs.gov/publication/fs00500
7. Orhan, O., Oliver-Cabrera, T., Wdowinski, S., Yalvac, S., & Yakar, M. (2021). Land subsidence and its relations with sinkhole activity in Karapinar region, Turkey. Sensors, 21(3), 774: https://pmc.ncbi.nlm.nih.gov/articles/PMC7865528/
8. Tapur, T., & Bozyigit, R. (2015). Current sinkhole formations in Konya Province. Marmara Cografya Dergisi, 31, 415-441: https://dergipark.org.tr/tr/download/article-file/3454
9. Great Fen Project — Holme Fen Posts & UKCEH Lowland Peatlands WP2 Briefing: https://www.greatfen.org.uk/about-great-fen/heritage/holme-fen-posts and https://lowlandpeat.ceh.ac.uk/sites/default/files/2022-07/Policy-brief-note-WP2.pdf
10. British Geological Survey — Swelling and Shrinking Soils (London Clay): https://www.bgs.ac.uk/geology-projects/shallow-geohazards/clay-shrink-swell/
11. Haghighi, M. H., & Motagh, M. (2024) (Tehran subsidence, PMC11086625) & Abidin, H. Z. et al. (2015) (Jakarta subsidence, PIAHS 372:115): https://pmc.ncbi.nlm.nih.gov/articles/PMC11086625/ and https://piahs.copernicus.org/articles/372/115/2015/
12. Nevada Geodetic Laboratory (NGL) GPS Networks, OpenStreetMap Contributors (ODbL), WorldPop (CC BY 4.0, DOI: 10.5258/SOTON/WP00645), USDA NASS Cropland Data Layer (Public Domain), and ESA WorldCover 10 m (CC BY 4.0, DOI: 10.5281/zenodo.7254221).
```
