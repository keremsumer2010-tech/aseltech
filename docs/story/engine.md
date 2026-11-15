# NISAR Vision — Single-Command Operational Engine

**What it does:** Turns any bounding box and date window into a quality-tagged NISAR L2 GUNW displacement time series (`data/<site>/meta.json`, `disp/*.png`, `points.json`, `summary.json`) and registers it in `data/catalog.json` with one command.

## Architecture (`pipeline/nisarpulse/`)

- `search.py` — Supports `--center lon,lat --box-deg 0.25` (default `±0.25°` ≈ 55 × 55 km) or explicit `--bbox w,s,e,n`, queries NASA CMR for `NISAR_L2_GUNW_PROVISIONAL_V1` (and `BETA_V1` when `--quality mixed`), classifies pairs (`>= 2026-06-17` provisional vs `beta-precal`), builds a continuous interferometric chain, and writes `coverage.json` (`coverage: "none"` on empty coverage) plus gap diagnostics.
- `fetch.py` — Enforces a `20.0 GB` free-disk floor, streams one HDF5 granule at a time via `pipeline.download.download_file`, subsets to compressed `.npz` via `pipeline.subset.subset_gunw`, and deletes the raw `.h5` immediately.
- `process.py` — Registers the site bounding box at runtime, runs `analysis/cumulative.py` unmodified (with optional `--data-dir` and out-of-basin `--ref-lonlat lon,lat` re-referencing), and appends standardized Atlas quality metrics (`p2_cm`, `rate_cm_per_100d`, `valid_fraction`, `confidence`) to `summary.json`.
- `catalog.py` — Upserts a `rules/VERI_SOZLESMESI.md`-compliant entry into `data/catalog.json` (skippable via `--no-catalog` for global atlas runs).

## End-to-End Verification (Sacramento–San Joaquin Delta)

1. **Dry-run plan (`1.20s`, `0` bytes downloaded):**
   ```bash
   python -m pipeline.nisarpulse run \
     --name delta \
     --bbox -121.85,37.95,-121.45,38.20 \
     --start 2026-06-17 --end 2026-10-15 \
     --track 42 --quality provisional --dry-run
   ```
   Output: `granules=18 chain_pairs=9 total_raw=19956.3 MB gaps=0` (Path 42, Frame 69, `2026-06-17 → 2026-10-15`).

2. **Full pipeline run with cached `.npz` subsets (`--resume`, `6.9s`):**
   ```bash
   python -m pipeline.nisarpulse run \
     --name delta \
     --bbox -121.85,37.95,-121.45,38.20 \
     --start 2026-06-17 --end 2026-10-15 \
     --track 42 --quality provisional --resume --no-catalog
   ```
   Output: `Done [delta] -> data/delta | max_subsidence_cm=-1.3 | elapsed=6.9s` (`range_cm=[-1.3, -1.1]`, `120 days`, `quality="provisional"`).

3. **Offline unit tests (`8/8` pass):**
   ```bash
   python -m unittest discover -s pipeline/nisarpulse/tests -v
   ```
   CI runs `python -m pytest pipeline/nisarpulse -q` on push/PR via `.github/workflows/tests.yml`.

## Multi-Region Global Atlas Proof (`data/global/`, `provisional`)

All five Priority-A basins below were processed end-to-end with `pipeline.nisarpulse` (`--quality provisional`, `--data-dir data/global/<city> --no-catalog`):

| City | Path / Frame | Period | Pairs | Max LOS (cm) | `p2_cm` | `rate_cm_per_100d` | `valid_fraction` | `confidence` |
|---|---|---|---:|---:|---:|---:|---:|---|
| `isfahan` | P056 / F018 | `2026-06-18 → 2026-10-16` | 9 | -2.5 | -2.90 | -2.08 | 0.325 | `medium` |
| `rafsanjan` | P128 / F017 | `2026-06-23 → 2026-10-21` | 9 | -5.8 | -4.30 | -4.83 | 0.847 | `medium` |
| `mashhad` | P078 / F070 | `2026-06-19 → 2026-10-17` | 9 | -8.6 | -6.68 | -7.17 | 0.705 | `medium` |
| `quetta` | P041 / F017 | `2026-06-17 → 2026-10-15` | 9 | -3.8 | -2.50 | -3.17 | 0.713 | `medium` |
| `delhi` | P106 / F074 | `2026-06-21 → 2026-10-19` | 8 | -4.3 | -4.45 | -3.58 | 0.053 | `low` |

## Reproduce any atlas region in one command

Every published atlas region can be reproduced directly from its `meta.json` granule list (`pipeline/nisarpulse/reproduce.py`):

```bash
python -m pipeline.nisarpulse reproduce <id>
# Dry-run plan (offline, 0 bytes):
python -m pipeline.nisarpulse reproduce <id> --dry-run
```

When cached `.npz` subsets are present in `pipeline/subset/<id>/`, `reproduce` recomputes the full cumulative chain with `--qc` enabled and compares the resulting `summary.json` against the published record (without overwriting `data/`):

| Region | Granules | Original `max_subsidence_cm` | Reproduced `max_subsidence_cm` | `range_cm` (Orig / Repro) | Rate (Orig / Repro) | Diff (`cm`) | Runtime |
|---|---:|---:|---:|---|---|---:|---:|
| `konya_plain` | 8 / 8 | `-9.6` | `-9.6` | `[-14.0, -9.6]` / `[-14.0, -9.6]` | `-32.5` / `-32.5 cm/yr` | **`0.0`** | `64.0 s` |
| `mashhad` | 9 / 9 | `-8.6` | `-8.6` | `[-8.6, -6.0]` / `[-8.6, -6.0]` | `-26.3` / `-26.3 cm/yr` | **`0.0`** | `12.5 s` |

Expected JSON output (`mode: "reproduced"` when subsets are cached, or `mode: "dry-run"` listing missing granules if offline without cache):

```json
{
  "mode": "reproduced",
  "region": "mashhad",
  "granules": 9,
  "cached": 9,
  "diff_max_cm": 0.0,
  "elapsed_s": 12.516
}
```
