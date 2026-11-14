# Game model parameters — "Valley Under Pressure" (`game/model.js`)

Owner of this file: PC3 (taken over from PC5, PC1 note 14:15). Code owner: PC6. Written 2026-11-14 14:35 TR.
Rule: every number has a source or is labelled **illustrative** (rules K-2). Status column:
**verified** = I read the value in the cited source (or a search result quoting it);
**partly** = source exists but the exact value in `model.js` is not confirmed;
**illustrative** = no source; game must show it as illustrative.

## 1. Measured target (NISAR, our own data)

| Quantity | Value | Unit | Source | Status |
|---|---|---|---|---|
| Max cumulative motion, Terra Bella N (p01) | −7.8 | cm LOS, 108 days | `data/central_valley/summary.json` (`max_subsidence_cm`) | verified |
| Range with 3 reference windows | −4.7 … −7.8 | cm LOS | `summary.json` `range_cm` (updated 15:00; the −4.7 end uses a valley-floor reference that may itself be sinking) | verified |
| Vertical estimate | −10.1 | cm | LOS / cos(39.1°), `summary.json` | verified (assumes purely vertical motion) |
| Window | 2026-06-28 → 2026-10-14 | 108 days | `summary.json` `period` | verified |
| p01 time series | 0, −0.84, −2.07, −3.0, −4.6, −3.35, −6.24, −7.8 | cm LOS | `data/central_valley/points.json` p01 | verified (matches `model.js` `nisarSeriesCm`) |

Note for the game text: the target is a **summer** (irrigation-season) value. Part of it is elastic and
recovers in winter, so 108 days × (365/108) is **not** a yearly rate.

## 2. Aquifer and compaction parameters

| Parameter (`model.js`) | Model value | Published value / range | Source | Status |
|---|---|---|---|---|
| Specific yield `S_y` | 0.12 | average **0.10** for San Joaquin Valley and Tulare Basin (Williamson et al., 1989, as cited) | Williamson, Prudic & Swain (1989) USGS PP 1401-D, cited in San Joaquin County doc: https://lfweb.sjgov.org/EHD/0/doc/728929/Page133.aspx ; CVHM: https://pubs.usgs.gov/publication/pp1766 | partly — 0.12 is plausible but above the cited average; suggest 0.10 or show "0.08–0.12" |
| Elastic skeletal specific storage `S_ske` | 1.0e-5 m⁻¹ | defined and estimated for San Joaquin Valley in Sneed (2001) OFR 01-35; exact m⁻¹ value **not read** (PDF returned 403) | https://pubs.usgs.gov/of/2001/of01-35/pdf/ofr0135.pdf | partly / not verified |
| Inelastic skeletal specific storage `S_skv` | 3.1e-4 m⁻¹ (= 31 × S_ske) | Sneed (2001): inelastic specific storage "generally is 20 to more" times larger than elastic (sentence truncated in the search result) | same as above | partly — ratio 31 is inside "≥ 20"; absolute value not verified |
| Clay (compressible) thickness `b0` | 76–82 m in districts | Corcoran Clay: **0–120 ft (0–37 m)** in Los Banos–Kettleman City area (USGS PP 497-E); **up to 200 ft (61 m)** (Page 1986, CVHM dataset) | https://pubs.usgs.gov/pp/0497e/report.pdf ; https://catalog-beta.data.gov/dataset/contours-of-corcoran-clay-thickness-in-feet-by-page-1986-for-the-central-valley-hydrologic | **mismatch if b0 means the Corcoran Clay alone** (76–82 m > 61 m). If b0 means the *aggregate* thickness of all fine-grained interbeds (as in CVHM's SUB package) it can be larger, but then the label in the game must say so. → PC6: rename to "total compressible clay interbeds (illustrative)" or cap at ≤ 61 m for "Corcoran Clay". |
| Baseline annual demand | 1.48 m/yr | — | none found | **illustrative** (already flagged in code) |
| Baseline annual recharge | 0.72 m/yr | — | none found | **illustrative** (already flagged in code) |
| Monthly pumping / recharge weights | 12 values | — | none found | **illustrative** — shape (summer pumping peak, winter recharge peak) is qualitatively right |
| Well depths, revenue per ha, irrigated area | district values | — | none | **illustrative** (code comment says so) |

