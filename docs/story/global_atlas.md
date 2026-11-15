# NISAR Vision Global Land Subsidence Atlas (June–October 2026)

*Provisional NISAR L2 GUNW (`P05023`, `>= 2026-06-17`) cumulative line-of-sight (LOS) measurements across 27 sinking regions, ranked over a common 93-day window (`2026-06-28` to `2026-09-29`).*

> **Data notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

## Summary

- **Total regions in `data/global/atlas.json`:** 27 (`13 reliable`, `14 indicative`)
- **Common ranking window:** `2026-06-28` → `2026-09-29` (93 days), using `rate_cm_per_100d_common` interpolated from each region's `most_subsiding` series (`points.json`).
- **Open-data & transparency:** `data/global/atlas.geojson`, `data/global/atlas.csv`, and `data/global/atlas_changelog.json`.

## Top 10 Ranked by `rate_cm_per_100d_common` (`reliable` first)

| Rank | Region | Country | Common Rate (`cm/100d`) | Full Rate (`cm/100d`) | Max LOS (`cm`) | `σ_med` (`cm`) | Confidence |
| ---: | :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| 1 | Konya Plain | Türkiye | -11.0 | -8.9 | -9.6 | 0.332 | medium (`reliable`) |
| 2 | Eloy | USA | -8.6 | -6.7 | -8.0 | — | high (`reliable`) |
| 3 | Kashmar | Iran | -7.0 | -5.2 | -6.2 | — | high (`reliable`) |
| 4 | Mashhad | Iran | -6.9 | -7.2 | -8.6 | 0.318 | medium (`reliable`) |
| 5 | Mexico City | Mexico | -6.3 | -5.8 | -7.0 | 0.343 | medium (`reliable`) |
| 6 | Semarang | Indonesia | -5.5 | -6.5 | -6.2 | 0.354 | medium (`reliable`) |
| 7 | Kerman | Iran | -5.3 | -5.1 | -6.1 | 0.258 | high (`reliable`) |
| 8 | Rafsanjan | Iran | -4.2 | -4.8 | -5.8 | 0.330 | medium (`reliable`) |
| 9 | Can Tho | Vietnam | -3.4 | -2.8 | -3.4 | 0.492 | medium (`reliable`) |
| 10 | Tianjin | China | -2.8 | -2.4 | -2.9 | 0.329 | medium (`reliable`) |
