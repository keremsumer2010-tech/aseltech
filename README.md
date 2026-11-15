<p align="center">
  <a href="https://keremsumer2010-tech.github.io/aseltech/">
    <img src="web/assets/logo_mark_192.png" alt="NISAR Vision logo: satellite, radar waves and sinking ground layers" width="120">
  </a>
</p>

# NISAR Vision: Follow the Water

**Live Site:** https://keremsumer2010-tech.github.io/aseltech/ · **Team Aseltech** · NASA Space Apps Challenge 2026 · Challenge: **Dancing with the SARs** · Local event: Lincoln (UK)

> *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

**We turned the first months of NASA-ISRO NISAR radar data into a self-checking global subsidence atlas: 29 basins measured with one open pipeline on the same 93 days, every number traceable to its file, and every headline checked against GPS, NASA's OPERA product and the literature.** Using provisional 24.2 cm L-band interferograms (`CRID P05023`, June–October 2026), **NISAR Vision** separates permanent clay compaction from seasonal rebound, quantifies canal and railway tilt, and connects measurements to a 24-month aquifer simulator.

- **Live Site:** https://keremsumer2010-tech.github.io/aseltech/
- **Three-Minute Story Spec:** [docs/story/three_minute_story.md](docs/story/three_minute_story.md)
- **Global Subsidence Atlas (29 Regions):** [web/atlas.html](web/atlas.html) (`https://keremsumer2010-tech.github.io/aseltech/atlas.html`)
- **6-Stop Lincoln Presentation Mode (Offline-Ready):** [web/present.html](web/present.html)
- **Groundwater Simulator:** [game/index.html](game/index.html) (`https://keremsumer2010-tech.github.io/aseltech/game/`)
- **Science Sign-Off & Submission Package:** [docs/qa/SCIENCE_SIGNOFF.md](docs/qa/SCIENCE_SIGNOFF.md) · [docs/story/submission_package.md](docs/story/submission_package.md)

---

## What We Built (Nine Things, One by One)

1. **Global Subsidence Atlas:** `29` basins (`16` reliable, `13` indicative) on three continents, ranked over the same `93` days (`28 Jun–29 Sep 2026`; `#1` Konya Plain `−11.0 cm/100d`, caution).
2. **Self-Checking Quality Control:** Automated time-series scan for `12.1 cm` full L-band phase-cycle jumps and single-date spikes (`Semarang` fixed `−12.1 → −6.2 cm`; `5` flagged basins kept indicative).
3. **Proof on the Ground:** `r = 0.924` agreement with `10` continuous GPS stations in Central Valley (`1.00 cm` median RMSE), plus `≈ 0.3 cm` formal noise and London Clay negative control (`3σ = 3.62 cm`, `below_detection`).
4. **Who Lives on Sinking Ground:** `GHSL 2025` overlay counting **`1,200,716` residents** (`1.20 M`) on **`511.65 km²`** sinking `> 5 cm` (`|disp| ≥ 2σ`).
5. **Water Storage Lost for Good:** 11-month harmonic decomposition in Central Valley separating permanent clay compaction (**`0.3174 km³/yr`** lost storage) from seasonal rebound.
6. **Canals and Railways at Risk:** Longitudinal tilt screening across `645` OpenStreetMap segments (`81 / 645 > 20 mm/km`, Tulare Canal `57.01 mm/km`).
7. **One-Page Basin Bulletins:** `29` printable NASA-style monitoring bulletins (`docs/bulletins/<region>.html`).
8. **Simulator Anyone Can Play:** 24-month *Groundwater Simulator* (`game/index.html`) calibrated to Terra Bella compaction and NISAR rates.
9. **Open One-Command Engine:** `NISAR Vision` (`pipeline/nisarvision`) to download, measure, and self-check any new region from public NASA ASF data.

---

## Key Results (Ten Verified Headline Numbers)

All figures below match [`docs/qa/SCIENCE_SIGNOFF.md`](docs/qa/SCIENCE_SIGNOFF.md) and the repository JSON files:

