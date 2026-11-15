# NASA Space Apps 2026 — Submission Package (`docs/story/submission_package.md`)

**Team:** Team Taykut / Team Aseltech (ASELSAN Vocational and Technical Anatolian High School, Ankara) · **Challenge:** *Dancing with the SARs* · **Local Event:** Lincoln (UK)  
**Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Live Public Links (Verified HTTP 200)

All links below have been verified accessible with public HTTP 200 responses (no authentication, no paywall, no token required):

| Item | URL | Status (`2026-11-15`) | Notes |
|---|---|---:|---|
| **Live Web App (Final Project)** | `https://keremsumer2010-tech.github.io/aseltech/` | `HTTP 200` | Public landing page (`web/` deployed at Pages root) |
| **GitHub Repository** | `https://github.com/keremsumer2010-tech/aseltech` | `HTTP 200` | Open-source code, data JSONs, pipeline scripts, QA logs |
| **Primary Demo (7-Slide Deck)** | `https://keremsumer2010-tech.github.io/aseltech/docs/story/slides.html` | `HTTP 200` | `≤ 7` English slides (also printable to PDF) |
| **Judge Brief (A4 One-Pager HTML)** | `https://keremsumer2010-tech.github.io/aseltech/docs/story/judge_brief.html` | `HTTP 200` | 3-minute executive summary: 5 KPIs, 4 contributions, links |
| **Judge Brief (A4 One-Pager PDF)** | `https://github.com/keremsumer2010-tech/aseltech/blob/main/docs/story/judge_brief.pdf` | `HTTP 200` | Clean single-page printable PDF generated from data |
| **Global Subsidence Atlas (29 Basins)** | `https://keremsumer2010-tech.github.io/aseltech/atlas.html` | `HTTP 200` | Interactive 29-region ranking, 93-day common window, QC filters |
| **Valley Under Pressure Simulator** | `https://keremsumer2010-tech.github.io/aseltech/game/` | `HTTP 200` | 24-month Terzaghi aquifer compaction educational game |
| **3D Orbit & Subsidence Explorer** | `https://keremsumer2010-tech.github.io/aseltech/web3d/` | `HTTP 200` | Three.js 3D terrain + CelesTrak SGP4 NISAR orbit visualization |
| **29 Regional Early-Warning Bulletins** | `https://keremsumer2010-tech.github.io/aseltech/docs/bulletins/` | `HTTP 200` | NASA Disasters map-package style printable city reports |
| **6-Stop Presentation Mode** | `https://keremsumer2010-tech.github.io/aseltech/present.html` | `HTTP 200` | Fast offline-ready 3-minute jury presentation flow |

*(Note: `https://keremsumer2010-tech.github.io/aseltech/web/index.html` returns `404` because `.github/workflows/pages.yml` deploys `web/.` at the Pages root; always use `https://keremsumer2010-tech.github.io/aseltech/`.)*

---

## 2. Space Apps Requirements Checklist (`docs/story/submission_rules.md`)

- **Official Challenge:** *Dancing with the SARs* (eligible for Global Judging).
- **Language:** All project-page fields, slides (`≤ 7`), and public web pages are in English.
- **No Login / No Paywall:** Verified public access on GitHub and GitHub Pages.
- **Demo Limit:** Single link to `7`-slide English browser deck (`slides.html`) or `29.62 s ≤ 30.0 s` captioned video (`docs/story/media/demo_30s.mp4`).
- **References & Calibration:** Every dataset, literature DOI, and NISAR calibration notice is cited in `docs/story/sources.md` and `docs/story/calibration_note.md`.
- **No Fake Metrics (`K-2`) & Brand Hygiene (`K-9`):** All headline figures trace to `data/` JSON files (`analysis/pc5/numbers_registry.py`: `0` discrepancies); zero NASA/ISRO official logos or `.netrc`/API secrets in the repo.
- **Portal Check (Human):** Team lead confirms event-year checkboxes and `spaceappschallenge.org` submission deadline in a browser before clicking Submit.

---

## 3. NASA & Space Agency Partner Data Used

1. **NASA–ISRO NISAR L2 `GUNW` (`CRID P05023`, `provisional` from `2026-06-17`; pre-`2026-06-17` `beta-precal` strictly isolated as `mixed`):** Unwrapped L-band interferograms, coherence, incidence angle, and split-spectrum ionosphere screen via NASA Earthdata CMR / ASF DAAC (`https://asf.alaska.edu/datasets/daac/nisar/`, `HTTP 200`).
2. **NASA–ISRO NISAR L2 `GCOV` (`P05023`, `preview` / `provisional`):** Dual-pol (`HH`, `HV`) geocoded polarimetric covariance for UK Fens cloud-penetration and crop-structure analysis.
3. **NASA NISAR L3 `SME2`:** Soil moisture epochs used in `drivers_analysis.md`.
4. **NASA JPL `OPERA_L3_DISP-S1_V1`:** Sentinel-1 C-band displacement cross-check (`docs/story/opera_check.md`, `docs/story/cross_sensor.md`).
5. **NASA GIBS (`VIIRS_SNPP_CorrectedReflectance_TrueColor`):** Same-day optical cloud comparison (`2026-10-20`) over eastern England (`data/uk/meta.json`).
6. **External Open Reference Data:** Nevada Geodetic Laboratory continuous GPS (`10` stations), OpenStreetMap infrastructure corridors, WorldPop `100 m` (2020), GHSL `GHS-POP E2025` (`100 m`), USDA CDL `30 m`, ESA WorldCover `10 m`, Tapur & Bozyiğit (2015) Karapınar sinkholes, and CelesTrak NORAD `65053` TLE.

---

## 4. AI Disclosure

- **Images:** Zero AI-generated images in the final site, slides, `web3d/`, `game/`, or `demo_30s.mp4` (commit `38b774f` removed all early illustrations). Every map and figure renders real satellite, GPS, or survey measurements.
- **Code & Documentation Assistance:** Claude and Gemini/Antigravity coding assistants were used for pipeline scripting, automated testing, and drafting documentation. All quantitative outputs were verified against committed JSON datasets, `numbers_registry.py`, `tools/atlas_qc.py`, and peer-reviewed literature DOIs.
