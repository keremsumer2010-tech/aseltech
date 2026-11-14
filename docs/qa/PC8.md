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

---

## 8. 14 Nov 2026 Akşamı Madde 4 — `docs/MASTER_PLAN.md` §9 Teslim Kontrol Listesi Doğrulaması

| # | `docs/MASTER_PLAN.md` §9 Maddesi | Durum | Doğrulama Kanıtı ve Açık Kalanlar |
|---|---|---|---|
| 1 | Proje sayfası İngilizce, tüm alanlar dolu (özet, nasıl çalışır, faydalar, hedefler, araçlar) | **HAZIR** | `docs/story/submission_form.md` içindeki 13 Space Apps alanı (16 `text` bloğu) tamamen İngilizce dolduruldu; karakter/kelime sınırları Python ile doğrulandı; `TBD`/`TODO` placeholder taraması `0` sonuç verdi (`[]`). |
| 2 | Demo: ≤30 sn video (İngilizce altyazı) VEYA ≤7 slayt; link herkese açık | **SLAYT HAZIR / VİDEO BEKLEMEDE** | `docs/story/slides.html` tam **7 slayt** (`<section class="slide"> = 7`), `docs/story/slides_notes.md` konuşmacı notları hazır. Video yolu için `docs/story/video_subtitles.srt` ve `docs/story/narration_script.md` hazır (video dondurulmuş durumda; sunumda canlı/PDF slayt linkinin herkese açık paylaşılması yeterli). |
| 3 | Repo linki ve canlı site linki herkese açık | **KISMEN AÇIK** | GitHub repo linki (`https://github.com/keremsumer2010-tech/aseltech`) `web/index.html`, `web/science.html`, `web/data.html` ve `docs/story/slides.html` içinde mevcut; ancak **canlı deploy URL'si** (GitHub Pages / Vercel) PC1/PC3 tarafından yayına alındıktan sonra teslim formuna eklenecek. |
| 4 | Kullanılan NASA verisi ve diğer kaynaklar listelendi | **HAZIR** | NASA-ISRO NISAR (provisional + NASA-JPL/ISRO kalibrasyon notu), OPERA DISP-S1, SMAP/IMERG, WorldPop 100 m (`CC BY 4.0`), USDA CDL 30 m (`Public Domain`), ESA WorldCover 10 m (`CC BY 4.0`) ve USGS/NGL GNSS kaynakları `submission_form.md`, `web/data.html`, `web/science.html` ve `docs/story/exposure.md` içinde listelendi. |
| 5 | Yapay zekâ kullanımı açıklandı (Claude, Gemini, Higgsfield — neyi ürettikleri) | **PC1 ONAYI BEKLİYOR** | `docs/story/submission_form.md` §AI Disclosure alanı ve `web/index.html` / `web/science.html` / `docs/story/slides.html` içinde Claude, Gemini ve Higgsfield açıklamaları mevcut; `MASTER_PLAN.md` §9 gereği son resmi metin onayı PC1 tarafından verilecek. |
| 6 | NASA logosu yok; AI görselleri etiketli | **GEÇTİ (`0` NASA logosu)** | 9 HTML dosyası (`web/*.html`, `game/*.html`, `docs/story/slides.html`) tarandı: `NASA_LOGO_HITS: 0`, gizli anahtar taraması `SECRET_HITS: 0`, `docs/story/media/` (`41` dosya) `BAD_MEDIA: 0`. `web/index.html`, `web/science.html` ve `slides.html` içinde AI üretimi/desteği etiketli. |
| 7 | Teslim saati: Pazar 23:59 UK = Pazartesi 02:59 TR — hedef Pazar 22:00 TR | **TAKİPTE** | `python -m pytest -q`: **`63 passed, 1 warning`**; `data/**/*.json` (`60` dosya): **`BAD_JSON: 0`**. Aşağıdaki 2 web hatası PC3/PC9 için kaydedildi. |

---

## 9. Hata Ayıklama Bulguları (`ASLA BOŞ KALMA` İlk Turu — Diğer PC Dosyalarına Dokunmadan)

