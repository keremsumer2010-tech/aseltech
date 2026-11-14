# PC4 durum

- Görev: 1, 2, 3 (BİTTİ) + Queue `Q11`, `Q12`, `Q16` (`web3d/`) & QA (`docs/qa/PC4.md`) BİTTİ — `git push` kullanıcı kimlik doğrulaması bekliyor
- Durum: tamamlandı (lokal commitler hazır, remote push engelli)
- Güncelleme: 2026-11-14 13:30 TR
- Çıktılar:
  - Görev 1: `data/uk/optical_2026-10-20.jpg` (`700x500`, `19,490 B`), `data/uk/radar_2026-10-20.png` (`700x500`, `631,556 B`), `data/uk/meta.json` (`1,421 B`, `quality: "preview"`)
  - Görev 2: `data/karapinar/sinkholes.geojson` (`18,638 B`, `29` doğrulanmış Karapınar obruğu, tümü `bbox = [33.3, 37.6, 33.8, 37.9]` içinde; Tapur & Bozyiğit 2015)
  - Görev 3: `docs/story/sources.md` (5 zorunlu konu + GIBS/ASF URL'leri), `docs/story/calibration_note.md` (BETA `<2026-06-17` vs PROVISIONAL `P05023` vs VALIDATED `>=2026-10-21` + zorunlu NISAR dipnotu)
  - Queue `Q11` & `Q12`: `docs/story/project_page.md` (depo URL'si `https://github.com/keremsumer2010-tech/aseltech` ve 4-çift Central Valley bulguları dahil), `docs/story/submission_rules.md` (`Space_Apps_2022_Project_Submission_Guide.pdf` HTTP 200)
  - Queue `Q16`: `web3d/` (`index.html`, `style.css`, `app.js`, `generate_3d_data.py`, `surfaces.json` `252,132 B`) — Three.js `@0.160.0` ile Central Valley (`2026-06-28` → `2026-08-27`, `80×96`) ve Karapınar (`2026-09-18` → `2026-09-30`, `48×80` + 29 obruk 3D derinlik sütunu) etkileşimli 3D görünüm
  - QA & Kuyruk: `docs/qa/PC4.md`, `tasks/QUEUE.md` (`Q11`, `Q12`, `Q16` `- [x PC4]`)
- Doğrulama:
  - UK görsel çifti (`700x500` RGB, `transparency` temiz), `meta.json` şeması ve `sinkholes.geojson` (`29/29` geçerli Point Feature, `NaN` yok) doğrulandı.
  - `web3d/surfaces.json` valid UTF-8 JSON (`252,132 B`, `NaN` yok), `node --check web3d/app.js` geçti, lokal `http.server` tüm `/web3d/` ve `/data/` yollarında HTTP 200 döndü.
  - PC4 dokümanları, Three.js CDN ve depo URL'si (`https://github.com/keremsumer2010-tech/aseltech`) dahil doğrulanan **22/22** benzersiz `https://` URL canlı **HTTP 200** döndü (`www.spaceappschallenge.org/resources/participant-faq/` hariç — Linux ortamında `CERTIFICATE_VERIFY_FAILED`, `submission_rules.md`'de raporlandı).
- BLOCKED: GitHub HTTPS/SSH kimlik doğrulaması ortamda tanımlı olmadığı için `GIT_TERMINAL_PROMPT=0 git push origin main` hata veriyor (`could not read Username`). Kullanıcı terminalde GitHub kimliğiyle `git push origin main` çalıştırmalı.
- AI: Antigravity → ASF/GIBS sorgulama, piksel hizalama, makale DMS koordinat çıkarma, GeoJSON üretimi, Three.js 3D görselleştirme (`web3d/`), kaynak/kalibrasyon sentezi ve HTTP 200 doğrulama
