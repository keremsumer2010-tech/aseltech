# 7-Slide Demo Adaptation & Presenter Notes (`docs/story/slides_notes.md`)

**Owner:** PC8 (`M3hmeT1888`) · **Target:** [`docs/story/slides.html`](slides.html) & Space Apps Demo Submission (`docs/CALISMA_HARITASI.md` PC8 Item 2)  
**Context:** Because the 30-second video capture is paused (`docs/CALISMA_HARITASI.md` PC6 #5), Space Apps rules (`docs/story/submission_rules.md` §2.B) allow submitting a **≤ 7-slide English presentation** (`slides.html` or its exported PDF) as the official **Link to Project "Demo"**. This document provides:
1. Slide-by-slide **30-second / 3-minute presenter notes and plain-English captions** aligned to `slides.html`.
2. **Exact update notes for PC4** to bring `slides.html` up to date with the newest Saturday evening datasets (`central_valley_fullyear`, `delta`, `konya_plain`, `karapinar_p172`, `global`, `exposure`).
3. **Pre-submit slide/PDF verification checks**.

---

## 1. Slide-by-Slide Presenter Notes & Self-Contained Captions (Slides 1–7)

> **Pacing Guide:** Judges stop reviewing at Slide 7. If read silently by a judge, each slide must stand on its own without audio; if presented live in **3 minutes**, spend **20–30 seconds per slide**.

### Slide 1 / 7 — Hook & Problem (`Hook`)
- **On-Screen Anchor:** Holme Fen Iron Post (`~4.0 m` exposed since `1851`, `2.75 m` below sea level), Central Valley (`−7.8 cm` LOS, `28 Jun–14 Oct 2026`), Karapınar (`−5.9 cm` LOS, `26 Jun–12 Oct 2026`), and aquifer compaction schematic (`Figure 1`).
- **30-Second Jury Caption (Self-Contained Summary):**  
  *When groundwater is pumped faster than rain refills it—or organic peat is drained—subsurface clay and peat compact silently beneath farms, canals, and homes. Our open web platform turns multi-gigabyte NASA–ISRO NISAR L-band interferograms into plain-English displacement maps, infrastructure risk rankings, and a 24-month policy simulator.*
- **Live Presenter Cue (`0:00–0:25`):** Start with the 1851 Holme Fen iron post (`~4 m` above ground today) to make invisible underground compaction tangible, then introduce the two 2026 NISAR summer measurements (`−7.8 cm` in California, `−5.9 cm` in Karapınar).

### Slide 2 / 7 — All-Weather L-Band Advantage (`UK Clouds`)
- **On-Screen Anchor:** VIIRS optical (`20 Oct 2026`, `~98%` cloud) vs. same-day NISAR L2 GCOV radar preview (`Figure 2a/2b`), Holme Fen (`1–2 cm/yr` modern rate), Fens dual-pol `HH`/`HV` (`4.27` vs `3.49 dB`), and London Clay negative-control test (`status: below_detection`, `3σ = 3.62 cm`, `data/uk_clay/detection.json`).
- **30-Second Jury Caption:**  
  *Passive optical sensors fail under persistent cloud cover, whereas NISAR's 24 cm L-band radar images The Wash coastline and Fens drainage on the same day. Equally important, we report a negative control honestly: over Greater London (21 Jun–19 Oct 2026, 9 pairs), single-season atmospheric noise (1.21 cm 1-sigma, 3.62 cm 3-sigma) exceeds expected 0.5–2.0 cm seasonal clay motion.*
- **Live Presenter Cue (`0:25–0:50`):** Point to the cloudy VIIRS frame vs. sharp NISAR coastline, then note that reporting London Clay as `"below detection limit for one season"` shows we do not overclaim noise as signal.

### Slide 3 / 7 — California Central Valley & Infrastructure Tilt (`Central Valley`)
- **On-Screen Anchor:** `2026-10-14` cumulative LOS map (`Figure 3`, `−7.8 cm` LOS / `−10.1 cm` vertical *estimate* at `6 km N of Terra Bella`, `1,578.27 km² <= −2 cm`, `239.54 km² <= −5 cm`), `p01` time series, and `Tulare Irrigation District Canal` profile (`Figure 4`, `57.01 mm/km`, `California Aqueduct` `49.12 mm/km`, `81/645` high-risk segments).
- **30-Second Jury Caption:**  
  *Extending NASA's Land Subsidence StoryMap (2013–2017 airborne UAVSAR) into 2026 from space, 7 provisional Track 34 NISAR pairs show 1,578 km² of the San Joaquin Valley sinking more than 2 cm LOS in 108 days. Differential tilt reaches 57.01 mm/km along the Tulare Irrigation District Canal and 49.12 mm/km along 102.8 km of the California Aqueduct, with top-10 rankings 100% invariant under ±25% threshold tests.*
- **Live Presenter Cue (`0:50–1:20`):** Connect directly to NASA's own Land Subsidence StoryMap (`Peacock et al., 2024`), then highlight that `79.2%` (`1,251.4 km²`) of California's `> 2 cm` sinking footprint is active farmland (`Citrus 355.6 km²`, `Pistachios 230.9 km²`) and `71,701` residents live on those valid pixels (`data/central_valley/exposure.json`).

### Slide 4 / 7 — Independent GPS Comparison & Multi-Geometry Checks (`GNSS Comparison`)
- **On-Screen Anchor:** 10-station NGL GPS scatter (`Figure 5`, `r = 0.924`, `1.37 cm` final RMSE, `1.00 cm` median TS RMSE), `CAHA` trace (`Figure 6`, `RMSE = 0.75 cm`, `r = 0.90`), Track 34 vs. Track 114 cross-check (`6,719` 1-km blocks, `85%` sign agreement for `|d| > 3 cm`), and two-orbit vector inversion (`−7.2 cm` vertical vs. `−0.1 cm` east-west at Alpaugh).
- **30-Second Jury Caption:**  
  *Every radar map is checked three independent ways: against 10 continuous Nevada Geodetic Laboratory GPS gauges (r = 0.924, 1.00 cm median RMSE), against descending Track 114 across 6,719 blocks (85% sign agreement for |d| > 3 cm), and by inverting ascending and descending LOS vectors to confirm that Alpaugh sank −7.2 cm vertically with negligible sideways drift.*
- **Live Presenter Cue (`1:20–1:50`):** Emphasize that we did not trust a single orbit or unverified phase values—GNSS, dual-orbit geometry, and Cramér-Rao pixel phase uncertainty (`0.294 cm` median) all agree.

### Slide 5 / 7 — Konya–Karapınar Basin & Sinkholes (`Karapınar`)
- **On-Screen Anchor:** Karapınar `2026-10-12` cumulative LOS map (`Figure 7`, `−5.9 cm` LOS / `−8.0 cm` vertical *estimate* `2 km W of Karapınar`), `p01` time series (`Figure 8`), `29` verified sinkholes (`0–1 km` ring `−4.15 cm` LOS = `6.4×` background `−0.65 cm`; `1.04 km` block permutation `p = 0.0001`), and `19.74 mm/km` road tilt near `Köken Obruğu-II`.
- **30-Second Jury Caption:**  
  *Applying the same pipeline to our home basin in Konya, Türkiye maps −5.9 cm LOS subsidence in Karapınar (cross-checked by ascending Track 172 at 12-point r = 0.767, RMSE = 1.12 cm LOS) and −9.6 cm LOS across the wider Konya Plain. Pixels within 1 km of 29 verified karst sinkholes sink 6.4 times faster than the far-field plateau, providing regional aquifer drawdown context without claiming to predict sudden roof-collapse dates.*
- **Live Presenter Cue (`1:50–2:20`):** Mention both the Track 172 independent cross-check (`p01` time-series `r = 0.798`) and the `69,854` Konya Closed Basin residents (`118,485` interpolated; `16,822` in `> 5 cm` LOS; including `11,572` in Karapınar) living on `> 2 cm` LOS sinking ground (`data/konya_plain/exposure.json`, `data/karapinar/exposure.json`).

### Slide 6 / 7 — Interactive Tools & 11-Month Decomposition (`Simulator & 3D`)
- **On-Screen Anchor:** `web/` 2D Story Map, `web3d/` Three.js 3D Surface Explorer (`10,000×–150,000×`), and `game/` *Valley Under Pressure* 24-month Terzaghi compaction simulator (`Figure 9`, `N = 1,000` Monte Carlo sensitivity, `k = 0.6232`).
- **30-Second Jury Caption:**  
  *Static maps alone do not change pumping behavior. Our browser suite pairs a multi-region 2D explorer (`web/explorer.html`) and a Three.js 3D basin viewer (`web3d/`) with Valley Under Pressure, a 24-month Terzaghi consolidation simulator matched to NISAR's Terra Bella summer measurement (−10.1 cm vertical) so growers and water boards can test pumping limits against irreversible clay collapse.*
- **Live Presenter Cue (`2:20–2:40`):** Point to the Monte Carlo uncertainty band (`Figure 9`) and mention our experimental 11-month `mixed` chain (`24 Nov 2025–14 Oct 2026`) separating `−16.8 cm/yr` LOS permanent compaction from `11.7 cm` peak-to-peak seasonal rebound near Earlimart (`data/central_valley_fullyear/decomp.json`).

### Slide 7 / 7 — Provenance, Global Transferability & Open Science (`Integrity & AI`)
- **On-Screen Anchor:** Mandatory NISAR provisional attribution (`Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team`), strict `beta-precal` vs. `provisional` separation, `pytest` coverage, zero AI-generated scientific imagery, and GitHub link.
- **30-Second Jury Caption:**  
  *NISAR data are provisional; calibration and validation are carried out by NASA–JPL and ISRO, not our team. Automated time-series QC flagged single-cycle unwrapping or noisy steps (e.g., Semarang, Delhi, Beijing, Bangkok) as indicative only, keeping Konya Plain at rank 1 ahead of Mashhad, Central Valley, Eloy, and Mexico City across 20 global regions (with Tehran re-computed at −7.4 cm LOS off-basin), verified by pytest suites and open data.*
- **Live Presenter Cue (`2:40–3:00`):** Close on scientific honesty, open-source reproducibility (`github.com/keremsumer2010-tech/aseltech`), and readiness for Q&A.

---

## 2. Recommended Updates for `docs/story/slides.html` (For PC4 Before PDF Export)

When PC4 refreshes `docs/story/slides.html` under `docs/CALISMA_HARITASI.md` PC4 #2, the following verified Saturday evening additions should be woven cleanly into the existing 7 slides without exceeding **7 slides**:

| Target Slide | Addition to Include | Verified Source |
|---|---|---|
| **Slide 2** | Update `UK` dual-pol line from `data/fens/polarizations.json`: mean temporal range `4.27 dB` (`HH`), `3.49 dB` (`HV`), `1.36 dB` (`HV/HH` ratio) + `80.4%` summer L-band coherence vs. C-band `OPERA DISP-S1` (`docs/story/cross_sensor.md`). | `data/fens/polarizations.json`, `data/central_valley_s1/cross_sensor.json` |
| **Slide 3** | Add **11-month `mixed` decomposition** note (`−16.77 cm/yr` LOS permanent vs. `11.67 cm` peak-to-peak seasonal at Earlimart, `24 Nov 2025–14 Oct 2026`), **O1 permanent storage loss** (`0.317 km³/yr`, `0.066–0.320 km³/yr` range, `~0.49× Millerton Lake`), **Delta levees** (`−1.3 cm` LOS peak, `−11.36 cm` local levee sample), and **USDA CDL + WorldPop exposure** (`71,701` residents, `79.2%` cultivated cropland led by `355.6 km²` citrus). | `data/central_valley_fullyear/decomp.json`, `data/central_valley_fullyear/storage_loss.json`, `data/delta/summary.json`, `data/central_valley/exposure.json` |
| **Slide 5** | Add **Konya Closed Basin** (`−9.6 cm` LOS peak south of Konya city, `data/konya_plain/summary.json`), **Karapınar Track 172 cross-check** (`12-point r = 0.767`, `RMSE = 1.12 cm` LOS; `p01` `r = 0.798`), and **WorldPop + ESA WorldCover exposure** (`69,854` Konya Basin residents `> 2 cm` LOS, `16,822` `> 5 cm` LOS; `11,572` in Karapınar). | `data/konya_plain/summary.json`, `analysis/pc8/kp_p7_vs_p172.json`, `data/konya_plain/exposure.json` |
| **Slide 6 / 7** | Add **Global Atlas (20 regions)** QC-checked Top 5 (`1 Konya Plain −8.9 cm/100d`, `2 Mashhad −7.2 cm/100d`, `3 Central Valley −7.2 cm/100d`, `4 Eloy −6.7 cm/100d`, `5 Mexico City −5.8 cm/100d`), **Tehran −7.4 cm LOS** (off-basin reference), single-sentence QC story (`Semarang, Delhi, Beijing, Bangkok` marked indicative/`Under revision`), GHSL exposure (`1,508,817` `< -5 cm/108d`), and **`web/explorer.html`** multi-region dashboard pill. | `data/global/atlas.json`, `data/global/vital_signs.json`, `docs/story/atlas_top5_check.md`, `web/explorer.html` |

---

## 3. Pre-Submission Print/PDF & Access Checklist (`submission_rules.md` §2.B)

1. Verify `docs/story/slides.html` renders cleanly at `16:9` (`1920×1080`) and prints to a clean **7-page PDF** (`@media print` in `slides.html` should place one `.slide` per page if exported as PDF).
2. Confirm **no slide exceeds 7** (`1 / 7` to `7 / 7`).
3. Confirm the mandatory calibration sentence (*"NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."*) appears visibly on the deck and no NASA/ISRO logo is embedded.
4. Test the live public URL (`https://keremsumer2010-tech.github.io/aseltech/docs/story/slides.html`) in an **incognito browser window** before pasting into the Space Apps **Link to Project "Demo"** field.
