# NISAR Pulse — Follow the Water: Pitch, Video Script & Slide Deck

> **Verified Data Policy (`K-2`, `Q30`):** All site measurements below resolve directly from committed repository datasets (`data/central_valley/*.json`, `data/karapinar/*.json`, `data/uk/meta.json`, `data/uk_clay/detection.json`, `docs/story/sources.md`, and `web3d/surfaces.json`). Zero synthetic or unlabelled estimates appear in any metric.

## Verified Repository Data Map

| Token | Verified Source File | Resolved Value (`quality: provisional` unless noted) |
|---|---|---|
| `{HOLME_FEN_M}` | `docs/story/sources.md` (Great Fen / Wikipedia) | `~4 metres` above ground today (`1851` post; site `2.75 m` below sea level) |
| `{CV_MAX_CM}` | `data/central_valley/summary.json` | `−7.8 cm` LOS (1 km block median peak, `6 km N of Terra Bella`) |
| `{CV_VERT_CM}` | `data/central_valley/summary.json` | `−10.1 cm` vertical estimate (`39.1°` incidence) |
| `{CV_RATE_CM_YR}` | `data/central_valley/summary.json` | `−26.4 cm/yr` linear 108-day summer estimate *(overstates net annual rate)* |
| `{CV_PERIOD}` / `{CV_N_PAIRS}` | `data/central_valley/summary.json` | `2026-06-28 → 2026-10-14` (`108` days, `7` pairs, Track 34 Asc.) |
| `{KP_MAX_CM}` | `data/karapinar/summary.json` | `−5.9 cm` LOS (1 km block median peak, `2 km W of Karapınar`) |
| `{KP_VERT_CM}` | `data/karapinar/summary.json` | `−8.0 cm` vertical estimate (`42.0°` incidence) |
| `{KP_RATE_CM_YR}` | `data/karapinar/summary.json` | `−20.0 cm/yr` linear 108-day summer estimate |
| `{KP_PERIOD}` / `{KP_N_PAIRS}` | `data/karapinar/summary.json` | `2026-06-26 → 2026-10-12` (`108` days, `8` pairs, Track 7 Desc.) |
| `{GNSS_N_STATIONS}` | `data/central_valley/validation.json` | `10` continuous NGL stations (`IGS20/NA` Up) |
| `{GNSS_RMSE_CM}` | `data/central_valley/validation.json`, `validation_report.md` | `1.33 cm` mean TS RMSE (`1.00 cm` median; `1.37 cm` final-epoch RMSE across `10` stations; `0.76 cm` final / `0.86 cm` 5-station active mean; `0.64 cm` best at `P566`) |
| `{GNSS_CORR}` | `data/central_valley/validation.json`, `validation_report.md` | **`r = 0.924` cross-station final fit** (`n = 10`); **`r = 0.851`** moving mean (`n = 4`); up to **`r = 0.90`** (`0.8957` at `CAHA`, `0.8955` at `HANF`) |
| `{DUAL_ORBIT}` | `analysis/out/cv_p34_vs_p114.json`, `docs/qa/PC3.md` | Track 34 Asc. ↔ Track 114 Desc. (`6,719` 1 km blocks): **`r = 0.489`** (`0.60` local `< 15 km`), **`RMSE = 2.65 cm`**, **`median diff = −1.29 cm`**, slope `0.514`, **`85%` sign agreement** (`\|d\| > 3 cm`, `n = 1,297`), `−5.7 cm` T114 median where T34 `< −6 cm` |
| `{TWO_ORBIT_VERT}` | `data/central_valley/vertical.json` (`Q22`) | Two-orbit pixel inversion (`49.6%` overlap): **Alpaugh / Earlimart bowl `−7.2 cm` vertical (`−0.1 cm` east-west)**; max block `−9.8 cm` vertical (`+2.4 cm` east); `up_cm` `p2 = −5.98`, `p50 = −1.25`, `p98 = +2.35 cm` |
| `{TOP_CANAL_NAME}` / Slope | `data/central_valley/assets.json` | `Tulare Irrigation District Canal` (`57.01 mm/km`, `2.17 km`) & `California Aqueduct` (`49.12 mm/km`, `102.8 km`); `81/645` high-risk segments |
| `{N_SINKHOLES}` | `data/karapinar/sinkholes.geojson`, `assets.json` | `29` verified Karapınar sinkholes (`0–1 km` ring mean **`−4.15 cm` LOS**, `6.4×` vs `>5 km` background; `19.74 mm/km` near `Köken Obruğu-II`) |
| `{CV_FULLYEAR}` | `data/central_valley_fullyear/decomp.json`, `docs/story/fullyear.md` | **Mixed-quality (`18` `beta-precal` + `7` `provisional`)** 11-month chain (`24 Nov 2025 → 14 Oct 2026`, `324 days`, `25` pairs): Earlimart (`p01`) `−20.3 cm` LOS cumulative (`−26.9 cm` vert. est.), decomposed (`R² = 0.97`) into **`−16.8 ± 2.2 cm/yr`** permanent compaction (`−14.9 cm` over 324 days) vs. **`11.7 cm`** peak-to-peak seasonal rebound (`1.28:1` ratio) |

