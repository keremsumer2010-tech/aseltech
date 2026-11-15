# 30-Second Demo Video Narration Script (`docs/story/narration_script.md`)

**Owner:** PC8 (`M3hmeT1888`) · **For:** PC6 (`docs/story/media/demo_30s.mp4` voiceover & subtitle burn-in)  
**Target Duration:** Strictly **≤ 30.0 seconds** (`00:00.0` to `00:30.0`, aligned shot-for-shot with [`docs/story/video_shotlist.md`](video_shotlist.md) and [`docs/story/video_subtitles.srt`](video_subtitles.srt))  
**Total Spoken Word Count:** **76 words** (~152 words per minute natural speaking pace = `29.6 seconds` with half-second breaths between cues)  
**Style Compliance:** Plain English (`docs/REVIEW_1500.md`), zero banned buzzwords, zero exclamation marks, exact repository numbers from `data/*/summary.json`, `data/central_valley/validation.json`, and `data/*/assets.json`.

---

## 1. Full Spoken Narration Copy (76 Words — Read Straight Through)

> **[00:00.0 – 00:04.2 | Shot 1 — Hero & Holme Fen Iron Post]**  
> When we drain deep groundwater faster than rain refills it, the land itself sinks.
>
> **[00:04.2 – 00:09.0 | Shot 2 — UK Fens Cloud vs. NISAR Radar Swipe]**  
> While optical satellites are blinded by clouds, NISAR L-band radar sees right through them.
>
> **[00:09.0 – 00:15.0 | Shot 3 — Central Valley 108-Day Subsidence Map]**  
> In California's Central Valley, provisional NISAR tracks up to minus seven point eight centimeters line-of-sight across one hundred and eight days.
>
> **[00:15.0 – 00:20.0 | Shot 4 — Canal Tilt, GNSS Validation & Karapinar Sinkholes]**  
> Tulare Canal slopes hit fifty-seven millimeters per kilometer, ten GPS stations agree at one centimeter median error, and Karapinar sinks minus five point nine centimeters near twenty-nine sinkholes.
>
> **[00:20.0 – 00:26.0 | Shot 5 — Valley Under Pressure 24-Month Simulator]**  
> Our simulator turns these radar rates into a twenty-four-month trade-off between pumping, clay collapse, and canal loss.
>
> **[00:26.0 – 00:30.0 | Shot 6 — 3D Surface Explorer & Provisional Calibration Notice]**  
> NISAR Vision: Follow the Water. Provisional data; calibration by NASA-JPL and ISRO.

---

## 2. Cue-by-Cue Timing, Subtitle Sync & Source Verification Table

| Cue | Timecode (`video_shotlist.md`) | Dur. | Spoken Words | Spoken Narration (`narration_script.md`) | Burned-in Subtitle (`video_subtitles.srt`) | Verified Repo Source |
|---|---|---:|---:|---|---|---|
| **1** | `00:00.0 – 00:04.2` | `4.2 s` | 14 | "When we drain deep groundwater faster than rain refills it, the land itself sinks." | `When we drain deep groundwater faster than rain refills it, the land itself sinks.` | [`docs/story/holme_fen.md`](holme_fen.md) (`~4 m` since `1851`) |
| **2** | `00:04.2 – 00:09.0` | `4.8 s` | 14 | "While optical satellites are blinded by clouds, NISAR L-band radar sees right through them." | `While optical satellites are blinded by clouds, NISAR L-band radar sees right through them.` | [`data/uk/meta.json`](../../data/uk/meta.json) (`2026-10-20`, `preview`) |
| **3** | `00:09.0 – 00:15.0` | `6.0 s` | 15 | "In California's Central Valley, provisional NISAR tracks up to -7.8 cm line-of-sight across 108 days." | `In California's Central Valley, provisional NISAR tracks up to -7.8 cm LOS (-10.1 cm vertical) across 108 days.` | [`data/central_valley/summary.json`](../../data/central_valley/summary.json) (`-7.8 cm` LOS, `-10.1 cm` vert. *est.*) |
| **4** | `00:15.0 – 00:20.0` | `5.0 s` | 19 | "Tulare Canal slopes hit 57 mm/km, 10 GPS stations agree at 1 cm median error, and Karapinar sinks -5.9 cm near 29 sinkholes." | `Tulare Canal slopes hit 57 mm/km; GNSS agrees at 1.00 cm median RMSE; Karapinar sinks -5.9 cm near 29 obruks.` | [`data/central_valley/assets.json`](../../data/central_valley/assets.json), [`validation.json`](../../data/central_valley/validation.json), [`data/karapinar/summary.json`](../../data/karapinar/summary.json) |
| **5** | `00:20.0 – 00:26.0` | `6.0 s` | 15 | "Our simulator turns these radar rates into a 24-month trade-off between pumping, clay collapse, and canal loss." | `Valley Under Pressure turns NISAR rates into a 24-month groundwater trade-off of clay collapse and canal loss.` | [`game/index.html`](../../game/index.html), [`game/model.js`](../../game/model.js) |
| **6** | `00:26.0 – 00:30.0` | `4.0 s` | 11 | "NISAR Vision: Follow the Water. Provisional data; calibration by NASA-JPL and ISRO." | `NISAR Vision: Follow the Water. Provisional NISAR L2 GUNW data (NASA-JPL / ISRO calibration).` | [`docs/story/calibration_note.md`](calibration_note.md) |

---

## 3. Recording & Pronunciation Notes

- **NISAR:** Pronounced *"NYE-sar"* (`NASA-ISRO Synthetic Aperture Radar`).
- **Karapınar:** Pronounced *"Kah-rah-puh-NAR"* (or plain English *"Kah-rah-pee-nar"*).
- **Pacing tip:** Keep total audio completion at **`29.5–29.8 seconds`** so the video file never exceeds the `30.00 s` Space Apps hard limit.