1. `web/index.html` (satır 117) -> `<img src="" data-src="docs/story/media/pc9_fullyear_point.png" ...>` kırık görsel yolu ve boş `src` (`web/app.js` içinde `data-src` işleyicisi yok; ayrıca `web/` altından göreli yol `../docs/story/media/pc9_fullyear_point.png` olmalı) -> **Nasıl tekrar edilir:** `web/index.html` dosyasında `pc9_fullyear_point.png` görselini arayın veya yerel sunucuda `http://localhost:8000/web/index.html` açıp Chapter 2 figürünün yüklenmediğini (404 / boş `src`) gözlemleyin.
2. `web/explorer.html` -> Sayfada NISAR provisional veri / NASA-JPL & ISRO kalibrasyon uyarısı metni bulunmuyor (`cal=False`) -> **Nasıl tekrar edilir:** `web/explorer.html` içinde `"calibration"` veya `"provisional"` araması yapın (0 eşleşme).
3. `python -m pytest -q` -> **`63 passed, 1 warning`** (`analysis/cumulative.py:127` `cmap.set_bad` PendingDeprecationWarning); `60` adet `data/**/*.json` dosyasında sözdizimi veya `NaN/Infinity` hatası yok (`BAD_JSON: 0`).
4. **[DÜZELTİLDİ — `docs/qa/PC6.md` satır 179 bulgusu]** `analysis/pc8/plot_uk_detection.py` güncellenerek `docs/story/media/pc8_uk_detection.png` Panel B'deki lejant `loc="center right"` (`xlim(0, 6.8)`) konumuna alındı (sıfır metin çakışması görsel olarak doğrulandı) ve 3 yıllık `3σ` hız eşiği tüm etiketlerde **`1.21 cm/yr (est.)`** olarak tekilleştirildi.
5. **PC8 `REVIEW_1500.md` Taraması (`14 Nov 19:55 TR`):** `docs/story/{submission_form,slides_notes,exposure,uk_findings,narration_script}.md` dosyalarının tamamında yasaklı pazarlama/abartı kelimesi ve ünlem işareti **`0` eşleşme**.

---

## 10. 20:00 PC1 Görevleri — Veri Düzeltmeleri ve `MASTER_PLAN.md` §9 Kapanış Yapılacaklar Listesi

- **Madde 1 (`analysis/pc8/fix_nan_json.py`):** `data/**/*.json` üzerinde `NaN` / `Infinity` / `-Infinity` -> `null` dönüştüren idempotent temizleyici yazıldı ve çalıştırıldı (`60` JSON tarandı, `0` bozuk sabit kaldı).
- **Madde 2 (`data/central_valley_s1/cross_sensor.json`):** Eksik `"quality": "mixed"` alanı ve OPERA L3 DISP-S1 + NGL GNSS + provisional NISAR kaynağını belirten `quality_note` eklendi.
- **Madde 3–4 (`docs/story/submission_form.md` & `docs/story/slides_notes.md`):** AI beyanı PC1 metniyle (Claude Code, Gemini/Antigravity/Gemini CLI, Codex; sıfır AI görseli, erken Higgsfield taslakları kaldırıldı) kesinleştirildi; Beijing (`-1.4 cm` LOS) ve Konya Closed Basin maruziyeti (`69,854` kişi `> 2 cm` LOS) eklendi.
- **Madde 5 — `MASTER_PLAN.md` §9 "KISMEN" ve "BEKLİYOR" Maddelerini Kapatma Yapılacaklar Listesi:**
  - [ ] **Demo Slayt Güncellemesi (PC4):** `docs/story/slides.html` (7 slayt) içine `docs/story/slides_notes.md` tablosundaki Cumartesi akşamı bulgularını (`central_valley_fullyear`, `delta`, `konya_plain`, `karapinar_p172`, `global` 4 şehir, `exposure` + `storage_loss`) işle ve tarayıcıda PDF'e basarak 7 sayfa taşma kontrolü yap.
  - [ ] **Canlı Site & Demo URL Doğrulaması (PC1 / PC3):** GitHub Pages / Vercel deploy URL'sini (`https://keremsumer2010-tech.github.io/aseltech/web/` ve `/docs/story/slides.html`) gizli sekmede `HTTP 200` olarak doğrula; `submission_form.md` §3–§4 içindeki bağlantılarla birebir eşleştir.
  - [ ] **Web Hatalarının Kapatılması (PC3 / PC9):** `web/index.html:117` (`pc9_fullyear_point.png` boş `src=""` ve eksik `../` yolu) ile `web/explorer.html` eksik NISAR kalibrasyon/provisional notunu kapat.
  - [ ] **AI Kullanım Beyanı Son Eşitleme (PC1):** `submission_form.md` §12 içindeki kesinleşmiş PC1 AI beyanını portal formuna birebir kopyala (site/oyun AI görseli = 0, kod/metin = Claude, Gemini, Codex).
  - [ ] **Pazar 22:00 TR Ön-Teslim Son Kontrolü (PC8):** Tüm portaldaki alanlar doldurulduktan sonra son `pytest`, JSON temizliği ve link kontrolünü tekrar çalıştır.

