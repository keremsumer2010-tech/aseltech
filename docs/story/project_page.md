# NASA Space Apps Project Page

> **Status:** Verified ready-to-paste English submission text aligned with the official Space Apps project submission form fields (`Q11`). All Central Valley, Karapınar, and UK metrics resolve directly from committed repository datasets (`data/central_valley/*.json`, `data/karapinar/*.json`, `data/uk/meta.json`, `data/uk_clay/detection.json`, `web3d/surfaces.json`), cross-linked with [`docs/story/sinkhole_timeline.md`](sinkhole_timeline.md), [`docs/story/judge_faq.md`](judge_faq.md), [`docs/story/slides.html`](slides.html), [`docs/story/video_shotlist.md`](video_shotlist.md), and [`docs/story/media/demo_30s.mp4`](media/demo_30s.mp4).

---

## Project Title

**NISAR Pulse — Follow the Water: Tracking Silent Land Subsidence with NASA–ISRO NISAR**

---

## High-Level Project Summary

Over-pumped aquifers, draining lowland peats, shrinking clays, and dissolving karst bedrock cause the ground to sink quietly beneath cities, aqueducts, levees, and farms—often under persistent cloud cover that blinds optical satellites. Our team pairs NASA–ISRO **NISAR L-band Synthetic Aperture Radar (24 cm wavelength)** imagery and Level-2 interferometric displacement (**GUNW**) with independent continuous GPS ground truth, OpenStreetMap infrastructure tilt indexing, peer-reviewed sinkhole inventories, a 3D surface explorer, and a physics-based water-policy simulator (**Valley Under Pressure**) to turn millimeter-to-centimeter radar phase shifts into plain-English water intelligence across three flagship regions: the **UK Fens**, **California's Central Valley & Delta**, and **Konya–Karapınar, Türkiye**.

---

## Link to Final Project

- **Source Code & Data Repository:** https://github.com/keremsumer2010-tech/aseltech  
- **Live Interactive Web App (`web/`, `game/`, `web3d/`):** https://keremsumer2010-tech.github.io/aseltech/ *(verify incognito/unauthenticated public access and latest workflow deployment before submission)*

---

## Link to Project "Demo"

`{PUBLIC_DEMO_LINK_30S_VIDEO_OR_7_SLIDES}` *(See 30-second capture guide & `.srt` in [`docs/story/video_shotlist.md`](video_shotlist.md) or deployable 7-slide deck at [`docs/story/slides.html`](slides.html) — `https://keremsumer2010-tech.github.io/aseltech/docs/story/slides.html`)*  
*(Must not exceed 30 seconds video or 7 slides.)*

---

## Detailed Project Description

