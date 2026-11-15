# Independent check of the atlas top ranks

*Team Aseltech · 15 November 2026 · checked by PC1. NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

## Why this check

The atlas ranks regions by one number per region: the most negative ~1 km block in the cumulative line-of-sight (LOS) map, expressed per 100 days. A single number can hide a processing error. Before the ranking goes to the judges we tested every region three ways.

1. **Time series of the headline point.** We read the cumulative series behind each headline value (`points.json`, point `p01`) and flag two failure modes automatically (`tools/atlas_qc.py`):
   - a single step close to one full interferometric phase cycle. For NISAR L-band (wavelength 24.2 cm) one cycle is 12.1 cm of LOS motion; a jump of that size between two dates is the signature of a phase-unwrapping error;
   - two consecutive steps of opposite sign, each larger than 5 cm, that cancel. One acquisition is off (atmosphere or unwrapping) while the dates around it agree.
2. **Location.** Does the headline point sit where subsidence is documented, and is the reference point outside the subsiding basin?
3. **Published rates.** We compare with published InSAR or GNSS rates. Our windows cover 108 to 120 summer days, when groundwater pumping peaks, so a 100-day value scaled to a year overstates the annual net rate. We therefore compare orders of magnitude, not exact numbers. Vertical values are estimates (LOS / cos incidence).

Flagged regions keep their data in the atlas but move to **indicative only**, with the reason printed in their note. `build_atlas.py` now runs the check before every rebuild, and rank 1 is always a region that passed it.

## Results

| Atlas rank (new) | Region | Our value (LOS, window) | Vertical estimate | Published | Verdict |
|---|---|---|---|---|---|
| 1 | Konya Plain, Türkiye | −9.6 cm, 108 d | −12.1 cm | 1–4 cm/yr in the Konya sub-basin (GPS and DInSAR, Ustun et al. 2015); about 2 cm/yr at the city-centre GNSS station; above 7 cm/yr in the neighbouring Karapınar sub-basin (Sentinel-1, 2021) | **Keep, with caution.** The series accumulates smoothly (largest step −5.1 cm), so this is a real summer signal. Its size is several times the published annual rates, valid pixels cover only 11.6 % of the scene, and irrigated fields can add L-band soil-moisture phase. A full-year check is not possible yet: the NISAR beta archive for this frame ends on 16 January 2026 and provisional products start on 21–26 June 2026, leaving a gap of about five months (Feb–Jun 2026) with no interferograms over the Konya Plain (`data/konya_plain_fullyear/summary.json`). |
| 2 | Mashhad, Iran | −8.6 cm, 120 d | −11.3 cm | 14.6 cm/yr LOS and 19.1 cm/yr vertical maximum (Sentinel-1 PSInSAR 2014–2017, *Scientific Reports* 2020); 16–20 cm per year in 2015–2018 | **Consistent.** About 0.6 of a published year in one summer window. |
| 3 | Central Valley (Tulare Basin), USA | −7.8 cm, 108 d | −10.1 cm | 17.7–34.5 cm/yr peak rates in 2015–2017, up to 60 cm in the 2015–2016 drought (sources in `data/central_valley/validation_note.json`) | **Consistent.** Also cross-checked with GNSS and a second NISAR track elsewhere in this project. |
| 4 | Eloy, Arizona, USA | −8.0 cm, 120 d | −10.3 cm | The Arizona Department of Water Resources maps the Eloy sub-basin every year from Radarsat-2 (March 2025 to March 2026 map); Arizona maxima up to about 12 cm/yr in 2005–2014 | **Consistent in order of magnitude.** We did not read a peak value from the ADWR map, so we make no closer claim. |
| — | Semarang, Indonesia (was rank 1) | −12.1 cm, 108 d | — | Northern coastal Semarang: about 5 to more than 10 cm/yr; the southern half is stable (Arimoto et al. 2011; Aditiya and Ito 2023: 10–12 cm/yr in the north and east) | **Rejected as a headline.** The whole −12.1 cm comes from the last step (29 Sep → 11 Oct, −11.2 cm, one phase cycle). Without that step the point shows −0.9 cm. The point also lies in the stable southern uplands, not on the subsiding coast. Under revision (PC10 to re-process with that pair checked). |
| — | Bangkok, Thailand (was rank 5) | −7.5 cm, 108 d | — | About 0.9 cm/yr on average and locally above 2 cm/yr (Sentinel-1 PS-InSAR 2016–2019); 1–3 cm/yr in 2005–2010 InSAR | **Indicative only.** Roughly ten times the published rate, and the series has ±4–5 cm steps in both directions, typical of tropical decorrelation. |
| — | Delhi, India | −4.3 cm | — | — | **Indicative only.** One acquisition (1 Sep) is off: −10.0 cm, then +8.1 cm. |
| — | Beijing, China | −1.4 cm | — | — | **Indicative only.** One acquisition (11 Jul) is off: −8.3 cm, then +7.0 cm. A full-box re-run with an off-basin reference is in progress (PC11). |

## What this changes

- The ranking now starts with eight regions that passed all checks: Konya Plain, Mashhad, Central Valley, Eloy, Mexico City, Rafsanjan, Quetta and the Sacramento–San Joaquin Delta. The fastest-sinking reliable place is the Konya Plain (−8.9 cm per 100 days, LOS), with the caution above.
- Tehran stays indicative for now because of its low valid-pixel fraction (38 %); its re-computed value with an off-basin reference is −7.4 cm LOS (the earlier −3.5 cm used a reference inside the subsiding area).
- Any new region is checked automatically before it enters the ranking.

## Limits of this check

It tests only the headline point of each region, not every pixel. It cannot detect an error that grows slowly over many dates. The literature comparison is an order-of-magnitude test across different years and sensors. A full validation needs GNSS in each basin and the year-round NISAR record, which the NISAR project will provide.

## Sources

- Mashhad: [Extreme subsidence in a populated city (Mashhad) detected by PSInSAR, *Scientific Reports* (2020)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7347893/)
- Konya: [Land subsidence in Konya Closed Basin and its spatio-temporal detection by GPS and DInSAR, *Environmental Earth Sciences* (2015), doi:10.1007/s12665-014-3890-5](https://acikerisim.selcuk.edu.tr/items/b95e6ec3-ac56-4e92-b527-ed8a6811c758); [Karapınar multi-sensor study, *Sensors* (2021)](https://mdpi.com/1424-8220/21/3/774)
- Eloy: [ADWR, Total land subsidence in the Eloy sub-basin, March 2025 – March 2026](https://www.azwater.gov/sites/default/files/2026-05/PicachoArea03-2025to03-2026_8x11.pdf); [*Hydrogeology Journal* (2015), doi:10.1007/s10040-015-1329-z](https://springerlink.bibliotecabuap.elogim.com/doi/10.1007/s10040-015-1329-z)
- Semarang: [Arimoto et al., JpGU 2011](https://www2.jpgu.org/meeting/2011/yokou/STT057-P01_E.pdf); [Aditiya and Ito, *Int. J. Applied Earth Observation and Geoinformation* (2023)](https://doaj.org/article/bc659cefcb624b38a679829477d8e2d1)
- Bangkok: [Sentinel-1 PS-InSAR 2016–2019, Burapha University](https://digital_collect.lib.buu.ac.th/dcms/files/61910094.pdf); [InSAR time series for Bangkok, Chulalongkorn University (2012)](https://doi.nrct.go.th/ListDoi/listDetail/10.14457%2FCU.the.2012.918)
- Method and code: `tools/atlas_qc.py`, `tools/test_atlas_qc.py`, `data/global/qc_flags.json`, `data/global/qc_manual.json`
