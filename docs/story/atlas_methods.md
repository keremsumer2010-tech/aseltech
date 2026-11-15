# Global Subsidence Atlas: Methodology and Limitations

> **Calibration Notice:** NISAR L2 GUNW (`CRID P05023`) interferograms used in this atlas are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.

This document describes the standardized processing chain, validation criteria, and limitations governing the NISAR Vision Global Subsidence Atlas 2026.

---

## 1. Standardized Spatial Bounding Box

To ensure fair comparisons across disparate geologic settings, each region is evaluated over a uniform geographic footprint:
- **Footprint size:** Center coordinate $\pm 0.25^\circ$ latitude and longitude ($\approx 55 \times 55\text{ km}$, or $\approx 3{,}000\text{ km}^2$).
- **Boundary rule:** For coastal or estuarine sites (e.g., Jakarta, Delta), the center coordinate is adjusted inland to cover populated or agricultural land while holding the total box dimension constant at $0.50^\circ \times 0.50^\circ$.
- **Objective:** Prevents artificial inflation or suppression of regional subsidence that occurs when comparing small urban city centers against multi-county agricultural plains.

---

## 2. Headline Metric and Spatial Filtering

Spaceborne interferometric phase unwrapping can produce localized phase jumps or single-pixel phase noise:
- **Phase to displacement conversion:**
  $$\Delta d_{\text{LOS}} = -\frac{\lambda}{4\pi} \Delta \phi_{\text{unwrapped}}$$
  where $\lambda = 23.84\text{ cm}$ for NISAR L-band.
- **Headline value:** Calculated as the most negative 1 km block median displacement across the cumulative interferometric stack.
- **Percentile baseline ($p_2$):** The 2nd percentile of valid pixels is recorded alongside the 1 km block median in `summary.json`. This dual-metric threshold prevents single isolated pixels or unwrap artifacts from dictating the regional maximum.

---

## 3. Period-Independent Rate Metric (`rate_cm_per_100d`)

Interferometric stacks in the provisional release cover observation windows between 108 and 120 days across varying orbital geometries (June to October 2026):
- **Why annualized rates are not used for ranking:** Summer observation windows coincide with peak irrigation pumping in semi-arid agricultural basins (e.g., Central Valley, Konya Plain). Direct linear annualization ($d \times 365 / \text{days}$) misrepresents seasonal elastic drawdowns as permanent yearly subsidence.
- **Standardized metric:** All atlas rankings are ordered strictly by Line-of-Sight displacement normalized to a 100-day window:
  $$\text{rate}_{\text{cm\_per\_100d}} = \frac{d_{\text{LOS}}}{\text{days}} \times 100$$
- **Annual estimates:** Values expressed in cm/yr are reported strictly as secondary estimates (`rate_cm_per_yr_estimate`) and are omitted from official ranking criteria.

---

## 4. Off-Basin Bedrock Reference Placement and Sensitivity

InSAR displacement is inherently relative to a spatial reference point. Placing a reference within an active subsidence bowl subtracts true compaction, leading to significant underestimation:
- **Reference rule:** Primary references must be situated outside the unconsolidated sediment basin on exposed bedrock or documented stable ground.
- **Impact demonstrated:** In Mexico City, an initial in-basin reference produced $-4.4\text{ cm}$ LOS over 120 days. Re-referencing to the southwestern volcanic margin increased measured displacement to $-7.0\text{ cm}$ LOS, consistent with published literature. In Tehran and Beijing, in-basin references similarly suppressed signals until bedrock references were established.
- **Sensitivity testing:** Every region is evaluated against up to three distinct reference windows. The reference spread ratio is defined as:
  $$\text{Ratio}_{\text{ref}} = \frac{\max(d_{\text{ref}}) - \min(d_{\text{ref}})}{|d_{\text{headline}}|}$$
  A ratio $< 0.30$ indicates high reference stability.

---

## 5. Confidence Classification (§4 Quality Standard)

