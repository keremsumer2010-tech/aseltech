# NISAR Pulse — 3-Minute Lincoln Presentation Cue Sheet (`docs/story/presentation_cues.md`)

> **Core Message (15 words):** *With NISAR's 24 cm L-band radar, we measure centimeter-scale ground sinking across aquifers and agricultural lands.*  
> **Target Rehearsal:** `17:30 TR` · **Duration:** `3:00` (`6 × 30 s` blocks) · **Live App:** https://keremsumer2010-tech.github.io/aseltech/  
> **Mandatory Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## Team Roles

| Role | Member | Responsibility During Live Pitch & Q&A |
|---|---|---|
| **Lead Speaker** | **Kerem** | Delivers the `6 × 30 s` plain-English narrative blocks (`0:00–3:00`) cleanly at ~135 wpm |
| **Live Demo Pilot** | **Memir** | Drives `Tab 1` (`web/index.html`), `Tab 2` (`explorer.html#central_valley_fullyear`), `Tab 3` (`game/index.html`), `Tab 4` (`web3d/index.html`) and executes `< 2 s` offline fallbacks (`Tab 5` `slides.html`, `demo_30s.mp4`) |
| **Technical Q&A & Timekeeper** | **Mehmet** | Runs silent stopwatch (`0:30` splits, **`2:30` simulator cue**, **`2:50 WRAP NOW`**) and answers jury questions on GUNW phase math, L-vs-C coherence, ionosphere/DEM deramp, 10-station GNSS agreement, dual-orbit Track 34/114, and 11-month decomposition |
| **Data, Impact & Policy Q&A Lead** | **İbrahim** | Answers jury questions on UK Fens `HH`/`HV` polarization & London clay `below_detection`, Karapınar 29 sinkholes & permutation tests, WorldPop/USDA exposure (`141,555` CV+Konya residents / `79.2%` CV cropland), Mexico City (`-4.4 cm` LOS), simulator priors, and verified sources (`sources.md`) |

---

## Pre-Flight Tab Layout (`T − 10 min`)

- **Tab 1:** `https://keremsumer2010-tech.github.io/aseltech/` (or `http://localhost:8000/web/index.html`) scrolled to top Hero (`#heroMap`)
- **Tab 2:** `explorer.html#central_valley_fullyear` pre-clicked near Earlimart (`7 km W of Earlimart`)
- **Tab 3:** `game/index.html` at `Month 0 of 24` with **Classroom Mode** open (`2. Multi-Year Drought` ready)
- **Tab 4:** `web3d/index.html` loaded with Central Valley / Karapınar 3D displacement mesh (`quality: provisional · CRID P05023`)
- **Tab 5 (Offline Backup):** `docs/story/slides.html` (`Slide 1`, arrow-key ready) + `docs/story/media/demo_30s.mp4` paused in VLC (`Alt+Tab`)

---

## 1. Six 30-Second Speaking & Demo Blocks (`0:00 – 3:00`)

### Block 1 (`0:00 – 0:30`) · Hook, Headline Numbers & 108 Days in Seconds
- **Speaker:** **Kerem**
- **Memir Clicks (`Tab 1: web/index.html`):**
  1. Start at Hero (`"The ground beneath our food is sinking."`, `#heroMap`), holding `4 s` on the four `.stats` headline cards (**`−7.8 cm`**, **`240 km²`**, **`1.0 cm`**, **`81 / 645`**).
  2. Scroll into `#watch` (*"108 days in seconds"* → `#cvVideo` Figure 0 muted loop) and click **`Story`** (`#story`) into Chapter 1 (`[data-step="intro"]`).
- **Kerem Says:**
  > Beneath the farms that feed us, heavy groundwater pumping is causing the land itself to sink quietly by centimetres in a single summer. Using open L-band radar from NASA–ISRO's NISAR satellite across 108 summer days in 2026, we measured up to minus 7.8 centimetres of sinking in California's Central Valley across 240 square kilometres, checked it within a 1.0-centimetre median difference against 10 GPS stations, and flagged 81 tilting canal and road sections out of 645.
