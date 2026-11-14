# NISAR Pulse — Follow the Water: Pitch, Video Script & Slide Deck

> **Placeholder Policy (Rule K-2):** All site measurements and derived statistics below use `{PLACEHOLDER}` tokens mapped to repository outputs so no unverified or hardcoded numbers ever enter the script. Replace each token once the corresponding file in `data/` is finalized.

## Placeholder Source Map

| Placeholder | JSON / Doc Source | Field / Key |
|---|---|---|
| `{HOLME_FEN_M}` | `web/index.html` / `docs/story/sources.md` (PC4) | Verified post height above peat soil |
| `{CV_MAX_CM}` | `data/central_valley/summary.json` | `max_subsidence_cm` |
| `{CV_VERT_CM}` | `data/central_valley/summary.json` | `max_subsidence_vertical_cm_estimate` |
| `{CV_RATE_CM_YR}` | `data/central_valley/summary.json` | `rate_cm_per_yr_estimate` |
| `{CV_PERIOD}` | `data/central_valley/summary.json` | `period[0]` → `period[1]` |
| `{CV_N_PAIRS}` | `data/central_valley/summary.json` | `n_pairs` |
| `{GNSS_N_STATIONS}` | `data/central_valley/validation.json` | `n_stations` |
| `{GNSS_RMSE_CM}` | `data/central_valley/validation.json` | `overall_rmse_cm` |
| `{GNSS_CORR}` | `data/central_valley/validation.json` | `overall_corr` |
| `{TOP_CANAL_NAME}` | `data/central_valley/assets.json` | `top_segments[0].name` |
| `{TOP_CANAL_SLOPE_MM_KM}` | `data/central_valley/assets.json` | `top_segments[0].slope_mm_per_km` |
| `{N_SINKHOLES}` | `data/karapinar/sinkholes.geojson` | Verified catalog feature count |

---

## 1. Live Presentation Script (3 Minutes — Lincoln Local Pitch)

**Roles (`MASTER_PLAN.md §7`):**
- **Speaker:** Kerem (walks through the narrative and live site)
- **Live Demo Pilot:** Co-presenter (drives the sliders, map click, and Aquifer Manager)
- **Data Q&A Lead:** Mehmet (handles technical questions on NISAR GUNW math, GNSS validation, and limitations)

### 0:00 – 0:20 · Hook (The Iron Post)
- **[ON SCREEN — Hero & Holme Fen Card]:** Slow orbital/radar hero background; cursor settles on Scene 1 card (*"Britain under clouds"*).
- **[SPEAKER]:**
  "In the 1850s, farmers in the English Fens hammered an iron post flush with the surface of the peatlands. Today, that same iron pipe stands **`{HOLME_FEN_M}` metres** up in the air — not because the iron grew, but because draining the land caused the ground beneath Britain's richest farmland to collapse."

### 0:20 – 0:45 · Problem & Solution
- **[ON SCREEN — Drag Cloud Slider in Scene 1]:** Slide optical cloudy GIBS view across to reveal the cloud-free NISAR L-band GCOV radar image underneath.
- **[SPEAKER]:**
  "The same crisis is happening silently over every major pumped aquifer on Earth. Optical satellites are blind under cloud and struggle inside vegetated valleys, while raw radar interferometry lives inside multi-gigabyte HDF5 files only specialists can open.
  Our project, **NISAR Pulse — Follow the Water**, turns NASA-ISRO NISAR L-band interferograms into plain-language maps and a 10-year water-policy decision tool — all running live in any browser."

### 0:45 – 1:45 · Live Demo: Central Valley & Karapınar
- **[ON SCREEN — Scene 2 (`The dancing ground · USA`)]:** Press Play on the date slider (`{CV_PERIOD}` across `{CV_N_PAIRS}` provisional NISAR GUNW pairs). Click the hotspot south-southeast of Tulare Lake (`max_subsidence_location`) and show `#cvSentence` + sparkline + GNSS comparison.
- **[SPEAKER]:**
  "Step one: California's San Joaquin Valley. Between `{CV_PERIOD}`, cumulative NISAR line-of-sight measurements across `{CV_N_PAIRS}` provisional pairs show the valley floor dropping by up to **`{CV_MAX_CM}` centimetres** — roughly **`{CV_VERT_CM}` centimetres** vertical equivalent — around intensely irrigated clay beds.
  Tap any point on the map and the chart strips away radar jargon into one plain sentence for water managers. And when underground clay compacts irreversibly, surface irrigation canals tilt. Overlaying OpenStreetMap waterways reveals differential slopes reaching **`{TOP_CANAL_SLOPE_MM_KM}` mm/km** along **`{TOP_CANAL_NAME}`**."
