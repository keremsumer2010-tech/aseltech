# PC5 — M3hmeT1888 bilgisayarında Antigravity (Gemini) — Oyun + sunum metni (klasör: game/, docs/story/)  ·  BUGÜN: docs/TODAY_PLAN.md

## Görev 1 — Aquifer Manager oyunu (12:00–16:00 TR)
`game/index.html` — saf HTML/CSS/JS, tek dosya olabilir, CDN kütüphanesi kullanırsan SABİT sürüm. Metinler İngilizce.
- Oyuncu her yıl için pompalama seviyesini (%0–150) seçer; yıl tipi rastgele: wet / normal / drought.
- Basit model, katsayılar tek bir `CONFIG` nesnesinde:
  `subsidence_cm = base_rate_cm_per_yr * (pumping/100) * year_factor` ; `base_rate_cm_per_yr = 10` şimdilik "placeholder — will be replaced by our NISAR measurement" yazısıyla.
- Görsel: yan kesit — yüzey, tarlalar, kanal ve yol; altında akifer katmanı. Çökme arttıkça yüzey iner, kanal eğilir, çatlak ikonları çıkar.
- 10 yıl sonunda sonuç ekranı: toplam çökme, çiftçi geliri (basit), "what this means" cümlesi, tekrar oyna.
- Alt bilgi: "Rates are illustrative until replaced with NISAR-derived values. NISAR data are provisional; calibration is done by the NISAR project (NASA-JPL/ISRO), not by our team."
- Mobil uyumlu, konsol temiz.

## Görev 2 — Sunum metni (16:00–17:30 TR)
`docs/story/pitch.md`: 30 sn video senaryosu (sahne sahne, İngilizce altyazı) + en fazla 7 slayt başlığı ve madde metni,
`docs/TODAY_PLAN.md` sahnelerine göre. Sayı yazma; sayı yerine `{CV_MAX_CM}` gibi yer tutucu bırak (PC1 dolduracak).

## Rapor
status/PC5.md: ne bitti, nasıl test edildi, ekran görüntüsü `docs/game_v1.png`.
