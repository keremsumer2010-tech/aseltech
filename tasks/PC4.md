# PC4 — acikgozibrahim032-hub — Web (klasör: web/)  ·  BUGÜN: docs/TODAY_PLAN.md
Önce CLAUDE.md'deki "Veri kalitesi ve kalibrasyon" kuralını oku.

## Görev 1 — Kaydırmalı hikâye sayfası (12:00–16:00 TR), sahte veriyle
Saf HTML/CSS/JS, MapLibre GL JS + Chart.js (CDN, SABİT sürüm). Giriş: `web/index.html`. Metinler İngilizce.
Sahneler (dikey kaydırma, her biri tam ekran):
1. **Britain under clouds** — iki görüntü arası kaydırmalı karşılaştırma (sol: bulutlu optik, sağ: NISAR radar).
   Görseller `web/assets/uk_optical.jpg` ve `web/assets/uk_radar.png` (PC1 koyacak; o zamana kadar yer tutucu).
   Radar görüntüsünde "PREVIEW" rozeti. Holme Fen kartı (metni PC1 verecek).
2. **The dancing ground** — Central Valley haritası; `DATA_ROOT/central_valley/meta.json` + `disp/<date>.png` image overlay;
   zaman kaydırıcı + oynat; lejant (cm); `points.json` noktalarına tıkla → Chart.js grafik + cümle:
   "This spot sank X cm between <d1> and <d2> — about the height of <insan ölçeği>." (X veriden hesaplanır).
3. **Konya's sinkholes** — Karapınar haritası; `DATA_ROOT/karapinar/sinkholes.geojson` noktaları (PC1 koyacak) + varsa disp katmanı.
4. **Aquifer Manager** — `../game/index.html` için büyük buton.
5. **How we know** — kaynaklar, veri kalitesi açıklaması, radarın eğik (LOS) ölçtüğü notu, Pazar planı.

## Kalite rozetleri (ZORUNLU)
- Her katman `meta.json` içindeki `quality` alanına göre rozet gösterir: PROVISIONAL (sarı), PRE-CALIBRATION BETA (turuncu), PREVIEW (gri, "not quantitative").
- Farklı kalite sınıfları aynı katmanda birleştirilmez; grafikte farklı çizgi stili (beta = kesikli).
- Sabit dipnot: "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team. We use the products as released."

- `web/mock/` altında veri sözleşmesine uyan sahte veri üret (quality alanları dahil). `DATA_ROOT = "mock"`; sonra `"../data"`.
- Mobil uyumlu, konsol temiz. 16:00'da push; PC1 birleştirip GitHub Pages'e alacak.

## Rapor
status/PC4.md + `docs/web_v1.png` ekran görüntüsü.
