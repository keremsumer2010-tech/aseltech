# PC4 — Web uygulaması (klasör: web/)

## Görev 1 — Sahte veriyle çalışan iskelet
1. Saf HTML/JS, MapLibre GL JS veya Leaflet + Chart.js (CDN, SABİT sürüm). Giriş `web/index.html`.
2. `web/mock/` altında CLAUDE.md veri sözleşmesine uyan sahte veri: `catalog.json`, `central_valley/{meta,points,decomp,drivers,assets}.json`, 5 tarihlik `disp/*.png`.
3. Arayüz:
   - Site seçici (`catalog.json`'dan otomatik)
   - Katmanlar: Çökme (zaman kaydırıcı + oynat), Kalıcı kayıp, Mevsimsel genlik, Altyapı riski
   - Renk lejantı (cm), opaklık
   - Tıkla → Chart.js grafik (çökme + nem + sulama aynı eksende) + sade İngilizce cümle ve insan ölçeği
   - "How we know" paneli: kaynak, belirsizlik, LOS notu
4. `DATA_ROOT` tek değişken (sonra `../data/`). Mobil uyumlu.

## Kabul
Konsol temiz; `docs/web_v1.png` ekran görüntüsü; status'ta nasıl test ettiğin.
