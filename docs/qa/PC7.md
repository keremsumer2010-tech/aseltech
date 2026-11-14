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
| `web/app.js` | 28 | `data/fens/crops.json` | `data/fens/crops.json` | OK |
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
| `web/app.js` | 215 | `data/central_valley_fullyear/decomp.json` | `data/central_valley_fullyear/decomp.json` | OK |
| `web/app.js` | 253 | `game/index.html` | `game/index.html` | OK |
| `web/app.js` | 253 | `web3d/index.html` | `web3d/index.html` | OK |
| `web/app.js` | 254 | `docs/story/media/cv_subsidence.mp4` | `docs/story/media/cv_subsidence.mp4` | OK |
| `web/data.html` | 8 | `style.css` | `web/style.css` | OK |
| `web/data.html` | 12 | `index.html` | `web/index.html` | OK |
| `web/data.html` | 13 | `data.html` | `web/data.html` | OK |
| `web/data.html` | 13 | `explorer.html` | `web/explorer.html` | OK |
| `web/data.html` | 13 | `faq.html` | `web/faq.html` | OK |
| `web/data.html` | 13 | `index.html#play` | `web/index.html` | OK |
| `web/data.html` | 13 | `index.html#story` | `web/index.html` | OK |
| `web/data.html` | 13 | `science.html` | `web/science.html` | OK |
| `web/data.html` | 38 | `docs.js` | `web/docs.js` | OK |
| `web/data.html` | 42 | `data/catalog.json` | `data/catalog.json` | OK |
| `web/faq.html` | 8 | `style.css` | `web/style.css` | OK |
| `web/faq.html` | 12 | `index.html` | `web/index.html` | OK |
| `web/faq.html` | 13 | `data.html` | `web/data.html` | OK |
| `web/faq.html` | 13 | `explorer.html` | `web/explorer.html` | OK |
| `web/faq.html` | 13 | `faq.html` | `web/faq.html` | OK |
| `web/faq.html` | 13 | `index.html#play` | `web/index.html` | OK |
| `web/faq.html` | 13 | `index.html#story` | `web/index.html` | OK |
| `web/faq.html` | 13 | `science.html` | `web/science.html` | OK |
| `web/faq.html` | 26 | `docs.js` | `web/docs.js` | OK |
| `web/faq.html` | 27 | `docs/story/judge_faq.md` | `docs/story/judge_faq.md` | OK |
| `web/index.html` | 13 | `style.css` | `web/style.css` | OK |
| `web/index.html` | 17 | `index.html` | `web/index.html` | OK |
| `web/index.html` | 19 | `data.html` | `web/data.html` | OK |
| `web/index.html` | 19 | `explorer.html` | `web/explorer.html` | OK |
| `web/index.html` | 19 | `faq.html` | `web/faq.html` | OK |
| `web/index.html` | 19 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 56 | `data.html` | `web/data.html` | OK |
| `web/index.html` | 56 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 64 | `science.html#findings` | `web/science.html` | OK |
| `web/index.html` | 116 | `explorer.html#central_valley_fullyear` | `web/explorer.html` | OK |
| `web/index.html` | 117 | `docs/story/media/pc9_fullyear_point.png` | `docs/story/media/pc9_fullyear_point.png` | OK |
| `web/index.html` | 121 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 141 | `science.html#risk` | `web/science.html` | OK |
| `web/index.html` | 197 | `docs/story/storage_loss.md` | `docs/story/storage_loss.md` | OK |
| `web/index.html` | 198 | `docs/story/engineering_risk.md` | `docs/story/engineering_risk.md` | OK |
| `web/index.html` | 199 | `docs/story/engine.md` | `docs/story/engine.md` | OK |
| `web/index.html` | 211 | `data.html` | `web/data.html` | OK |
| `web/index.html` | 212 | `explorer.html#central_valley` | `web/explorer.html` | OK |
| `web/index.html` | 232 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 236 | `assets/simulator.jpg` | `web/assets/simulator.jpg` | OK |
| `web/index.html` | 273 | `data.html` | `web/data.html` | OK |
| `web/index.html` | 273 | `science.html` | `web/science.html` | OK |
| `web/index.html` | 280 | `faq.html` | `web/faq.html` | OK |
| `web/index.html` | 286 | `app.js` | `web/app.js` | OK |
| `web/index.html` | 293 | `docs/story/technical_note.md` | `docs/story/technical_note.md` | OK |
| `web/science.html` | 8 | `style.css` | `web/style.css` | OK |
| `web/science.html` | 12 | `index.html` | `web/index.html` | OK |
| `web/science.html` | 13 | `data.html` | `web/data.html` | OK |
| `web/science.html` | 13 | `explorer.html` | `web/explorer.html` | OK |
| `web/science.html` | 13 | `faq.html` | `web/faq.html` | OK |
| `web/science.html` | 13 | `index.html#play` | `web/index.html` | OK |
| `web/science.html` | 13 | `index.html#story` | `web/index.html` | OK |
| `web/science.html` | 13 | `science.html` | `web/science.html` | OK |
| `web/science.html` | 90 | `data.html#reproduce` | `web/data.html` | OK |
| `web/science.html` | 95 | `docs.js` | `web/docs.js` | OK |
| `web/science.html` | 97 | `docs/story/calibration_note.md` | `docs/story/calibration_note.md` | OK |
| `web/science.html` | 98 | `docs/story/sources.md` | `docs/story/sources.md` | OK |
| `web/science.html` | 99 | `docs/story/key_findings.md` | `docs/story/key_findings.md` | OK |
| `web/science.html` | 100 | `docs/story/literature_comparison.md` | `docs/story/literature_comparison.md` | OK |
| `web/science.html` | 101 | `docs/story/uncertainty.md` | `docs/story/uncertainty.md` | OK |
| `web/science.html` | 102 | `docs/story/validation_report.md` | `docs/story/validation_report.md` | OK |
| `web/science.html` | 103 | `docs/story/risk_dossier.md` | `docs/story/risk_dossier.md` | OK |
| `web/science.html` | 104 | `data/central_valley/summary.json` | `data/central_valley/summary.json` | OK |
| `web/science.html` | 113 | `data/central_valley/validation.json` | `data/central_valley/validation.json` | OK |

Kontrol edilen yerel yol: 89. Eksik: 0.
Eksik yerel yol bulunmadı.
## 2. Veri sözleşmesi (offline)

