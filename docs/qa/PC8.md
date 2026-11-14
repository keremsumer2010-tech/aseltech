# PC8 QA ve Analiz Raporu (`docs/qa/PC8.md`)

**Denetleyen / Analist:** PC8 (`M3hmeT1888`) · **Tarih:** 2026-11-14 · **Veri Sınıfı:** **`provisional`** (`CRID P05023`)  
**Kalibrasyon Bildirimi:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. Q09 — UK Kil (`uk_clay`, Greater London) Kümülatif InSAR Analizi ve Algılama Sınırı (`tasks/PC8.md` Madde 1–2)

### 1.1 Honest Scientific Finding (3 Sentences, English — Also in `data/uk_clay/summary.json` `method_note`)

> Across 9 consecutive provisional NISAR GUNW pairs over Greater London (`2026-06-21` to `2026-10-19`, 120 days), the scene-wide 1 km block median is **-0.68 cm LOS** (`p2–p98` spread **-2.95 to -0.07 cm**; local southern-edge extreme **-5.3 cm LOS** or **-7.1 cm** vertical *estimate* at **41.6°** incidence), whereas expected seasonal London Clay shrink-swell motion is only a few millimetres to **1–2 cm**. While formal Cramér-Rao multilook pixel uncertainty ($L=208$) is **0.10 cm per pair** and **0.31 cm** across the 9-pair chain (matching PC5's **~0.3 cm** pixel uncertainty floor), uncompensated tropospheric delay (**1–3 cm/pair** typical wet delay; up to **2.87 cm** single-pair `p2–p98` spread and **0.50 cm/pair** post-deramp RMS) propagates to **1.50 cm** chain noise (**1.22 cm** cumulative scene std). Because this **1.50 cm** cumulative atmospheric noise floor and pair-to-pair weather oscillation exceed the **0.5–2.0 cm** seasonal clay amplitude, London Clay shrink-swell deformation is **below detection limit for one season** and requires multi-year InSAR stacking or weather-model tropospheric correction to resolve.

### 1.2 Özet Metrikler ve Gürültü Bütçesi Karşılaştırması (`data/uk_clay/summary.json`)

| Metrik / Bileşen | Değer | Birim / Not | Yorum |
|---|---|---|---|
| **Bölge & Geometri** | `[-0.5, 51.3, 0.2, 51.7]` (`EPSG:32630`) | Track 101 Ascending, Frame 28 | Greater London / Thames Havzası (`630 × 679` px, 80 m grid) |
| **Gözlem Dönemi & Çift Sayısı** | `2026-06-21` → `2026-10-19` (**120 gün**) | **9** ardışık `provisional` (`P05023`) çift | Boşluksuz zincir, $\lambda = 0.243932\text{ m}$ (1229 MHz) |
| **Tam Zincir Geçerli Piksel Oranı** | **73.61%** (`314,881 / 427,770` px) | Kentsel alanlarda yüksek koherens | Thames Nehri ve rezervuarlar şeffaf maskeli |
| **Referans Noktası (Croydon)** | `[-0.09804, 51.37603]` (`row=486, col=390`) | Ortalama koherens **0.923** | 3 bağımsız referans aralığı: `[-5.5, -5.3] cm` |
| **Sahne Geneli 1 km Blok Dağılımı (`p2 / p50 / p98`)** | **`-2.95 / -0.68 / -0.07 cm`** | LOS | Londra genelinde medyan değişim `-0.68 cm` |
| **Yerel 1 km Blok Uç Değeri (`max_subsidence_cm`)** | **`-5.3 cm` LOS** (`-7.1 cm` dikey *estimate*) | `[-0.31835, 51.32444]` (`4 km W of Epsom`) | Güney kenar atmosferik gradyan + orman/banliyö sınırı |
| **PC5 Cramér–Rao Piksel Belirsizliği ($L=208$)** | **0.099 cm/çift** → **0.308 cm** (9 çift zincir) | `p10–p90`: `0.186 – 0.509 cm` | PC5'in `~0.3 cm` teorik çoklu-bakış faz sınırı ile tam uyumlu |
| **Düzlem Çıkarımı Sonrası Çift Başına Saçılım** | **0.50 cm RMS/çift** (`0.41–0.60 cm`) | Tek çift `p2–p98` yayılımı **2.87 cm**'ye kadar | Modellememiş ıslak troposfer (`1–3 cm/çift`) baskın |
| **Yayılan Zincir Atmosfer Gürültüsü ($\sigma_{\text{pair}}\sqrt{9}$)** | **1.50 cm LOS** (sahne std **1.22 cm**) | — | Beklenen **0.5–2.0 cm** kil büzülme sinyalini örtüyor |
| **Algılama Kararı (`detection_status`)** | **`below detection limit for one season`** | Tek yaz-sonbahar sezonu | Çok yıllı (multi-year) istifleme veya GACOS/ERA5 troposfer düzeltmesi gerekli |

### 1.3 Çift Bazında İyonosfer ve Atmosfer Saçılım Tablosu (`analysis/pc8/uk_clay_pair_stats.json`)

| # | Çift (`date1` → `date2`) | Geçerli Piksel (%) | İyonosfer `p1 → p99` (cm LOS) | İyonosfer Yayılımı (cm) | Ham Std (cm) | İyonosfer Sonrası Std (cm) | Düzlem Sonrası Std (cm) | Referanslı `p2 / p50 / p98` (cm) |
|---|---|---|---|---|---|---|---|---|
| 1 | `2026-06-21` → `2026-07-03` | 92.3% | `+29.26 → +39.19` | 9.93 | 2.583 | 0.749 | 0.529 | `-1.30 / +0.20 / +1.21` |
| 2 | `2026-07-03` → `2026-07-15` | 85.1% | `+4.27 → +14.66` | 10.39 | **4.899** | **4.205** | **0.595** | **`-2.64 / -0.92 / +0.23`** |
| 3 | `2026-07-15` → `2026-07-27` | 87.8% | `-21.85 → -16.91` | 4.95 | 1.025 | 0.641 | 0.443 | `-0.57 / +0.31 / +1.51` |
| 4 | `2026-07-27` → `2026-08-20` | 89.6% | `-16.63 → -10.48` | 6.15 | 1.553 | 0.729 | 0.553 | `-1.10 / +0.26 / +1.66` |
| 5 | `2026-08-20` → `2026-09-01` | 89.9% | `-34.59 → -27.14` | 7.45 | 1.966 | 0.632 | 0.501 | `-1.43 / -0.13 / +0.94` |
| 6 | `2026-09-01` → `2026-09-13` | 89.4% | `-2.27 → +1.59` | 3.86 | 0.866 | 0.778 | 0.408 | `-1.13 / -0.01 / +0.94` |
| 7 | `2026-09-13` → `2026-09-25` | 86.7% | `-8.68 → -6.54` | 2.14 | 1.266 | 0.883 | 0.438 | `-1.64 / -0.51 / +0.54` |
| 8 | `2026-09-25` → `2026-10-07` | 91.9% | `-25.33 → -21.87` | 3.46 | 1.565 | 1.241 | 0.430 | `-0.45 / +0.45 / +1.51` |
| 9 | `2026-10-07` → `2026-10-19` | 87.5% | `+16.80 → +19.69` | 2.89 | 1.666 | 1.264 | **0.560** | **`-2.27 / -0.84 / +0.30`** |

**Neden "Below Detection Limit for One Season"?**
1. `2026-07-15` ve `2026-10-19` tarihli sahnelerde Croydon referansına göre tüm havza medyanı sırasıyla `-0.92 cm` ve `-0.84 cm` kaymakta, `2026-10-07` sahnesinde ise `+0.45 cm` ters yönde zıplamaktadır.
2. `2026-07-15` ile `2026-09-13` arasındaki 60 günlük en sıcak yaz döneminde (`p01` Epsom: `-2.93 → -3.00 cm`, `p04` Romford: `-1.97 → -2.25 cm`) net kümülatif değişim `< 0.3 cm` olup, toplam `-5.3 cm` uç değerin neredeyse tamamı iki tekil tarihteki (`2026-07-15` ve `2026-10-19`) doğrusal olmayan troposferik dalgalanmadan kaynaklanmaktadır.
3. Londra merkezindeki tipik noktalar (`p06` Sutton `-0.62 cm`, `p07` Hackney `-0.64 cm`, `p08` Greenwich `-0.82 cm`, `p09` Islington `-0.93 cm`, `p10` Camden `-0.69 cm`) `1.50 cm` zincir atmosfer gürültüsü bandının tamamen içinde kalmaktadır.

---

## 2. Madde 3 — Fens (`pipeline/subset/fens`) Kontrolü

- `pipeline/subset/` klasörü kontrol edildi: mevcut alt kümeler yalnızca `central_valley`, `karapinar` ve `uk_clay` klasörleridir.
- `fens` için kesilmiş GUNW alt kümesi (`pipeline/subset/fens/`) bulunmadığından (`tasks/PC8.md` Madde 3: *"pipeline/subset/ altında Fens GUNW varsa; yoksa bu adımı atla ve status'a yaz"*), bu adım atlanmış ve `status/PC8.md` içine kaydedilmiştir.

---

## 3. Test Görevi — `docs/story/media/` Dosya Listesi ve Boyut Kontrolü (K-12)

Toplam **25 dosya** kontrol edildi. Hiçbir dosya **0 bayt** veya **20 MB (20,480 KB)** sınırının üzerinde değildir.

| # | Dosya Adı | Boyut (Bayt) | Boyut (KB) | Durum (0 B / >20 MB Kontrolü) |
|---|---|---|---|---|
| 1 | `cv_subsidence.gif` | 4,437,162 | 4333.17 | OK |
| 2 | `cv_subsidence.mp4` | 3,221,104 | 3145.61 | OK |
| 3 | `gnss_CAD1.png` | 99,539 | 97.21 | OK |
| 4 | `gnss_CAFP.png` | 100,163 | 97.82 | OK |
| 5 | `gnss_CAHA.png` | 102,724 | 100.32 | OK |
| 6 | `gnss_HANF.png` | 103,025 | 100.61 | OK |
| 7 | `gnss_P056.png` | 100,937 | 98.57 | OK |
| 8 | `gnss_P564.png` | 98,895 | 96.58 | OK |
| 9 | `gnss_P565.png` | 99,363 | 97.03 | OK |
| 10 | `gnss_P566.png` | 96,457 | 94.20 | OK |
| 11 | `gnss_QCAP.png` | 103,639 | 101.21 | OK |
| 12 | `gnss_TLBN.png` | 106,226 | 103.74 | OK |
| 13 | `kp_subsidence.gif` | 1,422,183 | 1388.85 | OK |
| 14 | `kp_subsidence.mp4` | 917,889 | 896.38 | OK |
| 15 | `risk_1.png` | 106,894 | 104.39 | OK |
| 16 | `risk_10.png` | 108,038 | 105.51 | OK |
| 17 | `risk_2.png` | 110,445 | 107.86 | OK |
| 18 | `risk_3.png` | 113,421 | 110.76 | OK |
| 19 | `risk_4.png` | 107,879 | 105.35 | OK |
| 20 | `risk_5.png` | 111,968 | 109.34 | OK |
| 21 | `risk_6.png` | 103,455 | 101.03 | OK |
| 22 | `risk_7.png` | 106,056 | 103.57 | OK |
| 23 | `risk_8.png` | 113,695 | 111.03 | OK |
| 24 | `risk_9.png` | 109,243 | 106.68 | OK |
| 25 | `validation_scatter.png` | 215,829 | 210.77 | OK |
