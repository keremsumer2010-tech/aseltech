# Global Subsidence Atlas — Literature & NISAR First-Measurement Audit

> **Calibration Notice:** NISAR L2 GUNW (`CRID P05023`) products used across the atlas are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

This audit (`2026-11-14`) evaluates the 8 initial regions in `data/global/atlas.json` against peer-reviewed InSAR/GNSS subsidence literature, `docs/ATLAS_PLANI.md` Quality Standard rules (§1–§4), and prior NISAR publications. Per team policy, no unverified headline number may enter `docs/story/press_summary.md` or demo narration.

---

## 1. "Measured With NISAR for the First Time?" Literature Scan

1. **Mexico City (NOT first with NISAR):** NASA-JPL already published preliminary NISAR L-band InSAR subsidence results for Mexico City using October 2025 – January 2026 acquisitions (`> 2 cm/month` near the airport and eastern lakebed). Individual-city "first with NISAR" claims must NOT be made for Mexico City.
2. **Other 7 regions (`Central Valley`, `Delta`, `Konya Plain`, `Karapınar`, `Jakarta`, `Tehran`, `Beijing`):** As of `2026-11-14`, literature searches found no peer-reviewed spaceborne NISAR L-band time-series publication or standardized multi-basin global NISAR subsidence ranking covering these cities (note that NASA's NISAR StoryMap documented the Central Valley previously with airborne L-band UAVSAR in `2013–2017`).
3. **Allowable wording for the Atlas:** Use qualified phrasing only: *"To our knowledge, one of the first standardized multi-basin comparisons built on provisional NISAR L-band GUNW data using a single open-source pipeline."* Never use an unqualified "world's first" claim.

---

## 2. Eight-Region Validation Summary & Press Summary Gate

| Region | Period (`days`) | Measured Peak (`cm` LOS / `cm` vert *est.*) | `rate_cm_per_100d` (`cm/100 d` LOS) | Valid Pixels | Ref Spread / Peak | Published Vertical Range (`cm/yr`) | Recommended Confidence | Press Approved |
|---|---|---:|---:|---:|---:|---|---|---|
| **Sacramento–San Joaquin Delta** | `2026-06-17` to `2026-10-15` (`120 d`) | `-1.3` / `-1.6` | `-1.08` | `43.4%` | `0.15` | `-1.2` to `-2.2` (`Deverel & Leighton 2010`) | `high` | **Yes** |
| **Central Valley (Tulare)** | `2026-06-28` to `2026-10-14` (`108 d`) | `-7.8` / `-10.1` | `-7.22` | `64.2%` | `0.40` | `-17.7` to `-34.5` peak (`Neely et al. 2021`); `-16.8 cm/yr` perm. LOS full-year | `medium` | **Yes** (with GPS `RMSE 1.0 cm` + full-year note) |
| **Karapınar, Konya** | `2026-06-26` to `2026-10-12` (`108 d`) | `-5.9` / `-8.0` | `-5.46` | `14.5%` | `n_ref=1` | `-1.2` to `> -7.0` (`Üstün et al. 2010`; `Orhan et al. 2021`) | `low` | **Conditional** (sinkhole contrast `p = 0.021` only; exclude `-20.0 cm/yr` annual extrapolation) |
| **Konya Plain** | `2026-06-26` to `2026-10-12` (`108 d`) | `-9.6` / `-12.1` | `-8.89` | `11.6%` | `0.46` | `-1.2` to `> -7.0` (`Üstün et al. 2010`; `Orhan et al. 2021`) | `low` | **No** (pending standardized `±0.25°` bbox & full-year separation) |
| **Mexico City** | `2026-06-22` to `2026-10-20` (`120 d`) | `-4.4` / `-6.2` | `-3.67` | `63.9%` | `0.68` | `-30` to `-40` (`Chaussard et al. 2014`; `Cigna & Tapete 2021`) | `low` | **No** (in-basin Ecatepec ref + clipped `0.35°` bbox; see `docs/qa/PC5.md` §8) |
| **Tehran** | `2026-06-18` to `2026-10-16` (`120 d`) | `-3.5` / `-4.7` | `-2.92` | `36.4%` | `1.09` | `-15` to `-36` (`Haghighi & Motagh 2019`; `Mahmoudpour et al. 2016`) | `low` | **No** (primary ref in Shahriar cone; `alt_ref` gives `-7.3 cm` LOS) |
| **Beijing** | `2026-06-17` to `2026-10-15` (`120 d`) | `-1.4` / `-2.1` | `-1.17` | `73.0%` | `4.43` | `-1.0` to `-15.0` (`Chen et al.`; `Zhou et al.`) | `low` | **No** (primary ref in Tongzhou funnel; `alt_ref` gives `-7.6 cm` LOS) |
| **Jakarta** | `2026-06-27` to `2026-10-13` (`108 d`) | `-6.8` / `-9.3` | `-6.30` | `3.0%` | `n_ref=1` | `-1` to `-15` avg, hotspots `-20` to `-28` (`Abidin et al. 2011`; `Hakim et al.`) | `low` | **No** (`3.0%` valid pixels, indicative only) |

Machine-readable outputs for `pipeline/pc10/build_atlas.py` are stored in `data/global/<id>/validation_note.json` for all 8 regions.