---

## 11. 20:10 Özgün Katkı O1 — Central Valley Kalıcı Akifer Depolama Kaybı (`km³/yıl`)

- **Üretilen Dosyalar:** `analysis/pc8/storage_loss.py`, `analysis/pc8/test_storage_loss.py`, `data/central_valley_fullyear/storage_loss.json`, `docs/story/storage_loss.md`, `docs/story/media/pc8_storage_loss.png`.
- **Sonuçlar (`2025-11-24` → `2026-10-14`, `mixed` 25 çift, medyan geliş açısı `41.53°`):**
  - `> 1.0 cm/yr` kalıcı dikey çökme alanı (`4,508.29 km²`, ortalama `7.041 cm/yr` dikey): **`0.3174 km³/yr`** (`317.41 milyon m³/yr`).
  - Tüm geçerli pikseller (`5,384.88 km²`, `%46.04` geçerli): **`0.3110 km³/yr`** net kayıp.
  - **Belirsizlik (3 referans + 1 km blok SE):** **`0.0664 – 0.3198 km³/yr`** (`Main ref`: `0.2891–0.3174`, `Alt ref 1`: `0.0688`, `Alt ref 2`: `0.0774`; `se_block = 0.00123 km³/yr`).
  - **Karşılaştırmalar:** Millerton Lake (Friant Dam, `0.642 km³`) kapasitesinin **`0.49×`**'i / yılda **`126,966` Olimpik yüzme havuzu (`2,500 m³`)**; Smith et al. (2017) Güney San Joaquin `0.414–0.748 km³ / 3 yıl` (`0.138–0.249 km³/yr`) ile aynı büyüklük mertebesi.
  - **Birim Testi (`analysis/pc8/test_storage_loss.py`):** Sabit `-5.0 cm/yr` × `64.0 km²` (`100×100` piksel) → tam `0.0032 km³/yr` (`PASSED`).
  - **Karapınar Tam Yıl:** `data/karapinar_fullyear/decomp.json` henüz oluşmadığı için Karapınar tam yıl depolama kaybı sonraki döngüde eklenecek.

---

## 12. 14 Nov 20:15 TR — Tur 3 HTTP & Bağlantı QA Taraması

- **Yerel HTTP Sunucusu (`http.server`) Taraması:** `web/{index,science,data,explorer,faq}.html`, `game/index.html` ve `docs/story/slides.html` sayfalarının **7/7'si `HTTP 200`** döndü; yalnızca §9'da zaten kayıtlı `web/index.html:117` (`docs/story/media/pc9_fullyear_point.png`) `404` veriyor, diğer tüm gömülü göreli kaynaklar `200 OK`.
- **PC8 Markdown Bağlantıları:** `submission_form.md`, `slides_notes.md`, `exposure.md`, `storage_loss.md`, `uk_findings.md` içinde **`0` kırık göreli link**.
- **`submission_form.md` & `slides_notes.md` Senkronu:** O1 kalıcı akifer depolama kaybı (`0.317 km³/yr`, `0.066–0.320 km³/yr`, `~0.49× Millerton Lake`) §5 ve Slide 3 güncelleme notuna eklendi (`§5: 4,654 chars / 689 words`).

---

## 13. 14 Nov 20:26 TR — Tur 4 Sürekli QA & Güncelleme

- **`python analysis/pc8/fix_nan_json.py`:** `data/**/*.json` altındaki **`61` JSON** dosyası tarandı (`0` `NaN`/`Infinity` sabiti).
- **`python -m pytest -q`:** **`70 passed, 1 warning in 22.21s`**.
- **§9 Madde 1 Netleştirme (`docs/qa/PC7.md` §7 ile teyit):** `web/index.html:117` içindeki `data-src="docs/story/media/pc9_fullyear_point.png"` çalışma zamanında `web/app.js` `fullYear()` fonksiyonu tarafından `ROOT + im.dataset.src` ile çözülüyor; sorun yalnızca boş `src=""` niteliğinin tarayıcı/statik tarayıcıda ekstra sayfa isteğine yol açmasıdır (yalnızca `src=""` niteliği kaldırılmalı).
- **Karapınar Tam Yıl (`data/karapinar_fullyear/decomp.json`):** Henüz oluşturulmamış (`False`), sonraki döngüde kontrol edilecek.

