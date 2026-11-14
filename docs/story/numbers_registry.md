# Numbers Registry — Authoritative Source Mapping

> **Calibration Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

Every headline number in the web portal and story documents is traced to its authoritative JSON source (`29` metrics: `22` approved, `7` preliminary, `0` rejected; `0` open discrepancies).

| ID | Value | Unit | Quality | Verdict | Source (`file:key`) | Used In (count) |
|---|---:|---|---|---|---|---:|
| `cv_max_los_cm` | `-7.8` | cm | `provisional` | **approved** | `data/central_valley/summary.json` (`max_subsidence_cm`) | 55 |
| `cv_max_vert_cm_est` | `-10.1` | cm | `provisional` | **approved** | `data/central_valley/summary.json` (`max_subsidence_vertical_cm_estimate`) | 37 |
| `cv_rate_yr_est` | `-26.4` | cm/yr | `provisional` | **preliminary** | `data/central_valley/summary.json` (`rate_cm_per_yr_estimate`) | 13 |
| `cv_area_gt5cm_km2` | `239.54` | km2 | `provisional` | **approved** | `data/central_valley/area_stats.json` (`area_km2_lt_5cm[-1]`) | 4 |
| `cv_area_gt2cm_km2` | `1578.27` | km2 | `provisional` | **approved** | `data/central_valley/area_stats.json` (`area_km2_lt_2cm[-1]`) | 3 |
| `cv_sigma_median_cm` | `0.294` | cm | `provisional` | **approved** | `data/central_valley/uncertainty/meta.json` (`median_sigma_cm`) | 17 |
| `cv_gps_median_rmse_cm` | `1.004` | cm | `provisional` | **approved** | `data/central_valley/validation.json` (`median(rmse_cm)`) | 42 |
| `cv_high_risk_segments` | `81` | segments | `provisional` | **approved** | `data/central_valley/assets.json` (`summary.high_risk_count`) | 20 |
| `cv_pop_gt2cm` | `71701` | people | `provisional` | **approved** | `data/central_valley/exposure.json` (`population.population_subsidence_gt_2cm_los_estimate`) | 12 |
| `cv_crop_share_gt2cm` | `79.2` | % | `provisional` | **approved** | `data/central_valley/exposure.json` (`land_cover_and_crops.cultivated_cropland_gt_2cm_share_percent`) | 17 |
| `cv_fy_max_los_cm` | `-20.3` | cm | `mixed` | **approved** | `data/central_valley_fullyear/summary.json` (`max_subsidence_cm`) | 12 |
| `cv_fy_perm_rate_p01` | `-16.77` | cm/yr | `mixed` | **approved** | `data/central_valley_fullyear/decomp.json` (`point_decompositions[p01].permanent_cm_per_yr`) | 15 |
| `cv_fy_seasonal_p2p_p01` | `11.67` | cm | `mixed` | **approved** | `data/central_valley_fullyear/decomp.json` (`point_decompositions[p01].seasonal_peak_to_peak_cm`) | 22 |
| `cv_fy_storage_loss_km3` | `0.3174` | km3/yr | `mixed` | **approved** | `data/central_valley_fullyear/storage_loss.json` (`volume_km3_per_yr`) | 10 |
| `kp_max_los_cm` | `-5.9` | cm | `provisional` | **approved** | `data/karapinar/summary.json` (`max_subsidence_cm`) | 36 |
| `kp_rate_yr_est` | `-20.0` | cm/yr | `provisional` | **preliminary** | `data/karapinar/summary.json` (`rate_cm_per_yr_estimate`) | 10 |
| `kp_sigma_median_cm` | `0.326` | cm | `provisional` | **approved** | `data/karapinar/uncertainty/meta.json` (`median_sigma_cm`) | 11 |
| `uk_clay_threshold_cm` | `3.62` | cm | `provisional` | **approved** | `data/uk_clay/detection.json` (`detection_threshold_cm`) | 29 |
| `atlas_konya_plain_los_cm` | `-9.6` | cm | `provisional` | **approved** | `data/global/atlas.json` (`regions[konya_plain].max_cm_los`) | 20 |
| `atlas_mashhad_los_cm` | `-8.6` | cm | `provisional` | **approved** | `data/global/atlas.json` (`regions[mashhad].max_cm_los`) | 4 |
| `atlas_jakarta_los_cm` | `-6.8` | cm | `provisional` | **preliminary** | `data/global/atlas.json` (`regions[jakarta].max_cm_los`) | 23 |
| `atlas_bangkok_los_cm` | `-7.5` | cm | `provisional` | **approved** | `data/global/atlas.json` (`regions[bangkok].max_cm_los`) | 3 |
| `atlas_mexico_city_los_cm` | `-7.0` | cm | `provisional` | **approved** | `data/global/atlas.json` (`regions[mexico_city].max_cm_los`) | 29 |
| `atlas_rafsanjan_los_cm` | `-5.8` | cm | `provisional` | **approved** | `data/global/atlas.json` (`regions[rafsanjan].max_cm_los`) | 6 |
| `atlas_ho_chi_minh_los_cm` | `-4.2` | cm | `provisional` | **preliminary** | `data/global/atlas.json` (`regions[ho_chi_minh].max_cm_los`) | 6 |
| `atlas_tehran_los_cm` | `-3.5` | cm | `provisional` | **preliminary** | `data/global/atlas.json` (`regions[tehran].max_cm_los`) | 10 |
| `atlas_isfahan_los_cm` | `-2.5` | cm | `provisional` | **preliminary** | `data/global/atlas.json` (`regions[isfahan].max_cm_los`) | 11 |
| `atlas_beijing_los_cm` | `-1.4` | cm | `provisional` | **preliminary** | `data/global/atlas.json` (`regions[beijing].max_cm_los`) | 10 |
| `atlas_delta_los_cm` | `-1.3` | cm | `provisional` | **approved** | `data/global/atlas.json` (`regions[delta].max_cm_los`) | 15 |
