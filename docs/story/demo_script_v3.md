# NISAR Pulse — 60-Second Backup Screen-Recording Script (`docs/story/demo_script_v3.md`)

> **Target:** `60.0 s` (`1920×1080`, `30 fps`, real live site capture, **zero AI-generated images**)  
> **Source URL:** `https://keremsumer2010-tech.github.io/aseltech/` (or local `http://localhost:8000/web/index.html`)  
> **Mandatory Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## Shot-by-Shot 60-Second Flow

| Time | Duration | Screen / URL & Action | Burned-in English Subtitle / Voiceover |
|---|---:|---|---|
| `0:00–0:10` | `10 s` | **Home (`index.html`):** Load Hero (`#heroMap`) showing the four `.stats` cards (`−7.8 cm` LOS, `240 km² <= −5 cm`, `1.0 cm` GPS RMSE, `81 / 645` tilting corridors); scroll briefly past `#compare` (`20 Oct 2026` cloud vs. NISAR GCOV radar). | *"In summer 2026, provisional NASA–ISRO NISAR L-band radar sees through clouds and crops to map −7.8 cm of sinking in California's Central Valley, checked within 1.0 cm against 10 GPS stations."* |
| `0:10–0:24` | `14 s` | **Global Atlas (`atlas.html`):** Click **Atlas** in the top nav; show the **29-region** global map (`16` reliable, `13` indicative) ranked over the common `93`-day window (`2026-06-28` to `2026-09-29`), hovering the QC badge (`Semarang` 12.1 cm phase-jump caught & fixed). | *"Our open pipeline scales to 29 basins worldwide on a common 93-day window. Automated QC caught our own 12.1 cm phase-jump error in Semarang and isolated noisy regions as indicative only."* |
| `0:24–0:36` | `12 s` | **Konya Panel (`atlas.html` → Konya Plain):** Click **Konya Plain (#1 reliable)** in the atlas table/map to open the Konya panel (`−11.0 cm/100d` common, `−9.6 cm` LOS, `11.6%` low-coverage caution, `6.4×` faster sinking within `1 km` of 29 Karapınar sinkholes). | *"Konya Plain leads reliable basins at −11.0 cm per 100 days (flagged with a low-coverage caution), where land within 1 km of 29 sinkholes sinks 6.4× faster than background plateau."* |
| `0:36–0:46` | `10 s` | **Results & Science (`science.html`):** Open `science.html` and scroll smoothly across the `results_registry.json` cards (`atlas_feature`, `opera_check`, `exposure`, `storage_loss`, `validation_report`). | *"Every headline result—from 1,479,844 residents on fast-sinking ground to 0.317 km³/yr permanent aquifer storage loss—traces directly to open JSON datasets and peer-reviewed checks."* |
| `0:46–1:00` | `14 s` | **Simulator (`game/index.html`):** Open **Valley Under Pressure**, click **`2. Multi-Year Drought`** in Classroom Mode, step across `24` months showing permanent clay compaction below the preconsolidation threshold; hold final `3 s` on the calibration footer. | *"In our 24-month simulator calibrated to Terra Bella, over-pumping crushes clay irreversibly. NISAR data are provisional; calibration and validation are by NASA–JPL and ISRO."* |

---

## Pre-Recording Checklist

- Use `1920×1080` at `100%` browser zoom, bookmarks bar hidden (`Ctrl+Shift+B`), Do Not Disturb enabled.
- Confirm zero console errors (`Ctrl+Shift+I`) and zero missing tiles/figures before recording.
- Export MP4 (`H.264`, `<= 10 MB`) and verify `ffprobe` duration `<= 60.0 s`.
