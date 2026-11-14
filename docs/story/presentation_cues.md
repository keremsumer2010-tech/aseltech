# Lincoln Live Presentation Cue Sheet (3:00 Total)

> **Target Rehearsal:** `17:30 TR` (Push deadline `< 17:00 TR`)  
> **Live Web App URL:** https://keremsumer2010-tech.github.io/aseltech/  
> **Mandatory Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## Team Roles

| Role | Person | Responsibility During Live Pitch & Q&A |
|---|---|---|
| **Lead Speaker** | **Kerem** | Delivers the 6 × 30-second plain-English narrative blocks (`0:00–3:00`) |
| **Live Demo Driver** | **Memir** | Drives `https://keremsumer2010-tech.github.io/aseltech/` clicks, sliders, and `< 2 s` tab fallbacks in sync with Kerem |
| **Technical Q&A Lead** | **Mehmet** | Answers jury questions on NISAR GUNW physics, ionosphere/DEM deramping, 10-station GNSS validation, dual-orbit Track 34/114 cross-checks, and 11-month decomposition |
| **Data/Sources Q&A Lead & Timekeeper** | **İbrahim** | Keeps `30 s` splits (`2:30` visual warning) and answers jury questions on UK Fens / London clay detection limits, Karapınar 29-sinkhole dataset & permutation tests, verified sources, NISAR calibration rules, and simulator policy scenarios |

---

## Six 30-Second Speaking & Demo Blocks (`0:00 – 3:00`)

### Block 1 (`0:00 – 0:30`) · Hook, Key Numbers & Central Valley Time-Lapse
- **Speaker:** **Kerem**
- **Exact Spoken Lines:**  
  "Beneath the farms that feed us, heavy groundwater pumping is causing the land itself to sink quietly by centimetres in a single summer. Using open L-band radar from the NASA–ISRO NISAR satellite across 108 summer days in 2026, we measured up to 7.8 centimetres of sinking in California's Central Valley across 240 square kilometres, checked it within a 1-centimetre median difference against 10 GPS stations, and flagged 81 tilting canal and road segments."
- **Live Site Action (Memir — `https://keremsumer2010-tech.github.io/aseltech/`):**  
  Start at top hero (`"The ground beneath our food is sinking."`, `#heroMap`), pause `4 seconds` on the four summary cards in `.stats` (`−7.8 cm` / `28 Jun – 14 Oct 2026`, `240 km²`, `1.0 cm`, `81/645`), then click down to `#watch` (*"108 days in seconds"* → `"The Central Valley, 28 June to 14 October 2026"`) so `#cvVideo` (`Figure 0`) plays cleanly muted in the background.

### Block 2 (`0:30 – 1:00`) · Cloud-Penetrating Radar & Honest Detection Limits
- **Speaker:** **Kerem**
- **Exact Spoken Lines:**  
  "At Holme Fen in eastern England, draining peat soil since 1851 has lowered the land nearly 4 metres to 2.75 metres below sea level, yet clouds hide the region from optical cameras for most of the year. NISAR's 24-centimetre radar sees straight through 98 percent cloud cover on 20 October 2026—and in London's clay belt, our 9-pair noise check honestly marks sub-centimetre soil shrink–swell as below the 3.6-centimetre single-season detection threshold."
- **Live Site Action (Memir):**  
  Scroll smoothly through `#story` Chapter 1 (`[data-step="intro"]`, *"A satellite radar that measures ground motion"*) into Chapter 2 (`[data-step="uk"]`, *"Seeing the Fens through cloud"*); drag `#compareRange` left-to-right across `#compare` (`#ukOptical` VIIRS vs. `#ukRadar` NISAR GCOV preview, `Figure 1`), then hover briefly over `#holmeText` (`nearly 4 m` / `2.75 m below sea level`) and `#ukClay` (`±3.6 cm` detection limit, `status: "below_detection"`).