| Dosya | Parse | quality alanı | quality_note alanı | Sözleşme şeması |
|---|---|---|---|---|
| `data/catalog.json` | OK | records | records | OK |
| `data/central_valley/area_stats.json` | OK | root | root | not specified |
| `data/central_valley/assets.json` | OK | root | root | OK |
| `data/central_valley/assets_prob.json` | OK | root | root | not specified |
| `data/central_valley/drivers.json` | OK | root | root | OK |
| `data/central_valley/exposure.json` | OK | root | root | not specified |
| `data/central_valley/gcov/meta.json` | OK | root | root | OK |
| `data/central_valley/grid.json` | OK | root | root | not specified |
| `data/central_valley/meta.json` | OK | root | root | OK |
| `data/central_valley/points.json` | OK | missing | missing | OK |
| `data/central_valley/summary.json` | OK | root | root | OK |
| `data/central_valley/uncertainty/meta.json` | OK | root | root | not specified |
| `data/central_valley/validation.json` | OK | records | records | OK |
| `data/central_valley/vertical.json` | OK | root | root | not specified |
| `data/central_valley_fullyear/decomp.json` | OK | root | root | not specified |
| `data/central_valley_fullyear/meta.json` | OK | root | root | OK |
| `data/central_valley_fullyear/points.json` | OK | missing | missing | OK |
| `data/central_valley_fullyear/storage_loss.json` | OK | root | root | not specified |
| `data/central_valley_fullyear/summary.json` | OK | root | root | OK |
| `data/central_valley_p114_fullyear/meta.json` | OK | root | root | OK |
| `data/central_valley_p114_fullyear/points.json` | OK | missing | missing | OK |
| `data/central_valley_p114_fullyear/segments.json` | OK | root | missing | not specified |
| `data/central_valley_p114_fullyear/summary.json` | OK | root | root | OK |
| `data/central_valley_p114_fullyear/winter/meta.json` | OK | root | root | OK |
| `data/central_valley_p114_fullyear/winter/points.json` | OK | missing | missing | OK |
| `data/central_valley_p114_fullyear/winter/summary.json` | OK | root | root | OK |
| `data/central_valley_s1/cross_sensor.json` | OK | root | root | not specified |
| `data/delta/meta.json` | OK | root | root | OK |
| `data/delta/points.json` | OK | missing | missing | OK |
| `data/delta/summary.json` | OK | root | root | OK |
| `data/fens/crops.json` | OK | root | root | not specified |
| `data/global/atlas.json` | OK | root | root | not specified |
| `data/global/beijing/meta.json` | OK | root | root | OK |
| `data/global/beijing/points.json` | OK | missing | missing | OK |
| `data/global/beijing/summary.json` | OK | root | root | OK |
| `data/global/beijing/validation_note.json` | OK | missing | missing | not specified |
| `data/global/central_valley/validation_note.json` | OK | missing | missing | not specified |
| `data/global/delta/validation_note.json` | OK | missing | missing | not specified |
| `data/global/isfahan/coverage.json` | OK | root | missing | not specified |
| `data/global/isfahan/meta.json` | OK | root | root | OK |
| `data/global/isfahan/points.json` | OK | missing | missing | OK |
| `data/global/isfahan/summary.json` | OK | root | root | OK |
| `data/global/isfahan/validation_note.json` | OK | missing | missing | not specified |
| `data/global/jakarta/meta.json` | OK | root | root | OK |
| `data/global/jakarta/points.json` | OK | missing | missing | OK |
| `data/global/jakarta/summary.json` | OK | root | root | OK |
| `data/global/jakarta/validation_note.json` | OK | missing | missing | not specified |
| `data/global/karapinar/validation_note.json` | OK | missing | missing | not specified |
| `data/global/konya_plain/validation_note.json` | OK | missing | missing | not specified |
| `data/global/mexico_city/meta.json` | OK | root | root | OK |
| `data/global/mexico_city/points.json` | OK | missing | missing | OK |
| `data/global/mexico_city/summary.json` | OK | root | root | OK |
| `data/global/mexico_city/validation_note.json` | OK | missing | missing | not specified |
| `data/global/tehran/meta.json` | OK | root | root | OK |
| `data/global/tehran/points.json` | OK | missing | missing | OK |
| `data/global/tehran/summary.json` | OK | root | root | OK |
| `data/global/tehran/validation_note.json` | OK | missing | missing | not specified |
| `data/karapinar/area_stats.json` | OK | root | root | not specified |
| `data/karapinar/assets.json` | OK | root | root | OK |
| `data/karapinar/drivers.json` | OK | root | root | OK |
| `data/karapinar/exposure.json` | OK | root | root | not specified |
| `data/karapinar/grid.json` | OK | root | root | not specified |
| `data/karapinar/meta.json` | OK | root | root | OK |
| `data/karapinar/points.json` | OK | missing | missing | OK |
| `data/karapinar/sinkholes.geojson` | OK | root | root | OK |
| `data/karapinar/summary.json` | OK | root | root | OK |
| `data/karapinar/uncertainty/meta.json` | OK | root | root | not specified |
| `data/karapinar_fullyear/meta.json` | OK | root | root | OK |
| `data/karapinar_fullyear/points.json` | OK | missing | missing | OK |
| `data/karapinar_fullyear/segments.json` | OK | root | missing | not specified |
| `data/karapinar_fullyear/summary.json` | OK | root | root | OK |
| `data/karapinar_p172/meta.json` | OK | root | root | OK |
| `data/karapinar_p172/points.json` | OK | missing | missing | OK |
| `data/karapinar_p172/summary.json` | OK | root | root | OK |
| `data/konya_plain/exposure.json` | OK | root | root | not specified |
| `data/konya_plain/meta.json` | OK | root | root | OK |
| `data/konya_plain/points.json` | OK | missing | missing | OK |
| `data/konya_plain/summary.json` | OK | root | root | OK |
| `data/uk/meta.json` | OK | root | root | OK |
| `data/uk_clay/detection.json` | OK | root | root | not specified |
| `data/uk_clay/grid.json` | OK | root | root | not specified |
| `data/uk_clay/meta.json` | OK | root | root | OK |
| `data/uk_clay/points.json` | OK | missing | missing | OK |
| `data/uk_clay/summary.json` | OK | root | root | OK |

### Bulgular
- `data/central_valley/points.json`: dataset-level `quality` missing
- `data/central_valley/points.json`: dataset-level `quality_note` missing
- `data/central_valley_fullyear/points.json`: dataset-level `quality` missing
- `data/central_valley_fullyear/points.json`: dataset-level `quality_note` missing
- `data/central_valley_p114_fullyear/points.json`: dataset-level `quality` missing
- `data/central_valley_p114_fullyear/points.json`: dataset-level `quality_note` missing
- `data/central_valley_p114_fullyear/segments.json`: dataset-level `quality_note` missing
- `data/central_valley_p114_fullyear/winter/points.json`: dataset-level `quality` missing
- `data/central_valley_p114_fullyear/winter/points.json`: dataset-level `quality_note` missing
- `data/delta/points.json`: dataset-level `quality` missing
- `data/delta/points.json`: dataset-level `quality_note` missing
- `data/global/beijing/points.json`: dataset-level `quality` missing
- `data/global/beijing/points.json`: dataset-level `quality_note` missing
- `data/global/beijing/validation_note.json`: dataset-level `quality` missing
- `data/global/beijing/validation_note.json`: dataset-level `quality_note` missing
- `data/global/central_valley/validation_note.json`: dataset-level `quality` missing
- `data/global/central_valley/validation_note.json`: dataset-level `quality_note` missing
- `data/global/delta/validation_note.json`: dataset-level `quality` missing
- `data/global/delta/validation_note.json`: dataset-level `quality_note` missing
- `data/global/isfahan/coverage.json`: dataset-level `quality_note` missing
- `data/global/isfahan/points.json`: dataset-level `quality` missing
- `data/global/isfahan/points.json`: dataset-level `quality_note` missing
- `data/global/isfahan/validation_note.json`: dataset-level `quality` missing
- `data/global/isfahan/validation_note.json`: dataset-level `quality_note` missing
- `data/global/jakarta/points.json`: dataset-level `quality` missing
- `data/global/jakarta/points.json`: dataset-level `quality_note` missing
- `data/global/jakarta/validation_note.json`: dataset-level `quality` missing
- `data/global/jakarta/validation_note.json`: dataset-level `quality_note` missing
- `data/global/karapinar/validation_note.json`: dataset-level `quality` missing
- `data/global/karapinar/validation_note.json`: dataset-level `quality_note` missing
- `data/global/konya_plain/validation_note.json`: dataset-level `quality` missing
- `data/global/konya_plain/validation_note.json`: dataset-level `quality_note` missing
- `data/global/mexico_city/points.json`: dataset-level `quality` missing
- `data/global/mexico_city/points.json`: dataset-level `quality_note` missing
- `data/global/mexico_city/validation_note.json`: dataset-level `quality` missing
- `data/global/mexico_city/validation_note.json`: dataset-level `quality_note` missing
- `data/global/tehran/points.json`: dataset-level `quality` missing
- `data/global/tehran/points.json`: dataset-level `quality_note` missing
- `data/global/tehran/validation_note.json`: dataset-level `quality` missing
- `data/global/tehran/validation_note.json`: dataset-level `quality_note` missing
- `data/karapinar/points.json`: dataset-level `quality` missing
- `data/karapinar/points.json`: dataset-level `quality_note` missing
- `data/karapinar_fullyear/points.json`: dataset-level `quality` missing
- `data/karapinar_fullyear/points.json`: dataset-level `quality_note` missing
- `data/karapinar_fullyear/segments.json`: dataset-level `quality_note` missing
- `data/karapinar_p172/points.json`: dataset-level `quality` missing
- `data/karapinar_p172/points.json`: dataset-level `quality_note` missing
- `data/konya_plain/points.json`: dataset-level `quality` missing
- `data/konya_plain/points.json`: dataset-level `quality_note` missing
- `data/uk_clay/points.json`: dataset-level `quality` missing
- `data/uk_clay/points.json`: dataset-level `quality_note` missing

