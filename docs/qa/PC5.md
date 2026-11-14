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
python -m pytest analysis/decomp -q   # 16 passed, 2 failed (pyproj ortamda yok; PC3 ortaminda pyproj ile 18/18)
```

---

## 3. Görev 7 — Tam Yıl Veri Hazırlık Kontrol Listesi (`Q07` / `Q08` Sonrası)

PC2 **Q07** kapsamında tam yıl Central Valley zincirini (`2025-11-24 → 2026-10-14`, `pipeline/subset/central_valley_beta/` veya güncellenmiş tam yığın) ve PC3 `analysis/out/central_valley_cum_stack.npz` yığınını ürettiğinde (`docs/REVIEW_1500.md` notu uyarınca bu akşam / Pazar) çalıştırılacak eksiksiz doğrulama ve kalite kapısı listesi aşağıdadır:

### 3.1 Ön Koşul ve Bağımlılık Kontrolü
1. **Ortam bağımlılığı (`pyproj` uyarısı):** Yerel PC5 Python (`Python 3.12`) kurulumunda `pyproj` yüklü değildir; bu nedenle `analysis/cumulative.py` (`import pyproj`) üzerinden `to_latlon_grid` çağıran `analysis/decomp/run_decomp.py` ve `test_run_decomp_*` testleri `pyproj` kurulmadan hata verir. Pazar günü `run_decomp.py` çalıştırılmadan önce `python -c "import pyproj"` doğrulanmalı (yoksa PC3 ortamı kullanılmalı veya `pip install pyproj`). PC5'in `analysis/pc5/*` modülleri ise dahili saf-NumPy WGS84↔UTM dönüşümü ile `pyproj` olmadan da çalışır (`12 passed`).
2. **Kalite sınıfı kuralı (`rules/VERI_SOZLESMESI.md` §3):** `2026-06-28` öncesi `beta-precal` çiftleri varsa kümülatif tam-yıl ayrıştırma çıktısında `--quality mixed` bayrağı zorunludur (`quality: "provisional"` yalnız P05023 provisional zincirinde kalır; tam yıl beta içerdiğinde `"mixed"`, 2026-10-21 sonrası tamamen kalibreli veri setinde `"validated"` olabilir).

### 3.2 Pazar Çalıştırma Sırası (Birebir CLI Komutları)
1. **Tam yıl mevsimsel/kalıcı ayrıştırma (`analysis/decomp/run_decomp.py`):**
   ```bash
   python analysis/decomp/run_decomp.py central_valley --stack analysis/out/central_valley_cum_stack.npz --out data/central_valley_fullyear --quality mixed
   ```
   - *Beklenen çıktılar:* `data/central_valley_fullyear/decomp.json`, `data/central_valley_fullyear/decomp_permanent.png`, `data/central_valley_fullyear/decomp_seasonal.png`.
   - *Kalite kapısı:* `status == "ok"` (`span >= 9 ay`, `n_epochs >= 10`, geçerli piksel oranı `valid_fraction > 0.30`), `quality == "mixed"`, kalıcı hız medyan/p2 (`permanent_cm_per_yr.p2`) Central Valley literatür aralığı (`-17` ile `-35 cm/yr`, Neely et al. 2021) ile uyumlu, mevsimsel genlik (`seasonal_amp_cm`) `p01`/`p04` gibi tarım havzasında pozitif ve kış geri sıçramasını yakalıyor.
2. **Nokta bazında zaman serisi QA (`analysis/decomp/point_quality.py`):**
   ```bash
   python -m analysis.decomp.point_quality
   ```
   - *Kalite kapısı:* `suspect_ids == []` (hiçbir noktada `|Δd| > λ/4 = 6.05 cm` yarım-döngü faz açma atlaması olmamalı); `p08` (Richgrove) tek sahne sıçramasının tam yıl zincirinde artıp artmadığı kontrol edilmeli.
3. **Piksel bazında Cramér–Rao belirsizlik haritası (`analysis/pc5/uncertainty_map.py`):**
   ```bash
   python analysis/pc5/uncertainty_map.py central_valley --looks 208
   python analysis/pc5/uncertainty_map.py karapinar --looks 208
   ```
   - *Beklenen çıktılar:* `data/central_valley/uncertainty/{sigma_cm.png,meta.json}` ve `data/karapinar/uncertainty/{sigma_cm.png,meta.json}`.
   - *Kalite kapısı:* `fraction_above_vmax`, `valid_pixel_fraction` (~`%65` CV, ~`%15` Karapınar) ve $\sigma_{\text{toplam}} \propto \sqrt{N}$ büyümesi beklenen mertebede mi (`108` günlük 7 çift `0.294 cm` → ~30 çiftlik tam yılda `~0.61 cm` beklenir); `L = 100` duyarlılık bloğu güncellenmiş olmalı.
4. **Altyapı risk duyarlılığı ve GNSS karşılaştırması (`analysis/pc5/risk_sensitivity.py` & `validation/compare.py`):**
   ```bash
   python analysis/pc5/risk_sensitivity.py --write-doc
   python validation/compare.py
   ```
   - *Kalite kapısı:* İlk 10 altyapı segmenti tam-yıl yığınında da yüksek risk (`gradient >= 10 mm/km` veya `<= -10 cm`) statüsünü koruyor mu; GNSS RMSE / Pearson $r$ değerleri tam yıl mevsimsel döngü eklendikten sonra özellikle kararlı/kenar istasyonlarda (`CAD1`, `P564`, `CAFP`) iyileşiyor mu kontrol edilmeli.
5. **Son test doğrulaması (`pytest`):**
   ```bash
   python -m pytest analysis/pc5 analysis/decomp -q
   ```
   - *Hedef:* `pyproj` kurulu ortamda `30 passed` (veya `pyproj` yoksa `analysis/pc5` `12 passed`, `analysis/decomp` `16 passed` + `run_decomp` için PC3 ortamı).

### 3.3 Bilinen Açıklar ve Geri Dönüş (Rollback) Notları
- `analysis/decomp/run_decomp.py` içinde `valid < 100` veya zaman aralığı `< 0.75 yıl` kalırsa script otomatik olarak `status: "insufficient_data"` yazar ve PNG üretmez — site bozulmaz.
- `game/model.js` kalibrasyon verisi tam yıl gelirse yalnız `data/central_valley/summary.json` (108-günlük yaz hedefi) ile uyumlu olduğu için oyun modeli `k_cal = 0.6232` katsayısı aynı yaz penceresi hedefine bağlı kalmaya devam eder; yıllık net oran oyunu etkilemek üzere değiştirilecekse `game_sensitivity.py` yeniden çalıştırılmalıdır.

---

## 4. 15:30 Paketi Görev 5 — `Q08` Tam Yıl Çıktısı ve Yeni Veri Bağımsız Kontrolü

- **Denetim zamanı:** 2026-11-14 15:43 TR (`git pull` sonrası `main` durumu)
- **`data/central_valley_fullyear/` durumu:** **Henüz mevcut değil** (tam yıl ayrıştırma çıktısı henüz üretilmedi).
- **`pipeline/subset/central_valley_beta/` incelemesi (YENİ):** **`15`** adet `beta-precal` `.npz` çifti (`2025-11-24_2025-12-06.npz` → `2026-05-11_2026-05-23.npz`, ızgara `(1473, 1438)`, beklenen 15 anahtarlı şema tam) repoya inmiş durumda.
- **KRİTİK KÖPRÜ BOŞLUĞU UYARISI (PC2/PC3 için):** `central_valley_beta` zinciri **`2026-05-23`** tarihinde biterken provisional `pipeline/subset/central_valley/` zinciri **`2026-06-28`** tarihinde başlıyor; arada **36 günlük boşluk (`2026-05-23 → 2026-06-28`, üç 12-günlük çift: `05-23..06-04`, `06-04..06-16`, `06-16..06-28`)** var. `analysis/cumulative.py` boşluklu zinciri birleştirmeyeceği için tam yıl birleştirmede bu ara çiftlerin tamamlanması veya `analysis/decomp/decompose.py` için iki parçalı referans hizalaması gerekir.
- **Yeni eklenen diğer veri setleri bağımsız kontrolü:**
  - `analysis/out/central_valley_p114_cum.npz`: Track 114 alçalan yörünge (`2026-06-22 → 2026-10-20`, 9 tarih, `1,137,804 / 2,118,174 = %53.7` geçerli piksel, `min = -28.81 cm`, `max = +14.65 cm`) ve `data/central_valley/vertical.json` (`p2 = -5.98 cm`, `p50 = -1.25 cm`, `p98 = +2.35 cm` dikey bileşen).
  - `pipeline/subset/uk_clay/*.npz` (`9` çift, `2026-06-21 → 2026-10-19`, `(630, 679)`, `%93.9–%96.4` geçerli piksel) + `data/uk_clay/{summary,detection}.json`: `status: "below_detection"`, zincir gürültüsü `chain_sigma_cm = 1.21 cm`, 3σ eşiği `3.62 cm`, kuadratik düzlem sonrası ekstrem `-3.57 cm` (kenardan `5.1 km`), blokların `%97.7`'si `±1.5 cm` içinde.
- **Mevcut test durumu:** `analysis/pc5` **`19/19 passed`**, `analysis/decomp` `16 passed, 2 failed` (`test_run_decomp_end_to_end` & `test_run_decomp_insufficient` yerel ortamda `pyproj` eksikliği nedeniyle `ModuleNotFoundError: No module named 'pyproj'`; `decompose.py` çekirdek fonksiyonları `16/16` geçiyor).

---

## 5. `SONSUZ DÖNGÜ` — Tur 1 Denetimi (`a–d`)

### a) `data/*` Değişiklik ve Yeniden Çalıştırma Kontrolü
- `analysis/out/central_valley_cum.npz` (`2026-06-28..2026-10-14`, `1,332,149` geçerli piksel, tepe `-7.8 cm`) ve `analysis/out/karapinar_cum.npz` (`2026-06-26..2026-10-12`, `40,194` geçerli piksel, tepe `-5.9 cm`) yığınları değişmediği doğrulandı; `data/*/uncertainty/` (`0.294 cm` CV, `0.326 cm` KP medyan) ve `data/*/area_stats.json` (`239.5 km²` CV `< -5 cm`, `28.7 km²` KP `< -2 cm`) günceldir.

### b) `web/*.html` vs. `data/*` Sayı ve Tutarlılık Denetimi
- **`web/index.html` — TUTARLI:** `-7.8 cm`, `240 km²` (`area_stats.json` `239.54 km²` tam sayıya yuvarlatması), `1.0 cm` GPS medyan RMSE (`validation.json` 10 istasyon medyanı `1.004 cm`), `81 / 645` yüksek riskli altyapı, Londra kili `± 3.6 cm` (`uk_clay/detection.json` `3.62 cm`), Karapınar `-5.9 cm`, `4.2 cm` vs `0.6 cm` (`0–1 km` `-4.152` vs `>5 km` `-0.647 cm`, `10 / 29` obruk) değerlerinin tamamı `data/*` ile örtüşmektedir.
- **`web/science.html` — 3 TUTARSIZLIK TESPİT EDİLDİ (PC9 için aksiyon listesi):**
  1. **`web/science.html` satır 37 (eski referans yayılımı):** *"Changing the reference area moves the Central Valley maximum between −6.2 and −7.8 cm"* yazıyor; oysa güncel `data/central_valley/summary.json` 3 referans penceresiyle `range_cm: [-7.8, -4.7]` (`alt_ref 2 = -4.7 cm`) bildiriyor → **`−4.7 and −7.8 cm`** olarak güncellenmeli.
  2. **`web/science.html` satır 37 (çift aralığı):** *"Consecutive 12-day pairs"* ifadesi geçiyor; oysa zincirde `07-22→08-15` ve `09-20→10-14` (**24 günlük**) çiftler de var (`web/index.html` doğru biçimde `"12 to 24 days apart"` yazıyor).
  3. **`web/science.html` satır 28 (`SME2` durumu):** Tabloda `SME2 (L3)` için hâlâ **`Cause-and-effect panel (in progress)`** yazıyor; oysa `data/central_valley/drivers.json` ve `docs/story/drivers_analysis.md` tamamlandı (`N = 8` güç sınırı nedeniyle nedensellik için henüz erken).
- **`web/data.html` — EKSİK İNDİRME SATIRLARI (PC9 için öneri):** Tablo şu an `area_stats.json`, `drivers.json`, `vertical.json`, `uncertainty/meta.json`, `karapinar/assets.json` ve `uk_clay/{summary,detection,points}.json` dosyalarını listelemiyor; `"Every number, downloadable"` başlığıyla tam uyum için bu JSON'lar eklenebilir.

### c) `docs/story/literature_comparison.md` ve `docs/story/sources.md` HTTP Link Kontrolü
- İki dosyadaki **29 / 29** benzersiz HTTP/HTTPS URL'sinin tamamı canlı `HEAD/GET` sorgusunda **`200 OK`** döndürdü (sıfır kırık/404 bağlantı: NASA Earth Observatory, ASF NISAR User Guide [4 sayfa], ASF GCOV Browse PNG, NASA GIBS Worldview API, USGS SIR 2018-5144 & FS 005-00 [HTML+PDF], PMC8047915 / PMC6559157 / PMC7865528, NHESS 2010, ISPRS 2015, DergiPark PDF 3454 & 227372, BGS [2 sayfa], CEH UK Peat PDF, Great Fen, Wikipedia, KVPR).

### d) `web/science.html` ve `web/index.html` Bilimsel Yöntem Geliştirme Önerileri (PC9 için)
1. **Çift-yörünge dikey/doğu ayrıştırmasını belgeleme:** `web/science.html` §2–§3 şu an yalnızca tek yörünge `d_vert ≈ d_LOS / cos θ_inc` varsayımını açıklıyor; repoda artık track 34 (çıkan) + track 114 (alçalan) ortak `d_k = E·e_k + U·u_k` ayrıştırması (`data/central_valley/vertical.json`, dikey p2 `-5.98 cm`, doğu bileşeni `vertical_east.png`) var ve eklenirse yatay hareket belirsizliği şeffaf biçimde kapatılır.
2. **GPS medyan RMSE kapsamını hizalama:** `web/index.html` tüm 10 istasyonun medyanını (`1.0 cm`) yazarken `web/science.html` JS kodu (satır 87) yalnızca `r ≥ 0.4` olan 6 istasyonun medyanını (`0.8 cm`) yazdırıyor; her iki değerin hangi alt küme olduğu açıkça ayrılmalı.
3. **Troposfer / gelgit ve düzlemsel eğim (planar ramp) ayrımı:** `web/science.html` §2'de GUNW trofosfer LUT ve katı yer gelgitlerinin varsayılan olarak uygulanmadığı (ASF `gunw` belgesi) ve düzlemsel eğim çıkarmanın geniş ölçekli çökme kasesinin bir kısmını yutabileceği (`range_cm [-7.8, -4.7]`) kısaca belirtilirse yöntem bölümü jürinin olası faz-ekranı sorularını doğrudan karşılar.
4. **İstatistiksel doğrulama bağlantıları:** `web/science.html` sonundaki dökümantasyon listesine yeni üretilen [`sinkhole_stats.md`](../story/sinkhole_stats.md) (Karapınar katı küme kaydırma testi $p = 0.021$) ve [`drivers_analysis.md`](../story/drivers_analysis.md) (`N = 8` güç sınırı) belgeleri eklenebilir.
