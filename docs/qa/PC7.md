# PC7 QA notları

## 1. Link ve dosya yolları (offline)

Yayımlama eşlemesi: `web/` site kökü; `data/`, `game/`, `web3d/` ve `docs/story/` depo kökünden kopyalanıyor.

| Kaynak | Satır | Göreli yol | Repo karşılığı | Kontrol |
|---|---:|---|---|---|
| `web/app.js` | 23 | `data/central_valley/meta.json` | `data/central_valley/meta.json` | OK |
| `web/app.js` | 23 | `data/central_valley/points.json` | `data/central_valley/points.json` | OK |
| `web/app.js` | 23 | `data/central_valley/summary.json` | `data/central_valley/summary.json` | OK |
| `web/app.js` | 24 | `data/central_valley/assets.json` | `data/central_valley/assets.json` | OK |
| `web/app.js` | 24 | `data/central_valley/validation.json` | `data/central_valley/validation.json` | OK |
| `web/app.js` | 25 | `data/karapinar/meta.json` | `data/karapinar/meta.json` | OK |
| `web/app.js` | 25 | `data/karapinar/sinkholes.geojson` | `data/karapinar/sinkholes.geojson` | OK |
| `web/app.js` | 25 | `data/karapinar/summary.json` | `data/karapinar/summary.json` | OK |
| `web/app.js` | 25 | `data/uk/meta.json` | `data/uk/meta.json` | OK |
| `web/app.js` | 37 | `data/central_valley/disp/` | `data/central_valley/disp` | OK |
| `web/app.js` | 68 | `data/uk/radar_${D.uk.date}.png` | `data/uk/radar_*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 71 | `data/central_valley/disp/${m.dates[cvIdx]}.png` | `data/central_valley/disp/*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 92 | `data/karapinar/disp/${m.dates.at(-1)}.png` | `data/karapinar/disp/*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 130 | `data/uk/optical_${D.uk.date}.jpg` | `data/uk/optical_*.jpg` | OK (dynamic pattern has matches) |
| `web/app.js` | 131 | `data/uk/radar_${D.uk.date}.png` | `data/uk/radar_*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 141 | `data/central_valley/disp/${m.dates[i]}.png` | `data/central_valley/disp/*.png` | OK (dynamic pattern has matches) |
| `web/app.js` | 192 | `game/index.html` | `game/index.html` | OK |
| `web/app.js` | 192 | `web3d/index.html` | `web3d/index.html` | OK |
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
| `web/index.html` | 103 | `science.html#risk` | `web/science.html` | OK |
| `web/index.html` | 170 | `data.html` | `web/data.html` | OK |
| `web/index.html` | 170 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 177 | `faq.html` | `web/faq.html` | OK |
| `web/index.html` | 183 | `app.js` | `web/app.js` | OK |
| `web/science.html` | 8 | `style.css` | `web/style.css` | OK |
| `web/science.html` | 12 | `index.html` | `web/index.html` | OK |
| `web/science.html` | 13 | `data.html` | `web/data.html` | OK |
| `web/science.html` | 13 | `faq.html` | `web/faq.html` | OK |
| `web/science.html` | 13 | `index.html#play` | `web/index.html` | OK |
| `web/science.html` | 13 | `index.html#story` | `web/index.html` | OK |
| `web/science.html` | 13 | `science.html` | `web/science.html` | OK |
| `web/science.html` | 60 | `docs.js` | `web/docs.js` | OK |
| `web/science.html` | 62 | `docs/story/calibration_note.md` | `docs/story/calibration_note.md` | OK |
| `web/science.html` | 63 | `docs/story/sources.md` | `docs/story/sources.md` | OK |
| `web/science.html` | 64 | `data/central_valley/validation.json` | `data/central_valley/validation.json` | OK |

Kontrol edilen yerel yol: 67. Eksik: 0.
Eksik yerel yol bulunmadı.

## 2. Veri sözleşmesi (offline)

| Dosya | Parse | quality alanı | quality_note alanı | Sözleşme şeması |
|---|---|---|---|---|
| `data/catalog.json` | OK | records | records | OK |
| `data/central_valley/assets.json` | OK | root | root | OK |
| `data/central_valley/drivers.json` | OK | root | root | OK |
| `data/central_valley/gcov/meta.json` | OK | root | root | OK |
| `data/central_valley/meta.json` | OK | root | root | OK |
| `data/central_valley/points.json` | OK | missing | missing | OK |
| `data/central_valley/summary.json` | OK | root | root | OK |
| `data/central_valley/uncertainty/meta.json` | OK | root | root | not specified |
| `data/central_valley/validation.json` | OK | records | records | OK |
| `data/central_valley/vertical.json` | OK | root | root | not specified |
| `data/karapinar/assets.json` | OK | root | root | OK |
| `data/karapinar/meta.json` | OK | root | root | OK |
| `data/karapinar/points.json` | OK | missing | missing | OK |
| `data/karapinar/sinkholes.geojson` | OK | missing | missing | OK |
| `data/karapinar/summary.json` | OK | root | root | OK |
| `data/karapinar/uncertainty/meta.json` | OK | root | root | not specified |
| `data/uk/meta.json` | OK | root | root | OK |

### Bulgular
- `data/central_valley/points.json`: dataset-level `quality` missing
- `data/central_valley/points.json`: dataset-level `quality_note` missing
- `data/karapinar/points.json`: dataset-level `quality` missing
- `data/karapinar/points.json`: dataset-level `quality_note` missing
- `data/karapinar/sinkholes.geojson`: dataset-level `quality` missing
- `data/karapinar/sinkholes.geojson`: dataset-level `quality_note` missing

JSON/GeoJSON dosyası: 17; parse hatası: 0; tarih dizisi: 40; points/meta tarih karşılaştırması: 24, uyumsuzluk: 0; bulgu satırı: 6.

## 3. İngilizce metin ve yazım kontrolü (offline)

Kaynak: `web/*.html` (5 dosya). Script/style/noscript içerikleri görünür metin sayılmadı. Dinamik JS ve dış markdown bu statik HTML taramasına dahil değil.

| Satır | Kaynak | Metin | Sorun | Öneri |
|---:|---|---|---|---|
| 37 | `web/science.html` | Consecutive 12-day pairs (28 Jun → 14 Oct 2026 for track 34) are summed into a cumulative map. A chain with any gap is not joined. Headline numbers are the most negative median of ~1 km blocks with… | birimsiz sayı: −6.2 | İlk değerin yanına da `cm` birimini ekle |

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
