# PC6 QA Notları

Tarih: `2026-11-14` (`13:08 TR`) · Denetleyen: PC6

## 1. `data/*/meta.json` ve `web/mock/*/meta.json` Denetimi (Q14 — Faz 1)

Mevcut durumda `data/` altında henüz üretilmiş `meta.json` dosyası yok (`data/.gitkeep` mevcut; PC2/PC3/PC4 çıktıları bekleniyor). Mevcut örnek ve üretici kod denetimleri:

| Dosya | `quality` / `quality_note` | `vmin` / `vmax` | `bbox` (`[w,s,e,n]`) | Not |
|---|---|---|---|---|
| `web/mock/central_valley/meta.json` | `"placeholder"` / geliştirme notu var | `-6.1` / `6.1` (simetrik, `RdBu` ile uyumlu) | `[-120.2, 35.6, -119.0, 36.6]` (`VERI_SOZLESMESI.md` §1 ile birebir) | `dates` (3 tarih) `disp/*.png` ve `points.json` ile uyumlu. Mock dosyada `notes` yok ve `reference_point` string (`"scene median"`). |
| `analysis/cumulative.py` (üretici) | `"provisional"` + tam kalibrasyon dipnotu | Simetrik `-vlim` / `+vlim` | `BBOX[site]` ile birebir | `RdBu(0.0)` = `#67001f` (kırmızı, negatif/çökme) ve `RdBu(1.0)` = `#053061` (mavi, pozitif/yükselme) → `web/style.css` `.ramp` gradyanı ve `web/index.html` açıklaması ile tam uyumlu. |

## 2. İngilizce Metin, Etiket ve Sözleşme Denetimi (`web/`)

- **Dil ve anlatım (`web/index.html`, `web/app.js`):** `<html lang="en">`, tüm 6 sahne akıcı, sade ve bilimsel açıdan tutarlı İngilizce ile yazılmış; yazım hatası görülmedi.
- **Kalibrasyon dipnotu (`web/index.html:152`):** Zorunlu tam metin mevcut: *"NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."*
- **AI medya etiketleri (`web/index.html`, `web/assets/`):** 7 AI görselinin tamamı (`hero.jpg`, `fens_ai.jpg`, `holme_ai.jpg`, `canal_ai.jpg`, `sinkhole_aerial_ai.jpg`, `obruk_ai.jpg`, `game_valley_ai.jpg`) ve `hero.mp4` yuvası `"AI-generated illustration"` / `"AI-generated background illustration"` etiketi taşıyor. NASA logosu yok.
- **Analiz testleri (`python -m pytest analysis -q`):** `13 passed in 2.48s`.

## 3. Gözlenen Küçük İyileştirme Notları (Sahibine Bilgi — Dosyasına Dokunulmadı)

1. **`web/app.js:83-87` (`select(p)` null koruması):** `p.disp_cm.at(-1)` değeri `null` gelirse `Math.abs(null)` → `0` ve `0 < 0` → `false` olacağı için `"this spot rose 0.0 cm"` yazar. (`analysis/cumulative.py` geçerli piksellerden seçtiği için normalde `null` gelmez, ancak savunmacı `v == null` kontrolü faydalı olur.)
2. **`web/index.html:154` (kırık olabilecek link kontrolü):** `docs/story/sources.md` linki şu an henüz oluşmamış (PC4 üretince aktifleşecek). 17:00 yayını öncesi tekrar kontrol edilmeli.
3. **`web/index.html:47` (yer tutucu metin):** Holme Fen kartında `<span class="pending">Exact figure and source being verified.</span>` mevcut (PC4 kaynaklı rakamı verince güncellenmeli).
4. **Tekrar kontrol:** PC2/PC3/PC4 gerçek `data/*/meta.json` dosyalarını push ettiğinde Q14 tekrar çalıştırılıp `- [x PC6]` işaretlenecek.

---

## 4. `data/` Faz-2 Denetimi (`13:41 TR` — Central Valley Gerçek Verisi Geldi)

Gerçek `data/central_valley/` çıktıları (`meta.json`, `summary.json`, `points.json`, 8 `disp/*.png`) ve PC6 veri üretimleri (`validation.json`, `assets.json`) denetlendi (web sitesiyle ilgili `data/catalog.json`, `game/index.html`, `docs/game_v1.png`, `web/app.js` değişiklikleri kullanıcı isteğiyle geri alındı):

| Dosya | `quality` / `quality_note` | `vmin` / `vmax` | `bbox` (`[w,s,e,n]`) | Sonuç |
|---|---|---|---|---|
| `data/central_valley/meta.json` | `"provisional"` + tam NASA-JPL/ISRO kalibrasyon dipnotu | `-6.0` / `6.0` (simetrik, `RdBu`) | `[-120.2, 35.6, -119.0, 36.6]` (`VERI_SOZLESMESI.md` §1 ile birebir) | Geçti (8 PNG tümü mevcut, 7 granule CRID `P05023`, skip `beta-precal` notlu) |
| `data/central_valley/summary.json` | `"provisional"` + dipnot | `max_subsidence_cm: -7.8`, `rate_cm_per_yr_estimate: -26.4` | ref `(-119.14562, 36.45323)` | Geçti (`method_note` yaz mevsimi doğrusal ekstrapolasyon uyarısını dürüstçe içeriyor, `NaN` yok) |
| `data/central_valley/points.json` | n/a (site noktaları) | 12 nokta, `NaN` yok | Central Valley içi | Geçti (`2026-06-28 → 2026-10-14`, 8 tarih) |
| `data/central_valley/validation.json` | `"provisional"` + tam dipnot | `NaN` yok | 10 GNSS istasyonu footprint içi | Geçti (`CAHA` RMSE 0.752 cm `r=0.896`, `HANF` RMSE 0.834 cm `r=0.896`, `QCAP` RMSE 0.767 cm `r=0.820`, `TLBN` RMSE 1.173 cm `r=0.793`) |
| `data/central_valley/assets.json` | `"provisional"` + OSM ODbL + dipnot | 645 segment ≥ 1 km değerlendirildi (`high=81, medium=131, low=433`) | top 10 GeoJSON `NaN` yok | Geçti (Tulare Irrig. Canal 57.01 mm/km, California Aqueduct 49.12 mm/km, Friant-Kern Canal 46.06 mm/km) |

### Güncel Notlar
- `data/karapinar/meta.json` (`Q02`) henüz eklendi (`quality: provisional`, `vmin/vmax: -5.0/5.0`, `bbox: [33.3, 37.6, 33.8, 37.9]`, 9 PNG); tam Q14/UK kontrolü `data/uk/` tamamlandığında tekrarlanacak.
- `web/app.js`, `docs/URUN_TANIMI.md`, `game/`, `docs/game_v1.png`, `data/catalog.json` kullanıcı isteği üzerine PC6 öncesi duruma (`c7bac46` / `4cba32a`) geri alındı.

---

## Q28 · Karapınar Obruk & Altyapı Risk Analizi (`risk/karapinar_risk.py` → `data/karapinar/assets.json`)

- **Girdi verileri:** `analysis/out/karapinar_cum.npz` (`470×603`, `EPSG:32636`, `2026-06-26 → 2026-10-12`, `quality: provisional`, `40,194` geçerli piksel), `data/karapinar/sinkholes.geojson` (`29` kaynaklı obruk), `risk/karapinar_infra.geojson` (`64` OSM koridoru: `secondary=45`, `trunk=19`).
- **Bölge geneli (tüm geçerli pikseller):** Ortalama `−0.699 cm` · Medyan `−0.646 cm` · Std `1.555 cm` · En derin piksel `−9.055 cm`.

