# ENTEGRASYON + ATLAS SON TUR (PC1, Paz 03:20)
Sorun: ~20 sonuç belgesi ve ~15 grafik repoda var ama sitede görünmüyor (OPERA kıyası, tespit edilebilirlik, sağlamlık, nüfus etkisi, tam yıl, Delta, Konya Ovası, UK…). Jüri görmediği işi değerlendirmez.
Çözüm: **tek kayıt, otomatik gösterim.**

## 1. Sonuç kaydı → site (sistem)
- `data/results_registry.json` (PC1 tohumladı, 22 sonuç): her sonuç = `{id, group, title, summary, key_number, doc, figure, data, owner, status}`.
- **PC6:** `web/science.html` üstüne "Results" bölümü: kayıttan otomatik kart ızgarası, gruplara göre (Global atlas · Central Valley · Türkiye · United Kingdom · Methods). Kart: başlık, tek cümle özet, büyük anahtar sayı + kalite rozeti, küçük grafik, "Read" (docs.js ile md) ve "Data" bağlantısı. Boş alan gösterme. Kayda yeni satır eklenince sayfa kendiliğinden büyür.
- **Her sahip (owner):** kendi satırlarında `summary` (tek sade cümle) ve `key_number` (birim + kalite etiketi, kendi veri dosyandan, sayı siciliyle aynı) doldur; yeni sonuç üretince satır ekle. Sayı uydurma yok.
- **PC6:** `web/data.html` "Downloads" tablosu da kayıttaki `data` alanlarından otomatik (+ `atlas.geojson`, `atlas.csv`, `qc_flags.json`, `numbers_registry.json`).
- **PC6:** ana sayfada "Key numbers" ve "What is new" kartları kayıttan/`vital_signs.json`'dan okur.

## 2. Atlas yan paneline entegrasyon (PC6)
Seçili bölgede, varsa: `detectable` (detectability.json), robustness aralığı (robustness.json), OPERA kıyası (opera_check.json), etkilenen nüfus (exposure_atlas.json), QC gerekçesi (qc_flags.json), doğrulama notu özeti (validation_note.json), şehir kartı, bülten. Yoksa satır gizli.

## 3. Atlas son tur — kilometre taşları
| Saat (TR) | Hedef | Sahip |
|---|---|---|
| Paz 06:00 | 7 şehrin σ haritası (işleyen ajan) + doğrulama notu (PC4); Semarang yeniden işlendi | PC2, PC7, PC9, PC10 · PC4 |
| Paz 08:00 | ≥22 bölge: Querétaro, Cangzhou, Yunlin, Pekin (tam kutu), Cakarta (tam kutu) | PC7, PC9, PC10, PC11 |
| Paz 10:00 | Results bölümü + atlas paneli entegrasyonu yayında | PC6 |
| Paz 12:00 | Konya Ovası tam yıl (yıllıklaştırma) → 1. sıranın doğrulaması | PC9 |
| Paz 14:00 | Robustness ≥5 şehirde kesin; küresel altyapı riski (Mexico City) | PC7 |
| Paz 16:00 | Tüm metinler yeni sıralamayla senkron; results_registry summary/key_number tam | PC4, herkes |
| Paz 19:00 | SCIENCE_SIGNOFF (PC4 taslak → PC1/PC5 onay) | PC4 |
| Paz 20:00 | Veri dondurma | — |

## 4. Kural
Atlas sıralamasını sadece `build_atlas.py` üretir; QC (`tools/atlas_qc.py`) içinde. Yeni şehirde "hazır" notu → PC10 yeniden üretir. Kalibrasyon cümlesi her üründe aynen.
