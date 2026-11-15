# 30-Second Space Apps Demo Video — Recording Shotlist (`docs/story/video_shotlist.md`)

> **Compiled Deliverable (`365f767`):** [`docs/story/media/demo_30s.mp4`](media/demo_30s.mp4) (`29.62 s`, `1080p`, `24 fps`, `3,498,402 B`, burned-in English subtitles, zero agency logos) is generated reproducibly from real repository plots by [`analysis/pc6/make_demo_video.py`](../../analysis/pc6/make_demo_video.py). The manual browser screencast guide below mirrors the exact DOM flow for live demo capture (Operator: Kerem / PC3, strictly **<= 30.0 seconds** per [`docs/story/submission_rules.md`](submission_rules.md); subtitles matched to [`docs/story/pitch.md`](pitch.md) §2).

## Pre-Recording Setup Checklist

1. Serve the repo cleanly from root: `python3 -m http.server 8000`
2. Open `http://localhost:8000/web/` in a clean **1920×1080** browser window (`100%` zoom, bookmarks bar & DevTools hidden, `2×` playback speed off).
3. Keep `http://localhost:8000/web3d/` open in a **second pre-loaded browser tab** (California tab active, epoch at `2026-10-14`, orbit camera ready) for Shot 6.
4. Record raw silent screencast at **60 fps**; burn in or attach the English `.srt` subtitles below (`Arial / Inter SemiBold`, bottom center) and record voiceover cleanly at ~135 WPM, or submit [`docs/story/media/demo_30s.mp4`](media/demo_30s.mp4) directly.

---

## Shot-by-Shot Screen Capture Table (`30.0 s` Total — Aligned with Story 1–6 / Simulator / Science)

| Order | Timecode | Dur. | Page / Section & DOM Selector | Exact Mouse & UI Actions (PC3 / Kerem) | On-Screen English Subtitle (`video_30s.srt`) |
|---|---|---|---|---|---|
| **Shot 1** | `00:00.0 – 00:04.2` | `4.2 s` | `web/index.html#watch` & `#story` — Figure 0 + Story Chapters 1–2 (`#heroMap`, `#watch` `#cvVideo`, `[data-step="intro"]` → `[data-step="uk"]`, `#holmeText`) | Start on Hero map (`#heroMap`) & `.stats` bar, briefly flash `#watch` 108-day time-lapse (`#cvVideo` = `docs/story/media/cv_subsidence.mp4`), then scroll into Story Chapter 1 & Chapter 2 Holme Fen benchmark note (`~4 m` above peat since `1851`, `2.75 m` below sea level). | `When we drain deep groundwater faster than rain refills it, the land itself sinks.` |
| **Shot 2** | `00:04.2 – 00:09.0` | `4.8 s` | `web/index.html#story` — Story Chapter 2 (`[data-step="uk"]`, `#compare`, `#compareRange`, `#ukClay`) | Drag `#compareRange` slowly across `20 Oct 2026` cloudy VIIRS optical image (`#ukOptical`) to reveal the same-day NISAR L2 GCOV radar quick-look (`#ukRadar`, `Figure 1`) alongside `#ukClay` (`London clay below ±3.62 cm noise`). | `While optical satellites are blinded by clouds, NISAR L-band radar sees right through them.` |
| **Shot 3** | `00:09.0 – 00:15.0` | `6.0 s` | `web/index.html#story` — Story Chapter 3 (`[data-step="cv"]`, `#cvPlay`, `#slider`, `#readout`, `#pointChart`) | Click `#cvPlay` (`▶`) to step `28 Jun–14 Oct 2026`, then tap peak block `p01` (`6 km N of Terra Bella`, `36.011°N, 119.022°W`) so `#readout` and `#pointChart` (`−7.8 cm` LOS, `−10.1 cm` vertical estimate, `Figure 2`) update *(optional B-roll cut: `docs/story/media/cv_subsidence.mp4`)*. | `In California's Central Valley, provisional NISAR tracks up to -7.8 cm LOS (-10.1 cm vertical) across 108 days.` |
| **Shot 4** | `00:15.0 – 00:20.0` | `5.0 s` | `web/index.html#story` — Story Chapters 4–6 (`[data-step="gnss"]` `#gnssChart`/`#gnssTable` → `[data-step="risk"]` `#riskList` → `[data-step="kp"]` `#ringBox`/`#ringChart`/`#sinkList`) | Highlight Chapter 4 GPS validation (`CAHA`, `1.00 cm` median RMSE, `Figure 3`), Chapter 5 `Tulare Irrigation District Canal` (`57.01 mm/km`, `Figure 4`), and Chapter 6 Karapınar (`−5.9 cm` LOS, `26 Jun–12 Oct 2026`, `#ringChart` `4.2 cm` within `1 km` vs `0.6 cm` beyond `5 km`, `29` documented sinkholes in `#sinkList`, `Figure 5`). | `Tulare Canal slopes hit 57 mm/km; GNSS agrees at 1.00 cm median RMSE; Karapinar sinks -5.9 cm near 29 obruks.` |
| **Shot 5** | `00:20.0 – 00:26.0` | `6.0 s` | `web/index.html#play` — Simulator (`#play`, `#gameFrame` → `game/index.html`) | Scroll to Simulator (`#play`), select `Terra Bella` in `#gameFrame`, adjust pumping rate, and advance across the **24-month** simulation comparing simulated subsidence directly against NISAR measurements. | `Valley Under Pressure turns NISAR rates into a 24-month groundwater trade-off of clay collapse and canal loss.` |
| **Shot 6** | `00:26.0 – 00:30.0` | `4.0 s` | `web/index.html#how` + `web/science.html` (`#findings`, `#conv`, `#valid`, `#limits`, `#lit`, `#unc`, `#vreport`, `#dossier`) & `web3d/` (`#view3d`) | Orbit the extruded 3D basin mesh in pre-loaded `web3d/` tab (`quality: provisional · CRID P05023`), then cut cleanly to `#how` / `web/science.html` provisional attribution notice and findings sections (`Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.`). | `NISAR Vision: Follow the Water. Provisional NISAR L2 GUNW data (NASA-JPL / ISRO calibration).` |

