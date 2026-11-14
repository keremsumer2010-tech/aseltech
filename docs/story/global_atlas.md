# NISAR Pulse Global Land Subsidence Atlas (June–October 2026)

*Provisional NISAR L2 GUNW (`P05023`, `>= 2026-06-17`) cumulative line-of-sight (LOS) measurements across 19 sinking regions.*

> **Data notice:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team. Summer-only windows (108–120 days) are normalized to **`cm / 100 days`** (`rate_cm_per_100d`) rather than assuming a year-round linear rate, because seasonal groundwater pumping peaks in summer and partially rebounds in winter.

## Summary

- **Total regions in `data/global/atlas.json`:** 19 (`11 reliable`, `8 indicative`)
- **Methodology:** Each site uses consecutive 12–24 day provisional `P05023` pairs processed through `analysis/cumulative.py` (plane-only per-pair deramp where DEM is unavailable). Headline values report the most negative 1 km block median (`13x13` px), paired with `p2_cm` (2nd-percentile pixel displacement), `valid_fraction` (fraction of pixels valid across the full chain), and `ref_range_cm` (sensitivity across up to 3 stable reference windows `>= 30 km` apart).
- **Confidence tiers (`KALİTE STANDARDI §1`):**
  - `reliable` (`11` regions): `valid_fraction >= 0.30` (or legacy baseline) and reference spread `<= 4.5 cm`.
  - `indicative` (`8` regions): `valid_fraction < 0.30` or reference spread `> 4.5 cm` (`jakarta`, `karapinar`, `ho_chi_minh`, `tehran`, `yunlin`, `hanoi`, `isfahan`, `xian`).

## Top 10 Ranked by `rate_cm_per_100d` (LOS)

| Rank | Region | Country | Rate (`cm/100d`) | Max LOS (`cm`) | `p2` (`cm`) | Valid Frac | Confidence |
| ---: | :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| 1 | Semarang | Indonesia | -11.2 | -12.1 | -6.8 | 0.510 | high (`reliable`) |
| 2 | Konya Plain | Türkiye | -8.9 | -9.6 | — | — | medium (`reliable`) |
| 3 | Mashhad | Iran | -7.2 | -8.6 | -6.68 | 0.705 | medium (`reliable`) |
| 4 | Central Valley | United States | -7.2 | -7.8 | -5.8 | 0.629 | medium (`reliable`) |
| 5 | Eloy | United States | -6.7 | -8.0 | -4.3 | 0.696 | high (`reliable`) |
| 6 | Jakarta | Indonesia | -6.3 | -6.8 | -10.2 | 0.029 | low (`indicative`) |
| 7 | Bangkok | Thailand | -6.2 | -7.5 | -6.9 | 0.303 | medium (`reliable`) |
| 8 | Mexico City | Mexico | -5.8 | -7.0 | -5.7 | 0.639 | medium (`reliable`) |
| 9 | Karapınar | Türkiye | -5.5 | -5.9 | -4.2 | 0.142 | low (`indicative`) |
| 10 | Rafsanjan | Iran | -4.8 | -5.8 | -4.3 | 0.847 | medium (`reliable`) |

## Key Methodological Notes

- **Mexico City off-basin re-referencing:** Re-referencing from the northern lakebed margin (`-99.0126E, 19.5872N`, `-4.4 cm`) to stable volcanic bedrock on the SW margin (`-99.1840E, 19.3767N`) increased the measured LOS peak to **`-7.0 cm`** (`2.6 cm` difference), confirming that the original reference window was itself subsiding.
- **Indicative delta/wetland cities:** `jakarta` (`0.029`), `hanoi` (`0.257`), and `yunlin` (`0.282`) experience heavy agricultural/wetland decorrelation in L-band summer pairs; `ho_chi_minh` (`5.7 cm`), `tehran` (`3.8 cm` / `0.357`), and `hanoi` (`4.5 cm`) exhibit wide reference-window sensitivity and are flagged `indicative` for multi-reference/PS follow-up.
