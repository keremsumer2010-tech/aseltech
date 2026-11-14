# Technical Note: Tracking Agricultural Ground Subsidence, Infrastructure Tilt, and Karst Stress with Provisional NASA–ISRO NISAR L-Band Interferometry

**Document ID:** `NP-TN-2026-01` · **Date:** `14 November 2026` · **Authors:** Team Taykut (ASELSAN Vocational and Technical Anatolian High School, Ankara, Türkiye · NASA Space Apps Challenge 2026, Lincoln, UK)  
**Repository:** https://github.com/keremsumer2010-tech/aseltech · **Live Application:** https://keremsumer2010-tech.github.io/aseltech/  
**Mandatory Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## Abstract

Using open NASA–ISRO NISAR Level-2 Geocoded Unwrapped Interferograms (`GUNW`, `CRID P05023`) and Geocoded Polarimetric Covariance (`GCOV`) products, we developed a reproducible processing and risk-assessment pipeline for irrigated agricultural basins and urban aquifers. After split-spectrum ionospheric subtraction, elevation-aware planar deramping, coherence thresholding (`>= 0.30`), and `1 km` (`13×13` pixel) spatial block-median aggregation, provisional `108–120`-day summer stacks measure peak Line-of-Sight (`LOS`) subsidence of **`−7.8 cm`** in California's Central Valley (`239.54 km² <= −5 cm`), **`−5.9 cm`** in Karapınar (`−9.6 cm` across the wider Konya Closed Basin), **`−1.3 cm`** in the Sacramento–San Joaquin Delta, and **`−6.8` to `−1.4 cm`** across four global cities. Comparison against `10` continuous Nevada Geodetic Laboratory GPS stations yields a cross-station final correlation of **`r = 0.924`** and **`1.00 cm`** median time-series RMSE, while London clay returns **`below_detection`** (`3σ = 3.62 cm`), establishing quantitative error bounds for open water and infrastructure management.

---

## 1. Data & Product Maturity Taxonomy

Every quantitative metric in this repository traces to explicit HDF5/GeoTIFF granules and JSON contracts classified under four strict data-maturity labels:

| Dataset / Folder | Sensor & Product | Period (`n` pairs) | Track / Frame | Quality Class | Primary Role |
|---|---|---|---|---|---|
| `data/central_valley/` | NISAR L2 `GUNW` (`P05023`) | `2026-06-28 → 2026-10-14` (`7`, 108 d) | Track 34 Asc., Frame 20 | `provisional` | Summer Central Valley compaction & canal tilt |
| `data/central_valley/` (desc.) | NISAR L2 `GUNW` (`P05023`) | `2026-06-28 → 2026-10-14` | Track 114 Desc. | `provisional` | Dual-orbit cross-check (`Q21`) & E+U inversion (`Q22`) |
| `data/central_valley_fullyear/` | NISAR L2 `GUNW` | `2025-11-24 → 2026-10-14` (`25`, 324 d) | Track 34 Asc. | `mixed` (`18 beta-precal + 7 prov.`) | Exploratory seasonal vs. permanent decomposition |
| `data/delta/` | NISAR L2 `GUNW` (`P05023`) | `2026-06-17 → 2026-10-15` (`9`, 120 d) | Path 42 Desc., Frame 69 | `provisional` | Handbook Fig. 2-4 Sacramento–San Joaquin Delta levees |
| `data/karapinar/` & `konya_plain/` | NISAR L2 `GUNW` (`P05023`) | `2026-06-26 → 2026-10-12` (`8`, 108 d) | Track 7 Desc., Frame 69 | `provisional` | Karapınar sinkhole belt & full Konya Closed Basin |
| `data/karapinar_fullyear/` | NISAR L2 `GUNW` | `2025-10-17 → 2026-01-09` (`6`) | Track 7 Desc. | `mixed` (`pre-cal beta`) | Early winter baseline prior to provisional series |
| `data/uk_clay/` | NISAR L2 `GUNW` (`P05023`) | `2026-06-21 → 2026-10-19` (`9`, 120 d) | Track 101 Asc., Frame 28 | `provisional` | London clay seasonal shrink–swell negative control |
| `data/fens/` (`crops.json`) | NISAR L2 `GCOV` (`P05023`) | `2026-06-22 → 2026-10-08` (`8` dates) | UK Fens (`4` × `480 m` sites) | `provisional` | Dual-pol (`HH`/`HV`) crop backscatter time series |
| `data/uk/` | GIBS VIIRS + NISAR `GCOV` | `2026-10-20` (same day) | `[−0.3, 52.4, 0.4, 52.9]` | `preview` | Qualitative cloud-penetration browse comparison (`700×500`) |
| `data/global/{mexico_city,tehran,jakarta,beijing}/` | NISAR L2 `GUNW` (`P05023`) | `2026-06-17 → 2026-10-20` (`8–9`, 108–120 d) | Respective regional tracks | `provisional` | Unmodified pipeline global transferability showcase |
| `data/central_valley_s1/` | OPERA `L3_DISP-S1_V1` + NGL + NISAR | Archive ending `2026-04-26` (`2,663` gran.) vs. summer `2026` | Central Valley core | `mixed` | L-band vs. C-band cross-sensor coherence check |
| `data/karapinar/sinkholes.geojson` | Field survey DMS (`Tapur & Bozyiğit 2015`) | `1972–2013` (`29` verified sinkholes) | `[33.3, 37.6, 33.8, 37.9]` | `reference` | Peer-reviewed sinkhole coordinates & depths (`0.5–80 m`) |

