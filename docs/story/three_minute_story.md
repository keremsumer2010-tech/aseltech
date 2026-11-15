# Three-Minute Story Spec (`docs/story/three_minute_story.md`)

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

Extracted from the live 3-minute jury path in [`web/index.html`](../../web/index.html) (`web/home3.js`, `data/global/home_summary.json`) and synchronized with [`web/present.html`](../../web/present.html), [`docs/story/slides.html`](slides.html), and [`docs/story/presentation_cues.md`](presentation_cues.md).

## One-Sentence Core (Verbatim Everywhere)

> **We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: 29 basins measured with one open pipeline on the same 93 days, every number traceable to its file, and every headline checked against GPS, NASA's OPERA product and the literature.**

---

## Section 1 — Hero (`0:00–0:20`)

- **Heading (7 words):** `Where the ground is sinking: 29 basins`
- **Sentence (23 words):** `One open pipeline turns first NASA-ISRO NISAR radar data into centimetres of sinking across 29 basins over 93 days, checked against GPS.`
- **Big numbers:**
  - **`29` basins** (`16 reliable, 13 indicative`) · `provisional` · `data/global/home_summary.json:kpis[0]` / `data/global/atlas.json`
  - **`1.48 M` people** (`1,479,844` on `> 5 cm` sinking ground, `549.45 km²`) · `provisional` · `data/global/home_summary.json:kpis[1]` / `data/global/vital_signs.json`
  - **`r = 0.92` GPS** (`0.924`, 10 Central Valley stations) · `provisional` · `data/global/home_summary.json:kpis[2]` / `docs/story/validation_report.md`
  - **`0.32 km³/yr`** (`0.3174 km³/yr` permanent storage lost, Central Valley) · `mixed` · `data/global/home_summary.json:kpis[4]` / `data/central_valley_fullyear/storage_loss.json`
  - **`5` flagged basins** (shown as indicative) · `provisional` · `data/global/home_summary.json:qc_story.flagged`
- **Visual:** `docs/story/media/pc1_atlas_world.png` (world map of 29 measured basins: filled circles reliable, rings indicative) + `#top5` table (`web/index.html`).
- **Link:** `Open the interactive atlas →` (`atlas.html`) / `Try the simulator` (`game/`)

---

## Section 2 — 1 · The Atlas (`0:20–1:00`)

- **Heading (7 words):** `A global subsidence atlas on one ruler`
- **Sentence (24 words):** `Same radar, same code, same 93 days (28 Jun–29 Sep 2026) for 29 basins; values show motion toward or away from the satellite.`
- **Big numbers:**
  - **`#1` Konya Plain: `−11.0 cm/100d`** (common 93-day LOS rate; `medium` confidence, valid-pixel fraction not recorded, kept with caution) · `provisional` · `data/global/home_summary.json:top5[0].rate_cm_per_100d_common`
  - **`#2` Eloy: `−8.6 cm/100d`** (`high` confidence) · **`#3` Central Valley: `−7.3 cm/100d`** (`medium` confidence) · `provisional` · `data/global/home_summary.json:top5[1..2]`
- **Visual:** `docs/story/media/pc2_konya_plain.png` (Konya Closed Basin map, 26 Jun–12 Oct 2026, −9.6 cm peak) + `docs/story/media/pc1_atlas_world.png`.
- **Link:** `Open the atlas →` (`atlas.html`)

---

## Section 3 — 2 · Our Own Error, Caught (`1:00–1:30`)

- **Heading (7 words):** `A check that catches our own errors`
- **Sentence (24 words):** `Automated time-series checks flagged 12.1 cm full L-band phase-cycle jumps; Semarang dropped from −12.1 to −6.2 cm, and 5 basins stay indicative.`
- **Big numbers:**
  - **`−12.1 → −6.2 cm` LOS** (`Semarang` fixed after removing `11.2 cm` jump at last date; `#7` reliable) · `provisional` · `data/global/home_summary.json:qc_story.semarang`
  - **`5` indicative basins** (`bangkok, beijing, delhi, gorgan, pekalongan`); **Tehran** fixed `−3.5 → −7.4 cm` (off-basin reference) · `provisional` · `data/global/home_summary.json:qc_story` / `data/global/qc_flags.json`