Physics used in `model.js`: Terzaghi / USGS skeletal-storage compaction —
Δb = b0 · S_ske · Δh while head stays above the pre-consolidation head (recoverable, elastic);
Δb = b0 · S_skv · Δh for the part of the drawdown below it (permanent, inelastic), and the
pre-consolidation head then moves down. This is the standard formulation used in USGS subsidence
modelling (CVHM SUB package: https://catalog-beta.data.gov/dataset/critical-head-thickness-of-fine-grained-deposit-and-skeletal-elastic-storage-arrays-of-the).

## 3. Water-year types (California DWR, San Joaquin Valley index)

| Item | Value | Source | Status |
|---|---|---|---|
| Index formula | 0.6 × Apr–Jul runoff + 0.2 × Oct–Mar runoff + 0.2 × previous year's index (capped) | DWR / CDEC WSIHIST, as documented in https://rdrr.io/github/FlowWest/CDECRetrieve/man/water_year_indices.html | verified (secondary) |
| Thresholds | Wet ≥ 3.8 MAF; Above Normal 3.1–3.8 MAF; Below Normal / Dry / Critical cut-offs **not read** | same | partly |
| Class probabilities in `model.js` (W 0.30, AN 0.15, BN 0.17, D 0.18, C 0.20) | — | CDEC WSIHIST (https://cdec.water.ca.gov/reportapp/javareports?name=WSIHIST) could not be opened here (403) | **not verified → show as illustrative** until someone counts the WSIHIST table |
| Recharge multipliers / surface-water caps per class | 0.35–1.38 / 15–100 % | — | **illustrative** |

## 4. Canal damage examples

| Item | Value | Source | Status |
|---|---|---|---|
| Friant-Kern Canal capacity | design ~4,000 cfs → ~1,600 cfs in the worst reach (2017) | KVPR (2017): https://www.kvpr.org/environment/2017-08-03/friant-kern-canal-slows-by-60-percent-subsidence-to-blame | verified (news, quoting Friant Water Authority) |
| Deepest canal sinking | near Terra Bella | same; also our NISAR maximum (p01) is there | verified |
| Restoration project | Middle Reach Capacity Correction Project; 10-mile segment "lost more than 60 percent of its original capacity" | Friant Water Authority: https://friantwater.org/fkc-mrccp | verified (search result quote) |
| Delta-Mendota Canal | not checked in this pass | — | open |
| Risk thresholds 5 / 10 mm/km | aligned with `risk/compute_risk.py` | none in literature found | **illustrative** |

## 5. Calibration to NISAR

Target: baseline scenario (Below Normal year, 100 % pumping, 60 % surface allocation, 0 % fallow) at
district p01 must reproduce the NISAR 108-day value.

Scale factor (applied to the extraction stress, `CONFIG.calibration.extractionScaleFactor`):

    k = d_measured / d_model(k = 1)

with d_measured = −10.1 cm vertical (equivalently −7.8 cm LOS with cos 39.1° = 0.776), d_model = vertical
compaction the model produces over the same 108-day window (Jun 28 → Oct 14) with k = 1. Because elastic
and inelastic terms are linear in Δh, and Δh is linear in extraction for a fixed recharge, k is applied
once and the check is repeated; the game reports the result live (`ValleyModel.runCalibrationCheck`, box
"Calibration Verification" on the start screen) and passes if within ±10 %.

Current code: `extractionScaleFactor = 1.0`. I could not execute the JavaScript model here (no Node.js
on this machine), so **the numeric value of d_model(k = 1) is not reported in this file**. PC6: read the
value shown in the start-screen box, put k = −10.1 / d_model into `CONFIG`, and write both numbers here.
Uncertainty to carry into the game text: the target itself spans about −6.1 … −10.1 cm vertical
(−4.7 … −7.8 cm LOS, reference sensitivity with 3 reference windows; `summary.json` `range_cm`).

Wording suggestion for the game box: "Model check against NISAR" instead of "Calibration Verification",
so it is not confused with NISAR's own calibration (done by NASA-JPL / ISRO, rules §4).

## 6. What PC6 should change

1. `b0` label or value (Section 2): Corcoran Clay alone is ≤ ~61 m in USGS sources.
2. Water-year probabilities: mark `illustrative` until WSIHIST counts are filled in.
3. `S_y`: 0.10 (cited average) or show a range.
4. `S_ske`, `S_skv`: keep, but source line should say "order of magnitude, Sneed (2001) OFR 01-35; exact values not verified".
5. Fill in the calibration numbers (Section 5).
