# PC9 durum

- Görev: Central Valley tam yıl analizi (Q08 · `data/central_valley_fullyear/`, `docs/story/fullyear.md`, `docs/story/media/pc9_fullyear_point.png`)
- Durum: çalışıyor
- Görev 1 (Tam yıl kümülatif — **TAMAMLANDI**):
  - Komut: `python analysis/pc9/run_fullyear.py --step cumulative` (PC3 `analysis/cumulative.py --mixed` + `plane-only` deramp sarmalayıcı, 25 kesintisiz çift: 18 `beta-precal` `2025-11-24 → 2026-06-28` + 7 `provisional` `2026-06-28 → 2026-10-14`).
  - Çıktılar: `data/central_valley_fullyear/{meta.json,points.json,summary.json}` (`quality: "mixed"`) + 26 adet `disp/*.png` (`1200×1000` RGBA, max `1.42 MB`).
  - Özet sayılar: `max_subsidence_cm = -20.3 cm` LOS (`-26.9 cm` dikey `estimate`, insidans `40.9°`), konum `-119.35254E, 35.88329N` (`7 km W of Earlimart`), referans aralığı `range_cm = [-20.3, -11.7] cm` (3 referans penceresi), geçerli piksel oranı `46.0%`.
  - Doğrulama: `json` dosyaları açıldı/okundu, `2026-10-14.png` görsel olarak kontrol edildi.
- Şu an: Görev 2 (Q08 `decomp.json` + 2 PNG kalıcı/geri dönen ayrıştırması) çalıştırılıyor.
- BLOCKED: yok
- AI: Antigravity (Gemini) → PC3 `analysis/` sarmalayıcı, Q08 tam yıl analizi
