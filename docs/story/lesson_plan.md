# Educator Lesson Plan (40 Minutes): Tracking Sinking Farms & Infrastructure From Space with NISAR

> **Challenge Alignment (`A5` & `16:25` ARSET / Intro to SAR Integration):** Ready-to-run 40-minute high-school laboratory (`Grades 9–12` / Earth Science, Physics, Environmental Science, Geography). Uses measured NASA–ISRO NISAR data and the browser-based **Valley Under Pressure** simulator (`web/index.html` & `game/index.html`).  
> **Mandatory Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## Learning Objectives
By the end of this 40-minute lesson, students will be able to:
1. Explain why active **`24 cm` L-band Synthetic Aperture Radar (SAR)** maps the Earth's surface through thick clouds where passive optical cameras fail ([NASA Intro to SAR](https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar)).
2. Interpret interferometric radar line-of-sight (`LOS`) displacement (`Δr_LOS = −(λ / 4π) Δφ`, estimated vertical `≈ LOS / cos θ`) and evaluate satellite accuracy against continuous GPS stations (`r = 0.924`, `1.00 cm` median RMSE).
3. Distinguish **recoverable seasonal ground motion** (`11.7 cm` peak-to-peak near Earlimart) from **irreversible permanent clay compaction** (`−16.8 cm/yr`) when over-pumping drops groundwater head below the preconsolidation threshold.
4. Run controlled 24-month water-management experiments in **Valley Under Pressure** (`game/index.html`) to weigh short-term agricultural output against permanent aquifer loss, canal tilt, and Karapınar sinkhole hazards.

**Materials Required:** Classroom projector or student browsers opened to `https://keremsumer2010-tech.github.io/aseltech/` (or local `python3 -m http.server 8000` mirror), `game/index.html`, and [`docs/story/slides.html`](slides.html) (offline backup).

---

## 40-Minute Lesson Schedule

| Time | Activity & Live Browser Location | Teacher Actions & Student Tasks |
|---|---|---|
| **00–08 min** | **Part 1 · Hook & Cloud-Penetrating Radar** (`web/index.html` Chapter 2 `[data-step="uk"]`) | Show the `1851` **Holme Fen** iron post (`nearly 4 m` exposed, `2.75 m` below sea level in drained English peat). Have students drag the `#compareRange` slider on **`20 October 2026`**: optical VIIRS shows ~`98%` solid cloud while same-day NISAR L-band GCOV radar reveals The Wash coastline and Fens fields underneath. Note London clay (`±3.6 cm` noise floor -> honestly reported as `below_detection`). |
| **08–20 min** | **Part 2 · Guided Satellite Investigation** (`Chapter 3` `[data-step="cv"]`, `Chapter 4`, `Chapter 6`) | Play `#cvPlay` (`28 Jun – 14 Oct 2026`, `108` summer days) and inspect `6 km N of Terra Bella` (`−7.8 cm` LOS, `~−10.1 cm` vertical *estimate*; `239.54 km²` sinking `> 5 cm`). Check GPS agreement at station **`CAHA`** (`r = 0.90`; valley median `1.00 cm` RMSE), observe canal slopes (`Tulare Irrigation District Canal` `57.01 mm/km`; `California Aqueduct` `49.12 mm/km`), and inspect **Karapınar, Türkiye** (`−5.9 cm` LOS; `−4.15 cm` within `1 km` of `29` verified sinkholes vs. `−0.65 cm` beyond `5 km`). |
| **20–32 min** | **Part 3 · Hands-On Lab: *Valley Under Pressure*** (`#play` / `game/index.html`) | Working in pairs on **Terra Bella**, students run two 24-month simulations and log numbers:<br>• **Trial A (Unrestricted Over-Pumping / `2. Multi-Year Drought` Classroom preset):** Record final depth (`cm`), permanent clay compaction (`cm`), and canal tilt warnings.<br>• **Trial B (Sustainable Groundwater Management / SGMA Balance):** Adjust pumping downward until aquifer head stays above the preconsolidation threshold and compare total storage saved. |
| **32–40 min** | **Part 4 · Discussion & 5-Question Assessment** | Students answer the 5 check-for-understanding questions below (5 min writing, 3 min class debrief using the answer key). |

---

## Five Student Assessment Questions

