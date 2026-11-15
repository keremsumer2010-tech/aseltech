# Three-Minute Story Spec (`docs/story/three_minute_story.md`)

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

Extracted directly from the live 3-minute jury path in [`web/index.html`](../../web/index.html) (`web/home3.js`, `data/global/home_summary.json`) and synchronized with [`web/present.html`](../../web/present.html) and [`docs/story/presentation_cues.md`](presentation_cues.md).

## One-Sentence Core (Verbatim Everywhere)

> **We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: 29 basins measured with one open pipeline on the same 93 days, every number traceable to its file, and every headline checked against GPS, NASA's OPERA product and the literature.**

---

## Section 1 — Hero (`0:00–0:20`)

- **Heading:** `We turned NISAR's first radar data into a self-checking subsidence atlas.`
- **Sentence (25 words):** `29 basins, one open pipeline, the same 93 days for all; every number traces to its file, checked against GPS, OPERA and the literature.`
- **Big numbers:**
  - **`29` basins** (`16 reliable, 13 indicative`) · `provisional` · `data/global/home_summary.json` / `atlas.json`
  - **`1.20 M` people** (`1,200,716` on `< −5 cm` ground) · `provisional` · `data/global/vital_signs.json:people_on_sinking_ground`
  - **`r = 0.92` GPS** (`0.924`, Central Valley) · `r = 0.91` OPERA (`0.912`, Mexico City) · **`0.32 km³/yr`** storage lost (`0.3174 km³/yr`, `mixed`)
- **Visual:** Central Valley displacement loop (`docs/story/media/hero_poster.webp` / `#heroVideo`).
- **Link:** `See it in 3 minutes` (`#kpis`) / `Open the atlas` (`atlas.html`)

---

## Section 2 — 1 · The Atlas (`0:20–1:00`)

- **Heading (8 words):** `Where the ground sank fastest in 2026`
- **Sentence (24 words):** `Same radar, same code, same 93 days (28 Jun – 29 Sep 2026) for every basin; values show motion toward or away from the satellite.`
- **Big numbers:**
  - **`#1` Konya Plain: `−11.0 cm/100d`** (common 93-day LOS rate; `11.6%` valid-pixel caution) · `provisional` · `data/global/atlas.json:regions[0].rate_cm_per_100d_common`
  - **`#2` Eloy: `−8.6 cm/100d`** · **`#3` Central Valley: `−7.3 cm/100d`** · `provisional` · `data/global/atlas.json:regions[1..2]`
- **Visual:** `docs/story/media/pc1_atlas_world.png` (world map of 29 measured basins: filled circles reliable, rings indicative) + `#top5` table.
- **Link:** `Open the interactive atlas →` (`atlas.html`)

---

## Section 3 — 2 · Our Own Error, Caught (`1:00–1:30`)

- **Heading (4 words):** `The atlas checks itself`
- **Sentence (24 words):** `Semarang dropped −12.1 cm in one 11.2 cm L-band half-cycle step; re-processed it moved to −6.2 cm, and 5 flagged basins stay indicative only.`
- **Big numbers:**
  - **`−12.1 → −6.2 cm` LOS** (`Semarang` fixed after removing `11.2 cm` step at last date; `#7` reliable) · `provisional` · `data/global/atlas_changelog.json`
  - **`5` indicative basins** (`Bangkok, Beijing, Delhi, Gorgan, Pekalongan`); **Tehran** fixed `−3.5 → −7.4 cm` (off-basin ref) · `provisional` · `data/global/qc_flags.json`
- **Visual:** `#qcChart` SVG comparing old inland uplands (`−12.1 cm`) vs. re-processed subsiding north coast (`−6.2 cm`).
- **Link:** `How the check works →` (`science.html`)

---

## Section 4 — 3 · Why You Can Trust It (`1:30–2:05`)

- **Heading (7 words):** `Checked against the ground and against NASA`
- **Sentence (23 words):** `Provisional NISAR motion tracks 10 GPS stations, matches NASA JPL's OPERA product in Mexico City, and beats ≈ 0.3 cm formal phase noise.`
- **Big numbers:**
  - **`r = 0.92` GPS** (`RMSE 1.37 cm` final, `1.00 cm` median, 10 Central Valley stations) · `provisional` · `data/central_valley/validation.json`
  - **`r = 0.91` OPERA** (`0.912` Mexico City, same summer season one year earlier) · `provisional` · `data/global/mexico_city/summary.json` / `docs/story/opera_check.md`
  - **`≈ 0.3 cm` formal noise** (`0.294 cm` median); `26/29` uncertainty maps + `29/29` literature checks · `provisional` · `data/central_valley/summary.json`
- **Visual:** `docs/story/media/validation_scatter.png` (`NISAR vs GPS, Central Valley, 28 Jun – 14 Oct 2026`).
- **Link:** `See all checks in Science →` (`science.html`)

---

## Section 5 — 4 · What It Is For (`2:05–2:40`)

- **Heading (7 words):** `From a radar measurement to a decision`
- **Sentence (24 words):** `We turn sinking into 1.20 M exposed people, 0.32 km³/yr lost storage, 81/645 tilting corridors, 29 basin bulletins, and a 30-second simulator.`
- **Big numbers:**
  - **`1.20 M` people** (`1,200,716` on `< −5 cm` ground) · `provisional` · `data/global/exposure_atlas.json`
  - **`0.32 km³/yr`** (`0.3174 km³/yr` permanent Central Valley storage lost) · `mixed` · `data/central_valley_fullyear/storage_loss.json`
  - **`81 / 645` segments `> 20 mm/km`** (plus damage probability per corridor) · `provisional` · `data/central_valley/assets.json`
- **Visual:** `web/assets/simulator.jpg` (real simulator capture) + 5 impact cards.
- **Link:** `open the simulator →` (`game/`)

---

## Section 6 — 5 · What Is New (`2:40–3:00`)

- **Heading (6 words):** `What we built that did not exist`
- **Sentence (24 words):** `A comparable 29-basin NISAR atlas, self-checking QC ranking, decision-ready storage and tilt numbers, and an open one-command engine on public NASA data.`
- **Big numbers:**
  - **`4` original contributions** (`comparable atlas`, `self-checking ranking`, `decision numbers`, `open & reproducible`) · `open source` · `README.md`
  - **`1` open command** (`NISAR Pulse` engine reproduces any region from public ASF data) · `open source` · `docs/story/engine.md`
- **Visual:** 4 original contribution cards + one-command reproduction block.
- **Link:** `Reproduce from GitHub →` (`https://github.com/keremsumer2010-tech/aseltech`)