### Block 3 (`1:00 – 1:30`) · Central Valley Subsidence & 11-Month Rhythm
- **Speaker:** **Kerem**
- **Exact Spoken Lines:**  
  "Where NASA's NISAR StoryMap tracked the Central Valley subsidence bowl from airplanes in 2013 to 2017, we measured the same valley from space across 7 provisional NISAR pairs from 28 June to 14 October 2026, recording up to 7.8 centimetres of line-of-sight sinking—about 10.1 centimetres vertical—just 6 kilometres north of Terra Bella. Extending the chain across 11 months near Earlimart separates an 11.7-centimetre recoverable winter-to-summer bounce from 16.8 centimetres per year of permanent aquifer compaction."
- **Live Site Action (Memir):**  
  Scroll to Chapter 3 (`[data-step="cv"]`, *"Central Valley: up to −7.8 cm in 108 days"*), click `#cvPlay` next to `#slider` (`#dateLbl`) to step through all `8` dates (`28 Jun – 14 Oct 2026`), and click the `6 km N of Terra Bella` point (`p01`) on the map to update `#readout` and `#pointChart` (`Figure 2`).

### Block 4 (`1:30 – 2:00`) · GPS Validation, Dual-Orbit Cross-Check & Infrastructure Tilt
- **Speaker:** **Kerem**
- **Exact Spoken Lines:**  
  "Comparing our radar measurements against 10 continuous GPS stations gives a 0.924 cross-station correlation and a 1.00-centimetre median error, while independent ascending and descending NISAR orbits agree in sign across 85 percent of fast-sinking blocks. Overlaying 645 OpenStreetMap canals and roads flags 81 high-risk segments—led by the Tulare Irrigation District Canal at 57 millimetres per kilometre and 103 kilometres of the California Aqueduct at 49 millimetres per kilometre."
- **Live Site Action (Memir):**  
  Scroll to Chapter 4 (`[data-step="gnss"]`, *"Checking NISAR against GPS"*) and click station buttons in `#gnssTable` (`CAHA`, `P566`) to switch curves in `#gnssChart` (`Figure 3`); then scroll to Chapter 5 (`[data-step="risk"]`, *"Infrastructure on uneven ground"*) and hover along the top bars in `.riskbars` / `#riskList` (`Figure 4`).

### Block 5 (`2:00 – 2:30`) · Karapınar Sinkholes & Permanent Clay Compaction Physics
- **Speaker:** **Kerem**
- **Exact Spoken Lines:**  
  "In our home region of Karapınar in Konya, Türkiye, 8 provisional NISAR pairs measure up to 5.9 centimetres of summer sinking, and ground within 1 kilometre of 29 field-verified sinkholes sinks 6.4 times faster than the surrounding plateau at 4.15 centimetres versus 0.65 centimetres. Radar cannot predict the exact day a limestone roof collapses, but it maps where falling groundwater drains clay pores and permanently crushes storage capacity."
- **Live Site Action (Memir):**  
  Scroll to Chapter 6 (`[data-step="kp"]`, *"Karapınar, Konya: subsidence and sinkholes"*), pause on `#ringBox` / `#ringChart` (`4.2 cm` `< 1 km` vs. `0.6 cm` `> 5 km`, `p = 0.0001`) and `#sinkList` (`Figure 5`), then briefly show `#why` (*"Why part of the subsidence is permanent"*, `Figure 6`).

### Block 6 (`2:30 – 3:00`) · Interactive Simulator (`Valley Under Pressure`) & Scientific Close
- **Speaker:** **Kerem**
- **Exact Spoken Lines:**  
  "Finally, our Valley Under Pressure simulator—calibrated directly to NISAR's Terra Bella summer rate—lets farmers, students, and water managers test 24-month pumping policies and watch how over-pumping triggers irreversible clay compaction and canal capacity loss. All provisional NISAR processing code, 3D surfaces, and verified sources are open on GitHub—thank you, and we welcome your questions."