- **Offline Fallback Cue (`Tab 5`):** `Slide 1` (`docs/story/slides.html`) or `demo_30s.mp4`.

### Block 2 (`0:30 – 1:00`) · Why 24 cm L-Band Sees Through Clouds, Crop Canopies & Honest Limits
- **Speaker:** **Kerem**
- **Memir Clicks (`Tab 1: web/index.html` `[data-step="uk"]`):**
  1. Drag `#compareRange` left-to-right across `#compare` (`20 Oct 2026`: ~98% cloud VIIRS optical vs. NISAR `GCOV` radar preview) while showing `#holmeText` (**nearly `4 m`** since `1851`, `2.75 m` below sea level).
  2. Hover `#polBox` / `#polChart` (`4` Fens crop areas, `22 Jun – 8 Oct 2026`, `HH` ~`7 dB` brighter than `HV`, `data/fens/crops.json`) and `#ukClay` (London clay `±3.6 cm` noise floor, honest `"below_detection"`).
- **Kerem Says:**
  > In England's Fens, draining peat since 1851 has lowered Holme Fen nearly 4 metres to 2.75 metres below sea level, yet clouds hide farmland all year—on 20 October 2026, NISAR's 24-centimetre radar sees straight through 98 percent cloud while separate HH and HV polarizations track crop structure and soil moisture across 4 fields. Unlike short-wavelength C-band radar, L-band keeps 80.4 percent valid summer coherence over dense crops, and in London's clay belt our 9-pair test honestly reports seasonal soil shrink–swell as not detected below the 3.6-centimetre summer noise limit.
- **Offline Fallback Cue (`Tab 5`):** `Slide 2` (`docs/story/slides.html`).

### Block 3 (`1:00 – 1:30`) · Central Valley Subsidence, Full-Year Rhythm, GPS Check & Canal Tilt
- **Speaker:** **Kerem**
- **Memir Clicks (`Tab 1` `[data-step="cv"]`, `[data-step="gnss"]`, `[data-step="risk"]` + optional 3 s flash to `Tab 2: explorer.html#central_valley_fullyear`):**
  1. Press `#cvPlay` (`#slider` `28 Jun – 14 Oct 2026`, `7` pairs), tap `p01` (`6 km N of Terra Bella`) for `#readout` + `#pointChart`, pause on `#fyBox` (*"A whole year: what comes back and what does not"* — Earlimart **`20.3 cm` lower**, **`16.8 cm/yr` permanent**, **`11.7 cm` seasonal**, `explorer.html#central_valley_fullyear`) and `aside.note.storymap` (*"From the air to space"* — `2013–2017 UAVSAR → 2026 NISAR`).
  2. Scroll to `[data-step="gnss"]` (click **`CAHA`** in `#gnssTable`, `#gnssChart`) and `[data-step="risk"]` (highlight **`Tulare Irrigation District Canal — 57 mm/km`** in `#riskList` / `.riskbars`).
- **Kerem Says:**
  > NASA's NISAR StoryMap tracked the Central Valley bowl from aircraft in 2013 to 2017; from space across 108 summer days in 2026, NISAR measures minus 7.8 centimetres line of sight—about 10.1 centimetres vertical estimate—near Terra Bella, across farmland housing over 71,000 residents and 79 percent high-value crops like citrus and pistachios. Extending the chain across 11 mixed months near Earlimart separates an 11.7-centimetre seasonal bounce from 16.8 centimetres per year of permanent compaction, matches 10 GPS stations at 0.924 cross-station correlation, and flags steep canal tilts led by the Tulare Canal at 57 millimetres per kilometre.
- **Offline Fallback Cue (`Tab 5`):** `Slides 3 & 4` or `web/assets/cv_fullyear.mp4`.