### Obruk Çevresi Radyal Halka Çökme Analizi (29 Obruk Çevresi)
| Halka Mesafesi | Geçerli Piksel | Ortalama LOS (cm) | Medyan LOS (cm) | Min (cm) | Bölge Ort. Farkı | `≤ -2 cm` Piksel % |
|---|---:|---:|---:|---:|---:|---:|
| **0–1 km** (obruk çekirdeği) | 60 | **−4.152** | −4.186 | −5.627 | **−3.453 cm** | **100.0 %** |
| **1–2 km** | 176 | **−4.030** | −4.027 | −7.934 | −3.331 cm | 90.3 % |
| **2–5 km** | 985 | −1.957 | −1.818 | −7.775 | −1.258 cm | 47.8 % |
| **>5 km** (arka plan) | 38,973 | −0.647 | −0.619 | −9.055 | +0.052 cm | 17.9 % |
| *Kümülatif `≤ 1 km` / `≤ 2 km` / `≤ 5 km`* | 60 / 236 / 1,221 | −4.152 / −4.061 / −2.364 | −4.186 / −4.066 / −2.484 | — | — | 100.0 / 92.8 / 56.5 % |

**Bulgu:** İlk 1 km içindeki ortalama çökme (`−4.152 cm`), >5 km bölge arka planının (`−0.647 cm`) **6.4 katıdır**; radar izindeki 10 obruk çevresinde piksellerin %100'ü `−2 cm` eşiğini aşmaktadır. En yüksek 1 km içi ortalamalar: `Köken Obruğu-I` (`−4.71 cm`), `Köken Obruğu-II` (`−4.663 cm`), `Köken Obruğu-III` (`−4.158 cm`), `Seyithacı Obruğu-VI` (`−4.091 cm`), `Seyithacı Obruğu-I` (`−4.029 cm`).

### OSM Yol & Koridor Yakınlık ve Eğim Riski (`64` Segment)
- **Mesafe dağılımı:** `≤ 1 km`: **2** segment · `≤ 2 km`: **4** segment · `≤ 5 km`: **9** segment. (OSM sorgusunda Karapınar bounding box içinde `waterway=canal` bulunmamaktadır; tüm koridorlar `secondary` ve `trunk` karayollarıdır.)
- **Eğim risk sınıfları (`≥ 1000 m` geçerli kesim):** `high`: **10** · `medium`: **3** · `low`: **8** · `outside_or_short`: **43**.
- **En yakın segmentler:**
  1. `42-42` (`secondary`, osm: `208237483`): `Köken Obruğu-II`'ye **597.3 m**, InSAR diferansiyel eğim **19.74 mm/km** (`max=-5.07 cm`, `risk=high`).
  2. `42-42` (`secondary`, osm: `172934693`): `Seyithacı Obruğu-V`'e **619.0 m** (`risk=high` yakınlık).
  3. `Adana - Konya Yolu` / `Konya - Adana Yolu` (`trunk`, D-330): `Akkuyu Obruğu-IV`'e **1,478.5 m / 1,494.3 m** (`risk=medium` yakınlık).
- **Doğrulama:** `python risk/karapinar_risk.py --self-test` **PASS** (`0 NaN/Infinity`).

---

## Q14 · Tüm `data/*/meta.json` Tam Denetimi (14:29 TR Güncellemesi)

Tüm 3 bölge ve 12 `.json`/`.geojson` dosyası tarandı (`NaN`/`Infinity`: **0 adet**):

| Bölge (`meta.json`) | `quality` | `vmin / vmax` | `bbox` (`VERI_SOZLESMESI` uyumu) | Görseller (`disp/` veya `uk/`) | Bulgular & Not |
|---|---|---|---|---|---|
| `data/central_valley/meta.json` | `provisional` | `-6.0 / +6.0` | `[-120.2, 35.6, -119.0, 36.6]` ✅ Tam uyum | `8 / 8` PNG mevcut ✅ | `summary.json` tepe noktası `−7.8 cm` LOS (harita ±6 cm'de simetrik doygun, kasıtlı). `quality_note` NASA-JPL/ISRO şartını sağlıyor ✅ |
| `data/karapinar/meta.json` | `provisional` | `-5.0 / +5.0` | `[33.3, 37.6, 33.8, 37.9]` ✅ Tam uyum | `9 / 9` PNG mevcut ✅ | `summary.json` tepe noktası `−5.9 cm` LOS. `sinkholes.geojson` (`29`) ve `assets.json` (`64`) ile sıfır NaN ✅ |
| `data/uk/meta.json` | `preview` | `Yok` (optik/browse) | `[-0.3, 52.4, 0.4, 52.9]` ✅ Tam uyum | `optical_2026-10-20.jpg` & `radar_2026-10-20.png` mevcut ✅ | Not (PC1/PC4 için): `meta.json` içinde yerel dosya adları (`optical_image`/`radar_image`) yok, yalnızca `date` + URL var; `data/catalog.json` içinde `karapinar` ve `uk` hâlâ `pending` görünüyor (PC1 entegrasyon bekliyor). |

### Game v2 Model Parametre Uyumlama Notu (`docs/story/game_model.md` §5–6 · 14:33 TR)
- `game/model.js` & `game/game.js` güncellendi: `S_y = 0.10` (USGS PP 1401-D ortalaması), `S_ske`/`S_skv` kaynak notu (`Sneed 2001, OFR 01-35`), kil kalınlığı etiketi `"Compressible clay interbeds (CVHM aggregate, illustrative)"`, su-yılı sınıf olasılıkları `illustrative` bayraklı, Pages 404 riskini önlemek için birincil veri kaynağı olarak `../data/central_valley/assets.json` (Pages uyumlu), başlangıç kutusu başlığı `"Model check against NISAR"`.
- **Güncel Kalibrasyon Sayıları (`S_y = 0.10`):**
  - `d_measured` (NISAR 108 gün dikey eşdeğer): **`-10.1 cm`** (`-7.8 cm` LOS, `cos(39.1°)`)
  - Ölçek katsayısı (`extractionScaleFactor k`): **`0.623`**
  - `game/test_model.html`: **5/5 PASS**, 108 gün simülasyonu **`-10.1 cm`** dikey (`-7.84 cm` LOS), hata **`0%`** (`≤ ±10%`), tarayıcıda **0 konsol / 0 ağ hatası**.

## Oyun v2 Canlı Site Kontrolü (`14:45 Paket — Adım 4`)

- **Kontrol Tarihi / Ortamı:** `https://keremsumer2010-tech.github.io/aseltech/#play` (iframe) ve `https://keremsumer2010-tech.github.io/aseltech/game/` (tam ekran), canlı GitHub Pages tarayıcı denetimi.
- **Veri ve Ağ Durumu:** `../data/central_valley/summary.json`, `assets.json` ve `points.json` **HTTP 200 OK** ile yüklendi; **0 konsol hatası**, **0 HTTP 4xx/5xx** hatası (yalnızca hızlı harita kaydırmada beklenen Esri tile `net::ERR_ABORTED` iptalleri).
- **Tam Ekran Masaüstü (`1280x850`) & Mobil (`390x844`):**
  - Bağımsız `/aseltech/game/` mobil `scrollWidth = 390 px` (yatay taşma **0 px**).
  - Tüm sürgüler (`Groundwater Pumping`, `Surface Water Allocation`, `Temporary Land Fallowing`), önayarlar (`2026 Baseline`, `Over-Pump`, `SGMA Balance`), 7 ilçe seçicisi, `Next Month →` / `+6 Mo` / `Reset`, 24 ay audit penceresi ve harita katmanları (`Live Simulation`, `Blend`, `2026 NISAR Raster`) doğrulandı.
- **`game/` İyileştirmesi:** `#play` içindeki `535x300 px` gömülü iframe'de açılış diyaloğunun altındaki `"Start 24-Month Simulation →"` düğmesi kaydırma gerektiriyordu; yalnızca `game/style.css` dosyasına `@media (max-height: 460px)` kompakt iframe/modal kuralları eklendi (`web/`'e dokunulmadı).
- **Bilgi Notu (`web/` kapsam dışı):** Canlı ana sayfanın (`aseltech/`) `390x844` mobil kontrolünde Chapter 4 tablosu (`487 px`) ve iframe kutusu (`535 px`) nedeniyle ana sayfa `scrollWidth = 569 px` ölçüldü (`web/` PC6 yazma yetkisi dışında olduğu için yalnızca raporlandı).