Regions are classified into two reporting tiers based on quantitative diagnostic thresholds:

| Classification | Valid Pixel Fraction | Reference Spread Ratio | Literature Concordance | Atlas Presentation |
|---|---|---|---|---|
| **Reliable** (`high` / `medium`) | $\ge 20\%$ (high if $\ge 40\%$) | $< 0.50$ (high if $< 0.30$) | Consistent within published order of magnitude | Ranked on main atlas board and press summaries |
| **Indicative Only** (`low`) | $< 20\%$ or monsoon atmospheric delay | $\ge 0.50$ or single reference | Discrepant due to short-window weather or baseline bias | Segregated to "Indicative Only" table with caveat badge |

### Environmental Caveats
- **Tropical and coastal decorrelation:** In Jakarta, dense tropical vegetation and urban structures reduce valid pixel coverage to $2.9\%$, precluding basin-wide spatial integration.
- **Monsoon atmospheric delay:** In Bangkok, wet tropospheric water vapor during June–October acquisitions inflates apparent short-term LOS change to $-7.5\text{ cm}$, roughly 7–10 times higher than modern multi-year InSAR rates. Such regions are categorized as `indicative only`.

---

## 6. Line-of-Sight to Vertical Conversion

NISAR measures ground displacement along the satellite's oblique Line-of-Sight (LOS) vector:
- **Vertical approximation:**
  $$d_{\text{vertical}} \approx \frac{d_{\text{LOS}}}{\cos \theta_{\text{inc}}}$$
  where nominal incidence angle $\theta_{\text{inc}} \approx 37^\circ$ ($\cos \theta_{\text{inc}} \approx 0.798$).
- **Limitation:** This projection assumes purely vertical motion. In proximity to deep extraction funnels, horizontal ground motion vectors (often 10%–30% of vertical displacement) contribute to the measured LOS phase, introducing projection errors if interpreted strictly as vertical compaction.

---

## 7. Pipeline Reproducibility

Every regional result in this atlas can be regenerated from raw ASF DAAC GUNW products using the open-source `pipeline.nisarpulse` tool:

```bash
# Sacramento–San Joaquin Delta (USA)
python -m pipeline.nisarpulse run --name delta --bbox -121.80,37.85,-121.35,38.25 \
  --ref-lonlat -121.75,37.95 --start 2026-06-17 --end 2026-10-15 --quality provisional

# Central Valley (USA)
python -m pipeline.nisarpulse run --name central_valley --center -119.0217,36.0112 \
  --box-deg 0.25 --ref-lonlat -118.80,36.00 --start 2026-06-28 --end 2026-10-14 --quality provisional

# Mexico City (Mexico)
python -m pipeline.nisarpulse run --name mexico_city --center -99.0362,19.2749 \
  --box-deg 0.25 --ref-lonlat -99.184,19.377 --start 2026-06-22 --end 2026-10-20 --quality provisional

# Isfahan (Iran)
python -m pipeline.nisarpulse run --name isfahan --center 51.67,32.65 \
  --box-deg 0.25 --ref-lonlat 51.589,32.355 --start 2026-06-18 --end 2026-10-16 --quality provisional

# Rafsanjan (Iran)
python -m pipeline.nisarpulse run --name rafsanjan --center 55.99,30.40 \
  --box-deg 0.25 --ref-lonlat 56.236,30.646 --start 2026-06-23 --end 2026-10-21 --quality provisional

# Bangkok (Thailand) [Indicative]
python -m pipeline.nisarpulse run --name bangkok --center 100.7374,13.8137 \
  --box-deg 0.25 --start 2026-06-21 --end 2026-10-19 --quality provisional

# Jakarta (Indonesia) [Indicative]
python -m pipeline.nisarpulse run --name jakarta --center 107.0115,-6.1406 \
  --box-deg 0.25 --ref-lonlat 106.911,-6.116 --start 2026-06-27 --end 2026-10-13 --quality provisional
```
