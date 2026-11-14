# NISAR Pulse — Follow the Water: Pitch, Video Script & Slide Deck

> **Verified Data Policy (Rule K-2 · Updated for Q30):** All site measurements below are resolved directly from committed repository datasets (`data/central_valley/summary.json`, `data/karapinar/summary.json`, `data/central_valley/validation.json`, `data/central_valley/assets.json`, `data/karapinar/sinkholes.geojson`, `docs/story/sources.md`, and `web3d/surfaces.json`). Zero synthetic or extrapolated claim numbers appear unlabelled.

## Verified Repository Data Map (Resolved from `{PLACEHOLDER}` Tokens)

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
| `{GNSS_RMSE_CM}` | `data/central_valley/validation.json` | `1.33 cm` mean RMSE (`1.00 cm` median; `0.64 cm` best at `P566`) |
| `{GNSS_CORR}` | `data/central_valley/validation.json` | Up to `r = 0.90` (`0.8957` at `CAHA`, `0.8955` at `HANF`; `0.38` 10-station mean) |
| `{TOP_CANAL_NAME}` / Slope | `data/central_valley/assets.json` | `Tulare Irrigation District Canal` (`57.01 mm/km`, `2.17 km`) & `California Aqueduct` (`49.12 mm/km`, `102.8 km`); `81/645` high-risk segments |
| `{N_SINKHOLES}` | `data/karapinar/sinkholes.geojson` | `29` verified Karapınar sinkholes (inside `[33.3, 37.6, 33.8, 37.9]`, Tapur & Bozyiğit 2015) |

---

## 1. Live Presentation Script (3 Minutes — Lincoln Local Pitch)

**Roles (`MASTER_PLAN.md §7`):**
- **Speaker:** Kerem (walks through the narrative and live site)
- **Live Demo Pilot:** Co-presenter (drives the sliders, map click, and Aquifer Manager)
- **Data Q&A Lead:** Mehmet (handles technical questions on NISAR GUNW math, GNSS validation, and limitations)

### 0:00 – 0:20 · Hook (The Iron Post)
- **[ON SCREEN — Hero & Holme Fen Card]:** Slow orbital/radar hero background; cursor settles on Scene 1 card (*"Britain under clouds"*).
- **[SPEAKER]:**
  "In **1851**, drainage engineers in the English Fens hammered a cast-iron post flush with the surface of the peatlands. Today, that same iron post stands **nearly 4 metres** above the ground — leaving Holme Fen **2.75 metres below sea level**, Britain's lowest land point — not because the iron grew, but because draining the peat caused the ground beneath Britain's richest farmland to collapse."

### 0:20 – 0:45 · Problem & Solution
- **[ON SCREEN — Drag Cloud Slider in Scene 1]:** Slide optical cloudy **VIIRS SNPP (`2026-10-20`)** view across to reveal the same-day **NISAR L-band GCOV radar preview** underneath, showing The Wash coastline crystal-clear under **98%+ cloud cover**.
- **[SPEAKER]:**
  "The same crisis is happening silently over every major pumped aquifer on Earth. Optical satellites are blind under cloud and struggle inside vegetated valleys, while raw radar interferometry lives inside multi-gigabyte HDF5 files only specialists can open.
  Our project, **NISAR Pulse — Follow the Water**, turns NASA–ISRO NISAR L-band interferograms into plain-language maps, a Three.js 3D surface explorer, and a 10-year water-policy simulator — all running live in any browser."

### 0:45 – 1:45 · Live Demo: Central Valley & Karapınar
- **[ON SCREEN — Scene 2 (`The dancing ground · USA`)]:** Press Play on the date slider (**`2026-06-28` → `2026-10-14`**, **`7` provisional NISAR GUNW pairs**). Click `p01` (`6 km N of Terra Bella`, `max_subsidence_location`) and show `#cvSentence` + sparkline + GNSS comparison.
- **[SPEAKER]:**
  "Step one: California's San Joaquin Valley. Across **108 summer days (`2026-06-28` to `2026-10-14`)**, cumulative NISAR line-of-sight measurements over **7 provisional pairs** show the valley floor dropping by up to **`−7.8 centimetres` LOS** — roughly **`−10.1 centimetres`** vertical equivalent — near **Terra Bella**.
  Tap any point on the map and the chart strips away radar jargon into one plain sentence for water managers. And when underground clay compacts irreversibly, surface canals tilt: evaluating **645 OpenStreetMap corridors** reveals **81 high-risk segments**, with differential slopes reaching **`57.01 mm/km`** on the **Tulare Irrigation District Canal** and **`49.12 mm/km`** along **102.8 km of the California Aqueduct**."
