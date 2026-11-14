# PC6 durum

- Görev: 14:10 paketi — `Q19` Valley Under Pressure v2 TAMAM; sıradaki `Q28` Karapınar obruk/altyapı riski → `Q14` → `Q13` → `Q15` → `Q17`
- Durum: `Q19` tamamlandı (v2 sıfırdan, AI görselsiz, `game/` + `docs/game_v2.png` doğrulandı)
- Çıktılar:
  - Görev 1 (GNSS): `validation/gnss_stations.csv` (23 istasyon), `validation/gnss/*.csv` (10 istasyon, 2025-11 → 2026-11), `validation/README.md`
  - Görev 2 & 3 (OSM): `risk/central_valley_infra.geojson` (3238 hat, 1.07 MB), `risk/karapinar_infra.geojson` (64 hat, 0.04 MB), `risk/README.md`
  - Q05: `validation/compare.py`, `data/central_valley/validation.json` (`10/10` istasyon, CAHA `r=0.8957, rmse=0.752 cm`, HANF `r=0.8955`)
  - Q06: `risk/compute_risk.py`, `data/central_valley/assets.json` (`645` segment: `81` high, `131` medium, `433` low)
  - Q20: `docs/story/pitch.md`
  - Q19 v2 ("Valley Under Pressure"): `game/model.js`, `game/test_model.html`, `game/style.css`, `game/index.html`, `game/game.js`, `docs/game_v2.png`
- Doğrulama:
  - `game/test_model.html`: 5/5 test PASS (108 gün baz kalibrasyon `-10.1 cm` dikey / `-7.84 cm` LOS, `summary.json` ile %0 fark; preconsolidation hysteresis + Critical Water Year 15% cap + 0 NaN).
  - Tarayıcı testi: masaüstü `1280x850` ve mobil `390x844` (`scrollWidth === 390`, 0 yatay taşma, 0 konsol/ağ hatası, sıfır AI görseli).
- BLOCKED: yok. (NOT: `docs/story/game_model.md` henüz PC5 tarafından eklenmediğinden `CONFIG` içindeki USGS PP 1766 / DWR kaynaklı değerler ve açık `ILLUSTRATIVE` etiketli kuyu/gelir/kanal kayıp eğrileri kullanıldı.)
- AI: Kod üretimi + tarayıcı doğrulaması; ölçümler ve altyapı hatları NASA-ISRO NISAR (provisional), NGL ve OpenStreetMap kaynaklıdır.