Ancillary open datasets include Nevada Geodetic Laboratory (`NGL`) daily `IGS20/NA` GPS coordinates (`10` stations), OpenStreetMap (`ODbL`) canals, roads, and railways (`645` evaluated corridors `>= 1 km` in Central Valley), `WorldPop 100 m (2020)` population (`doi:10.5258/SOTON/WP00645`), `USDA NASS CDL 30 m (2021)`, and `ESA WorldCover 10 m v200 (2021)` (`doi:10.5281/zenodo.7254221`).

---

## 2. Methods

1. **Phase-to-LOS Conversion:** Each `80 m` NISAR `GUNW` `unwrappedPhase` layer ($\Delta\phi$) is converted to Line-of-Sight displacement using the exact granule radar wavelength $\lambda = c / f_0$ from `centerFrequency`:
   $$\Delta r_{\text{LOS}} = -\frac{\lambda}{4\pi}\Delta\phi$$
   with $\lambda = 24.20\text{ cm}$ (`12.10 cm` full $2\pi$ fringe; `6.05 cm` half-cycle unwrapping limit). Negative values indicate surface motion away from the radar (subsidence).
2. **Quality Masking & Outlier Rejection:** Pixels with `coherenceMagnitude < 0.30` or `connectedComponents == 0` are masked (`analysis/insar.py`). Connected valid regions under `200` pixels (`~1.3 km²`) and single-pair jumps exceeding `λ/4` from the `720 m` local median or `> 15.0 cm` are rejected before stacking.
3. **Atmospheric & Topographic Deramping:** Because default `GUNW unwrappedPhase` retains ionospheric and stratified tropospheric delays, `analysis/cumulative.py` subtracts the shipped split-spectrum `ionospherePhaseScreen` (`2.93–17.26 cm` `p1–p99` dispersion per pair) and fits a joint planar + Copernicus DEM (`elevation_m`) trend over stable low-subsidence pixels.
4. **Weighted Temporal Chaining & Spatial Aggregation:** Adjacent `12–24`-day pairs are chained using valid-overlap weighting, referenced to local stable windows (`1 km` medians with coherence `0.86–0.93`), and summarized as **`1 km` (`13×13` pixel) block medians** (`>= 50%` valid pixels, `std <= 2 cm`).
5. **Projections, Inversion & Decomposition:** Pure vertical *estimates* use $\Delta z \approx \Delta r_{\text{LOS}} / \cos\theta$. Where ascending (`Track 34`, $e = +0.64, u = 0.747$) and descending (`Track 114`, $e = -0.60, u = 0.774$) overlap (`49.6%`), least-squares 2-geometry inversion solves East ($E$) and Up ($U$) components (`data/central_valley/vertical.json`). For the `25`-pair full-year chain (`data/central_valley_fullyear/decomp.json`), displacement is modeled as linear secular compaction plus an annual harmonic sinusoid ($R^2 = 0.97$ at Earlimart).
6. **Differential Infrastructure Gradient:** Along `645` OSM corridors (`>= 1 km`), local displacement differences over segment spans yield differential tilt (`mm/km`), tested across `±25%` high-risk thresholds (`7.5 / 10.0 / 12.5 mm/km`).

