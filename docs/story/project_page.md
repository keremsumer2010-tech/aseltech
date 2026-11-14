# NASA Space Apps Project Page Draft (`Q11`)

> **Status:** Ready-to-paste English draft aligned with the official Space Apps project submission form fields (`Q11` + final `ZAMAN_CIZELGESI` Sunday QA). Quantitative Central Valley, Karapınar, and UK Fens metrics come directly from repository data files (`data/central_valley/*.json`, `data/karapinar/*.json`, `web3d/surfaces.json`, `data/uk/meta.json`), linked cleanly with [`docs/story/sinkhole_timeline.md`](sinkhole_timeline.md), [`docs/story/judge_faq.md`](judge_faq.md), [`docs/story/slides.html`](slides.html), and [`docs/story/video_shotlist.md`](video_shotlist.md). Bracketed tokens (`{...}`) mark live verification placeholders before final submission.

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
3. **Checking Ground Truth, Dual-Orbit Geometry & Infrastructure Strain (`GNSS` + `Q21/Q22` + `assets.json`):** Validates NISAR vertical projections against **10 continuous NGL GPS stations** (cross-station final **`r = 0.924`**, `1.37 cm` final RMSE; moving `|GPS| > 2 cm` `n = 4` final RMSE **`0.76 cm`** / mean TS `r = 0.851`; median RMSE **`1.00 cm`**, active-basin 5-station mean **`0.86 cm`** / `r = 0.81`, [`validation_report.md`](validation_report.md)), cross-checks ascending **Track 34** against independent descending **Track 114** across **`6,719` 1 km blocks** (**`r = 0.489`**, `RMSE = 2.65 cm`, `median diff = −1.29 cm`, slope `0.514`, **`85%` sign agreement** where `|d| > 3 cm`, local `< 15 km` `r = 0.60`), solves two-geometry vertical + east-west inversion (**Alpaugh / Earlimart bowl `−7.2 cm` vertical, `−0.1 cm` east-west**, max `−9.8 cm` vertical, `data/central_valley/vertical.json`), and flags **81 high-risk segments** out of **645** OSM corridors (`Tulare Irrigation District Canal` **`57.01 mm/km`**, `California Aqueduct` **`49.12 mm/km`**, [`risk_dossier.md`](risk_dossier.md)).
4. **Mapping Active Sinkhole Clusters (Karapınar, Konya):** Overlays **29 field-verified sinkhole coordinates** (strictly inside `[33.3, 37.6, 33.8, 37.9]`, analyzed chronologically in [`docs/story/sinkhole_timeline.md`](sinkhole_timeline.md)) onto our **8-pair** NISAR Track 7 displacement stack (`−5.9 cm` LOS peak `2 km W of Karapınar`).
5. **Interactive Simulator — *Valley Under Pressure* (`game/index.html`):** A **24-month** Terzaghi / USGS skeletal-storage compaction model across **7** Tulare Basin districts calibrated directly to NISAR's Terra Bella summer subsidence measurement (`−7.8 cm` LOS / `−10.1 cm` vertical est.), exposing irreversible permanent clay collapse and Friant-Kern-scale canal loss when over-pumping drops groundwater head below preconsolidation threshold *h<sub>pc</sub>*.
6. **3D "Breathing Earth" Surface Explorer (`web3d/`):** Renders time-interpolated Three.js 3D displacement surfaces with interactive vertical exaggeration (`10,000×–150,000×`), epoch animation across both the Central Valley (`80×96`) and Karapınar (`48×80`) stacks, and 3D depth columns (`0.5–80 m`) for all `29` verified Karapınar sinkholes.

### Quantitative Results & Calibration Transparency
*(All quantitative InSAR numbers come strictly from NISAR **Provisional** Level-2 `GUNW` collections acquired on or after **2026-06-17**, while same-day UK Fens GCOV browse imagery is strictly labeled **`preview`**).*