> **Challenge Alignment & NASA StoryMap Context (`16:15` / `16:25`):** NASA's [NISAR Land Subsidence StoryMap](https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828) showed the Central Valley subsidence bowl with airborne radar (2013–2017). We measured the same valley — and the same aqueduct — from space with NISAR in 2026, checked it against GPS, and ranked the canal and road segments at risk. Built as an open-source **interactive application** to **track and visualize surface change**, seasonal **patterns and rhythms**, subsurface **physical drivers**, five-audience **actionable insights** (`audiences.md`), and NISAR **future applications** (`future_applications.md`), backed by **`B1` L-vs-C cross-sensor coherence** (`80.4%` valid Tulare ag-core pixels vs. C-band `2.77 cm` fringe, `cross_sensor.md`), **`B3` population & crop exposure** (`141,555` residents across CV & Konya Basin on `> 2 cm` LOS land — `71,701` CV + `69,854` Konya, incl. `11,572` Karapınar; `79.2%` / `1,251.37 km²` CV cropland led by citrus & pistachios, `exposure.md`), **`A12` UK Fens `HH`/`HV` crop polarimetry** (`~7 dB` offset across `4` fields, `polarization.md`), and **`A2` Mexico City** (`−4.4 cm` LOS peak across `8` provisional pairs, `data/global/mexico_city/summary.json`).

---

## 1. Live Presentation Script (3 Minutes — Lincoln Local Pitch)

**Roles (`MASTER_PLAN.md §7`):**
- **Speaker:** Kerem (walks through the narrative and live site)
- **Live Demo Pilot:** Co-presenter (drives the sliders, map click, and Valley Under Pressure)
- **Data Q&A Lead:** Mehmet (handles technical questions on NISAR GUNW math, GNSS validation, and limitations)

### 0:00 – 0:20 · Hook (The Iron Post)
- **[ON SCREEN — Hero & Story Chapter 2 (`[data-step="uk"]`, `#holmeText`)]:** Slow orbital/radar hero background; scroll into Chapter 2 Holme Fen benchmark card (`1851` post, `~4 m`).
- **[SPEAKER]:**
  "In **1851**, drainage engineers in the English Fens hammered a cast-iron post flush with the surface of the peatlands. Today, that same iron post stands **nearly 4 metres** above the ground — leaving Holme Fen **2.75 metres below sea level**, Britain's lowest land point — not because the iron grew, but because draining the peat caused the ground beneath Britain's richest farmland to collapse."

### 0:20 – 0:45 · Problem & Solution
- **[ON SCREEN — Story Chapter 2 (`#compare`, `#compareRange`)]:** Slide optical cloudy **VIIRS SNPP (`20 Oct 2026`)** view across to reveal the same-day **NISAR L-band GCOV radar preview** underneath, showing The Wash coastline clearly resolved under **98%+ cloud cover**.
- **[SPEAKER]:**
  "The same crisis is happening silently over every major pumped aquifer on Earth. Optical satellites are blind under cloud and struggle inside vegetated valleys, while raw radar interferometry lives inside multi-gigabyte HDF5 files only specialists can open.
  Our project, **NISAR Pulse — Follow the Water**, turns NASA–ISRO NISAR L-band interferograms into plain-language maps, a Three.js 3D surface explorer, and a 24-month water-policy simulator (**Valley Under Pressure**) — all running live in any browser."

