# PC5 Bağımsız QA Raporu (`docs/qa/PC5.md`)

**Denetleyen:** PC5 (`M3hmeT1888`) · **Tarih:** 2026-11-14 · **Veri Sınıfı:** **`provisional`** (`beta-precal` dahil edilmedi)  
**Kalibrasyon Bildirimi:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Görev 3 — `summary.json` Bağımsız Sayı Doğrulaması (`central_valley` & `karapinar`)

Bağımsız saf NumPy + WGS84 ters-UTM betiğiyle `analysis/out/<site>_cum.npz` dizileri doğrudan okunmuş, 13×13 piksel (`~1 km`, $\ge 50\%$ geçerli piksel, blok içi std $\le 2.0\text{ cm}$) blok medyanları ve insidans/ekstrapolasyon hesapları sıfırdan tekrar üretilmiştir. Tüm alanlar **`data/<site>/summary.json`** dosyalarıyla tam örtüşmektedir.

### 1.1 Central Valley (`data/central_valley/summary.json` vs. `analysis/out/central_valley_cum.npz`)

- **Grid & Kapsam:** `EPSG:32611`, şekil `(1473, 1438)`, geçerli piksel `1,332,149` (`62.89%`).
- **İşaret Konvansiyonu:** Negatif değer uyduya uzaklaşma = yer çökmesi (ISCE3/MintPy/NISAR ATBD ile uyumlu; havza içi GPS istasyonlarıyla da doğrulandı).

| Alan | `summary.json` Değeri | Bağımsız Yeniden Hesap (Ham) | Yuvarlatılmış | Sonuç |
|---|---|---|---|---|
| `max_subsidence_cm` (LOS) | **`-7.8`** | `-7.8015 cm` | `-7.8` | **GEÇTİ** |
| `max_subsidence_location` | `[-119.02173, 36.01119]` | `(-119.02173, 36.01119)` | Aynı | **GEÇTİ** |
| `reference_point` | `[-119.14562, 36.45323]` | `(-119.14562, 36.45323)` | Aynı | **GEÇTİ** |
| `incidence_deg_at_max` | **`39.1`** | `39.125°` | `39.1` | **GEÇTİ** |
| `period` / `n_pairs` | `["2026-06-28", "2026-10-14"]` / **`7`** | 108 gün, 8 tarih → 7 ardışık çift | Aynı | **GEÇTİ** |
| `rate_cm_per_yr_estimate` | **`-26.4`** (`estimate`) | `-26.384 cm/yr` (`-7.8015 / 108 * 365.25`) | `-26.4` | **GEÇTİ** |
| `max_subsidence_vertical_cm_estimate` | **`-10.1`** (`estimate`) | `-10.056 cm` (`-7.8015 / cos(39.125°)`) | `-10.1` | **GEÇTİ** |
| Sinyal / Zincir Gürültüsü (SNR) | `-7.8 cm` LOS vs `uncertainty.md` | $\sigma_{\text{toplam}} = 1.74\text{ cm}$ (yerel) / $2.87\text{ cm}$ (sahne) | **4.5× / 2.7×** | **Anlamlı Sinyal** |

### 1.2 Karapınar (`data/karapinar/summary.json` vs. `analysis/out/karapinar_cum.npz`)

- **Grid & Kapsam:** `EPSG:32636`, şekil `(470, 603)`, geçerli piksel `40,194` (`14.18%`).

| Alan | `summary.json` Değeri | Bağımsız Yeniden Hesap (Ham) | Yuvarlatılmış | Sonuç |
|---|---|---|---|---|
| `max_subsidence_cm` (LOS) | **`-5.9`** | `-5.9270 cm` | `-5.9` | **GEÇTİ** |
| `max_subsidence_location` | `[33.53056, 37.71818]` | `(33.53056, 37.71818)` | Aynı | **GEÇTİ** |
| `reference_point` | `[33.74416, 37.74659]` | `(33.74416, 37.74659)` | Aynı | **GEÇTİ** |
| `incidence_deg_at_max` | **`42.0`** | `42.000°` | `42.0` | **GEÇTİ** |
| `period` / `n_pairs` | `["2026-06-26", "2026-10-12"]` / **`8`** | 108 gün, 9 tarih → 8 ardışık çift | Aynı | **GEÇTİ** |
| `rate_cm_per_yr_estimate` | **`-20.0`** (`estimate`) | `-20.045 cm/yr` (`-5.9270 / 108 * 365.25`) | `-20.0` | **GEÇTİ** |
| `max_subsidence_vertical_cm_estimate` | **`-8.0`** (`estimate`) | `-7.976 cm` (`-5.9270 / cos(42.000°)`) | `-8.0` | **GEÇTİ** |

