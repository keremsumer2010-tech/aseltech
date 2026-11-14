# Science Sign-Off — DRAFT by PC4 — PC1 review

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

**Date:** 2026-11-15 · **Scope:** Final delivery package (`web/`, `web3d/`, `game/`, `docs/story/`, `docs/bulletins/`) · **Status:** DRAFT by PC4 — pending PC1 final review (PC5 offline).

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
| 9 | **2026 Global Subsidence Atlas (#1 Reliable)** | **#1 Konya Plain `−11.0 cm/100d`** (`93`-d common; `−8.9` full, `−9.6 cm` LOS); `9` reliable / `12` indicative (`21` total) | Konya `11.6%` valid-coverage caution; Semarang reprocessed to `−6.2 cm` LOS (`#5`); `3` QC-flagged regions `indicative` (`atlas_top5_check.md`) | `provisional` | `data/global/atlas.json:regions[0]` |
| 10 | **Global GHSL Exposure (`< −5 cm / 108 d`)** | **`1,508,817` residents** (`591.31 km²`); `8,047,490` `< −2 cm` (`19` independent footprints) | Excludes nested `karapinar`; static `GHSL E2025` (`100 m`) overlay | `provisional` | `data/global/vital_signs.json` (`docs/story/exposure.md`) |

---

## 2. Known Scientific & Methodological Limitations

1. **Provisional & Mixed Product Status:** All core NISAR `GUNW` and `GCOV` science products carry **`provisional`** status (`CRID P05023`, `>= 2026-06-17`). Pre-calibration `beta` granules (`< 2026-06-17`) are isolated strictly in `quality: "mixed"` full-year datasets (`central_valley_fullyear`, `karapinar_fullyear`).
2. **Line-of-Sight (LOS) Geometry:** Base displacement maps measure 1D motion along the radar LOS (`~36°–44°` incidence), not pure vertical sinking. Single-orbit vertical conversions (`LOS / cos θ`) are explicitly labeled **estimates** assuming negligible horizontal deformation (verified only where dual-orbit Track 34/114 decomposition was solved at Alpaugh: `−7.2 cm` vertical / `−0.1 cm` E–W).
3. **108–120 Day Summer Observation Window:** Acquisitions span peak summer–autumn agricultural pumping (`June–October 2026`). Linear `cm/yr` extrapolations (`−26.4 cm/yr` CV, `−32.5 cm/yr` Konya Plain) illustrate seasonal stress and **overstate** net annual compaction where winter elastic recharge occurs. All atlas rankings use `rate_cm_per_100d` instead of `cm/yr`.
4. **Atmospheric & Ionospheric Residuals:** `GUNW unwrappedPhase` ships without default ionosphere/troposphere subtraction. While our pipeline subtracts `ionospherePhaseScreen` and fits an elevation-aware plane per pair, unmodeled turbulent troposphere adds `~1.0–1.2 cm` (`1σ`) single-season noise (`3σ = 3.62 cm` in London clay) and drives monsoon inflation in tropical basins (e.g., Bangkok, Jakarta).
5. **Automated Time-Series QC Limits:** `tools/atlas_qc.py` inspects the headline point (`p01`) for single-step `12.1 cm` phase-cycle unwrapping jumps (`Semarang` flagged) and cancelling `> 5 cm` single-date spikes (`Delhi`, `Beijing` flagged). It does not detect slow multi-date drift, and `4` flagged regions plus low-coverage scenes (`< 50%` valid) are segregated as `indicative only`.
6. **Static Exposure Overlays & Karst Prediction:** `WorldPop (2020)`, `USDA CDL (2021)`, `WorldCover (2021)`, and `GHSL (E2025)` precede or simplify `2026` crop rotations. Regional L-band subsidence cannot predict exact collapse dates or locations of individual Karapınar limestone sinkholes.

---

## 3. Mandatory Calibration Statement

Every public webpage, slide, bulletin, and story document must carry the verbatim notice:

> *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 4. Basis for `"to our knowledge"` Wording

- **Mexico City Disclaimed:** NASA-JPL previously published preliminary NISAR L-band InSAR subsidence results for Mexico City (`Oct 2025 – Jan 2026`, `> 2 cm/month`); we make **zero** "first with NISAR" claim for Mexico City.
- **Standardized 20-Basin Pipeline Audit:** A literature audit as of `2026-11-14` (`docs/story/atlas_validation.md`, `docs/story/judge_faq.md` #26) identified no prior peer-reviewed spaceborne NISAR L-band multi-basin comparative ranking using one open-source pipeline (`pipeline/nisarpulse/`). Allowed phrasing is strictly qualified: *"To our knowledge, one of the first standardized multi-basin comparisons built on provisional NISAR L-band GUNW data using a single open-source pipeline."*