---

## Exported English Subtitles (`video_30s.srt`)

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
NISAR Vision: Follow the Water. Provisional NISAR L2 GUNW data (NASA-JPL / ISRO calibration).
```

## Compliance Reminders (`submission_rules.md`)

- **Do not use** NASA or ISRO logos anywhere in the title card or end slate.
- **Do not cut** out the `provisional` quality badge or attribution line (`Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team`).
- **Keep final MP4 runtime `<= 29.8 s`** (leave a `0.2 s` buffer below `30.0 s`).

---

## Line-by-Line Subtitle & Claim Verification Matrix

Every spoken cue, numeric claim, and UI label in `video_30s.srt` was audited (`2026-11-14`) against committed repo JSON outputs and HTTP-200 literature sources:

| Cue | Timecode | Spoken Claims & Metrics | Verified Repo / Literature Source | Result |
|---|---|---|---|---|
| **Cue 1** | `00:00.0–00:04.2` | Groundwater depletion causing land sinking (`Holme Fen ~4 m` on-screen card since `1851`, `2.75 m` below sea level) | [`docs/story/holme_fen.md`](holme_fen.md) · [`docs/story/sources.md`](sources.md) §1 ([Great Fen](https://www.greatfen.org.uk/about-great-fen/heritage/holme-fen-posts), [Wikipedia](https://en.wikipedia.org/wiki/Holme_Fen), [Defra WP2](https://lowlandpeat.ceh.ac.uk/sites/default/files/2022-07/Policy-brief-note-WP2.pdf)) | **PASS (HTTP 200)** |
| **Cue 2** | `00:04.2–00:09.0` | Cloud obstruction vs. `24 cm` NISAR L-band `GCOV` radar (`2026-10-20` UK Fens pair) | [`data/uk/meta.json`](../../data/uk/meta.json) (`quality: "preview"`, `VIIRS_SNPP` + `NISAR_L2_PR_GCOV_..._20261020T192237`) | **PASS (HTTP 200)** |
| **Cue 3** | `00:09.0–00:15.0` | Central Valley `-7.8 cm` LOS, `-10.1 cm` vertical est., `108` days (`2026-06-28 → 2026-10-14`, `7` provisional pairs) | [`data/central_valley/summary.json`](../../data/central_valley/summary.json) (`max_subsidence_cm: -7.8`, `max_subsidence_vertical_cm_estimate: -10.1`, `incidence_deg_at_max: 39.1`, `n_pairs: 7`) | **PASS (Exact)** |
| **Cue 4** | `00:15.0–00:20.0` | `Tulare Canal` `57 mm/km` (`57.01 mm/km`), `1.00 cm` median GNSS RMSE, Karapınar `-5.9 cm` LOS, `29` obruks | [`data/central_valley/assets.json`](../../data/central_valley/assets.json) (`57.01 mm/km`, `81` high-risk) · [`data/central_valley/validation.json`](../../data/central_valley/validation.json) (`median RMSE 1.00 cm`, `10` stations) · [`data/karapinar/summary.json`](../../data/karapinar/summary.json) (`-5.9 cm`) · [`data/karapinar/sinkholes.geojson`](../../data/karapinar/sinkholes.geojson) (`29` Features) | **PASS (Exact)** |
| **Cue 5** | `00:20.0–00:26.0` | `Valley Under Pressure` (`24-month` simulation reading NISAR rates) | [`game/index.html`](../../game/index.html) (`Month 0 / 24`, `#pumpSlider`, `Over-Pump` preset) · [`game/model.js`](../../game/model.js) (`summary.json` target, Terzaghi compaction, canal loss vs. KVPR/USGS) | **PASS (Updated to v2)** |
| **Cue 6** | `00:26.0–00:30.0` | `Provisional NISAR L2 GUNW` + `NASA-JPL / ISRO calibration` notice & `web3d/` `CRID P05023` pill | [`docs/story/calibration_note.md`](calibration_note.md) · [`web3d/index.html`](../../web3d/index.html) (`quality: provisional · CRID P05023`) · [`docs/story/submission_rules.md`](submission_rules.md) | **PASS (Compliant)** |
