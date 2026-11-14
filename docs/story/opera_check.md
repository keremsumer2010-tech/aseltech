# NISAR vs NASA JPL OPERA DISP-S1 Cross-Check

Independent validation of NISAR L-band GUNW displacement against NASA JPL OPERA DISP-S1 (Sentinel-1 C-band) across three North American subsidence basins.

> **Note:** NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

| Basin | NISAR Period | OPERA Period | Co-located `n` | Pearson `r` | RMSE (`cm/100d`) | Slope | Figure |
|---|---|---|---:|---:|---:|---:|---|
| `central_valley` | `2026-06-22 → 2026-10-20` | `2025-07-19 → 2025-10-17` | 7571 | **0.399** | 2.95 | 0.362 | ![central_valley](media/pc2_opera_central_valley.png) |
| `eloy` | `2026-06-19 → 2026-10-17` | `2026-01-24 → 2026-04-30` | 581 | **0.091** | 1.03 | 0.102 | ![eloy](media/pc2_opera_eloy.png) |
| `mexico_city` | `2026-06-22 → 2026-10-20` | `2025-12-25 → 2026-03-25` | 10 | **0.912** | 5.09 | 1.278 | ![mexico_city](media/pc2_opera_mexico_city.png) |

## Five Diagnostic Tests: Why `r` Varies Across Basins

To explain why Mexico City reaches `r = 0.912` while Central Valley (`r = 0.399`) and Eloy (`r = 0.091`) are much lower, we ran five controlled sensitivity tests (`pipeline/pc2/opera_explain.py`):

| Test | Central Valley (`r / RMSE / slope / n`) | Eloy (`r / RMSE / slope / n`) | Mexico City (`r / RMSE / slope / n`) | Finding |
|---|---|---|---|---|
| **Baseline** (LOS, re-ref, 1 km) | `0.399 / 2.95 / 0.362 / 7571` | `0.091 / 1.03 / 0.102 / 581` | `0.912 / 5.09 / 1.278 / 10` | Reference benchmark (`opera_check.json`) |
| **(a) Temporal overlap** | `0 days` overlap (Sum '25 vs Sum '26) | `0 days` overlap (Spring '26 vs Sum '26) | `0 days` overlap (Win '26 vs Sum '26) | **Primary driver:** OPERA CMR archive ends `2026-02..04` |
| **(b) Vertical (`LOS / cos θ`)** | `0.399 / 3.80 / 0.361 / 7571` | `0.091 / 1.32 / 0.102 / 581` | `0.875 / 4.30 / 0.654 / 10` *(54d)* | **Not a driver:** `r` unchanged; `1/cos θ` scales noise |
| **(c) Unaligned reference** | `0.399 / 2.20 / 0.362 / 7571` | `0.091 / 1.04 / 0.102 / 581` | `0.875 / 3.09 / 0.708 / 10` *(54d)* | **Not a driver for `r`:** only shifts constant offset/RMSE |
| **(d) Resolution (`80 m → 1 km → 2 km`)** | `0.354 → 0.399 → 0.417` (`RMSE 3.11→2.86`) | `0.035 → 0.091 → 0.130` (`RMSE 1.20→1.00`) | — (point windows) | **Moderate factor:** block averaging reduces 80 m speckle |
| **(e) Landcover (`coh ≥ 0.55` vs `< 0.55`)** | High: `0.320` (`n=4269`) / Agri: `0.474` (`n=1653`) | High: `0.118` (`n=321`) / Agri: `-0.021` (`n=158`) | Urban clay (`100%` high-SNR) | **Eloy C-band loss:** OPERA masks `80.6%` of Eloy (`valid=0.194`) |

### Honest Interpretation

1. **Zero temporal overlap (`OPERA` archive stops in spring 2026):** Steady year-round clay compaction in Mexico City (`-7` to `-14 cm/100d`) preserves spatial correlation (`r = 0.912`) across non-overlapping windows. By contrast, Eloy switches between spring recharge/low pumping (OPERA `Jan–Apr 2026`, `RMSE = 1.03 cm/100d`) and summer peak irrigation (NISAR `Jun–Oct 2026`), while Central Valley compares two different summers (`2025` vs `2026`, inter-annual pumping shift).
2. **C-band agricultural decorrelation in Eloy:** Sentinel-1 C-band `recommended_mask == 1` retains only `19.4%` of Eloy pixels (`80.6%` masked), and in agricultural pixels (`coh < 0.55`) correlation collapses to `r = -0.021`.
3. **Geometry and reference alignment do not explain low `r`:** Vertical `cos θ` projection and reference alignment change RMSE/offset, leaving `r` identical.

## Methodology & LOS Geometry Note

- **Central Valley (direct temporal overlap):** Two OPERA F38502 cumulative frames (`2025-10-17 → 2025-11-28` and `2025-10-17 → 2026-02-14`) were differenced to isolate `2025-11-28 → 2026-02-14` (78 days), matching NISAR Path 114 `2025-11-30 → 2026-02-10` (72 days) on the exact `EPSG:32611` UTM grid and shared reference window.
- **Eloy & Mexico City (cross-season rate comparison):** OPERA DISP-S1 archive currently extends through spring 2026 (`2026-04-30` / `2026-03-31`), whereas NISAR provisional starts `2026-06-17`. Both products are normalized to `cm / 100 days` over co-located 1 km blocks (Eloy) or 300 m point windows (Mexico City).
- **LOS geometry:** NISAR L-band (`~37–43°` incidence) and Sentinel-1 C-band (`~39°` IW incidence) view angles differ slightly; for purely vertical subsidence, `LOS = V * cos(theta)`, introducing up to ~5–10% geometric scaling difference plus seasonal pumping variations between winter/spring and summer.
- **Houston/Katy:** No NISAR provisional/beta coverage in `data/global/` at check time (`OPERA F38239` spans `2025-09-23 → 2026-02-14`).
