# Judge FAQ

## 1. Why do you report motion along the satellite's line of sight?
Radar measures movement toward or away from the satellite most directly. Turning that into vertical movement requires an assumption about horizontal motion, so we label line-of-sight (LOS) values clearly.

## 2. Why compare the same 93 days?
The atlas uses the common window **2026-06-28 to 2026-09-29** so basin rates use the same part of the season. This improves comparability, though it does not make one summer a long-term trend.

## 3. How does the quality check work?
We screen each time series for sudden jumps that look like a radar phase error and review suspicious dates and reference areas. The review corrected Semarang's headline from −12.1 cm (−4.8 in) to −6.2 cm (−2.4 in); flagged basins stay indicative while under review.

## 4. Why is Konya marked indicative?
Its summer signal is stronger than the longer-term context supports, and the result depends on the reference and valid-pixel coverage. We keep it visible for transparency but leave it out of the reliable ranking.

## 5. How did you check the satellite measurements with GPS?
We compared NISAR with 10 continuous GPS stations in California's Central Valley. The agreement is **r = 0.924**, with **1.37 cm RMSE** at the final date.

## 6. What does “provisional” mean?
These are early NISAR products that have not completed the mission team's calibration and validation. The NISAR project (NASA-JPL and ISRO) performs those steps; our team does not.

## 7. Why is NASA's OPERA product not the headline comparison?
OPERA provides an independent shape check for Mexico City, but its comparison window is **2025-12-25 to 2026-03-25**, while NISAR covers **2026-06-22 to 2026-10-20**. Because the seasons differ, it is not a same-time validation.

## 8. How did you estimate the exposed population?
We overlaid the atlas movement screen on the **GHSL 2025** population grid and counted people where measured sinking exceeds **5 cm**. The global summary reports **369,770** people across the measured basins.

## 9. What does “permanent water storage loss” mean here?
It is the estimated aquifer storage loss associated with ground compaction that does not recover in the seasonal cycle. The current Central Valley estimate is **0.3174 km³ per year**; it is a model-based estimate, not a direct water-meter reading.

## 10. Can another team reproduce the results?
Yes: the code, input products, quality labels, and result files are open in the repository. The documented pipeline can be rerun for a selected basin, and its checks expose the inputs and assumptions.

## 11. What are the main limits?
The atlas covers one shared summer window and uses provisional products, so it cannot establish a long-term annual trend. Radar observes a slanted view, and horizontal movement or atmospheric noise can affect a vertical estimate.

## 12. How can a city use the atlas?
Use it to identify places that may deserve a closer look, then compare the signal with local survey, groundwater, and infrastructure records. It is a screening tool, not a safety rating or a substitute for local engineering review.