- **Live Site Action (Memir):**  
  At **`2:30`**, jump directly to `#play` (*"Simulator — Valley Under Pressure"*), click `#gamePlay` (`"Load simulator here"`) inside `#gameBox` (or `Ctrl+Tab` to pre-loaded Tab 3 `game/index.html` if iframe loading takes `> 1 s`), select **Terra Bella**, pull the pumping slider to **`150%` Over-Pump**, and finish on `#how` (*"Method & honesty — How we know"*, `.qlegend` `PROVISIONAL` badge).

---

## Top 5 Most Likely Jury Questions — Single-Sentence Answers (`judge_faq.md` & `data/*/summary.json`)

1. **Q1 · Calibration & Data Maturity (Assigned: İbrahim)**  
   *Question:* Which NISAR data maturity tier do your numbers use, and did your team perform the sensor calibration?  
   *1-Sentence Answer:* All quantitative subsidence and risk figures come strictly from post-17 June 2026 NISAR Level-2 `GUNW` **Provisional** products (`CRID P05023`) calibrated by NASA–JPL and ISRO rather than our team, while pre-calibration beta pairs are isolated in `data/central_valley_fullyear/` (`quality: "mixed"`) and UK Fens GCOV browse imagery is labeled `preview`.

2. **Q2 · Line-of-Sight vs. Vertical Motion & Dual-Orbit Check (Assigned: Mehmet)**  
   *Question:* NISAR measures along a tilted radar line of sight—how do you know the Valley is truly sinking downward rather than shifting horizontally?  
   *1-Sentence Answer:* We explicitly label `LOS / cos(θ)` as a vertical *estimate* (`−7.8 cm` LOS -> `−10.1 cm` vertical at `39.1°`) and confirm direction independently with ascending Track 34 plus descending Track 114 two-orbit inversion across `6,719` blocks (`85%` sign agreement), which measures `−7.2 cm` vertical sinking and only `−0.1 cm` east-west motion in the Alpaugh bowl.

3. **Q3 · Ionosphere, Troposphere & Error Budget (Assigned: Mehmet)**  
   *Question:* Atmospheric delays and unwrapping errors can mimic ground motion in single interferograms—how did you isolate real deformation?  
   *1-Sentence Answer:* We subtract each `GUNW` file's split-spectrum ionospheric phase screen (`ion`), remove a per-pair planar plus Copernicus DEM (`elevation_m`) topographic ramp over stable bedrock, and achieve a `0.66 cm` local noise floor (`SNR 2.7×–4.5×`), a `0.294 cm` median Cramér-Rao phase sigma, and a `1.00 cm` median RMSE (`r = 0.924` cross-station final fit) across 10 continuous GPS stations.

4. **Q4 · Predicting Sinkhole Collapses in Karapınar (Assigned: İbrahim)**  
   *Question:* Can NISAR tell local residents in Karapınar the exact day a karst sinkhole roof will collapse?  
   *1-Sentence Answer:* No—sudden roof collapse is a brittle failure inside limestone caverns, so NISAR instead maps the broad `−5.9 cm` LOS groundwater drawdown bowl and confirms statistically (`p = 0.0001` `1.04 km` block permutation, `p = 0.0207` `3,423` constellation shifts) that terrain within `1 km` of the 29 verified sinkholes sinks `6.4×` faster (`−4.15 cm` vs. `−0.65 cm` beyond `5 km`) without claiming collapse-date prediction.

5. **Q5 · 108-Day Summer Rate (`−26.4 cm/yr`) vs. Full-Year Multi-Season Reality (Assigned: Mehmet)**  
   *Question:* Why is your linearized Central Valley rate (`−26.4 cm/yr` LOS / `−34.1 cm/yr` vertical) higher than many multi-year Valley averages?  
   *1-Sentence Answer:* Because `28 June – 14 October 2026` isolates peak summer irrigation when downward elastic drawdown and permanent compaction add in phase, extending our stack to 25 pairs across 11 months near Earlimart (`R² = 0.97`) separates `11.7 cm` of recoverable winter-summer bounce from `−16.8 cm/yr` of permanent compaction, bringing the long-term rate in line with multi-year San Joaquin literature.
