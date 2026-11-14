# ATLAS — KUSURSUZLUK LİSTESİ (PC1, Paz 01:00) · `docs/ATLAS_FINAL.md`'nin son turu
Ölçüt: jüri atlas sayfasını açar, herhangi bir şehre tıklar ve **hiçbir boş alan, kırık bağlantı, savunulamayan sayı görmez.**

## A. Her atlas şehri için 6'lı paket (eksik = kusur)
| # | Parça | Dosya | Sahip |
|---|---|---|---|
| 1 | Çökme serisi + summary (kalite standardı) | `data/global/<id>/{summary,meta,points}.json`, `disp/*.png` | şehri işleyen (PC2/7/9/10/11) |
| 2 | Belirsizlik haritası | `data/global/<id>/uncertainty/sigma_cm.png` | PC5 |
| 3 | Bilimsel karar | `data/global/<id>/validation_note.json` | PC5 |
| 4 | Şehir kartı | `docs/story/atlas_cities/<id>.md` | PC4 |
| 5 | Bülten | `docs/bulletins/<id>.html` | PC8 |
| 6 | Nüfus etkisi | `data/global/exposure_atlas.json` satırı | PC8 |
**PC8:** `tools/atlas_completeness.py` → `docs/qa/ATLAS_COMPLETENESS.md` (şehir × 6 parça tablosu, ✓/✗, sahibi). Her 30 dk yeniden çalışır; ✗ olan sahibine iş.

## B. Sayıların doğruluğu
- Tahran ve Pekin tam kutu yeniden hesap (PC11; Paz 06:00'da yoksa PC10).
- Semarang 1. sırada: PC5 bağımsız kontrol (literatür, referans, koherens).
- Robustness ≥5 şehirde kesin (PC7). Detectability tüm şehirlerde (PC5).

## C. Kapsam
Paz 14:00'te ≥20 şehir: PC2 (Delhi), PC7 (Xi'an, Taiyuan, Querétaro, Aguascalientes, Kashmar), PC9 (Eloy, Cangzhou, Gorgan, Houston, Lagos), PC10 (Hanoi, Yunlin), PC11 (Celaya, Kerman, Tianjin, Bulacan).

## D. NISAR 3D (PC1)
Yapıldı: gerçek TLE/SGP4 yörünge, sol bakışlı 33–47° swath, sonraki gerçek geçiş + geri sayım, SweepSAR taraması, şerit boyunca veri açılımı, JPL görseline göre model, Blue Marble NG + şehir ışıkları, yer izi, varsayılan açılış.
Sırada (PC1): ölçümde kullanılan gerçek geçiş tarihlerinin (meta.dates, 12 gün aralık) panelde gösterimi; InSAR ilkesini anlatan kısa açıklama kutusu; mobil düzen kontrolü.

## E. Site geneli
PC6: atlas UI son cila + mobil/projektör; PC4: metin senkronu; PC5: Paz 19:00 SCIENCE_SIGNOFF; PC8: teslim formu.
Yayın: JS/CSS önbellek kırıcı sürüm ve atlas GeoJSON/CSV artık deploy sırasında otomatik (PC1, `.github/workflows/pages.yml`).
