# Three-Minute Story Spec (`docs/story/three_minute_story.md`)

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

## One-Sentence Core (Verbatim Everywhere)

> **We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: 29 basins measured with one open pipeline on the same 93 days, every number traceable to its file, and every headline checked against GPS, NASA's OPERA product and the literature.**

---

## Section 1 — Hero (`0:00–0:20`)

- **Heading (5 words):** `A self-checking global subsidence atlas`
- **Sentence (24 words):** `Using provisional NASA-ISRO NISAR radar, we measure centimeter-scale ground sinking along the satellite's line of sight across 29 basins on the same 93 days.`
- **Big numbers:**
  - **`29` basins** (`16` reliable, `13` indicative) · `provisional` · `data/global/atlas.json:n_regions`
  - **`1.48 million` residents** (`1,479,844` on `< −5 cm` sinking ground) · `provisional` · `data/global/vital_signs.json:people_on_sinking_ground`
  - **`r = 0.92` GPS** (`0.924`, `1.00 cm` median RMSE, 10 stations) · `provisional` · `data/central_valley/validation.json` / `docs/story/validation_report.md`
- **Visual:** `3D Earth subsidence globe` (`web/assets/earth_day_3600.jpg` / `web3d/`) or Central Valley displacement hero map.
- **Link:** `Explore the atlas →` (`atlas.html`)

---

## Section 2 — Atlas (`0:20–1:00`)

- **Heading (6 words):** `Twenty-nine basins ranked on 93 days`
- **Sentence (23 words):** `One open pipeline measures every basin over the shared 28 June–29 September 2026 window, placing Konya Plain first with an explicit coverage caution.`
- **Big numbers:**
  - **`#1` Konya Plain: `−11.0 cm/100d`** (common 93-day LOS rate; `−9.6 cm` in 108 d, `11.6%` valid-pixel caution) · `provisional` · `data/global/atlas.json:regions[0].rate_cm_per_100d_common`
  - **`#2` Eloy: `−8.6 cm/100d`** · **`#3` Central Valley: `−7.3 cm/100d`** · `provisional` · `data/global/atlas.json:regions[1..2]`
- **Visual:** Small interactive globe preview + Top-5 reliable table (common 93-day window) + Konya Plain panel with `11.6%` caution badge.
- **Link:** `Open the 29-region atlas →` (`atlas.html#konya_plain`)

---

## Section 3 — We Caught Our Own Error (`1:00–1:30`)

- **Heading (6 words):** `Self-checking quality control caught our error`
- **Sentence (24 words):** `Automated time-series checks flagged a 12.1 cm radar phase jump in Semarang; re-processing corrected it to −6.2 cm and isolated flagged basins.`
- **Big numbers:**
  - **`−12.1 → −6.2 cm` LOS** (`Semarang` corrected to `#7` reliable after removing epoch `10–11` half-cycle jump) · `provisional` · `data/global/atlas_changelog.json` / `data/global/semarang/summary.json`
  - **`5` QC-flagged basins** (`Gorgan`, `Delhi`, `Pekalongan`, `Beijing`, `Bangkok` moved to `indicative only`; plus Tehran `−3.5 → −7.4 cm` off-basin ref fix) · `provisional` · `data/global/qc_flags.json`
- **Visual:** Semarang before/after (`−12.1` vs `−6.2 cm`) two-number comparison + `p01` time-series step plot.
- **Link:** `Read the QC audit →` (`docs/story/atlas_top5_check.md`)

---

## Section 4 — Why You Can Trust It (`1:30–2:05`)

- **Heading (6 words):** `Checked against GPS, OPERA, and noise`
- **Sentence (23 words):** `Provisional NISAR motion (toward or away from the satellite) tracks 10 GPS stations, matches NASA's OPERA product in Mexico City, and beats noise.`
- **Big numbers:**
  - **`r = 0.92` GPS** (`0.924` across 10 Central Valley stations, `1.00 cm` median RMSE) · `provisional` · `docs/story/validation_report.md`
  - **`r = 0.91` OPERA** (`0.912` in Mexico City vs. `OPERA DISP-S1`; L-band beats C-band in farmland) · `provisional` · `docs/story/opera_check.md`
  - **`σ ≈ 0.3 cm` formal** (`0.294 cm` median formal uncertainty; London clay `3σ = 3.62 cm` floor) · `provisional` · `data/central_valley/summary.json`, `data/uk_clay/detection.json`
- **Visual:** Central Valley GNSS scatter plot (`docs/story/media/pc5_gnss_scatter.png` or `#gnssTable`) + OPERA comparison card.
- **Link:** `See all validation checks →` (`science.html`)

---

## Section 5 — What It Is Useful For (`2:05–2:40`)

- **Heading (7 words):** `From ground motion to water and infrastructure`
- **Sentence (23 words):** `We convert sinking into exposed residents, permanent aquifer storage lost each year, canal tilt risk, one-page city bulletins, and a 24-month simulator.`
- **Big numbers:**
  - **`1,479,844` residents** on `549.45 km²` (`< −5 cm`, `|disp| ≥ 2σ`, GHSL E2025) · `provisional` · `data/global/exposure_atlas.json`
  - **`0.3174 km³/yr`** (`317.41 million m³/yr` permanent Central Valley aquifer storage loss) · `mixed` · `data/central_valley_fullyear/storage_loss.json:volume_km3_per_yr`
  - **`81 / 645` segments `> 20 mm/km`** (Tulare Canal `57.01 mm/km` tilt) · `provisional` · `data/central_valley/assets.json`
- **Visual:** `web/assets/simulator.jpg` (real simulator capture) + Central Valley canal risk / bulletin preview.
- **Link:** `Try the simulator (30 s) →` (`game/index.html`)

---

## Section 6 — Original & Open (`2:40–3:00`)

- **Heading (6 words):** `Four original contributions, one open command`
- **Sentence (24 words):** `Every number, figure, and ranking table in our 29-basin atlas reproduces from one open-source command chain using provisional NASA-ISRO NISAR products.`
- **Big numbers:**
  - **`4` original contributions** (`93-day common atlas`, `self-checking QC`, `GPS/OPERA cross-checks`, `storage + tilt + simulator`) · `provisional` · `README.md`
  - **`1` command chain** (`build_atlas.py`, `atlas_qc.py`, `sync_atlas_text.py`, `vital_signs.py`) · `open source` · `docs/story/engine.md`
- **Visual:** 4 crisp contribution cards + one-command code snippet + Team Taykut byline.
- **Link:** `Reproduce from GitHub →` (`https://github.com/keremsumer2010-tech/aseltech`)
