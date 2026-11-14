# 30-Second Space Apps Demo Video — Recording Shotlist (`docs/story/video_shotlist.md`)

> **Operator:** Kerem / PC1 · **Target Duration:** Strictly **≤ 30.0 seconds** (`Space Apps` hard cap verified in [`docs/story/submission_rules.md`](submission_rules.md)) · **Subtitles:** Matched verbatim to [`docs/story/pitch.md`](pitch.md) §2 (`video_30s.srt`).

## Pre-Recording Setup Checklist

1. Serve the repo cleanly from root: `python3 -m http.server 8000`
2. Open `http://localhost:8000/web/` in a clean **1920×1080** browser window (`100%` zoom, bookmarks bar & DevTools hidden, `2×` playback speed off).
3. Keep `http://localhost:8000/web3d/` open in a **second pre-loaded browser tab** (California tab active, epoch at `2026-10-14`, orbit camera ready) for Shot 6.
4. Record raw silent screencast at **60 fps**; burn in or attach the English `.srt` subtitles below (`Arial / Inter SemiBold`, bottom center) and record voiceover cleanly at ~135 WPM.

---

## Shot-by-Shot Screen Capture Table (`30.0 s` Total)

| Order | Timecode | Dur. | Page / Section | Exact Mouse & UI Actions (PC1 / Kerem) | On-Screen English Subtitle (`video_30s.srt`) |
|---|---|---|---|---|---|
| **Shot 1** | `00:00.0 – 00:04.2` | `4.2 s` | `web/#hero` → `web/#uk` (`#holmeCard`) | Start on Hero title *"Follow the water."*, smoothly scroll down so `#uk` header + **Holme Fen** card fill left panel. Keep cursor steady over Holme Fen text (`~4 m` above peat since `1851`). | `When we drain deep groundwater faster than rain refills it, the land itself sinks.` |
| **Shot 2** | `00:04.2 – 00:09.0` | `4.8 s` | `web/#uk` (`#compare` swipe) | Drag `#compareRange` slider slowly from `5%` (`VIIRS 2026-10-20` cloud blanket) across to `95%` (cloud-free `NISAR L2 GCOV` Wash coastline), then settle around `65%`. | `While optical satellites are blinded by clouds, NISAR L-band radar sees right through them.` |
| **Shot 3** | `00:09.0 – 00:15.0` | `6.0 s` | `web/#usa` (`#cvPlay`, `#cvMap`) | Scroll directly to Scene 2 (`California, USA`). Click `#cvPlay` (`▶`) to animate `2026-06-28 → 2026-10-14`; at `12.0 s`, click the Terra Bella hotspot (`36.011°N, -119.022°E`) so `#cvChart` & `#cvSentence` (`−7.8 cm LOS`) populate cleanly. | `In California's Central Valley, provisional NISAR tracks up to -7.8 cm LOS (-10.1 cm vertical) across 108 days.` |
| **Shot 4** | `00:15.0 – 00:20.0` | `5.0 s` | `web/#usa` (canals & GNSS) → `web/#konya` | Briefly highlight `Tulare Irrigation District Canal` (`57.01 mm/km`) / `CAHA` GNSS trace (`RMSE 0.75 cm`), then cut/scroll cleanly to Scene 3 (`Karapınar, TR`) with `29` verified sinkhole markers over `-5.9 cm` LOS cumulative map. | `Tulare Canal slopes hit 57 mm/km; GNSS agrees at 1.00 cm median RMSE; Karapinar sinks -5.9 cm near 29 obruks.` |
| **Shot 5** | `00:20.0 – 00:26.0` | `6.0 s` | `web/#game` (`game/index.html`) | Scroll to Scene 5 (`Aquifer Manager`). Drag pumping slider up to `135%`, advance `3` drought years so groundwater table drops, clay compaction bar turns red, and infrastructure repair cost rises. | `Aquifer Manager turns radar rates into a 10-year groundwater trade-off for farms and planners.` |
| **Shot 6** | `00:26.0 – 00:30.0` | `4.0 s` | `/web3d/` Tab (`+ web/#how` end slate) | Switch to pre-loaded `web3d/` tab: smoothly orbit right-to-left around the extruded 3D San Joaquin Valley subsidence basin (`quality: provisional · CRID P05023` pill clearly visible in header), ending on title & repo link. | `NISAR Pulse: Follow the Water. Provisional NISAR L2 GUNW data (NASA-JPL / ISRO calibration).` |

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
Aquifer Manager turns radar rates into a 10-year groundwater trade-off for farms and planners.

6
00:00:26,000 --> 00:00:30,000
NISAR Pulse: Follow the Water. Provisional NISAR L2 GUNW data (NASA-JPL / ISRO calibration).
```

## Compliance Reminders (`submission_rules.md`)

- **Do not use** NASA or ISRO logos anywhere in the title card or end slate.
- **Do not cut** out the `provisional` quality badge or attribution line (`Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team`).
- **Keep final MP4 runtime `<= 29.8 s`** (leave a `0.2 s` buffer below `30.0 s`).