### Block 4 (`1:30 – 2:00`) · Konya–Karapınar Sinkholes, Mexico City Scaling & Compaction Physics
- **Speaker:** **Kerem**
- **Memir Clicks (`Tab 1` `[data-step="kp"]` + `#why`):**
  1. Scroll to **Chapter 6 · Türkiye — our home** (`[data-step="kp"]`), point to `#ringBox` / `#ringChart` (**`4.2 cm`** `< 1 km` vs. **`0.6 cm`** `> 5 km`, `10` of `29` coherent sinkholes), and click one item in `#sinkList` (`29` cited sinkholes).
  2. Scroll past `#why` (`Figure 6` clay/aquifer cross-section showing elastic rebound vs. permanent clay collapse).
- **Kerem Says:**
  > In our home basin of Karapınar, Türkiye, 8 provisional NISAR pairs record minus 5.9 centimetres line-of-sight sinking where 29 documented sinkholes sit in irrigated karst, with terrain within 1 kilometre sinking 4.2 centimetres on average versus 0.6 centimetres beyond 5 kilometres. Radar cannot predict a sudden roof collapse date, so we present that honestly—just as we verified pipeline transferability across Mexico City at minus 4.4 centimetres line of sight—mapping where deep clay and pore water lose irreversible capacity.
- **Offline Fallback Cue (`Tab 5`):** `Slide 5` (`docs/story/slides.html`) or `web/assets/kp_subsidence.mp4`.

### Block 5 (`2:00 – 2:30`) · Actionable Simulator (`Valley Under Pressure`) & 3D Surface Viewer
- **Speaker:** **Kerem**
- **Memir Clicks (`Tab 1` `#play` -> `Tab 3: game/index.html` + `Tab 4: web3d/index.html`):**
  1. In `#play`, click **`#gamePlay` (`"▶ Play the simulator"`)** or switch to pre-loaded **`Tab 3` (`game/index.html`)** via **`#gameOpen` (`"Open full screen ↗"`)**.
  2. Click preset **`2. Multi-Year Drought`** in **Classroom Mode**, step forward across the 24-month horizon against the 2026 NISAR dashed benchmark, then switch for `5–8 s` to **`Tab 4` (`web3d/index.html`)** via **`#view3d` (`"3D view of the sinking ground ↗"`)** and toggle Karapınar `29` sinkholes + breathing loop.
- **Kerem Says:**
  > Maps diagnose past pumping; our Valley Under Pressure simulator matches NISAR's 2026 Terra Bella summer rate so growers, students, and water boards can test two-year pumping decisions live. Pulling water levels below the historical preconsolidation low permanently crushes clay in the 24-month chart and Three.js 3D bowl, showing storage capacity that never returns even when wet winters come back.
- **Offline Fallback Cue (`Tab 5`):** `Slide 6` (`docs/story/slides.html`).

### Block 6 (`2:30 – 3:00`) · Five User Groups, Future NISAR Applications & Mandatory Attribution Close
- **Speaker:** **Kerem**
- **Memir Clicks (`Tab 1` `#who` -> `#next` -> `#how`):**
  1. Scroll smoothly through **`#who`** (*"One measurement, five kinds of users"*: Scientists, Water & canal managers, Educators, Decision-makers, Everyone) and **`#next`** (*"Looking ahead — What NISAR can do next"*).
  2. Stop cleanly on **`#how`** (*"Method & honesty — How we know"*) showing `.qlegend` (`PROVISIONAL` / `PRE-CALIBRATION BETA` / `PREVIEW`) and `.disclaimer`, hovering **`Science`** (`science.html`) and **`Data`** (`data.html`).
- **Kerem Says:**
  > Every dataset, GPS check, 40-minute classroom lesson, and test lives openly under an MIT licence for scientists, canal managers, educators, policymakers, and farming communities—ready to scale into 12-day global NISAR canal warnings and aquifer accounting. All NISAR science products used here are provisional, with calibration and validation performed by NASA–JPL and ISRO, not by our team—thank you, and we welcome your questions.