---

## 14. 14 Nov 20:36 TR — Tur 5 QA & `docs/qa/PC4.md` `REVIEW_1500.md` Bulgularının Kapatılması

- **[DÜZELTİLDİ — `docs/qa/PC4.md` satır 279–281]:** PC4'ün kardeş dosya `REVIEW_1500.md` taramasında PC8 dosyaları için bildirdiği ifadelerin tamamı temizlendi:
  - `docs/story/narration_script.md` L28 & L41: `calibrated by NASA-JPL and ISRO` → `calibration by NASA-JPL and ISRO`
  - `docs/story/slides_notes.md` L25 (`proves` → `shows`), L33 (`Ground Truth` → `GPS Comparison`), L48 (`calibrated to` → `matched to`), L54 (`calibrated by` → `calibration and validation are carried out by`)
  - `docs/story/submission_form.md` L33: `validated against 10 GPS stations` → `compared against 10 GPS stations` (`492 chars / 73 words`)
- **`docs/story/slides.html` & `docs/story/technical_note.html` Link Taraması:** `0` kırık göreli bağlantı.
- **`python -m pytest -q`:** **`70 passed, 1 warning in 22.41s`**.

---

## 15. 14 Nov 20:46 TR — Tur 6 QA (`validate_json.py`, Web Kapanışları & `pytest`)

- **Önceki Web Bulguları Kapandı (`c2b40e1` & `b24925c`, PC7):** §9'da bildirilen `web/index.html:117` (`pc9_fullyear_point.png` `src` düzeltmesi) ve `web/explorer.html` kalibrasyon/provisional uyarısı eksiklikleri PC7 tarafından kapatıldı; §10'daki ilgili "Web Hatalarının Kapatılması" maddesi tamamlandı.
- **`python pipeline/pc7/validate_json.py`:** `61` JSON dosyası tarandı (`Parse errors: 0`, `Non-finite numeric values: 0`, `Missing quality field: 0`).
- **`python analysis/pc8/fix_nan_json.py`:** `61/61` JSON temiz.
- **`python -m pytest -q`:** **`70 passed, 1 warning in 23.41s`**.

---

## 16. 14 Nov 20:57 TR — `docs/ATLAS_PLANI.md` PC8 Görevleri (`tools/bulletin.py` & `submission_form.md`)

- **Operasyonel Erken Uyarı Bülteni (`tools/bulletin.py` + `analysis/pc8/test_bulletin.py`):**
  - `data/global/atlas.json` içindeki tüm aktif bölgeler için yazdırılabilir tek sayfalık HTML bültenleri (`docs/bulletins/<bölge>.html` + `docs/bulletins/index.html`) üreten araç yazıldı; `O2` (`assets_prob.json`) gelince otomatik okuyacak biçimde tasarlandı, mevcut durumda `assets.json` ilk 5 segmenti, `points.json` son çift adımı, `validation.json` GNSS uyumu, `exposure.json` ve `disp/<son_tarih>.png` haritalarını içeriyor.
  - Üretilen **8 bölge bülteni** (`konya_plain`, `central_valley`, `jakarta`, `karapinar`, `mexico_city`, `tehran`, `beijing`, `delta`) + `index.html`: tüm gömülü görsel/link kontrollerinde **`0` kırık bağlantı**.
  - `analysis/pc8/test_bulletin.py`: `1 passed in 0.24s`.
- **`docs/story/submission_form.md`:** `data/global/atlas.json` (8 aktif bölge sıralaması) ve `tools/bulletin.py` (`docs/bulletins/*.html`) eklendi (`§5: 5,239 chars / 746 words`, `§6: 1,956 chars / 256 words`).
- **O1 Karapınar Durumu:** `data/karapinar_fullyear/decomp.json` henüz oluşturulmamış (`False`), sonraki `git pull` döngülerinde takip edilecek.

---

## 17. 14 Nov 21:08 TR — Tur 8 QA: `O2` Olasılıksal Risk & `ATLAS_PLANI.md` 21:05 Kalite Standardı

