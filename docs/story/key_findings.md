# Key Quantitative Findings & GNSS Validation Analysis

> **Calibration Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

## 1. Headline Quantitative Findings

1. **Central Valley peak subsidence reached -7.8 cm (28 Jun–14 Oct 2026):** Across the southern San Joaquin Valley (`bbox`), 1 km block-median ground motion along the radar line of sight (LOS, the direction between the satellite and the ground) reached -7.8 cm (range -6.2 to -7.8 cm depending on reference point; median Cramér–Rao phase-noise uncertainty ±0.29 cm). Assuming purely vertical motion at the 39.1° radar look angle gives -10.1 cm vertical (estimate) and an annualized summer-only rate of -26.4 cm/yr LOS (estimate), with 239.5 km² sinking faster than -5 cm and 1,578.3 km² faster than -2 cm (`data/central_valley/summary.json`, `data/central_valley/area_stats.json`, `data/central_valley/uncertainty/meta.json`).

2. **Karapınar basin subsided up to -5.9 cm (26 Jun–12 Oct 2026):** In Central Anatolia (`bbox`), 1 km block-median LOS displacement reached -5.9 cm (±0.33 cm median Cramér–Rao uncertainty), corresponding to -8.0 cm vertical (estimate) at the 42.0° look angle and an annualized summer-only rate of -20.0 cm/yr LOS (estimate). Cumulative subsidence exceeded -5 cm across 3.1 km² and -2 cm across 28.7 km² (`data/karapinar/summary.json`, `data/karapinar/area_stats.json`, `data/karapinar/uncertainty/meta.json`).

3. **Radar phase noise is 18× smaller than the peak signal (±0.29 cm CV, ±0.33 cm Karapınar):** Using the Cramér–Rao bound (a theoretical lower bound on random radar phase noise derived from pixel coherence, which measures how consistently the surface reflects radar waves across passes, at nominal L = 208 looks), median cumulative phase noise is ±0.294 cm (10th–90th percentile 0.163–0.471 cm; ±0.424 cm if L = 100) over Central Valley's 7 pairs and ±0.326 cm (0.176–0.548 cm; ±0.470 cm if L = 100) over Karapınar's 8 pairs. Peak subsidence signals (-5.9 to -7.8 cm LOS) exceed this formal phase noise by more than 18×, though unmodeled atmospheric water-vapor delay (~1–3 cm per pair) remains outside this bound (`data/central_valley/uncertainty/meta.json`, `data/karapinar/uncertainty/meta.json`).

4. **Independent GPS stations confirm -0.75 to -1.17 cm accuracy in sinking areas (28 Jun–14 Oct 2026):** Comparing NISAR vertical estimates against 10 continuous Nevada Geodetic Laboratory GNSS stations yields an overall median root-mean-square error (RMSE) of 1.004 cm (range 0.639–2.791 cm) and median correlation r = 0.541. Across the four actively sinking interior Tulare Basin stations (`CAHA`, `HANF`, `QCAP`, `TLBN`), InSAR matches GPS with 0.752–1.173 cm RMSE, r = 0.793–0.896, and -0.041 cm mean bias (`data/central_valley/validation.json`).

5. **An independent satellite track reproduces the same sinking pattern (28 Jun–14 Oct 2026):** Over 6,719 common 1 km blocks shared by ascending Track 34 and neighboring ascending Track 114, vertical-projected cumulative displacements correlate positively (r = 0.489, RMSE 2.65 cm, median difference -1.29 cm; 2nd-percentile peak -6.47 cm on Track 34 vs. -7.13 cm on Track 114), confirming that subsidence reflects real ground motion rather than a single-track processing artifact (`analysis/out/cv_p34_vs_p114.json`).

6. **Central Valley canals and railways cross steep subsidence gradients (28 Jun–14 Oct 2026):** Out of 645 evaluated infrastructure segments ≥ 1 km long (from 3,238 mapped features), 81 segments (12.6%) are classified high risk (gradient ≥ 10 mm/km with subsidence ≤ -2 cm, or ≤ -10 cm total) and 131 (20.3%) medium risk, led by the Tulare Irrigation District Canal at 57.01 mm/km longitudinal gradient and -6.75 cm peak LOS displacement (`data/central_valley/assets.json`).

7. **Subsidence in Karapınar concentrates around sinkholes (26 Jun–12 Oct 2026):** Areas within 0–1 km and 1–2 km of 29 cataloged sinkholes (*obruks*) average -4.152 cm (100% > 2 cm) and -4.030 cm (90.3% > 2 cm) LOS displacement, sinking 3.45 cm and 3.33 cm more than background terrain beyond 5 km (-0.647 cm mean). Ten road and canal segments rank high risk, topped by secondary highway 42-42 (19.74 mm/km gradient, -5.07 cm peak LOS, 597 m from `Köken Obruğu-II`), while `Köken Obruğu-I` averages -4.71 cm within 1 km (`data/karapinar/assets.json`).

