# NISAR Pulse: Follow the Water

Team Taykut · NASA Space Apps Challenge 2026 · Challenge: **Dancing with the SARs** · Local event: Lincoln (UK)

Farms are irrigated, groundwater is pumped, and the ground sinks. NASA-ISRO's NISAR radar sees through
clouds and measures that motion in centimetres. We turn it into maps, human-scale sentences and risk
layers anyone can read.

**Study areas:** California Central Valley (USA) · Konya / Karapınar (Türkiye) · The Fens (UK)

**Data:** NASA-ISRO NISAR (GUNW, GCOV, SME2) via ASF DAAC.
NISAR data are provisional. Calibration and validation are carried out by the NISAR project
(NASA-JPL and ISRO), not by our team. We use the products as released.

**Live site:** _link added after first deploy_

---

## What is in this repository

| Folder | What it does |
|---|---|
| `pipeline/` | Search ASF for NISAR products, download them, cut each one to a study-area box (`.npz`) |
| `analysis/` | Phase → centimetres, masks, reference, cumulative maps, web outputs (`analysis/insar.py`, `analysis/cumulative.py`) |
| `analysis/decomp/` | Permanent vs seasonal (recoverable) subsidence: trend + annual sine per pixel |
| `validation/` | Comparison with continuous GNSS stations (Nevada Geodetic Laboratory) |
| `risk/` | Subsidence gradient along canals, railways and highways (OpenStreetMap) |
| `data/` | Small files the website reads (JSON, PNG, GeoJSON). Format: `rules/VERI_SOZLESMESI.md` §4 |
| `web/` | The story website (static HTML/JS, MapLibre GL, Chart.js) |
| `game/` | "Aquifer Manager" browser game (illustrative model, numbers labelled) |
| `web3d/` | 3D "breathing earth" viewer |
| `docs/` | Plans, data structure notes, sources (`docs/story/sources.md`), QA notes |

Raw NISAR files (`.h5`, ~2.3 GB each) are **never** stored in the repository; they go to `raw/` (git-ignored)
and are deleted after cutting.

## Setup

Python 3.11+:

```bash
pip install asf_search h5py numpy scipy matplotlib pyproj rasterio shapely requests pytest
```

Downloading `.h5` files needs a free NASA Earthdata account. Put your credentials in `~/.netrc`
(Windows: `%USERPROFILE%\_netrc`) yourself, exactly in this form (no colons):

```
machine urs.earthdata.nasa.gov
login YOUR_USERNAME
password YOUR_PASSWORD
```

Never commit this file (`.gitignore` already excludes it). Browse PNGs and GNSS / OpenStreetMap data need no login.

## Running the data pipeline, step by step

Study areas and their boxes are fixed in `rules/VERI_SOZLESMESI.md` §1
(`central_valley`, `karapinar`, `konya`, `fens`). Only **provisional** products (both dates on or after
2026-06-17, CRID P05023) go into the same sum; earlier "beta" products are kept in separate folders.

**1 · Find products** (writes `pipeline/<site>_gunw.csv`)
```bash
python pipeline/search.py central_valley
```

**2 · Download one pair** (into `raw/`)
```bash
python pipeline/download.py pipeline/central_valley_gunw.csv --date1 2026-06-28 --date2 2026-07-10
```

**3 · Cut it to the study box** (writes `pipeline/subset/<site>/<date1>_<date2>.npz`: phase, coherence,
connected components, ionosphere screen, coordinates, wavelength, incidence, quality)
```bash
python pipeline/subset.py raw/<granule>.h5 central_valley
```
Repeat 2–3 for every consecutive pair. Alternative used by the analysis team (search + download + cut +
delete raw, one pair at a time): `python analysis/fetch_subset.py central_valley 34 020 100`
(site, track, frame, reference height in metres for the incidence angle).

**4 · Cumulative ground motion** (reads every `.npz` of the site, checks the chain has no gaps)
```bash
python analysis/cumulative.py central_valley
python analysis/cumulative.py karapinar --ref-radius 10
```
Per pair: phase → cm with −λ/(4π) (λ from each file's `centerFrequency`; negative = away from the satellite =
sinking) → subtract the product's ionosphere screen → masks (coherence ≥ 0.3, connected components,
small islands, unwrapping-cycle jumps) → remove a plane + elevation term (Copernicus DEM GLO-90, downloaded
to `raw/dem/`) → reference all pairs to the same stable window → add up.
Writes:
- `data/<site>/meta.json`, `points.json`, `summary.json`, `disp/<date>.png` (what the website reads)
- `analysis/out/<site>_cum.npz` and `<site>_cum_stack.npz` (numeric grids for validation and risk)

**5 · Validation and risk**
```bash
python validation/fetch_gnss.py
python validation/compare.py --npz analysis/out/central_valley_cum.npz --out data/central_valley/validation.json
python risk/fetch_osm_infra.py
python risk/compute_risk.py
```

**6 · Website** — open locally from the repository root:
```bash
python -m http.server 8000
```
then visit `http://localhost:8000/web/`. On every push to `main`, `.github/workflows/pages.yml` publishes
`web/` + `data/` + `game/` to GitHub Pages.

## Tests

```bash
cd analysis && python -m pytest -q
python -m pytest analysis/decomp -q
python validation/compare.py --self-test
python risk/compute_risk.py --self-test
```

## Honest limits

- Values on the maps are **line of sight** (the radar's viewing direction), not purely vertical. Vertical
  numbers are estimates (LOS / cos(incidence)).
- One summer of data: yearly rates are linear extrapolations and labelled "estimate".
- Troposphere model layers and solid-earth tides are not applied; a plane + elevation fit is used instead.
  A few cm of atmospheric noise per pair remains.
- The absolute size of the largest value depends on the reference area (Central Valley: −6.2 to −7.8 cm,
  stored in `summary.json` → `max_subsidence_range_cm`).

## Sources

Every number in the story has a source in [`docs/story/sources.md`](docs/story/sources.md). Key method references:

- NISAR GUNW product guide (ASF): https://nisar-docs.asf.alaska.edu/gunw
- NISAR Solid Earth ATBD: https://github.com/nisar-solid/ATBD
- MintPy (sign convention, phase-to-range, phase–elevation correction): https://github.com/insarlab/MintPy
- ISCE3 (interferogram formation): https://github.com/isce-framework/isce3
- Copernicus DEM GLO-90: https://copernicus-dem-90m.s3.amazonaws.com/ (© DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018, provided under COPERNICUS by the European Union and ESA)
- GNSS: Nevada Geodetic Laboratory, https://geodesy.unr.edu/
- Map data © OpenStreetMap contributors, ODbL. Basemap imagery © Esri, Maxar, Earthstar Geographics.

## AI use

Code and texts were written with the help of AI assistants (Claude Code, Antigravity / Gemini). Images and
video made with AI (Higgsfield) are labelled "AI-generated illustration" on the site and are never shown as
data. Every measured number comes from NISAR files by code, not from an AI model.

## Team

Team Taykut — Kerem (`keremsumer2010-tech`), Memir (`memir-erdogmus`), Mehmet (`M3hmeT1888`),
İbrahim (`acikgozibrahim032-hub`).

## License

MIT (see [`LICENSE`](LICENSE)). Map data © OpenStreetMap contributors, ODbL.

---
Contributors and AI agents: start with [`CLAUDE.md`](CLAUDE.md).
