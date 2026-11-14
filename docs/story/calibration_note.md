# NISAR Calibration & Data Maturity Note

**Mandatory Attribution:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. ASF / NASA-JPL / ISRO Maturity Tiers

According to the Alaska Satellite Facility (ASF) NISAR Data User Guide ([Products Overview](https://nisar-docs.asf.alaska.edu/products-overview/)), distributed L-band products fall into three distinct processing-maturity stages that must not be blindly mixed in quantitative analyses:

| Maturity Tier | Acquisition Window | Release & CRID | Calibration Status | Our Project Policy (`VERI_SOZLESMESI.md` §3) |
|---|---|---|---|---|
| **BETA (Pre-Calibration)** | Early mission acquisitions **before `2026-06-17`** | Released **Jan / Feb 2026** (e.g., `NISAR_L2_*_BETA_*`) | **Not fully calibrated.** Known valid-data mask misalignment, cross-track antenna pattern radiometric banding, and parallel streaks in low-backscatter scenes ([Pre-Calibration Known Issues](https://nisar-docs.asf.alaska.edu/product-known-issues/)). | Labeled **`beta-precal`**. Excluded from quantitative displacement maps and cross-date time series; if ever shown, display strictly as exploratory imagery with explicit warning. |
| **PROVISIONAL** | **`2026-06-17`** through part of **`2026-10-23`** | Released **July 20, 2026** (`CRID P05023`, e.g., `NISAR_L2_GCOV_PROVISIONAL_V1`) | **Calibrated & partially validated** at a limited set of global cal/val sites. Known caveats: high-latitude ionospheric residuals/geolocation offsets, RFI filter under/over-suppression, low-level SLC edge ripples, and Frequency B (5 MHz) calibration residuals ([Provisional Known Issues](https://nisar-docs.asf.alaska.edu/provisional-known-issues/)). | Labeled **`provisional`**. Permitted for our Level-2 GUNW interferometric displacement pipeline (`> 2026-06-17`, single coherent processing baseline) with uncertainty and un-applied ionospheric/tropospheric caveat documented. |
| **VALIDATED** | **`2026-10-21` onward** | Released **November 6, 2026** for Level 0–2 products (e.g., `NISAR_L2_GCOV_V1`, observed on recent ASF granules with `CRID P05036`) | **Fully calibrated and validated**; collection name drops the maturity suffix. | Labeled **`validated`**. Not mixed across reprocessing boundaries with Provisional scenes unless explicitly documented and baseline-checked. |

---

## 2. Specific Technical Caveats for Our Project Outputs

1. **Unapplied Phase Correction Layers in GUNW (`>= 2026-06-17`):**  
   Per the [ASF GUNW Product Guide](https://nisar-docs.asf.alaska.edu/gunw), L2 GUNW products store a Frequency A split-spectrum **ionospheric phase screen** plus external lookup tables for **solid Earth tides** and **tropospheric delays**, **none of which are removed from `unwrappedPhase` by default**. Single 12-day interferograms therefore can contain broad ionospheric or atmospheric ramps alongside ground deformation; cumulative stacking, spatial deramping, and coherence/connected-component masking are required and flagged in product `notes`.

2. **Preview Imagery Policy (`data/uk/`):**  
   Browse PNG files distributed via ASF datapool (`*_LATLON.png`, such as `NISAR_L2_PR_GCOV_..._P05023_..._LATLON.png` on `2026-10-20` in `data/uk/meta.json`) are intended for rapid visual inspection of radar geometry and cloud-free imaging—**not calibrated radiometric backscatter (`dB`/`gamma0`)**. In our schema they always carry `quality: "preview"` and are never used to derive quantitative subsidence numbers.

3. **Scientific Provenance Statement:**  
   All NISAR orbital calibration, radiometric/polarimetric tuning, and geophysical validation campaigns are performed by the **NISAR project teams at NASA-JPL and ISRO** ([NASA Science Mission Page](https://science.nasa.gov/mission/nisar/)). Any derived metrics or visualizations in this repository reflect standard L2 product post-processing (masking, referencing, phase-to-LOS displacement conversion using per-file `centerFrequency`) subject to ASF/JPL provisional product caveats.