| Site / Metric | Value | Period / Maturity | Source |
|---|---|---|---|
| **Central Valley 7-Pair Cumulative Stack (`summary.json` & `web3d/surfaces.json`)** | Peak 1 km block median `−7.8 cm` LOS (3-reference spread **`−7.8` to `−4.7 cm`**; `−10.1 cm` vert. est. at `39.1°` inc., `6 km N of Terra Bella`); linear 108-day estimate `−26.4 cm/yr` *(overstates net annual rate)*; stack percentiles p2 `−5.83`, p50 `−0.51`, p98 `+3.26` cm LOS (`62.9%` valid); Cramér-Rao phase sigma median **`0.294 cm`** (`L = 208`) | `2026-06-28` to `2026-10-14` (`108` days, `7` pairs, `provisional`, `P05023`, iono + plane + DEM deramp) | `data/central_valley/summary.json`, `data/central_valley/uncertainty/meta.json`, `web3d/surfaces.json` |
| **Karapınar 8-Pair Cumulative Stack (`summary.json` & `web3d/surfaces.json`)** | Peak 1 km block median `−5.9 cm` LOS (`−8.0 cm` vert. est. at `41.9°–42.0°` inc., `2 km W of Karapınar`); linear 108-day estimate `−20.0 cm/yr`; stack percentiles p2 `−4.18`, p50 `−0.65`, `p98` `+2.45` cm LOS (`14.2%` valid across all 8 pairs); Cramér-Rao phase sigma median **`0.326 cm`** (`L = 208`) | `2026-06-26` to `2026-10-12` (`108` days, `8` pairs, `provisional`, `P05023`, iono + plane + DEM deramp) | `data/karapinar/summary.json`, `data/karapinar/uncertainty/meta.json`, `web3d/surfaces.json` |
| **Central Valley Continuous GNSS Validation (`validation.json`)** | **10** NGL `IGS20/NA` stations vs. NISAR vertical (`LOS / cos θ`): **cross-station final `r = 0.924`** (`1.37 cm` final RMSE), **1.00 cm median RMSE** (`1.33 cm` mean TS RMSE; moving `\|GPS\| > 2 cm` `n = 4` final **`0.76 cm`** / TS `r = 0.851`; active 5-station mean **`0.86 cm`** / `r = 0.81`; best `0.64 cm` at `P566`), peak `r = 0.90` at `CAHA` & `HANF` | `2026-06-28` to `2026-10-14` (`provisional`) | `data/central_valley/validation.json`, `docs/story/validation_report.md`, `docs/story/uncertainty.md` |
| **Dual-Orbit Cross-Check (`Q21`) & Vertical Inversion (`Q22`)** | **Track 34 Asc. ↔ Track 114 Desc.** (`6,719` 1 km blocks): **`r = 0.489`** (`0.60` local `< 15 km`), **`RMSE = 2.65 cm`**, **`median diff = −1.29 cm`**, slope `0.514`, **`85%` sign agreement** (`\|d\| > 3 cm`, `n = 1,297`), `−5.7 cm` T114 median where T34 `< −6 cm`; **2-geometry inversion:** **Alpaugh bowl `−7.2 cm` vertical (`−0.1 cm` east)**, max block `−9.8 cm` up (`+2.4 cm` east), `up_cm` p2 `−5.98`, p50 `−1.25`, p98 `+2.35` cm (`49.6%` overlap) | `2026-06-28` to `2026-10-14` (`provisional`) | `analysis/out/cv_p34_vs_p114.json`, `data/central_valley/vertical.json`, `docs/qa/PC3.md` |
| **Infrastructure Differential Tilt Index (`assets.json`)** | **645** OSM corridors evaluated (`3,238` total): **81 high-risk** (`>10 mm/km`); steepest slope **`57.01 mm/km`** on `Tulare Irrigation District Canal` (`2.17 km`) and **`49.12 mm/km`** over `102.8 km` of `California Aqueduct` | `2026-06-28` to `2026-10-14` (`provisional`, OSM ODbL) | `data/central_valley/assets.json` |
| **UK Fens All-Weather Optical vs. Radar Pair** | 98%+ cloud optical vs. 100% valid radar preview (`700×500`) | `2026-10-20` (`preview`, `P05023`) | `data/uk/meta.json` |
| **Verified Karapınar Sinkhole Inventory & Ring Risk (`assets.json`)** | **29** verified sinkholes inside `[33.3, 37.6, 33.8, 37.9]`; **`0–1 km` ring mean `−4.152 cm` LOS** (`6.4×` vs `>5 km` background `−0.647 cm`); **10 high-risk highways** (`19.74 mm/km`, `597.3 m` from `Köken Obruğu-II`) | Field surveys (`1972–2013`) & NISAR (`provisional`) | `data/karapinar/sinkholes.geojson`, `data/karapinar/assets.json` |

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
- **Visual Media:** Seven illustrative scene graphics created earlier in `web/assets/` (Higgsfield AI, tagged `"AI-generated illustration"`) remain archived in the repository while Site v2 uses a live NISAR MapLibre displacement map for its hero background alongside custom physics SVG schematics; our 7-slide presentation (`docs/story/slides.html`) and v2 simulator (`game/index.html`) contain **zero AI artwork**.
- **Software & Documentation Support:** AI coding and research assistants (Claude Code, Gemini / Antigravity) assisted with Python InSAR utility scaffolding, unit tests, coordinate extraction verification from published tables, and documentation drafting (`docs/story/judge_faq.md`, `docs/story/sources.md`). Every numerical claim, URL, coordinate, and unit conversion was independently verified by team members against primary source PDFs, ASF API responses, and automated tests.