### 0:45 – 1:45 · Live Demo: Central Valley & Karapınar
- **[ON SCREEN — Story Chapter 3 (`[data-step="cv"]`, `#cvPlay`, `#slider`, `#readout`, `#pointChart`)]:** Press `#cvPlay` on the date slider (**`28 Jun – 14 Oct 2026`**, **`7` provisional NISAR GUNW pairs**). Tap `p01` (`6 km N of Terra Bella`, `max_subsidence_location`) and show `#readout` + `#pointChart` + Chapter 4 GPS comparison.
- **[SPEAKER]:**
  "Step one: California's San Joaquin Valley. Across **108 summer days (`2026-06-28` to `2026-10-14`)**, cumulative NISAR line-of-sight measurements over **7 provisional pairs** show the valley floor dropping by up to **`−7.8 centimetres` LOS** — roughly **`−10.1 centimetres`** vertical equivalent — near **Terra Bella**.
  Tap any point on the map and the chart strips away radar jargon into one plain sentence for water managers. And when underground clay compacts irreversibly, surface canals tilt: evaluating **645 OpenStreetMap corridors** reveals **81 high-risk segments**, with differential slopes reaching **`57.01 mm/km`** on the **Tulare Irrigation District Canal** and **`49.12 mm/km`** along **102.8 km of the California Aqueduct**—and **`±25%`** threshold sensitivity tests (`72–115` high-risk segments) leave our top-10 priority ranking **100% invariant**."
- **[ON SCREEN — Story Chapter 6 (`[data-step="kp"]`, `#sinkList`)]:** Scroll to Karapınar; highlight documented sinkhole markers (**`29` field-verified locations**) over the **`8`-pair (`26 Jun – 12 Oct 2026`)** L-band displacement map.
- **[SPEAKER]:**
  "Step two: our home basin — **Karapınar in Konya, Türkiye** — where **8 provisional pairs** over the same **108-day** irrigation window reveal up to **`−5.9 centimetres` LOS** (`~−8.0 centimetres` vertical) just **2 kilometres west of Karapınar**, overlaid with **29 peer-reviewed karst sinkholes**—and valid pixels within 1 km of those sinkholes sink **6.4 times faster (`−4.15 cm`)** than the far-field plateau (`−0.65 cm`)."

### 1:45 – 2:05 · Interactive Decision Tool: Simulator (`#play`, `#gameFrame`) (15–20 sec)
- **[ON SCREEN — Simulator (`#play`, `game/index.html` embedded in `#gameFrame`)]:** Pilot selects **Terra Bella**, triggers **Over-Pump** (`#pumpSlider` up toward `150%`), steps across the **24-month** timeline, and points to permanent coral clay compaction and canal conveyance warnings; then resets to `SGMA Balance`.
- **[SPEAKER]:**
  "Maps tell you what happened; our **Valley Under Pressure** simulator — matched directly against NISAR's Terra Bella summer subsidence (`−7.8 cm` LOS / `−10.1 cm` vertical, `k = 0.6232`, `N = 1,000` Monte Carlo uncertainty `−18.69 cm` nominal / `p10–p90 −27.10` to `−6.23 cm` over 24 months) across seven Tulare Basin districts — lets growers and water boards test the **24-month** trade-off. Over-pumping boosts short-term revenue, but drops groundwater head past the preconsolidation threshold, permanently crushes deep clay, and bends canals toward Friant-Kern-scale flow losses."

