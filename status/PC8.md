# PC8 durum

- Görev: 15:35 görevleri (`uk_findings`, `karapinar_p172`, `PC3/PC9 site yapılacaklar listesi`) + 16:10 EK GÖREV A/B (`submission_form.md`, `video_subtitles.srt`, `narration_script.md`) + 16:15 CHALLENGE UYUMU B3 (`exposure.py`, `data/*/exposure.json`, `docs/story/exposure.md`, `pc8_exposure.png`)
- Durum: **TAMAMLANDI** (Tüm 15:35, 16:10 ve 16:15 görevleri tamamlandı, doğrulandı ve push edildi; sürekli QA/izleme adımında)
- Çıktılar:
  - **15:35 Madde 1 (`uk_findings` + algılama grafiği):** `docs/story/uk_findings.md`, `docs/story/media/pc8_uk_detection.png` (190.0 KB), `analysis/pc8/plot_uk_detection.py`
  - **15:35 Madde 2 (`karapinar_p172` çapraz kontrolü):** `data/karapinar_p172/{meta,points,summary}.json`, `data/karapinar_p172/disp/*.png` (9 PNG), `docs/story/media/pc8_kp_p7_vs_p172.png` (264.3 KB), `analysis/pc8/karapinar_p172_check.py`, `analysis/pc8/kp_p7_vs_p172.json` (`p01` zaman serisi `r = 0.798`, `RMSE = 1.25 cm` LOS; 12 nokta `r = 0.767` LOS, `RMSE = 1.12 cm` LOS, `maks fark = 2.34 cm` LOS)
  - **15:35 Madde 3 (Site yapılacaklar tek liste özeti — PC3 / PC9 için):** `docs/qa/PC8.md` §3 (7 maddelik öncelikli açık site bulguları listesi)
  - **16:10 Görev A (Teslim formu metinleri):** `docs/story/submission_form.md` (`docs/story/submission_rules.md` alanlarına göre kopyala-yapıştır hazır İngilizce metinler, her kutunun tam karakter ve kelime sayısı, NASA Land Subsidence StoryMap 2026 çerçevesi)
  - **16:10 Görev B (Video altyazısı ve seslendirme metni):** `docs/story/video_subtitles.srt` (6 sahne, `00:00.0–00:30.0`, `docs/story/video_shotlist.md` ile birebir uyumlu) ve `docs/story/narration_script.md` (76 kelime, ~152 WPM = 29.6 sn)
  - **16:15 Challenge Uyumu B3 (Nüfus ve ürün/arazi maruziyeti):**
    - `analysis/pc8/exposure.py`, `data/central_valley/exposure.json`, `data/karapinar/exposure.json`, `docs/story/exposure.md`, `docs/story/media/pc8_exposure.png` (241.5 KB)
    - **WorldPop 100 m (`2020`, `CC BY 4.0`) nüfus maruziyeti (`estimate`):** Central Valley'de `> 2 cm` LOS çöken alanda **`71,701` kişi** (`78,464` havza enterpolasyonlu), `> 5 cm` LOS çöken alanda **`3,407` kişi** (`4,270` enterpolasyonlu); Karapınar'da `> 2 cm` LOS çöken alanda **`11,572` kişi** (`18,906` enterpolasyonlu), `> 5 cm` LOS çöken alanda **`2,214` kişi** (`3,481` enterpolasyonlu).
    - **USDA CDL 30 m (`2021`, `Public Domain`) Central Valley ilk 5 ürün (`> 2 cm` LOS `1,579.2 km²` içinde `%79.2` ekili tarım = `1,251.4 km²`):** 1. Citrus (`355.64 km²`, `> 5 cm` içinde `166.59 km²`), 2. Pistachios (`230.92 km²`), 3. Fallow/Idle Cropland (`216.14 km²`), 4. Winter Wheat (`97.27 km²`), 5. Almonds (`73.74 km²`).
    - **ESA WorldCover 10 m (`2021 v200`, `CC BY 4.0`) Karapınar ilk 5 arazi türü (`> 2 cm` LOS koherensli `28.69 km²` / enterpolasyonlu havza `141.08 km²`):** 1. Grassland (`16.54 km²` / `58.79 km²`), 2. Built-up (`7.24 km²` / `8.65 km²`), 3. Bare/sparse vegetation (`3.92 km²` / `47.46 km²`), 4. Tree cover (`0.57 km²` / `0.67 km²`), 5. Cropland (`0.42 km²` koherensli / `24.99 km²` enterpolasyonlu havza).
- Doğrulama:
  - Üretilen tüm görseller (`pc8_uk_detection.png`, `pc8_kp_p7_vs_p172.png`, `pc8_exposure.png`) görsel olarak açılıp kontrol edildi (sıfır metin çakışması, tüm dosyalar ≤ 265 KB, ham TIFF dosyaları repoya eklenmedi).
- AI: Antigravity (Gemini) → `analysis/pc8/*.py`, `data/karapinar_p172/*`, `data/*/exposure.json`, `docs/story/{uk_findings,submission_form,narration_script,exposure}.md`, `docs/story/video_subtitles.srt`, `docs/story/media/pc8_*.png`, `docs/qa/PC8.md` ve `status/PC8.md`
- BLOCKED: yok