---

## Companion Submission Package (`docs/story/`)

- [`docs/story/slides.html`](slides.html) — Interactive `7`-slide browser deck using real NISAR/VIIRS maps and inline SVG charts (zero AI art).
- [`docs/story/video_shotlist.md`](video_shotlist.md) — `30.0`-second capture shotlist (`Shot 1–6`) and line-verified `video_30s.srt` subtitles.
- [`docs/story/judge_faq.md`](judge_faq.md) — `15`-question technical Jury Q&A card rendered live in [`web/faq.html`](../../web/faq.html).
- [`docs/story/sinkhole_timeline.md`](sinkhole_timeline.md) — Chronology and groundwater-driver synthesis across all `29` verified Karapınar sinkholes (`1972–2013`).
- [`docs/story/holme_fen.md`](holme_fen.md) — Verified Holme Fen single-sentence website copy (`1851` post, `~4 m`, `2.75 m` below sea level).
- [`docs/story/calibration_note.md`](calibration_note.md) & [`docs/story/submission_rules.md`](submission_rules.md) — NISAR BETA/PROVISIONAL/VALIDATED rules & Space Apps compliance checks.
- [`docs/story/uncertainty.md`](uncertainty.md) & `data/*/uncertainty/sigma_cm.png` — Pair-chain error budget (`0.66 cm` local RMS, `SNR 2.7×–4.5×`) & per-pixel Cramér-Rao formal phase uncertainty (`0.294 cm` CV, `0.326 cm` Karapınar).
- [`docs/story/validation_report.md`](validation_report.md), [`docs/story/risk_dossier.md`](risk_dossier.md), & [`docs/story/game_model.md`](game_model.md) — 10-station GNSS scatter & traces (`r = 0.924`), Top-10 infrastructure corridor profiles, and Terzaghi compaction physics documentation.
- `docs/story/media/` — Real-data 1080p subsidence animations ([`cv_subsidence.mp4`](media/cv_subsidence.mp4), [`kp_subsidence.mp4`](media/kp_subsidence.mp4)), GNSS plots (`validation_scatter.png`, `gnss_*.png`), and corridor profile charts (`risk_1..10.png`).

---

## References

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
