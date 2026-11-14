# PC7 QA notları

## 1. Link ve dosya yolları (offline)

Yayımlama eşlemesi: `web/` site kökü; `data/`, `game/`, `web3d/` ve `docs/story/` depo kökünden kopyalanıyor.

| Kaynak | Satır | Göreli yol | Repo karşılığı | Kontrol |
|---|---:|---|---|---|
| `web/app.js` | 25 | `data/central_valley/meta.json` | `data/central_valley/meta.json` | OK |
| `web/app.js` | 25 | `data/central_valley/points.json` | `data/central_valley/points.json` | OK |
| `web/app.js` | 25 | `data/central_valley/summary.json` | `data/central_valley/summary.json` | OK |
| `web/app.js` | 26 | `data/central_valley/assets.json` | `data/central_valley/assets.json` | OK |
| `web/app.js` | 26 | `data/central_valley/validation.json` | `data/central_valley/validation.json` | OK |
| `web/app.js` | 27 | `data/karapinar/meta.json` | `data/karapinar/meta.json` | OK |
| `web/app.js` | 27 | `data/karapinar/sinkholes.geojson` | `data/karapinar/sinkholes.geojson` | OK |
| `web/app.js` | 27 | `data/karapinar/summary.json` | `data/karapinar/summary.json` | OK |
| `web/app.js` | 27 | `data/uk/meta.json` | `data/uk/meta.json` | OK |
| `web/app.js` | 28 | `data/central_valley/area_stats.json` | `data/central_valley/area_stats.json` | OK |
| `web/app.js` | 28 | `data/karapinar/assets.json` | `data/karapinar/assets.json` | OK |
| `web/app.js` | 28 | `data/uk_clay/detection.json` | `data/uk_clay/detection.json` | OK |
| `web/app.js` | 44 | `docs/story/key_findings_public.md` | `docs/story/key_findings_public.md` | OK |
| `web/app.js` | 57 | `data/central_valley/disp/` | `data/central_valley/disp` | OK |
| `web/app.js` | 94 | `data/uk/radar_${D.uk.date}.png` | `data/uk/radar_*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 97 | `data/central_valley/disp/${m.dates[cvIdx]}.png` | `data/central_valley/disp/*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 118 | `data/karapinar/disp/${m.dates.at(-1)}.png` | `data/karapinar/disp/*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 157 | `data/uk/optical_${D.uk.date}.jpg` | `data/uk/optical_*.jpg` | OK (dynamic pattern has matches) |
| `web/app.js` | 158 | `data/uk/radar_${D.uk.date}.png` | `data/uk/radar_*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 168 | `data/central_valley/disp/${m.dates[i]}.png` | `data/central_valley/disp/*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 232 | `game/index.html` | `game/index.html` | OK |
| `web/app.js` | 232 | `web3d/index.html` | `web3d/index.html` | OK |
| `web/app.js` | 233 | `docs/story/media/cv_subsidence.mp4` | `docs/story/media/cv_subsidence.mp4` | OK |
| `web/data.html` | 8 | `style.css` | `web/style.css` | OK |
| `web/data.html` | 12 | `index.html` | `web/index.html` | OK |
| `web/data.html` | 13 | `data.html` | `web/data.html` | OK |
| `web/data.html` | 13 | `faq.html` | `web/faq.html` | OK |
| `web/data.html` | 13 | `index.html#play` | `web/index.html` | OK |
| `web/data.html` | 13 | `index.html#story` | `web/index.html` | OK |
| `web/data.html` | 13 | `science.html` | `web/science.html` | OK |
| `web/data.html` | 25 | `docs.js` | `web/docs.js` | OK |
| `web/data.html` | 28 | `data/central_valley/meta.json` | `data/central_valley/meta.json` | OK |
| `web/data.html` | 29 | `data/central_valley/summary.json` | `data/central_valley/summary.json` | OK |
| `web/data.html` | 30 | `data/central_valley/points.json` | `data/central_valley/points.json` | OK |
| `web/data.html` | 31 | `data/central_valley/validation.json` | `data/central_valley/validation.json` | OK |
| `web/data.html` | 32 | `data/central_valley/assets.json` | `data/central_valley/assets.json` | OK |
| `web/data.html` | 33 | `data/karapinar/meta.json` | `data/karapinar/meta.json` | OK |
| `web/data.html` | 34 | `data/karapinar/summary.json` | `data/karapinar/summary.json` | OK |
| `web/data.html` | 35 | `data/karapinar/points.json` | `data/karapinar/points.json` | OK |
| `web/data.html` | 36 | `data/karapinar/sinkholes.geojson` | `data/karapinar/sinkholes.geojson` | OK |
| `web/data.html` | 37 | `data/uk/meta.json` | `data/uk/meta.json` | OK |
| `web/data.html` | 38 | `data/catalog.json` | `data/catalog.json` | OK |
| `web/faq.html` | 8 | `style.css` | `web/style.css` | OK |
| `web/faq.html` | 12 | `index.html` | `web/index.html` | OK |
| `web/faq.html` | 13 | `data.html` | `web/data.html` | OK |
| `web/faq.html` | 13 | `faq.html` | `web/faq.html` | OK |
| `web/faq.html` | 13 | `index.html#play` | `web/index.html` | OK |
| `web/faq.html` | 13 | `index.html#story` | `web/index.html` | OK |
| `web/faq.html` | 13 | `science.html` | `web/science.html` | OK |
| `web/faq.html` | 24 | `docs.js` | `web/docs.js` | OK |
| `web/faq.html` | 25 | `docs/story/judge_faq.md` | `docs/story/judge_faq.md` | OK |
| `web/index.html` | 13 | `style.css` | `web/style.css` | OK |
| `web/index.html` | 17 | `index.html` | `web/index.html` | OK |
| `web/index.html` | 19 | `data.html` | `web/data.html` | OK |
| `web/index.html` | 19 | `faq.html` | `web/faq.html` | OK |
| `web/index.html` | 19 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 56 | `data.html` | `web/data.html` | OK |
| `web/index.html` | 56 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 64 | `science.html#findings` | `web/science.html` | OK |
| `web/index.html` | 112 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 132 | `science.html#risk` | `web/science.html` | OK |
| `web/index.html` | 194 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 198 | `assets/simulator.jpg` | `web/assets/simulator.jpg` | OK |
| `web/index.html` | 219 | `data.html` | `web/data.html` | OK |
| `web/index.html` | 219 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 226 | `faq.html` | `web/faq.html` | OK |
| `web/index.html` | 232 | `app.js` | `web/app.js` | OK |
| `web/science.html` | 8 | `style.css` | `web/style.css` | OK |
| `web/science.html` | 12 | `index.html` | `web/index.html` | OK |
| `web/science.html` | 13 | `data.html` | `web/data.html` | OK |
| `web/science.html` | 13 | `faq.html` | `web/faq.html` | OK |
| `web/science.html` | 13 | `index.html#play` | `web/index.html` | OK |
| `web/science.html` | 13 | `index.html#story` | `web/index.html` | OK |
| `web/science.html` | 13 | `science.html` | `web/science.html` | OK |
| `web/science.html` | 83 | `docs.js` | `web/docs.js` | OK |
| `web/science.html` | 85 | `docs/story/calibration_note.md` | `docs/story/calibration_note.md` | OK |
| `web/science.html` | 86 | `docs/story/sources.md` | `docs/story/sources.md` | OK |
| `web/science.html` | 87 | `docs/story/key_findings.md` | `docs/story/key_findings.md` | OK |
| `web/science.html` | 88 | `docs/story/literature_comparison.md` | `docs/story/literature_comparison.md` | OK |
| `web/science.html` | 89 | `docs/story/uncertainty.md` | `docs/story/uncertainty.md` | OK |
| `web/science.html` | 90 | `docs/story/validation_report.md` | `docs/story/validation_report.md` | OK |
| `web/science.html` | 91 | `docs/story/risk_dossier.md` | `docs/story/risk_dossier.md` | OK |
| `web/science.html` | 92 | `data/central_valley/summary.json` | `data/central_valley/summary.json` | OK |
| `web/science.html` | 101 | `data/central_valley/validation.json` | `data/central_valley/validation.json` | OK |

Kontrol edilen yerel yol: 84. Eksik: 0.
Eksik yerel yol bulunmadı.
## 2. Veri sözleşmesi (offline)

| Dosya | Parse | quality alanı | quality_note alanı | Sözleşme şeması |
|---|---|---|---|---|
| `data/catalog.json` | OK | records | records | OK |
| `data/central_valley/area_stats.json` | OK | root | root | not specified |
| `data/central_valley/assets.json` | OK | root | root | OK |
| `data/central_valley/drivers.json` | OK | root | root | OK |
| `data/central_valley/gcov/meta.json` | OK | root | root | OK |
| `data/central_valley/meta.json` | OK | root | root | OK |
| `data/central_valley/points.json` | OK | missing | missing | OK |
| `data/central_valley/summary.json` | OK | root | root | OK |
| `data/central_valley/uncertainty/meta.json` | OK | root | root | not specified |
| `data/central_valley/validation.json` | OK | records | records | OK |
| `data/central_valley/vertical.json` | OK | root | root | not specified |
| `data/central_valley_fullyear/decomp.json` | OK | root | root | not specified |
| `data/central_valley_fullyear/meta.json` | OK | root | root | OK |
| `data/central_valley_fullyear/points.json` | OK | missing | missing | OK |
| `data/central_valley_fullyear/summary.json` | OK | root | root | OK |
| `data/fens/crops.json` | OK | root | root | not specified |
| `data/karapinar/area_stats.json` | OK | root | root | not specified |
| `data/karapinar/assets.json` | OK | root | root | OK |
| `data/karapinar/meta.json` | OK | root | root | OK |
| `data/karapinar/points.json` | OK | missing | missing | OK |
| `data/karapinar/sinkholes.geojson` | OK | root | root | OK |
| `data/karapinar/summary.json` | OK | root | root | OK |
| `data/karapinar/uncertainty/meta.json` | OK | root | root | not specified |
| `data/karapinar_p172/meta.json` | OK | root | root | OK |
| `data/karapinar_p172/points.json` | OK | missing | missing | OK |
| `data/karapinar_p172/summary.json` | OK | root | root | OK |
| `data/uk/meta.json` | OK | root | root | OK |
| `data/uk_clay/detection.json` | OK | root | root | not specified |
| `data/uk_clay/meta.json` | OK | root | root | OK |
| `data/uk_clay/points.json` | OK | missing | missing | OK |
| `data/uk_clay/summary.json` | OK | root | root | OK |

### Bulgular
- `data/central_valley/points.json`: dataset-level `quality` missing
- `data/central_valley/points.json`: dataset-level `quality_note` missing
- `data/central_valley_fullyear/points.json`: dataset-level `quality` missing
- `data/central_valley_fullyear/points.json`: dataset-level `quality_note` missing
- `data/karapinar/points.json`: dataset-level `quality` missing
- `data/karapinar/points.json`: dataset-level `quality_note` missing
- `data/karapinar_p172/points.json`: dataset-level `quality` missing
- `data/karapinar_p172/points.json`: dataset-level `quality_note` missing
- `data/uk_clay/points.json`: dataset-level `quality` missing
- `data/uk_clay/points.json`: dataset-level `quality_note` missing

JSON/GeoJSON dosyası: 31; parse hatası: 0; tarih dizisi: 83; points/meta tarih karşılaştırması: 60, uyumsuzluk: 0; bulgu satırı: 10.
## 3. İngilizce metin ve yazım kontrolü (offline)

Kaynak: `web/*.html` (5 dosya). Script/style/noscript içerikleri görünür metin sayılmadı. Dinamik JS ve dış markdown bu statik HTML taramasına dahil değil.

| Satır | Kaynak | Metin | Sorun | Öneri |
|---:|---|---|---|---|
| 23 | `web/science.html` | The main result. Parts of California's Central Valley moved up to −7.8 cm away from the satellite in 108 days; depending on the stable area used as reference the value lies between −4.7 and −7.8 cm. | birimsiz sayı: −4.7 | İlk değerin yanına da `cm` birimini ekle |

Toplam bulgu: 1.
## 4. Oyun modeli: 24 aylık strateji testi (Node, offline)

`game/model.js` değiştirilmedi. `pipeline/pc7/game_strategy_test.js` modeli doğrudan çalıştırdı; her satırda toplam çökme ve kalıcı çökme, 24. ay sonunda en çok çöken bölgenin mutlak dikey değeri; gelir ise modelin vadi toplamı (milyon USD).

| Strateji | Su yılı (iki yıl) | Pompalama | Nadas | Toplam çökme (cm) | Kalıcı çökme (cm) | Gelir (M USD) |
|---|---|---:|---:|---:|---:|---:|
| D0 | Dry | 0% | 0% | 0.08 | 0.00 | 452.1 |
| D50 | Dry | 50% | 0% | 6.05 | 6.03 | 849.9 |
| D100 | Dry | 100% | 0% | 28.87 | 28.84 | 1308.9 |
| D150 | Dry | 150% | 0% | 51.68 | 51.66 | 1748.5 |
| W100 | Wet | 100% | 0% | 0.04 | 0.00 | 1748.1 |
| BN100 | Below Normal | 100% | 0% | 17.62 | 17.60 | 1529.8 |
| D100-F30 | Dry | 100% | 30% | 15.18 | 15.15 | 898.6 |
| W0-F30 | Wet | 0% | 30% | 0.24 | 0.00 | 572.1 |
| W150-F30 | Wet | 150% | 30% | 0.41 | 0.39 | 1292.4 |
| BN50-F30 | Below Normal | 50% | 30% | 0.09 | 0.00 | 739.8 |

Kontroller: 0–150% pompalama serisinde çökme monoton arttı; kalıcı çökme toplam çökme değerini aşmadı; ölçümler sonlu ve negatif olmayan büyüklüklerdi. Bu model çalıştırmasında sayısal hata görülmedi. Daha fazla pompalama daha yüksek gelir de üretti; bu, modelin kısa dönem gelir fonksiyonunun sonucu ve gerçek dünya tahmini olarak yorumlanmamalı. Su yılı sınıfları ve bazı ekonomik/fiziksel parametreler modelde açıklayıcı/temsili olarak işaretlidir.

## 5. Q10 Fens GCOV zaman serisi (yerel kesitler, offline)

Son pull'da sekiz PC2 kesiti bulundu: 2026-06-22, 07-04, 07-16, 08-21, 09-02, 09-14, 09-26 ve 10-08. Hepsinin `quality` değeri `provisional`; aynı EPSG:32630 40 m ızgarasında HH/HV dB alanları var. `pipeline/pc7/analyze_fens_crops.py` her tarihte aynı dört ayrı 12 × 12 piksel (480 m × 480 m) pencerenin sonlu HH/HV piksellerini ortaladı; koordinatlar pencere merkezlerinden dönüştürüldü.

HV dizileri, tarihler yukarıdaki sırada (dB):

| Örnek pencere | HV zaman serisi (dB) | İlk–son değişim (dB) |
|---|---|---:|
| f01 | −16.51, −17.23, −17.09, −13.97, −15.54, −15.67, −17.17, −16.10 | +0.41 |
| f02 | −20.45, −21.56, −21.42, −17.25, −18.14, −17.79, −20.16, −19.75 | +0.70 |
| f03 | −21.18, −22.17, −21.78, −20.39, −20.33, −21.00, −22.25, −20.95 | +0.23 |
| f04 | −22.65, −22.24, −21.61, −18.19, −20.25, −20.07, −22.51, −21.52 | +1.13 |

Dört pencerede de ilk tarihten son tarihe net HV düşüşü yok (son değerler 0.23–1.13 dB daha az negatif); ara tarihlerde ise yön değişiyor. Bu seri tek başına hasat veya sürüm etkisini kanıtlamıyor. Pencereler GCOV dokusundan seçilmiş örnekleme kareleri; kadastro parseli olarak doğrulanmadı.

Çıktılar: `data/fens/crops.json` ve `data/fens/hv_timeseries.png`. JSON parse edildi; tarihler sıralı/benzersiz, alan dizileri tarihlerle aynı uzunlukta ve sonlu, kalite etiketi provisional, yöntem üç cümle. Grafik dosyası oluşturulup görsel olarak açıldı. ASF sorgusu veya veri indirme yapılmadı.

## 6. Polarizasyon karşılaştırması (offline)

`data/fens/crops.json` her örnek pencere için `hh_db`, `hv_db`, doğrusal `hv_hh_ratio` ve `hv_hh_ratio_db` dizilerini içeriyor. Oran, her pikselde `10 ** ((HV_dB − HH_dB) / 10)` ile hesaplandı ve sonra pencere içinde ortalandı; grafikte log oran `10 log10(HV/HH)` olarak gösteriliyor.

| Kanal | Dört pencerenin ortalama zaman aralığı | Okuma |
|---|---:|---|
| HH | 4.27 dB | En büyük gözlenen değişim; zemin, pürüzlülük ve nem de etkiler. |
| HV | 3.49 dB | Daha küçük değişim; bitki örtüsündeki hacim saçılması için daha doğrudan yorumlanabilir. |
| HV/HH | 1.36 dB | En kararlı seri; bu örneklerde daha az zaman değişimi gösterdi. |

Bu ölçülmüş aralıklar HH'nin en geniş sayısal salınımı verdiğini, SAR fiziğinin ise HV'yi bitki yapısı için daha doğrudan gösterge yaptığını ortaya koyuyor. Sekiz tarih ve doğrulanmamış örnek pencereleri ekim/hasat tarihini kanıtlamıyor. Kaynaklar: [NASA NISAR Food Security white paper](https://assets.science.nasa.gov/content/dam/science/missions/nisar/nisar-jpl/pdf/NISAR_Applications_Food_Security1.pdf), [NASA Earthdata SAR Handbook, Chapter 2](https://earthdata.nasa.gov/s3fs-public/2025-04/SARHB_CH2_Content.pdf). NASA StoryMap'in Central Valley/Aqueduct çökme çerçevesi ayrı arazi-hareketi uygulamasıdır: [NISAR StoryMap](https://storymaps.arcgis.com/stories/109e602e748346f3be8dc89124619828).

`docs/story/polarization.md` ve `docs/story/media/pc7_polarization.png` üretildi. Üç kanal için değerler sonlu; JSON oran dizileri 8 tarih uzunluğunda; karşılaştırma grafiği açılıp görsel olarak kontrol edildi.
