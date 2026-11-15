# NISAR Pulse — Printable Jury Q&A Cards & 3-Minute Timed Rehearsal (`docs/story/qa_cards.md`)

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Twelve Most Likely Jury Questions (2-Sentence Answers)

**Q1. Are these NISAR measurements fully calibrated science products?**  
No — all core interferograms carry `provisional` status (`CRID P05023`, `>= 2026-06-17`), and calibration/validation are performed by NASA-JPL and ISRO, not by our team. We isolate pre-calibration `beta` granules (`< 2026-06-17`) strictly in `mixed` full-year folders and report every uncertainty floor transparently.

**Q2. How do you know the −7.8 cm Central Valley signal is not atmospheric noise?**  
Across 10 continuous Nevada Geodetic Laboratory GNSS stations projected into radar LOS, our provisional NISAR chain achieves `r = 0.924` with `1.00 cm` median RMSE (`0.76 cm` on active sites `> 2 cm`). Furthermore, our 9-pair London Clay negative control establishes a `3σ = 3.62 cm` seasonal noise floor, placing the `−7.8 cm` Central Valley peak more than twice above the `3σ` floor.

**Q3. Why does Konya Plain rank #1 (`−11.0 cm/100d`) even though it only has `11.6%` valid pixels?**  
All 29 atlas regions are ranked on the shared 93-day summer window (`2026-06-28 → 2026-09-29`) using 1 km block medians (`p2` filtered) so differing observation spans do not bias the leaderboard. We retain Konya Plain with an explicit `11.6%` coverage caution and `medium` confidence rather than hiding sparse agricultural coherence, and independent Path 172 confirms the `−9.6 cm` 108-day bowl.

**Q4. Tell us about a mistake you caught in your own pipeline.**  
Automated time-series QC (`tools/atlas_qc.py`) flagged a single-step `12.1 cm` half-wavelength unwrapping jump in Semarang at epoch `10–11` (`2026-09-29 → 2026-10-11`). After re-processing without the jump, Semarang's peak moved to the northern coast at `−6.2 cm` LOS (`#7` reliable), and `6` other flagged regions remain segregated as `indicative only`.

**Q5. Why did Central Valley stay `medium` confidence even though its reference spread is `5.34 cm`?**  
By explicit rule in `data/global/independent_validation.json`, any basin with independent GNSS correlation `r >= 0.80` retains `medium` confidence when the reference spread reflects real basin-wide deformation gradients rather than noise. Central Valley's 10-station GNSS check (`r = 0.924`) easily clears that threshold.

**Q6. What is the difference between LOS and vertical subsidence?**  
InSAR measures 1D motion along the radar line of sight (`~36°–44°` incidence), not pure vertical sinking. Single-orbit `LOS / cos θ` conversions are labeled **estimates** assuming negligible horizontal motion, which we verified using dual-orbit Track 34/114 decomposition at Alpaugh (`−7.2 cm` vertical vs. `−0.1 cm` E–W).

**Q7. How do you separate permanent aquifer damage from seasonal rebound?**  
Over 25 pairs (`324` days, `2025-11-24 → 2026-10-14`, `mixed` beta+provisional), a linear + annual-sinusoid fit at Earlimart (`p01`) yields `−16.8 ± 2.2 cm/yr` permanent compaction alongside `11.7 cm` peak-to-peak seasonal oscillation (`R² = 0.97`). Integrating the permanent slope across `4,508.29 km²` gives `0.3174 km³/yr` (`317.41 million m³/yr`) of lost aquifer storage.

**Q8. Why does canal tilt (`mm/km`) matter more than maximum depth?**  
Gravity-fed irrigation canals and rail lines fail when differential settling tilts the bed slope, not when an entire plain drops uniformly. We find `81 / 645` segments exceeding `20 mm/km` (peaking at `57.01 mm/km` on the Tulare Irrigation District Canal), and the top-10 list is `100%` rank-invariant under `±25%` threshold shifts.

**Q9. Can NISAR predict when a Karapınar sinkhole will collapse?**  
No — regional L-band interferometry cannot predict exact collapse dates or locations of individual limestone sinkholes. However, `1.04 km` block permutations (`p = 0.0001`) and `3,423` rigid constellation shifts (`p = 0.0207`) show `6.4×` faster sinking (`−4.15 cm` vs. `−0.65 cm`) within `1 km` of 29 mapped sinkholes, helping prioritize field monitoring.

**Q10. Why did NISAR beat Sentinel-1/OPERA in Central Valley (`r = 0.399`) and Eloy (`r = 0.091`)?**  
NISAR's 24.2 cm L-band wavelength penetrates irrigated crops and preserves `80.4%` valid coherence in summer Tulare farmland where C-band (`5.55 cm`) decorrelates, while in urban Mexico City (`r = 0.912`) both sensors agree closely. Additionally, public `OPERA_L3_DISP-S1_V1` coverage ends at `2026-04-26`, before the June–October 2026 NISAR window.

**Q11. How many people live on sinking ground in your global atlas?**  
Intersecting `GHSL GHS-POP E2025` (`100 m`) with 108-day scaled subsidence `< −5 cm` (`|disp| >= 2σ`, excluding nested `karapinar` to avoid double-counting) places **`1,200,716` residents** on **`511.65 km²`** of sinking ground (`7,475,011` below `−2 cm`) across all 29 atlas regions.

**Q12. How did you use AI, and are any images AI-generated?**  
AI assistants (Anthropic Claude and Google Gemini) helped draft analysis scripts, tests, and documentation, with every number read directly from repository JSONs and checked by Team Taykut. There are **zero AI-generated images** anywhere on the website, presentation deck, 3D viewer, or simulator.

---

## 2. 3-Minute Timed Rehearsal Plan (`web/present.html`, 6 Stops)

| Time | Stop (`present.html`) | Speaker / Action | Target Key Cue |
|---|---|---|---|
| `0:00–0:30` | **Stop 1: Home Summary** | Kerem opens; `ArrowRight` → Stop 1 | `−7.8 cm` LOS in 108 d, `0.3174 km³/yr` permanent storage loss |
| `0:30–1:00` | **Stop 2: 29-Region Atlas** | Kerem; `ArrowRight` → Stop 2 | `29` regions (`16` reliable / `13` indicative), common 93-day window |
| `1:00–1:30` | **Stop 3: Konya Plain & Karapınar** | Kerem; `ArrowRight` → Stop 3 | `#1 Konya Plain −11.0 cm/100d` (`11.6%` cov. caution), Karapınar `6.4×` |
| `1:30–2:00` | **Stop 4: Self-Caught QC** | Kerem; `ArrowRight` → Stop 4 | Semarang `12.1 cm` jump caught & fixed (`−6.2 cm` `#7`), `6` flagged isolated |
| `2:00–2:30` | **Stop 5: Results & GNSS** | Kerem; `ArrowRight` → Stop 5 | `10` GNSS `r = 0.924` (`1.00 cm` RMSE), `81/645` tilt, London `3.62 cm` floor |
| `2:30–3:00` | **Stop 6: Simulator & Close** | Mehmet cues `2:30`; `ArrowRight` → Stop 6 | `Valley Under Pressure` (`game/index.html?basin=konya`), mandatory provisional notice |
