# PC4 durum

- Görev: 1, 2, 3 (BİTTİ) + Queue `Q11`, `Q12` & QA (`docs/qa/PC4.md`) hazır — `git push` kullanıcı kimlik doğrulaması bekliyor
- Durum: tamamlandı (lokal commitler hazır, remote push engelli)
- Güncelleme: 2026-11-14 13:22 TR
- Çıktılar:
  - Görev 1: `data/uk/optical_2026-10-20.jpg` (`700x500`, `19,490 B`), `data/uk/radar_2026-10-20.png` (`700x500`, `631,556 B`), `data/uk/meta.json` (`1,421 B`, `quality: "preview"`)
  - Görev 2: `data/karapinar/sinkholes.geojson` (`18,638 B`, `29` doğrulanmış Karapınar obruğu, tümü `bbox = [33.3, 37.6, 33.8, 37.9]` içinde; Tapur & Bozyiğit 2015)
  - Görev 3: `docs/story/sources.md` (5 zorunlu konu + GIBS/ASF URL'leri), `docs/story/calibration_note.md` (BETA `<2026-06-17` vs PROVISIONAL `P05023` vs VALIDATED `>=2026-10-21` + zorunlu NISAR dipnotu)
  - Queue & QA: `docs/story/project_page.md` (`Q11` taslağı, `data/central_valley/summary.json` beklenirken `{CV_MAX_CM}`/`{CV_RATE_CM_YR}` yer tutuculu), `docs/story/submission_rules.md` (`Q12`), `docs/qa/PC4.md`
- Doğrulama:
  - UK görsel çifti (`700x500` RGB, `transparency` temiz), `meta.json` şeması ve `sinkholes.geojson` (`29/29` geçerli Point Feature, `NaN` yok) Python scripti ile doğrulandı.
  - Tüm PC4 dosyalarındaki **19/19** benzersiz `https://` URL canlı **HTTP 200** döndü.
  - `https://www.spaceappschallenge.org/resources/participant-faq/` bu Linux ortamında `CERTIFICATE_VERIFY_FAILED` verdiği için `Q12` resmi `Space_Apps_2022_Project_Submission_Guide.pdf` (HTTP 200) üzerine kuruldu ve canlı portal son kontrolü `submission_rules.md` içine eklendi (`RULES.md` §9 E-06). (`tasks/QUEUE.md` remote push sonrası güncellenmek üzere dokunulmadı.)
- BLOCKED: GitHub HTTPS/SSH kimlik doğrulaması ortamda tanımlı olmadığı için `GIT_TERMINAL_PROMPT=0 git push origin main` hata veriyor (`could not read Username`). Kullanıcı terminalde GitHub kimliğiyle `git push origin main` çalıştırmalı.
- AI: Antigravity → ASF/GIBS sorgulama, piksel hizalama, makale DMS koordinat çıkarma, GeoJSON üretimi, kaynak/kalibrasyon sentezi ve HTTP 200 doğrulama