---

## 2. Q26 — Nokta Bazında Zaman Serisi Kalitesi (`analysis/decomp/point_quality.py`)

Her nokta için doğrusal en küçük kareler uyumu $d(t) = a + v \cdot t$, açıklanan varyans $R^2$, artık standart sapması $\sigma_{\text{res}}$ (`ddof=2`) ve ardışık tarihler arası en büyük sıçrama (`max_jump_cm`) hesaplanmıştır. NISAR L-bant ($\lambda \approx 0.242\text{ m}$) faz belirsizliği ölçekleri:
- Tam $2\pi$ faz açma döngüsü: $\lambda/2 \approx 12.10\text{ cm}$ LOS
- Yarım döngü ($\pi\text{ rad}$): $\lambda/4 \approx 6.05\text{ cm}$ (`UNWRAP_SUSPECT`, `analysis/insar.py` `cycle_outliers` eşiğiyle aynı)
- Çeyrek döngü ($\pi/2\text{ rad}$): $\lambda/8 \approx 3.02\text{ cm}$ (`ELEVATED_JUMP`, tek çift sıçrama uyarısı)
- `WATCH`: $2.00 < |\Delta d|_{\max} \le 3.02\text{ cm}$; `OK`: $|\Delta d|_{\max} \le 2.00\text{ cm}$.

### 2.1 Central Valley (`data/central_valley/points.json`, 12 Nokta, 108 Gün)

| ID | Sınıf | Konum Adı | Son Değer (cm) | Doğrusal Hız (*est.*, cm/yr) | Doğrusal Uyum 108g (cm) | $R^2$ | Artık Std (cm) | En Büyük Sıçrama (cm) | Sıçrama Çifti | Durum |
|---|---|---|---|---|---|---|---|---|---|---|
| `p01` | `most_subsiding` | 6 km N of Terra Bella | -7.80 | -24.97 | -7.38 | **0.930** | 0.753 | -2.89 | `2026-09-08->2026-09-20` | `WATCH` |
| `p02` | `most_subsiding` | 21 km S of Lemoore | -7.78 | -24.50 | -7.24 | **0.956** | 0.581 | -2.10 | `2026-06-28->2026-07-10` | `WATCH` |
| `p03` | `most_subsiding` | 10 km SW of Huron | -7.22 | -25.72 | -7.61 | **0.897** | 0.963 | **-3.25** | `2026-08-15->2026-08-27` | **`ELEVATED_JUMP`** |
| `p04` | `most_subsiding` | 15 km W of Corcoran | -7.00 | -27.21 | -8.05 | **0.928** | 0.835 | -2.38 | `2026-07-22->2026-08-15` | `WATCH` |
| `p05` | `most_subsiding` | 5 km NE of Ivanhoe | -6.25 | -23.61 | -6.98 | **0.924** | 0.749 | -2.39 | `2026-08-15->2026-08-27` | `WATCH` |
| `p06` | `median` | 6 km S of Avenal | -0.46 | -1.56 | -0.46 | 0.126 | 0.453 | +1.19 | `2026-08-27->2026-09-08` | `OK` |
| `p07` | `median` | 6 km W of Lost Hills | -0.18 | -1.20 | -0.36 | 0.055 | 0.550 | -1.82 | `2026-07-22->2026-08-15` | `OK` |
| `p08` | `median` | Richgrove | -0.29 | -0.37 | -0.11 | 0.001 | **1.439** | **+4.44** | `2026-08-27->2026-09-08` | **`ELEVATED_JUMP`** |
| `p09` | `median` | 12 km NE of Lost Hills | -0.29 | -1.04 | -0.31 | 0.077 | 0.395 | +1.17 | `2026-08-15->2026-08-27` | `OK` |
| `p10` | `median` | 27 km S of Avenal | -0.28 | -2.19 | -0.65 | 0.171 | 0.530 | +1.20 | `2026-07-10->2026-07-22` | `OK` |
| `p11` | `near_reference` | 7 km NW of Woodlake | +0.23 | +0.79 | +0.23 | 0.426 | **0.101** | +0.25 | `2026-08-27->2026-09-08` | `OK` |
| `p12` | `near_reference` | 5 km NW of Woodlake | -0.24 | -1.23 | -0.36 | 0.083 | 0.449 | -1.34 | `2026-08-15->2026-08-27` | `OK` |

