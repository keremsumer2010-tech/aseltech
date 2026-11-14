# Code review (Q15, PCQ) · 2026-11-14 14:35 TR · HEAD 8467459

Scope: `pipeline/`, `analysis/` (incl. `decomp/`), `validation/`, `risk/`, `web/`, `game/`, `web3d/`, `.github/workflows/pages.yml`.
I report only; owners fix. Format: `OK` / `HATA: file → problem → fix`. Most important first.
Transparency: PCQ wrote parts of `analysis/` earlier in this session (as PC3), so that part is reviewed by
re-running tests and linting, not by a fully independent eye.

## Tests (run on this machine, Python 3.12, Windows)

| Command | Result |
|---|---|
| `python -m pytest analysis -q` (insar + cumulative + decomp) | **24 passed** in 4.1 s |
| `python validation/compare.py --self-test` | **passed** ("10 stations evaluated, JSON clean") |
| `python risk/compute_risk.py --self-test` | **passed** ("top 10 segments valid GeoJSON, zero NaNs") |
| `pipeline/*` | no tests (network/Earthdata-bound scripts) |
| `game/test_model.html` | browser-only, not run automatically |
| `web/`, `web3d/` | no tests |

## Findings

### High
- HATA: `.github/workflows/pages.yml` → publishes only `web/ + data/ + game/`. `game/game.js:910` fetches
  `../risk/central_valley_infra.geojson`, which will be **404 on GitHub Pages** (works locally). The game
  catches it (no crash) but the infrastructure backdrop disappears online → copy `risk/*.geojson` into `_site/risk/`
  (or move the file under `data/central_valley/`). Owner: PC1 (workflow) / PC6 (game).
- HATA: `.github/workflows/pages.yml` → `web3d/` (3D viewer, mentioned in `docs/story/project_page.md` as a
  deliverable) is **not deployed** and not linked from `web/index.html` → add `cp -r web3d _site/web3d` and a link,
  or drop it from the project page. Owner: PC1.
- HATA: `pipeline/download.py:18-27,75` → takes the **first** `password` token in `~/.netrc` (ignores the
  `machine` line) and sends it as `Authorization: Bearer …`. With the documented `.netrc` format (rules E-07:
  real Earthdata password) this is not a bearer token → 401; with several machines in `.netrc` the wrong secret
  can be sent. Works today only if the user stored an EDL token as "password". → use `netrc.netrc().authenticators("urs.earthdata.nasa.gov")`
  with `requests` session auth (as `analysis/fetch_subset.py` does via `curl --netrc-file`), or read an explicit
  `EARTHDATA_TOKEN` env var. (Secret is never printed: OK.) Owner: PC2.

### Medium
- HATA: `web/app.js` `humanScale()` / `select()` → see `docs/qa/PCQ.md` (no scale below a bank card, no noise
  threshold, "sank" for LOS, month rounding 3.5→4). Owner: PC1.
- HATA: `analysis/cumulative.py:24` → unused imports `median_filter`, `minimum_filter` (pyflakes). Harmless. Owner: PC3.
- HATA: `web3d/generate_3d_data.py:90` → unused `h5py` import (pyflakes). Harmless, but makes the script need h5py. Owner: PC4.
- HATA: `analysis/cumulative.py` `choose_reference` → pure-Python double loop over the grid (stride 3, ~235 k
  windows on 1473×1438): ~10 s, acceptable now; for the full-year run consider a vectorised box filter. Owner: PC3.
- HATA: no `requirements.txt` → installs are described only in README. Suggest pinning:
  `asf_search h5py numpy scipy matplotlib pyproj rasterio shapely requests pytest`. Owner: PC1 (root file).
- BİLGİ: `game/game.js:923` → box title "Calibration Verification" means *model* calibration against NISAR; to avoid
  confusion with NISAR's own calibration (rules §4) → "Model check against NISAR". Owner: PC6.

### Hard-coded paths
- OK: no absolute paths (`C:\`, `/Users/`, `/home/`) in any `.py`, `.js`, `.html`.
- OK: scripts resolve the repo root from `__file__` (`analysis/*.py`, `pipeline/search.py`) or take paths as arguments.
- OK: web uses relative paths (`../data` locally, `./data` on Pages, `web/app.js:3-4`).
- OK: wavelength is never hard-coded; read from `centerFrequency` per file (`analysis/gunw_io.py`, MintPy-style).
- BİLGİ: study-area boxes are duplicated in `analysis/gunw_io.py` (`BBOX`) and `pipeline/` (`SITES`); both match
  `rules/VERI_SOZLESMESI.md` §1 today. A single shared module would avoid drift.

### Error-handling / data-safety
- OK: no script deletes folders; deletions are limited to its own raw `.h5`/`.part`/cookie file (`analysis/fetch_subset.py:57-65`,
  `pipeline/download.py:116`) — rule K-7 respected.
- OK: `pipeline/download.py` checks free disk (RULES §8) and the HDF5 magic bytes before accepting a file; resumes with `Range`.
- OK: `analysis/cumulative.py` refuses non-provisional pairs, stops at chain gaps, refuses mismatched grids, and
  warns when an output exceeds 20 MB (K-12).
- OK: `analysis/gunw_io.py` checks that the reference date is earlier than the secondary date (sign convention).
- BİLGİ: `web/app.js` `getJSON()` and `game/game.js` `boot()` swallow fetch errors silently. Fine for users,
  but a `console.warn` would make broken deploys visible.
- BİLGİ: `analysis/gunw_io.py:87` broad `except Exception` only around reading `granuleId` (falls back to file
  name) — acceptable.

## Summary
All automated tests pass. No secrets or absolute paths in code. The two deploy gaps (`risk/` file used by the game,
`web3d/` not published) and the `.netrc` bearer-token handling are the items to fix before submission.