- **[ON SCREEN — Scene 3 (`Konya's sinkholes · TR`)]:** Scroll to Karapınar; toggle sinkhole pins (`{N_SINKHOLES}` verified locations) over L-band phase displacement.
- **[SPEAKER]:**
  "Step two: Karapınar Basin in Konya, Türkiye, where agricultural overdraft drives sudden sinkhole collapse. Linking `{N_SINKHOLES}` documented sinkhole sites with NISAR radar tracks how wide regional drawdown concentrates stress before localized failures occur."

### 1:45 – 2:05 · Interactive Decision Tool: Aquifer Manager (15–20 sec)
- **[ON SCREEN — Scene 5 (`game/index.html` embedded in `#gameFrame`)]:** Pilot moves pumping slider up to `135%` in a Drought year, advances turns, and points to the tilting canal and clay compaction readout; then resets and shows `65%` sustainable balance.
- **[SPEAKER]:**
  "Maps tell you what happened; our **Aquifer Manager** game lets growers and water boards feel the 10-year trade-off. Cranking the pump through droughts saves this season's harvest, but irreversibly crushes deep clay pore space, bends the aqueduct, and wipes out late-decade income."

### 2:05 – 2:40 · How We Know (Physics, GNSS Validation & Scientific Honesty)
- **[ON SCREEN — Scene 4 (`GNSS vs NISAR` summary & Scene 6 `How we built it` SVG diagram)]:** Show real daily vertical GNSS station traces from Nevada Geodetic Laboratory alongside NISAR pixel extractions.
- **[SPEAKER]:**
  "Every step follows open physical principles: L-band 24-centimetre radar penetrates canopy cover; our pipeline converts unwrapped phase via `−λ / 4π` using each granule's exact center wavelength, masks decoherent water (`coherence >= 0.3`), strips unwrapping glitches, removes the ionospheric phase screen, and checks its own work against **`{GNSS_N_STATIONS}` independent continuous GNSS stations** across the Central Valley (`RMSE {GNSS_RMSE_CM} cm`, correlation `{GNSS_CORR}`).
  And we are explicit about limits: NISAR science data are currently marked **provisional** — sensor calibration is performed by NASA-JPL and ISRO, not our team."

### 2:40 – 3:00 · Road Ahead & Close
- **[ON SCREEN — Full-year decomposition roadmap + GitHub repository / live URL]:**
- **[SPEAKER]:**
  "Looking forward, separating seasonal elastic bounce in winter from permanent clay collapse lets regions track true aquifer death in real time. Because L-band radar never blinks for clouds, water managers can finally manage what they couldn't see. Thank you — and we welcome your questions."

### Prepared Jury Q&A Notes
- **"Is this fully calibrated?"** → Every layer clearly displays its quality badge (`provisional` or `illustrative`). Final radiometric/geometric calibration is performed by NASA-JPL and ISRO under the NISAR mission; our open-source converter transforms provisional L2 GUNW unwrapped phase directly and validates it independently against Nevada Geodetic Lab daily GNSS series.
- **"Are values line-of-sight or true vertical?"** → Base raster maps stay honestly in radar Line-of-Sight (negative = away from satellite ≈ subsidence) at ~39° incidence; GNSS point comparisons project NISAR LOS to vertical via `LOS / cos(incidence)` with horizontal-assumption caveats documented.
- **"What about ionosphere and troposphere noise?"** → Each GUNW product's shipped `ionosphere` screen is subtracted, and long-wavelength plane + linear DEM-correlated ramp is removed per pair while documenting expected few-cm residual tropospheric noise.

---

## 2. 30-Second Video Script & English `.srt` Subtitles

**Target length:** `30.0 seconds` (`00:00:00,000` to `00:00:30,000`).  
**Visual rhythm:** Fast-cut web capture + clean overlay captions; zero fabricated data values.

