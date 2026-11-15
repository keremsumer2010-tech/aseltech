# Independent Verification of Reliable Ranks 6–16 (`docs/story/atlas_rank_check_6_16.md`)

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

This audit extends `docs/story/atlas_top5_check.md` to **reliable ranks 6–16** in `data/global/atlas.json` (ranked by common 93-day window `2026-06-28 → 2026-09-29`). For each region we compare our annualized LOS estimate (`rate_cm_per_yr_estimate`, summer window) against `data/global/literature_rates.json`, check `p01` step-to-step time-series QC (`tools/atlas_qc.py` thresholds: `12.1 cm` half-cycle jump, `> 5 cm` cancelling single-date spike), and assign a status (**consistent**, **caution**, or **suspect**).

## 1. Ranks 6–16 Verification Matrix

| Rank | Region (`id`) | Common Rate (`cm/100d`) | Peak LOS (`cm`) | Annualized Est. (`cm/yr`) | Literature Vertical (`cm/yr`) & Source | Max `p01` Step (`cm`) | Time-Series QC | Decision |
|---:|---|---:|---:|---:|---|---:|---|---|
| 6 | **Mexico City** (`mexico_city`) | `−6.3` | `−7.0` | `−21.2` | `−30 to −40` (eastern/northern lakebed; Chaussard et al. 2021, off-basin volcanic ref.) | `3.55` | Pass (`0` flags) | **consistent** |
| 7 | **Semarang** (`semarang`) | `−5.5` | `−6.2` | `−23.6` | `−6 to −19` coastal hotspots (Arimoto et al. 2011; Aditiya & Ito 2023; `10-11` jump fixed) | `5.14` | Pass (`0` flags post-fix) | **consistent** |
| 8 | **Kerman** (`kerman`) | `−5.3` | `−6.1` | `−18.6` | `> 35` province basins ([10.1126/sciadv.adp0896](https://doi.org/10.1126/sciadv.adp0896)) | `1.60` | Pass (`0` flags) | **consistent** |
| 9 | **Rafsanjan** (`rafsanjan`) | `−4.2` | `−5.8` | `−10.7` | `15 to 30+` across Rafsanjan Plain (Motagh et al. 2017) | `1.19` | Pass (`0` flags) | **consistent** |
| 10 | **Houston** (`houston`) | `−4.0` | `−5.2` | `−15.9` | `1.0–4.9` peripheral groundwater/clay ([10.3390/rs14236184](https://doi.org/10.3390/rs14236184)) | `1.70` | Pass (`0` flags; `46.1%` valid px) | **caution** |
| 11 | **Can Tho** (`can_tho`) | `−3.4` | `−3.4` | `−10.3` | `1.0–4.0+` urban & Holocene clay ([10.3390/rs13020189](https://doi.org/10.3390/rs13020189)) | `1.76` | Pass (`0` flags) | **consistent** |
| 12 | **Tianjin** (`tianjin`) | `−2.8` | `−2.9` | `−8.7` | `5–17` coastal/inland cones ([10.3390/s26041203](https://doi.org/10.3390/s26041203)) | `1.37` | Pass (`0` flags) | **consistent** |
| 13 | **Cangzhou** (`cangzhou`) | `−2.4` | `−2.4` | `−7.2` | `~2–4` post-diversion ([10.1007/s12665-013-2532-7](https://doi.org/10.1007/s12665-013-2532-7)) | `1.07` | Pass (`0` flags) | **consistent** |
| 14 | **Lagos** (`lagos`) | `−2.1` | `−2.4` | `−8.2` | `0.2–8.7` coastal fill & urban aquifers ([10.1016/j.geog.2019.12.006](https://doi.org/10.1016/j.geog.2019.12.006)) | `1.49` | Pass (`0` flags; `32.8%` valid px) | **consistent** |
| 15 | **Sacramento–San Joaquin Delta** (`delta`) | `−1.4` | `−1.3` | `−4.0` | `−1.2 to −2.2` peat oxidation (up to `−3.0` locally) | `1.58` | Pass (`0` flags) | **consistent** |
| 16 | **Quetta** (`quetta`) | `−0.7` | `−3.8` | `−11.6` | `−3` valley flanks, `−12 to −16.6` central urban core (Kakar et al. 2016) | `4.15` | Pass (`0` flags; edge-epoch heavy) | **caution** |

## 2. Caution & QC Manual Recommendations

- **No `suspect` (`qc_manual.json` demotion) regions found in ranks 6–16:** All 11 reliable basins pass `tools/atlas_qc.py` with `0` phase-cycle (`12.1 cm`) or cancelling spike (`> 5 cm`) flags, and `9/11` match published orders of magnitude directly.
- **Houston (`#10`, `caution`):** Peak `−5.2 cm` LOS (`−15.9 cm/yr` summer annualized) exceeds modern `1.0–4.9 cm/yr` GPS/InSAR baselines (`10.3390/rs14236184`) and has `46.1%` valid pixels. Retain as `medium` with explicit reference-sensitivity and summer-pumping caution rather than demoting, because `p01` shows monotonic `1.70 cm` max step without spikes.
- **Quetta (`#16`, `caution`):** Common-window rate (`−0.7 cm/100d`) diverges sharply from full-window (`−3.8 cm`, `−11.6 cm/yr`) because most drawdown occurs on edge acquisitions with a `4.15 cm` single-step jump. Keep `medium` with timing caution; no `qc_manual.json` exclusion needed.
