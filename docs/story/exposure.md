# Population and Crop / Land-Cover Exposure in Subsiding Zones (`docs/story/exposure.md`)

**Owner:** PC8 (`M3hmeT1888`) · **Target:** Website Story / Science Integration (`PC3` `tasks/PC3.md` §16:15 item 6 — Challenge Alignment **B3**)  
**Data Quality Class:** `provisional` (`CRID P05023`, `28 Jun – 14 Oct 2026` Central Valley; `26 Jun – 12 Oct 2026` Karapınar)  
**Calibration Notice:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Plain-English Web Copy (4 Sentences, `docs/REVIEW_1500.md` Compliant)

### Orchards, Grain Fields, and 83,000 Residents Sit Inside the 2026 Summer Subsidence Bowls

Combining our 108-day provisional NISAR line-of-sight (`LOS`) displacement maps (`28 Jun – 14 Oct 2026` in California; `26 Jun – 12 Oct 2026` in Türkiye) with **WorldPop 100 m gridded population counts (2020)** shows that an *estimated* **`71,701` residents in California's Central Valley** (`78,464` with `<= 2.5 km` rural basin interpolation; `124,561` on vertical *estimates*) and **`11,572` residents in Karapınar, Konya** (`18,906` with basin interpolation) live on land that sank more than **`2 cm` LOS** in a single summer. Within the deepest **`> 5 cm` LOS** subsidence cores (`239.8 km²` in California and `3.1 km²` common-valid area in Karapınar), **`3,407` Central Valley residents** (`4,270` interpolated) and **`2,214` Karapınar residents** (`3,481` interpolated) are directly exposed to rapid ground settlement along rural towns and farmsteads. Overlaying the **30 m USDA Cropland Data Layer (2021)** in California reveals that **`79.2%` (`1,251.4 km²`)** of the **`1,579.2 km²`** zone subsiding more than `2 cm` LOS—and **`91.2%` (`218.7 km²`)** of the **`> 5 cm` LOS** zone—is active cultivated farmland, led by high-value perennial **citrus (`355.6 km²`)**, **pistachios (`230.9 km²`)**, **fallow or idle cropland (`216.1 km²`)**, **winter wheat (`97.3 km²`)**, and **almonds (`73.7 km²`)** (`grapes` `49.9 km²`, `pomegranates` `37.0 km²`, `alfalfa` `24.6 km²`). Over **Karapınar**, **ESA WorldCover 10 m (2021)** shows that coherent pixels sinking more than `2 cm` LOS (`28.7 km²`) span **semi-arid grassland (`16.54 km²`, `57.7%`)**, **built-up town and village fabric (`7.24 km²`, `25.2%`)**, **bare or sparse karst terrain (`3.92 km²`, `13.7%`)**, **tree cover (`0.57 km²`, `2.0%`)**, and **cropland (`0.42 km²`, `1.4%` coherent; rising to `24.99 km²` across the `141.1 km²` interpolated basin where irrigated center-pivot fields lose L-band coherence during summer growth)**.

---

## 2. Source & License Attribution Line (Required by `tasks/PC8.md` B3)

