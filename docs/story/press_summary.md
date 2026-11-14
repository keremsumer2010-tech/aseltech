# Press Summary: Tracking Earth's Sinking Aquifers from Space with NASA–ISRO NISAR

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

![Same NISAR L-band engine applied across four sinking regions](media/pc10_global.png)

**Ankara / Lincoln — 14 November 2026.** Using open **provisional** L-band radar interferograms from the newly operational NASA–ISRO **NISAR** satellite (`CRID P05023`, `>= 17 June 2026`), high school student team **Team Taykut** (ASELSAN Vocational and Technical Anatolian High School, Ankara) has built an open-source, single-command processing and risk platform—**NISAR Pulse**—that maps groundwater-driven land subsidence, infrastructure tilt, and human exposure across agricultural basins worldwide.

Over California's **Central Valley** (`2026-06-28 → 2026-10-14`, `108` days, `7` provisional pairs), NISAR L-band interferograms track up to **`−7.8 cm` line-of-sight (LOS) subsidence (`−7.22 cm / 100 days`)** near Terra Bella (`−10.1 cm` vertical *estimate*) and match `10` continuous Nevada Geodetic Laboratory GPS stations at **`r = 0.924` (`1.00 cm` median RMSE)**. Along `645` mapped canal and road corridors, `81` segments exceed `20 mm/km` tilt, led by the **Tulare Irrigation District Canal (`57.01 mm/km`)** and **California Aqueduct (`49.12 mm/km`)**. Applying the identical workflow to Türkiye's **Karapınar basin** (`2026-06-26 → 2026-10-12`, `108` days, `8` pairs) measures **`−5.9 cm` LOS peak subsidence (`−5.46 cm / 100 days`)** and shows that farmland within `1 km` of `29` verified karst sinkholes sank **`6.4×` faster (`−4.15 cm`)** than terrain beyond `5 km` (`−0.65 cm`, `p = 0.0001` permutation test), while flagging Highway `42-42` at `19.74 mm/km` only `597 m` from **Köken Obruğu-II**.

To turn multi-gigabyte satellite files into actionable local decisions, **NISAR Pulse** pairs a multi-region 2D/3D web explorer (`web/`, `web3d/`) with **Valley Under Pressure**, a 24-month Terzaghi soil-compaction simulator matched to NISAR's Terra Bella measurements (`k = 0.6232`), and an expanding **2026 Global Subsidence Atlas** (`pipeline/nisarpulse/`, `data/global/atlas.json`, audited in `docs/story/atlas_validation.md`)—to our knowledge, one of the first standardized multi-basin comparisons built on provisional NISAR L-band GUNW data using a single open-source pipeline. The atlas normalizes all basins to a period-independent **`cm per 100 days` Line-of-Sight (LOS)** rate over single `108–120`-day summer windows (including our Press-Approved Sacramento–San Joaquin Delta levee run at `−1.3 cm` LOS / `−1.08 cm per 100 days`, off-basin Mexico City rerun at `−7.0 cm` LOS / `−5.80 cm per 100 days`, and Isfahan at `−2.5 cm` LOS / `−2.08 cm per 100 days`), tags unverified basins as **`preliminary`**, separates low-coverage scenes as **`indicative only`**, and reports honest detection limits (`below_detection` over London clay). Overlaying WorldPop population grids and USDA/ESA land cover identifies **`141,555` estimated residents** living on `> 2 cm` LOS subsiding ground across the Central Valley and Konya Basin (`79.2%` of California's `> 2 cm` footprint is active cropland).

### Key Numbers at a Glance
- **`1.00 cm` median GPS RMSE (`r = 0.924`)** across `10` continuous Central Valley stations (`−7.8 cm` LOS / `−7.22 cm per 100 days` over `108` days).
- **`57.01 mm/km` peak canal tilt** (`81 / 645` segments `> 20 mm/km` in California; `6.4×` faster sinking within `1 km` of `29` Karapınar sinkholes, `p = 0.0001`).
- **`141,555` estimated residents** on `> 2 cm` LOS ground across Central Valley (`71,701`) and Konya Basin (`69,854`, incl. `11,572` in Karapınar).

### Project Links & Contact
- **Live Interactive Web Application:** https://keremsumer2010-tech.github.io/aseltech/
- **Open-Source Repository & Data:** https://github.com/keremsumer2010-tech/aseltech
- **Team:** Team Taykut — ASELSAN Vocational and Technical Anatolian High School, Ankara, Türkiye (NASA Space Apps Challenge 2026, Lincoln, UK)