### The Problem
Ground subsidence rarely arrives like an earthquake, yet its cumulative toll rivals major rapid disasters:
- **Agricultural Peat Drainage (UK Fens & Sacramento Delta):** Draining organic peatlands exposes ancient carbon to oxygen, shrinking the land surface over decades. At **Holme Fen (Cambridgeshire)**, an iron gauge driven in **1851** now stands **approximately 4 metres** above ground, leaving the reserve **2.75 metres below sea level** (Britain's lowest land point), while contemporary arable fenland sinks **1–2 cm/yr**. In California's **Sacramento–San Joaquin Delta**, peat oxidation at **1–3 inches/yr** has dropped central islands **10 to nearly 25 feet** below sea level behind **more than 1,100 miles** of levees—triggering roughly **100 levee failures** since the **1890s** and threatening freshwater exports serving **over 20 million** residents.
- **Groundwater Over-Draft & Canal Loss (California San Joaquin Valley):** Pumping from aquifers below confining clay beds caused up to **8.5 meters (28 feet)** of compaction since the **1920s**, up to **0.6 meters (2 feet) per year** during drought peaks near Chowchilla and Corcoran, reduced freeboard along a **145-kilometer** stretch of the California Aqueduct, and dropped **152-mile Friant-Kern Canal** capacity by about **60 percent** (**4,000 → 1,600 cfs**) across a **25-mile** reach with deepest sinking near **Terra Bella** (~$400 million estimated full-canal adjustment).
- **Sudden Karst Collapse (Konya–Karapınar, Türkiye):** Groundwater decline in soluble carbonate strata has accelerated catastrophic sinkhole (*obruk*) formation—with **104** sinkholes documented across Konya Province (**86** in Karapınar district, **43** recent collapses during **1972–2014**; **`24` of `29` verified frame collapses (`82.8%`) occurred in `2007–2013`**, see [`docs/story/sinkhole_timeline.md`](sinkhole_timeline.md)), reaching **80 m** deep (**Akviran Obruğu**) and **76 m** deep (**Yarımoğlu Obruğu**).
- **Urban Soil Shrink–Swell (Great Britain):** Moisture-driven clay shrinkage and swelling in the **upper two metres** of soil is Britain's most damaging geohazard, costing **£540 million** after the **1991** drought and spiking **350%** to **£64 million** across **>10,000** household insurance claims in a single dry quarter (**July–September 2018**).

### What Our Solution Does
Our multi-page web platform (`web/`: Story Map, `science.html`, `data.html`, `faq.html`, plus `web3d/` and `game/`) guides citizens and planners through six synchronized evidence chapters and two interactive tools:
1. **Seeing Through Clouds (UK Fens Comparison):** A side-by-side interactive swipe comparing an optical **VIIRS SNPP** true-color capture on **2026-10-20** (~98% cloud obscured) against a **same-day NISAR L-band GCOV radar preview**, proving all-weather imaging of The Wash coastline and Fens drainage geometry alongside the verified **Holme Fen** benchmark (`nearly 4 metres` exposed since `1851`).
2. **Reading Millimeter-Scale Ground Motion (California Central Valley):** An interactive MapLibre time-series map showing cumulative NISAR Level-2 **GUNW** Line-of-Sight (LOS) displacement across **8** epochs (**7** consecutive `12–24`-day pairs, `2026-06-28 → 2026-10-14`), paired with click-to-inspect borehole hydrographs and plain-English sentences.
3. **Checking Ground Truth, Dual-Orbit Geometry & Infrastructure Strain (`GNSS` + `Q21/Q22` + `assets.json`):** Validates NISAR vertical projections against **10 continuous NGL GPS stations** (cross-station final **`r = 0.924`**, `1.37 cm` final RMSE; moving `|GPS|max > 2 cm` `n = 5` median **`0.834 cm` RMSE / `r = 0.820`**, interior `n = 4` median **`0.800 cm`** / `0.76 cm` final RMSE / `r = 0.793–0.896`, [`validation_report.md`](validation_report.md)), cross-checks ascending **Track 34** against independent descending **Track 114** across **`6,719` 1 km blocks** (**`r = 0.489`**, `RMSE = 2.65 cm`, `median diff = −1.29 cm`, slope `0.514`, **`85%` sign agreement** where `|d| > 3 cm`, local `< 15 km` `r = 0.60`), solves two-geometry vertical + east-west inversion (**Alpaugh / Earlimart bowl `−7.2 cm` vertical, `−0.1 cm` east-west**, max `−9.8 cm` vertical, `data/central_valley/vertical.json`), and flags **81 high-risk segments** out of **645** OSM corridors (`Tulare Irrigation District Canal` **`57.01 mm/km`**, `California Aqueduct` **`49.12 mm/km`**, [`risk_dossier.md`](risk_dossier.md))—with `±25%` threshold sensitivity tests (`72–115` high-risk count) confirming the **top-10 priority ranking is 100% invariant** ([`risk_sensitivity.md`](risk_sensitivity.md)).
4. **Mapping Active Sinkhole Clusters (Karapınar, Konya):** Overlays **29 field-verified sinkhole coordinates** (strictly inside `[33.3, 37.6, 33.8, 37.9]`, analyzed chronologically in [`docs/story/sinkhole_timeline.md`](sinkhole_timeline.md)) onto our **8-pair** NISAR Track 7 displacement stack (`−5.9 cm` LOS peak `2 km W of Karapınar`).
5. **Interactive Simulator — *Valley Under Pressure* (`game/index.html`):** A **24-month** Terzaghi / USGS skeletal-storage compaction model across **7** Tulare Basin districts calibrated directly to NISAR's Terra Bella summer subsidence measurement (`−7.8 cm` LOS / `−10.1 cm` vertical est. at demand multiplier `k = 0.6232`, `b0 · S_skv ≈ 0.02356`; `N = 1,000` Monte Carlo trials yield `108`-day `p10–p90` `−13.69` to `−4.12 cm` and `24`-month stochastic `p10–p90` `−27.10` to `−6.23 cm` around `−18.69 cm` nominal, [`game_sensitivity.md`](game_sensitivity.md)), exposing irreversible permanent clay collapse and Friant-Kern-scale canal loss when over-pumping drops groundwater head below preconsolidation threshold *h<sub>pc</sub>*.
6. **3D "Breathing Earth" Surface Explorer (`web3d/`):** Renders time-interpolated Three.js 3D displacement surfaces with interactive vertical exaggeration (`10,000×–150,000×`), epoch animation across both the Central Valley (`80×96`) and Karapınar (`48×80`) stacks, and 3D depth columns (`0.5–80 m`) for all `29` verified Karapınar sinkholes.

### Quantitative Results & Calibration Transparency
*(All quantitative InSAR numbers come strictly from NISAR **Provisional** Level-2 `GUNW` collections acquired on or after **2026-06-17**, while same-day UK Fens GCOV browse imagery is strictly labeled **`preview`**).*

| Site / Metric | Value | Period / Maturity | Source |
|---|---|---|---|
| **Central Valley 7-Pair Cumulative Stack (`summary.json`, `area_stats.json` & `web3d/surfaces.json`)** | Peak 1 km block median `−7.8 cm` LOS (3-reference spread **`−7.8` to `−4.7 cm`**; `−10.1 cm` vert. est. at `39.1°` inc., `6 km N of Terra Bella`); linear 108-day estimate `−26.4 cm/yr` *(overstates net annual rate)*; common-valid-pixel footprint (`1,203,856 px = 7,704.68 km²`, `area_stats.json`): **`239.54 km² <= −5 cm`** & **`1,578.27 km² <= −2 cm`** LOS (`1,661.49 km²` peak on `2026-09-20`; vs. `258.7 / 1,673.9 km²` single-epoch cumulative mask in `summary.json`, `62.9%` valid); `drivers.json` moisture coupling **`r = 0.654`** (`irrigation_index`, `p_perm = 0.088`) & **`r = 0.638`** (12-day lagged `SME2` soil moisture, `p_perm = 0.130`)—non-significant at `α = 0.05` over `N = 8` epochs (`\|r_crit\| = 0.707–0.754`; detrended `Δd/Δt` rate `r = 0.037–0.130`, `p >= 0.81`, `drivers_analysis.md`); Cramér-Rao phase sigma median **`0.294 cm`** (`L = 208`) | `2026-06-28` to `2026-10-14` (`108` days, `7` pairs, `provisional`, `P05023`, iono + plane + DEM deramp) | `data/central_valley/summary.json`, `data/central_valley/area_stats.json`, `data/central_valley/drivers.json`, `docs/story/drivers_analysis.md`, `data/central_valley/uncertainty/meta.json`, `web3d/surfaces.json` |
| **Karapınar 8-Pair Cumulative Stack (`summary.json`, `area_stats.json` & `web3d/surfaces.json`)** | Peak 1 km block median `−5.9 cm` LOS (`−8.0 cm` vert. est. at `41.9°–42.0°` inc., `2 km W of Karapınar`); linear 108-day estimate `−20.0 cm/yr`; common-valid-pixel footprint (`33,169 px = 212.28 km²`, `area_stats.json`): **`3.10 km² <= −5 cm`** & **`28.66 km² <= −2 cm`** LOS (vs. `3.1 / 49.1 km²` single-epoch cumulative mask in `summary.json`, `14.2%` valid across 8 pairs); Cramér-Rao phase sigma median **`0.326 cm`** (`L = 208`) | `2026-06-26` to `2026-10-12` (`108` days, `8` pairs, `provisional`, `P05023`, iono + plane + DEM deramp) | `data/karapinar/summary.json`, `data/karapinar/area_stats.json`, `data/karapinar/uncertainty/meta.json`, `web3d/surfaces.json` |
| **Central Valley Continuous GNSS Validation (`validation.json`)** | **10** NGL `IGS20/NA` stations vs. NISAR vertical (`LOS / cos θ`): **cross-station final `r = 0.924`** (`1.37 cm` final RMSE), **1.00 cm median RMSE** (`1.33 cm` mean TS RMSE; moving `\|GPS\|max > 2 cm` `n = 5` median **`0.834 cm`** / `r = 0.820`; interior `n = 4` median **`0.800 cm`** / final **`0.76 cm`** / TS `r = 0.851`; stable `n = 5` median **`1.570 cm`**; best `0.64 cm` at `P566`), peak `r = 0.90` at `CAHA` & `HANF` | `2026-06-28` to `2026-10-14` (`provisional`) | `data/central_valley/validation.json`, `docs/story/key_findings.md`, `docs/story/validation_report.md`, `docs/story/uncertainty.md` |
| **Dual-Orbit Cross-Check (`Q21`) & Vertical Inversion (`Q22`)** | **Track 34 Asc. ↔ Track 114 Desc.** (`6,719` 1 km blocks): **`r = 0.489`** (`0.60` local `< 15 km`), **`RMSE = 2.65 cm`**, **`median diff = −1.29 cm`**, slope `0.514`, **`85%` sign agreement** (`\|d\| > 3 cm`, `n = 1,297`), `−5.7 cm` T114 median where T34 `< −6 cm`; **2-geometry inversion:** **Alpaugh bowl `−7.2 cm` vertical (`−0.1 cm` east)**, max block `−9.8 cm` up (`+2.4 cm` east), `up_cm` p2 `−5.98`, p50 `−1.25`, p98 `+2.35` cm (`49.6%` overlap) | `2026-06-28` to `2026-10-14` (`provisional`) | `analysis/out/cv_p34_vs_p114.json`, `data/central_valley/vertical.json`, `docs/qa/PC3.md` |
| **Infrastructure Differential Tilt Index & `±25%` Sensitivity** | **645** OSM corridors evaluated (`3,238` total): **81 high-risk** (`12.6%`); steepest slope **`57.01 mm/km`** on `Tulare Irrigation District Canal` (`2.17 km`) and **`49.12 mm/km`** over `102.8 km` of `California Aqueduct`; `±25%` threshold sensitivity shifts high-risk count (`72–115`) while **top-10 priority ranking stays 100% invariant** | `2026-06-28` to `2026-10-14` (`provisional`, OSM ODbL) | `data/central_valley/assets.json`, `docs/story/risk_sensitivity.md` |
| **UK Fens All-Weather Optical vs. Radar Pair** | 98%+ cloud optical vs. 100% valid radar preview (`700×500`) | `2026-10-20` (`preview`, `P05023`) | `data/uk/meta.json` |
| **UK London Clay 9-Pair Detection Test (`Q09`)** | **`status: "below_detection"`** — `chain_sigma = 1.21 cm`, `3σ threshold = 3.62 cm`; after quadratic atmosphere removal **`97.7%` of `1 km` blocks lie within `±1.5 cm`** (`p2/p50/p98 = −1.47 / +0.19 / +1.26 cm`, `0` interior blocks detected; raw `-5.29 cm` at `2.0 km` from scene boundary is an atmospheric edge artifact—confirming `<= 1 cm` seasonal clay shrink–swell lies below single-season noise) | `2026-06-21` to `2026-10-19` (`120` days, `9` pairs, Track 101 Asc., `provisional`, `P05023`) | `data/uk_clay/detection.json`, `docs/qa/PC3.md` |
| **Verified Karapınar Sinkhole Inventory, Ring Risk & Spatial Significance (`assets.json` & `sinkhole_stats.md`)** | **29** verified sinkholes inside `[33.3, 37.6, 33.8, 37.9]`; **`0–1 km` ring mean `−4.152 cm` LOS** (`6.4×` vs `>5 km` `−0.647 cm`; `Köken Obruğu-I` `−4.71 cm`); **`0–2 km` belt (`n = 236` px, `16` coherent sinkholes) `−4.06 cm`** vs `>5 km` `−0.65 cm` (`−3.41 cm` diff); **`1.04 km` block permutation `p = 0.0001`** (`−3.04 cm` diff, Welch `p = 9.7 × 10⁻⁸`) & **`3,423` rigid `29`-sinkhole constellation shifts `p = 0.0207`**; **10 high-risk highways** (`42-42` `19.74 mm/km`, `597.3 m` from `Köken Obruğu-II`) | Field surveys (`1972–2013`) & NISAR (`provisional`) | `data/karapinar/sinkholes.geojson`, `data/karapinar/assets.json`, `docs/story/sinkhole_stats.md` |

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

## Development Process and Technical Challenges

Working as a coordinated multi-workstation team, we split ownership cleanly into orbital search & HDF5 subsetting, InSAR phase inversion & testing, literature & ground-truth curation, frontend storytelling, and quality assurance. One key challenge was handling early NISAR product maturity differences safely: pre-`2026-06-17` BETA acquisitions carry mask-offset and radiometric-banding caveats, so we strictly excluded `beta-precal` scenes from quantitative claims and anchored every quantitative chart to uniform `2026-06-17+` Provisional collections while communicating NISAR project provenance clearly.

---

## AI & Tool Disclosure

In line with open scientific transparency and competition integrity rules:
- **Visual Media:** Zero AI-generated images appear in the live website, slide deck, simulator, 3D explorer, or video. All seven early placeholder illustrations in `web/assets/` were removed in commit `38b774f`, leaving only a real screenshot (`web/assets/simulator.jpg`), alongside live NISAR MapLibre displacement maps, real satellite/GPS PNG plots (`docs/story/media/`), and custom physics SVG schematics directly from measured NISAR, GPS, and survey datasets.
- **Software & Documentation Support:** AI coding and research assistants (Claude Code, Gemini / Antigravity) assisted with Python InSAR utility scaffolding, unit tests, coordinate extraction verification from published tables, and documentation drafting (`docs/story/judge_faq.md`, `docs/story/sources.md`). Every numerical claim, URL, coordinate, and unit conversion was independently verified by team members against primary source PDFs, ASF API responses, and automated tests.

---

## Companion Submission Package (`docs/story/`)

- [`docs/story/presentation_cues.md`](presentation_cues.md) & [`docs/story/rehearsal_checklist.md`](rehearsal_checklist.md) — 3-minute Lincoln live presentation cue sheet (`6 × 30 s` blocks aligned to live site sections + top 5 Q&As) and offline/rehearsal backup checklist (`python3 -m http.server 8000`, tab order, MP4/slides fallbacks).
- [`docs/story/slides.html`](slides.html) — Interactive `7`-slide browser deck using real NISAR/VIIRS maps and inline data charts (`38b774f` zero-AI policy).
- [`docs/story/video_shotlist.md`](video_shotlist.md) & [`docs/story/media/demo_30s.mp4`](media/demo_30s.mp4) — `30.0`-second capture shotlist (`Shot 1–6`), line-verified `video_30s.srt` subtitles, and rendered `29.62 s` 1080p MP4 demo video (`analysis/pc6/make_demo_video.py`).
- [`docs/story/judge_faq.md`](judge_faq.md) — `15`-question technical Jury Q&A card rendered live in [`web/faq.html`](../../web/faq.html).
- [`docs/story/sinkhole_timeline.md`](sinkhole_timeline.md) — Chronology and groundwater-driver synthesis across all `29` verified Karapınar sinkholes (`1972–2013`).
- [`docs/story/holme_fen.md`](holme_fen.md) — Verified Holme Fen single-sentence website copy (`1851` post, `~4 m`, `2.75 m` below sea level).
- [`docs/story/calibration_note.md`](calibration_note.md) & [`docs/story/submission_rules.md`](submission_rules.md) — NISAR BETA/PROVISIONAL/VALIDATED rules & Space Apps compliance checks.
- [`docs/story/uncertainty.md`](uncertainty.md) & `data/*/uncertainty/sigma_cm.png` — Pair-chain error budget (`0.66 cm` local RMS, `SNR 2.7×–4.5×`) & per-pixel Cramér-Rao formal phase uncertainty (`0.294 cm` CV, `0.326 cm` Karapınar).
- [`docs/story/validation_report.md`](validation_report.md), [`docs/story/risk_dossier.md`](risk_dossier.md), [`docs/story/key_findings.md`](key_findings.md), [`docs/story/key_findings_public.md`](key_findings_public.md), [`docs/story/sinkhole_stats.md`](sinkhole_stats.md), [`docs/story/drivers_analysis.md`](drivers_analysis.md), [`docs/story/fullyear.md`](fullyear.md), [`docs/story/literature_comparison.md`](literature_comparison.md), [`docs/story/risk_sensitivity.md`](risk_sensitivity.md), & [`docs/story/game_sensitivity.md`](game_sensitivity.md) — 10-station GNSS scatter & traces (`r = 0.924`), public takeaway summary, Karapınar `1.04 km` block-permutation (`p = 0.0001`) & rigid `29`-sinkhole constellation shift tests (`p = 0.0207`), `N = 8` soil-moisture/irrigation statistical caveats (`p_perm = 0.088/0.130`), 11-month Earlimart seasonal-vs-permanent decomposition (`-16.8 cm/yr` perm vs `11.7 cm` seasonal), Top-10 infrastructure corridor profiles (`±25%` rank-invariant), peer-reviewed rate comparison, and `N = 1,000` Monte Carlo simulator calibration (`game_sensitivity.png`).
- `docs/story/media/` — Real-data 1080p demo and subsidence animations ([`demo_30s.mp4`](media/demo_30s.mp4), [`cv_subsidence.mp4`](media/cv_subsidence.mp4), [`kp_subsidence.mp4`](media/kp_subsidence.mp4)), affected-area time series ([`pc5_area_cv.png`](media/pc5_area_cv.png)), Karapınar sinkhole permutation & bootstrap distribution ([`pc5_sinkhole_perm.png`](media/pc5_sinkhole_perm.png)), Central Valley moisture drivers ([`pc5_drivers.png`](media/pc5_drivers.png)), 11-month Earlimart time series ([`pc9_fullyear_point.png`](media/pc9_fullyear_point.png)), GNSS plots (`validation_scatter.png`, `gnss_*.png`), and corridor profile charts (`risk_1..10.png`).

---

## References

- **Neely et al. (2021), *Water Resources Research* 57(4):e2020WR028451 (Central Valley Sentinel-1 InSAR & cGPS):** https://pmc.ncbi.nlm.nih.gov/articles/PMC8047915/
- **Ojha, Werth & Shirzaei (2019), *JGR Solid Earth* 124:3127–3143 (San Joaquin Valley ALOS/Sentinel-1 InSAR):** https://pmc.ncbi.nlm.nih.gov/articles/PMC6559157/
- **Orhan et al. (2021), *Sensors* 21(3):774 (Karapınar SBAS-InSAR & cGNSS):** https://pmc.ncbi.nlm.nih.gov/articles/PMC7865528/
- **Üstün, Tuşat & Yalvaç (2010), *NHESS* 10:1151–1164 (Konya Closed Basin GNSS):** https://nhess.copernicus.org/articles/10/1151/2010/
- **Canaslan Çomut et al. (2015), *ISPRS Archives* XL-1/W5:115–119 (Konya Basin Multi-Band InSAR):** https://isprs-archives.copernicus.org/articles/XL-1-W5/115/2015/
- **Friant-Kern Canal Slows By 60 Percent, Subsidence To Blame — KVPR (Ezra David Romero, Aug 3, 2017):** https://www.kvpr.org/environment/2017-08-03/friant-kern-canal-slows-by-60-percent-subsidence-to-blame
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
