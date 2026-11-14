# Central Valley Infrastructure Risk Threshold Sensitivity (±25%)

> **Calibration Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

This report tests how sensitive `risk/compute_risk.py` classifications and top-10 segment rankings are to ±25% variations in the high-risk longitudinal gradient threshold (`7.5 / 10.0 / 12.5 mm/km`, medium scaled proportionally at `0.5×`) and cumulative LOS subsidence threshold (`7.5 / 10.0 / 12.5 cm`, medium scaled at `0.5×`).

## 1. Baseline Cross-Check (`data/central_valley/assets.json` vs. Full Re-evaluation)

- **Evaluated GeoJSON features:** `645` valid ≥ 1 km segments out of `3238` total features in `risk/central_valley_infra.geojson` (matches `assets.json` `evaluated_segments = 645`).
- **Baseline `(10.0 mm/km, 10.0 cm)` counts:** High = **`81`** (matches `81`), Medium = **`131`** (matches `131`), Low = **`433`** (matches `433`).
- **Assets file top-10 verification:** Re-evaluated top-10 `osm_id` list matches `data/central_valley/assets.json` `features[:10]` identically (minimum top-10 gradient `42.34 mm/km`, maximum `57.01 mm/km`, least-negative `max_cm` = `-4.29 cm`).

## 2. ±25% Threshold Sensitivity Matrix (`n = 645` Evaluated Segments)

| High Gradient Threshold (`mm/km`) | High Subsidence Threshold (`cm`) | Medium Thresholds (`mm/km` / `cm`) | High-Risk Segments | High Share (`%`) | Δ High vs. Baseline | Medium-Risk | Low-Risk | Top-10 List Identical? |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 7.5 | 7.5 | 3.75 / 3.75 | **115** | 17.8% | +34 | 140 | 390 | Yes (exact order) |
| 7.5 | 10.0 | 3.75 / 5.00 | **115** | 17.8% | +34 | 137 | 393 | Yes (exact order) |
| 7.5 | 12.5 | 3.75 / 6.25 | **115** | 17.8% | +34 | 137 | 393 | Yes (exact order) |
| 10.0 | 7.5 | 5.00 / 3.75 | **81** | 12.6% | 0 (baseline) | 138 | 426 | Yes (exact order) |
| 10.0 | 10.0 | 5.00 / 5.00 | **81** | 12.6% | 0 (baseline) | 131 | 433 | Yes (exact order) |
| 10.0 | 12.5 | 5.00 / 6.25 | **81** | 12.6% | 0 (baseline) | 131 | 433 | Yes (exact order) |
| 12.5 | 7.5 | 6.25 / 3.75 | **72** | 11.2% | -9 | 125 | 448 | Yes (exact order) |
| 12.5 | 10.0 | 6.25 / 5.00 | **72** | 11.2% | -9 | 115 | 458 | Yes (exact order) |
| 12.5 | 12.5 | 6.25 / 6.25 | **72** | 11.2% | -9 | 115 | 458 | Yes (exact order) |

## 3. Top-10 Highest-Risk Segments (Invariant Across All ±25% Combinations)

| Rank | Segment Name | Type | `osm_id` | Gradient (`mm/km`) | Peak LOS (`cm`) | Length (`km`) | Classified Risk Across All 9 Threshold Pairs |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | Tulare Irrigation District Canal | canal | `79592963` | 57.01 | -6.75 | 2.17 | Always **high** |
| 2 | Exeter Subdivision | rail | `196474322` | 55.61 | -6.18 | 10.07 | Always **high** |
| 3 | Exeter Subdivision | rail | `196530229` | 49.69 | -7.80 | 13.68 | Always **high** |
| 4 | California Aqueduct | canal | `24016778` | 49.12 | -7.42 | 102.82 | Always **high** |
| 5 | Alta East Branch Canal | canal | `202390442` | 48.10 | -6.87 | 6.68 | Always **high** |
| 6 | Porterville Subdivision | rail | `196158173` | 47.85 | -4.74 | 5.34 | Always **high** |
| 7 | Friant-Kern Canal | canal | `1226257286` | 46.06 | -4.51 | 1.54 | Always **high** |
| 8 | Unnamed canal (osm:75230703) | canal | `75230703` | 44.77 | -6.01 | 1.99 | Always **high** |
| 9 | Friant-Kern Canal | canal | `79593586` | 44.47 | -5.92 | 2.09 | Always **high** |
| 10 | CA 65 | trunk | `211929583` | 42.34 | -4.29 | 6.18 | Always **high** |

## 4. Technical Summary (3 Sentences)

Varying the high-risk thresholds by ±25% shifts the high-risk segment count across the 645 evaluated Central Valley lines from **115** (`+34` at `7.5 mm/km`, `7.5 cm`) down to **72** (`-9` at `12.5 mm/km`, `12.5 cm`) around the **`81`**-segment baseline, showing that segment classification is driven predominantly by the differential gradient threshold rather than the absolute subsidence cutoff (which adds 0 segments even when lowered to `7.5 cm` at a fixed gradient, compare `sub_7.5=[115, 81, 72]` vs. `sub_12.5=[115, 81, 72]`). Most importantly, **the top-10 highest-risk segment list and its exact rank order remain 100% unchanged** (`invariant`) across all nine threshold combinations because all ten priority corridors exhibit gradients between `42.34` and `57.01 mm/km`—well above the strictest `12.5 mm/km` boundary—and local displacement magnitudes between `-4.29` and `-7.80 cm`. Consequently, priority canal and aqueduct remediation targets identified in `data/central_valley/assets.json` are mathematically robust to reasonable expert disagreement over risk classification cutoffs.
