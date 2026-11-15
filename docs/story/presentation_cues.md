# NISAR Pulse — 3-Minute Lincoln Presentation Cue Sheet (`docs/story/presentation_cues.md`)

> **Core Message (15 words):** *With NISAR's 24 cm L-band radar, we measure centimeter-scale ground sinking across aquifers and agricultural lands.*  
> **Target Rehearsal:** `17:30 TR` · **Duration:** `3:00` (`6 × 30 s` blocks) · **Live App:** https://keremsumer2010-tech.github.io/aseltech/ · **Offline Presentation Mode (6 stops):** [web/present.html](../../web/present.html)  
> **Mandatory Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## Team Roles

| Role | Member | Responsibility During Live Pitch & Q&A |
|---|---|---|
| **Lead Speaker** | **Kerem** | Delivers the `6 × 30 s` plain-English narrative blocks (`0:00–3:00`) cleanly at ~135 wpm |
| **Live Demo Pilot** | **Memir** | Drives `Tab 1` (`web/index.html`), `Tab 2` (`explorer.html#central_valley_fullyear`), `Tab 3` (`game/index.html`), `Tab 4` (`web3d/index.html`) and executes `< 2 s` offline fallbacks (`Tab 5` `slides.html`, `demo_30s.mp4`) |
| **Technical Q&A & Timekeeper** | **Mehmet** | Runs silent stopwatch (`0:30` splits, **`2:30` simulator cue**, **`2:50 WRAP NOW`**) and answers jury questions on GUNW phase math, L-vs-C coherence, ionosphere/DEM deramp, 10-station GNSS agreement, dual-orbit Track 34/114, and 11-month decomposition |
| **Data, Impact & Policy Q&A Lead** | **İbrahim** | Answers jury questions on UK Fens `HH`/`HV` polarization & London clay `below_detection`, Karapınar 29 sinkholes & permutation tests, WorldPop/USDA exposure (`141,555` CV+Konya residents / `79.2%` CV cropland), Mexico City (`-7.0 cm` LOS off-basin rerun), simulator priors, and verified sources (`sources.md`) |

---

## Pre-Flight Tab Layout (`T − 10 min`)

- **Tab 1:** `https://keremsumer2010-tech.github.io/aseltech/` (or `http://localhost:8000/web/index.html`) scrolled to top Hero (`#heroMap`)
- **Tab 2:** `explorer.html#central_valley_fullyear` pre-clicked near Earlimart (`7 km W of Earlimart`)
- **Tab 3:** `game/index.html` at `Month 0 of 24` with **Classroom Mode** open (`2. Multi-Year Drought` ready)
- **Tab 4:** `web3d/index.html` loaded with Central Valley / Karapınar 3D displacement mesh (`quality: provisional · CRID P05023`)
- **Tab 5 (Offline Backup):** `docs/story/slides.html` (`Slide 1`, arrow-key ready) + `docs/story/media/demo_30s.mp4` paused in VLC (`Alt+Tab`)

---

## 1. Six 30-Second Speaking & Demo Blocks (`0:00 – 3:00`)

### Block 1 (`0:00 – 0:20`) · Hero: A Self-Checking Global Subsidence Atlas
- **Speaker:** **Kerem**
- **Memir Clicks (`web/present.html` Stop 1 or `web/index.html` Hero):**
  1. Show the single-sentence core and 3 headline numbers (**`29` basins · `1.20 M` residents · `r = 0.92` GPS**), then click **`Explore the atlas →`**.
- **Kerem Says:**
  > We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: 29 basins measured with one open pipeline on the same 93 days, every number traceable to its file, and every headline checked against GPS, NASA's OPERA product and the literature.
- **Offline Fallback Cue:** `web/present.html` Stop 1 (`docs/story/three_minute_story.md` §1).

### Block 2 (`0:20 – 1:00`) · Atlas: Twenty-Nine Basins Ranked on 93 Days
- **Speaker:** **Kerem**
- **Memir Clicks (`web/present.html` Stop 2 or `web/atlas.html#konya_plain`):**
  1. Show the 3D globe preview and Top-5 common-window table (`28 Jun – 29 Sep 2026`), highlighting **#1 Konya Plain (`−11.0 cm/100d`, `11.6%` valid-coverage caution)**, `#2 Eloy (−8.6)`, `#3 Central Valley (−7.3)`.
- **Kerem Says:**
  > One open pipeline measures every basin over the shared 28 June to 29 September 2026 window—using a ±0.25-degree box and off-basin rock reference—placing Konya Plain first at minus 11.0 centimetres per 100 days with an explicit 11.6 percent coverage caution.
