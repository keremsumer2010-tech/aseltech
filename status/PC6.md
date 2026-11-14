# PC6 durum

- Görev: 14:10 paketi — `Q19` ✅ · `Q28` ✅ · `Q14` ✅ · sıradaki `Q13` (README.md) → `Q15` (code review) → `Q17` (`data/water/`)
- Durum: `Q28` (Karapınar obruk halka + OSM yakınlık riski) ve `Q14` (`data/*/meta.json` tam denetimi) tamamlandı ve doğrulandı; şimdi `Q13` (`README.md`) başlıyor.
- Çıktılar:
  - Görev 1–3, Q05, Q06, Q20: tamamlandı (`validation/`, `risk/`, `data/central_valley/{validation,assets}.json`, `docs/story/pitch.md`)
  - Q19 v2: `game/` (`model.js`, `test_model.html`, `style.css`, `index.html`, `game.js`), `docs/game_v2.png`
  - Q28: `risk/karapinar_risk.py`, `data/karapinar/assets.json` (`64` segment, `0 NaN`; `0–1 km` ort. `−4.152 cm` vs bölge arka planı `−0.647 cm` [6.4×]; `42-42` yolu obruğa `597.3 m`, `19.74 mm/km`), `docs/qa/PC6.md`
  - Q14: `docs/qa/PC6.md` (`central_valley`, `karapinar`, `uk` meta.json tam denetim + 12 JSON sıfır NaN)
- Doğrulama:
  - `python risk/karapinar_risk.py --self-test` PASS; `data/karapinar/assets.json` sıfır `NaN`/`Infinity` doğrulandı.
  - `python -c ...` (Q14 taraması): 3 bölge `meta.json` ve 17/17 PNG görseli tam doğrulandı.
- BLOCKED: yok.
- AI: Kod ve analiz üretimi; veriler NASA-ISRO NISAR (provisional), NGL ve OpenStreetMap kaynaklıdır.