1. **Active Radar vs. Passive Optical:** On `20 October 2026`, the optical VIIRS satellite image over eastern England showed solid white cloud cover, yet the NISAR radar image captured on the same day clearly mapped rivers, fields, and The Wash coastline. Explain the physical difference between optical sunlight reflection and `24 cm` L-band radar sensing that makes this possible.
2. **Reading Radar Line-of-Sight (`LOS`) Geometry:** Near Terra Bella, California, NISAR's radar beam points downward at a `39.1°` angle from vertical and measured `−7.8 cm` of displacement along that line of sight over `108` summer days (`cos 39.1° ≈ 0.776`). Calculate the estimated purely vertical sinking in centimetres, and explain why comparing ascending and descending orbits helps verify that the motion is vertical rather than sideways.
3. **Seasonal Bounce vs. Permanent Aquifer Loss:** Our experimental 11-month NISAR time series near Earlimart (`24 Nov 2025 – 14 Oct 2026`, `324 days`, `mixed` quality) recorded `+2.1 cm` winter lift followed by summer drawdown to `−20.3 cm` LOS. Using what you observed in **Valley Under Pressure**, explain why winter rain restores part of the land height (`11.7 cm` seasonal swing) while `−16.8 cm/yr` cannot recover once underground clay beds crush.
4. **Why Tilt (`mm/km`) Matters More Than Total Depth for Canals:** Suppose an entire 50 km concrete irrigation canal sank evenly by `5.0 cm` from start to finish versus another canal that sank `5.0 cm` at kilometer `20` and `0 cm` everywhere else. Using the **California Aqueduct** (`49.12 mm/km`) and **Tulare Irrigation District Canal** (`57.01 mm/km`), explain which scenario disrupts gravity water flow and why.
5. **Scientific Honesty & Sinkhole Limits in Karapınar:** NISAR shows that farmland within `1 km` of `29` verified Karapınar sinkholes sank `−4.15 cm` over `108` days compared with `−0.65 cm` more than `5 km` away (`p = 0.0001`). Based on this satellite finding, can an engineer tell farmers the exact date a new limestone sinkhole roof will collapse? Why or why not?

---

## Answer Key (For Educators)

1. **Answer 1:** Passive optical sensors like VIIRS rely on reflected sunlight in visible wavelengths (`~0.4–0.7 µm`), which are scattered and blocked by water droplets in clouds. Active L-band Synthetic Aperture Radar (`24 cm` wavelength) transmits its own long microwave pulses that penetrate right through cloud droplets and forest canopies day or night, measuring ground backscatter (`GCOV`) and phase change (`GUNW`).
2. **Answer 2:** Dividing line-of-sight displacement by `cos 39.1°` gives `−7.8 cm / 0.776 ≈ −10.1 cm` of estimated vertical sinking (`summary.json` reports `−10.1 cm`). Because single-orbit radar combines vertical and east-west motion into one slant direction, comparing opposite viewing directions (ascending Track 34 plus descending Track 114 across `6,719` blocks, `r = 0.489`, `85%` sign agreement) separates vertical from east-west motion and confirms the Alpaugh bowl sank `−7.2 cm` vertically with only `−0.1 cm` east-west displacement.
3. **Answer 3:** Sand and gravel aquifers deform **elastically**: when winter recharge refills pore water pressure, those coarse layers rebound slightly (`+2.1 cm` winter rise; `11.7 cm` peak-to-peak seasonal swing near Earlimart). However, once pumping pulls hydraulic head below the historical minimum (preconsolidation head *h<sub>pc</sub>*), fine clay platelets realign permanently (**inelastic compaction**, `−16.8 cm/yr` / `−14.9 cm` over 324 days), permanently destroying water-storage pore space.
4. **Answer 4:** Uniform sinking keeps the canal's downward water slope intact, so water still flows by gravity. **Differential subsidence** (measured in `mm/km` tilt, such as `57.01 mm/km` on the Tulare Canal or `49.12 mm/km` along the California Aqueduct) creates local sags or reverse gradients that pool water, crack concrete linings, reduce freeboard, and slash flow capacity (similar to the historic `60%` capacity drop on the Friant-Kern Canal).
5. **Answer 5:** No—sudden sinkhole collapse is a rapid, brittle mechanical failure of an underground limestone cavity roof that occurs between or within narrow footprints rather than giving a reliable day-ahead radar countdown signal. What NISAR honestly provides is regional **susceptibility and shared groundwater-drawdown mapping** (`6.4×` faster subsidence inside `1 km` of known sinkholes), helping planners prioritize field geophysical surveys and highway tilt checks (such as Highway `42-42` at `19.74 mm/km`) without overclaiming collapse-date prediction.

---

## Further Learning Resources (`16:25 KAYNAKLAR`)
- **What is Synthetic Aperture Radar (Intro to SAR) — NASA Earthdata:** https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/sar
- **Earth Observation Data Basics (Intro to Remote Sensing) — NASA Earthdata:** https://www.earthdata.nasa.gov/learn/earth-observation-data-basics
- **NASA ARSET — Applied Remote Sensing Training (Free SAR & Water Courses):** https://appliedsciences.nasa.gov/get-involved/training
- **NASA NISAR ArcGIS StoryMap — Land Subsidence:** https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828
- **NASA JPL UAVSAR Educational Postcards:** https://uavsar.jpl.nasa.gov/education/postcards.html
- **Canadian Space Agency (CSA) — SAR Python & QGIS Tutorial:** https://github.com/asc-csa/Synthetic_Aperture_Radar_Tutorial
