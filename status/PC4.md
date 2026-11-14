# PC4 durum

- Görev: 1, 2, 3 + Queue `Q11`, `Q12`, `Q16`, `Q30` (14:10 Paketi #1) BİTTİ — 14:10 Paketi #2 (`Q31`) sürüyor
- Durum: çalışıyor (14:10 Yeni Paket #1 `Q30` tamamlandı, sıradaki #2 `Q31`)
- Güncelleme: 2026-11-14 14:13 TR
- Çıktılar:
  - Görev 1: `data/uk/optical_2026-10-20.jpg` (`700x500`, `19,490 B`), `data/uk/radar_2026-10-20.png` (`700x500`, `631,556 B`), `data/uk/meta.json` (`1,421 B`, `quality: "preview"`)
  - Görev 2: `data/karapinar/sinkholes.geojson` (`18,638 B`, `29` doğrulanmış Karapınar obruğu, tümü `bbox = [33.3, 37.6, 33.8, 37.9]` içinde; Tapur & Bozyiğit 2015)
  - Görev 3: `docs/story/sources.md` (5 zorunlu konu + GIBS/ASF URL'leri), `docs/story/calibration_note.md` (BETA `<2026-06-17` vs PROVISIONAL `P05023` vs VALIDATED `>=2026-10-21` + zorunlu NISAR dipnotu)
  - Queue `Q11`, `Q12` & `Q30`: `docs/story/project_page.md`, `docs/story/pitch.md` (`data/central_valley/summary.json` −7.8 cm LOS / −10.1 cm dikey, `data/karapinar/summary.json` −5.9 cm LOS / −8.0 cm dikey, `validation.json` 10 GNSS medyan RMSE 1.00 cm, `assets.json` 57.01 mm/km Tulare Kanalı ile birebir eşlendi), `docs/story/submission_rules.md`
  - Queue `Q16`: `web3d/` (`surfaces.json` `508,881 B` / `497.0 KB`) — Three.js `@0.160.0` ile Central Valley (`2026-06-28` → `2026-10-14`, `7` çift / `8` epok, `80×96`, maks `−7.8 cm` LOS `6 km N of Terra Bella`) ve Karapınar (`2026-06-26` → `2026-10-12`, `8` çift / `9` epok, `48×80`, maks `−5.9 cm` LOS `2 km W of Karapınar` + 29 obruk 3D sütunu) etkileşimli 3D görünüm
  - QA & Kuyruk: `docs/qa/PC4.md`, `tasks/QUEUE.md` (`Q11`, `Q12`, `Q16`, `Q30` `- [x PC4]`)
- Doğrulama:
  - UK görsel çifti (`700x500` RGB, `transparency` temiz), `meta.json` şeması ve `sinkholes.geojson` (`29/29` geçerli Point Feature, `NaN` yok) doğrulandı.
  - `web3d/surfaces.json` valid UTF-8 JSON (`508,881 B`, `NaN` yok), `node --check web3d/app.js` geçti, lokal HTTP sunucu `/web3d/` ve `/data/` yollarında HTTP 200 döndü.
  - PC4 dokümanları, Three.js CDN ve depo URL'si (`https://github.com/keremsumer2010-tech/aseltech`) dahil doğrulanan **22/22** benzersiz `https://` URL canlı **HTTP 200** döndü.
- Doğrulanmadı (K-2):
  - `Küpbasan Yeni Obruk-I`: Tapur & Bozyiğit (2015) Tablo 1'deki `37° 43' 99"` saniye yazım hatası nedeniyle koordinatı doğrulanmadı; GeoJSON'a dahil edilmedi.
  - `https://www.spaceappschallenge.org/resources/participant-faq/`: Linux ortamında TLS `CERTIFICATE_VERIFY_FAILED` hatası nedeniyle doğrudan doğrulanmadı; resmi `Space_Apps_2022_Project_Submission_Guide.pdf` HTTP 200 ile doğrulandı (`submission_rules.md`).
- AI: Antigravity → ASF/GIBS sorgulama, piksel hizalama, makale DMS koordinat çıkarma, GeoJSON üretimi, Three.js 3D görselleştirme (`web3d/`), kaynak/kalibrasyon sentezi ve HTTP 200 doğrulama
