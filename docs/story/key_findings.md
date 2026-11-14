# Key Quantitative Findings & Validation Statistical Analysis

> **Calibration Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

---

## 1. Headline Quantitative Findings (8 Core Takeaways)

1. **Central Valley 108-day peak subsidence (`2026-06-28` → `2026-10-14`):** Maximum 1 km block-median LOS displacement reaches **`-7.8 cm`** (`-7.8` to `-6.2 cm` across alternative reference-point sensitivity; implied vertical **`-10.1 cm`** at `39.1°` incidence; linearized summer-only rate estimate **`-26.4 cm/yr` LOS** / **`-34.1 cm/yr` vertical**), with **`258.7 km²`** subsiding beyond `-5 cm` LOS and **`1,673.9 km²`** beyond `-2 cm` LOS against a median pixel Cramér–Rao formal uncertainty of **`±0.294 cm`** (`p90 = 0.471 cm`) (`data/central_valley/summary.json`, `analysis/out/central_valley_cum.npz`, `data/central_valley/uncertainty/meta.json`).
2. **Karapınar 108-day peak subsidence (`2026-06-26` → `2026-10-12`):** Maximum 1 km block-median LOS displacement reaches **`-5.9 cm`** (implied vertical **`-8.0 cm`** at `42.0°` incidence; linearized summer-only rate estimate **`-20.0 cm/yr` LOS**), with **`3.1 km²`** exceeding `-5 cm` LOS and **`49.1 km²`** exceeding `-2 cm` LOS against a median Cramér–Rao formal uncertainty of **`±0.326 cm`** (`p90 = 0.548 cm`) (`data/karapinar/summary.json`, `analysis/out/karapinar_cum.npz`, `data/karapinar/uncertainty/meta.json`).
3. **Per-pixel Cramér–Rao phase-noise bound (`L = 208` nominal looks, sensitivity at `L = 100`):** Short-scale decorrelation noise across the 7-pair Central Valley chain has median **`0.294 cm`** (`p10–p90: 0.163–0.471 cm`, `64.69%` valid coverage; `0.424 cm` median at `L = 100`) and across the 8-pair Karapınar chain **`0.326 cm`** (`p10–p90: 0.176–0.548 cm`, `15.44%` valid coverage; `0.470 cm` median at `L = 100`). Peak subsidence (`-5.9` to `-7.8 cm`) exceeds formal phase noise by `> 18×`, while residual unmodeled tropospheric delay (`~1–3 cm/pair`) remains the dominant unquantified error term (`data/central_valley/uncertainty/meta.json`, `data/karapinar/uncertainty/meta.json`, `data/*/meta.json`).
4. **Independent GNSS validation (`10` NGL stations, `8` epochs):** Across all 10 Central Valley stations converted from LOS to vertical via `LOS / cos(θ)`, median RMSE is **`1.004 cm`** (`range 0.639–2.791 cm`, mean `1.330 cm`) and median Pearson $r$ is **`0.541`** (`-0.410` to `+0.896`). At actively subsiding interior basin stations (`CAHA`, `HANF`, `QCAP`, `TLBN`), InSAR tracks vertical GNSS with RMSE **`0.752–1.173 cm`** (median `0.800 cm`), Pearson $r =$ **`0.793–0.896`**, and mean bias `-0.041 cm` (`data/central_valley/validation.json`).
5. **Cross-track verification (Ascending Path 34 vs. Path 114, `6,719` common 1 km blocks):** Over the identical `2026-06-28` → `2026-10-14` window, vertical-projected cumulative displacement fields correlate positively across both independent viewing geometries (**Pearson $r = 0.489$**, `RMSE = 2.65 cm`, median difference `-1.29 cm`, 2nd-percentile basin peak `-6.47 cm` in P34 vs. `-7.13 cm` in P114), confirming that broad Tulare Basin subsidence is geometry-independent rather than a single-track orbit or unwrapping artifact (`analysis/out/cv_p34_vs_p114.json`).
6. **Central Valley linear infrastructure exposure (`645` evaluated segments):** Out of `3,238` OpenStreetMap features (`min_span >= 1 km`), **`81`** segments (`12.6%`) meet high-risk criteria (`gradient >= 10 mm/km` with `max_cm <= -2 cm`, or `max_cm <= -10 cm`) and **`131`** (`20.3%`) meet medium-risk criteria, led by **Tulare Irrigation District Canal** (`osm:79592963`, longitudinal gradient **`57.01 mm/km`**, `max = -6.75 cm`, length `2.17 km`) (`data/central_valley/assets.json`).
7. **Karapınar sinkhole ring & road exposure (`29` cataloged obruks, `64` road/canal segments):** Pixels within **`0–1 km`** (`mean -4.152 cm`, `100.0%` > `2 cm`) and **`1–2 km`** (`mean -4.030 cm`, `90.3%` > `2 cm`) of cataloged sinkholes subside **`3.45 cm`** and **`3.33 cm`** faster than the regional background (`> 5 km mean -0.647 cm`, `n = 40,194` valid pixels), with **`10` high-risk** infrastructure segments topped by secondary highway **`42-42`** (`osm:208237483`, gradient **`19.74 mm/km`**, `max = -5.07 cm`, `597.3 m` from `Köken Obruğu-II`), while `Köken Obruğu-I` averages `-4.71 cm` within `1 km` (`min = -5.627 cm`) (`data/karapinar/assets.json`).
8. **Agricultural moisture–subsidence coupling (`drivers.json`):** Comparing `NISAR L3 SME2` `200 m` EASE-Grid soil moisture (`0.156–0.184 m³/m³`) and `HV` backscatter (`-18.17` to `-18.62 dB`) against Terra Bella (`p01`) subsidence (`0.0` to `-7.8 cm`) across 8 epochs yields correlation **`r = 0.654`** for the normalized `irrigation_index` and **`r = 0.638`** for 12-day lagged (`lag-1`) soil moisture (`r = 0.573` synchronous), linking mid-summer agricultural water demand directly to accelerated late-summer compaction (`data/central_valley/drivers.json`).