---

## 3. Cross-Checks & Validation Results

We treat external comparisons strictly as consistency checks rather than formal instrument calibration:

- **Continuous GPS (`NGL IGS20/NA`, `n = 10` stations):** Projecting NISAR `3×3` pixel medians (`LOS / cos θ`) yields a **cross-station final correlation `r = 0.924`** (`1.37 cm` final-epoch RMSE across all `10` stations) and **`1.00 cm` median time-series RMSE** (`1.33 cm` mean TS RMSE; best `0.64 cm` at `P566`). Across the `4` fastest-moving interior stations (`|GPS| > 2.0 cm`: `TLBN, CAHA, QCAP, HANF`), final RMSE improves to **`0.76 cm`** (`r = 0.851` mean temporal, `r = 0.90` at `CAHA` and `HANF`, `docs/story/validation_report.md`).
- **Dual-Orbit Independent Pass (`Track 34 Asc.` ↔ `Track 114 Desc.`):** Across `6,719` matching `1 km` blocks (`28 Jun–14 Oct 2026`), both passes correlate at **`r = 0.489`** (`0.60` locally `< 15 km`, `RMSE = 2.65 cm`, `median diff = −1.29 cm`) with **`85%` sign agreement** where `|d| > 3 cm` (`n = 1,297`). Where Track 34 exceeds `6 cm` sinking, Track 114 records a `−5.7 cm` median; two-orbit vector inversion recovers **`−7.2 cm` vertical sinking and only `−0.1 cm` east-west motion** in the Alpaugh/Earlimart bowl (`max −9.8 cm` vertical).
- **L-Band vs. C-Band (`OPERA_L3_DISP-S1_V1`, `docs/story/cross_sensor.md`):** In the irrigated Tulare agricultural core, NISAR (`24.20 cm` L-band) retains **`80.4%` valid pixels (`coh >= 0.30`, median `0.539`)** in summer (`92.7%` winter, `77.6%` spring) and matches `5` core GPS stations at **`RMSE = 0.823 cm` (`r = 0.7462`)**. Five single `12–24`-day Tulare/Earlimart steps (`−2.89` to `−5.10 cm`) exceed C-band's `2.77 cm` full fringe, and Earthdata CMR (`2,663` Sentinel-1 granules) ends on `2026-04-26` (`0` granules in our `2026-06-28 → 2026-10-14` window).
- **London Clay Negative Control (`data/uk_clay/detection.json`, `docs/story/uk_findings.md`):** Over `9` provisional Track 101 pairs (`21 Jun–19 Oct 2026`, `120` days), quadratic atmosphere removal leaves **`97.7%` of `1 km` blocks within `±1.5 cm`** (`p2/p50/p98 = −1.47 / +0.19 / +1.26 cm`) with `0` interior blocks exceeding the `3σ = 3.62 cm` detection threshold (`status: "below_detection"`).

---

## 4. Uncertainty & Sensitivity Budget

1. **Formal Phase-Noise Bound (`Cramér-Rao`, `data/*/uncertainty/meta.json`):** At `L = 208` nominal looks per `80 m` pixel, Cramér-Rao phase-noise medians are **`0.294 cm` LOS** in Central Valley and **`0.326 cm` LOS** in Karapınar.
2. **Empirical Residual & Chain Uncertainty (`docs/story/uncertainty.md`):** Post-deramp single-pair spatial RMS is **`0.66 cm`**, propagating to **`1.74 cm` local** (`SNR 2.7×–4.5×` at `−7.8 cm`) and **`2.87 cm` full-scene** cumulative uncertainty across `7` pairs, while independent London clay yields `chain_sigma = 1.21 cm` over `9` pairs. Zero half-cycle (`>= 6.05 cm`) unwrapping jumps were observed across `12` Central Valley and `12` Karapınar sampled points.
3. **Reference-Area Sensitivity:** Re-referencing each cumulative stack across `2–3` independent stable patches shows substantial regional spread in wide/urban scenes: `[−7.8, −4.7] cm` in Central Valley summer, `[−20.3, −11.7] cm` in Full-Year CV, `[−14.0, −9.6] cm` in Konya Basin, `[−1.3, −1.1] cm` in Delta, `[−7.4, −4.4] cm` in Mexico City, `[−7.3, −3.5] cm` in Tehran, and `[−7.6, −1.4] cm` in Beijing.

