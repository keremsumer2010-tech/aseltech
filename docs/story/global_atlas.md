# NISAR Pulse Global Land Subsidence Atlas (June–October 2026)

*Provisional NISAR L2 GUNW (`P05023`, `>= 2026-06-17`) cumulative line-of-sight (LOS) measurements across 20 sinking regions.*

> **Data notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team. Summer-only windows (96–120 days) are normalized to **`cm / 100 days`** (`rate_cm_per_100d`) rather than assuming a year-round linear rate, because seasonal groundwater pumping peaks in summer and partially rebounds in winter.

## Summary

- **Total regions in `data/global/atlas.json`:** 20 (`8 reliable`, `12 indicative`)
- **Open-data exports:** `data/global/atlas.geojson` and `data/global/atlas.csv` (updated on every `build_atlas.py` run).
- **Confidence & QC rules (`KALİTE STANDARDI` + `ATLAS_FINAL §2` + `tools/atlas_qc.py`):**
  - `reliable` (`8` regions): `valid_fraction >= 0.30` (or legacy baseline), `detectable != false`, `robustness_spread <= |max_cm_los| / 2`, and no `qc_flags.json` time-series anomaly.
  - `indicative` (`12` regions): flagged by low valid fraction, wide reference/robustness spread, or time-series QC (`delhi`, `beijing`, `bangkok`).

## Top 10 Ranked by `atlas.json` Order (`reliable` first, then `indicative` by `rate_cm_per_100d`)

| Rank | Region | Country | Rate (`cm/100d`) | Max LOS (`cm`) | `p2` (`cm`) | Valid Frac | Confidence |
| ---: | :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| 1 | Konya Plain | Türkiye | -8.9 | -9.6 | — | — | medium (`reliable`) |
| 2 | Mashhad | Iran | -7.2 | -8.6 | -6.68 | 0.705 | medium (`reliable`) |
| 3 | Eloy | USA | -6.7 | -8.0 | -4.3 | 0.696 | high (`reliable`) |
| 4 | Semarang | Indonesia | -6.5 | -6.2 | -5.2 | 0.515 | medium (`reliable`) |
| 5 | Mexico City | Mexico | -5.8 | -7.0 | -5.7 | 0.639 | medium (`reliable`) |
| 6 | Rafsanjan | Iran | -4.8 | -5.8 | -4.3 | 0.847 | medium (`reliable`) |
| 7 | Quetta | Pakistan | -3.2 | -3.8 | -2.5 | 0.713 | medium (`reliable`) |
| 8 | Sacramento–San Joaquin Delta | USA | -1.1 | -1.3 | — | — | medium (`reliable`) |
| 9 | Central Valley (Tulare Basin) | USA | -7.2 | -7.8 | -5.8 | 0.629 | low (`indicative`, robustness spread) |
| 10 | Jakarta | Indonesia | -6.3 | -6.8 | -10.2 | 0.029 | low (`indicative`, low valid frac) |

## Key Methodological Notes

- **Semarang phase-cycle fix:** Removing the single-pair `2026-09-29→2026-10-11` unwrapping jump (`-11.18 cm` ≈ 1 L-band cycle `12.1 cm` in the SW upland) moved the 7-pair (`2026-06-25→2026-09-29`, 96 d) peak directly onto the northern Semarang–Demak coastal plain (`110.6080E, -6.8100S`, `-6.2 cm` LOS, `-6.5 cm/100d`), clearing `qc_flags.json`.
- **Mexico City off-basin re-referencing:** Re-referencing from the northern lakebed margin (`-99.0126E, 19.5872N`, `-4.4 cm`) to stable volcanic bedrock on the SW margin (`-99.1840E, 19.3767N`) increased the measured LOS peak to **`-7.0 cm`** (`2.6 cm` difference).