- **`tools/bulletin.py` Güncellemesi:**
  - `data/central_valley/assets_prob.json` gerçek O2 şemasına (`beta_max`, `p_beta_exceed` `{'1/500', '1/1000'}`, `max_differential_cm`, `p_diff_gt_10cm`, `ci90`) uyarlandı; `docs/bulletins/central_valley.html` artık en riskli 5 koridor için `Max Diff (90% CI)`, `Beta Max`, `P(Diff > 10 cm)` ve `P(Beta > 1/1000 | 1/500)` tablolarını basıyor, diğer bölgeler `assets.json` tablosuna düşüyor.
  - `docs/ATLAS_PLANI.md` **21:05 Kalite Standardı** uygulandı: dönem uzunluğundan bağımsız **`rate_cm_per_100d`** ana metrik olarak eklendi (`docs/bulletins/index.html` bu metriğe göre sıralanıyor; `rate_cm_per_yr_estimate` ikincil tahmine alındı) ve her bültene/satıra **`confidence` (`HIGH` / `MEDIUM` / `LOW (indicative only)`)** rozeti eklendi.
- **Doğrulama:**
  - `python tools/bulletin.py`: 8 bölge HTML bülteni + `docs/bulletins/index.html` yeniden üretildi (`9` HTML dosyasında **`0` kırık bağlantı**).
  - `analysis/pc8/test_bulletin.py`: `cm/100d`, `CONFIDENCE:` rozeti, `assets_prob.json` / `Beta Max` kontrolleri eklendi.
  - `python -m pytest -q`: **`74 passed, 1 warning in 22.80s`**.
- **O1 Karapınar Durumu:** `data/karapinar_fullyear/decomp.json` henüz oluşturulmamış (`False`), sonraki 10 dakikalık döngüde izlenmeye devam edecek.

---

## 18. BUGFIX Kayıtları (Cmt 22:00+)