## Pazar Hazırlığı — Q07 Tam Yıl (`mixed`) Yeniden Çalıştırma Komutları (`14:45 Paket — Adım 5`)

PC2'nin Q07 tam yıl verisi (`beta` + `provisional` = `mixed` kalite etiketi) geldiğinde mevcut varsayılan `data/central_valley/` veya `data/karapinar/` dosyalarını ezmeden ayrı bir klasöre (`--data-dir`) ve `--quality mixed` etiketiyle çıktı alabilmek için PC6 scriptleri güncellendi:

- `validation/compare.py`: `--npz`, `--stations`, `--gnss-dir`, `--data-dir`, `--out`, `--quality` seçenekleri eklendi (`--out` verilmezse `<data-dir>/validation.json` yazar).
- `risk/compute_risk.py`: `--infra`, `--npz`, `--data-dir`, `--out`, `--quality`, `--top` seçenekleri eklendi (`--out` verilmezse `<data-dir>/assets.json` yazar).
- `risk/karapinar_risk.py`: `--sinkholes`, `--infra`, `--npz`, `--data-dir`, `--out`, `--quality` seçenekleri eklendi (`--out` verilmezse `<data-dir>/assets.json` yazar).

### Örnek Pazar Komutları (Ayrı Klasöre Yazma)

```bash
# 1) Central Valley tam yıl GNSS doğrulaması (varsayılan data/central_valley/'yi bozmaz)
python validation/compare.py \
  --npz <Q07_TAM_YIL_CV_CUM_NPZ> \
  --data-dir data/central_valley_full \
  --quality mixed

# 2) Central Valley tam yıl altyapı risk indeksi
python risk/compute_risk.py \
  --npz <Q07_TAM_YIL_CV_CUM_NPZ> \
  --data-dir data/central_valley_full \
  --quality mixed

# 3) Karapınar tam yıl obruk + altyapı risk indeksi (gerekirse)
python risk/karapinar_risk.py \
  --npz <Q07_TAM_YIL_KP_CUM_NPZ> \
  --data-dir data/karapinar_full \
  --quality mixed
```

Ana site verilerini doğrudan güncellemek gerektiğinde `--data-dir data/central_valley` (veya `--data-dir` parametresiz varsayılan yol) + `--quality mixed` kullanılabilir; `--npz` içindeki `quality` alanı doğrudan `mixed` ise `--quality` parametresi isteğe bağlıdır.

### Doğrulama (`14:45 Paket — Adım 5` sonrası çalıştırılan kontroller)

- `python validation/compare.py --self-test` → `Self-test passed (10 stations evaluated, JSON clean).`
- `python risk/compute_risk.py --self-test` → `Self-test passed (top 10 segments valid GeoJSON, zero NaNs).`
- `python risk/karapinar_risk.py --self-test` → `PASS self-test: 0-1km=-6.564 cm < 1-2km=-3.05 cm < 2-5km=-0.178 cm | line dist=0.0 m`
- `python -m pytest analysis -q` → `42 passed, 1 warning in 7.60s`
- Geçici `--data-dir` + `--quality mixed` testi (`validation/compare.py`, `risk/compute_risk.py`, `risk/karapinar_risk.py`) → `10` istasyon, `81` yüksek riskli CV segmenti ve `64` Karapınar segmenti `quality="mixed"` ile ayrı klasöre temiz JSON olarak üretildi (geçici dizin silindi).

---

## 7. SONSUZ DÖNGÜ — Tur 1 & 16:15/16:25 Challenge Uyum Güncellemesi

### 7.1 16:15 & 16:25 Yeni Görevler (Classroom Mode, NASA StoryMap / UAVSAR Kıyası, Kaynaklar & Demo Videosu)