- **[ON SCREEN — Scene 3 (`Konya's sinkholes · TR`)]:** Scroll to Karapınar; toggle sinkhole pins (**`29` field-verified locations**) over the **`8`-pair (`2026-06-26` → `2026-10-12`)** L-band displacement map.
- **[SPEAKER]:**
  "Step two: our home basin — **Karapınar in Konya, Türkiye** — where **8 provisional pairs** over the same **108-day** irrigation window reveal up to **`−5.9 centimetres` LOS** (`~−8.0 centimetres` vertical) just **2 kilometres west of Karapınar**, overlaid with **29 peer-reviewed karst sinkholes** reaching up to **80 metres deep**."

### 1:45 – 2:05 · Interactive Decision Tool: Aquifer Manager (15–20 sec)
- **[ON SCREEN — Scene 5 (`game/index.html` embedded in `#gameFrame`)]:** Pilot moves pumping slider up to `135%` in a Drought year, advances turns, and points to the tilting canal and clay compaction readout; then resets and shows `65%` sustainable balance.
- **[SPEAKER]:**
  "Maps tell you what happened; our **Aquifer Manager** simulator — seeded dynamically with the Central Valley's observed **`−26.4 cm/yr` summer drawdown ceiling** — lets growers and water boards feel the 10-year trade-off. Cranking the pump through droughts saves this season's harvest, but irreversibly crushes deep clay pore space, bends the aqueduct, and wipes out late-decade income."

### 2:05 – 2:40 · How We Know (Physics, GNSS Validation & Scientific Honesty)
- **[ON SCREEN — Scene 4 (`GNSS vs NISAR` summary & Scene 6 `How we built it` SVG diagram)]:** Show real daily vertical GNSS station traces from Nevada Geodetic Laboratory alongside NISAR pixel extractions.
- **[SPEAKER]:**
  "Every step follows open physical principles: L-band 24-centimetre radar penetrates canopy cover; our pipeline converts unwrapped phase via `−λ / 4π` using each granule's exact center wavelength, masks decoherent water (`coherence >= 0.3`), strips unwrapping glitches, removes the ionospheric screen and topographic plane, and checks itself against **10 continuous GNSS stations** across the valley — achieving **`1.00 cm` median RMSE** (`1.33 cm` mean RMSE, down to `0.64 cm` at `P566`) and **`r = 0.90` correlation** at peak stations **`CAHA`** and **`HANF`**.
  And we are explicit about limits: NISAR science data are currently marked **provisional** — sensor calibration is performed by NASA–JPL and ISRO, not our team."

### 2:40 – 3:00 · Road Ahead & Close
- **[ON SCREEN — `/web3d/` 3D "Breathing Earth" interactive mesh + GitHub repository URL]:**
- **[SPEAKER]:**
  "Looking forward, separating seasonal elastic bounce in winter from permanent clay collapse lets regions track true aquifer death in real time. Because L-band radar never blinks for clouds, water managers can finally manage what they couldn't see. Thank you — and we welcome your questions."

### Prepared Jury Q&A Notes
- See full **15-question card** in `docs/story/judge_faq.md` (`quality: provisional` vs. `preview`, LOS vs. vertical `cos θ`, ionosphere + Copernicus DEM GLO-90 deramp, 108-day linear rate caution, GNSS station-by-station spread, Karapınar sinkhole predictability limits, and AI disclosure).

---

## 2. 30-Second Video Script & English `.srt` Subtitles

**Target length:** `30.0 seconds` (`00:00:00,000` to `00:00:30,000`).  
**Visual rhythm:** Fast-cut web capture + clean overlay captions; every cited statistic matches `data/*/summary.json`, `validation.json`, and `assets.json`.

