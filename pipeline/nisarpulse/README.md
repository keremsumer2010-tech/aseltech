# NISAR Vision (`pipeline.nisarpulse`)

Single-command CLI that turns a bounding box and date range into a quality-tagged NISAR L2 GUNW displacement time series (`data/<site>/` + `data/catalog.json`).

## 5-Minute Quickstart

1. **Prerequisites:** Python 3.11+, `requests`, `numpy`, `h5py`, `matplotlib`, and NASA Earthdata credentials in `~/.netrc` (only needed when downloading; `--dry-run` and unit tests require no credentials).
2. **Plan first (no downloads):**
   ```bash
   python -m pipeline.nisarpulse run \
     --name delta \
     --bbox -121.85,37.95,-121.45,38.20 \
     --start 2026-06-17 --end 2026-10-15 \
     --track 42 --quality provisional --dry-run
   ```
3. **Run end-to-end (stream-download → subset → delete raw `.h5` → cumulative → update `data/catalog.json`):**
   ```bash
   python -m pipeline.nisarpulse run \
     --name delta \
     --bbox -121.85,37.95,-121.45,38.20 \
     --start 2026-06-17 --end 2026-10-15 \
     --track 42 --quality provisional --resume
   ```
4. **Run offline tests:**
   ```bash
   python -m pytest pipeline/nisarpulse -q
   # or without pytest:
   python -m unittest discover -s pipeline/nisarpulse/tests -v
   ```

## Options

- `--quality provisional|mixed`: `provisional` keeps only calibrated-era pairs (`>= 2026-06-17`); `mixed` includes pre-calibration `beta-precal` pairs and tags the output `mixed`.
- `--track N`: Lock to a specific relative orbit / path.
- `--dry-run`: Query CMR, build the interferometric chain, report raw size and any temporal gaps, without downloading.
- `--resume`: Reuse existing `.npz` subsets in `pipeline/subset/<name>/`.
- `--no-catalog`: Skip updating `data/catalog.json`.
