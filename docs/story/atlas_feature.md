# Where the Ground Is Sinking Fastest in 2026

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

![Global Subsidence Hotspots Measured by NASA–ISRO NISAR in 2026](media/pc10_global.png)
*Figure 1. Standardized 108–120 day cumulative displacement maps across subsiding basins in 2026. Data: NASA-ISRO NISAR via ASF DAAC. Analysis: Team Aseltech.*

When groundwater is pumped faster than rain recharges it, deep fine-grained silt and clay layers compact like a deflating sponge. Over weeks, this silent compaction lowers the ground by centimeters, cracking aqueducts, damaging buildings, and tilting gravity canals. In summer 2026, the newly operational NASA–ISRO Synthetic Aperture Radar (NISAR) satellite began systematic observations of Earth's land surface. Using its long-wavelength (24 cm) L-band radar, NISAR peered through haze and agricultural canopies to map ground motion across entire valleys at unprecedented detail. High school researchers at ASELSAN Vocational and Technical Anatolian High School (Team Aseltech) built an open-source pipeline to compare these sinking regions under a standardized benchmark: the 2026 Global Subsidence Atlas.

Globally, the fastest verified subsidence concentrates in arid agricultural plains and historic lakebed basins where groundwater extraction exceeds recharge. Leading our 21-region 2026 Global Subsidence Atlas (v2, 93-day common window `2026-06-28` to `2026-09-29`, audited in `atlas_top5_check.md`), Türkiye's Konya Plain sank at −11.0 cm/100d common-window (−8.9 cm/100d full, −9.6 cm LOS, with caution due to 11.6% valid coverage). Eloy, Arizona (−8.6 cm/100d common, −8.0 cm LOS), Mashhad Valley (−6.9 cm/100d common, −8.6 cm LOS), and Mexico City (−6.3 cm/100d common, −7.0 cm LOS) follow. California's San Joaquin Valley measures −7.3 cm/100d common (−7.8 cm LOS), where 10 Nevada Geodetic Laboratory GPS stations confirm NISAR within 1.00 cm median RMSE while differential sinking tilts the Tulare Canal (57.01 mm/km) and California Aqueduct (49.12 mm/km).

Crucially, automated time-series quality control (`tools/atlas_qc.py`) caught a single-step 12.1 cm L-band phase-cycle jump in Semarang (−11.18 cm on 29 September–11 October) alongside single-date outliers in Delhi, Beijing, and Bangkok. Reprocessing Semarang without the 11 October phase jump shifted the peak to the northern coast at −6.2 cm LOS (−5.5 cm/100d common, #5 reliable), while Tehran reads −7.4 cm LOS (indicative) against off-basin Alborz bedrock and Cangzhou enters at #7 (−2.4 cm LOS). Pairing open satellite data with strict self-audit turns local groundwater overdraft into reliable planetary vital signs.

---

*Story by Team Aseltech, Ankara, Türkiye. Data courtesy NASA-ISRO NISAR via ASF DAAC, Nevada Geodetic Laboratory, and OpenStreetMap.*
