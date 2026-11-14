# PC7 durum

- Görev: Fens GCOV ritmi, polarizasyon karşılaştırması, çevrimdışı site QA ve Node oyun testi
- Durum: BLOCKED — Git index yazma izni yok
- ASF araması: platform=NISAR, processingLevel=GCOV, bbox [-0.3, 52.4, 0.4, 52.9], başlangıç 2026-06-17; 49 P05023 GCOV ürünü HH/HV ile eşleşti.
- Tekrarlı seri: path 52, frame 61, 10 benzersiz tarih: 2026-06-17–2026-10-15. Granül listesi `pipeline/pc7/fens_gcov_catalog.json` içinde.
- Doğrulama: `pipeline/pc7/search_fens_gcov.py` çalıştırıldı; katalog JSON olarak tekrar açılıp parse edildi.
- Q10: Sekiz yerel provisional kesit (2026-06-22–2026-10-08); dört 480 m pencere için HH, HV ve HV/HH dizileri `data/fens/crops.json`, `data/fens/hv_timeseries.png` içinde.
- Polarizasyon: Pencere ortalama zamansal aralığı HH 4.27 dB, HV 3.49 dB, log(HV/HH) 1.36 dB. HH'nin sayısal salınımı geniş, HV bitki yapısını fiziksel olarak daha doğrudan temsil ediyor; ekim/hasat tarihi doğrulanmadı. Açıklama/atıflar `docs/story/polarization.md`, grafik `docs/story/media/pc7_polarization.png`.
- Site QA (offline): 84 yerel yol bulundu, eksik 0; 31 JSON/GeoJSON parse hatası 0; 83 tarih dizisi sıralı, 60 points/meta eşleşmesinde uyumsuzluk 0. On `points.json` kalite alanı/quality_note bulgusu mevcut (sahip dosyaları değiştirilmedi). İngilizce metinde bir bulgu: `web/science.html` satır 23'te −4.7 değerine `cm` eklenmeli.
- Oyun: Node ile 10 strateji × 24 ay tekrar çalıştırıldı; pompalama monotonluğu, kalıcı ≤ toplam çökme ve sonlu/negatif olmayan değer kontrolleri geçti.
- Sınırlama: Sekiz tarih hasat/sürüm etkisini kanıtlamıyor; pencereler doğrulanmış kadastro parselleri değil. Yeni kesit gelirse seri yeniden hesaplanabilir. Veri indirme yapılmadı.
- QA sonuçları: `docs/qa/PC7.md`.
- Kaynak: https://api.daac.asf.alaska.edu/services/search/param (ASF SearchAPI)
- AI: Codex → yerel GCOV analizi, kaynak sentezi, offline QA scriptleri ve Node test sürücüsü.
- BLOCKED: `git status --short --branch` → `fatal: this operation must be run in a work tree`. `git pull --rebase origin main` başarılıydı; bu hata sonrası repo kuralı gereği Git işlemleri durduruldu.