| Time | Visual Cue | Spoken Narration (English) |
|---|---|---|
| `0:00 – 0:04` | Web hero → Holme Fen (`1851` post `~4 m`) + clouds clearing over UK radar swipe | "Over centuries of draining aquifers, dry farmland doesn't wait to sink — it collapses beneath our feet." |
| `0:04 – 0:09` | Scene 1 swipe slider moving across Fens `2026-10-20` cloudy optical vs bright NISAR radar | "While optical cameras stall under clouds, NASA–ISRO NISAR's 24-centimetre L-band radar sees straight to the ground." |
| `0:09 – 0:15` | Scene 2 time-lapse across Central Valley (`2026-06-28 → 2026-10-14`) + `p01` Terra Bella click | "Across California's Central Valley, 7 provisional NISAR pairs measure up to −7.8 cm of sinking in 108 summer days." |
| `0:15 – 0:20` | GNSS validation (`1.00 cm` median RMSE) + Karapınar (`−5.9 cm` LOS) with 29 sinkhole pins | "Checked against 10 GNSS stations, and extended to Karapınar's −5.9 cm basin subsidence and 29 sinkholes." |
| `0:20 – 0:26` | Aquifer Manager game slider dragged in drought turn, surface dropping & aqueduct tilting | "Our browser simulator turns gigabytes of radar math into a 10-year water decision anyone can test." |
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
Aquifer Manager turns radar rates into a 10-year groundwater trade-off for farms and planners.

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
- **Observation (`2026-06-28 → 2026-10-14`):** `7` provisional ascending Track 34 NISAR pairs show peak LOS subsidence of **`−7.8 cm`** (`~−10.1 cm` vertical est. at `39.1°` near `6 km N of Terra Bella`; linear summer rate est. `−26.4 cm/yr`).
- **Critical Infrastructure:** Out of `645` evaluated corridors, `81` are high-risk, led by **Tulare Irrigation District Canal** (`57.01 mm/km`) and **California Aqueduct** (`49.12 mm/km` over `102.8 km`).
- **Interactive UX:** Click any valley coordinate for cumulative displacement history in plain language (`web/` & 3D `web3d/`).

### Slide 4 · How We Know: Independent GNSS Validation
- **Ground Truth:** Daily `IGS20/NA` vertical time series from **10 Nevada Geodetic Laboratory stations** inside the NISAR frame.
- **Method:** `3×3 px` pixel extraction projected from LOS to vertical via per-pixel incidence angle (`LOS / cos(θ)`).
- **Agreement:** **1.00 cm median RMSE** (`1.33 cm` mean RMSE across 10 stations; `0.64 cm` RMSE at `P566`), with **`r = 0.90` correlation** at deforming valley sites `CAHA` (`0.75 cm` RMSE) and `HANF` (`0.83 cm` RMSE).

### Slide 5 · Global Transferability: Karapınar Basin & Sinkholes (Türkiye)
- **Observation (`2026-06-26 → 2026-10-12`):** `8` provisional descending Track 7 NISAR pairs measure up to **`−5.9 cm` LOS** (`~−8.0 cm` vertical est. at `42.0°`, `−20.0 cm/yr` summer rate est.) **`2 km W of Karapınar`**.
- **Karst Inventory:** Overlays **29 field-verified sinkholes** (from `104` regional *obruk* survey records, reaching `80 m` deep at Akviran) strictly inside `[33.3, 37.6, 33.8, 37.9]`.
- **Honesty Guard:** Explicitly shows regional groundwater drawdown context without claiming InSAR predicts exact sudden roof-collapse dates.

### Slide 6 · Decision Tool: Aquifer Manager (Physical Simulator)
- **Empowering Non-Experts:** Single-page browser simulator (`game/index.html`) driven dynamically by `data/central_valley/summary.json` (`−26.4 cm/yr` ceiling).
- **10-Year Trade-Off:** Pure physics model (zero AI illustrations) letting users adjust pumping (`0%–150%`) across stochastic weather regimes to balance crop income against irreversible clay compaction and canal slope stress.

### Slide 7 · Scientific Integrity, Provenance & AI Disclosure
- **Calibration Notice:** NISAR data used here are **provisional** (`CRID P05023`); sensor calibration and validation are performed by the NISAR project (NASA–JPL / ISRO), not by our team.
- **Open & Reproducible:** Pure Python/NumPy pipeline (`pytest`-verified phase-to-cm tests) + interactive MapLibre & Three.js (`web3d/`) hosted statically.
- **AI Transparency:** Site hero/editorial artwork uses tagged `"AI-generated illustration"` badges (zero in `docs/story/slides.html` or `game/`); zero measurement data are AI-generated. Coding & QA assistance provided by Claude and Gemini/Antigravity.