- **Offline Fallback Cue (`Tab 5`):** `Slide 7` (`docs/story/slides.html`).

---

## 2. Quick-Glance Verified Number Reference

| Region / Topic | Source Dataset | Period (`quality`) | Headline Numbers (Verified Direct Read) |
|---|---|---|---|
| **Central Valley (Summer)** | `data/central_valley/summary.json`, `area_stats.json` | `2026-06-28 → 2026-10-14` (`provisional`, `7` pairs) | Peak **`−7.8 cm` LOS** (`−10.1 cm` vert. est. at `39.1°`, `−26.4 cm/yr` summer linear est., ref spread `−7.8` to `−4.7 cm`); common valid **`239.54 km² <= −5 cm`** (`240 km²` card), **`1,578.27 km² <= −2 cm`** |
| **Central Valley (Full Year)** | `data/central_valley_fullyear/decomp.json`, `fullyear.md` | `2025-11-24 → 2026-10-14` (`mixed`: `18` pre-cal beta + `7` provisional) | `7 km W of Earlimart` (`p01`): **`−20.3 cm` LOS** (`−26.9 cm` vert. est.), decomposed (`R² = 0.97`) into **`−16.8 ± 2.2 cm/yr`** permanent trend vs. **`11.7 cm`** seasonal swing (`1.28:1`) |
| **GNSS & Dual-Orbit Check** | `data/central_valley/validation.json`, `cv_p34_vs_p114.json`, `vertical.json` | `2026-06-28 → 2026-10-14` (`provisional`) | **`10` NGL stations:** `1.00 cm` median RMSE (`r = 0.924` final fit, `CAHA` `r = 0.90`); **T34 Asc. ↔ T114 Desc.:** `6,719` blocks, `85%` sign agreement (`\|d\| > 3 cm`), Alpaugh bowl **`−7.2 cm` vertical / `−0.1 cm` east-west** |
| **Infrastructure Tilt Risk** | `data/central_valley/assets.json`, `risk_sensitivity.md` | `2026-06-28 → 2026-10-14` (`provisional`, OSM ODbL) | **`81 / 645` high-risk segments:** **Tulare Irrigation District Canal** **`57.01 mm/km`**, **California Aqueduct** **`49.12 mm/km`** (`102.8 km`), **Friant-Kern Canal** `16.5 mm/km` (`17 mm/km`); top-10 ranking `100%` invariant to `±25%` thresholds |
| **L-Band vs C-Band Cross-Sensor** | `docs/story/cross_sensor.md`, `data/central_valley_s1/cross_sensor.json` | Summer `2026` vs OPERA `DISP-S1` | NISAR L-band (`24.20 cm`, `12.10 cm` fringe) keeps **`80.4%` valid Tulare ag-core pixels (`coh >= 0.30`)** in summer; `5` Tulare GPS **`RMSE = 0.823 cm`**; OPERA C-band (`2.77 cm` fringe) ends **`2026-04-26`** (`0` summer frames) |
| **Population & Crop Exposure** | `docs/story/exposure.md` (`WorldPop`, `USDA CDL`, `ESA WorldCover`) | `2026` summer `> 2 cm` / `> 5 cm` LOS footprints | **`141,555` combined residents** on `> 2 cm` LOS land (**`71,701` CV** + **`69,854` Konya Basin**, incl. `11,572` Karapınar); **`79.2%` (`1,251.37 km²`)** of CV `> 2 cm` footprint is cropland (citrus **`355.64 km²`**, pistachios **`230.92 km²`**) |
| **Karapınar Basin & Sinkholes** | `data/karapinar/summary.json`, `assets.json`, `sinkhole_stats.md` | `2026-06-26 → 2026-10-12` (`provisional`, `8` pairs) | Peak **`−5.9 cm` LOS** (`−8.0 cm` vert. est. at `42.0°`); **`29` verified sinkholes:** `< 1 km` mean **`−4.15 cm` (`4.2 cm`)** vs `> 5 km` **`−0.65 cm` (`0.6 cm`)** (`6.4×`); `1.04 km` block perm `p = 0.0001`; `3,423` constellation shifts `p = 0.0207` |
| **UK Fens, Polarimetry & London Clay** | `data/uk/meta.json`, `data/fens/crops.json`, `data/uk_clay/detection.json` | `22 Jun – 20 Oct 2026` (`preview` + `provisional`) | Holme Fen **`~4 m`** since `1851` (`2.75 m` bsl); `20 Oct 2026` VIIRS ~98% cloud vs NISAR `GCOV`; **`4` Fens fields (`22 Jun–8 Oct`):** `HH` ~`7 dB` brighter than `HV` (`4.27` vs `3.49 dB` range); **London (`9` pairs):** **`status: below_detection`** (`3σ = 3.62 cm`, **`97.7%` within `±1.5 cm`**) |
| **Mexico City (4th Region)** | `data/global/mexico_city/summary.json` | `2026-06-22 → 2026-10-20` (`provisional`, `8` pairs) | Peak 1 km block median **`−4.4 cm` LOS** (`−7.4` to `−4.4 cm` ref spread; **`−6.2 cm` vert. est.** at `44.2°` incidence; linear rate est. `−13.5 cm/yr`) |