### 2:05 – 2:40 · How We Know (Physics, GNSS Validation & Scientific Honesty)
- **[ON SCREEN — Story Chapter 4 (`[data-step="gnss"]`, `#gnssChart`, `#gnssTable`) & Method (`#how` / `science.html`)]:** Show real daily vertical GNSS station traces from Nevada Geodetic Laboratory alongside NISAR pixel extractions.
- **[SPEAKER]:**
  "Every step follows open physical principles: L-band 24-centimetre radar penetrates canopy cover; our pipeline converts unwrapped phase via `−λ / 4π` using each granule's exact center wavelength (`0.294 cm` CV / `0.326 cm` Karapınar Cramér-Rao median phase sigma), masks decoherent water (`coherence >= 0.3`), strips unwrapping glitches, removes the ionospheric screen and topographic plane, and verifies itself two independent ways: first against **10 continuous GNSS stations** across the valley (`r = 0.924` cross-station final fit, `1.00 cm` median RMSE, **`r = 0.90`** at **`CAHA`** and **`HANF`**), and second across **two independent NISAR orbits** (**Track 34 ascending ↔ Track 114 descending**): across `6,719` 1 km blocks (`r = 0.489`, `RMSE = 2.65 cm`, `median diff = −1.29 cm`), where one orbit sees more than 6 cm of sinking the other sees `−5.7 cm` median (`85%` sign agreement on `|d| > 3 cm`), and two-geometry inversion confirms the **Alpaugh bowl sank `−7.2 cm` vertically with `−0.1 cm` sideways motion**.
  And we are explicit about limits: NISAR science data are currently marked **provisional** — sensor calibration is performed by NASA–JPL and ISRO, not our team."

### 2:40 – 3:00 · Road Ahead & Close
- **[ON SCREEN — `/web3d/` 3D "Breathing Earth" interactive mesh + Five-Audience Cards + GitHub URL]:**
- **[SPEAKER]:**
  "Looking forward—from extending NASA's 2013–2017 airborne Central Valley StoryMap into our 2026 11-month Earlimart decomposition (`−16.8 cm/yr` permanent compaction vs. `11.7 cm` seasonal swing)—continuous 12-day L-band NISAR passes turn radar phase into actionable insights for scientists, canal managers, educators, decision-makers, and local communities alike. Thank you — and we welcome your questions."

### Prepared Jury Q&A Notes
- See [`docs/story/presentation_cues.md`](presentation_cues.md) (`6 × 30 s` Lincoln blocks + 5 single-sentence Q&As), [`docs/story/rehearsal_checklist.md`](rehearsal_checklist.md) (offline failsafes), and full **15-question card** in [`docs/story/judge_faq.md`](judge_faq.md), plus [`docs/story/audiences.md`](audiences.md), [`docs/story/future_applications.md`](future_applications.md), [`docs/story/team_story.md`](team_story.md), [`docs/story/lesson_plan.md`](lesson_plan.md), [`docs/story/cross_sensor.md`](cross_sensor.md), [`docs/story/exposure.md`](exposure.md), [`docs/story/polarization.md`](polarization.md), [`docs/story/uk_findings.md`](uk_findings.md), and [`data/global/mexico_city/summary.json`](../../data/global/mexico_city/summary.json).

---

## 2. 30-Second Video Script & English `.srt` Subtitles

**Target length:** `30.0 seconds` (`00:00:00,000` to `00:00:30,000`).  
**Rendered video deliverable:** [`docs/story/media/demo_30s.mp4`](media/demo_30s.mp4) (`29.62 s`, `1080p`, `24 fps`, burned English subtitles, logoless, generated via `analysis/pc6/make_demo_video.py`).  
**Visual rhythm:** Fast-cut web capture + clean overlay captions; every cited statistic matches `data/*/summary.json`, `validation.json`, and `assets.json`.

| Time | Visual Cue | Spoken Narration (English) |
|---|---|---|
| `0:00 – 0:04` | Web hero → Holme Fen (`1851` post `~4 m`) + clouds clearing over UK radar swipe | "Over centuries of draining aquifers, dry farmland doesn't wait to sink — it collapses beneath our feet." |
| `0:04 – 0:09` | Scene 1 swipe slider moving across Fens `2026-10-20` cloudy optical vs bright NISAR radar | "While optical cameras stall under clouds, NASA–ISRO NISAR's 24-centimetre L-band radar sees straight to the ground." |
| `0:09 – 0:15` | Scene 2 time-lapse across Central Valley (`2026-06-28 → 2026-10-14`) + `p01` Terra Bella click | "Across California's Central Valley, 7 provisional NISAR pairs measure up to −7.8 cm of sinking in 108 summer days." |
| `0:15 – 0:20` | GNSS validation (`1.00 cm` median RMSE) + Karapınar (`−5.9 cm` LOS) with 29 sinkhole pins | "Checked against 10 GNSS stations, and extended to Karapınar's −5.9 cm basin subsidence and 29 sinkholes." |
| `0:20 – 0:26` | Valley Under Pressure (`#pumpSlider` / `Over-Pump` across 24 months), clay collapse & canal loss | "Valley Under Pressure turns NISAR rates into a 24-month trade-off of clay collapse and canal loss." |
| `0:26 – 0:30` | `/web3d/` 3D mesh orbit + End slate (`NISAR provisional data · NASA-JPL/ISRO calibration`) | "NISAR Pulse — Follow the Water. Open science before the ground gives way." |