JSON/GeoJSON dosyası: 84; parse hatası: 0; tarih dizisi: 218; points/meta tarih karşılaştırması: 175, uyumsuzluk: 0; bulgu satırı: 51.
## 3. İngilizce metin ve yazım kontrolü (offline)

Kaynak: `web/*.html` (6 dosya). Script/style/noscript içerikleri görünür metin sayılmadı. Dinamik JS ve dış markdown bu statik HTML taramasına dahil değil.

| Satır | Kaynak | Metin | Sorun | Öneri |
|---:|---|---|---|---|
| 20 | `web/data.html` | Reproduce our data in 5 steps | birimsiz sayı: 5 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: -120.2 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 35.6 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: -119 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 35.6 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: -119 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 36.6 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: -120.2 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 36.6 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: -120.2 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 35.6 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 06 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 17 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 10 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 24 | `web/data.html` | import asf_search as asf asf.search(platform="NISAR", processingLevel="GUNW", intersectsWith="POLYGON((-120.2 35.6,-119 35.6,-119 36.6,-120.2 36.6,-120.2 35.6))", start="2026-06-17", end="2026-10-31") | birimsiz sayı: 31 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 28 | `web/data.html` | Download and cut each pair to the study box (about 2.4 GB in, 20 MB out): python analysis/fetch_subset.py central_valley 34 020 100 (track 34, frame 20). | birimsiz sayı: 2.4 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 28 | `web/data.html` | Download and cut each pair to the study box (about 2.4 GB in, 20 MB out): python analysis/fetch_subset.py central_valley 34 020 100 (track 34, frame 20). | birimsiz sayı: 020 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 28 | `web/data.html` | Download and cut each pair to the study box (about 2.4 GB in, 20 MB out): python analysis/fetch_subset.py central_valley 34 020 100 (track 34, frame 20). | birimsiz sayı: 100 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 32 | `web/data.html` | Needs Python 3.11+ and pip install asf_search h5py numpy scipy matplotlib pyproj rasterio shapely requests pytest . Without an Earthdata login you can still open every file on this page. | birimsiz sayı: 3.11 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 101 | `web/index.html` | Two radar “colours”. NISAR sends and receives its pulses in different orientations. In 4 field-like areas of the Fens, the HH signal is about 7 dB brighter than HV, which comes mostly from the 3-D … | birimsiz sayı: 7 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 101 | `web/index.html` | Two radar “colours”. NISAR sends and receives its pulses in different orientations. In 4 field-like areas of the Fens, the HH signal is about 7 dB brighter than HV, which comes mostly from the 3-D … | birimsiz sayı: 3 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 117 | `web/index.html` | Mixed series: 18 pre-calibration beta + 7 provisional radar image pairs. Analysis: Team Taykut. | birimsiz sayı: 18 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 117 | `web/index.html` | Mixed series: 18 pre-calibration beta + 7 provisional radar image pairs. Analysis: Team Taykut. | birimsiz sayı: + 7 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 118 | `web/index.html` | From the air to space. NASA's NISAR StoryMap on land subsidence shows a “subsidence bowl” along the California Aqueduct in the Central Valley, measured with NASA's airborne radar UAVSAR between 201… | birimsiz sayı: 40 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 119 | `web/index.html` | Land Subsidence StoryMap — Peacock, A., An, K., Pinto, N. & Lou, Y. (2024), NISAR ArcGIS StoryMaps, Zenodo, doi:10.5281/zenodo.10818833 . UAVSAR data courtesy NASA/JPL-Caltech. | birimsiz sayı: 10818833 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |
| 23 | `web/science.html` | The main result. Parts of California's Central Valley moved up to −7.8 cm away from the satellite in 108 days; depending on the stable area used as reference the value lies between −4.7 and −7.8 cm. | birimsiz sayı: −4.7 | İlk değerin yanına da `cm` birimini ekle |
| 90 | `web/science.html` | Find and download NISAR data yourself: ASF Vertex · our guide “Reproduce our data in 5 steps” . | birimsiz sayı: 5 | Ölçümse birim/tarih ekle; sayım veya kimlikse açıkça adlandır |

Toplam bulgu: 27.
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

## 8. 20:00 hata ayıklama 1 — tam yıl görsel yolu

`web/app.js` içindeki `fullYear()` `ROOT + im.dataset.src` ile görseli yüklediğinden mevcut `data-src="docs/story/media/pc9_fullyear_point.png"` yolu yerel `/web/` ve yayın kökünde doğrudur; dosya repoda vardır. Son değişiklik PC3'ten 15 dakikadan eskiydi. `web/index.html` içindeki boş `src=""` kaldırıldı; böylece başlangıçta sayfanın kendisi görsel diye istenmez, uygulama aynı `data-src` yükleyicisini kullanır.

## 9. 20:00 hata ayıklama 2 — Explorer kalibrasyon uyarısı

`web/explorer.html` kontrol paneline site genelindeki sabit kalibrasyon/validasyon açıklaması eklendi. `.disclaimer` stili zaten `web/style.css` içinde mevcut; yeni stil gerekmedi. Metin NISAR ürünlerinin provisional olduğunu ve kalibrasyon/doğrulamanın NASA-JPL/ISRO proje sorumluluğunda olduğunu açıkça söylüyor.

## 10. 20:00 hata ayıklama 3 — Python gereksinimleri

Repo kökünde önceden `requirements.txt` yoktu. İstenen Python paketleri (`asf_search`, `h5py`, `numpy`, `scipy`, `matplotlib`, `pyproj`, `rasterio`, `shapely`, `requests`, `pytest`, `Pillow`) kurulum gereksinimi olarak eklendi; bu görevde paket indirme/kurma yapılmadı.

## 11. 20:00 hata ayıklama 4 — tam pytest

`python -m pytest -q` çalıştırıldı. 110 saniyeden uzun süre stdout/stderr üretmedi ve tamamlanmadı; komut Ctrl+C ile durduruldu. Bu nedenle test sonucu **alınamadı**; PASS/FAIL sayısı raporlanmıyor. Paket kurulumu veya test verisi indirmesi yapılmadı.

## 12. 20:00 hata ayıklama 5 — veri JSON denetimi

`pipeline/pc7/validate_json.py` tüm `data/**/*.json` dosyalarını UTF-8 ile okur; JSON parse hatalarını, `NaN`/`Infinity` sabitlerini ve taşma sonucu oluşan sonlu olmayan sayıları arar. Kök kalite alanı olmayan `points.json` dizilerinde aynı klasördeki `meta.json` kalitesini açıkça miras kabul eder; diğer belgelerde kalite alanını veya katalog kayıtlarındaki katman kalitesini denetler.

