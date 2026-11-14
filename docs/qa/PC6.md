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