8. **Mid-summer irrigation moisture precedes late-summer subsidence (28 Jun–14 Oct 2026):** Comparing NISAR L3 soil moisture (0.156–0.184 m³/m³) and HV radar backscatter (-18.17 to -18.62 dB) against Terra Bella (`p01`) LOS subsidence (0.0 to -7.8 cm) yields r = 0.654 for the normalized irrigation index and r = 0.638 at a 12-day lagged soil moisture signal (`data/central_valley/drivers.json`).

---

## 2. Q27 — Statistical Interpretation of GNSS Validation (`data/central_valley/validation.json`)

This comparison evaluates all 10 continuous Nevada Geodetic Laboratory GNSS stations across 8 common NISAR dates (28 Jun–14 Oct 2026), using 3×3 block-median vertical InSAR estimates (`LOS / cos(θ)`) and 7-day (`±3 day`) median GNSS vertical positions zero-referenced to 28 Jun 2026.

### 2.1 Moving vs. Stable Station Groups (`|GNSS|max` threshold = 2.0 cm)

| Station Group | Stations ($n$) | Median RMSE (cm) | Mean RMSE (cm) | RMSE Range (cm) | Median Pearson $r$ | Mean Pearson $r$ | $r$ Range | Median End Diff (`InSAR − GNSS`, cm) | Mean Bias (cm) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **All Stations** | 10 (`all`) | **1.004** | 1.330 | 0.639–2.791 | **0.541** | 0.379 | -0.410 to +0.896 | +0.961 | +0.539 |
| **Moving (`|GNSS|max > 2 cm`)** | 5 (`CAFP, CAHA, HANF, QCAP, TLBN`) | **0.834** | 1.263 | 0.752–2.791 | **0.820** | 0.695 | +0.069 to +0.896 | -0.218 | +0.365 |
| — *Interior Moving (excl. `CAFP`)* | 4 (`CAHA, HANF, QCAP, TLBN`) | **0.800** | 0.881 | 0.752–1.173 | **0.858** | 0.851 | +0.793 to +0.896 | -0.307 | -0.041 |
| **Stable (`|GNSS|max <= 2 cm`)** | 5 (`CAD1, P056, P564, P565, P566`) | **1.570** | 1.397 | 0.639–1.998 | **-0.101** | 0.064 | -0.410 to +0.661 | +1.866 | +0.714 |

### 2.2 Per-Station Verification Summary

| Station | Regime | Look Angle $\theta$ (deg) | Max `|GNSS|` (cm) | GNSS End (cm) | InSAR Vert End (cm) | End Diff (cm) | RMSE (cm) | Pearson $r$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `TLBN` | Moving | 41.09 | 4.454 | -4.454 | -4.850 | -0.396 | 1.173 | **+0.7926** |
| `QCAP` | Moving | 41.44 | 3.510 | -3.199 | -2.542 | +0.657 | 0.767 | **+0.8198** |
| `CAHA` | Moving | 41.38 | 3.436 | -3.228 | -3.446 | -0.218 | 0.752 | **+0.8957** |
| `CAFP` | Moving (basin margin) | 43.34 | 2.992 | -1.003 | +0.477 | +1.480 | 2.791 | +0.0689 |
| `HANF` | Moving | 41.75 | 2.882 | -2.223 | -3.511 | -1.288 | 0.834 | **+0.8955** |
| `P056` | Stable | 39.28 | 1.653 | -1.451 | -2.496 | -1.045 | 0.788 | +0.6613 |
| `CAD1` | Stable | 40.62 | 0.974 | -0.707 | +1.247 | +1.954 | 1.991 | -0.4097 |
| `P564` | Stable | 41.38 | 0.793 | -0.167 | +1.921 | +2.088 | 1.570 | -0.1009 |
| `P565` | Stable | 40.62 | 0.789 | -0.543 | +1.323 | +1.866 | 1.998 | -0.2520 |
| `P566` | Stable | 39.56 | 0.408 | +0.187 | +1.452 | +1.265 | 0.639 | +0.4209 |

### 2.3 Statistical Interpretation

Across all ten Central Valley GPS stations, provisional NISAR vertical displacement reproduces independent GPS trajectories with a median RMSE of 1.004 cm (0.834 cm median across moving sites with `|GNSS|max > 2 cm` vs. 1.570 cm across stable sites), while Pearson correlation diverges sharply between moving stations (median 0.820; 0.793–0.896 at interior Tulare Basin stations `CAHA`, `HANF`, `QCAP`, and `TLBN`) and stable stations (median -0.101). This contrast occurs because Pearson correlation measures linear covariance relative to true signal variance: at stable stations (`|GNSS| <= 2 cm`), real ground motion approaches zero and epoch-to-epoch differences are dominated by ~1–2 cm unmodeled tropospheric wet-delay fluctuations (plus long-wavelength plane/DEM removal residuals), producing near-zero or slightly negative correlation even when absolute error stays near 1.5 cm RMSE. At high-signal basin stations and western-margin site `CAFP` (2.791 cm RMSE due to a single +4.36 cm atmospheric spike on 8 Sep 2026), RMSE bounds absolute accuracy while correlation reflects trajectory agreement only where deformation exceeds atmospheric noise.