Çalıştırma: `python pipeline/pc7/validate_json.py`. Sonuç: **61 JSON**, 0 parse/standart dışı sabit hatası, 0 sonlu olmayan sayı, 0 kalite etiketi eksik dosya; 12 `points.json` kaliteyi kardeş `meta.json` dosyasından alıyor. Bu denetim mevcut dosyaları değiştirmez.

## 7. 20:00 hata ayıklama turu — madde 1

`web/index.html` satır 117'de `src=""` ve `data-src="docs/story/media/pc9_fullyear_point.png"` bulunuyor. `web/app.js` içindeki `fullYear()` yükleyicisi `ROOT + im.dataset.src` kullanıyor; Pages ve yerel `/web/` köklerini destekliyor. Ancak `web/index.html` son commit'i `4317bc1` (`20:09:26 +03:00`), bu kontrol `20:22` civarında yapıldı; PC1 notundaki 15 dakika koruması nedeniyle dosyaya dokunulmadı. `src=""` boş bırakılması tarayıcının geçerli sayfayı görsel olarak tekrar istemesine neden olabilir; en yakın güvenli düzeltme, 15 dakika geçtikten sonra boş `src` niteliğini kaldırıp `data-src` yükleyicisini korumaktır. Bu adımda dosya değiştirilmedi.

## 13. 20:10 O2 — olasılıksal altyapı riski (offline)