### English Subtitles (`video_30s.srt`)

```srt
1
00:00:00,000 --> 00:00:04,200
When we drain deep groundwater faster than rain refills it, the land itself sinks.

2
00:00:04,200 --> 00:00:09,000
While optical satellites are blinded by clouds, NISAR L-band radar sees right through them.

3
00:00:09,000 --> 00:00:15,000
In California's Central Valley, provisional NISAR tracks up to -7.8 cm LOS (-10.1 cm vertical) across 108 days.

4
00:00:15,000 --> 00:00:20,000
Tulare Canal slopes hit 57 mm/km; GNSS agrees at 1.00 cm median RMSE; Karapinar sinks -5.9 cm near 29 obruks.

5
00:00:20,000 --> 00:00:26,000
Valley Under Pressure turns NISAR rates into a 24-month groundwater trade-off of clay collapse and canal loss.

6
00:00:26,000 --> 00:00:30,000
NISAR Pulse: Follow the Water. Provisional NISAR L2 GUNW data (NASA-JPL / ISRO calibration).
```

---

## 3. Pitch Slide Deck (7 Slides Max)

### Slide 1 · NISAR Pulse: Follow the Water
- **Subtitle:** Turning L-Band Radar Interferograms into Actionable Groundwater & Infrastructure Intelligence
- **Core Hook:** Holme Fen Iron Post (UK Fens, `1851` benchmark standing **~4 m** above drained peat at **2.75 m below sea level**).
- **Problem:** Pumping aquifers lowers pressure inside compressible clay layers — once collapsed, storage capacity never recovers.

### Slide 2 · Why NISAR L-Band? (UK Fens Live Swipe)
- **All-weather visibility:** 24 cm L-band radar penetrates **98%+ cloud cover** on `2026-10-20` where VIIRS optical fails.
- **Vegetation penetration:** Maintains coherence across irrigated croplands better than short-wavelength C-band radar.
- **Data barrier removed:** Pure-Python pipeline distills ~2 GB GUNW HDF5 granules into lightweight web tiles and plain-English cards.

### Slide 3 · Central Valley: Sinking Valley, Tilting Canals
- **Observation (`2026-06-28 → 2026-10-14`):** `7` provisional ascending Track 34 NISAR pairs show peak LOS subsidence of **`−7.8 cm`** (`~−10.1 cm` vertical est. at `39.1°` near `6 km N of Terra Bella`; linear summer rate est. `−26.4 cm/yr`), with common-valid-pixel affected area reaching **`239.54 km² <= −5 cm`** and **`1,578.27 km² <= −2 cm`** (`data/central_valley/area_stats.json`).
- **Critical Infrastructure & Sensitivity:** Out of `645` evaluated corridors, `81` are high-risk (`12.6%`), led by **Tulare Irrigation District Canal** (`57.01 mm/km`) and **California Aqueduct** (`49.12 mm/km` over `102.8 km`); varying thresholds by `±25%` shifts totals (`72–115`) while keeping the **top-10 priority corridor ranking 100% invariant** (`docs/story/risk_sensitivity.md`).
- **Interactive UX:** Click any valley coordinate for cumulative displacement history in plain language (`web/` & 3D `web3d/`).

