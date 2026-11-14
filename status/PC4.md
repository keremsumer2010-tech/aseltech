# PC4 durum

- Görev: 2 (BİTTİ) → sıradaki Görev 3 (`docs/story/sources.md`, `docs/story/calibration_note.md`)
- Durum: çalışıyor
- Güncelleme: 2026-11-14 13:16 TR
- Çıktılar:
  - Görev 1: `data/uk/optical_2026-10-20.jpg` (700x500, VIIRS SNPP TrueColor via NASA GIBS Worldview Snapshots), `data/uk/radar_2026-10-20.png` (700x500, NISAR L2 GCOV `NISAR_L2_PR_GCOV_033_124_D_062_2005_DHDH_A_20261020T192237_20261020T192312_P05023_N_F_J_001_LATLON.png`), `data/uk/meta.json` (`quality: "preview"`)
  - Görev 2: `data/karapinar/sinkholes.geojson` (29 doğrulanmış Karapınar obruğu, tümü radar bbox `[33.3, 37.6, 33.8, 37.9]` içinde; kaynak: Tapur & Bozyiğit 2015, *Marmara Coğrafya Dergisi* 31:415-446)
- Doğrulama:
  - Görev 1: `2026-10-20` VIIRS %98+ bulutlu, aynı günün NISAR GCOV browse PNG'si %100 geçerli piksel ve The Wash kıyı çizgisi hizalı; her iki URL HTTP 200.
  - Görev 2: Tapur & Bozyiğit (2015) PDF (`https://dergipark.org.tr/tr/download/article-file/3454`) HTTP 200 doğrulandı; 29/29 Point Feature geçerli UTF-8 GeoJSON, NaN yok, tüm koordinatlar `[33.3, 37.6, 33.8, 37.9]` içinde. (Not: PDF'teki `43' 99"` yazım hatalı `Küpbasan Yeni Obruk-I` dışarıda bırakıldı; bbox dışındaki `İnoba`, `Tutal`, `Sekizli Büyük`, `Meyil` ve `Çıralı` `sources.md`'de dokümante edilecek.)
- BLOCKED: GitHub HTTPS/SSH kimlik doğrulaması ortamda tanımlı olmadığı için `git push origin main` lokal commit sonrası kullanıcı aksiyonu bekliyor.
- AI: Antigravity → ASF/GIBS sorgulama, piksel hizalama, makale DMS koordinat çıkarma, GeoJSON üretimi ve doğrulama