---

## 5. Multi-Region Results Summary

- **Central Valley Summer (`2026-06-28 → 2026-10-14`, `7` pairs):** Peak **`−7.8 cm` LOS** (`−10.1 cm` vert. est. at `39.1°`, `6 km N of Terra Bella`); common-valid footprint (`7,704.68 km²`) includes **`239.54 km² <= −5 cm`** and **`1,578.27 km² <= −2 cm`**. Out of `645` OSM corridors, **`81` (`12.6%`)** are high-risk, led by **Tulare Irrigation District Canal (`57.01 mm/km`)** and **`102.8 km` of the California Aqueduct (`49.12 mm/km`)**, with top-10 ranking **100% invariant** across `±25%` thresholds (`72–115` total high-risk).
- **Central Valley 11-Month Decomposition (`2025-11-24 → 2026-10-14`, `25` pairs, `quality: "mixed"`):** Near Earlimart (`p01`), cumulative settlement reaches **`−20.3 cm` LOS** (`−26.9 cm` vert. est.), decomposing (`R² = 0.97`) into **`−16.8 ± 2.2 cm/yr` permanent compaction** (`−14.9 cm` over `324` days) and **`11.7 cm` peak-to-peak seasonal bounce** (`1.28:1` ratio; basin median `−3.74 cm/yr` permanent vs. `3.32 cm` seasonal).
- **Sacramento–San Joaquin Delta (`2026-06-17 → 2026-10-15`, `9` pairs):** `1 km` block-median peak **`−1.3 cm` LOS** (`−1.6 cm` vert. est. at `35.8°`); `N = 87` OSM levee alignment samples show a `10th` percentile of `−3.48 cm` LOS and reach `−11.36 cm` on a `4.09 km` segment (`docs/story/delta.md`).
- **Konya Closed Basin & Karapınar Sinkholes (`2026-06-26 → 2026-10-12`, `8` pairs):** Full-basin `1 km` median peak reaches **`−9.6 cm` LOS** south of Konya city (`−12.1 cm` vert. est., `32.628°E, 37.816°N`, `docs/story/konya_plain.md`). Inside Karapınar (`−5.9 cm` LOS peak, `−8.0 cm` vert. est., `3.10 km² <= −5 cm`, `28.66 km² <= −2 cm`), pixels within `0–1 km` of `29` verified sinkholes sink **`6.4×` faster** (`−4.15 cm` vs. `−0.65 cm` beyond `5 km`); discrete `1.04 km` block permutations (`p = 0.0001`, Welch `p = 9.7 × 10⁻⁸`) and `3,423` rigid constellation shifts (`p = 0.0207`, `docs/story/sinkhole_stats.md`) confirm significant spatial association over shared drawdown.
- **Population, Crop & UK Fens Polarimetry (`exposure.md`, `polarization.md`):** Across Central Valley + Konya Basin `> 2 cm` LOS footprints, **`141,555` estimated residents** (`71,701` CV + `69,854` Konya Basin, `11,572` in Karapınar; `196,949` with `<= 2.5 km` basin interpolation) live on subsiding ground; **`79.2%` (`1,251.37 km²`)** of Central Valley `> 2 cm` land is cultivated cropland led by **citrus (`355.64 km²`)** and **pistachios (`230.92 km²`)**. In the UK Fens (`4` fields, `8` `GCOV` dates), `HH` sits **`~7 dB` brighter** than `HV` (`4.27` vs. `3.49 dB` temporal range).
- **Four Global Cities (`docs/story/global_showcase.md`):** Unmodified pipeline execution records `1 km` peak LOS subsidence of **`−4.4 cm` (Mexico City)**, **`−3.5 cm` (Tehran)**, **`−6.8 cm` (Jakarta, `2.9%` valid pixels)**, and **`−1.4 cm` (Beijing, `[−7.6, −1.4] cm` ref. spread)**.

### 5.1 Global Subsidence Atlas (2026 Provisional Benchmark)

Using the single-command `pipeline/nisarpulse/` engine with identical `provisional`-only (`>= 2026-06-17`, `P05023`) thresholds across basins worldwide, our expanding **2026 NISAR Global Subsidence Atlas** currently ranks `8` completed regions (`108–120` summer–autumn days; additional cities from `data/global/atlas.json` are appended as acquisitions complete):

