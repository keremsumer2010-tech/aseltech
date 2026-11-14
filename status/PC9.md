# PC9 durum

- Görev: Central Valley tam yıl analizi (Q08 · `data/central_valley_fullyear/`, `docs/story/fullyear.md`, `docs/story/media/pc9_fullyear_point.png`)
- Durum: tamamlandı (30 dakikalık sürekli kontrol döngüsü aktif)
- Görev 1 (Tam yıl kümülatif — **TAMAMLANDI**, commit `6b4a510`):
  - Komut: `python analysis/pc9/run_fullyear.py --step cumulative` (25 kesintisiz çift: 18 `beta-precal` `2025-11-24 → 2026-06-28` + 7 `provisional` `2026-06-28 → 2026-10-14`, `plane-only` deramp sarmalayıcı).
  - Çıktılar: `data/central_valley_fullyear/{meta,points,summary}.json` (`quality: "mixed"`) + 26 adet `disp/*.png`.
  - Sayılar: `max_subsidence_cm = -20.3 cm` LOS (`-26.9 cm` dikey `estimate`, `40.9°`), `p01` (`7 km W of Earlimart`), `range_cm = [-20.3, -11.7] cm` (3 referans), geçerli piksel `%46.0`.
- Görev 2 (Q08 Kalıcı vs geri dönen ayrıştırma — **TAMAMLANDI**, commit `bec8f7c`):
  - Komut: `python analysis/pc9/run_fullyear.py --step decomp` (`975,173` geçerli piksel = `%46.04`, `status: "ok"`).
  - Çıktılar: `data/central_valley_fullyear/decomp.json`, `decomp_permanent.png` (`±15 cm/yr`), `decomp_seasonal.png` (`0..7 cm`).
  - Sayılar: havza medyan (`p50`) kalıcı `-3.74 cm/yr` (`324` günde `-3.32 cm`) vs mevsimsel genlik `1.66 cm` (`3.32 cm` tepeden tepeye, `1.00:1`); `p01` Earlimart kalıcı `-16.77 ± 2.24 cm/yr` (`-14.88 cm` / `324 g`) vs `11.67 cm` tepeden tepeye (`5.83 cm` genlik, `low_month = 8` Ağustos, `1.28:1`, `R² = 0.972`).
- Görev 3 (Metin + grafik + QA + test — **TAMAMLANDI**):
  - Komutlar: `python analysis/pc9/plot_fullyear_point.py` + `python -m pytest analysis/pc9 analysis/decomp analysis/test_insar.py analysis/test_cumulative.py -v` (`40 passed in 8.56s`).
  - Çıktılar: `docs/story/fullyear.md`, `docs/story/media/pc9_fullyear_point.png` (`465.4 KB`, `beta-precal` kesikli + `provisional` düz çizgi), `analysis/pc9/test_fullyear.py`, `docs/qa/PC9.md`.
- **16:35 ACİL Sunum & Prova Paketi (PC4 yedek — TAMAMLANDI):**
  - `docs/story/presentation_cues.md`: `https://keremsumer2010-tech.github.io/aseltech/` güncel bölümleri ve tıklama ipuçlarıyla 6 × 30 sn'lik `3:00` Lincoln konuşma metni (Kerem anlatır, Memir demo sürer, Mehmet ve İbrahim soruları alır), `data/*/summary.json` kaynaklı doğrulanmış sayılar (tam yıl için `"includes pre-calibration data"` bildirimi) ve `docs/story/judge_faq.md`'den 5 jüri sorusuna 1'er cümlelik yanıt.
  - `docs/story/rehearsal_checklist.md`: Lincoln `17:30` provası için sekme sırası (Tab 1–5), internet kesilirse yerel `docs/story/slides.html` + `docs/story/media/demo_30s.mp4` (`3.49 MB`) yedek planı, ekran paylaşımı/ses kontrolleri, süre tutma sinyalleri ve ekip görev dağılımı.
- BLOCKED: yok
- AI: Antigravity (Gemini) → PC3 `analysis/` sarmalayıcı, Q08 ayrıştırma/grafik, `docs/story/fullyear.md`, doğrulama testleri ve `16:35` sunum/prova paketi