- **Oyun Sınıf Modu (`Classroom Mode` — `game/index.html`, `game/game.js`, `game/style.css`):**
  - Sağ kontrol paneline (`#classroomCard`) ve üst çubuğa (`#classroomModeBtn`) **Classroom Mode (3 Scenarios)** eklendi:
    1. **Scenario 1 — Normal Year:** `Below Normal → Above Normal`, `%100` pompalama, `%70` yüzey suyu, `%0` nadas.
    2. **Scenario 2 — Multi-Year Drought:** `Dry → Critical`, `%140` pompalama, `%20` yüzey suyu, `%0` nadas (ön-konsolidasyon eşiği $h_{pc}$ altına inerek kalıcı kil sıkışması, kanal kapasite kaybı ve Konya'da obruk risk göstergesini tetikler).
    3. **Scenario 3 — Sustainable Pumping:** `Below Normal → Dry`, `%55` pompalama, `%85` yüzey suyu, `%25` nadas (su seviyesini $h_{pc}$ civarında tutarak kalıcı çökmeyi önler).
  - Hem sağ paneldeki açılır bölümde (`.classroom-q-details`) hem de 24 ay sonu karne penceresinde (`#endClassroomBox`) **3 tartışma sorusu** (1. Elastik geri tepme vs kalıcı kil sıkışması, 2. Diferansiyel kanal eğimi `mm/km` vs toplam çökme, 3. Tulare ve Konya havzalarında 12 günlük NISAR verisiyle yönetim kararları) gösterilmektedir.
- **Oyun `Sources & Parameters` Sekmesine NASA StoryMap + White Papers Entegrasyonu (`game/game.js`):**
  - `#paramsModal` penceresinin en üstüne **NASA Space Apps Challenge Resources & Land Subsidence StoryMap Framework** kutusu eklendi:
    - **NASA NISAR Land Subsidence StoryMap:** Peacock, A., An, K., Pinto, N., & Lou, Y. (2024), *NISAR ArcGIS Storymaps*, Zenodo (`https://doi.org/10.5281/zenodo.10818833`, StoryMap: `https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828`); Miller et al. (2020) & Jones et al. (2020) UAVSAR `>40 inç` (`>100 cm`) California Aqueduct çökme bulguları ile 2026 NISAR uzaydan ölçümümüzün bağlantısı.
    - **NASA NISAR Applications White Papers (`https://science.nasa.gov/mission/nisar/societal-benefits/`):** *Subsidence*, *Drought and Groundwater Withdrawal*, *Sinkholes and Cavern Collapse*, *Levees and Dams*, *Soil Moisture and Water Resources*.
    - **Eğitim & Kılavuz Bağlantıları:** ASF NISAR Data User Guide (`https://nisar-docs.asf.alaska.edu/`), NASA Earthdata Intro to SAR, NASA ARSET SAR Trainings, NASA/JPL UAVSAR Postcards.
- **Altyapı Risk Dosyasında (`docs/story/risk_dossier.md` & `analysis/pc6/make_risk_profiles.py`) California Aqueduct vs. NASA UAVSAR (2013–2017) Kıyası:**
  - `#4 California Aqueduct` (`102.82 km`, tepe eğim `49.12 mm/km`, 108 günde maks `-7.42 cm` LOS / `~-9.6 cm` dikey *estimate*, yıllıklandırılmış yaz hızı `~-25.1 cm/yr` LOS *estimate*) ile NASA NISAR StoryMap'te raporlanan 2013–2017 UAVSAR havadan L-bant ölçümleri (`>40 inç` / `>101.6 cm` kümülatif, `~20–25 cm/yr`, Miller et al. 2020; Jones et al. 2020) karşılaştırma tablosuyla (§2.1) eklendi. İki ölçüm aynı büyüklük mertebesindedir (`~20–25 cm/yr` yaz çekimi).
- **30 Saniyelik Demo Videosu (`analysis/pc6/make_demo_video.py` → `docs/story/media/demo_30s.mp4`):**
  - Sahne başlıkları Space Apps Challenge diline (`"Track and Visualize Surface Change"`, `"Patterns and Rhythms"`, `"Actionable Insights"`, `"Interactive Simulator & Classroom Mode"`) güncellendi (`1920x1080`, `h264`, `yuv420p`, `29.62 s < 30.0 s`).

### 7.2 `data/central_valley_fullyear/` Tam Yıl Animasyonu (`SONSUZ DÖNGÜ` c maddesi)

- `analysis/pc6/make_animation.py central_valley_fullyear` çalıştırılarak `docs/story/media/cv_fullyear.mp4` (`1920x1080`, `h264`, `yuv420p`, `24 fps`, `14.25 s`, `4.22 MB`, `26` tarih `2025-11-24` → `2026-10-14`, `18 beta-precal + 7 provisional`, `p01` Earlimart `-20.32 cm` LOS) üretildi ve `ffprobe` ile doğrulandı.
- Not: `analysis/out/central_valley_fullyear_cum_stack.npz` (`50.8 MB`) `docs/qa/PC9.md` §3 gereği `rules/RULES.md` K-12 sınırından ötürü repoya eklenmemiştir (PC9 yerel diskindedir); `.npz` paylaşıldığında §6'daki `--data-dir data/central_valley_fullyear --quality mixed` komutları doğrudan çalıştırılmaya hazırdır.

### 7.3 `docs/qa/*.md` Bulgularının Çözümü ve İngiltere (`UK`) Bilimsel Gerçekçilik Denetimi

- **Kapatılan PC6 QA Bulguları (`docs/qa/PCQ.md`):**
  - `game/model.js:750`: Konya Kapalı Havzası'nda `sinkholeRiskActive` bayrağının `d.headM <= d.preconsolidationHeadM` katı eşitsizliği yüzünden tetiklenmemesi düzeltildi (`d.headM <= d.preconsolidationHeadM + 0.05 && Math.abs(d.totalCm) >= CONFIG.thresholds.sinkholeAlertCm`). `game/test_model.html` içinde `6/6 tests passed` (`sinkholeRiskActive=true`) doğrulandı.
  - `game/game.js:1035`: Başlangıç kalibrasyon kutusunun `summaryData.range_cm || summaryData.max_subsidence_range_cm` alanını dinamik okuması sağlandı (`ref range -4.7…-7.8 cm LOS`).
- **İngiltere (`data/uk`, `data/fens`, `data/uk_clay`, `docs/story/uk_findings.md`, `docs/story/holme_fen.md`) Bilimsel Gerçekçilik Denetimi:**
  1. **The Fens & Holme Fen (`data/uk/meta.json`, `docs/story/holme_fen.md` — `quality: "preview"`):** `2026-10-20` tarihinde VIIRS optik görüntüsü `%98` bulutla kaplıyken NISAR L-bant (`24 cm`) `GCOV` geri saçılımı bulutları aşarak The Wash kıyı çizgisini ve drenaj kanallarını net göstermektedir. Holme Fen demir direğinin **1851**'den beri **~4 metre** açığa çıkması, zeminin deniz seviyesinin **2.75 m altına** inmesi ve güncel **1–2 cm/yıl** turba oksidasyonu birincil kaynaklarla (`The Great Fen`, `UKCEH / Defra SP1218 WP2`) birebir uyumludur.
  2. **The Fens L-Bant `GCOV` HV Zaman Serisi (`Q10`, `data/fens/crops.json`, `data/fens/hv_timeseries.png` — `quality: "provisional"`):** 8 tarihte (`2026-06-22` → `2026-10-08`) 4 ayrı `480 m × 480 m` pencerede (`f01..f04`) `2026-08-21` tarihinde eşzamanlı `+1.4` ile `+4.2 dB` HV artışı ve sezon sonunda `+0.23` ile `+1.13 dB` net değişim ölçülmüştür. Veri uydurulmamış, net bir hasat düşüşü olmadığı dürüstçe raporlanmıştır.
  3. **Greater London Kil (`London Clay`) Algılama Sınırı (`Q09`, `data/uk_clay/detection.json`, `summary.json`, `docs/story/uk_findings.md` — `quality: "provisional"`):** 9 ardışık çiftte (`2026-06-21` → `2026-10-19`, 120 gün) çift başına 1 km blok standart sapması `0.31–0.47 cm` olup 9 çiftlik zincir gürültüsü $\sigma_{\text{chain}} = \mathbf{1.21\text{ cm}}$ ve **$3\sigma$ algılama eşiği $3.62\text{ cm}$**'dir. Kuadratik atmosferik yüzey çıkarıldıktan sonra 1 km blokların **`%97.7`'si (`%98`) $\pm 1.5\text{ cm}$ içinde** kalmakta (`p2 = -1.47 cm`, `p50 = +0.19 cm`, `p98 = +1.26 cm`), sahne kenarından $\ge 10\text{ km}$ içeride $3.62\text{ cm}$ eşiğini aşan blok sayısı **`0` (`n_detected_blocks: 0`, `status: "below_detection"`)** olmaktadır. BGS literatüründe Londra Kili mevsimsel genliği `0.5–2.0 cm` olduğundan tek sezonda `"below_detection"` çıkması %100 gerçekçi ve güçlü bir negatif kontroldür.
  4. **PC8 / PC9 İçin Tespit Edilen 4 Küçük Görsel/Metin Notu (PC6 yazma alanı dışında olduğundan burada raporlanmıştır):**
     - `docs/story/media/pc8_uk_detection.png` Panel B'de sağ alt lejant kutusu yeşil çubuğun `"1.21 cm/yr (est.)"` yazısıyla kısmen çakışıyor ve 3 yıllık hız eşiği aynı panelde üç farklı yuvarlamayla (`~1.1`, `1.21`, `~1.2 cm/yr`) yazılmış.
     - `data/uk_clay/summary.json` içinde `max_subsidence_cm: -5.2` (`-6.9 cm` dikey), `docs/qa/PC8.md` içinde ise `-5.3 cm LOS (-7.1 cm dikey)` geçiyor (0.1–0.2 cm yuvarlama farkı).
     - `web/index.html` satır 99–100'de `#holmeText` ve `#ukClay` (`±3.6 cm`) yayında; ancak `docs/story/media/pc8_uk_detection.png` ile `data/fens/hv_timeseries.png` görselleri ve `web/data.html` indirme tablosundaki `uk_clay/{detection,summary}.json` + `fens/crops.json` bağlantıları PC9 tarafından eklenebilir.
     - `data/uk_clay/points.json` içindeki nokta `name` alanları ham koordinat dizgesi (`"51.324N 0.318W"`) olarak bırakılmış.

### 7.4 20 Farklı Strateji × 2 Havza (40 Koşu) Otomatik Oyun Testi (`analysis/pc6/test_20_strategies.py --self-test`)

Komut: `python analysis/pc6/test_20_strategies.py --self-test`
- **Tulare Kalibrasyonu:** `k = 0.623`, simüle `-10.1 cm` dikey (`-7.84 cm` LOS) vs NISAR `-10.1 cm` dikey (`-7.8 cm` LOS) → **Hata: `%0.0`**
- **Konya Kalibrasyonu:** `k = 0.621`, simüle `-8.0 cm` dikey (`-5.95 cm` LOS) vs NISAR `-8.0 cm` dikey (`-5.9 cm` LOS) → **Hata: `%0.0`**
- **Sonuç:** `40/40` 24-aylık simülasyon koşusu **PASS** (`0 NaN/Infinity`, `PC7` Node.js referans tablosuyla `<= 0.01 cm` birebir uyum, monoton pompalama tepkisi ve Konya obruk göstergesi doğrulandı).

| Strategy | WY (Y1/Y2) | Pump | Fallow | Tulare Tot/Perm (cm) | Tulare Rev (\$M) | Konya Tot/Perm (cm) | Konya Obruk Ind. |
|---|---|---:|---:|---:|---:|---:|:---:|
| `S01-D0` | Dry | 0% | 0% | 0.08 / 0.00 | 452.1 | 0.07 / 0.00 | Safe |
| `S02-D50` | Dry | 50% | 0% | 6.05 / 6.03 | 849.9 | 4.11 / 4.09 | Elevated |
| `S03-D100` | Dry | 100% | 0% | 28.87 / 28.84 | 1308.9 | 22.34 / 22.32 | Elevated |
| `S04-D150` | Dry | 150% | 0% | 51.68 / 51.66 | 1748.5 | 40.57 / 40.55 | Elevated |
| `S05-W100` | Wet | 100% | 0% | 0.04 / 0.00 | 1748.1 | 0.10 / 0.00 | Safe |
| `S06-BN100` | Below Normal | 100% | 0% | 17.62 / 17.60 | 1529.8 | 12.87 / 12.85 | Elevated |
| `S07-D100-F30` | Dry | 100% | 30% | 15.18 / 15.15 | 898.6 | 11.40 / 11.38 | Elevated |
| `S08-W0-F30` | Wet | 0% | 30% | 0.24 / 0.00 | 572.1 | 0.20 / 0.00 | Safe |
| `S09-W150-F30` | Wet | 150% | 30% | 0.41 / 0.39 | 1292.4 | 0.04 / 0.00 | Safe |
| `S10-BN50-F30` | Below Normal | 50% | 30% | 0.09 / 0.00 | 739.8 | 0.09 / 0.00 | Safe |
| `S11-C0-F50` | Critical | 0% | 50% | 0.04 / 0.00 | 215.2 | 0.04 / 0.00 | Safe |
| `S12-C150` | Critical | 150% | 0% | 59.42 / 59.40 | 1576.5 | 47.08 / 47.06 | Elevated |
| `S13-C100-F25` | Critical | 100% | 25% | 25.20 / 25.17 | 828.6 | 19.74 / 19.72 | Elevated |
| `S14-AN75` | Above Normal | 75% | 0% | 0.09 / 0.00 | 1447.4 | 0.11 / 0.00 | Safe |
| `S15-BN-SGMA` | Below Normal | 40% | 25% | 0.10 / 0.00 | 726.2 | 0.10 / 0.00 | Safe |
| `S16-BN-OverPump` | Below Normal | 145% | 0% | 43.50 / 43.47 | 1575.7 | 33.77 / 33.75 | Elevated |
| `S17-WetToCrit120` | Wet/Critical | 120% | 10% | 21.02 / 20.99 | 1435.1 | 15.57 / 15.55 | Elevated |
| `S18-CritToWet60` | Critical/Wet | 60% | 20% | 5.92 / 6.07 | 602.4 | 4.50 / 4.64 | Elevated |
| `S19-DryToAN90-F15` | Dry/Above Normal | 90% | 15% | 10.77 / 10.75 | 1028.7 | 7.56 / 7.55 | Elevated |
| `S20-CritToBN-NoSurf` | Critical/Below Normal | 80% | 0% | 22.04 / 22.02 | 836.1 | 16.98 / 16.96 | Elevated |

---

## 8. ÇALIŞMA HARİTASI (19:45) — PC6 Görev Doğrulamaları

### 8.1 Görev 1 · Oyun Son Testi (20 Strateji + Tarayıcı `test_model.html` & `game/`)
- **Tarih / Saat:** `2026-11-14 19:41 TR`
- **20 Strateji × 2 Havza (`python analysis/pc6/test_20_strategies.py --self-test`):** **40/40 PASS** (`0 NaN/Infinity`).
  - Tulare kalibrasyonu: `k = 0.623`, simüle `-10.1 cm` dikey (`-7.84 cm` LOS) vs NISAR `-10.1 cm` dikey (`-7.8 cm` LOS) → `%0.0` hata.
  - Konya kalibrasyonu: `k = 0.621`, simüle `-8.0 cm` dikey (`-5.95 cm` LOS) vs NISAR `-8.0 cm` dikey (`-5.9 cm` LOS) → `%0.0` hata.
- **Canlı Tarayıcı Testi (`http://127.0.0.1:8766/game/test_model.html`):** **6/6 PASS**, 0 konsol hatası, 0 başarısız ağ isteği.
- **Ana Oyun Açılışı (`http://127.0.0.1:8766/game/`):** HTTP 200, 36 ağ isteği (0 hata), 0 konsol hatası.
- **Bulunan Hata:** Yok (`0` hata).

### 8.2 Görev 2 · Sınıf Modu Kontrolü ve `lesson_plan.md` Uyumu
- **Tarih / Saat:** `2026-11-14 19:44 TR`
- **Tespit Edilen Eksik:** PC3'ün açık tema yeniden tasarımında (`54029c7`..`e0be89c`) `game/game.js` içinde `CLASSROOM_SCENARIOS` / `runClassroomScenario()` duruyorken `game/index.html` içindeki Classroom Mode arayüzü (`#classroomModal`, 3 tek tık senaryo, `#endClassroomBox`) kaldırılmıştı.
- **Düzeltme (`game/index.html`, `game/game.js`, `game/style.css`):**
  - Üst çubuğa `#classroomBtn` eklendi; tıklanınca `docs/story/lesson_plan.md` (40 dakikalık ders planı, Trial A / Trial B) ile birebir uyumlu **3 hazır senaryo** (`Normal Year`, `Multi-Year Drought · Trial A`, `Sustainable Pumping · Trial B`) ve **3 tartışma sorusu** içeren `#classroomModal` açılıyor.
  - 24 ay sonunda `#endModal` içinde `#endClassroomBox` ve `#endClassroomScenarioTag` otomatik görüntüleniyor.
- **Canlı Tarayıcı Doğrulaması (`http://127.0.0.1:8766/game/`):** `#classroomBtn` → `#classroomModal` (3 senaryo + 3 soru) → `Multi-Year Drought` (`[data-classroom="drought"]`) tek tıkla 24 ay koştu, `#endModal` ve `#endClassroomBox` (`Tulare Basin · Scenario 2: Multi-Year Drought`) açıldı; **0 konsol hatası, 0 ağ hatası**.

### 8.3 Görev 3 · Telefon (`375×812`) ve Projektör (`1280×720`) Testi + Dokunmatik Hedefler (≥ 44 px)
- **Tarih / Saat:** `2026-11-14 19:48 TR`
- **İlk Tarayıcı Testinde Bulunan Hatalar (`375×812`):**
  1. Başlangıç kutusu ve ana simülatörde `scrollWidth = 434.4 px > 375 px` (~`59.4 px` yatay taşma; `.topbar-meta` ve `.modal-card` dar ekrana sarılmıyordu).
  2. Dokunmatik hedefler (`#startBtn` `33 px`, `.seg-btn` `26 px`, `#classroomBtn` `32.6 px`, `#paramsBtn` `34×34 px`, `.layer-btn` `27.6 px`, `.dmark` `25.6 px`, `.maplibregl-ctrl-group button` `29×29 px`, `#nextMonthBtn` `38 px`, `#fastForwardBtn`/`#resetBtn` `32.6 px`) `< 44 px` idi.
- **Düzeltme (`game/style.css`):** `@media (max-width: 1100px)` ve `@media (max-width: 640px)` kuralları güncellendi (`min-width: 0; max-width: 100%`, `#presetSeg` tam genişlik, `.topbar-meta` sarma, tüm etkileşimli düğme/katman/işaretçi/harita zoom kontrollerine `min-height: 44px` / `min-width: 44px`).
- **Tekrar Test Sonucu:**
  - **Telefon (`375×812`):** Başlangıç kutusu `scrollWidth = 360 ≤ 375`, ana simülatör `scrollWidth = 375 === 375` (**0 px taşma**), `< 44 px` dokunmatik hedef sayısı: **0** (tümü `>= 44 px`), **0 konsol hatası, 0 ağ hatası**.
  - **Projektör (`1280×720`):** `1280×720` tam sığma (yatay/dikey taşma **0 px**), harita + alt grafik/okuma + sağ kontrol paneli çakışmasız ve okunaklı, **0 konsol hatası**.

### 8.4 Görev 4 · Oyunda "Sources" Sekmesi Kontrolü
- **Tarih / Saat:** `2026-11-14 19:50 TR`
- **Kod & Canlı Tarayıcı Kontrolü (`game/game.js` `buildParamsTableHtml()` + `game/model.js` `CONFIG.physics` + `#paramsModal`):**
  - **NASA NISAR Land Subsidence StoryMap:** Peacock et al. (2024, Zenodo `doi:10.5281/zenodo.10818833`), Miller et al. (2020) & Jones et al. (2020) UAVSAR (`>40 inç` / `>100 cm`) vs. 2026 NISAR California Aqueduct (`-7.42 cm` LOS / `49.12 mm/km`) güncel.
  - **NASA NISAR Applications White Papers:** `Subsidence`, `Drought & Groundwater Withdrawal`, `Sinkholes & Cavern Collapse`, `Levees & Dams`, `Soil Moisture & Water Resources` + ASF NISAR Data User Guide + NASA Earthdata Intro to SAR + NASA ARSET + JPL UAVSAR Postcards bağlantıları mevcut ve güncel.
  - **`docs/story/game_model.md` §6 Uyumu:** `S_y = 0.10` (`SOURCED`, USGS PP 1401-D), `S_ske = 1.0e-5` & `S_skv = 3.1e-4` (`ILLUSTRATIVE`, Sneed 2001 OFR 01-35 büyüklük mertebesi notu), `b0` (`12–82 m` CVHM SUB aggregate interbeds, Corcoran Clay `<= 61 m` notu), su-yılı olasılıkları (`ILLUSTRATIVE`), canlı kalibrasyon katsayısı `k` (`0.623` Tulare / `0.621` Konya) hepsi güncel ve tutarlı.

### 8.5 Görev 5 · Demo Videosu (`demo_30s.mp4`)
- **Durum:** `CALISMA_HARITASI.md` gereği DURDURULDU — dokunulmadı (`analysis/pc6/make_demo_video.py` ve `docs/story/media/demo_30s.mp4` değiştirilmedi).

---

## 9. ASLA BOŞ KALMA — Hata Ayıklama Turu 1 (`19:54 TR`)
- **`python -m pytest -q`:** **63 passed**, 1 `PendingDeprecationWarning` (`analysis/cumulative.py:127` `cmap.set_bad`).
- **`data/` JSON/GeoJSON Taraması:** 61/61 `.json`/`.geojson` dosyası geçerli JSON, 0 gerçek `NaN`/`Infinity`, 0 boş nesne. (`data/{central_valley,karapinar}/uncertainty/meta.json` içindeki `"NaN transparent"` yalnızca renk haritası açıklama metnidir.)
- **`web/` Yerel Tarayıcı Hata Ayıklaması (`http://127.0.0.1:8766/web/`, `1280×800`):** `index.html`, `explorer.html`, `science.html`, `data.html`, `faq.html`, `panel.html` (6/6 sayfa) — **0 konsol hatası, 0 başarısız ağ isteği, 0 kırık görsel, 0 yatay taşma**.

## 10. ASLA BOŞ KALMA — Tur 2 (`19:58 TR`)
- `git pull`: `442fdda` çekildi (`CALISMA_HARITASI.md` / `tasks/PC6.md` değişmedi; `PC8` önceki `pc8_uk_detection.png` QA bulgumuzu düzeltti `25641d0`).
- **`docs/qa/PC4.md:161` Bulgusu Kapatıldı:** `docs/story/validation_report.md:21` içinde `(-119.1456°E, 36.4532°N)` yazan referans boylamı `(119.1456°W, 36.4532°N)` olarak düzeltildi (`game/model.js:139` `Total compressible fine-grained interbeds` yorumu zaten günceldi).

## 11. ASLA BOŞ KALMA — Tur 3 (`20:08 TR`)
- `git pull`: `7f3abad` çekildi (`docs/CALISMA_HARITASI.md` / `tasks/PC6.md` değişmedi).
- **PC6 Öz-Testleri:** `analysis/pc6/test_20_strategies.py --self-test` (`40/40 PASS`), `validation/compare.py --self-test` (PASS), `risk/compute_risk.py --self-test` (PASS), `risk/karapinar_risk.py --self-test` (PASS).
- **Kırık Bağıl Link Taraması (`docs/**/*.md` + `README.md`):** **0** kırık bağıl link.

## 12. ASLA BOŞ KALMA — Tur 4 (`20:18 TR`)
- `git pull`: `823cd0c` çekildi (`CALISMA_HARITASI.md` / `tasks/PC6.md` değişmedi; yeni `storage_loss.json`, `nisarpulse`, `web/index.html` kartları geldi).
- **`python -m pytest -q`:** **70 passed**, 1 uyarı (`22.03 s`).
- **`data/` JSON/GeoJSON Taraması:** **62/62** dosya geçerli, 0 `NaN`/`Infinity`, 0 boş nesne.

## 13. ASLA BOŞ KALMA — Tur 5 (`20:28 TR`)
- `git pull`: `61b558d` çekildi (`CALISMA_HARITASI.md` / `tasks/PC6.md` değişmedi).
- **`analysis/pc6/test_20_strategies.py --self-test`:** **40/40 PASS** (`0 NaN/Infinity`).
- **Tarayıcı Hata Ayıklaması (`1280×800`):**
  - `/web/index.html`: **0 konsol hatası**, **0 kırık görsel** (`3/3` yüklü). Not (`PC3/PC4/PC7` için): yeni eklenen kartlardaki `HEAD /docs/story/engineering_risk.md` ve `HEAD /docs/story/technical_note.md` dosyalar henüz eklenmediği için `404` dönüyor (`storage_loss.md` ve `engine.md` `200 OK`).
  - `/docs/story/slides.html`: **0 konsol hatası**, **0 kırık görsel**; yalnızca henüz eklenmemiş `HEAD /docs/story/technical_note.md` `404` dönüyor.

## 14. ASLA BOŞ KALMA — Tur 6 (`20:40 TR`)
- `git pull`: `b24925c` çekildi (`CALISMA_HARITASI.md` / `tasks/PC6.md` değişmedi).
- **`python -m pytest -q`:** **70 passed**, 1 uyarı (`22.29 s`).
- **Tarayıcı Tekrar Kontrolü (`1280×800`):**
  - `/docs/story/slides.html`: **0 konsol hatası, 0 ağ hatası (404 kapandı), 0 kırık görsel**.
  - `/game/test_model.html`: **6/6 PASS**, 0 konsol hatası, 0 ağ hatası.
  - `/web/index.html`: **0 konsol hatası, 0 kırık görsel**; `technical_note.md` `200 OK` oldu, yalnızca henüz eklenmemiş `HEAD /docs/story/engineering_risk.md` `404` dönüyor.

---

## 15. `ATLAS_PLANI.md` (20:50) — PC6 Sinematik 3D Demo Videosu v2
- **Tarih / Saat:** `2026-11-14 21:01 TR`
- **Üretim Hattı:**
  - `analysis/pc6/build_demo_v2_data.py` → `analysis/pc6/demo_v2_data.json` (`0.78 MB`): AWS Açık Veri **Copernicus DEM GLO-30** (`rasterio /vsicurl/` ile Central Valley `50.9–1186.4 m` ve Karapınar `980.5–2001.5 m` yükseklik ızgaraları), `data/central_valley_fullyear/` (`26` epok, `mixed`), `data/karapinar/` (`9` epok + `29` obruk), `8` küresel atlas noktası.
  - `analysis/pc6/demo_v2_scene.html`: Three.js (`r158`) WebGL 3D sahnesi (0–12 s Central Valley 3D arazi + aylık dikey "nefes", 12–20 s 3D Dünya küresi + atlas çubukları, 20–26 s Konya/Karapınar 3D + 29 obruk halkası, 26–30 s kapanış kartı; sade İngilizce büyük altyazı, `"LOS"` yok, AI görseli/sesi yok).
  - `analysis/pc6/render_demo_v2.py`: Headless Chrome ile `900/900` kare yakalama + `ffmpeg` kodlama.
- **Doğrulama (`ffprobe` + Tarayıcı):**
  - `docs/story/media/demo_30s_v2.mp4`: `14.64 MB` (`≤ 20 MB`), `1920×1080`, `h264`, `yuv420p`, `30.000 s`.
  - `docs/story/media/demo_30s_v2_web.mp4`: `3.56 MB` (`web/` için hafif sürüm), `1280×720`, `h264`, `yuv420p`, `30.000 s`.
  - Tarayıcı kontrolü (`http://127.0.0.1:8766/analysis/pc6/demo_v2_scene.html`): 50/50 istek `HTTP 200 OK`, **0 konsol hatası, 0 ağ hatası**.
- **PC3 Notu:** `docs/story/media/demo_30s_v2_web.mp4` (`3.56 MB`, `720p`) siteye bağlanmaya hazır.

## 16. ASLA BOŞ KALMA — Tur 7 (`21:08 TR`)
- `git pull`: `a9a28a6` çekildi (`CALISMA_HARITASI.md` / `tasks/PC6.md` / `ATLAS_PLANI.md` PC6 satırı değişmedi).
- **`python -m pytest -q`:** **74 passed**, 1 uyarı (`22.99 s`).
- **`python pipeline/pc7/validate_json.py`:** **70** JSON dosyası, `0` parse hatası, `0` sonlu olmayan sayı (`NaN`/`Infinity`), `0` eksik `quality` alanı.

---

## 17. BUGFIX (`tasks/QUEUE.md` B16–B29)
- **B16 (`S-19 Kritik`):** `data/central_valley/validation.json` üzerinden 5 sabit kenar istasyonunda (`CAD1, CAFP, P564, P565, P566`) NISAR − GPS sapması `+1.26` ile `+2.09 cm` (ort. `+1.73 cm`) ölçüldü. `web/index.html` Bölüm 4 metnine bu sistematik sapma cümlesi eklendi ve `#gnssTable` başlığı `Diff.` → `RMSE (cm)` yapıldı; `web/app.js` içinde yeşil `r` eşiği `0.4` → `0.6` (`gnss.good`, `gnss` görünüm/katman, `gnssTable`) güncellendi (`P566` `0.42` artık gri `weak`, `5` çöken istasyon `>= 0.66` yeşil `good`). `http://127.0.0.1:8765/web/index.html` tarayıcı testinde 0 konsol hatası ile doğrulandı.
- **B17 (`S-20 Kritik`):** `risk/karapinar_risk.py` içindeki `_band_stats` fonksiyonuna `std_cm` alanı eklenip `data/karapinar/assets.json` yeniden üretildi (`0-1 km`: `mean=-4.152, std=0.712, n=60`; `1-2 km`: `mean=-4.03, std=1.463, n=176`; `2-5 km`: `mean=-1.957, std=1.931, n=985`; `>5 km`: `mean=-0.647, std=1.509, n=38973`; `--self-test` PASS). `web/index.html` Bölüm 6 metnine "Low confidence" (%14 ölçülebilir alan, ±3–4 cm gürültü), yumuşatılmış −5.9 cm ifadesi ve `>5 km` yayla notu eklendi; `web/app.js` `ringChart()` grafiğine piksel sayıları `(n=...)` ve `±1 SD` hata çubukları (`ringErrBars` eklentisi) eklendi. `http://127.0.0.1:8765/web/index.html` tarayıcı testinde 0 konsol hatası ile doğrulandı.
- **B18 (`S-24 Kritik`):** `docs/story/key_findings.md` madde 5'te Track 114 ifadesi `"neighboring ascending Track 114"` → `"descending Track 114"` olarak düzeltildi.
- **B19 (`S-26 Yüksek`):** `docs/story/key_findings.md` madde 7'de Karapınar 0–1 km (`-4.152 cm`) ve 1–2 km (`-4.030 cm`) halkalarının `>5 km` arka plan (`-0.647 cm`) ile farkları `3.45 / 3.33 cm` → `3.51 / 3.38 cm` olarak düzeltildi.
- **B20 (`S-27 Yüksek`):** `risk/compute_risk.py` (`classify_risk`) kuralı (`gradient >= 10.0 and max_cm <= -2.0 or max_cm <= -10.0`; medium `gradient >= 5.0 and max_cm <= -1.0 or max_cm <= -5.0`) ile uyumlu olacak şekilde `web/science.html` Bölüm 5 metni güncellendi (`docs/story/key_findings.md` madde 6 zaten uyumluydu). `http://127.0.0.1:8765/web/science.html` tarayıcı testinde 0 konsol hatası ile doğrulandı.
- **B21 (`S-28 Yüksek`):** `docs/story/key_findings.md` madde 4'te `"-0.75 to -1.17 cm accuracy"` → `"0.75 to 1.17 cm (RMSE) accuracy"` olarak düzeltildi.
- **B22 (`S-29 Yüksek`):** `data/central_valley/summary.json` `range_cm` (`[-7.8, -4.7]`) ile uyumlu olacak şekilde `docs/story/key_findings.md` madde 1 ve `docs/story/uncertainty.md` (satır 10, 16, 60) referans duyarlılık aralığı `-4.7 to -7.8 cm` / `-7.8 to -4.7 cm` olarak güncellendi (`docs/story/key_findings_public.md` dosyasına dokunulmadı).
- **B23 (`S-17 Yüksek`):** `analysis/pc6/make_smooth_disp.py` ile `7×7` NaN-duyarlı ortalama + `sigma=1.0` Gauss yumuşatma uygulanarak `data/central_valley/disp_smooth/` (8 PNG) ve `data/karapinar/disp_smooth/` (9 PNG) üretildi. `web/index.html` (`#dispModeBtn`) ve `web/app.js` içine `View: Detailed` / `View: Smoothed` geçiş düğmesi eklendi; `cv-disp` ve `kp-disp` varsayılan saydamlığı `0.65` olarak ayarlandı. (Tarayıcı doğrulaması kullanıcı talebiyle geçildi.)
- **B24 (`S-14 Yüksek`):** `data/central_valley/points.json` içindeki `p04` noktası (eski konum `%50.3` geçerli piksel, boşluk kenarında) `analysis/out/central_valley_cum_stack.npz` üzerinden en yakın `>= %90` geçerli `13×13` (`~1 km`) bloğa taşındı: `14 km W of Corcoran` (`-119.71162, 36.09707`, `%91.7` geçerli, son değer `-3.26 cm`) ve `"note"` alanı eklendi.
- **B30 (`S-31 Yüksek`):** `analysis/pc6/make_hero_loop.py` ile Esri World Imagery Central Valley altlığı headless Chrome'da yakalanıp soluklaştırılmış/koyulaştırılmış ve sol tarafı başlık kontrastı için koyu gradyanlı 12 sn dikişsiz döngü üretildi (çökme/renk katmanı yok): `docs/story/media/hero_loop.mp4` (`1119.8 KB`, `h264`, `1920×1080`, `12.0 s`), `docs/story/media/hero_loop.webm` (`588.2 KB`, `vp9`, `1920×1080`) ve `docs/story/media/hero_poster.webp` (`118.8 KB`). `ffprobe` ve boyut sınırları (`<= 1.5 MB` video, `<= 150 KB` poster) doğrulandı.
- **B35 (`S-35 Yüksek`):** `analysis/pc6/capture_game_poster.py` ile `game/index.html` (Terra Bella, Blend katmanı, +6 ay) headless Chrome CDP üzerinden `1600×900` olarak yakalandı: `docs/game_v4.png` ve `web/assets/simulator.jpg` (`<= 150 KB`) kaydedildi, `web/index.html` `#gamePoster` `alt` metni `"light-themed simulator: map, chart and three water sliders"` olarak güncellendi.
- **B25 (`S-15 Yüksek`):** `docs/story/key_findings.md` madde 1 içinde kenar başlık noktası `p01` (6 km N of Terra Bella, `-7.8 cm`) ile birlikte vadi içindeki `p02` (21 km S of Lemoore, `-7.78 cm`) noktası da açıkça anıldı.
- **B26 (`S-02 Yüksek`):** `analysis/pc6/make_animation.py` içinde harita arka planı `#0f1722` yerine açık gri `#a8b3c2` yapıldı ve harita göstergesine `Patch(..., label="Grey = no reliable radar signal")` eklendi. `cv_subsidence.*` ve `kp_subsidence.*` yeniden üretildi.
- **B27 (`S-01 Orta`):** `analysis/pc6/make_animation.py` içinde üst sağdaki `Peak` etiketi sabit `p01` yerine her karede `points` içindeki geçerli en negatif (`min`) noktayı gösterecek şekilde güncellendi (örn. Epoch 2'de `Peak P02: -2.10 cm` doğrulandı).
- **B28 (`S-04 Orta`):** `analysis/pc6/make_animation.py` içinde Central Valley video başlığı `"Central Valley (San Joaquin Valley), CA — NISAR Cumulative LOS Subsidence"` olarak güncellendi.
- **B29 (`S-05 Orta`):** `analysis/pc6/make_animation.py` içinde harita/grafik eksenleri `bottom=0.175` seviyesine çekilip alt kaynak (`y=0.106/0.118`) ve kalite notu (`y=0.080/0.101`) satırları yukarı alındı; video kontrol çubuğu altında kalmadığı kare çıktısıyla (`cv_frame_check.png`) doğrulandı.
- **B31 (`S-31 Yüksek`):** `web/index.html` hero bölümünde `#heroMap` kaldırılıp `<video id="heroVideo" class="hero-map" autoplay muted loop playsinline preload="metadata" poster="docs/story/media/hero_poster.webp">` eklendi ve alt yazı `"Background: Central Valley, California, 28 Jun–14 Oct 2026 (provisional)"` yapıldı; `web/style.css` `.hero-map` için `width:100%;height:100%;object-fit:cover;pointer-events:none` eklendi; `web/app.js` içinde MapLibre `hero()` kaldırılıp `heroVideo()` (`prefers-reduced-motion: reduce` durumunda yalnızca poster) bağlandı. Headless Chrome'da `1440×900` ve `375×812` görünümlerinde `hero_loop.webm` (`readyState=4`, `588.2 KB`) yüklendiği doğrulandı.
- **B32 (`S-32 Yüksek`):** `web/index.html` (8 yer: hero byline, Figure 0/2/3/5/6 kredileri, fullyear görsel kredisi, sayfa sonu), `web/data.html`, `web/faq.html`, `web/science.html` içindeki her `Team Taykut` → `Team Aseltech`; `grep` ile web/ HTML ve app.js içinde 0 kalıntı doğrulandı. Okul/şehir bilgisi (ASELSAN ... Ankara) aynı bırakıldı.
- **C03 (`ORTAK İŞLER`):** `web/index.html`, `web/explorer.html`, `web/science.html`, `web/data.html`, `web/faq.html` üst menülerine `Atlas` (`atlas.html`) bağlantısı eklendi; `web/index.html` `#next` bölümüne `data/global/atlas.json` sayılarıyla (`11` bölge, `6` reliable, `5` indicative) tek özet kartı (`#atlasSummaryCard`) eklendi; `web/data.html` tablosuna `data/global/atlas.json` (`PROVISIONAL`) satırı ile `atlas_data_dictionary.md` / `atlas_methods.md` dokümantasyon bağlantıları (`#atlasDocs`) eklendi. `http://127.0.0.1:8765/web/*.html` (5 sayfa) headless Chrome testinde `rc=0` ve `0` konsol hatasıyla doğrulandı.
- **ATLAS FİNAL (`tasks/PC6.md` 1–8):** `web/atlas.html`, `web/atlas.css`, `web/atlas.js`, `web/vendor/maplibre-gl.{js,css}` (`v5.3.0`), `web/assets/bluemarble_2k.jpg` (NASA Visible Earth kamu malı) güncellendi:
  1. Yan panelde `meta.json` `dates` serisi için Play/Pause + zaman kaydırıcı + tarih etiketi + renk ölçeği + `PROVISIONAL` rozeti eklendi; seçili şehrin kümülatif PNG'si (`disp/<date>.png`) haritadaki `meta.bbox` üzerine şeffaf (`0.72`) katman olarak bağlandı.
  2. Haritada tek tıkla katman seçimi (`Subsidence`, `Uncertainty (σ)`, `Confidence`) ve dinamik lejant eklendi.
  3. Üst şeritte `data/global/vital_signs.json` tabanlı 4 Vital Signs kartı (`#vitalBar`, alan/dosya yoksa gizli) eklendi.
  4. `Tour top 5` düğmesi (ilk 5 şehir, 6 sn/şehir, altyazı kutusu `#tourCaption`) eklendi.
  5. Çevrimdışı yedek: `vendor/maplibre-gl.{js,css}` yerel sunum + `bluemarble_2k.jpg` altlık katmanı (`#offlinePill` uyarısıyla).
  6. Paylaşılabilir `#<id>` URL desteği (`hashchange` + `history.replaceState`) ve PC10 alanları (`detectable`, `robustness_spread`, `people_exposed`, `opera_check`) ile PC4 `City card` / PC8 `Open bulletin` bağlantıları eklendi.
  - Doğrulama (`http://127.0.0.1:8765/web/atlas.html` ve `#mexico_city`): `1920×1080` ve `375×812` headless Chrome testlerinde `rc=0`, `slider=True`, `tourBtn=True`, `cityCard=True`, `bulletin=True`, `vendor=True`, `0` konsol hatası.
- **TAKVİYE (`tasks/PC6.md` 1–7, `Paz 00:55`):** `web/atlas.html`, `web/atlas.css`, `web/atlas.js` güncellendi:
  1. `data/global/vital_signs.json` anahtarları (`cities_measured: 13`, `fastest.name: Konya Plain`, `area_km2_lt_minus5cm: 474`, `people_on_sinking_ground: 1,434,355`) canlı bağlandı.
  2. Yan panelde seçili şehrin tepe noktası (`points.json` `p01`) için kütüphanesiz SVG tarih–cm çizgi grafiği ve `±2σ` belirsizlik bandı eklendi.
  3. `Compare two cities` (`#compareBox`) ile iki şehir yan yana (hız, max LOS, dikey tahmin, güven ve `p01` üst üste SVG grafiği) eklendi.
  4. Arama kutusu (`#atlasSearch`), güven sınıfı (`#atlasConfFilter`) ve ülke (`#atlasCountryFilter`) filtreleri liste ve küreye birlikte bağlandı.
  5. `Values: LOS` ↔ `Values: Vertical (est.)` anahtarı (`#unitToggle`), `Data & citation` indirme kutusu (`#atlasDataBox`, `atlas.geojson`/`atlas.csv` varsa otomatik gösterim) ve Central Valley için `data/central_valley/validation.json` GNSS istasyon katmanı (`cv-gnss`, tıklanınca `r`/`RMSE` popup) eklendi.
  6. `window.atlasSelect(id)` ve `atlas:select` olayı korundu; `web/atlas_sat.*` dosyalarına dokunulmadı.
  - Doğrulama (`1920×1080` & `#central_valley` `375×812` headless Chrome): `rc=0`, `vital=True`, `svg=True`, `search=True`, `compare=True`, `unit=True`, `cite=True`, `0` konsol hatası.
- **`SUREKLI.md` Tur 1 (`23:49 TR`):** `python -m pytest -q` → **83 passed**, 1 `PendingDeprecationWarning` (`23.71 s`).