- **B01 (S-18 Kritik):** `web/app.js` `hero()` içinden `'h'` görüntü kaynağı, `'h'` raster katmanı ve `updateImage` döngüsü kaldırıldı (yalnızca uydu altlığı bırakıldı). `web/index.html` `.hero-caption` metni `Background: Central Valley, California (satellite basemap).` olarak güncellendi. Test: `http://localhost:8765/web/` üzerinde headless Chrome (`375x812`, `--dump-dom`) ile konsol/render doğrulaması yapıldı.
- **B02 (S-22 Kritik):** `web/app.js` içinde hero dönme `setInterval` kaldırıldı; `hero()` ve `storyMap()` haritalarına `fadeDuration: 0, renderWorldCopies: false` eklendi; `storyMap()` `IntersectionObserver` (`rootMargin: '300px'`) ile tembel başlatmaya alındı; `cvControls()` içinde sadece sonraki kare (`(i + 1) % n`) ön-yüklenir yapıldı; `J()`, `findings()` ve `web/index.html` `ok()` çağrılarından `cache: 'no-cache'` kaldırıldı; `web/index.html` `#cvVideo` etiketine `preload="none"` verildi (`autoplay` kaldırıldı); `.github/workflows/pages.yml` içine yalnızca `_site` kopyasını sıkıştıran (`128` renk PNG + `quality=82` JPG, repodaki orijinallere dokunmayan) Pillow optimizasyon adımı eklendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B03 (S-06 Kritik):** `web/index.html` ana sayfa `−7.8 cm` istatistik kartının altına `<small data-k="cv.range"></small>` eklendi ve `web/app.js` `load()` içinde `data/central_valley/summary.json` `range_cm` alanından dinamik olarak `range −4.7 to −7.8 cm depending on reference area` yazdırıldı. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B04 (S-13 Kritik):** `web/index.html` `#mapLegend` içine `.lg-note#lgGapNote` ("Gaps: no reliable radar signal (fields ploughed, irrigated or flooded between passes), not \"no sinking\".") ve `web/style.css` içine `.lg-note` stili eklendi; Chapter 3 Corcoran metni `(partly hidden by gaps where irrigated or ploughed fields lost radar coherence)` ifadesiyle güncellendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B05 (S-08 Kritik):** `web/app.js` içinde UK sahnesine aynı günün bulutlu VIIRS görüntüsü (`uk-opt`) bbox'a oturtuldu, `step === 'uk'` iken bulutsuz uydu altlığı (`sat`) opaklığı `0.14` düzeyine düşürüldü ve `VIEWS.uk.tag` ile `web/index.html` Figure 1 altyazısına `cloud-free mosaic from other dates` notu eklendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B06 (S-03 Yüksek):** `web/index.html` `#cvVideo` Figure 0 altyazısına ve `#mapLegend` içine `.lg-note#lgBlueNote` (`Blue = less sinking than the stable reference area; changes under about ±2 cm are within the noise.`) eklendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B07 (S-25 Yüksek):** `data/central_valley/meta.json` tarihlerinden Track 34 çift aralıkları `[12, 12, 24, 12, 12, 12, 24]` gün olarak doğrulandı; `web/science.html` satır 47 `12 to 36 days` → `12 to 24 days` yapıldı (cümle yalnızca track 34 için). Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/science.html` doğrulandı.
- **B08 (S-07 Orta):** `web/app.js` içinde `CLOSE_NOISE_CM = 3.0` eklendi ve `pickPoint()` tıkla-oku çıktısı `1.0–3.0 cm` aralığı için `"small change, close to the noise"` verecek biçimde güncellendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B09 (S-12 Orta):** `web/style.css` `.cmp-l,.cmp-r` seçicisinde eksik olan `color:#fff; z-index:2;` eklendi; `web/index.html` etiketleri `VIIRS 20 Oct · cloud` ve `NISAR 20 Oct · radar` yapıldı; `web/app.js` `compare()` içinde `r.value = 50` ile çizginin her açılışta ortada (`50%`) başlaması sağlandı. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B10 (S-09 Orta):** `web/index.html` Figure 1 altyazısına DHDH (HH/HV) radar renklerinin sade açıklaması (`false-colour HH/HV polarisations: bright = rough surfaces and buildings, dark = smooth water and bare fields`) eklendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B11 (S-10 Orta):** `web/app.js` içinde `uk-opt` ve `uk-radar` katmanlarına `maxzoom: 11` eklendi ve `show()` içinde `step === 'uk'` iken `map.setMaxZoom(10.5)` (diğer adımlarda `18`) uygulanarak 700×500 önizleme PNG'sinin aşırı yakınlaştırmada pikselleşmesi engellendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B12 (S-11 Orta):** `web/app.js` içinde UK bbox çevresine ince çerçeve (`uk-frame` line katmanı) ve `The Wash` `[0.250, 52.880]`, `Peterborough` `[-0.248, 52.574]`, `King's Lynn` `[0.395, 52.752]`, `Holme Fen` `[-0.217, 52.483]` için yalnızca `step === 'uk'` iken görünen `maplibregl.Marker` (`.uk-lbl` stili `web/style.css`) etiketleri eklendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` doğrulandı.
- **B13 (S-30 Orta):** `http://localhost:8765/web/science.html` tarayıcı çıktısında `$n$`, `$r$`, `$\theta$`, `$R^2$`, `$N=7$` ham LaTeX ve tablo satırlarındaki `` `|...|` `` mutlak değer dik çizgileri yüzünden kırılan `**Moving (`|max > 2 cm`)**` ile `| Station | Regime | ... |` tabloları tespit edildi. `web/science.html` içinde `marked.parse` ön-işleyicisi eklenerek tablo satırlarındaki backtick içi `|` → `&#124;` kaçışlandı ve satır içi `$...$` ifadeleri HTML/Unicode'a dönüştürüldü. Test: headless Chrome (`375x812`, `--dump-dom`) ile 0 ham `**` / `$...$` / kırık tablo doğrulandı.
- **B14 (S-16 Düşük):** `web/app.js` `pickPoint()` Chart.js grafiğine `cvDateLine` eklentisi (seçili `cvIdx` tarihinde kesikli lacivert dikey çizgi) ve `cvControls()` `go()` içine `chartP.update('none')` eklendi. Test: headless Chrome (`375x812`, `--dump-dom`) ile `http://localhost:8765/web/` `#pointChart` çizimi doğrulandı.
- **B33 (S-33 Yüksek):** `web/app.js` `load()` içine `validation/gnss_stations.csv` (`source_url` eşlemesi), `docs/story/holme_fen.md` (`The Great Fen` bağlantısı) ve `data/uk_clay/meta.json` (`bbox` + `source`) eklendi; `.github/workflows/pages.yml` içine `validation/gnss_stations.csv` kopyası eklendi. `storyMap()` içinde `cv-pts` ("NISAR measurement point", dönem sonu değeri, ASF GUNW linki), `gnss` ("GPS reference station", r/RMSE, `gnss_stations.csv` Nevada Geodetic Laboratory linki), `risk` (`assets.json` `license` + OSM Telif linki) ve UK bölümüne 3 tıklanabilir işaret (`Holme Fen`, `NISAR GCOV frame`, `London Clay` — `.uk-lbl.uk-pin` `web/style.css`) eklendi. Test: tüm 5 kaynak URL'si HTTP 200 doğrulandı (`nisar.asf.earthdatacloud.nasa.gov/BROWSE/...` 403 döndüğü için `https://nisar-docs.asf.alaska.edu/gcov` kullanıldı), `http://localhost:8765/web/` ve `#story` üzerinde headless Chrome (`375x812`) 0 JS hatası ve tüm 8 veri uç noktası HTTP 200 doğrulandı.
- **B34 (S-34 Yüksek):** Sekme değiştirip dönünce kaydırma donması için kök nedenler tespit edilip düzeltildi: (1) `web/style.css` içinde genel `html{scroll-behavior:smooth}` kaldırıldı ve `web/app.js` içinde yalnızca `a[href^="#"]` bağlantı tıklamalarında JS `scrollIntoView({behavior:'smooth'})` kullanıldı; (2) `document.visibilitychange` dinleyicisi eklendi: sekme gizliyken `map?.stop()`, `heroVideo?.pause()`, `cvVideo?.pause()` çalışıyor, `show()` ve `cvControls` oynatma zamanlayıcısı `document.hidden` iken atlanıyor (sekme görünür olunca `heroVideo` devam ediyor); (3) `storyMap()` haritasına `scrollZoom: false` yanına `cooperativeGestures: true` eklendi; (4) `extras()` içinde simülatör iframe'i açıldığında odağı kilitleyen `f.focus()` kaldırıldı. Test: `http://localhost:8765/web/` ve `#story` üzerinde headless Chrome (`375x812` mobil ve `1280x800` masaüstü) 0 JS hatası doğrulandı.
- **C01 (Atlas Sayfası):** `web/atlas.html`, `web/atlas.js`, `web/atlas.css` oluşturuldu ve `.github/workflows/pages.yml` içine `docs/bulletins` kopyası eklendi. Sabit `maplibre-gl@5.3.0` küre projeksiyonu (2D yedekli), `../data/global/atlas.json` noktaları (`rate_cm_per_100d` renk/sıra), güven rozeti (`low` → `indicative only`), tıklanınca yan panelde dönem, çift sayısı, geçerli piksel oranı, referans aralığı, `meta.json` kaynak bilgisi, son tarih `disp/*.png` haritası ve mevcutsa `docs/bulletins/<id>.html` bağlantısı eklendi; `null`/`NaN` alanlara karşı korumalı. Test: `http://127.0.0.1:8766/web/atlas.html` üzerinde headless Chrome (`375x812` ve `1280x800`) 0 JS hatası, `Konya Plain`, `indicative only` rozetleri ve `Open bulletin` bağlantısı doğrulandı.
- **C02 (Atlas Sıralama Tabloları):** `web/atlas.html`, `web/atlas.js` (`renderTables()`) ve `web/atlas.css` içine `"Fastest-sinking places in our 2026 NISAR atlas"` bölümü eklendi: `Reliable measurements` (`6` bölge) ve `Indicative only (low confidence)` (`5` bölge) olmak üzere iki ayrı tablo, `cm/100d, LOS` hızı, dönem, `LOS` ve `provisional` kalibrasyon uyarısı ile; satıra tıklanınca kürede o bölgeyi seçip yukarı kaydırıyor. Test: `http://127.0.0.1:8766/web/atlas.html` üzerinde headless Chrome (`375x812` ve `1280x800`) 0 JS hatası, her iki tablonun eksiksiz dolduğu doğrulandı.
- **C04 (Atlas Sayfası QA Testi):** `web/atlas.html#isfahan`, `#jakarta` ve `#konya_plain` üzerinde `375x812` (telefon) ve `1440x900` (dizüstü) headless Chrome testi yapıldı. Boş `country` (`Isfahan`) için görülen `<h2>Isfahan ()</h2>` ve liste alt satırındaki baştaki `·` ile `null` alanlarda görülen `— cm` birimli gösterimi `web/atlas.js` içinde `fmtUnit()` ve koşullu `country` biçimlendirmesiyle düzeltildi. Yeniden testte: `375x812` ve `1440x900` görünümlerinde `0` JS/konsol hatası, `0` `NaN` çıktısı doğrulandı.