### Slide 4 · How We Know: Independent GNSS & Dual-Orbit Validation
- **GPS Comparison:** Daily `IGS20/NA` vertical time series from **10 Nevada Geodetic Laboratory stations** inside the NISAR frame.
- **Method & Agreement:** `3×3 px` pixel extraction projected via `LOS / cos(θ)` achieves **1.00 cm median RMSE** (`1.33 cm` mean TS RMSE; **`r = 0.924` cross-station final fit**, `1.37 cm` final RMSE across 10 stations; `0.76 cm` final RMSE across the `4` sites moving `> 2 cm`; `r = 0.90` at `CAHA` & `HANF`; Cramér-Rao pixel phase sigma median `0.294 cm` CV).
- **Dual-Orbit & Vertical Inversion (`Q21` + `Q22`):** **Track 34 Asc. ↔ Track 114 Desc.** (`6,719` 1 km blocks, `2026-06-28 → 2026-10-14`) reach **`85%` sign agreement** across `|d| > 3 cm` zones (**`r = 0.489`** overall / `0.60` local `< 15 km`, **`RMSE = 2.65 cm`**, **`median diff = −1.29 cm`**, slope `0.514`, `−5.7 cm` T114 median where T34 `< −6 cm`), while two-orbit vector inversion recovers **`−7.2 cm` vertically with `−0.1 cm` east-west motion** in the **Alpaugh / Earlimart bowl** (max `−9.8 cm` vertical block).

### Slide 5 · Global Transferability: Karapınar Basin & Sinkholes (Türkiye)
- **Observation (`2026-06-26 → 2026-10-12`):** `8` provisional descending Track 7 NISAR pairs measure up to **`−5.9 cm` LOS** (`~−8.0 cm` vertical est. at `42.0°`, `−20.0 cm/yr` summer rate est.) **`2 km W of Karapınar`**, with **`3.10 km² <= −5 cm`** and **`28.66 km² <= −2 cm`** across common valid pixels (`data/karapinar/area_stats.json`).
- **Karst Inventory & Spatial Significance (`assets.json` & `sinkhole_stats.md`):** Overlays **29 field-verified sinkholes** strictly inside `[33.3, 37.6, 33.8, 37.9]`; pixels inside `0–1 km` average **`−4.15 cm` LOS (`6.4×` background `−0.65 cm`)** and `0–2 km` (`n = 236` px) average `−4.06 cm` (`−3.41 cm` diff)—confirmed statistically via **`1.04 km` block permutations (`−3.04 cm` diff, `p = 0.0001`)** and **`3,423` rigid `29`-sinkhole constellation shifts (`p = 0.0207`)**, with highways tilting up to `19.74 mm/km` near `Köken Obruğu-II`.
- **Honesty Guard:** Explicitly shows regional groundwater drawdown context without claiming InSAR predicts exact sudden roof-collapse dates.

### Slide 6 · Decision Tool: Valley Under Pressure (Physical Simulator)
- **Interactive Policy Model:** Browser simulator (`game/index.html`) matched directly against `data/central_valley/summary.json` (`−7.8 cm` LOS / `−10.1 cm` vertical target across `108` summer days, `28 Jun–14 Oct 2026`).
- **24-Month Trade-Off & Monte Carlo Check (`game_sensitivity.md`):** 1D Terzaghi consolidation model (`k = 0.6232`, `b0 · S_skv ≈ 0.02356`) letting users test `0%–150%` pumping across `7` Tulare Basin districts (`−18.69 cm` 24-month nominal vertical, `N = 1,000` stochastic `p10–p90` `−27.10` to `−6.23 cm`).

### Slide 7 · Scientific Integrity, Provenance & AI Disclosure
- **Calibration Notice:** NISAR data used here are **provisional** (`CRID P05023`); sensor calibration and validation are performed by the NISAR project (NASA–JPL / ISRO), not by our team.
- **Open & Reproducible:** Pure Python/NumPy pipeline (`pytest`-verified phase-to-cm tests) + interactive MapLibre & Three.js (`web3d/`) hosted statically, extending NASA's [Land Subsidence StoryMap](https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828) and [NISAR Societal Benefits White Papers](https://science.nasa.gov/mission/nisar/societal-benefits/) (`docs/story/sources.md §7`).
- **AI Transparency:** **Zero AI-generated images** appear in the live website, slide deck, simulator, 3D explorer, or `demo_30s.mp4` (`38b774f`); all maps, charts, and simulator panels display measured satellite, GPS, and field-survey data. Coding & documentation assistance provided by Claude and Gemini/Antigravity.
