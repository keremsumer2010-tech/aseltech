# PC4 durum

- Görev: 1 (BİTTİ) → sıradaki Görev 2
- Durum: çalışıyor
- Güncelleme: 2026-11-14 13:12 TR
- Çıktılar:
  - `data/uk/optical_2026-10-20.jpg` (700x500, VIIRS SNPP TrueColor via NASA GIBS Worldview Snapshots)
  - `data/uk/radar_2026-10-20.png` (700x500, NISAR L2 GCOV `NISAR_L2_PR_GCOV_033_124_D_062_2005_DHDH_A_20261020T192237_20261020T192312_P05023_N_F_J_001_LATLON.png` fens bbox'ına kırpılıp hizalandı)
  - `data/uk/meta.json` (`quality: "preview"`)
- Doğrulama:
  - 2026-10-20 tarihli VIIRS görüntüsü %98+ bulutlu (MODIS %100 bulutlu); aynı günün NISAR GCOV browse PNG'si %100 geçerli piksel kapsıyor.
  - Kıyı çizgisi (The Wash) ve Fens drenaj hatları bulutsuz GIBS referansıyla (2026-09-26 / 2026-10-08) piksel bazında hizalı doğrulandı; her iki URL HTTP 200 döndü.
- BLOCKED:
- AI: Antigravity (Orchestrator) → ASF/GIBS sorgulama, piksel hizalama, görsel ve JSON doğrulama
