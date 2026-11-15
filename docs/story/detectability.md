# Global Atlas Detectability & Minimum Detectable Rate

> **Calibration Notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

Across 12 atlas basins (`2026-06-17` to `2026-10-21`, `108–120` days), median formal radar phase-noise uncertainty is `0.29–0.36 cm` (`2-sigma` threshold `0.578 cm/100 d`, range `0.544–0.615 cm/100 d`). All 12 of 12 basins exceed `2-sigma` (`SNR = 3.7–28.9`). Because formal phase noise excludes atmospheric water-vapor turbulence, our UK London Clay control (`data/uk_clay/detection.json`) sets the empirical scene-level `3-sigma` floor at `3.62 cm`.

| City | Period (`days`) | Rate (`cm/100 d` LOS) | `2-sigma` Noise (`cm/100 d`) | `SNR` | Min Detectable (`cm/100 d`) | Detectable |
|---|---:|---:|---:|---:|---:|:---:|
| `konya_plain` | `108 d` | `-8.89` | `±0.615` | `28.9` | `0.615` | **true** |
| `central_valley` | `108 d` | `-7.22` | `±0.544` | `26.5` | `0.544` | **true** |
| `jakarta` | `108 d` | `-6.30` | `±0.615` | `20.5` | `0.615` | **true** |
| `bangkok` | `120 d` | `-6.25` | `±0.545` | `22.9` | `0.545` | **true** |
| `mexico_city` | `120 d` | `-5.80` | `±0.572` | `20.4` | `0.572` | **true** |
| `karapinar` | `108 d` | `-5.46` | `±0.604` | `18.1` | `0.604` | **true** |
| `rafsanjan` | `120 d` | `-4.83` | `±0.550` | `17.6` | `0.550` | **true** |
| `ho_chi_minh` | `120 d` | `-3.50` | `±0.607` | `11.5` | `0.607` | **true** |
| `tehran` | `120 d` | `-2.92` | `±0.577` | `10.1` | `0.577` | **true** |
| `isfahan` | `120 d` | `-2.08` | `±0.578` | `7.2` | `0.578` | **true** |
| `beijing` | `120 d` | `-1.17` | `±0.607` | `3.8` | `0.607` | **true** |
| `delta` | `120 d` | `-1.08` | `±0.578` | `3.7` | `0.578` | **true** |

Figure 1. Subsidence rate (`cm/100 d` LOS) with formal `2-sigma` Cramér-Rao error bars and minimum detectable rate threshold (`docs/story/media/pc5_detectability.png`). Data: NASA-ISRO NISAR, ASF DAAC. Analysis: Team Aseltech.