**Teknik QA Yorumu (Central Valley):**
- Hiçbir noktada yarım $2\pi$ faz açma sınırını ($\lambda/4 = 6.05\text{ cm}$) aşan bir atlama (`UNWRAP_SUSPECT`) yoktur.
- **`p08` (Richgrove)** dikkat çekici biçimde geçici bir pozitif sıçrama sergilemektedir (`-2.53 → +1.91 → -1.12 cm`, `max_jump = +4.44 cm`, `res_std = 1.439 cm`). Hemen ertesi tarihte eski seviyesine dönmesi bunun kalıcı deformasyon değil, **2026-09-08 sahnesindeki atmosferik gecikme veya yerel faz açma artefaktı** olduğunu gösterir.
- **`p03` (Huron)** `-3.25 cm` adımını takip eden küçük bir geri sekme göstermekle birlikte genel doğrusal eğilimi korur ($R^2 = 0.897$); aynı çift (`2026-08-15->2026-08-27`) `error_budget.py` içinde de en yüksek yerel gürültülü dönem (`1.14 cm`) olarak ölçülmüştür.
- En hızlı çöken 5 nokta (`p01`–`p05`) yüksek doğrusallık ($R^2 = 0.90\text{–}0.96$, artık std $0.58\text{–}0.96\text{ cm}$) ve net $-23.6\text{ ile }-27.2\text{ cm/yıl}$ (*estimate*) arası LOS eğilim üretmektedir.

### 2.2 Karapınar (`data/karapinar/points.json`, 9 Nokta, 108 Gün — Ek Denetim)

| ID | Sınıf | Konum Adı | Son Değer (cm) | Doğrusal Hız (*est.*, cm/yr) | $R^2$ | Artık Std (cm) | En Büyük Sıçrama (cm) | Sıçrama Çifti | Durum |
|---|---|---|---|---|---|---|---|---|---|
| `p01` | `most_subsiding` | 2 km W of Karapınar | -5.93 | -15.58 | **0.854** | 0.715 | -2.24 | `2026-09-30->2026-10-12` | `WATCH` |
| `p02` | `most_subsiding` | 3 km W of Oymalı | -2.57 | -5.04 | 0.492 | 0.569 | -1.44 | `2026-09-30->2026-10-12` | `OK` |
| `p03` | `most_subsiding` | 5 km NW of Akören | -1.82 | -2.01 | 0.062 | 0.865 | +1.27 | `2026-08-25->2026-09-06` | `OK` |
| `p04` | `most_subsiding` | 6 km SE of Gazi Osman Paşa | -1.74 | -3.20 | 0.308 | 0.532 | -1.08 | `2026-09-30->2026-10-12` | `OK` |
| `p05` | `most_subsiding` | 2 km S of Ekizli | -0.88 | -1.02 | 0.110 | 0.322 | -0.73 | `2026-09-18->2026-09-30` | `OK` |
| `p06` | `median` | 7 km N of Kesmez | -0.35 | +1.78 | 0.069 | 0.724 | +1.41 | `2026-07-20->2026-08-13` | `OK` |
| `p07` | `median` | 2 km SE of Işıklar | -0.42 | +1.17 | 0.038 | 0.657 | -1.15 | `2026-09-18->2026-09-30` | `OK` |
| `p08` | `near_reference` | 2 km SE of Yeşilyurt | +0.47 | +1.02 | 0.564 | **0.100** | +0.28 | `2026-06-26->2026-07-08` | `OK` |
| `p09` | `near_reference` | 4 km SE of Yeşilyurt | -1.30 | -2.61 | 0.409 | 0.349 | -0.86 | `2026-09-30->2026-10-12` | `OK` |

**Doğrulama Komutu:**
```bash
python -m analysis.decomp.point_quality
python -m pytest analysis/decomp -q   # 15 passed
```
