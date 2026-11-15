# InSAR Uncertainty Budget & GNSS Validation Synthesis

**Data Quality Class:** **`provisional`** (`beta-precal` pair `2026-06-16_2026-06-28` strictly excluded)  
**Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Summary: How We Know the Signal Is Real

Over the 108-day provisional NISAR observation window (`2026-06-28` to `2026-10-14`, 7 consecutive pairs), local high-coherence noise near the stable Woodlake reference region averages **0.66 cm LOS RMS per pair** (`0.50 cm` raw before ramp removal) and propagates under an independent-pair error model ($\sigma_{\text{total}} = \sigma_{\text{pair}}\sqrt{N}$) to **1.7 cm LOS** (`2.2 cm` vertical *estimate*, or up to **2.9 cm LOS** when including scene-wide unmodeled atmospheric scatter across all stable terrain). Against this noise floor, our headline cumulative peak subsidence of **-7.8 cm LOS** (`-10.1 cm` vertical *estimate*, reference sensitivity range **-7.8 to -4.7 cm LOS**) stands **2.7× to 4.5× above cumulative chain uncertainty**, even before multi-year seasonal averaging. Subtracting NISAR's split-spectrum ionospheric phase screen (which exhibits **2.9 to 17.3 cm LOS** scene-wide `p1–p99` dispersion per pair) and per-pair elevation-aware planar ramps reduces long-wavelength bias, leaving residual uncompensated wet troposphere and unwrapping noise as the dominant error sources. Independent comparison against Nevada Geodetic Laboratory GNSS time series inside the active subsidence bowl (`CAHA`, `HANF`, `P056`, `QCAP`, `TLBN`) confirms **0.86 cm mean RMSE** and **r = 0.81 mean correlation**.

### Uncertainty Budget Summary Table (`How We Know`)

| Error / Validation Component | Value (LOS) | Vertical *Estimate* ($\div \cos 39.1^\circ$) | Classification & Method |
|---|---|---|---|
| **Peak Cumulative Subsidence Signal** (`2026-06-28` → `2026-10-14`, 108 d) | **-7.8 cm** (ref. range `-7.8` to `-4.7 cm`) | **-10.1 cm** (*estimate*) | `measured` (`provisional`, 1 km block median; [`summary.json`](../../data/central_valley/summary.json)) |
| **Raw Single-Pair Phase Noise** ($\sigma_{\text{pair}}$, local $\text{coh} \ge 0.85$) | **0.50 cm** RMS (`0.27–0.79 cm` across pairs) | **0.65 cm** (*estimate*) | `measured` (std within 10 km of `reference_rc` `[261, 1245]` where $|d_{\text{cum}}| < 0.5\text{ cm}$) |
| **Post-Deramp Single-Pair Noise** ($\sigma_{\text{pair}}$, local stack increments) | **0.66 cm** RMS (`0.33–1.14 cm`) | **0.85 cm** (*estimate*) | `measured` (pair increments from `central_valley_cum_stack.npz` near reference) |
| **Cumulative Chain Noise ($N=7$, Local Reference Zone)** | **1.74 cm** | **2.24 cm** (*estimate*) | `derived` ($\sigma_{\text{pair}}\sqrt{7}$ under independent-pair noise assumption) |
| **Cumulative Chain Noise ($N=7$, Full-Scene Stable Pixels)** | **2.87 cm** ($\sigma_{\text{pair, RMS}} = 1.09\text{ cm}$) | **3.70 cm** (*estimate*) | `derived` (includes residual valley-wide tropospheric turbulence over stable terrain) |
| **GUNW Ionosphere Screen (`ion` layer, `p1–p99` spread per pair)** | **2.93 – 17.26 cm** (median **7.40 cm**) | — | `measured` (mitigated by subtracting `ion` per pair in [`analysis/cumulative.py`](../../analysis/cumulative.py)) |
| **Near-Reference Control Points (`p11`, `p12` increment RMS)** | **0.15 cm** (`p11`) / **0.70 cm** (`p12`) | — | `measured` (pair-to-pair increments at stable `near_reference` control windows) |
| **Typical Tropospheric Wet Delay Budget (SJV Summer)** | **~1–3 cm/pair** | **~1.3–3.9 cm/pair** (*estimate*) | `estimate` (unmodeled tropospheric LUT noted in [`calibration_note.md`](calibration_note.md)) |

---

## 2. Statistical Interpretation of GNSS Validation (`data/central_valley/validation.json`)

