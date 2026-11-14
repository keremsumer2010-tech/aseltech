# NISAR Data Pipeline (`pipeline/`)

Short usage guide for all data-acquisition, subsetting, and driver-extraction scripts.

## Core Scripts (`pipeline/*.py`)

- `pipeline/search.py`: Searches ASF (`asf_search`) for NISAR L2 GUNW products over predefined `SITES` bounding boxes and exports granule metadata CSVs (`pipeline/<site>_gunw.csv`).
- `pipeline/download.py`: Authenticated Earthdata streaming downloader into `raw/` (gitignored). Enforces `MIN_FREE_GB = 20.0` before downloading.
- `pipeline/inspect_gunw.py`: Inspects a NISAR L2 GUNW HDF5 file's groups, grids, units, and attributes and writes `docs/gunw_structure.md`.
- `pipeline/subset.py`: Subsets GUNW HDF5 files to a site bounding box (unwrapped phase → cm LOS, coherence, connected components, ionosphere screen, incidence angle, quality tag) and saves compressed `.npz` files under `pipeline/subset/<site>/`.
- `pipeline/gcov_subset.py`: Extracts provisional NISAR L2 GCOV HV backscatter (`gamma0_HV` in dB) for Central Valley and renders north-up RGBA PNG overlays + `data/central_valley/gcov/meta.json`.
- `pipeline/sme2_drivers.py`: Streams NISAR L2 SME2 soil moisture and GCOV HV backscatter via HTTP Range (`0 GB` local raw HDF5 storage) and builds `data/central_valley/drivers.json`.

## PC2 Site Wrappers & Helpers (`pipeline/pc2/*.py`)

- `pipeline/pc2/batch_subset.py`: One-by-one ASF search → stream download → `subset.py` → immediate `.h5` deletion wrapper. Supports `--out-dir`, `--csv-path`, `--include-beta`, `--start-date`, `--end-date`, `--max-pairs`, `--dry-run`.
  - Example: `python -u pipeline/pc2/batch_subset.py karapinar_fullyear --include-beta --start-date 2025-10-17 --end-date 2026-01-10`
- `pipeline/pc2/run_cumulative.py`: Registers PC2 site bounding boxes (`delta`, `delta_p135`, `konya_plain`, `karapinar_fullyear`, `central_valley_p114`) in `gunw_io.BBOX` and invokes `analysis/cumulative.py` unmodified.
  - Example: `python pipeline/pc2/run_cumulative.py konya_plain --data-dir data/konya_plain`
- `pipeline/pc2/delta_levees.py`: Queries OSM Overpass for Sacramento–San Joaquin Delta levees/dams, samples `data/delta` cumulative LOS subsidence along ways, and writes `docs/story/media/pc2_delta.png` + `docs/story/delta.md`.
- `pipeline/pc2/konya_plain_plot.py`: Generates `docs/story/media/pc2_konya_plain.png` and `docs/story/konya_plain.md` from `data/konya_plain/`.
- `pipeline/pc2/karapinar_drivers.py`: Streams provisional SME2 soil moisture + GCOV HV backscatter over HTTP Range for Karapınar (`2026-06-26 → 2026-10-12`) and writes `data/karapinar/drivers.json`.

## Operational Rules

- Always keep free disk space `>= 20.0 GB`; download at most 1 `.h5` file at a time and delete it immediately after subsetting.
- Never commit `raw/` HDF5 files; only commit compressed `.npz` subsets and `data/<site>/` outputs.
- Preserve `quality` tags (`provisional`, `beta-precal`, `mixed`) and `quality_note` per `rules/VERI_SOZLESMESI.md`.
