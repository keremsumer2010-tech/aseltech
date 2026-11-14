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