| Rank | Region / City | Period (`n` pairs) | Peak 1 km LOS (`cm`) | Ref. Range (`cm`) | Vertical Est. (`cm`) | Linearized Rate Est. (`cm/yr`) | Coverage / Note |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | **Konya Closed Basin, Türkiye** | `2026-06-26 → 2026-10-12` (`8`) | **`−9.6`** | `[−14.0, −9.6]` | `−12.1` | `−32.5` | Full basin (`provisional`) |
| 2 | **Central Valley, USA** | `2026-06-28 → 2026-10-14` (`7`) | **`−7.8`** | `[−7.8, −4.7]` | `−10.1` | `−26.4` | 10-GPS `r = 0.924`, `1.00 cm` RMSE |
| 3 | **Jakarta, Indonesia** | `2026-06-27 → 2026-10-13` (`8`) | **`−6.8`** | 1 ref only | `−9.3` | `−23.2` | `2.9%` valid pixels (tropical veg.) |
| 4 | **Karapınar, Türkiye** | `2026-06-26 → 2026-10-12` (`8`) | **`−5.9`** | — | `−8.0` | `−19.9` | 29 sinkholes (`p = 0.0001` perm.) |
| 5 | **Mexico City, Mexico** | `2026-06-22 → 2026-10-20` (`8`) | **`−4.4`** | `[−7.4, −4.4]` | `−6.2` | `−13.5` | Eastern lakebed clays |
| 6 | **Tehran, Iran** | `2026-06-18 → 2026-10-16` (`9`) | **`−3.5`** | `[−7.3, −3.5]` | `−4.7` | `−10.7` | SW Tehran plain trough |
| 7 | **Beijing, China** | `2026-06-17 → 2026-10-15` (`9`) | **`−1.4`** | `[−7.6, −1.4]` | `−2.1` | `−4.3` | Wide reference sensitivity |
| 8 | **Sacramento–San Joaquin Delta, USA** | `2026-06-17 → 2026-10-15` (`9`) | **`−1.3`** | `[−1.3, −1.1]` | `−1.6` | `−4.0` | Levee samples reach `−11.36 cm` |

---

## 6. Original Contributions (`docs/OZGUN_KATKILAR.md`)

1. **O1 — Permanent Aquifer Storage Loss (`km³/yr`):** Integrating valid `v_vert < −1.0 cm/yr` pixels from `decomp.json` (`4,508.29 km²`, mean vertical rate `7.04 cm/yr`, median `41.53°` incidence, `quality: "mixed"`) under the USGS Circular 1182 inelastic-storage convention yields **`0.3174 km³/yr`** (`317.41 million m³/yr`; net basin **`0.3110 km³/yr`** across `5,384.88 km²`), with a `1 km` block SE (`±0.00123 km³/yr`) plus 3-reference sensitivity range of **`0.0664–0.3198 km³/yr`** (`~0.49×` Millerton Lake `0.642 km³`, comparable in order of magnitude to `0.138–0.249 km³/yr` in Smith et al. 2017; `data/central_valley_fullyear/storage_loss.json`, [`docs/story/storage_loss.md`](storage_loss.md)).
2. **O2 — Probabilistic Engineering Infrastructure Risk:** Computes structural angular distortion ($\beta = \Delta s / L$, Skempton & MacDonald 1956; Boscardin & Cording 1989) and canal freeboard-loss differential settlement along `1 km` corridor samples, propagating pixel-level $\sigma$ through `1,000` Monte Carlo trials to yield threshold-exceedance probabilities. **[pending PC7: `data/central_valley/assets_prob.json` & `docs/story/engineering_risk.md`]**
3. **O3 — `pipeline/nisarpulse/` Operational CLI Engine:** Packages the established search (`search.py`), `20.0 GB`-floored streaming HDF5 subsetting (`fetch.py`), `analysis/cumulative.py` processing (`process.py`), and `VERI_SOZLESMESI.md` cataloging (`catalog.py`) into a tested CLI (`python -m pipeline.nisarpulse run`). Verified end-to-end on the Sacramento–San Joaquin Delta (`delta`, `2026-06-17 → 2026-10-15`, `9` chain pairs, `0` gaps, `quality="provisional"`): dry-run `1.20 s`, cached `--resume` execution `6.9 s` (`-1.3 cm` peak LOS), and `6/6` offline unit tests passing in `0.016 s` (plus CI `pytest` via `.github/workflows/tests.yml`; [`engine.md`](engine.md)).

