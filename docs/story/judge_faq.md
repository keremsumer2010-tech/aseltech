# Judge & Engineer FAQ (`docs/story/judge_faq.md`)

### 1. What does `provisional` mean for these NISAR measurements?
Every science layer in our atlas uses NASA-ISRO NISAR Level-2 `GUNW` products (`CRID P05023`, acquired on or after `2026-06-17`), which are still in early mission operations. Pre-calibration `beta` granules (`< 2026-06-17`) are excluded from our headline atlas and isolated into a separate `mixed` seasonal dataset. *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

### 2. Why report Line-of-Sight (LOS) displacement instead of pure vertical sinking?
InSAR measures one-dimensional motion along the radar's slanted Line of Sight (`~39.1°` incidence in Central Valley, `~42°` in Karapınar), so we keep base maps in honest LOS (`−λ / 4π × Δφ`). Vertical figures (`LOS / cos θ`, e.g., `−10.1 cm` vs. `−7.8 cm` LOS in Central Valley) are explicitly labeled as *estimates*. In California, dual-orbit Track 34 ascending vs. Track 114 descending (`6,719` 1 km blocks, `85%` sign agreement for `|d| > 3 cm`) further isolates `−7.2 cm` vertical subsidence with `−0.1 cm` east-west motion at Alpaugh.

### 3. Why rank 29 basins on a 93-day common window instead of annual `cm/yr` rates?
Summer-only linear extrapolation (`cm/yr`) overstates net multi-year subsidence because confined aquifers rebound elastically during winter recharge. Ranking all `29` basins on the identical `93`-day common window (`2026-06-28` to `2026-09-29`, normalized to `cm/100d` LOS) compares seasonal drawdown fairly without site-specific tuning.

### 4. How well do NISAR measurements match independent continuous GPS stations?
Across `10` continuous Nevada Geodetic Laboratory (`IGS20/NA`) GPS stations in California's Central Valley, NISAR vertical estimates achieve **`r = 0.924`** cross-station correlation and **`1.00 cm` median RMSE** (`0.82 cm` across `5` core Tulare stations). This GPS comparison is our primary independent validation.

### 5. Why is NASA JPL's OPERA DISP-S1 product a secondary check rather than a headline KPI?
Over Mexico City, our NISAR spatial pattern matches NASA JPL's `OPERA_L3_DISP-S1_V1` product at `10` points (`r = 0.912`), although OPERA covers winter and NISAR covers summer (`0` days of temporal overlap). In the Central Valley and at Eloy, agreement is weak (`r = 0.40` and `r = 0.09`) because observation seasons, agricultural C-band masking (`80.6%` masked in Eloy), and viewing geometry differ.

### 6. How does your self-checking QC catch unwrapping and reference errors?
`tools/atlas_qc.py` scans every basin's step-by-step time series for `12.1 cm` full L-band phase-cycle jumps, opposite-sign single-date spikes, and off-basin reference bias. It caught a `12.1 cm` unwrapping jump in Semarang (`−12.1` → `−6.2 cm` coastal peak after fixing) and a `−10.1 cm` phase jump in Beijing, downgrading `13` of `29` basins (`beijing`, `gorgan`, `pekalongan`, `delhi`, `bangkok`, `jakarta`, `tehran`, etc.) to `indicative only`.

### 7. Why does #1 Konya Plain (`−11.0 cm/100d`) carry an `11.6%` coverage caution?
Across the Konya Closed Basin (`108` days, `−9.6 cm` LOS peak), agricultural harvest and surface scatter leave only `11.6%` coherent valid pixels across the wide `1.5° × 0.7°` box (`0.46` reference spread). We therefore highlight #1 Konya Plain with an explicit low-coverage caution alongside `6.4×` faster subsidence within `1 km` of `29` verified Karapınar sinkholes.

### 8. Why is Querétaro excluded from the 29-basin global atlas?
In our diagnostic test (`data/global/queretaro/validation_note.json`), Querétaro showed `−22.9 cm / 120 d`—over an order of magnitude above INEGI's `~1.5 cm/yr` literature rate—with `48.6%` of pixels driven by a single-date spike and no independently verified off-basin reference. Following our QC gate, `build_atlas.py` excludes Querétaro from the `29`-basin atlas rather than publishing an unverified outlier.

### 9. How did you calculate `1,200,716` (`1.20 M`) people living on sinking ground?
We intersected `GHSL GHS-POP E2025` (`100 m`) population grids with pixels sinking faster than `−5 cm` per `108` days *and* exceeding each basin's `2-sigma` formal noise floor (`511.65 km²` total; `8.25 M` below `−2 cm`). Nested `karapinar` is excluded from the sum to avoid double-counting inside `konya_plain`.

### 10. How was `0.3174 km³/yr` permanent aquifer storage loss separated from seasonal bounce?
Near Earlimart (`data/central_valley_fullyear/decomp.json`), an `11`-month `mixed` chain (`18` beta-precal + `7` provisional pairs) decomposes (`R² = 0.97`) `−16.8 ± 2.2 cm/yr` LOS permanent clay compaction from `11.7 cm` peak-to-peak elastic seasonal rebound. Integrating permanent vertical compaction across `4,508.3 km²` (`> 1 cm/yr`) yields an estimated **`0.3174 km³/yr`** (`0.066–0.320 km³/yr` 3-ref range) permanent aquifer storage-capacity loss.

### 11. Are the `81/645` infrastructure flags structural safety assessments, and how does the simulator connect?
No—the `81` of `645` OpenStreetMap canal, road, and rail segments exceeding `10 mm/km` differential tilt are strictly a **preliminary screening index** to prioritize field leveling, not a structural safety assessment. Our 24-month `Groundwater Simulator` (`game/index.html`) calibrates a Terzaghi clay-compaction model directly to NISAR's Terra Bella summer rate (`−10.1 cm` vertical est., `k = 0.6232`).

### 12. Can an external engineer reproduce your pipeline, and what DEM/AI safeguards apply?
Yes—any `±0.25°` basin can be reproduced from public NASA ASF `GUNW` granules with `python -m pipeline.nisarvision`, using `Copernicus DEM GLO-90` strictly for elevation-dependent tropospheric delay correction (`tools/check_site.py` and `pytest` verify every number). Code and text drafts used Claude Code, Gemini/Antigravity, and OpenAI Codex with human/test verification, and **zero AI-generated images** appear anywhere on the site.