- **Offline Fallback Cue:** `web/present.html` Stop 2 (`docs/story/three_minute_story.md` §2).

### Block 3 (`1:00 – 1:30`) · We Caught Our Own Error (Self-Checking QC)
- **Speaker:** **Kerem**
- **Memir Clicks (`web/present.html` Stop 3 or `web/atlas.html` QC badge):**
  1. Show **Semarang before/after (`−12.1 cm → −6.2 cm`)** and the `5` QC-flagged basins (`Gorgan`, `Delhi`, `Pekalongan`, `Beijing`, `Bangkok`) separated as `indicative only`, plus Tehran (`−3.5 → −7.4 cm` off-basin ref fix).
- **Kerem Says:**
  > Before ranking any city, our automated time-series quality control caught our own pipeline errors—flagging a 12.1-centimetre half-cycle phase jump in Semarang, correcting it to minus 6.2 centimetres (#7 reliable), fixing Tehran and Beijing references, and isolating five flagged basins as indicative only.
- **Offline Fallback Cue:** `web/present.html` Stop 3 (`docs/story/three_minute_story.md` §3).

### Block 4 (`1:30 – 2:05`) · Why You Can Trust It (GPS, OPERA, Noise Floor)
- **Speaker:** **Kerem**
- **Memir Clicks (`web/present.html` Stop 4 or `web/science.html`):**
  1. Show **10-station Central Valley GPS (`r = 0.924`, `1.00 cm` median RMSE)**, **Mexico City OPERA (`r = 0.912`)**, formal uncertainty (`σ ≈ 0.3 cm`), and London Clay negative control (`3σ = 3.62 cm`, `below_detection`).
- **Kerem Says:**
  > Provisional NISAR motion—along the satellite's line of sight—tracks 10 continuous GPS stations at r equals 0.92, matches NASA's OPERA product in Mexico City at r equals 0.91, and stays cleanly above our 0.3-centimetre formal uncertainty and 3.6-centimetre London clay noise floor.
- **Offline Fallback Cue:** `web/present.html` Stop 4 (`docs/story/three_minute_story.md` §4).

### Block 5 (`2:05 – 2:40`) · What It Is Useful For (Exposure, Storage, Tilt, Simulator)
- **Speaker:** **Kerem**
- **Memir Clicks (`web/present.html` Stop 5 → `game/index.html?basin=konya`):**
  1. Flash **1.20 million residents** (`511.65 km² < −5 cm`), **`0.3174 km³/yr` permanent Central Valley storage loss**, **`81 / 645` canal/rail segments `> 20 mm/km`** (Tulare Canal `57.01 mm/km`), and launch the 24-month simulator (`Valley Under Pressure`).
- **Kerem Says:**
  > We turn radar centimetres into decisions: 1.20 million people living on sinking ground, 0.32 cubic kilometres per year of permanent Central Valley aquifer loss, 81 high-tilt canal and rail segments, one-page city bulletins, and a 24-month simulator anyone can play.
- **Offline Fallback Cue:** `web/present.html` Stop 5 (`docs/story/three_minute_story.md` §5).

### Block 6 (`2:40 – 3:00`) · Original, Open & Mandatory Provisional Close
- **Speaker:** **Kerem**
- **Memir Clicks (`web/present.html` Stop 6 / `README.md`):**
  1. Show the 4 original contributions, the single-command reproduction chain (`build_atlas.py`, `atlas_qc.py`, `sync_atlas_text.py`, `vital_signs.py`), Team Taykut credits, and the verbatim calibration notice.
- **Kerem Says:**
  > Every number, figure, and ranking table in our 29-basin atlas reproduces from one open-source command chain. All NISAR data used here are provisional; calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team—thank you, and we welcome your questions.
- **Offline Fallback Cue:** `web/present.html` Stop 6 (`docs/story/three_minute_story.md` §6).

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
| **Mexico City (4th Region)** | `data/global/mexico_city/summary.json` | `2026-06-22 → 2026-10-20` (`provisional`, `8` pairs) | Peak 1 km block median **`−7.0 cm` LOS** (`−8.0` to `−4.6 cm` ref spread; **`−9.7 cm` vert. est.** at `44.2°` incidence; `−5.80 cm/100d` rate; off-basin rerun) |

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
   Testing identical Python scripts across California alluvial clays (`−7.8 cm` LOS), Karapınar karst (`−5.9 cm` LOS), UK Fens/London clay (`below_detection`), and Mexico City (`−7.0 cm` LOS) shows open transferability while overlaying WorldPop and USDA/ESA land cover identifies **`141,555` residents** (CV + Konya Basin) and **`79.2%` Central Valley cropland** on `> 2 cm` sinking ground.
