# Karapınar Sinkhole (*Obruk*) Chronology & Groundwater Drivers (`docs/story/sinkhole_timeline.md`)

> **Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.* All field coordinates, dimensions, and formation years below match [data/karapinar/sinkholes.geojson](../../data/karapinar/sinkholes.geojson) and peer-reviewed primary tables verbatim (`rules/RULES.md` K-2).

---

## 1. Executive Summary

Across Konya Province (central Türkiye), peer-reviewed field inventories record **104 documented sinkholes** (**61 historical** and **43 formed between 1972 and 2014**; **86 located in Karapınar district alone**) triggered by subsurface carbonate dissolution accelerated by multi-decadal agricultural groundwater extraction ([Tapur & Bozyiğit, 2015](https://dergipark.org.tr/tr/download/article-file/3454); [Tapur & Bozyiğit, 2016](https://dergipark.org.tr/tr/download/article-file/227372)).

Filtering strictly to GPS-verified collapses inside the NISAR Karapınar radar frame **`[33.3, 37.6, 33.8, 37.9]`** preserves **29 sinkholes** spanning **`1972` to `2013`**:
- **Accelerated clustering:** **`24` of `29` (`82.8%`)** verified frame sinkholes opened within just **7 years (`2007–2013`)**, compared with only **5** documented inside this bounding box across the preceding **35 years (`1972–2006`)**.
- **Peak drought surge (`2007–2009` & `2010–2013`):** Both windows record **12** collapses each (`4` per year in `2007`, `2008`, `2009`; `5` in `2011`; `4` in `2012`), matching reported groundwater declines over recent **30-year** pumping cycles.
- **Depth & water-table regime:** Only **3** deep collapses reach standing groundwater today (`Akviran Obruğu` **80.0 m**, `1977`; `Yavşançukuru Obruğu` **56.0 m**, `2000`; `Yarımoğlu Obruğu` **76.0 m**, `2009`), whereas **24** are **dry** (`0.5–70.0 m` depth) and **2** have been **filled** (`Akkuyu Obruğu-II`, `Seyithacı Yaylası Obruğu-VIII`). *(Excluded per K-2: `Küpbasan Yeni Obruk-I` due to a typographical `37° 43' 99"` coordinate in Table 1.)*

---

## 2. Temporal Distribution Inside `[33.3, 37.6, 33.8, 37.9]`

| Formation Window | Count (`n = 29`) | Share of Subset | Status Split | Deepest Recorded Collapse (`m`) |
|---|---|---|---|---|
| `1972–1999` (`28` yr) | `3` | `10.3%` | `2` dry, `1` water-bearing | `Akviran Obruğu` (`80.0 m`, `1977`); `Nebili Obruğu-II` (`70.0 m`, `1972`) |
| `2000–2006` (`7` yr) | `2` | `6.9%` | `1` dry, `1` water-bearing | `Yavşançukuru Obruğu` (`56.0 m`, `2000`) |
| `2007–2009` (`3` yr drought cluster) | `12` | `41.4%` | `9` dry, `1` water-bearing, `2` filled | `Yarımoğlu Obruğu` (`76.0 m`, `2009`) |
| `2010–2013` (`4` yr sustained cluster) | `12` | `41.4%` | `12` dry | `Küçükkarakuyu Aşıroğlu Obruğu-III` (`8.0 m`, `2012`) |

---

## 3. Hydrogeological Drivers & Connection to NISAR L2 GUNW Measurements

1. **Pumping, Pore-Pressure Loss & Void Unroofing:** Heavy agricultural irrigation across the closed Konya–Karapınar sub-basin draws groundwater along regional karstic flow paths toward Tuz Gölü. Tapur & Bozyiğit (2016) note **30-year groundwater drops** directly mirrored by a **10 m water-level decline** in historic **Kızören Obruğu** (measured at **145 m** depth in `1992`). As water tables fall inside fractured Neogene carbonate rocks, buoyant support disappears and overburden cover arches collapse suddenly along clusters such as **Seyithacı** (`9` collapses, `2007–2012`), **Akkuyu** (`4` collapses plus `Yarımoğlu`, `2007–2012`), and **Karakuyu / Köken** (`8` collapses, `2010–2013`).
2. **Contemporary Basin Subsidence Measured by NISAR (`quality: provisional`):** From **`2026-06-26` to `2026-10-12`** (`108` summer irrigation days, **`8` consecutive Track 7 descending GUNW pairs**, `CRID P05023`), `data/karapinar/summary.json` detects cumulative Line-of-Sight subsidence reaching **`−5.9 cm` LOS** (`~−8.0 cm` vertical estimate at `42.0°` incidence; linear summer rate estimate `−20.0 cm/yr`) centered at **`2 km W of Karapınar`** (`33.53056°E, 37.71818°N`).
3. **Spatial Offset & Scientific Caution:** Mapped frame sinkholes lie **`5.9 km`** (`Yavşançukuru Obruğu`, `2000`) to **`21.7 km`** (`Akviran Obruğu`, `1977`) from the summer LOS peak, with dense `2009–2013` Karakuyu/Eşeli collapses clustered **`6.7–7.5 km`** to the north. Consistent with NASA/ASF guidelines and our scientific honesty standard, **NISAR L-band interferometry maps regional multi-pixel ground settling linked to groundwater overdraft rather than forecasting the exact date or micro-location of catastrophic roof collapse.**

---

## 4. Verified Primary Sources (HTTP 200)

- **Tapur & Bozyiğit (2015)**, *"Konya İlinde Güncel Obruk Oluşumları"*, *Marmara Coğrafya Dergisi* 31:415–446 — [Article PDF](https://dergipark.org.tr/tr/download/article-file/3454): Primary GPS coordinates, formation years (`1972–2014`), depths, diameters, and status for all `29` features in `data/karapinar/sinkholes.geojson` (`İnoba Obruğu` `42 m` depth in `2008` also prompted `7` families to relocate).
- **Tapur & Bozyiğit (2016)**, *"Konya İli Obruklarının Turizm Potansiyeli"*, *Marmara Coğrafya Dergisi* 34:253–267 — [Article PDF](https://dergipark.org.tr/tr/download/article-file/227372): Karapınar total (`86` of `104`), **30-year groundwater drawdown**, and lake-level drops (`Kızören`, `Meyil`, `Çıralı` obruks).

---

## 5. Complete Chronological Catalogue (`29` Verified Features)

| # | Year | Name | Lon (`°E`) | Lat (`°N`) | Diameter (`m`) | Depth (`m`) | Status |
|---:|---:|---|---:|---:|---:|---:|---|
| 1 | `1972` | Nebili Obruğu-II (Naciye Aba Obruğu) | `33.53278` | `37.80889` | `18x16` | `70.0` | `dry` |
| 2 | `1977` | Akviran Obruğu (Güvercin Obruğu) | `33.42500` | `37.89444` | `24` | `80.0` | `water-bearing` |
| 3 | `1983` | Sekizli Küçük Obruk | `33.46806` | `37.87667` | `16` | `3.5` | `dry` |
| 4 | `2000` | Yavşançukuru Obruğu | `33.47611` | `37.74861` | `21` | `56.0` | `water-bearing` |
| 5 | `2003` | Hanyıkığı Obruğu | `33.46889` | `37.79444` | `7.7x5.6` | `6.0` | `dry` |
| 6 | `2007` | Akkuyu Obruğu-I | `33.36806` | `37.74500` | `19x17` | `2.5` | `dry` |
| 7 | `2007` | Seyithacı Obruğu-I | `33.58083` | `37.81528` | `15x12` | `1.0` | `dry` |
| 8 | `2007` | Seyithacı Obruğu-II | `33.57500` | `37.80944` | `16x13` | `3.0` | `dry` |
| 9 | `2007` | Seyithacı Obruğu-III | `33.57611` | `37.81361` | `25x22` | `4.0` | `dry` |
| 10 | `2008` | Akkuyu Obruğu-II | `33.38361` | `37.73111` | `16` | `1.0` | `filled` |
| 11 | `2008` | Seyithacı Obruğu-IV | `33.58111` | `37.81583` | `17x15` | `2.0` | `dry` |
| 12 | `2008` | Seyithacı Obruğu-V | `33.58111` | `37.81500` | `14x12` | `4.0` | `dry` |
| 13 | `2008` | Seyithacı Obruğu-VI | `33.57389` | `37.80500` | `6` | `6.0` | `dry` |
| 14 | `2009` | Eşeli Obruğu | `33.51306` | `37.77667` | `18` | `1.5` | `dry` |
| 15 | `2009` | Seyithacı Obruğu-VII (Hüseyin İvriz) | `33.56667` | `37.80250` | `13` | `5.0` | `dry` |
| 16 | `2009` | Seyithacı Yaylası Obruğu-VIII | `33.57889` | `37.81583` | `3` | `2.0` | `filled` |
| 17 | `2009` | Yarımoğlu Obruğu (Akkuyu-III) | `33.36556` | `37.74833` | `28` | `76.0` | `water-bearing` |
| 18 | `2010` | Akkuyu Obruğu-IV | `33.35750` | `37.72556` | `16` | `1.0` | `dry` |
| 19 | `2010` | Küçükkarakuyu Aşıroğlu Obruğu-I | `33.55361` | `37.78306` | `19` | `4.0` | `dry` |
| 20 | `2011` | Büyükkarakuyu Koçhan Obruğu | `33.53583` | `37.78583` | `14` | `2.0` | `dry` |
| 21 | `2011` | Büyükkarakuyu Şenyurt Obruğu | `33.53944` | `37.78806` | `15` | `2.5` | `dry` |
| 22 | `2011` | Köken Obruğu-I | `33.56139` | `37.78806` | `10` | `1.0` | `dry` |
| 23 | `2011` | Köken Obruğu-II | `33.56278` | `37.78833` | `16` | `1.0` | `dry` |
| 24 | `2011` | Küçükkarakuyu Aşıroğlu Obruğu-II | `33.55389` | `37.78750` | `20` | `2.0` | `dry` |
| 25 | `2012` | Akkuyu Obruğu-V | `33.36167` | `37.73750` | `15` | `0.7` | `dry` |
| 26 | `2012` | Büyükkarakuyu Direkli Obruk | `33.54417` | `37.77778` | `25` | `1.0` | `dry` |
| 27 | `2012` | Küçükkarakuyu Aşıroğlu Obruğu-III | `33.55417` | `37.78639` | `16` | `8.0` | `dry` |
| 28 | `2012` | Seyithacı Obruğu-IX | `33.57028` | `37.80722` | `16` | `0.5` | `dry` |
| 29 | `2013` | Köken Obruğu-III | `33.55750` | `37.78306` | `18` | `0.5` | `dry` |
