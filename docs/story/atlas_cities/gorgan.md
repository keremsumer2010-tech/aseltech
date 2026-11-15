# Gorgan Plain, Iran — Confined Aquifer & Phase-Jump QC Flag

**Driver & Risk:** Agricultural groundwater extraction from the Gorgan Confined Aquifer System near the Khazar fault zone compacts thick aquitards, stressing roads, irrigation networks, and settlements.

**Literature:** Rezaei et al. ([2019](https://doi.org/10.1016/j.jhydrol.2019.124196)) measured ~7 cm/yr inelastic mean subsidence via Sentinel-1 InSAR, while Ma et al. ([2026](https://doi.org/10.5194/isprs-annals-XI-3-2026-433-2026)) reported localized LOS velocities up to 13 cm/yr.

**NISAR L-Band Measurement (`provisional`, `indicative only`):** Over 2026-06-21 to 2026-10-19 (9 pairs, 120 days), raw output reads **−34.6 cm** LOS (**−22.7 cm/100d** common, 26.7% valid, 2-ref −34.6 to −13.8 cm). However, automated QC flagged a `phase_cycle_jump` (−10.26 cm on 2026-07-03→07-15); without that step, the point reads −24.39 cm.

**NISAR Value:** Self-audit QC isolates unwrapping errors before ranking while confirming strong summer drawdown requiring `--qc` reprocessing.

*NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*
