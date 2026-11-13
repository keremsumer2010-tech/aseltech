# PC4 — Web uygulaması (klasör: web/)

## Görev 1 — Sahte veriyle çalışan iskelet
1. Saf HTML/JS (build aracı yok), MapLibre GL JS veya Leaflet (CDN, sabit sürüm). Giriş: `web/index.html`.
2. `web/mock/central_valley/` altına CLAUDE.md'deki **veri sözleşmesine** uyan sahte veri üret
   (meta.json, 5 tarihlik disp/<date>.png gradyan, 10 noktalı points.json).
3. Özellikler:
   - Uydu altlık haritası + çökme katmanı (image overlay, bbox'a oturur), opaklık ayarı
   - Zaman kaydırıcısı + oynat butonu (animasyon)
   - Renk lejantı (cm)
   - Noktaya tıkla → Chart.js ile yer değiştirme grafiği + sade İngilizce cümle
     ("This spot sank X cm in N months — about the height of ...")
   - Site seçici: central_valley / konya / fens
4. Veri yolu tek bir değişkende olsun (`DATA_ROOT`), sonra `../data/` ile değiştireceğiz.
5. Mobilde de düzgün görünsün.

## Kabul
- `web/index.html` tarayıcıda hatasız açılıyor (konsol temiz), status'ta ekran görüntüsü yolu: `docs/web_v1.png`.