- **Visual:** `#qcChart` SVG (`web/index.html`, `web/home3.js`) comparing Semarang old inland point (`−12.1 cm`) vs. re-processed north coast (`−6.2 cm`).
- **Link:** `See how the check works →` (`science.html`)

---

## Section 4 — 3 · Why You Can Trust It (`1:30–2:05`)

- **Heading (6 words):** `Proof on the ground and uncertainty`
- **Sentence (24 words):** `Provisional NISAR motion tracks 10 Central Valley GPS stations (r = 0.92), beats 0.3 cm noise, and matches Mexico City OPERA patterns (r = 0.91).`
- **Big numbers:**
  - **`r = 0.92` GPS** (`0.924`, `RMSE 1.37 cm` final, 10 Central Valley stations — primary validation) · `provisional` · `data/global/home_summary.json:kpis[2]` / `data/central_valley/validation.json`
  - **`≈ 0.3 cm` formal noise** (`0.294 cm` median); `29/29` literature checks · `provisional` · `data/central_valley/summary.json`
  - **OPERA pattern check (secondary, seasonal caveat):** *Over Mexico City the spatial pattern matches NASA JPL's OPERA product at 10 points (r = 0.91), although OPERA covers winter (2025-12-25 to 2026-03-25) and NISAR summer (2026-06-22 to 2026-10-20); in the Central Valley and at Eloy the agreement is weak (r = 0.40 and 0.09) because seasons and viewing geometry differ.* · `provisional` · `data/global/opera_check.json`
- **Visual:** `docs/story/media/validation_scatter.png` (`NISAR vs GPS, Central Valley, 28 Jun – 14 Oct 2026`).
- **Link:** `See all checks in Science →` (`science.html`)

---

## Section 5 — 4 · What It Is For (`2:05–2:40`)

- **Heading (7 words):** `From a radar measurement to a decision`
- **Sentence (22 words):** `We turn sinking into 1.48 M exposed people, 0.32 km³/yr lost storage, 81/645 tilting corridors, 29 bulletins, and a 30-second simulator.`
- **Big numbers:**
  - **`1.48 M` people** (`1,479,844` on `> 5 cm` sinking ground, `549.45 km²`) · `provisional` · `data/global/exposure_atlas.json` / `data/global/vital_signs.json`
  - **`0.32 km³/yr`** (`0.3174 km³/yr` permanent Central Valley storage lost) · `mixed` · `data/central_valley_fullyear/storage_loss.json`
  - **`81 / 645` sections `> 20 mm/km`** (corridors with tilt/damage probability) · `provisional` · `data/central_valley/assets.json`
- **Visual:** `web/assets/simulator.jpg` (simulator capture) + `docs/story/media/pc9_fullyear_point.png` + `docs/story/media/pc7_risk_prob.png`.
- **Link:** `Play the simulator →` (`game/`) / `Open the Konya Plain bulletin →` (`docs/bulletins/konya_plain.html`)

---

## Section 6 — 5 · What Is New & Open (`2:40–3:00`)

- **Heading (6 words):** `Open engine and four original contributions`
- **Sentence (24 words):** `We built a comparable 29-basin atlas, self-checking QC ranking, decision-ready storage and tilt metrics, and an open one-command pipeline on public NASA data.`
- **Big numbers:**
  - **`4` original contributions** (`comparable 29-basin atlas`, `self-checking QC`, `decision metrics`, `open one-command engine`) · `open source` · `README.md`
  - **`1` open command** (`python -m pipeline.nisarpulse run ...` + `python pipeline/pc10/build_atlas.py`) · `open source` · `docs/story/engine.md`
- **Visual:** One-command reproduction block (`web/index.html#w9`) + 4 contribution summary.
- **Link:** `Get the code and data →` (`data.html`) / `GitHub` (`https://github.com/keremsumer2010-tech/aseltech`)
