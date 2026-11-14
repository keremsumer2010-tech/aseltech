# PC9 durum

- Görev: Central Valley tam yıl analizi (Q08 · `data/central_valley_fullyear/`, `docs/story/fullyear.md`, `docs/story/media/pc9_fullyear_point.png`)
- Durum: çalışıyor
- Görev 1 (Tam yıl kümülatif — **TAMAMLANDI**):
  - Komut: `python analysis/pc9/run_fullyear.py --step cumulative` (25 kesintisiz çift: 18 `beta-precal` `2025-11-24 → 2026-06-28` + 7 `provisional` `2026-06-28 → 2026-10-14`, `plane-only` deramp sarmalayıcı).
  - Çıktılar: `data/central_valley_fullyear/{meta,points,summary}.json` (`quality: "mixed"`) + 26 adet `disp/*.png` (`1200×1000` RGBA, max `1.42 MB`).
  - Özet sayılar: `max_subsidence_cm = -20.3 cm` LOS (`-26.9 cm` dikey `estimate`, insidans `40.9°`), `rate_cm_per_yr_estimate = -22.9 cm/yr`, konum `-119.35254E, 35.88329N` (`7 km W of Earlimart`), referans aralığı `range_cm = [-20.3, -11.7] cm` (3 referans penceresi), geçerli piksel oranı `46.0%`.
- Görev 2 (Q08 Kalıcı vs geri dönen ayrıştırma — **TAMAMLANDI**):
  - Komut: `python analysis/pc9/run_fullyear.py --step decomp` (PC3 `analysis/decomp/run_decomp.py`, `--quality mixed`).
  - Çıktılar: `data/central_valley_fullyear/decomp.json` (`8.3 KB`), `decomp_permanent.png` (`1.46 MB`, `vmin/vmax = ±15 cm/yr`), `decomp_seasonal.png` (`1.59 MB`, `vmin/vmax = 0..7 cm`).
  - Sayılar (`975,173 / 2,118,174 = 46.04%` geçerli piksel):
    - Kalıcı hız (`permanent_cm_per_yr` LOS): `p2 = -12.64`, `p50 = -3.74`, `p98 = +1.89 cm/yr`.
    - Mevsimsel genlik (`seasonal_amp_cm` LOS): `p2 = 0.16`, `p50 = 1.66`, `p98 = 6.29 cm` (`low_month_mode = 8`, Ağustos).
    - Tepe nokta `p01` (`7 km W of Earlimart`): kalıcı **`-16.77 cm/yr`** LOS (`±2.24` SE), mevsimsel genlik **`5.83 cm`** (`11.67 cm` tepeden tepeye, `R² = 0.972`).
  - Doğrulama: `decomp.json` parse edildi, 12 nokta model uyumları eklendi, `decomp_permanent.png` ve `decomp_seasonal.png` görsel olarak incelendi.
- Şu an: Görev 3 (`docs/story/fullyear.md` + `docs/story/media/pc9_fullyear_point.png` + `docs/qa/PC9.md`) hazırlanıyor.
- BLOCKED: yok
- AI: Antigravity (Gemini) → PC3 `analysis/` sarmalayıcı, Q08 tam yıl ve ayrıştırma analizi
