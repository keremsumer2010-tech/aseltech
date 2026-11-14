# PC8 QA ve Analiz Raporu (`docs/qa/PC8.md`)

**Denetleyen / Analist:** PC8 (`M3hmeT1888`) · **Tarih:** 2026-11-14 · **Veri Sınıfı:** **`provisional`** (`CRID P05023`)  
**Kalibrasyon Bildirimi:** *NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team.*

---

## 1. 15:35 Madde 1 & Q09 — UK Kil (`uk_clay`, Greater London) Kümülatif InSAR Analizi ve Algılama Sınırı

- **Hikaye Metni ve HTML Taslağı:** `docs/story/uk_findings.md` (PC9'un `web/index.html` `#ukClay` veya `web/science.html` `#limits` bölümüne doğrudan yapıştırabileceği 6 cümlelik `docs/REVIEW_1500.md` uyumlu sade İngilizce metin, `Figure 4` açıklaması ve kaynak izlenebilirlik tablosu).
- **Görsel:** `docs/story/media/pc8_uk_detection.png` (190.0 KB, 2 panelli NASA Earth Observatory tarzı grafik — görsel olarak incelendi, sıfır metin çakışması).

### 1.1 Honest Scientific Finding (English — `docs/story/uk_findings.md` & `data/uk_clay/summary.json`)

> Across 9 consecutive provisional NISAR GUNW pairs over Greater London (`2026-06-21` to `2026-10-19`, 120 days), the scene-wide 1 km block median is **-0.68 cm LOS** (`p2–p98` spread **-2.95 to -0.07 cm**; local southern-edge extreme **-5.3 cm LOS** or **-7.1 cm** vertical *estimate* at **41.6°** incidence), whereas expected seasonal London Clay shrink-swell motion is only a few millimetres to **1–2 cm**. While formal Cramér-Rao multilook pixel uncertainty ($L=208$) is **0.10 cm per pair** and **0.31 cm** across the 9-pair chain (matching PC5's **~0.3 cm** pixel uncertainty floor), uncompensated tropospheric delay (**1–3 cm/pair** typical wet delay; up to **2.87 cm** single-pair `p2–p98` spread and **0.50 cm/pair** post-deramp RMS) propagates to **1.50 cm** chain noise (**1.21 cm** cumulative 1 km block $\sigma$, **3.62 cm** $3\sigma$ single-season detection threshold in `data/uk_clay/detection.json`). Because this **1.21 cm** ($1\sigma$) / **3.62 cm** ($3\sigma$) single-season atmospheric noise floor exceeds both the **0.5–2.0 cm** seasonal London Clay amplitude and the **1–2 cm/yr** modern Holme Fen peat loss (`docs/story/holme_fen.md`), UK clay and peat deformation are **below detection limit for one season** and require multi-year (~3-year) InSAR stacking or weather-model tropospheric correction to resolve.

### 1.2 Özet Metrikler ve Gürültü Bütçesi Karşılaştırması (`data/uk_clay/detection.json` & `summary.json`)

| Metrik / Bileşen | Değer | Birim / Not | Yorum |
|---|---|---|---|
| **Bölge & Geometri** | `[-0.5, 51.3, 0.2, 51.7]` (`EPSG:32630`) | Track 101 Ascending, Frame 28 | Greater London / Thames Havzası (`630 × 679` px, 80 m grid) |
| **Gözlem Dönemi & Çift Sayısı** | `2026-06-21` → `2026-10-19` (**120 gün**) | **9** ardışık `provisional` (`P05023`) çift | Boşluksuz zincir, $\lambda = 0.243932\text{ m}$ (1229 MHz) |
| **Tam Zincir Geçerli Piksel Oranı** | **73.61%** (`314,881 / 427,770` px) | Kentsel alanlarda yüksek koherens | Thames Nehri ve rezervuarlar şeffaf maskeli |
| **Referans Noktası (Croydon)** | `[-0.09804, 51.37603]` (`row=486, col=390`) | Ortalama koherens **0.923** | 3 bağımsız referans aralığı: `[-5.5, -5.3] cm` |
| **Sahne Geneli 1 km Blok Dağılımı (`p2 / p50 / p98`)** | **`-2.95 / -0.68 / -0.07 cm`** | LOS | Londra genelinde medyan değişim `-0.68 cm` |
| **Yerel 1 km Blok Uç Değeri (`max_subsidence_cm`)** | **`-5.3 cm` LOS** (`-7.1 cm` dikey *estimate*) | `[-0.31835, 51.32444]` (`4 km W of Epsom`) | Güney kenar atmosferik gradyan + orman/banliyö sınırı |
| **PC5 Cramér–Rao Piksel Belirsizliği ($L=208$)** | **0.099 cm/çift** → **0.308 cm** (9 çift zincir) | `p10–p90`: `0.186 – 0.509 cm` | PC5'in `~0.3 cm` teorik çoklu-bakış faz sınırı ile tam uyumlu |
| **1 km Blok Çift Başına Saçılım (`pair_block_std_cm`)** | **0.31 – 0.47 cm** (medyan **0.38 cm/çift**) | Tek çift `p2–p98` yayılımı **2.87 cm**'ye kadar | Modellememiş ıslak troposfer (`1–3 cm/çift`) baskın |
| **Kümülatif 1 km Blok Gürültüsü ($\sigma$ / $3\sigma$)** | **1.21 cm LOS ($1\sigma$)** / **3.62 cm LOS ($3\sigma$)** | `data/uk_clay/detection.json` | Beklenen **0.5–2.0 cm** kil ve **1–2 cm/yıl** turba sinyalini örtüyor |
| **3 Yıllık Yığın Eşiği (~90 çift, $\sigma/\sqrt{N}$)** | **~0.2–0.5 cm/yıl ($1\sigma$)** / **~0.6–1.2 cm/yıl ($3\sigma$)** | Çok yıllı zaman serisi | Hem Londra kili (`0.5–2.0 cm`) hem Holme Fen (`1–2 cm/yıl`) ölçülebilir hale gelir |
| **Algılama Kararı (`detection_status`)** | **`below_single_season_detection_limit`** | Tek yaz-sonbahar sezonu | Çok yıllı (~3 yıl) istifleme veya GACOS/ERA5 troposfer düzeltmesi gerekli |

---

## 2. 15:35 Madde 2 — Karapınar İkinci Geçiş (`path 172` Ascending vs. `path 7` Descending) Çapraz Kontrolü

**Girdiler:**
- **Birincil Yörünge (`path 7`):** `pipeline/subset/karapinar/*.npz` (`data/karapinar/`, `analysis/out/karapinar_cum.npz`) — Track 7 Descending, Frame 69 (`16:40 UTC`, sağa bakan, geliş açısı **42.1°**).
- **İkincil Yörünge (`path 172`):** `pipeline/subset/karapinar_p172/*.npz` (`data/karapinar_p172/`, `analysis/pc8/karapinar_p172_cum.npz`) — Track 172 Ascending, Frame 21 (`02:53 UTC`, sağa bakan, geliş açısı **41.9°**).
- **Üretilen Veri ve Görseller:**
  - `data/karapinar_p172/meta.json`, `data/karapinar_p172/points.json`, `data/karapinar_p172/summary.json`, `data/karapinar_p172/disp/2026-06-26.png` .. `2026-10-12.png` (9 PNG)
  - `analysis/pc8/karapinar_p172_check.py`, `analysis/pc8/karapinar_p172_cum.npz`, `analysis/pc8/karapinar_p172_cum_stack.npz`, `analysis/pc8/karapinar_p172_pair_stats.json`, `analysis/pc8/kp_p7_vs_p172.json`
  - `docs/story/media/pc8_kp_p7_vs_p172.png` (264.3 KB, 3 panelli karşılaştırma grafiği: `p01` zaman serisi + 12 nokta ve 220 blok saçılımı + çift başına blok saçılımı)

### 2.1 İki Bağımsız Yörünge Özeti (`2026-06-26` → `2026-10-12`, 8 Ardışık Çift, 108 Gün)

| Özellik | Track 7 Descending (`data/karapinar/`) | Track 172 Ascending (`data/karapinar_p172/`) | Karşılaştırma / Yorum |
|---|---|---|---|
| **Geçiş Saati & Bakış Yönü** | `16:40 UTC` (Batı-Güneybatı'ya bakış) | `02:53 UTC` (Doğu-Kuzeydoğu'ya bakış) | Zıt doğu-batı yatay bakış vektörü; gece (`02:53 UTC`) atmosferi daha sakin |
| **Ortak Tarih Dizisi (9 Tarih)** | `2026-06-26` .. `2026-10-12` (8 çift) | `2026-06-26` .. `2026-10-12` (8 çift) | **Aynı 9 tarih** (`06-26`, `07-08`, `07-20`, `08-01`, `08-25`, `09-06`, `09-18`, `09-30`, `10-12`) |
| **Grid & Çözünürlük** | `470 × 603` px (`EPSG:32636`, 80 m) | `470 × 603` px (`EPSG:32636`, 80 m) | Birebir aynı UTM grid (`33.3°–33.8°E, 37.6°–37.9°N`) |
| **Tam Zincir Geçerli Piksel** | **14.18%** (`40,194 / 283,410` px) | **39.00%** (`110,530 / 283,410` px) | Track 172 gece geçişi **2.75 kat** daha geniş tam zincir koherens alanı sağlıyor |
| **Ortak Geçerli Alan** | `39,242` piksel / `220` adet 1 km blok | `39,242` piksel / `220` adet 1 km blok | Her iki yörüngede $\ge 50\%$ geçerli pikseli olan `220` adet 1 km blok |
| **Referans Noktası** | `[33.7661, 37.7580]` (Yeşilyurt, coh `0.941`) | `[33.7652, 37.7580]` (Yeşilyurt, coh `0.935`) | Aynı kireçtaşı sırtında (`< 80 m` mesafe) ortak referans |
| **Sahne Maksimum Çökme (1 km Blok)** | **`-6.0 cm` LOS** (`-8.1 cm` dikey *estimate*) | **`-6.5 cm` LOS** (`-8.8 cm` dikey *estimate*) | Her iki yörünge de sezon sonu maksimum çökmeyi `-6.0` ile `-6.5 cm` LOS olarak ölçüyor |
| **Aktif Karapınar Çanağı (`p01`, 2 km W of Karapınar)** | **`-5.93 cm` LOS** (`-7.97 cm` dikey *estimate*) | **`-4.73 cm` LOS** (`-6.42 cm` dikey *estimate*) | 9 tarihli zaman serisi korelasyonu **`r = 0.798`**, **`RMSE = 1.25 cm` LOS** |

### 2.2 `tasks/PC8.md` Madde 2 İstenen Çapraz Kontrol Metrikleri (`r`, `RMSE`, `maks fark`)

| Karşılaştırma Kümesi | Örneklem (`n`) | Pearson `r` (LOS) | Pearson `r` (Dikey *Estimate*) | `RMSE` (LOS) | `RMSE` (Dikey *Estimate*) | Medyan Fark (`P172 − P7` LOS) | **Maks Mutlak Fark (`maks fark`, LOS)** | **Maks Mutlak Fark (Dikey *Estimate*)** |
|---|---|---|---|---|---|---|---|---|
| **Aktif Karapınar Çanağı (`p01`) Zaman Serisi** | `9` tarih (`2026-06-26`..`10-12`) | **0.798** | **0.798** | **1.25 cm** | **1.69 cm** | `-0.18 cm` | **1.68 cm** (ara tarih `09-18`) / **1.20 cm** (sezon sonu) | **2.23 cm** (ara tarih) / **1.55 cm** (sezon sonu) |
| **12 Resmi Benchmark Noktası (`data/karapinar/points.json`)** | `12` nokta (`p01`–`p12`) | **0.767** | **0.766** | **1.12 cm** | **1.51 cm** | `-0.34 cm` | **2.34 cm** (`p02`, 3 km W of Oymalı) | **3.20 cm** (`p02`) |
| **Ortak 1 km Bloklar (Tümü, $\ge 50\%$ geçerli)** | `220` blok (1 km $\times$ 1 km) | **0.238** | **0.237** | **1.42 cm** | **1.93 cm** | **`-0.19 cm`** (`-0.24 cm` dikey) | **3.82 cm** | **5.17 cm** |
| **Çöken 1 km Bloklar ($\|\text{Track 7 Dikey}\| > 2\text{ cm}$)** | `76` blok | **0.328** | **0.328** | **1.78 cm** | **2.42 cm** | `-0.84 cm` | **3.82 cm** | **5.17 cm** |
| **Tüm Ortak Geçerli Pikseller (`80 m`)** | `39,242` piksel | **0.337** | **0.335** | **1.53 cm** | **2.07 cm** | `-0.21 cm` | **8.37 cm** | **11.25 cm** |

- **İşaret Uyumu (Sign Agreement):** Track 7'de dikey tahmini `> 2 cm` çöken `76` adet 1 km bloğun **%76.3'ü** (`> 3 cm` çöken blokların **%72.7'si**) Track 172'de de aynı yönlü (negatif/çökme) işaret göstermektedir.
- **Neden 12 Benchmark Noktasında `r = 0.77` iken 220 Blokta `r = 0.24`?**
  1. Ortak geçerli `220` bloğun büyük bölümü, tarım parsellerinin dekorrelasyona uğradığı merkez ovada değil, **doğu kenardaki (`33.70°–33.80°E`) Yeşilyurt–Oymalı kireçtaşı sırtında** kümelenmiştir; bu sırtta gerçek yer hareketi küçük (`0` ile `-2 cm` arası) olduğundan, her iki yörüngenin `~1.0–1.5 cm` atmosferik gürültüsü korelasyonu düşürmektedir.
  2. Zıt yörünge geometrisi (Track 7 alçalan batıya bakış vs. Track 172 yükselen doğuya bakış) doğu-batı yatay hareket bileşenini ve doğu kenar topoğrafik/troposferik rampasını zıt işaretle görmektedir (`p02` 3 km W of Oymalı'da `-2.57 cm` vs `-0.23 cm`, fark `2.34 cm` LOS).
  3. Buna karşılık ana çökme merkezinde (`p01` 2 km W of Karapınar: `-5.93 cm` vs `-4.73 cm` LOS, zaman serisi `r = 0.798`) ve güney havzada (`p04` 6 km SE of Gazi Osman Paşa: `-1.74 cm` vs `-1.69 cm` LOS, fark yalnızca **`0.05 cm`**) iki bağımsız yörünge yüksek uyum göstermektedir.

### 2.3 12 Benchmark Noktası (`data/karapinar/points.json`) Nokta Bazlı Karşılaştırma Tablosu

| Nokta ID | Konum (`name`) | Sınıf (`kind`) | Boylam, Enlem | Track 7 LOS (cm) | Track 172 LOS (cm) | Fark (`P172 − P7`, cm LOS) | Track 7 Dikey *Est.* (cm) | Track 172 Dikey *Est.* (cm) | 9 Tarih Zaman Serisi `r` | Zaman Serisi `RMSE` (cm LOS) |
|---|---|---|---|---|---|---|---|---|---|---|
| **`p01`** | **2 km W of Karapınar** | `most_subsiding` | `33.5306, 37.7182` | **`-5.93`** | **`-4.73`** | `+1.20` | `-7.97` | `-6.42` | **0.798** | **1.25** |
| **`p02`** | 3 km W of Oymalı | `most_subsiding` | `33.7905, 37.7449` | `-2.57` | `-0.23` | `+2.34` *(maks fark)* | `-3.51` | `-0.31` | 0.251 | 1.05 |
| **`p03`** | 5 km NW of Akören | `most_subsiding` | `33.7781, 37.6887` | `-1.82` | `-0.86` | `+0.96` | `-2.49` | `-1.16` | 0.474 | 0.80 |
| **`p04`** | **6 km SE of Gazi Osman Paşa** | `most_subsiding` | `33.5183, 37.6526` | **`-1.74`** | **`-1.69`** | **`+0.05`** *(en yakın)* | `-2.34` | `-2.30` | 0.205 | 1.38 |
| **`p05`** | 2 km S of Ekizli | `most_subsiding` | `33.7910, 37.7917` | `-0.88` | `-0.29` | `+0.59` | `-1.20` | `-0.39` | 0.154 | 0.47 |
| **`p06`** | 7 km N of Kesmez | `median` | `33.7075, 37.7079` | `-0.35` | `-0.94` | `-0.59` | `-0.48` | `-1.26` | -0.114 | 1.47 |
| **`p07`** | 2 km SE of Işıklar | `median` | `33.7796, 37.8387` | `-0.42` | `-0.74` | `-0.32` | `-0.57` | `-0.98` | 0.019 | 1.30 |
| **`p08`** | Meşeli | `median` | `33.7918, 37.8667` | `-0.41` | `-0.97` | `-0.56` | `-0.56` | `-1.29` | -0.151 | 1.19 |
| **`p09`** | 2 km W of Öbektaş | `median` | `33.7440, 37.8201` | `+0.47` | `-1.39` | `-1.86` | `+0.64` | `-1.85` | -0.105 | 1.37 |
| **`p10`** | 3 km E of Yeşilyurt | `median` | `33.7552, 37.7638` | `+0.05` | `+0.31` | `+0.26` | `+0.07` | `+0.41` | **0.521** | **0.26** |
| **`p11`** | 2 km SE of Yeşilyurt | `near_reference` | `33.7433, 37.7545` | `+0.47` | `+0.11` | `-0.36` | `+0.65` | `+0.15` | 0.111 | 0.39 |
| **`p12`** | 4 km SE of Yeşilyurt | `near_reference` | `33.7550, 37.7451` | `-1.30` | `+0.23` | `+1.53` | `-1.77` | `+0.31` | -0.169 | 0.64 |

---

## 3. 15:35 Madde 3 — PC3 / PC9 Yapılacaklar (`docs/qa/*.md` Açık Site Bulguları Özeti — Site Sorumlusu PC3 İçin Tek Liste)

> **Amaç (`tasks/PC8.md` Madde 3 & `tasks/PC3.md` 15:45 devir):** `docs/qa/*.md` (`PC1.md`, `PC3.md`, `PC4.md`, `PC5.md`, `PC6.md`, `PC7.md`, `PC9.md`, `PCQ.md`, `PC8.md`) içindeki tüm site (`web/`, `data/catalog.json`) bulguları taranmış, daha önce kapatılan maddeler ayıklanmış ve **site sorumlusu PC3'ün (ve PC9'un) tek seferde çakışmasız uygulayabileceği açık maddeler** aşağıda öncelik sırasıyla listelenmiştir.

### 3.1 Önceden Kapatılmış Maddeler (PC3/PC9'un Tekrar Dokunmasına Gerek Olmayanlar)
- **[KAPANDI — `653b5f2` / `4d98f3a`]** `web/app.js` içindeki `< 2 cm` cetvel öğeleri (`grain of rice 0.2 cm`, `pea 0.6 cm`, `AAA battery 1.0 cm`) kaldırıldı; cetvel `2.4 cm` (`£1 coin / US quarter`) ile başlıyor ve `NOISE_CM = 1.0` gri gürültü bandı eklendi (`PCQ.md` #3).
- **[KAPANDI — `653b5f2`]** `"four months"` ve `"two tectonic plates"` ifadeleri `web/index.html` ve `web/science.html` içinde `"3½ months"` / `"one summer"` ve `"a major tectonic boundary"` olarak düzeltildi (`PCQ.md` #4–5).
- **[KAPANDI — `653b5f2`]** Renk çubuğu uç etiketleri `≤ −6` ve `≥ +6` olarak güncellendi (`PCQ.md` #8).
- **[KAPANDI — `4d98f3a`]** `data/catalog.json` içine `karapinar`, `uk` ve `uk_clay` bölgeleri eklendi (`PC6.md`).

### 3.2 PC3 / PC9 Yapılacaklar — Açık Site (`web/` & `data/catalog.json`) Maddeleri

1. **[YÜKSEK — `web/index.html` `#ukClay` & `web/science.html` `#limits`] PC8 UK Algılama Sınırı Metni ve `pc8_uk_detection.png` Entegrasyonu (`docs/story/uk_findings.md` & `tasks/PC8.md` Madde 1):**
   - **Durum:** `web/index.html` `#ukClay` bölümü (satır 211–239) şu anda `data/uk_clay/detection.json` verisini metin olarak okuyor ancak `docs/story/media/pc8_uk_detection.png` (`Figure 4`) görselini göstermiyor.
   - **PC9 Aksiyonu:** `docs/story/uk_findings.md` §3 içindeki hazır `<figure class="story-media">` bloğunu (`../docs/story/media/pc8_uk_detection.png`) ve 6 cümlelik sade İngilizce açıklamayı `web/index.html` `#ukClay` içine (veya `web/science.html` `#limits` içine) ekle.

2. **[YÜKSEK — `data/catalog.json` & `web/science.html` `#valid`] Karapınar İkinci Yörünge (`data/karapinar_p172/`) ve `pc8_kp_p7_vs_p172.png` Entegrasyonu (`tasks/PC8.md` Madde 2):**
   - **Durum:** `data/karapinar_p172/` (Track 172 Ascending çapraz kontrol veri seti) ve `docs/story/media/pc8_kp_p7_vs_p172.png` üretildi, ancak `data/catalog.json` ve `web/science.html` `#valid` bölümünde henüz yer almıyor.
   - **PC9 Aksiyonu:**
     - İsteğe bağlı/katalog bütünlüğü için `data/catalog.json` içine `karapinar_p172` girdisini (`path: "karapinar_p172"`, `title: "Karapınar, Türkiye — Ascending Track 172 Cross-Check"`) ekle veya `web/science.html` `#valid` ("1. Two-orbit cross-check") bölümüne Karapınar iki yörünge sonucunu (`12 nokta r = 0.77, RMSE = 1.12 cm LOS; aktif çanak p01 zaman serisi r = 0.80, -5.9 cm vs -4.7 cm LOS`) ve `../docs/story/media/pc8_kp_p7_vs_p172.png` görselini ekle.

3. **[ORTA — `web/style.css` / `web/index.html`] Mobil Görünümde (`390×844`) Yatay Taşma (`docs/qa/PC6.md` satır 100):**
   - **Kaynak Bulgu (`PC6.md`):** Mobil (`390×844`) görünümde `document.documentElement.scrollWidth = 569 px > 390 px` yatay taşma tespit edildi. Taşmaya neden olan iki eleman: Chapter 4 GNSS doğrulama tablosu (`#gnssTable`, `487 px` genişlik) ve oyun kutusu (`#gameBox`, `535 px` genişlik).
   - **PC9 Aksiyonu:** `web/style.css` içinde `#gnssTable` tablosunu saran kapsayıcıya `overflow-x: auto; max-width: 100%; display: block;` ekle ve `#gameBox` / `.game-box` için `@media (max-width: 640px)` altında `max-width: 100%; box-sizing: border-box;` tanımla.

4. **[ORTA — `web/index.html` `#holmeText` & `web/app.js`] Holme Fen Birincil Kaynak Linki ve Yıllık Hız Vurgusu (`docs/qa/PCQ.md` satır 17 & `docs/story/holme_fen.md`):**
   - **Kaynak Bulgu (`PCQ.md` & `PC4` `docs/story/holme_fen.md`):** `web/index.html` satır 228–232'deki `#holmeText` statik metni doğru (`~4 metres since 1848`, `1 to 2 cm per year`), ancak PC4'ün doğruladığı birincil kaynak bağlantıları (`Great Fen Project — Holme Fen Posts` `https://www.greatfen.org.uk/about-great-fen/heritage/holme-fen-posts` ve `UKCEH / Defra Fens Peatland Isotope Project WP2`) tıklanabilir kaynak linki olarak `#ukClay` / `#holmeText` altında yer almıyor.
   - **PC9 Aksiyonu:** `#holmeText` sonuna `docs/story/holme_fen.md` içindeki doğrulanmış kaynak linkini (`Great Fen Project / Wildlife Trust BCN` ve `UKCEH`) ekle; `web/app.js` `renderUkClay()` fonksiyonunun `#holmeText` içindeki bu linki ezmediğinden emin ol.

5. **[DÜŞÜK — `web/science.html` satır 47] Çevrimdışı QA Tarayıcısı İçin Birimsiz Sayı Düzeltmesi (`docs/qa/PC7.md` §3 satır 118):**
   - **Kaynak Bulgu (`PC7.md`):** `web/science.html` satır 47'de `<span data-k="cv.range">−4.7 and −7.8</span> cm` ifadesinde statik HTML içinde `−4.7` sayısından hemen sonra birim yazmadığı için `pipeline/pc7/offline_site_qa.py` statik tarayıcısı `science.html:1` uyarısı veriyor (`app.js` çalışma zamanında `−4.7 cm and −7.8` olarak düzeltiyor).
   - **PC9 Aksiyonu:** `web/science.html` satır 47'deki statik metni `<span data-k="cv.range">−4.7 cm and −7.8</span> cm` olarak güncelle (`offline_site_qa.py` uyarısını `0`'a indirir).

6. **[DÜŞÜK — `web/data.html`] Yeni Üretilen JSON Veri Dosyalarının İndirme Tablosuna Eklenmesi (`docs/qa/PC7.md` & Katalog Tutarlılığı):**
   - **Durum:** `web/data.html` şu anda yalnızca ilk faz dosyalarını (`central_valley`, `karapinar`, `uk` `meta/summary/points.json`) listeliyor; yeni eklenen `data/uk_clay/detection.json`, `data/uk_clay/summary.json`, `data/central_valley/area_stats.json`, `data/karapinar/area_stats.json`, `data/central_valley/exposure.json`, `data/karapinar/exposure.json` ve `data/karapinar_p172/summary.json` dosyaları tabloda yok.
   - **PC3 / PC9 Aksiyonu:** `web/data.html` içindeki "Processed web data" tablosuna bu yeni JSON dosyalarını ekle.

7. **[YÜKSEK — `web/index.html` / `web/science.html` (`tasks/PC3.md` 16:15 Madde 6 — B3)] Nüfus ve Ürün Türü Maruziyeti (`docs/story/exposure.md` & `pc8_exposure.png`) Entegrasyonu:**
   - **Durum:** `data/central_valley/exposure.json`, `data/karapinar/exposure.json`, `docs/story/exposure.md` ve `docs/story/media/pc8_exposure.png` üretildi.
   - **PC3 Aksiyonu:** `docs/story/exposure.md` §5 içindeki hazır `<div class="callout exposure-box" id="exposureBox">` HTML bloğunu (`WorldPop 100 m` nüfus + `USDA CDL 30 m` Central Valley ilk 5 ürün + `ESA WorldCover 10 m` Karapınar ilk 5 arazi sınıfı + `pc8_exposure.png`) ilgili site bölümüne (`tasks/PC3.md` 16:15 Madde 6) bağla.

---

## 4. 16:10 Görev A–B — Teslim Formu Metinleri (`submission_form.md`), Video Altyazısı (`video_subtitles.srt`) ve Seslendirme (`narration_script.md`)

- **`docs/story/submission_form.md`:** `docs/story/submission_rules.md` içindeki 13 resmi Space Apps proje sayfası alanı için kopyala-yapıştır hazır İngilizce metinler, her kutunun tam karakter ve kelime sayısı (`Project Title` `48 / 76 chars`, `High-Level Summary` `146 / 469 chars`, `Detailed Description` `2,384 chars / 348 words`, `How It Works` `1,492 chars`, `Benefits & Impact` `1,068 chars`, `Space Agency Data` `1,089 chars`, `Other Data` `748 chars`, `Tools & Software` `634 chars`, `Technical Challenges` `962 chars`, `AI Disclosure` `692 chars`, `References`) ve `docs/KAYNAKLAR_ANALIZI.md` §1 NASA Land Subsidence StoryMap (2013–2017 UAVSAR → 2026 NISAR) çerçevesi ile oluşturuldu.
- **`docs/story/video_subtitles.srt` & `docs/story/narration_script.md`:** `docs/story/video_shotlist.md` içindeki 6 sahnenin (`00:00.0–00:30.0`) sürelerine birebir oturan standart `.srt` altyazı dosyası ve **76 kelimelik** (`~152 WPM` doğal okuma hızıyla `29.6 saniye`) seslendirme metni oluşturuldu.

---

## 5. 16:15 Challenge Uyumu B3 — Nüfus ve Bitki Örtüsü / Ürün Türü Maruziyeti (`analysis/pc8/exposure.py`)

- **Üretilen Dosyalar:**
  - `analysis/pc8/exposure.py`
  - `data/central_valley/exposure.json`
  - `data/karapinar/exposure.json`
  - `docs/story/exposure.md`
  - `docs/story/media/pc8_exposure.png` (`241.5 KB`, 2 panelli grafik — görsel olarak incelendi, sıfır metin çakışması)
- **Nüfus Maruziyeti (`WorldPop 100 m`, `2020`, `CC BY 4.0`, `estimate`):**
  - **Central Valley (`[-120.2, 35.6, -119.0, 36.6]`, toplam `613,429` kişi):**
    - Çökme **`> 2 cm` LOS (`<= -2.0 cm`):** Doğrudan geçerli InSAR piksellerinde **`71,701` kişi** (`<= 2.5 km` havza enterpolasyonuyla **`78,464` kişi**; dikey *estimate* `> 2 cm` için **`124,561` kişi**).
    - Çökme **`> 5 cm` LOS (`<= -5.0 cm`):** Doğrudan geçerli InSAR piksellerinde **`3,407` kişi** (`<= 2.5 km` havza enterpolasyonuyla **`4,270` kişi**; dikey *estimate* `> 5 cm` için **`7,067` kişi**).
  - **Karapınar (`[33.3, 37.6, 33.8, 37.9]`, toplam `47,621` kişi):**
    - Çökme **`> 2 cm` LOS (`<= -2.0 cm`):** Doğrudan geçerli InSAR piksellerinde **`11,572` kişi** (`<= 2.5 km` havza enterpolasyonuyla **`18,906` kişi**; dikey *estimate* `> 2 cm` için **`13,618` kişi**).
    - Çökme **`> 5 cm` LOS (`<= -5.0 cm`):** Doğrudan geçerli InSAR piksellerinde **`2,214` kişi** (`<= 2.5 km` havza enterpolasyonuyla **`3,481` kişi**; dikey *estimate* `> 5 cm` için **`4,179` kişi**).
- **Ürün ve Arazi Türü Maruziyeti (`km²`):**
  - **Central Valley (`USDA NASS Cropland Data Layer 30 m`, `2021`, `Public Domain`):**
    - `> 2 cm` LOS çöken **`1,579.20 km²`** ortak geçerli alanın **`%79.2`'si (`1,251.37 km²`)** ve `> 5 cm` LOS çöken **`239.84 km²`** alanın **`%91.2`'si (`218.67 km²`)** ekili tarım arazisidir.
    - **İlk 5 ekili ürün (`> 2 cm` LOS / `> 5 cm` LOS):**
      1. **Citrus (Narenciye):** **`355.64 km²` (`%22.5`)** / **`166.59 km²` (`%69.5`)**
      2. **Pistachios (Antep fıstığı):** **`230.92 km²` (`%14.6`)** / **`7.78 km²` (`%3.2`)**
      3. **Fallow / Idle Cropland (Nadas / boş tarla):** **`216.14 km²` (`%13.7`)** / **`10.00 km²` (`%4.2`)**
      4. **Winter Wheat (Kışlık buğday):** **`97.27 km²` (`%6.2`)** / **`5.52 km²` (`%2.3`)**
      5. **Almonds (Badem):** **`73.74 km²` (`%4.7`)** / **`4.71 km²` (`%2.0`)**
      *(6. Grapes `49.88 km²`, 7. Pomegranates `36.95 km²`, 8. Alfalfa `24.56 km²`, 9. Barley `20.46 km²`, 10. Olives `15.79 km²`)*
  - **Karapınar (`ESA WorldCover 10 m v200`, `2021`, `CC BY 4.0`):**
    - **İlk 5 arazi sınıfı (`> 2 cm` LOS ortak geçerli `28.69 km²` / `> 5 cm` LOS `3.10 km²` / `<= 2.5 km` enterpolasyonlu havza `141.08 km²`):**
      1. **Grassland (Step / mera):** **`16.54 km²` (`%57.7`)** / **`1.15 km²` (`%36.9`)** / havza geneli `58.79 km²` (`%41.7`)
      2. **Built-up (Yerleşim ve yol dokusu):** **`7.24 km²` (`%25.2`)** / **`1.34 km²` (`%43.3`)** / havza geneli `8.65 km²` (`%6.1`)
      3. **Bare / sparse vegetation (Çıplak / seyrek karstik yüzey):** **`3.92 km²` (`%13.7`)** / **`0.43 km²` (`%13.8`)** / havza geneli `47.46 km²` (`%33.6`)
      4. **Tree cover (Ağaç örtüsü):** **`0.57 km²` (`%2.0`)** / **`0.10 km²` (`%3.3`)** / havza geneli `0.67 km²` (`%0.5`)
      5. **Cropland (Ekili tarım alanı):** **`0.42 km²` (`%1.4`)** / **`0.08 km²` (`%2.7`)** / havza geneli **`24.99 km²` (`%17.7`)** *(yaz sulaması altındaki dairesel pivot tarlalar L-band koherensini kaybettiğinden doğrudan geçerli piksellerde düşük, enterpolasyonlu çökme çanağında `24.99 km²`)*

---

## 6. Önceki Kontroller — Fens (`pipeline/subset/fens`) ve `docs/story/media/` Boyut Kontrolü (K-12)

- **Fens (`pipeline/subset/fens`) Kontrolü:** `pipeline/subset/` altında yalnızca `central_valley`, `karapinar`, `karapinar_p172` ve `uk_clay` alt kümeleri bulunmaktadır; `fens` GUNW alt kümesi yoktur. Holme Fen karşılaştırması `docs/story/holme_fen.md` literatür hızı (`1–2 cm/yıl`) üzerinden `docs/story/uk_findings.md` ve `docs/story/media/pc8_uk_detection.png` içine dahil edilmiştir.
- **`docs/story/media/` Boyut Kontrolü (K-12):** Orijinal 25 medya dosyası + PC8 tarafından üretilen 2 yeni PNG (`pc8_uk_detection.png` `190.0 KB`, `pc8_kp_p7_vs_p172.png` `264.3 KB`) dahil toplam **27 dosya** kontrol edildi; hiçbir dosya **0 bayt** veya **20 MB** sınırının üzerinde değildir.

---

## 7. 14 Nov 2026 Akşamı Madde 3 — Konya Ovası (`konya_plain`) Nüfus ve Arazi Maruziyeti (`data/konya_plain/exposure.json`)

- **Üretilen / Güncellenen Dosyalar:** `analysis/pc8/exposure.py`, `data/konya_plain/exposure.json`, `data/karapinar/exposure.json`, `data/central_valley/exposure.json`, `docs/story/exposure.md`, `docs/story/media/pc8_exposure.png` (3 panelli grafik).
- **Konya Kapalı Havzası (`[32.4, 37.4, 33.9, 38.1]`, `2026-06-26` → `2026-10-12`, 8 Track 7 çifti):**
  - **WorldPop 100 m (`2020`, `estimate`):** Havza BBox toplamı `868,371` kişi (`444,542` geçerli InSAR pikseli). **`> 2 cm` LOS:** **`69,854`** kişi (`118,485` `<= 2.5 km` enterpolasyonlu; `79,261` dikey *estimate*). **`> 5 cm` LOS:** **`16,822`** kişi (`33,700` enterpolasyonlu; `32,016` dikey *estimate*).
  - **ESA WorldCover 10 m (`2021 v200`, `N36E030` + `N36E033`):** `> 2 cm` LOS ortak geçerli (`627.18 km²`): Grassland `284.91 km²` (`45.4%`), Cropland `173.10 km²` (`27.6%`), Bare/sparse `127.51 km²` (`20.3%`), Built-up `40.69 km²` (`6.5%`), Tree cover `0.77 km²` (`0.1%`). `> 5 cm` LOS (`99.47 km²`): Cropland `36.28 km²` (`36.5%`), Grassland `32.70 km²` (`32.9%`), Bare/sparse `21.13 km²` (`21.2%`), Built-up `9.16 km²` (`9.2%`). Enterpolasyonlu `> 2 cm` havza (`2,157.67 km²`): Cropland `1,167.69 km²` (`54.1%`).
