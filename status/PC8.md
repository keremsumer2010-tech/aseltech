# PC8 durum

- Görev: 15:35 görevleri (`uk_findings`, `karapinar_p172`, `PC3/PC9 site yapılacaklar listesi`) + 16:10 EK GÖREV A/B (`submission_form.md`, `video_subtitles.srt`, `narration_script.md`) + 16:15 CHALLENGE UYUMU B3 (`exposure.py`, `data/*/exposure.json`, `docs/story/exposure.md`)
- Durum: 15:35 Madde 1–3 ve 16:10 Görev A–B **TAMAMLANDI**; 16:15 B3 (Nüfus ve ürün türü maruziyeti: WorldPop, USDA CDL, ESA WorldCover) üzerinde **çalışılıyor**
- Çıktılar:
  - **15:35 Madde 1 (`uk_findings` + algılama grafiği):** `docs/story/uk_findings.md`, `docs/story/media/pc8_uk_detection.png` (190.0 KB), `analysis/pc8/plot_uk_detection.py`
  - **15:35 Madde 2 (`karapinar_p172` çapraz kontrolü):** `data/karapinar_p172/{meta,points,summary}.json`, `data/karapinar_p172/disp/*.png` (9 PNG), `docs/story/media/pc8_kp_p7_vs_p172.png` (264.3 KB), `analysis/pc8/karapinar_p172_check.py`, `analysis/pc8/kp_p7_vs_p172.json` (`p01` zaman serisi `r = 0.798`, `RMSE = 1.25 cm` LOS; 12 nokta `r = 0.767` LOS, `RMSE = 1.12 cm` LOS, `maks fark = 2.34 cm` LOS)
  - **15:35 Madde 3 (Site yapılacaklar tek liste özeti — PC3 / PC9 için):** `docs/qa/PC8.md` §3
  - **16:10 Görev A (Teslim formu metinleri):** `docs/story/submission_form.md` (`docs/story/submission_rules.md` alanlarına göre proje adı, 150/500 karakter özet, detaylı açıklama, nasıl çalışır, faydalar, NASA verisi, diğer veri, araçlar, AI kullanımı, demo ve repo linki, referanslar; her alanın tam karakter/kelime sayısı yazılı, NASA Land Subsidence StoryMap 2026 çerçevesi dahil)
  - **16:10 Görev B (Video altyazısı ve seslendirme metni):** `docs/story/video_subtitles.srt` (6 sahne, `00:00.0–00:30.0`, `docs/story/video_shotlist.md` ile tam uyumlu) ve `docs/story/narration_script.md` (76 kelime, ~152 WPM = 29.6 sn, sahne bazlı kaynak doğrulama tablosu)
- AI: Antigravity (Gemini) → `analysis/pc8/*.py`, `data/karapinar_p172/*`, `docs/story/{uk_findings,submission_form,narration_script}.md`, `docs/story/video_subtitles.srt`, `docs/story/media/pc8_*.png`, `docs/qa/PC8.md` ve `status/PC8.md`
- BLOCKED: yok