---

## 2. Q27 — Statistical Interpretation of GNSS Validation (`data/central_valley/validation.json`)

Comparison spans all `10` continuous NGL IGS20/NA GPS stations across `8` common acquisitions (`2026-06-28` to `2026-10-14`), using 3×3 block-median NISAR vertical estimates (`LOS / cos(θ)`) and 7-day (`±3 d`) median GNSS Up series zero-referenced to `2026-06-28`.

### 2.1 Moving vs. Stable Station Breakdown (`|GNSS|max` threshold = `2.0 cm`)

| Group (`|GNSS|max` criterion) | Stations ($n$) | Median RMSE (`cm`) | Mean RMSE (`cm`) | RMSE Range (`cm`) | Median Pearson $r$ | Mean Pearson $r$ | $r$ Range | Median End-Epoch Diff (`InSAR − GNSS`, `cm`) | Mean Bias (`cm`) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **All Stations** | 10 (`all`) | **1.004** | 1.330 | `0.639–2.791` | **0.541** | 0.379 | `-0.410` to `+0.896` | `+0.961` | `+0.539` |
| **Moving (`|GNSS|max > 2 cm`)** | 5 (`CAFP, CAHA, HANF, QCAP, TLBN`) | **0.834** | 1.263 | `0.752–2.791` | **0.820** | 0.695 | `+0.069` to `+0.896` | `-0.218` | `+0.365` |
| — *Interior Moving (excl. `CAFP`)* | 4 (`CAHA, HANF, QCAP, TLBN`) | **0.800** | 0.881 | `0.752–1.173` | **0.858** | 0.851 | `+0.793` to `+0.896` | `-0.307` | `-0.041` |
| **Stable (`|GNSS|max <= 2 cm`)** | 5 (`CAD1, P056, P564, P565, P566`) | **1.570** | 1.397 | `0.639–1.998` | **-0.101** | 0.064 | `-0.410` to `+0.661` | `+1.866` | `+0.714` |

### 2.2 Per-Station Verification Table (`data/central_valley/validation.json`)

| Station | Regime | $\theta$ (`deg`) | Max `|GNSS|` (`cm`) | GNSS End (`cm`) | InSAR Vert End (`cm`) | End Diff (`cm`) | RMSE (`cm`) | Pearson $r$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
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

### 2.3 Statistical Interpretation (3 Sentences — English)

Across all ten Central Valley cGPS stations, provisional NISAR vertical displacement reproduces independent GNSS trajectories with a median RMSE of `1.004 cm` (`0.834 cm` median across moving sites with `|GNSS|max > 2 cm` vs. `1.570 cm` across stable sites), while Pearson $r$ diverges sharply between moving stations (median `0.820`; `0.793–0.896` at interior Tulare Basin stations `CAHA`, `HANF`, `QCAP`, `TLBN`) and stable stations (median `-0.101`). This contrast occurs because Pearson correlation measures covariance relative to true signal variance: at stable stations (`|GNSS| <= 2 cm`), real ground motion approaches zero and epoch-to-epoch residuals are dominated by `~1–2 cm` unmodeled tropospheric wet-delay fluctuations (plus long-wavelength plane/DEM removal bias), producing near-zero or slightly negative $r$ even when absolute error stays within ~`1.5 cm` RMSE. At high-signal basin stations and along western-margin station `CAFP` (`2.791 cm` RMSE, where `2026-09-08` shows a localized `+4.36 cm` atmospheric spike), RMSE directly bounds geophysical accuracy whereas correlation reliably reflects trajectory agreement only where deformation exceeds atmospheric noise.
