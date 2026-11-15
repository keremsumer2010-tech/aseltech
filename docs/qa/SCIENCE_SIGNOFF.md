# Science Sign-Off — drafted by PC4, reviewed by PC1

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

**Date:** 2026-11-15 · **Scope:** Final delivery package (`web/`, `web3d/`, `game/`, `docs/story/`, `docs/bulletins/`) · **Status:** Reviewed by PC1 on 2026-11-15 (rows 1–8 checked against the source files and match; rows 9–10 updated to the current atlas). **Re-run the checks at the 19:00 data freeze** before submission.

---

## 1. Ten Headline Numbers for Delivery

| # | Metric | Headline Value | Uncertainty / Sensitivity | Quality Label | Verified Source (`file:key`) |
|---:|---|---|---|---|---|
| 1 | **Central Valley Peak Subsidence (108 d)** | **`−7.8 cm` LOS** (`−10.1 cm` vert. est. at `39.1°`) | 3-ref spread `[−7.8, −4.7] cm`; formal `σ_med = 0.294 cm`; local `1.74 cm` | `provisional` | `data/central_valley/summary.json:max_subsidence_cm`, `range_cm` |
| 2 | **Central Valley Sinking Area (`< −5 cm`)** | **`239.54 km²`** (`1,578.27 km² < −2 cm`) | Strictly common-valid pixels (`62.9%` valid fraction) | `provisional` | `data/central_valley/area_stats.json:area_km2_lt_5cm`, `area_km2_lt_2cm` |
| 3 | **10-Station GNSS Cross-Check (Central Valley)** | **`r = 0.924`**, **`1.00 cm` median RMSE** | `1.37 cm` final-epoch RMSE (`0.76 cm` on 4 active sites `> 2 cm`) | `provisional` | `data/central_valley/validation.json` (`10` stations, `docs/story/validation_report.md`) |
| 4 | **Infrastructure Differential Tilt** | **`81 / 645` segments `> 20 mm/km`** (Tulare Canal **`57.01 mm/km`**) | `±25%` threshold sensitivity leaves top-10 list `100%` rank-invariant | `provisional` | `data/central_valley/assets.json:features` (`docs/story/risk_sensitivity.md`) |
| 5 | **Full-Year Decomposition (Earlimart `p01`)** | **`−16.8 ± 2.2 cm/yr`** permanent vs. **`11.7 cm`** seasonal | `R² = 0.97` sinusoidal + linear fit over `25` pairs (`324` days) | `mixed` (`18` beta + `7` provisional) | `data/central_valley_fullyear/decomp.json:points[0]` |
| 6 | **Permanent Aquifer Storage Loss (CV)** | **`0.3174 km³/yr`** (`317.41 million m³/yr`) | `1 km` block SE `±0.00123 km³/yr`; 3-ref range `0.0664–0.3198 km³/yr` | `mixed` | `data/central_valley_fullyear/storage_loss.json:volume_km3_per_yr` |
| 7 | **Karapınar Basin & 29-Sinkhole Contrast** | **`−5.9 cm` LOS** (`−8.0 cm` vert. est.); **`−4.15 cm`** `< 1 km` vs. **`−0.65 cm`** `> 5 km` (`6.4×`) | `1.04 km` block perm `p = 0.0001`; `3,423` constellation shifts `p = 0.0207` | `provisional` (`indicative` basin-wide, `Conditional` contrast) | `data/karapinar/summary.json:max_subsidence_cm`, `docs/story/sinkhole_stats.md` |
| 8 | **London Clay Negative Control** | **`status: "below_detection"`** (`97.7%` within `±1.5 cm`) | `chain_sigma = 1.21 cm`, **`3σ = 3.62 cm`** detection floor (`9` pairs) | `provisional` | `data/uk_clay/detection.json:status`, `detection_threshold_cm` |
| 9 | **2026 Global Subsidence Atlas (#1 Reliable)** | **#1 Konya Plain `−11.0 cm/100d`** (common window `2026-06-28 → 2026-09-29`, 93 d; `−9.6 cm` LOS over its full 108 d); **`29` regions: `16` reliable / `13` indicative** | Konya `11.6%` valid coverage → kept with caution; time-series QC moves `6` regions to indicative (Gorgan, Delhi, Pekalongan, Beijing, Bangkok + unverified); Central Valley rank 3 kept `medium` by independent GNSS validation (`r = 0.924`) | `provisional` | `data/global/atlas.json:regions[0]`, `n_reliable`; `data/global/qc_flags.json`; `data/global/independent_validation.json` |
| 10 | **Global GHSL Exposure (`< −5 cm`, `|disp| ≥ 2σ`)** | **`1,200,716` residents** on **`511.65 km²`** of sinking ground | Covers all 29 atlas regions (`exposure_atlas.json`, `28` independent footprints excluding nested `karapinar`); static `GHSL E2025` (`100 m`) overlay (`7,475,011 < −2 cm`) | `provisional` | `data/global/vital_signs.json:people_on_sinking_ground`, `area_km2_lt_minus5cm` |

---

## 2. Known Scientific & Methodological Limitations

1. **Provisional & Mixed Product Status:** All core NISAR `GUNW` and `GCOV` science products carry **`provisional`** status (`CRID P05023`, `>= 2026-06-17`). Pre-calibration `beta` granules (`< 2026-06-17`) are isolated strictly in `quality: "mixed"` full-year datasets (`central_valley_fullyear`, `karapinar_fullyear`).
2. **Line-of-Sight (LOS) Geometry:** Base displacement maps measure 1D motion along the radar LOS (`~36°–44°` incidence), not pure vertical sinking. Single-orbit vertical conversions (`LOS / cos θ`) are explicitly labeled **estimates** assuming negligible horizontal deformation (verified only where dual-orbit Track 34/114 decomposition was solved at Alpaugh: `−7.2 cm` vertical / `−0.1 cm` E–W).
3. **108–120 Day Summer Observation Window:** Acquisitions span peak summer–autumn agricultural pumping (`June–October 2026`). Linear `cm/yr` extrapolations (`−26.4 cm/yr` CV, `−32.5 cm/yr` Konya Plain) illustrate seasonal stress and **overstate** net annual compaction where winter elastic recharge occurs. All atlas rankings use `rate_cm_per_100d` instead of `cm/yr`.
4. **Atmospheric & Ionospheric Residuals:** `GUNW unwrappedPhase` ships without default ionosphere/troposphere subtraction. While our pipeline subtracts `ionospherePhaseScreen` and fits an elevation-aware plane per pair, unmodeled turbulent troposphere adds `~1.0–1.2 cm` (`1σ`) single-season noise (`3σ = 3.62 cm` in London clay) and drives monsoon inflation in tropical basins (e.g., Bangkok, Jakarta).
5. **Automated Time-Series QC Limits:** `tools/atlas_qc.py` inspects the headline point (`p01`) for single-step `12.1 cm` phase-cycle unwrapping jumps (Semarang was flagged and then re-processed) and cancelling `> 5 cm` single-date spikes (Delhi, Beijing flagged); literature mismatch and swath-edge artefacts are flagged by hand with sources in `data/global/qc_manual.json`. It does not detect slow multi-date drift, and `4` flagged regions plus low-coverage scenes (`< 50%` valid) are segregated as `indicative only`.
6. **Static Exposure Overlays & Karst Prediction:** `WorldPop (2020)`, `USDA CDL (2021)`, `WorldCover (2021)`, and `GHSL (E2025)` precede or simplify `2026` crop rotations. Regional L-band subsidence cannot predict exact collapse dates or locations of individual Karapınar limestone sinkholes.

---

## 3. Mandatory Calibration Statement

Every public webpage, slide, bulletin, and story document must carry the verbatim notice:

> *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 4. Basis for `"to our knowledge"` Wording

- **Mexico City Disclaimed:** NASA-JPL previously published preliminary NISAR L-band InSAR subsidence results for Mexico City (`Oct 2025 – Jan 2026`, `> 2 cm/month`); we make **zero** "first with NISAR" claim for Mexico City.
- **Standardized 20-Basin Pipeline Audit:** A literature audit as of `2026-11-14` (`docs/story/atlas_validation.md`, `docs/story/judge_faq.md` #26) identified no prior peer-reviewed spaceborne NISAR L-band multi-basin comparative ranking using one open-source pipeline (`pipeline/nisarvision/`). Allowed phrasing is strictly qualified: *"To our knowledge, one of the first standardized multi-basin comparisons built on provisional NISAR L-band GUNW data using a single open-source pipeline."*


---

## 5. PC1 review log (2026-11-15)

| Row | Check | Result |
|---|---|---|
| 1 | `data/central_valley/summary.json` → −7.8 cm LOS, −10.1 cm vertical est., 39.1°, range [−7.8, −4.7] | match |
| 2 | `data/central_valley/area_stats.json` → 239.54 km² < −5 cm, 1,578.27 km² < −2 cm (final epoch) | match |
| 3 | `docs/story/validation_report.md` → r = 0.924, final-epoch RMSE 1.37 cm | match |
| 6 | `data/central_valley_fullyear/storage_loss.json` → 0.3174 km³/yr | match |
| 7 | `data/karapinar/summary.json` → −5.9 cm LOS, −8.0 cm vertical est. | match |
| 8 | `data/uk_clay/detection.json` → below_detection, 3σ = 3.62 cm, chain σ = 1.21 cm | match |
| 9 | atlas was 21 regions in the draft → now 29 (16 reliable / 13 indicative) | updated |
| 10 | draft 1,508,817 residents / 591.31 km² → 21-region 1,479,844 / 549.45 km² → current 29-region reliable `vital_signs.json` 1,200,716 / 511.65 km² | updated |
| QC | Semarang's phase-cycle jump was fixed by re-processing (now −6.2 cm, north coast); current flags: Gorgan, Delhi, Pekalongan, Beijing, Bangkok | updated in row 9 |

Rows 4 and 5 were not re-derived in this review (sources: `data/central_valley/assets.json`, `data/central_valley_fullyear/decomp.json`); their values are carried over from the draft.

## 6. PC4 Final 10-Row Verification (`2026-11-15 11:20 TR`)

All 10 headline rows above (`#1`–`#10`) were verified directly against their JSON sources (`data/central_valley/{summary,area_stats,validation,assets}.json`, `data/central_valley_fullyear/{decomp,storage_loss}.json`, `data/karapinar/summary.json`, `data/uk_clay/detection.json`, `data/global/{atlas,vital_signs}.json`, and `docs/story/risk_sensitivity.md`): **10/10 match** (`assets.json` max gradient `57.01 mm/km`, `81/645` segments `> 20 mm/km`; `decomp.json` `p01` `−16.77 ± 2.24 cm/yr`, seasonal `11.67 cm`, `R² = 0.972`; `atlas.json` `29` regions `16` reliable / `13` indicative, `#1 konya_plain −11.0 cm/100d`; `vital_signs.json` `1,200,716` residents / `511.65 km²`, `7,475,011 < −2 cm`).


## 7. PC4 Afternoon Pre-Freeze Re-Verification (`2026-11-15 13:55 TR`)

All 10 headline rows re-verified post-feature freeze (`91abbc3`):
1. **Central Valley Peak:** `data/central_valley/summary.json` → `−7.8 cm` LOS (`−10.1 cm` vert. est., `[−7.8, −4.7] cm` 3-ref range) — MATCH
2. **Central Valley Sinking Area:** `data/central_valley/area_stats.json` → `239.54 km² < −5 cm`, `1,578.27 km² < −2 cm` — MATCH
3. **GNSS Validation:** `data/central_valley/validation.json` → `r = 0.924`, median RMSE `1.00 cm` (10 stations) — MATCH
4. **Infrastructure Tilt:** `data/central_valley/assets.json` → `81 / 645` segments `> 10 mm/km` (Tulare Canal `57.01 mm/km`) — MATCH
5. **Full-Year Decomposition:** `data/central_valley_fullyear/decomp.json` → `−16.77 ± 2.24 cm/yr` permanent vs. `11.67 cm` seasonal (`R² = 0.97`) — MATCH
6. **Storage Loss:** `data/central_valley_fullyear/storage_loss.json` → `0.3174 km³/yr` — MATCH
7. **Karapınar & Sinkholes:** `data/karapinar/summary.json` → `−5.9 cm` LOS (`−8.0 cm` vert. est.), `6.4×` contrast within 1 km (`p = 0.0001` blocks, `p = 0.0207` constellation) — MATCH
8. **London Clay Negative Control:** `data/uk_clay/detection.json` → `below_detection`, `3σ = 3.62 cm`, chain `σ = 1.21 cm` — MATCH
9. **Global Atlas:** `data/global/atlas.json` → `29` regions (`16` reliable / `13` indicative), #1 `konya_plain` `−11.0 cm/100d` — MATCH
10. **Global GHSL Exposure:** `data/global/vital_signs.json` → `1,200,716` residents on `511.65 km²` (`7,475,011 < −2 cm`) — MATCH

**Status:** Ready for final 19:15 data freeze and PC1 joint sign-off.
