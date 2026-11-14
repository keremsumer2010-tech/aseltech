# PC4 durum

- Görev: 3 (BİTTİ) → sıradaki `tasks/QUEUE.md` (`Q11`, `Q12`) ve QA (`docs/qa/PC4.md`)
- Durum: çalışıyor
- Güncelleme: 2026-11-14 13:18 TR
- Çıktılar:
  - Görev 1: `data/uk/optical_2026-10-20.jpg` (700x500), `data/uk/radar_2026-10-20.png` (700x500), `data/uk/meta.json` (`quality: "preview"`)
  - Görev 2: `data/karapinar/sinkholes.geojson` (29 doğrulanmış Karapınar obruğu, tümü `[33.3, 37.6, 33.8, 37.9]` içinde; Tapur & Bozyiğit 2015)
  - Görev 3: `docs/story/sources.md` (5 zorunlu konu + doğrudan GIBS/ASF URL'leri), `docs/story/calibration_note.md` (BETA `<2026-06-17` vs PROVISIONAL `P05023` vs VALIDATED `>=2026-10-21` + zorunlu NISAR kalibrasyon dipnotu)
- Doğrulama:
  - Görev 1: `2026-10-20` VIIRS %98+ bulutlu, GCOV %100 geçerli piksel ve The Wash kıyı çizgisi hizalı.
  - Görev 2: `sinkholes.geojson` 29/29 Feature geçerli GeoJSON, NaN yok, kaynak PDF HTTP 200.
  - Görev 3: `sources.md` ve `calibration_note.md` içindeki tüm kaynak URL'leri HTTP 200 döndü ve alıntılanan tüm sayılar doğrudan kaynak metinlerde doğrulandı.
- BLOCKED: GitHub HTTPS/SSH kimlik doğrulaması ortamda tanımlı olmadığı için `git push origin main` lokal commit sonrası kullanıcı aksiyonu bekliyor.
- AI: Antigravity → ASF/GIBS sorgulama, piksel hizalama, makale DMS koordinat çıkarma, kaynak/kalibrasyon sentezi ve URL doğrulama