---

## 7. Limitations

- **Product Maturity:** All core products carry NASA–ISRO **`provisional`** status; `data/central_valley_fullyear/` and `data/karapinar_fullyear/` mix pre-calibration `beta` acquisitions (`< 2026-06-17`) and must be interpreted with caution (`quality: "mixed"`).
- **Summer-Only Extrapolation:** Linear `cm/yr` projections from `108–120` summer irrigation days (`−26.4 cm/yr` CV, `−32.5 cm/yr` Konya Basin) illustrate seasonal peak stress and overstate net multi-year compaction where winter recharge occurs.
- **Moisture Driver Sample Size (`drivers_analysis.md`):** Summer `SME2` irrigation coupling (`r = 0.654`, `r = 0.638` lagged) yields `p_perm = 0.088` and `0.130` over `N = 8` acquisitions—non-significant at `α = 0.05` (`|r_crit| = 0.707–0.754`); detrended rates give `r = 0.037–0.130` (`p >= 0.81`).
- **Atmospheric Residual, Geometry & Static Overlays:** Single-season unmodeled troposphere adds `~1 cm` spatial uncertainty (`3σ = 3.62 cm` in London clay); single-orbit vertical conversions assume negligible horizontal motion; tropical decorrelation restricts Jakarta to `2.9%` valid coverage; `WorldPop (2020)` and `CDL/WorldCover (2021)` overlays precede `2026` InSAR acquisitions.
- **Karst Collapse Forecasting:** Regional L-band subsidence cannot predict exact collapse dates or locations of individual brittle limestone sinkholes.

---

## References (Verified Live `HTTP 200` via `docs/story/sources.md`)

1. Peacock, A., An, K., Pinto, N., & Lou, Y. (2024). *NISAR Land Subsidence StoryMap*. Zenodo / ArcGIS StoryMaps: https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828
2. NASA–JPL NISAR Societal Benefits & Applications White Papers (Subsidence, Drought & Groundwater, Levees & Dams, Sinkholes, Food Security, Soil Moisture): https://science.nasa.gov/mission/nisar/societal-benefits/
3. Alaska Satellite Facility (ASF) NISAR Data User Guide & GUNW Product Specification: https://nisar-docs.asf.alaska.edu/gunw
4. Neely et al. (2021), *Water Resources Research* 57(4):e2020WR028451: https://pmc.ncbi.nlm.nih.gov/articles/PMC8047915/
5. Ojha, Werth, & Shirzaei (2019), *JGR Solid Earth* 124:3127–3143: https://pmc.ncbi.nlm.nih.gov/articles/PMC6559157/
6. Orhan et al. (2021), *Sensors* 21(3):774: https://pmc.ncbi.nlm.nih.gov/articles/PMC7865528/
7. Üstün, Tuşat, & Yalvaç (2010), *NHESS* 10:1151–1164: https://nhess.copernicus.org/articles/10/1151/2010/
8. Haghighi & Motagh (2024) (Tehran InSAR): https://pmc.ncbi.nlm.nih.gov/articles/PMC11086625/
9. Abidin et al. (2015), *PIAHS* 372:115–120 (Jakarta): https://piahs.copernicus.org/articles/372/115/2015/
10. Tapur & Bozyiğit (2015), *Marmara Coğrafya Dergisi* 31: https://dergipark.org.tr/tr/download/article-file/3454
11. NASA SERVIR (2019), *SAR Handbook Ch. 2*: https://earthdata.nasa.gov/s3fs-public/2025-04/SARHB_CH2_Content.pdf
12. USDA NASS Cropland Data Layer (`CDL`, 30 m): https://www.nass.usda.gov/Research_and_Science/Cropland/SARS1a.php
13. Full `43`-source catalog & dataset contracts: [`docs/story/sources.md`](sources.md) · [`docs/story/validation_report.md`](validation_report.md) · [`docs/story/uncertainty.md`](uncertainty.md) · [`docs/story/cross_sensor.md`](cross_sensor.md) · [`docs/story/exposure.md`](exposure.md)