- `risk/probabilistic_risk.py`, PC5'in Cramér–Rao fonksiyonunu yerel yedi provisional Central Valley kesitinde kullandı. Bbox içi yeniden hesaplanan sigma medyanı `0.2943 cm` LOS; meta'daki yuvarlatılmış değer `0.294 cm` ile uyumlu.
- `risk/central_valley_infra.geojson` içindeki 3.238 OSM hattının tamamı tarandı; en az iki geçerli profil örneği olan **2.082** hat skorlandı. `data/central_valley/assets.json` deterministik ilk on listeyi karşılaştırma için koruyor. 100 m profillerde yerel incidence rasterıyla LOS→dikey tahmin, 100/500/1000 m β pencereleri, 1000 seeded Monte Carlo, iki eşik olasılığı, 10 cm diferansiyel olasılığı ve koşullu %90 aralık üretildi.
- `python -m pytest -q risk/test_probabilistic_risk.py`: **2 passed** (bilinen eğim/β ve σ=0 kesin olasılık uçları). `python risk/probabilistic_risk.py` 2.082 skorlanabilir satır üretti; JSON `quality: provisional`, `allow_nan=False`. `python pipeline/pc7/validate_json.py`: **70 JSON**, parse/non-standard constant hatası 0, non-finite sayı 0, kalite etiketi eksiği 0; 14 `points.json` kardeş `meta.json` kalitesini miras alıyor.
- Skorlanan tüm 2.082 hatta `P(β > 1/500) = 0/1000` ve `P(β > 1/1000) = 0/1000`; en büyük β `0.00072276`, `1/1000` değerinden küçük. Beş hatta `P(Δ > 10 cm)>0`. OSM `196530229` Exeter Subdivision'da maksimum diferansiyel `12.564 cm` ve `P(Δ > 10 cm)=1.0`. Sıfır eşik geçişi 1000 deneme çözünürlüğündeki tahmindir, sıfır gerçek risk kanıtı değildir.
- Olasılıksal ilk on, eski deterministik `assets.json` ilk onuyla **1/10** OSM kimliği paylaşıyor (`196530229`). California Aqueduct OSM `24016778`, mevcut gradyan listesinde 4.; tüm skorlanan hatlar arasında olasılık ekranı sırası 39. β `0.00036111`, diferansiyel `4.557 cm`, `P(Δ>10 cm)=0/1000`; mevcut gradyan `49.12 mm/km`.
- Kaynak denetimi: `docs/OZGUN_KATKILAR.md` Skempton & MacDonald (1956), Boscardin & Cording (1989) ve yaklaşık `1/300–1/500` bağlamını anıyor; yerel kaynak kataloğunda tam künye/orijinal metin yok. İstenen `1/500` ve `1/1000` raporda yalnız screening/sensitivity kesitleri; `1/1000` yayımlanmış hasar sınırı veya tasarım standardı diye sunulmuyor. Aqueduct/Friant-Kern tarihsel bağlamı yerel [USGS SIR 2018-5144](https://pubs.usgs.gov/publication/sir20185144) ve [KVPR 2017](https://www.kvpr.org/environment/2017-08-03/friant-kern-canal-slows-by-60-percent-subsidence-to-blame) kaynak kayıtlarıyla sınırlandı.
- Sınırlar: formel faz gürültüsü alt sınırı atmosfer/ramp/unwrapping hatalarını ve örnekler arası korelasyonu içermiyor; dönem tek provisional yaz zinciri; LOS→dikey yatay hareketi ihmal ediyor; kanal enkesiti/su seviyesi/freeboard ölçüsü yok, diferansiyel yalnız proxy; 1,156 çizgi iki geçerli örnek sağlayamadı. Çıktı emniyet/hasar değerlendirmesi değildir.

Rapor: `docs/story/engineering_risk.md`; veri: `data/central_valley/assets_prob.json`; grafik: `docs/story/media/pc7_risk_prob.png`; kod/test: `risk/probabilistic_risk.py`, `risk/test_probabilistic_risk.py`.

## 14. Global atlas kalite standardı ve O2 yeniden kontrolü

`python tools/validate_atlas.py` ile `data/global/atlas.json` ve şehir dizinleri kontrol edildi. Son pull'da PC10 Mexico City'yi −7.0 cm olarak yeniden hesapladı; PC5 sekiz `validation_note.json` dosyası ekledi. Isfahan `data/global/isfahan/` verisi de mevcut fakat henüz atlas listesinde yok. Doğrulayıcı 8 atlas bölgesini ve toplam 9 şehir dizinini inceledi; atlas ve şehir ağaçlarındaki **46 JSON** dosyasında parse/NaN/sonsuz sayı bulgusu yok. Komut **128 bulgu** ile beklenen exit code `1` döndürdü: **119 sözleşme hatası, 9 referans uyarısı**. Atlasın `regions` sıralaması saklanan `rate_cm_per_100d` alanlarıyla uyumlu.

| Şehir | meta bbox boyutu (lon × lat) | gün | atlas/summary hızı cm/100d | ref aralığı / başlık |
|---|---:|---:|---:|---|
| Beijing | 0.60° × 0.40° | 120 | −1.2 / −1.17 (özet türevi) | 442.9%, n=3 |
| Central Valley | 1.20° × 1.00° | 108 | −7.2 / −7.22 (özet türevi) | 39.7%, n=3 |
| Jakarta | 0.37° × 0.30° | 108 | −6.3 / −6.30 (özet türevi) | aralık yok, n=1 |
| Karapınar | 0.50° × 0.30° | 108 | −5.5 / −5.46 (özet türevi) | aralık yok, n=1 |
| Mexico City | 0.35° × 0.35° | 120 | −5.8 / −5.83 (özet türevi) | 48.6%, n=3 |
| Tehran | 0.55° × 0.40° | 120 | −2.9 / −2.92 (özet türevi) | 108.6%, n=2 |
| Konya Plain | 1.50° × 0.70° | 108 | −8.9 / −8.89 (özet türevi) | 45.8%, n=3 |
| Delta | 0.40° × 0.25° | 120 | −1.1 / −1.08 (özet türevi) | 15.4%, n=2 |
| Isfahan | 0.60° × 0.60° | 120 | −2.08 (summary; atlas girdisi yok) | 72.0%, n=3 |

Bbox hedefi her iki boyutta `0.50°` (merkez ±`0.25°`); dokuz şehir klasörünün her birinde en az bir boyut uygunsuz. Hız denetimi `headline × 100 / (end-start gün)` formülünü kullanıyor; `0.051 cm/100d` tolerans bir ondalıkla yuvarlanmış atlas değerlerini kabul ediyor. Mexico City `−5.8` bu toleransta tutarlı; summary alanı `−5.8`, p2 `−5.7`, valid fraction `0.639`, ancak confidence `null` ve `ref_range_cm` boş. Summary'sinde `confidence`/`valid_fraction` alanları eksik olan legacy şehirler de var.

Atlasın yeni kalite alanlarında kalan eksikler: Konya ve Delta için `p2_cm` ile `valid_fraction` null; Jakarta ve Karapınar için `ref_range_cm` null. Bu eksikler `reliable`/`indicative` kopyalarında da mevcut. Isfahan'ın `summary.json` alanları `p2_cm=−2.9`, `rate_cm_per_100d=−2.08`, `confidence=medium`, `valid_fraction=0.325`; gün aralığı hesabıyla hız tutarlı ve orta güven etiketi ≥0.40 high koşulunu ihlal etmiyor. Fakat bbox `0.60° × 0.60°`, referans aralığı/başlık `72%`, `ref_range_cm` yok ve atlas kaydı yok.

Hiçbir şehirde açık `reference_outside_basin` kanıt alanı yok. Bu yüzden havza dışı referansın coğrafi/jeolojik konumu kesin doğrulanamıyor; ref aralığı proxy'si dokuz şehir için de 3 alternatif ve `<30%` ölçütünü karşılamadı veya gerekli aralık bulunmadı. Atlas JSON'unda 16 boş `note` alanı var (8 `regions`, 5 `reliable`, 3 `indicative`). Güven sınıfı/geçerli alan uyumunda high sınıfına ait bir ihlal bulunmadı; ancak Konya ve Delta'nın atlas `valid_fraction` değeri boş olduğu için güven koşulu doğrulanamıyor.

`python pipeline/pc7/validate_json.py`: **83 JSON**, parse/non-standard constant hatası 0, non-finite sayı 0, **4 quality alanı eksiği** (`data/global/{central_valley,delta,karapinar,konya_plain}/validation_note.json`); 20 `points.json`/not dosyası kaliteyi kardeş meta'dan alıyor. PC5'in kaynak dosyalarına dokunulmadı.

O2 yeniden kontrolü: olasılıksal risk kodu/verisi/raporu/grafiği mevcut; `technical_note.md/html` ve `project_page.md` sonuçları içeriyor. `python -m pytest -q risk/test_probabilistic_risk.py`: **2 passed**. Eşik kaynaklarının tam bibliyografisi yerel kaynak kaydında hâlâ yok; O2 raporunda eşikler yalnız tarama/sensitivity değeri olarak sunuluyor.

Doğrulayıcı: `tools/validate_atlas.py` (çevrimdışı, salt-okunur). `python -m py_compile tools/validate_atlas.py` başarılı. Yeni şehir eklendiğinde `python tools/validate_atlas.py` yeniden çalıştırılmalı. PC10 atlas/verileri ve PC5 validation notları değiştirilmedi.

## 15. ASLA BOŞ KALMA — güncel yerel doğrulama turu

- Pull sonrası web yolları denetimi: `python pipeline/pc7/offline_site_qa.py paths` başarılı; 89 yerel yol bulundu, eksik yok.
- Veri sözleşmesi taraması: `python pipeline/pc7/offline_site_qa.py data` 84 JSON/GeoJSON dosyasında 0 parse hatası, 218 sıralı tarih dizisi ve 175 `points.json`/`meta.json` tarih karşılaştırmasında 0 uyumsuzluk buldu. Ayrıntılı kalite alanı uyarıları bu raporun §2 tablosunda; eksikler diğer sahiplerin dosyalarında olduğundan değiştirilmedi.
- `python pipeline/pc7/validate_json.py`: 83 JSON; 0 parse/non-standard constant hatası, 0 non-finite sayı; 4 eksik `quality` (`data/global/{central_valley,delta,karapinar,konya_plain}/validation_note.json`). 20 dosyada kalite kardeş `meta.json` üzerinden miras alınıyor.
- Atlas denetimi `python tools/validate_atlas.py`: 8 atlas kaydı ve 9 şehir klasörü; 128 bulgu (119 hata, 9 uyarı). Esas kalanlar şehir bbox'larının 0.50° standardına uymaması, eksik özet/atlas metrikleri, referans havzası kanıtı, boş `note` alanları ve Isfahan'ın atlas kaydının olmaması. Şehir klasörleri ve `atlas.json` PC10/diğer veri sahiplerine ait olduğundan değiştirilmedi.
- Genel `python -m pytest -q` toplama aşamasında durdu: `analysis/pc5/test_cross_sensor.py` ve `pipeline/nisarpulse/tests/test_nisarpulse.py`, eksik `requests` modülü yüzünden import edilemedi. Bu çevrimdışı turda paket kurulmadı/indirilmedi. PC7 O2 testi ayrı olarak `2 passed`.
- Fens analizi yerel `pipeline/subset/fens_gcov/` kesitlerinden tekrar üretildi; `data/fens/crops.json` önceki sürümle semantik olarak aynı. Veri indirme yapılmadı.
- `node pipeline/pc7/game_strategy_test.js`: 10 stratejinin tamamı 24 ay çalıştı; kuru yıl %0–150 pompalama serisi monoton, kalıcı çökme toplamı aşmıyor, gelir ve çökme değerleri sonlu ve negatif değil.
- `python pipeline/pc7/offline_site_qa.py text` 27 statik metin uyarısı verdi. Bunların çoğu kod örneklerindeki koordinat/ürün kimliği, tarih veya sayım değerleri; olası gerçek birimsiz metin bulgusu `web/science.html` içindeki `−4.7` değeridir. Site sahipliği PC3/PC1'de olduğundan düzenleme yapılmadı; bulgu sahibi dosyasında düzeltilecek.
- PC7'nin atlas şehir klasörü ataması yok; PC11 şehirlerini yeniden çalıştırmadım ve PC11 status/görev dosyalarına yazmadım. Fens, risk ve QA çıktıları dışında başka sahiplerin dosyaları değiştirilmedi.

## 16. Atlas sağlamlık taraması (yerel, provisional, indirmesiz)

`python pipeline/pc7/atlas_robustness.py` sekiz `atlas.json` şehrinin yerel provisional GUNW çift zincirlerini denedi. Her varyant; üç referans adayı, koherens `0.3/0.4/0.5` ve ±`0.20/0.25/0.30°` kutu kombinasyonudur. Başlık her varyantta 13×13 piksel blok medyanlarının en negatifi (≥%50 geçerli piksel, blok std ≤2 cm); p2 ayrıca kaydedilir. Alt kümeler istenen kutunun ≥%98'ini kapsamıyorsa varyant geçersiz bırakılır.

| Şehir | Referans adayı | Geçerli / denenebilir varyant | Başlık aralığı (cm) | Hız aralığı (cm/100 gün) | Neden/sonuç |
|---|---:|---:|---:|---:|---|
| Beijing | 3 | 9/27 | −4.4178 … −2.6638 | −3.68151 … −2.21985 | ±0.20° tümü; daha geniş kutular veri kapsama şartını karşılamadı |
| Central Valley | 3 | 27/27 | −7.8168 … −2.4806 | −7.23780 … −2.29682 | Tüm varyantlar hesaplandı |
| Delta | 0 | 0 | — | — | ±0.20° kutu kapsaması 0.7244 |
| Jakarta | 0 | 0 | — | — | ±0.20° kutu kapsaması 0.8427 |
| Karapınar | 0 | 0 | — | — | ±0.20° kutu kapsaması 0.8454 |
| Konya Plain | 1 | 0 | — | — | Üç referans köşesi için yeterli ortak-geçerli pencere yok |
| Mexico City | 0 | 0 | — | — | ±0.20° kutu kapsaması 0.9324 |
| Tehran | 1 | 0 | — | — | Üç referans köşesi için yeterli ortak-geçerli pencere yok |

İlk üç şehir sırasının sabitliği **sonuçlandırılamadı**: tüm 27 varyantı tamamlanmış yalnız bir şehir var; geçerli üçlü şehir sıralaması yok. Bu yüzden Kendall tau hesaplanamadı (`n_variant_rankings=0`). Referans adayları kutu köşelerindeki yüksek koherensli/düşük göreli hareketli pencerelerden seçilir; jeolojik havza dışı veya bağımsız GPS ile sabit oldukları doğrulanmış değildir. Yöntem bu sınırlamayı `data/global/robustness.json` içinde açıkça bildirir; `atlas.json` değiştirilmedi.

Ağsız testler: `python -m pytest -q pipeline/pc7/tests/test_atlas_robustness.py` — 4 passed. Tam depo: `python -m pytest -q` (Python 3.12.10) — 79 passed, 1 `PendingDeprecationWarning`. Çıktılar: `data/global/robustness.json`, `docs/story/media/pc7_atlas_robustness.png`; ağ/veri indirmesi yapılmadı.

Son JSON doğrulaması `python pipeline/pc7/validate_json.py`: 93 JSON, 0 parse hatası, 0 NaN/Infinity, 0 eksik `quality`; 15 points dosyası kalitesini kardeş `meta.json`'dan alıyor.

## 17. B yeni şehirler — kapsam ve referans ön incelemesi

NISAR Pulse `--dry-run` (2026-06-17–2026-10-31, ±0.25°, provisional) indirme yapmadan üç şehirde de 9 zincir çifti buldu; kapsama var, dolayısıyla `no coverage` sonucu değil:

| Şehir | ASF path/frame | Tarih aralığı | Tahmini toplam ham veri | Durum |
|---|---|---|---:|---|
| Xi'an | P076 F071 | 2026-06-19–2026-10-17 | 20,976.1 MB | zincir tam; referans doğrulaması gerekiyor |
| Taiyuan | P068 F020 | 2026-06-18–2026-10-16 | 20,247.7 MB | zincir tam; referans doğrulaması gerekiyor |
| Querétaro | P041 F078 | 2026-06-17–2026-10-15 | 20,053.5 MB | zincir tam; referans doğrulaması gerekiyor |

Referans kaynağı kontrolü henüz savunulabilir birer havza-dışı koordinat vermiyor. Xi'an SBAS çalışması kararlı bir referans bölgesini haritada işaretliyor, fakat metin koordinat yayımlamıyor ([Shi et al. 2020](https://www.mdpi.com/2072-4292/12/22/3756), §4.1/Fig. 3). Taiyuan çalışmasında K001 (112.7°E, 37.7°N) düşük düşey hızla kararlı yer olarak tanımlanıyor; ancak koordinat hedef ±0.25° kutunun içinde ve çalışmada referans noktası havza dışında diye belirtilmiyor ([Zhao et al. 2018](https://www.mdpi.com/2072-4292/10/9/1499)). INEGI Querétaro için 2015–2018 PSI haritası yayımlıyor fakat özet kaydı belirli bir kararlı referans koordinatı sağlamıyor ([INEGI, 2019](https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463849674)); ek bir çalışmada şehrin doğu kesimi kararlı alan diye tarif ediliyor, yine de tekil koordinat doğrulanmıyor ([Pacheco-Martínez et al.](https://doczz.net/doc/986787/dinsar-analysis-of-differential-ground-subsidence-affecti...)). Bu yüzden bu aşamada koordinat uydurulmadı ve `ready` denmedi.

`python -m pipeline.nisarpulse run --dry-run` çıktıları yalnız katalog/ASF kapsama ön kontrolüdür; dosya indirme ve üretim analizi henüz yapılmadı. B kalite standardı havza-dışı, bilinen sabit referans gerektirdiğinden bu kanıt tamamlanmadan sonuçları yayımlamak uygun değil. A sağlamlık çıktıları ve `data/global/atlas.json` değiştirilmedi.

## 18. Uzun plan FAZ 1 — provisional kapsam ön kontrolü

Python 3.12.10 ile her şehir için NISAR Pulse `--dry-run`, `--box-deg 0.25`, `2026-06-17`–`2026-10-31`, `quality=provisional`, `--no-catalog` çalıştırıldı. CMR erişimi için ağ izni kullanıldı; dry-run ürün indirmedi.

| Şehir | Tam hedef bbox `[w,s,e,n]` | Path/frame | Zincir | Dönem | Tahmini ham toplam |
|---|---|---|---:|---|---:|
| Xi'an | `[108.70,34.02,109.20,34.52]` | P076/F071 | 9 çift, 0 boşluk | 2026-06-19–2026-10-17 | 20,976.1 MB |
| Taiyuan | `[112.30,37.60,112.80,38.10]` | P068/F020 | 9 çift, 0 boşluk | 2026-06-18–2026-10-16 | 20,247.7 MB |
| Querétaro | `[-100.64,20.34,-100.14,20.84]` | P041/F078 | 9 çift, 0 boşluk | 2026-06-17–2026-10-15 | 20,053.5 MB |
| Aguascalientes | `[-102.54,21.63,-102.04,22.13]` | P041/F077 | 9 çift, 0 boşluk | 2026-06-17–2026-10-15 | 19,905.5 MB |
| Kashmar | `[58.21,34.99,58.71,35.49]` | P078/F071 | 9 çift, 0 boşluk | 2026-06-19–2026-10-17 | 20,354.3 MB |

Bu sonuçlar yalnızca ASF/CMR kapsamasını ve tarih zincirini doğrular; analiz veya “hazır” durumu değildir. Xi'an kaynak taramasında eski InSAR çalışması Xingping'i deformasyonsuz referans yeri olarak tanımlıyor (https://www.tandfonline.com/doi/full/10.1080/19475705.2018.1542350); yayın koordinatlı ölçüm istasyonu vermediği için şehir merkezi koordinatı ölçüm noktası gibi kullanılmayacak. Taiyuan için K001 CGPS (112.7°E,37.7°N) eski çalışmada düşük düşey hızla kararlı olarak tanımlanıyor (https://www.mdpi.com/2072-4292/10/9/1499), fakat çalışmanın aynı metni K001'i havza içinde yer alan istasyon olarak listeliyor; “havza dışı” şartını tek başına karşılamaz. Querétaro literatüründe doğu kesimde kararlı deformasyon alanı tarif ediliyor, ancak sayısal sabit nokta koordinatı bu taramada doğrulanmadı (https://doczz.net/doc/986787/dinsar-analysis-of-differential-ground-subsidence-affecti...). Referans doğrulaması çözülmeden referans uydurulmayacak ve `hazır` beyanı yapılmayacak.

## 19. Xi'an üretim hattı hazırlığı

`pipeline/pc7/run_atlas_city.py` eklendi ve Python 3.12 ile derleme + bbox/ref koordinat yardımcıları için smoke check geçti. Hat, ASF aramasını hedef ±0.25° kutuda yapar; ham GUNW'yi tek tek indirip genişletilmiş kesit alır, her ham dosyayı kesitten sonra siler ve cumulative motorunu geçici dizinde çalıştırır (PC3 `analysis/out/` dosyalarına yazmaz). Referans koordinatı, kaynakta adı geçen sabit Xingping bölgesindeki yerleşim merkezi yakınıdır: ([Xi'an referans çalışması](https://www.tandfonline.com/doi/full/10.1080/19475705.2018.1542350), [UNGEGN şehir koordinatı](https://ungegn.un.org/dashboard/cities/details?id=2459)). Gerçek 7×7 referans piksel penceresi NISAR gridinden seçilip koordinatı çıktıya yazılır. Üretim analizi henüz başlatılmadı; dosyalar ve indirme logu olmadan `hazır` denmeyecek.

## 20. Atlas kalite bekçisi — Xi'an indirmesi öncesi taban çizgisi

`python tools/validate_atlas.py` salt-okunur çalıştırmasında **11 atlas kaydı, 12 şehir klasörü, 157 bulgu (145 hata, 12 uyarı)** bulundu. Bulguların çoğu eski kayıtların bbox ±0.25° olmaması, summary/atlas metrik eksikleri, boş note/country değerleri ve referans kanıtı eksikleridir. Bu turda atlas veya başka PC'lerin şehir verileri değiştirilmedi; Tahran, Pekin ve Cakarta'ya dokunulmadı. Yeni Xi'an çıktısı tamamlandığında denetim tekrar çalıştırılıp fark raporlanacak.

Robustness çıktısı güncellendi ve ağsız regresyonu `python -m pytest -q pipeline/pc7/tests/test_atlas_robustness.py` ile **4/4 PASS** oldu. Şu anki girişlerde 10 şehirden sadece Central Valley 27/27 varyant üretiyor; diğer şehirler 27 varyantın tamamını sağlayamadığı için ilk üç sıra kararı **sonuçlandırılamadı** (`n_variant_rankings=0`). `data/global/robustness.json` ve `docs/story/media/pc7_atlas_robustness.png` yenilendi; atlas.json'a dokunulmadı.

Xi'an üretim denemesinde `pipeline/subset/global_xian/` altında bir kesit oluştu ancak arka plan süreci artık çalışmıyor ve tamamlanma özeti yok; dolayısıyla şehir hazır değil. Kesiti koruyup `--resume` ile kalan çiftleri tamamlayacağım. `tools/validate_atlas.py` tekrar çalıştı: hâlâ **157 bulgu (145 hata, 12 uyarı)**; şehir özeti oluşmadığından taban çizgisi değişmedi.

## 21. FAZ 1 — Xi'an indirme ve referans denetimi

Xi'an hattı yeniden `--resume` ile başlatıldı; gözlem anında bir sonraki ham GUNW granülü indiriliyor. H5 kesitlenince aynı granülün ham dosyası downloader `finally` bloğunda silinir. `data/global/xian/summary.json` henüz oluşmadığı için **hazır değil**.

Aktarım ilerlemesi: son kontrolde 9 çiftin 8'i `pipeline/subset/global_xian/` altında kesildi; kesilen granüllerin ham `.h5` dosyaları silindi. Dokuzuncu ve son çift tekli aktarımda. Boş disk eşiği 20 GB, mevcut boş alan önceki kontrolde yaklaşık 482 GB ölçüldü.

Referans notu: Shi et al. çalışması Xingping'i “no deformation” referansı olarak tanımlar ([çalışma](https://www.tandfonline.com/doi/full/10.1080/19475705.2018.1542350)); UNGEGN yerleşim koordinatı yalnızca yaklaşık ankordur ([UNGEGN ID 2459](https://ungegn.un.org/dashboard/cities/details?id=2459)). Daha geniş Weihe Basin çalışması Xingping yakınında yaklaşık 38 mm/y subsidence rapor ettiği için ([2022 çalışma](https://www.mdpi.com/2072-4292/14/13/3182)), bu yerel piksel seçimini bağımsız GPS doğrulaması gibi yorumlamayacağım. Herhangi bir şehir sonucu bu referans belirsizliğini taşıyacak.

Diğer şehirler için ilk kaynak taraması: Aguascalientes Valley çalışması, vadinin çevresindeki kaya yüzleklerini kararlı referans alanları olarak kabul ediyor ([Cigna et al. 2015](https://www.mdpi.com/2072-4292/7/12/15868)). INEGI, batıdaki Cerro del Muerto zirvesini 21°52′49″N, 102°25′52″W olarak listeliyor; bu kaynaklı yerellik adayını NISAR kesitindeki gerçek koherensli pencereye bağlayacağım ([INEGI](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463916680.pdf)). Taiyuan için K001 (112.7°E, 37.7°N; 0.95 mm/y) düşük düşey hızla kararlı denmiş olsa da kaynak istasyonu Taiyuan havzasında konumlandırıyor; kalite standardındaki havza-dışı koşulunu sağlamaz ([Zhao et al. 2018](https://www.mdpi.com/2072-4292/10/9/1499)). Kashmar için yayımlanmış çalışma, 58°12′E boylamının batısında tarımsal çökme alanı dışında sıfıra yakın hareket bildiriyor, ancak aranabilir metinde tam bir referans koordinatı vermiyor; bu kısmi değerden nokta çıkarmayacağım ([Motagh et al.](https://academic.oup.com/gji/article/174/1/287/577293)). Querétaro için INEGI'nin 2014–2018 haritası maksimum 1.4 cm/y, 2015–2018 çökme envanteri 1.5 cm/y veriyor ([INEGI Vol. 1](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825188290.pdf), [Vol. 3](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463904441.pdf)); Aguascalientes için 2015–2020 yerel maksimumu >12 cm/y raporlanmış ([Figueroa-Miranda et al.](https://www.sciencedirect.com/science/article/pii/S0034425720306271)). Querétaro'nun güneyindeki El Cimatario Ulusal Parkı için resmi koordinat sınırları 20°28′30″–20°33′23″N, 100°19′37″–100°23′12″W olarak yayımlı; kaynak, burayı korunan volkanik alan diye tanımlıyor ([CONANP / park kaydı](https://paot.org.mx/centro/ine-semarnat/anp/AN07.pdf), [yerel jeoloji](https://www.scielo.org.mx/scielo.php?pid=S0185-092X2017000200084&script=sci_arttext)). Bu, havza dışı aday alanı sağlar; NISAR yüksek-koherensli gerçek pencere ve yerel hareket kontrolü yine gerekli.

Xi'an indirmesi sürerken tüm yerel test paketi tekrar çalıştırıldı: `python -m pytest -q` → **83 passed, 1 PendingDeprecationWarning, 27.56 s**. İndirme çalışma anında tek `.h5.part` dosyasıydı; boş disk yaklaşık 482 GB, NISAR Pulse güvenli alan eşiği 20 GB'ın üzerindeydi.

Yerel sözleşme taraması `python pipeline/pc7/validate_json.py`: **111 JSON**, 0 parse/non-standard constant hatası, 0 NaN/Infinity; yalnız `data/numbers_registry.json` `quality` alanından yoksun (başka sahibin dosyası, değiştirilmedi). 18 `points.json` quality alanını kardeş `meta.json`'dan miras alıyor.

## 22. FAZ 1 — Xi'an tamamlandı

**hazır: Xi'an** — 9 provisional NISAR GUNW zincir çifti, 2026-06-19–2026-10-17 (120 gün); hedef kutu `[108.70, 34.02, 109.20, 34.52]`, P076/F071. `pipeline/subset/global_xian/` içinde dokuz kesit var; kapsama kaydı 0 boşluk ve ham dosyaların kesim sonrası silindiğini doğruluyor. Çıktılar `data/global/xian/summary.json`, `meta.json`, `points.json`, `coverage.json` ve `disp/` altında.

Sonuç provisional ve orta güven: en negatif yaklaşık 1 km blok medyanı **−1.5 cm LOS**, `p2_cm=−1.6`, `rate_cm_per_100d=−1.25`, `valid_fraction=0.362`, `ref_range_cm=2.4`. 120 günlük doğrusal yıllıklaştırma −4.5 cm/yıl olarak kaydedilmiş, fakat yaz dönemi gözleminden yıllık hız çıkarımı kış toparlanmasını dışarıda bırakabileceği için yıllık tahmin değildir. Referans duyarlılığı büyük (2.4 cm aralık; headline mutlak değerinin yaklaşık %160'ı); sıra/karşılaştırma için sağlam sonuç sayılmamalı.

Referans ankru Xingping literatürde deformasyonsuz bölge olarak tanımlanıyor; yerel 7×7 ortak-geçerli pencere koherensi 0.7912, seçilen piksel `[108.488199, 34.302914]`. Başka bir Weihe Basin çalışması Xingping civarında hareket rapor ettiğinden bu koordinat bağımsız GNSS sabitliği kanıtı değildir. Üç referans alternatifi değerlendirilmiş olsa da iki alternatifin yerel sonuçları −2.5 ve −3.9 cm çıktı; ana sonuç referans seçimine hassas.

Kontroller: `meta.json` 10 tarih içeriyor; 12 noktanın her biriyle tarihler eşleşiyor ve `disp_cm` değerleri sonlu. `python -m pytest -q pipeline/pc7/tests/test_atlas_robustness.py` **4/4 PASS**. `tools/validate_atlas.py` **14 atlas bölgesi / 15 şehir klasörü, 172 bulgu (158 hata, 14 uyarı)** raporladı; Xi'an'a özel bulgular, PC10 sahipliğindeki `data/global/atlas.json` içinde bölge ve metrik kaydının bulunmaması. PC7 atlas dosyasını değiştirmedi. Güncellenen sağlamlık hesabında Xi'an için 27 varyant üretilemedi (0 tam varyant); bu nedenle Xi'an varyant sıralamasına dahil değil.

## 23. FAZ 1 — Taiyuan kapsamı ve referans kapısı

Taiyuan için Python 3.12 ile elevated, indirmesiz NISAR Pulse dry-run çalıştırıldı: bbox `[112.30, 37.60, 112.80, 38.10]`, 2026-06-17–2026-10-31, provisional. ASF 9 ardışık çift, 0 boşluk, P068/F020 ve 20,247.7 MB tahmini ham veri gösterdi.

Referans kapısı henüz geçilmedi. Taiyuan Basin çalışması havzayı batıda Lüliang, doğuda Taihang dağlarıyla sınırlar; K001'i kararlı istasyon seçse de GPS istasyonlarını havza çalışma alanı içinde tarif eder. Diğer kaynak J004'ü Fenyang'da konumlandırır ve onu havza CGPS ağına dahil eder. Dolayısıyla K001/J004'ü “havza dışı” referans diye kullanmak kalite standardıyla çelişir. Kaynaklar: [Tang et al., 2021, basin geology and GPS stations](https://gfzpublic.gfz-potsdam.de/pubman/item/item_5008823_4/component/file_5009699/5008823.pdf), [Tang et al., 2018, station locations and K001 stability](https://www.mdpi.com/2072-4292/10/9/1499). Bu turda indirme/şehir analizi yapılmadı ve “hazır: Taiyuan” yazılmadı. Dış havzada belgeli sabit referans bulunmadan tahmini koordinat kullanmayacağım.

## 24. Querétaro — tam provisional kesit zinciri, referans penceresi yok

P041/F078 için 2026-06-17–2026-10-15 dönemindeki dokuz provisional GUNW çifti `pipeline/subset/global_queretaro/` altına kesildi; ham granüller kesimlerden sonra kaldırıldı. Ancak El Cimatario parkının resmi koordinat sınırı/jeoloji kaydıyla verilen yerellik çevresinde 3 km içinde, dokuz çiftin tamamında geçerli ve koherensi ≥0.5 olan ortak 7×7 pencere bulunmadı. Dolayısıyla kümülatif şehir özeti üretilmedi ve `data/global/queretaro/summary.json` yok.

Kaynak alanı: [CONANP/PAOT El Cimatario kaydı](https://paot.org.mx/centro/ine-semarnat/anp/AN07.pdf) (resmi park sınırları ve volkanik alan tanımı). Park sınırının ortası ve OSM'deki Cerro El Cimatario zirvesi yakınında arama yapıldı; 5 km uzaktaki daha koherent aday, kaynakla havza dışı ve kararlı olduğu kanıtlanmadığı için kullanılmadı. Bu nedenle **hazır: Querétaro kesitleri**; analiz ve referans kalite kapısı tamamlanmadı. 9 kesit saklandı; atıf/koherens gerekçesi olmadan daha geniş arama yarıçapı kullanılmayacak.

## 25. Yerel doğrulama devamı

`python -m pytest -q pipeline/pc7/tests/test_atlas_robustness.py`: **4 passed**. Aguascalientes indirmesi sürerken tekrar alınan `python -m pipeline.pc7.validate_json`: **147 JSON**, 0 parse/non-standard constant hatası, 0 non-finite değer; kalite alanı bulguları `data/global/qc_flags.json` ve `data/global/qc_manual.json` (başka sahiplerin dosyaları). `python tools/validate_atlas.py`: **20 atlas region, 20 şehir klasörü, 188 bulgu (169 hata, 19 uyarı)**. Ortak atlas verisi eşzamanlı değiştiğinden bu, o anki salt-okunur anlık görüntüdür; `atlas.json` PC10 sahipliğinde olduğundan değiştirilmedi.

`python pipeline/pc7/atlas_robustness.py`: 14 şehir, `common_27=1`, `top3_stable=null`, `n_variant_rankings=0`; sağlam ilk üç sırası bu veriyle belirlenemiyor. `data/global/robustness.json` ve `docs/story/media/pc7_atlas_robustness.png` yenilendi. Aguascalientes katalog dry-run'ı hedef bbox `[-102.54,21.63,-102.04,22.13]` içinde P041/F077, 9 çift ve 0 boşluk gösterdi (19,905.5 MB tahmini). Dokuz kesit tamamlandı; kaynaklı Cerro del Muerto koordinatı `(-102.431111,21.880278)` ankruyla 3 km içinde tüm tarihlerde ortak geçerli 7×7 pencere bulunmadı. Ayrıntı §26.

## 26. Aguascalientes — provisional kesitler hazır, referans penceresi yok

**hazır: Aguascalientes kesit zinciri** — P041/F077, 9 ardışık provisional GUNW çifti, 2026-06-17–2026-10-15, 0 boşluk. Dokuz NPZ `pipeline/subset/global_aguascalientes/` altında; her granül kesildikten sonra ham `.h5` kaldırıldı. Fakat kaynaklı Cerro del Muerto ankru `(-102.431111,21.880278)` çevresinde 3 km içinde dokuz kesitin tamamında ortak-geçerli yüksek-koherensli 7×7 referans penceresi bulunmadı. Bu nedenle `summary.json`/şehir analizi üretilmedi ve Aguascalientes sonuç kalitesi tamamlanmış sayılmıyor.

Kaynak dayanağı önceki bölümdeki INEGI zirve koordinatı ve Cigna et al. kaya yüzlekleri açıklamasıdır. Daha uzak pikselleri havza dışında/sabit diye niteleyen bir kaynak olmadan referans arama yarıçapı artırılmadı. Önizleme/kapsam hazır, fiziksel sonuç beklemede. Ham toplam katalog tahmini 19,905.5 MB; gerçek indirilen granüller kesimden sonra tek tek silindi. `atlas.json` değiştirilmedi.