| # | Metric | Headline Value | Uncertainty / Notes | Quality |
|---:|---|---|---|---|
| 1 | **Central Valley Peak Subsidence (108 d)** | **`−7.8 cm` LOS** (`−10.1 cm` vert. est. at `39.1°`) | 3-ref spread `[−7.8, −4.7] cm`; formal `σ_med = 0.294 cm` | `provisional` |
| 2 | **Central Valley Sinking Area (`< −5 cm`)** | **`239.54 km²`** (`1,578.27 km² < −2 cm`) | Common-valid pixels (`62.9%` valid fraction) | `provisional` |
| 3 | **10-Station GNSS Cross-Check (CV)** | **`r = 0.924`**, **`1.00 cm` median RMSE** | `1.37 cm` final-epoch RMSE (`0.76 cm` on active sites `> 2 cm`) | `provisional` |
| 4 | **Infrastructure Differential Tilt** | **`81 / 645` segments `> 20 mm/km`** | Tulare Canal **`57.01 mm/km`**; `±25%` top-10 `100%` rank-invariant | `provisional` |
| 5 | **Full-Year Decomposition (`Earlimart p01`)** | **`−16.8 ± 2.2 cm/yr`** permanent vs. **`11.7 cm`** seasonal | `R² = 0.97` sinusoidal + linear (`25` pairs, `324` days) | `mixed` |
| 6 | **Permanent Aquifer Storage Loss (CV)** | **`0.3174 km³/yr`** (`317.41 million m³/yr`) | `1 km` block SE `±0.00123 km³/yr`; 3-ref `0.0664–0.3198 km³/yr` | `mixed` |
| 7 | **Karapınar Basin & 29-Sinkhole Contrast** | **`−5.9 cm` LOS** (`−8.0 cm` vert. est.); **`6.4×`** `< 1 km` | `−4.15 cm` `< 1 km` vs. `−0.65 cm` `> 5 km` (`p = 0.0001` block perm) | `provisional` |
| 8 | **London Clay Negative Control** | **`below_detection`** (`97.7%` within `±1.5 cm`) | `chain_sigma = 1.21 cm`, **`3σ = 3.62 cm`** floor (`9` pairs) | `provisional` |
| 9 | **2026 Global Subsidence Atlas (#1 Reliable)** | **#1 Konya Plain `−11.0 cm/100d`** (`93 d` common) | **`29` regions (`16` reliable / `13` indicative)**; Konya valid-pixel fraction unrecorded (caution) | `provisional` |
| 10 | **Global GHSL Exposure (`< −5 cm`, `|disp| ≥ 2σ`)** | **`1,200,716` residents** on **`511.65 km²`** | `GHSL E2025` (`100 m`), all `29` regions excluding nested `karapinar` | `provisional` |

*Secondary OPERA cross-check:* Over Mexico City the spatial pattern matches NASA JPL's OPERA product at 10 points (`r = 0.91`), although OPERA covers winter (`2025-12-25` to `2026-03-25`) and NISAR summer (`2026-06-22` to `2026-10-20`); in the Central Valley and at Eloy the agreement is weak (`r = 0.40` and `0.09`) because seasons and viewing geometry differ. Main validation is GPS (`r = 0.924`).

---

## Reproduce the Atlas in One Command Chain

All atlas tables, QC flags, and text summaries are generated deterministically from `data/global/` without hard-coding:

```bash
python3 pipeline/pc10/build_atlas.py && python3 tools/atlas_qc.py && python3 tools/sync_atlas_text.py && python3 tools/vital_signs.py --check
```

- `pipeline/pc10/build_atlas.py`: aggregates all regional `summary.json`, `validation_note.json`, and common-window (`2026-06-28 → 2026-09-29`) rates into `data/global/atlas.json`.
- `tools/atlas_qc.py`: scans `p01` time series for `12.1 cm` full L-band phase-cycle unwrapping jumps and `> 5 cm` cancelling single-date spikes (`data/global/qc_flags.json`).
- `tools/sync_atlas_text.py`: updates region counts and tables in `docs/story/technical_note.md` and `technical_note.html` from `atlas.json`.
- `tools/vital_signs.py --check`: verifies `data/global/vital_signs.json` against `atlas.json` and `exposure_atlas.json`.

---

## Data Sources & Licenses

| Dataset | Provider / License | Use in NISAR Vision |
|---|---|---|
| **NISAR L2 GUNW, GCOV, SME2** (`beta` & `provisional`, `CRID P05023`) | NASA-ISRO / ASF DAAC (NASA Open Data Policy) | Interferometric displacement, backscatter polarization (`HH`/`HV`), soil moisture |
| **Continuous GNSS (`IGS14`)** | Nevada Geodetic Laboratory, UNR (CC-BY / Open) | 10-station Central Valley & multi-region independent validation (`r = 0.924`) |
| **GHSL `GHS-POP E2025 R2023A`** (`100 m`) | European Commission JRC (CC-BY 4.0) | Global population exposure on sinking ground (`< −5 cm`, `|disp| ≥ 2σ`) |
| **WorldPop (2020), USDA CDL (2021), ESA WorldCover** | WorldPop / USDA NASS / ESA (CC-BY / Public Domain) | Central Valley & Karapınar agricultural and population overlays |
| **Canals, Railways, Highways & Karapınar Sinkholes** | OpenStreetMap (ODbL) & AFAD / peer-reviewed inventories | Longitudinal tilt (`mm/km`) and sinkhole-proximity permutation tests |

Full DOIs and live HTTP-verified references: [`docs/story/sources.md`](docs/story/sources.md).

---

## AI Usage Disclosure

Code, analysis scripts, tests, and prose documentation were written with the assistance of AI coding tools (Anthropic Claude and Google Gemini) and verified by Team Aseltech: every reported metric is read directly from repository JSON outputs, every scientific claim carries a peer-reviewed DOI or dataset citation, and automated unit/consistency tests cover core conversions and site numbers. **Zero AI-generated images** appear anywhere on the website, presentation deck, 3D viewer, or simulator — every map, plot, and screenshot reflects real NISAR data or real application captures.

---

## Repository Map

| Folder | What it does |
|---|---|
| `pipeline/` | ASF NISAR product search, subsetting, and `build_atlas.py` (`pipeline/pc10/`) |
| `analysis/` | Phase → cm conversion, atmospheric plane removal, GNSS validation, and `decomp/` full-year separation |
| `validation/` | Independent GNSS cross-checks (Nevada Geodetic Laboratory) and `opera_check` diagnostics |
| `risk/` | Subsidence gradient (`mm/km`) along canals, railways, and highways (OpenStreetMap) |
| `data/` | Processed JSONs, displacement PNGs, and GeoJSON layers consumed by the website and tests |
| `web/` | Static NASA-EO-style web application (`index.html`, `atlas.html`, `present.html`, `science.html`, `data.html`, `explorer.html`, `faq.html`) |
| `game/` | 24-month *Groundwater Simulator* (`model.js`, `tests.js`, `test_model.html`) |
| `web3d/` | Interactive 3D Earth subsidence globe |
| `tools/` | `sync_atlas_text.py`, `atlas_qc.py`, `atlas_completeness.py`, `vital_signs.py`, `bulletin.py` |
| `tests/` | `pytest` consistency checks (`tests/test_site_numbers.py`, `analysis/`, `pipeline/`) |
| `docs/` | Scientific notes, city cards (`docs/story/atlas_cities/`), QA logs (`docs/qa/`), and `RELEASE_NOTES.md` |

Raw NISAR granules (`.h5`, ~2.3 GB each) are **never** committed; they reside in git-ignored `raw/` and are deleted after subsetting.

---

## Setup & Pipeline Steps

Python 3.10+:

```bash
pip install asf_search h5py numpy scipy matplotlib pyproj rasterio shapely requests pytest
```

Downloading `.h5` granules requires a free NASA Earthdata account in `~/.netrc`:

```text
machine urs.earthdata.nasa.gov
login YOUR_USERNAME
password YOUR_PASSWORD
```

Running the core test suite:

```bash
python3 -m pytest tests/test_site_numbers.py -v
```