---

## 19. ATLAS FİNAL Kayıtları (`tasks/PC8.md` Paz 00:20, PC1)

- **Madde 1 (`data/global/exposure_atlas.json`, `docs/story/exposure.md` §6):**
  - JRC `GHSL GHS-POP E2025 R2023A 4326_3ss` (100 m, açık erişim) karoları `raw/ghsl/` altına indirilip (`git`'e eklenmeden) `data/global/atlas.json` içindeki tüm **13 bölge** için ortak geçerli InSAR kümülatif LOS yer değiştirmesi (`pipeline/subset/*` ve `analysis/out/*_cum.npz`, `108` güne ölçeklenmiş) ile kesiştirildi.
  - `data/global/detectability.json` içindeki şehir bazlı `2 * sigma` gürültü tabanı (`0.588`–`0.728 cm`; Mashhad için Cramér-Rao `0.634 cm`) altındaki pikseller sayılmadı.
  - Yuvalanmış `karapinar` alt kümesi çift sayımı önlemek için küresel toplamlardan hariç tutuldu: `474.26 km²` (`< -5 cm / 108 gün`), `1,434,355` kişi (`< -5 cm / 108 gün`), `7,151,872` kişi (`< -2 cm / 108 gün`). Yöntem `docs/story/exposure.md` §6 altına yazıldı. Commit: `b11db53`.
- **Madde 2 (`data/global/vital_signs.json`):**
  - `cities_measured: 13`, `fastest: {id: "konya_plain", rate_cm_per_100d: -8.9}`, `area_km2_lt_minus5cm: 474.26`, `people_on_sinking_ground: 1434355` (her alan kaynak etiketli, `quality: "provisional"`). Commit: `b11db53`.
- **Madde 3 (`tools/bulletin.py` v2.0 → `docs/bulletins/*.html`):**
  - NASA Disasters Program harita paketi düzenine yükseltildi: üst meta blok (`Product ID: NP-<CITY>-2026-001`, UTC yayın zamanı, veri penceresi, sensör `NISAR L-band GUNW, provisional`, kalite sınıfı, güven rozeti, `v2.0`), en çok çöken ilk 3 bölge (`1 km` blok medyanı), GHSL etkilenen nüfus, altyapı (`O2` / `assets.json`) ve 3 maddelik `"What This Means"` özeti, alt kalibrasyon uyarısı ve A4 yazdırma CSS'i (`@page { size: A4 portrait; margin: 12mm; }`).
  - Tüm **13 bölge bülteni + `index.html`** (`14` HTML) yeniden üretildi; bağlantı/görsel taraması: `0` kırık bağlantı. Commit: `b8854a1`.
- **Madde 4 (`docs/story/submission_form.md`):**
  - 13 bölgelik küresel atlas, GHSL maruziyet sayıları (`474.26 km²`, `1,434,355` kişi) ve `Bulletin v2.0` özeti §5 madde 4 ve madde 7 içine eklendi (sade İngilizce, `REVIEW_1500.md` uyumlu).
- **Madde 5 (Doğrulama):**
  - `python -m pytest -q`: **`83 passed, 1 warning in 26.34s`**.
  - `docs/bulletins/*.html` (`14` HTML): **`0` kırık link**.
- **SÜREKLİ Döngü (`semarang` eklendi, 14 bölge):**
  - `data/global/atlas.json` içinde `semarang` (`-11.2 cm/100d`) tespit edilince `exposure_atlas.json` (`semarang`: `592,366` `< -2 cm`, `67,138` `< -5 cm`, `100.87 km²`, `2*sigma = 0.742 cm`), `vital_signs.json` (`cities_measured: 14`, `fastest: semarang -11.2 cm/100d`, `area_km2_lt_minus5cm: 575.13`, `people_on_sinking_ground: 1501493`), `docs/bulletins/semarang.html` + tüm `14` bülten ve `index.html`, `docs/story/exposure.md`, `docs/story/submission_form.md` yeniden üretildi.
  - `python -m pytest analysis/pc8/test_bulletin.py -q`: `1 passed`.
- **SÜREKLİ Döngü (`hanoi` eklendi, 15 bölge):**
  - `data/global/atlas.json` içinde `hanoi` tespit edilince `exposure_atlas.json` (`hanoi`: `85,952` `< -2 cm`, `3,372` `< -5 cm`, `1.61 km²`, `2*sigma = 0.708 cm`), `vital_signs.json` (`cities_measured: 15`, `fastest: semarang -11.2 cm/100d`, `area_km2_lt_minus5cm: 576.74`, `people_on_sinking_ground: 1504865`), `docs/bulletins/hanoi.html` + tüm `15` bülten ve `index.html`, `docs/story/exposure.md`, `docs/story/submission_form.md` yeniden üretildi.
  - `python -m pytest analysis/pc8/test_bulletin.py -q`: `1 passed`.
