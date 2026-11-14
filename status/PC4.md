# PC4 durum

- Görev: 1, 2, 3 (BİTTİ) + Queue `Q11`, `Q12`, `Q16` (`web3d/`) & QA (`docs/qa/PC4.md`) BİTTİ
- Durum: tamamlandı
- Güncelleme: 2026-11-14 13:56 TR
- Çıktılar:
  - Görev 1: `data/uk/optical_2026-10-20.jpg` (`700x500`, `19,490 B`), `data/uk/radar_2026-10-20.png` (`700x500`, `631,556 B`), `data/uk/meta.json` (`1,421 B`, `quality: "preview"`)
  - Görev 2: `data/karapinar/sinkholes.geojson` (`18,638 B`, `29` doğrulanmış Karapınar obruğu, tümü `bbox = [33.3, 37.6, 33.8, 37.9]` içinde; Tapur & Bozyiğit 2015)
  - Görev 3: `docs/story/sources.md` (5 zorunlu konu + GIBS/ASF URL'leri), `docs/story/calibration_note.md` (BETA `<2026-06-17` vs PROVISIONAL `P05023` vs VALIDATED `>=2026-10-21` + zorunlu NISAR dipnotu)
  - Queue `Q11` & `Q12`: `docs/story/project_page.md` (depo URL'si `https://github.com/keremsumer2010-tech/aseltech` ve `data/central_valley/summary.json` kaynaklı 7-çift Central Valley bulguları: maks `−7.8 cm` LOS, `6 km N of Terra Bella`), `docs/story/submission_rules.md` (`Space_Apps_2022_Project_Submission_Guide.pdf` HTTP 200)
  - Queue `Q16`: `web3d/` (`index.html`, `style.css`, `app.js`, `generate_3d_data.py`, `surfaces.json` `371,298 B`) — Three.js `@0.160.0` ile Central Valley (`2026-06-28` → `2026-10-14`, `7` çift / `8` epok, `80×96`, maks `−7.8 cm` LOS `6 km N of Terra Bella`) ve Karapınar (`2026-09-18` → `2026-09-30`, `48×80` × `2` epok + 29 obruk 3D derinlik sütunu) etkileşimli 3D görünüm
  - QA & Kuyruk: `docs/qa/PC4.md`, `tasks/QUEUE.md` (`Q11`, `Q12`, `Q16` `- [x PC4]`)
- Doğrulama:
  - UK görsel çifti (`700x500` RGB, `transparency` temiz), `meta.json` şeması ve `sinkholes.geojson` (`29/29` geçerli Point Feature, `NaN` yok) doğrulandı.
  - `web3d/surfaces.json` valid UTF-8 JSON (`371,298 B`, `NaN` yok), `node --check web3d/app.js` geçti, lokal HTTP sunucu `/web3d/` ve `/data/` yollarında HTTP 200 döndü.
  - PC4 dokümanları, Three.js CDN ve depo URL'si (`https://github.com/keremsumer2010-tech/aseltech`) dahil doğrulanan **22/22** benzersiz `https://` URL canlı **HTTP 200** döndü.
- Doğrulanmadı (K-2):
  - `Küpbasan Yeni Obruk-I`: Tapur & Bozyiğit (2015) Tablo 1'deki `37° 43' 99"` saniye yazım hatası nedeniyle koordinatı doğrulanmadı; GeoJSON'a dahil edilmedi.
  - `https://www.spaceappschallenge.org/resources/participant-faq/`: Linux ortamında TLS `CERTIFICATE_VERIFY_FAILED` hatası nedeniyle doğrudan doğrulanmadı; resmi `Space_Apps_2022_Project_Submission_Guide.pdf` HTTP 200 ile doğrulandı (`submission_rules.md`).
- AI: Antigravity → ASF/GIBS sorgulama, piksel hizalama, makale DMS koordinat çıkarma, GeoJSON üretimi, Three.js 3D görselleştirme (`web3d/`), kaynak/kalibrasyon sentezi ve HTTP 200 doğrulama
