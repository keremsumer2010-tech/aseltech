# PC7 durum

- Görev: Q10 — Fens GCOV ekin ritmi
- Durum: çalışıyor, Q10 başladı
- ASF araması: platform=NISAR, processingLevel=GCOV, bbox [-0.3, 52.4, 0.4, 52.9], başlangıç 2026-06-17; 49 P05023 GCOV ürünü HH/HV ile eşleşti.
- Tekrarlı seri: path 52, frame 61, 10 benzersiz tarih: 2026-06-17–2026-10-15. Granül listesi `pipeline/pc7/fens_gcov_catalog.json` içinde.
- Doğrulama: `pipeline/pc7/search_fens_gcov.py` çalıştırıldı; katalog JSON olarak tekrar açılıp parse edildi.
- Sınırlama: HDF5 rasterları ve tarla zaman serileri henüz işlenmedi.
- Kaynak: https://api.daac.asf.alaska.edu/services/search/param (ASF SearchAPI)
- AI: Codex → ASF sorgu scripti ve veri kataloğu.