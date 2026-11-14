# PC7 durum

- Görev: Q10 — Fens GCOV ekin ritmi
- Durum: Q10 mevcut yerel kesitlerle işlendi; site QA ve 10 stratejili Node testi tamamlandı
- ASF araması: platform=NISAR, processingLevel=GCOV, bbox [-0.3, 52.4, 0.4, 52.9], başlangıç 2026-06-17; 49 P05023 GCOV ürünü HH/HV ile eşleşti.
- Tekrarlı seri: path 52, frame 61, 10 benzersiz tarih: 2026-06-17–2026-10-15. Granül listesi `pipeline/pc7/fens_gcov_catalog.json` içinde.
- Doğrulama: `pipeline/pc7/search_fens_gcov.py` çalıştırıldı; katalog JSON olarak tekrar açılıp parse edildi.
- Q10: PC2'nin dört yerel provisional kesiti (2026-06-22, 07-04, 07-16, 08-21) işlendi; 4 adet 480 m kare örnekleme penceresinin HH/HV dB ortalaması `data/fens/crops.json` ve `data/fens/hv_timeseries.png` içinde.
- Sınırlama: Dört seyrek tarih hasat/sürüm etkisini kanıtlamıyor; pencereler doğrulanmış kadastro parselleri değil. Push öncesi son rebase'te 2026-09-02, 09-14, 09-26 ve 10-08 kesitleri geldi; mevcut Q10 çıktısına henüz dahil değiller. İndirme yapılmadı.
- QA: Göreli yollar, veri sözleşmesi, görünür İngilizce metin ve oyun modeli çevrimdışı kontrol edildi; sonuçlar `docs/qa/PC7.md` içinde.
- Kaynak: https://api.daac.asf.alaska.edu/services/search/param (ASF SearchAPI)
- AI: Codex → ASF sorgu scripti ve veri kataloğu.
- BLOCKED: yok
- BLOCKED: git push origin main → rejected (fetch first); tek pull --rebase sonrası push yeniden reddedildi. RULES §2.4 gereği burada duruldu.