---

## 3. Top 5 Jury Questions — One-Sentence Flash Cues (`judge_faq.md`)

1. **Q1 (`FAQ #1` · Calibration & Pre-Calibration Full-Year Tier — Lead: İbrahim):**  
   Every core headline metric uses post-17 June 2026 NASA–ISRO NISAR `provisional` `GUNW` products (`CRID P05023`)—whose calibration and validation are carried out by NASA–JPL and ISRO rather than our team—while pre-calibration winter pairs in the 11-month Earlimart chart sit isolated in a `mixed` dataset with dashed curves and explicit caution banners.
2. **Q2 (`FAQ #2` · Slant LOS vs. Vertical Sinking — Lead: Mehmet):**  
   InSAR measures 1D beam motion (`39.1°` California, `41.9°` Karapınar), so base maps stay strictly in LOS, `LOS / cos θ` values are labeled as vertical estimates, and combining ascending Track 34 with descending Track 114 independently recovers **`−7.2 cm` vertical** (`−0.1 cm` east-west) in the Alpaugh bowl.
3. **Q3 (`FAQ #3–5` · Atmosphere, Reference Choice & L-vs-C Advantage — Lead: Mehmet):**  
   Each pair removes the `GUNW` ionospheric screen and topography-aware plane, reports `1 km` block medians plus `0.294 cm` Cramér-Rao phase noise (`1.00 cm` GPS median RMSE), preserves `80.4%` summer Tulare crop coherence at `24.20 cm` L-band (`12.10 cm` fringe vs. C-band `2.77 cm`), and uses London clay (`97.7%` within `±1.5 cm`, `3σ = 3.62 cm`) as a negative control.
4. **Q4 (`FAQ #7` · Karapınar Sinkholes vs. Roof-Collapse Prediction — Lead: İbrahim):**  
   NISAR tracks multi-pixel groundwater drawdown rather than day-ahead cavern roof failure, yet pixels within `1 km` of 29 field-verified sinkholes sink `6.4×` faster (`−4.15 cm` LOS) than farmland beyond `5 km` (`−0.65 cm`; `p = 0.0001` permutation / `p = 0.0207` constellation shift).
5. **Q5 (`FAQ #6 & B3` · Multi-Region Transferability & Human/Crop Exposure — Lead: İbrahim):**  
   Testing identical Python scripts across California alluvial clays (`−7.8 cm` LOS), Karapınar karst (`−5.9 cm` LOS), UK Fens/London clay (`below_detection`), and Mexico City (`−4.4 cm` LOS) shows open transferability while overlaying WorldPop and USDA/ESA land cover identifies **`141,555` residents** (CV + Konya Basin) and **`79.2%` Central Valley cropland** on `> 2 cm` sinking ground.