| Time | Visual Cue | Spoken Narration (English) |
|---|---|---|
| `0:00 – 0:04` | Holme Fen archival pole cut → clouds clearing over UK radar swipe | "Over centuries of draining aquifers, dry farmland doesn't wait to sink — it collapses beneath our feet." |
| `0:04 – 0:09` | Scene 1 swipe slider moving smoothly over Fens cloudy GIBS vs bright NISAR radar | "While optical cameras stall under clouds, NASA-ISRO NISAR's 24-centimetre L-band radar sees straight to the ground." |
| `0:09 – 0:15` | Scene 2 time-lapse pulsing red across San Joaquin Valley (`{CV_PERIOD}`) + map click chart | "Across California's Central Valley, NISAR tracks up to `{CV_MAX_CM}` cm of summer sinking in `{CV_PERIOD}` — linked directly to bending irrigation canals." |
| `0:15 – 0:20` | GNSS station scatter overlay (`{GNSS_RMSE_CM}` cm RMSE) + Karapınar sinkhole pins | "Validated against `{GNSS_N_STATIONS}` daily GPS stations, and extended to Karapınar's active sinkhole zones." |
| `0:20 – 0:26` | Aquifer Manager game slider dragged in drought turn, surface dropping & aqueduct tilting | "Our browser simulator turns gigabytes of radar math into a 10-year water decision anyone can test." |
| `0:26 – 0:30` | End slate with live site URL + "NISAR provisional data · NASA-JPL/ISRO calibration" | "NISAR Pulse — Follow the Water. Open science before the ground gives way." |

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
In California's Central Valley, provisional NISAR tracks up to {CV_MAX_CM} cm of sinking across {CV_PERIOD}.

4
00:00:15,000 --> 00:00:20,000
Differential slopes stress vital canals like {TOP_CANAL_NAME}, checked against {GNSS_N_STATIONS} GNSS stations.

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
- **Core Hook:** Holme Fen Iron Post (UK Fens, 1850s benchmark standing `{HOLME_FEN_M}` m above drained peat).
- **Problem:** Pumping aquifers lowers pressure inside compressible clay layers — once collapsed, storage capacity never recovers.

### Slide 2 · Why NISAR L-Band?
- **All-weather visibility:** 24 cm L-band radar penetrates dense cloud cover where optical sensors fail (UK Fens Live Swipe).
- **Vegetation penetration:** Maintains coherence across croplands better than short-wavelength C-band radar.
- **Data barrier removed:** Our pipeline distills ~2 GB GUNW HDF5 granules into lightweight web tiles and plain-English outputs.

### Slide 3 · Central Valley: Sinking Valley, Tilting Canals
- **Observation (`{CV_PERIOD}`):** `{CV_N_PAIRS}` provisional ascending Track 34 NISAR pairs show peak LOS motion of `{CV_MAX_CM}` cm (`~{CV_VERT_CM}` cm vertical est.).
- **Critical Infrastructure:** OpenStreetMap canal/rail overlay highlights differential slopes reaching `{TOP_CANAL_SLOPE_MM_KM}` mm/km along `{TOP_CANAL_NAME}`.
- **Interactive UX:** Click any valley coordinate for cumulative displacement history in plain language.

### Slide 4 · How We Know: Independent GNSS Validation
- **Ground Truth:** Daily `IGS20/NA` vertical time series from `{GNSS_N_STATIONS}` Nevada Geodetic Laboratory stations inside the NISAR frame.
- **Method:** Pixel extraction projected from LOS to vertical via exact per-pixel incidence angle (`LOS / cos(θ)`).
- **Agreement:** Overall RMSE `{GNSS_RMSE_CM}` cm (`r = {GNSS_CORR}` across concurrent provisional dates).

### Slide 5 · Global Transferability: Karapınar Sinkholes (Türkiye)
- **Geohazard:** Severe groundwater withdrawal in Konya Closed Basin threatens agricultural infrastructure.
- **Mapping:** Linking `{N_SINKHOLES}` documented sinkhole occurrences with NISAR Track 7 displacement patterns.
- **Same Open Pipeline:** Automated download, coherence/connected-component masking, and static JSON tile export.

### Slide 6 · Decision Tool: Aquifer Manager (Interactive Simulator)
- **Empowering Non-Experts:** Single-page browser simulator driven dynamically by `data/central_valley/summary.json`.
- **10-Year Trade-Off:** Adjust pumping (`0%–150%`) across stochastic `wet`, `normal`, and `drought` years to balance harvest revenue against irreversible clay compaction and canal repair penalties.

### Slide 7 · Scientific Integrity, Provenance & AI Disclosure
- **Calibration Notice:** NISAR data used here are **provisional**; sensor calibration and validation remain the responsibility of the NISAR project (NASA-JPL / ISRO).
- **Open & Reproducible:** Pure Python/NumPy pipeline (`pytest`-verified phase-to-cm tests) + zero-backend static web app on GitHub Pages.
- **AI Transparency:** Generative video/poster assets (Higgsfield) are strictly editorial/illustrative and clearly tagged `"AI-generated"`; zero measurement data are AI-generated. Coding assistance provided by Claude and Gemini.