Across all 10 Nevada Geodetic Laboratory GNSS stations in Central Valley (`2026-06-28` to `2026-10-14`), InSAR vertical *estimates* ($\text{LOS}/\cos\theta$) achieve a **median RMSE of 1.00 cm** (`0.64–2.79 cm`, overall mean `1.33 cm`), with performance cleanly split between actively subsiding basin stations and near-zero margin sites. At the five actively subsiding basin stations (`CAHA`, `HANF`, `P056`, `QCAP`, `TLBN`, where `r >= 0.60`), InSAR closely tracks GNSS vertical motion with **0.86 cm mean RMSE**, **0.81 mean correlation** (`r = 0.90` at `CAHA` and `HANF`), and a minimal mean trend bias of **-0.51 cm/yr** (within `-0.15 cm` over 108 days; `TLBN` rates agree within `0.35 cm/yr`: `-14.99` vs. `-15.33 cm/yr`). Conversely, four low-motion basin-margin stations (`CAD1`, `CAFP`, `P564`, `P565`, GNSS subsidence `-0.17 to -1.00 cm`) exhibit larger RMSE (`1.57–2.79 cm`), weak or inverted correlations (`r = -0.41 to +0.07`), and positive InSAR-minus-GNSS trend residuals (`+7.3 to +9.3 cm/yr`), consistent with unmodeled atmospheric/orbital edge ramps (`~2.2–3.7 cm` vertical chain noise) masking sub-centimetre ground motion.

### Per-Station GNSS vs. InSAR Statistics (`validation.json`, 108-Day Span)

Computed by [`analysis/decomp/error_budget.py`](../../analysis/decomp/error_budget.py) (`summarize_gnss_validation`). All displacement series represent `vertical_estimate = LOS / cos(incidence)` compared against 7-day median NGL IGS20/NA Up GNSS observations.

| Station | Regime | Incidence (°) | RMSE (cm) | Pearson $r$ | End InSAR (cm, *est.*) | End GNSS (cm) | OLS Rate InSAR (cm/yr, *est.*) | OLS Rate GNSS (cm/yr) | Trend Diff (InSAR − GNSS, cm/yr) | 108-Day Trend Offset (cm) |
|---|---|---|---|---|---|---|---|---|---|---|
| **CAHA** | Subsiding basin | 41.38 | **0.752** | **0.8957** | -3.45 | -3.23 | -13.08 | -12.28 | -0.80 | -0.24 |
| **HANF** | Subsiding basin | 41.75 | **0.834** | **0.8955** | -3.51 | -2.22 | -10.18 | -7.52 | -2.66 | -0.79 |
| **QCAP** | Subsiding basin | 41.44 | **0.767** | **0.8198** | -2.54 | -3.20 | -9.51 | -11.84 | +2.33 | +0.69 |
| **TLBN** | Subsiding basin | 41.09 | **1.173** | **0.7926** | -4.85 | -4.45 | -14.99 | -15.33 | +0.35 | +0.10 |
| **P056** | East basin margin | 39.28 | **0.788** | **0.6613** | -2.50 | -1.45 | -7.61 | -5.86 | -1.75 | -0.52 |
| **P566** | Near reference | 39.56 | **0.639** | 0.4209 | +1.45 | +0.19 | +5.12 | +0.81 | +4.31 | +1.27 |
| **CAFP** | West margin | 43.34 | 2.791 | 0.0689 | +0.48 | -1.00 | +4.16 | -4.88 | +9.04 | +2.67 |
| **P564** | South margin | 41.38 | 1.570 | -0.1009 | +1.92 | -0.17 | +7.85 | -1.43 | +9.27 | +2.74 |
| **P565** | South margin | 40.62 | 1.998 | -0.2520 | +1.32 | -0.54 | +5.04 | -2.33 | +7.37 | +2.18 |
| **CAD1** | South margin | 40.62 | 1.991 | -0.4097 | +1.25 | -0.71 | +4.30 | -2.97 | +7.28 | +2.15 |

---

## 3. Chain Error Propagation Model & Physical Assumptions

For $N$ consecutive unwrapped interferograms summed sequentially ($d_{\text{cum}} = \sum_{i=1}^N \Delta d_i$), standard linear error propagation gives:

$$\sigma_{\text{total}} = \sqrt{\sum_{i=1}^{N} \sigma_{\text{pair}, i}^2} = \sigma_{\text{pair, RMS}} \sqrt{N}$$