- **Population Data:** WorldPop Open Population Repository (`WorldPop_Total_Population_100m`, `2020` UN-adjusted 100 m / 3 arc-second gridded population counts, University of Southampton, DOI: [10.5258/SOTON/WP00645](https://doi.org/10.5258/SOTON/WP00645)) — **License: CC BY 4.0**.
- **California Crop Data:** USDA National Agricultural Statistics Service (`NASS`) Cropland Data Layer (`CDL`, `2021`, `30 m` resolution, accessed via [CropScape / Microsoft Planetary Computer STAC](https://www.nass.usda.gov/Research_and_Science/Cropland/SARS1a.php)) — **License: U.S. Public Domain (`17 USC § 105`)**.
- **Türkiye Land-Cover Data:** European Space Agency (`ESA`) WorldCover `10 m` `2021 v200` (Sentinel-1 and Sentinel-2 global land cover, Zanaga et al. 2022, DOI: [10.5281/zenodo.7254221](https://doi.org/10.5281/zenodo.7254221)) — **License: CC BY 4.0**.

---

## 3. Figure & Caption (`docs/REVIEW_1500.md` Format)

![Crop, Land-Cover, and Population Exposure in Central Valley and Karapinar Subsiding Zones](media/pc8_exposure.png)

**Figure 5.** **Agricultural crop, land-cover, and population exposure inside summer 2026 NISAR subsidence zones (`> 2 cm` and `> 5 cm` LOS).** **A.** Top five cultivated crop types (`km²`) inside the California Central Valley common-valid subsidence footprint (`28 Jun – 14 Oct 2026`, `7` provisional pairs, `1,579.2 km²` with `> 2 cm` LOS sinking in blue and `239.8 km²` with `> 5 cm` LOS sinking in red), derived from the 30 m USDA NASS Cropland Data Layer (`2021`). Callout box lists estimated exposed population from WorldPop 100 m (`2020`). **B.** Top five land-cover classes (`km²`) inside the Karapınar, Türkiye common-valid subsidence footprint (`26 Jun – 12 Oct 2026`, `8` provisional pairs, `28.7 km²` with `> 2 cm` LOS sinking in green and `3.1 km²` with `> 5 cm` LOS sinking in orange), derived from ESA WorldCover 10 m (`2021 v200`). *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.* Data: NASA-ISRO NISAR L2 GUNW (ASF DAAC), WorldPop 100 m (CC BY 4.0), USDA CDL 30 m (Public Domain), ESA WorldCover 10 m (CC BY 4.0). Analysis: Team Taykut.

---

## 4. Summary Tables (`data/central_valley/exposure.json` & `data/karapinar/exposure.json`)

### 4.1 Population Exposure (`WorldPop 100 m`, `2020`, `estimate`)

| Site & Bounding Box | Total BBox Population | Population on Valid InSAR Pixels | **`> 2 cm` LOS (Valid Pixels)** | **`> 5 cm` LOS (Valid Pixels)** | `> 2 cm` LOS (`<= 2.5 km` Basin Interp.) | `> 5 cm` LOS (`<= 2.5 km` Basin Interp.) | `> 2 cm` Vertical *Estimate* (Valid Pixels) | `> 5 cm` Vertical *Estimate* (Valid Pixels) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Central Valley, CA** (`[-120.2, 35.6, -119.0, 36.6]`) | `613,429` | `578,449` | **`71,701`** | **`3,407`** | `78,464` | `4,270` | `124,561` | `7,067` |
| **Karapınar, Konya** (`[33.3, 37.6, 33.8, 37.9]`) | `47,621` | `18,114` | **`11,572`** | **`2,214`** | `18,906` | `3,481` | `13,618` | `4,179` |
| **Combined Two-Basin Total** | `661,050` | `596,563` | **`83,273`** | **`5,621`** | **`97,370`** | **`7,751`** | **`138,179`** | **`11,246`** |

### 4.2 Central Valley Top Cultivated Crops in Subsiding Zones (`USDA CDL 30 m`, `2021`)

| Rank | CDL Code | Crop / Land-Cover Name | Area in `> 2 cm` LOS (`km²`) | Share of `> 2 cm` Zone (`%`) | Area in `> 5 cm` LOS (`km²`) | Share of `> 5 cm` Zone (`%`) |
|---:|---:|---|---:|---:|---:|---:|
| **1** | `72` | **Citrus** | **`355.64`** | `22.5%` | **`166.59`** | `69.5%` |
| **2** | `204` | **Pistachios** | **`230.92`** | `14.6%` | **`7.78`** | `3.2%` |
| **3** | `61` | **Fallow / Idle Cropland** | **`216.14`** | `13.7%` | **`10.00`** | `4.2%` |
| **4** | `24` | **Winter Wheat** | **`97.27`** | `6.2%` | **`5.52`** | `2.3%` |
| **5** | `75` | **Almonds** | **`73.74`** | `4.7%` | **`4.71`** | `2.0%` |
| 6 | `69` | Grapes | `49.88` | `3.2%` | `2.46` | `1.0%` |
| 7 | `217` | Pomegranates | `36.95` | `2.3%` | `2.85` | `1.2%` |
| 8 | `36` | Alfalfa | `24.56` | `1.6%` | `1.10` | `0.5%` |
| 9 | `21` | Barley | `20.46` | `1.3%` | `1.16` | `0.5%` |
| 10 | `211` | Olives | `15.79` | `1.0%` | `3.79` | `1.6%` |
| — | `176` | *Grassland / Pasture (non-cultivated)* | `146.19` | `9.3%` | `5.32` | `2.2%` |
| — | — | **All Cultivated Cropland Combined** | **`1,251.37`** | **`79.2%`** | **`218.67`** | **`91.2%`** |

### 4.3 Karapınar Land Cover in Subsiding Zones (`ESA WorldCover 10 m v200`, `2021`)

| Rank | WorldCover Code | Land-Cover Class | Coherent `> 2 cm` LOS (`km²`) | Share (`%`) | Coherent `> 5 cm` LOS (`km²`) | Share (`%`) | Basin-Interpolated `> 2 cm` LOS (`km²`) | Basin Share (`%`) |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| **1** | `30` | **Grassland** | **`16.54`** | `57.7%` | **`1.15`** | `36.9%` | `58.79` | `41.7%` |
| **2** | `50` | **Built-up (settlements & roads)** | **`7.24`** | `25.2%` | **`1.34`** | `43.3%` | `8.65` | `6.1%` |
| **3** | `60` | **Bare / sparse vegetation** | **`3.92`** | `13.7%` | **`0.43`** | `13.8%` | `47.46` | `33.6%` |
| **4** | `10` | **Tree cover** | **`0.57`** | `2.0%` | **`0.10`** | `3.3%` | `0.67` | `0.5%` |
| **5** | `40` | **Cropland (irrigated & rainfed)** | **`0.42`** | `1.4%` | **`0.08`** | `2.7%` | **`24.99`** | **`17.7%`** |
| — | — | **Total Subsiding Footprint** | **`28.69`** | `100.0%` | **`3.10`** | `100.0%` | **`141.08`** | `100.0%` |

---

## 5. Ready-to-Paste HTML Snippet for PC3 (`web/index.html` or `web/science.html`)

```html
<div class="callout exposure-box" id="exposureBox">
  <h3>Who and What Are on Sinking Ground? (Population &amp; Crop Exposure)</h3>
  <p>
    Combining our 108-day provisional NISAR line-of-sight (<code>LOS</code>) displacement maps with
    <strong>WorldPop 100 m gridded population counts (2020)</strong> shows that an <em>estimated</em>
    <strong>71,701 residents in California's Central Valley</strong> (78,464 with &le; 2.5 km rural basin interpolation) and
    <strong>11,572 residents in Karap&#305;nar, Konya</strong> (18,906 with basin interpolation) live on land that sank more than
    <strong>2 cm LOS</strong> during summer 2026, including <strong>3,407 Central Valley</strong> and
    <strong>2,214 Karap&#305;nar residents</strong> inside the deepest <strong>&gt; 5 cm LOS</strong> subsidence bowls.
    Overlaying the <strong>30 m USDA Cropland Data Layer (2021)</strong> in California shows that
    <strong>79.2% (1,251.4 km&sup2;)</strong> of the <strong>1,579.2 km&sup2;</strong> zone subsiding more than 2 cm LOS is active
    cultivated farmland, led by <strong>citrus (355.6 km&sup2;)</strong>, <strong>pistachios (230.9 km&sup2;)</strong>,
    <strong>fallow or idle cropland (216.1 km&sup2;)</strong>, <strong>winter wheat (97.3 km&sup2;)</strong>, and
    <strong>almonds (73.7 km&sup2;)</strong>.
    In <strong>Karap&#305;nar</strong>, <strong>ESA WorldCover 10 m (2021)</strong> shows that coherent pixels sinking more than
    2 cm LOS (28.7 km&sup2;) span <strong>grassland (16.54 km&sup2;, 57.7%)</strong>, <strong>built-up town and village fabric
    (7.24 km&sup2;, 25.2%)</strong>, <strong>bare karst terrain (3.92 km&sup2;, 13.7%)</strong>, <strong>tree cover
    (0.57 km&sup2;, 2.0%)</strong>, and <strong>cropland (0.42 km&sup2; coherent; 24.99 km&sup2; across the 141.1 km&sup2;
    interpolated basin)</strong>.
  </p>
  <figure class="story-media">
    <img src="../docs/story/media/pc8_exposure.png"
         alt="Horizontal bar charts of top 5 cultivated crops in Central Valley and top 5 land-cover classes in Karapinar inside > 2 cm and > 5 cm LOS subsidence zones, with WorldPop 100 m population callouts."
         loading="lazy" width="1280" height="540">
    <figcaption>
      <strong>Figure 5.</strong> Crop, land-cover, and human population exposure inside summer 2026 NISAR subsidence zones (&gt; 2 cm and &gt; 5 cm LOS).
      Data: NASA-ISRO NISAR L2 GUNW (provisional, CRID P05023), WorldPop 100 m (2020, CC BY 4.0), USDA NASS Cropland Data Layer 30 m (2021, Public Domain), ESA WorldCover 10 m v200 (2021, CC BY 4.0). Calibration by NASA-JPL and ISRO.
    </figcaption>
  </figure>
</div>
```