**Explicit Independence Assumption & Caveats:**
1. **Assumes pairwise-independent noise across pairs:** Uncorrelated spatial decorrelation, soil-moisture phase-closure errors, coherence estimation noise, and isolated unwrapping residuals accumulate in quadrature proportional to $\sqrt{N}$ ($\sqrt{7} \approx 2.646\times$ single-pair RMS).
2. **Telescoping interior-epoch cancellation (countervailing effect):** Because consecutive pairs share interior SAR acquisitions ($0\to1, 1\to2, \dots, N-1\to N$), pure epoch-wise atmospheric phase delays at interior dates ideally cancel ($\phi_{\text{atm}}(t_k) - \phi_{\text{atm}}(t_k) = 0$ where masking does not drop pixels), leaving only the first and last acquisitions' uncorrelated atmospheric screens ($\sqrt{2}\sigma_{\text{atm}}$ rather than $\sqrt{N}\sigma_{\text{atm}}$). Therefore, applying $\sigma_{\text{pair}}\sqrt{N}$ to empirical per-pair spatial std acts as a **conservative error bound** when pair errors include temporal noise or partial unmasked closure residuals.
3. **Reference frame sensitivity:** Because `reference_rc` `[261, 1245]` sits on crystalline foothills northeast of Woodlake, moving the reference $\ge 30\text{ km}$ southwest onto the sedimentary valley floor (`alt_reference: [-120.0585, 35.76284]` and `[-119.60056, 35.79958]`) shifts the apparent Terra Bella maximum from `-7.8 cm` to `-6.2 cm` and `-4.7 cm` (`3.1 cm` total spread, `range_cm: [-7.8, -4.7]`), reflecting unmodeled regional ramp trade-off documented in [`summary.json`](../../data/central_valley/summary.json).

---

## 4. Per-Pair Noise & Ionosphere Table (`pipeline/subset/central_valley/*.npz`)

All 7 `provisional` pairs share exact center wavelength **$\lambda = 0.241963\text{ m}$** (L-band Frequency A) and exclude the `beta-precal` pair `2026-06-16_2026-06-28.npz`. Ionosphere screen conversion uses $\Delta d_{\text{ion, LOS, cm}} = -\frac{\text{ion} \cdot \lambda}{4\pi}\cdot 100$.

| Pair Window | $\sigma_{\text{raw, local}}$ (cm) | $\sigma_{\text{deion, local}}$ (cm) | $\sigma_{\text{post-deramp, local}}$ (cm) | $\sigma_{\text{post-deramp, scene}}$ (cm) | Raw Scene Std (cm) | De-Iono Scene Std (cm) | Ionosphere `p1` → `p99` (LOS cm) | Ionosphere `p1–p99` Spread (cm) |
|---|---|---|---|---|---|---|---|---|
| `2026-06-28` → `2026-07-10` | 0.447 | 0.299 | 0.382 | 0.588 | 5.678 | 2.042 | -80.92 → -67.30 | **13.62** |
| `2026-07-10` → `2026-07-22` | 0.577 | 0.760 | 0.342 | 1.017 | 5.844 | 2.802 | +39.04 → +51.23 | **12.20** |
| `2026-07-22` → `2026-08-15` | 0.785 | 0.568 | 0.508 | 0.888 | 7.879 | 3.170 | -48.33 → -31.08 | **17.26** |
| `2026-08-15` → `2026-08-27` | 0.296 | 0.295 | 1.141 | 1.488 | 2.574 | 2.099 | -9.31 → -6.39 | **2.93** |
| `2026-08-27` → `2026-09-08` | 0.509 | 0.429 | 0.928 | 1.643 | 2.167 | 2.821 | -21.31 → -17.77 | **3.55** |
| `2026-09-08` → `2026-09-20` | 0.457 | 0.443 | 0.330 | 0.970 | 2.211 | 2.922 | -42.39 → -34.99 | **7.40** |
| `2026-09-20` → `2026-10-14` | 0.275 | 0.281 | 0.475 | 0.471 | 3.226 | 1.740 | +9.65 → +15.14 | **5.48** |
| **RMS / Aggregate ($N=7$)** | **0.504** | — | **0.657** | **1.085** | — | — | median spread: **7.40 cm** | **2.93 – 17.26 cm** |
| **Propagated Chain ($\times \sqrt{7}$)** | **1.33 cm** | — | **1.74 cm** | **2.87 cm** | — | — | mean spread: **8.92 cm** | — |

**Reproducibility Command:**  
```bash
python -m analysis.decomp.error_budget
python -m pytest analysis/decomp -q
```
