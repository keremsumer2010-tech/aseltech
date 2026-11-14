# PC3 QA notları

## Q21 · İki bağımsız yörünge: track 34 (yükselen) ↔ track 114 (alçalan) · 2026-11-14 14:50 TR

**Soru:** Central Valley'de gördüğümüz çökme gerçek mi, yoksa tek bir yörüngenin atmosfer/unwrapping artefaktı mı?
İki farklı yörünge yeri zıt taraflardan görür; atmosfer ve unwrapping hataları birbirinden bağımsızdır, gerçek
(çoğunlukla dikey) hareket ise ikisinde de görünmelidir.

**Veri:** track 114 descending frame 70, 8 ardışık provisional çift 2026-06-22 → 10-20 (bbox'un %94'ü), aynı hat
(`analysis/cumulative.py central_valley_p114 --data-dir analysis/out/p114_web`: iyonosfer ekranı, maskeler, düzlem +
yükseklik, aynı referans mantığı → referans −119.162, 36.457, ort. koherens 0.96; track 34 referansına 1.6 km).
Karşılaştırma: `analysis/compare_tracks.py` → `docs/cv_p34_vs_p114.png`, `analysis/out/cv_p34_vs_p114.json`.
Track 114 zamanda track 34 tarihlerine enterpole edildi, 06-28'de sıfırlandı (ortak dönem 06-28 → 10-14), ızgara eşlendi,
her ikisi dikeye çevrildi (LOS / cos geliş açısı), ~1 km bloklarda karşılaştırıldı.

| Ölçüt | Değer |
|---|---|
| Blok sayısı (1 km, ≥ %50 geçerli) | 6 719 |
| Pearson r (tüm bloklar) | **0.49** |
| r (15 km'den büyük eğilimler çıkarılınca) | **0.60** |
| RMSE | 2.6 cm |
| Medyan fark (114 − 34) | −1.3 cm |
| İşaret uyumu, \|track 34\| > 3 cm olan bloklar | **%85** (n = 1 297) |

Sınıflandırılmış ilişki (track 34'e göre gruplayıp track 114'ün medyanı):

| Track 34 dikey (cm) | n | Track 114 medyan (cm) |
|---|---|---|
| < −6 | 198 | **−5.7** |
| −6 … −4 | 500 | −4.5 |
| −4 … −2 | 1 293 | −3.6 |
| −2 … 0 | 2 223 | −2.1 |
| ≥ 0 | 2 505 | −1.0 |

**Yorum**
- Tekdüze ilişki ve %85 işaret uyumu: en çok çöken bölgeler **iki bağımsız yörüngede de çöküyor**. Bu, sonucun tek
  yörünge artefaktı olmadığını gösteren en güçlü kanıtımız (GNSS: vadi tabanı istasyonları r 0.66–0.90 ile birlikte).
- Uyum mükemmel değil: r 0.49, eğim 0.51, sabit −1.3 cm kayma. Muhtemel sebepler: (1) tek yaz sezonunda çift başına
  ±2–3 cm atmosfer artığı (track 114'ün ilk iki çiftinde sahne geneli +2.5 / −3.6 cm medyan kaymaları var), (2) farklı
  referans pencereleri, (3) yatay (doğu-batı) hareket: yükselen ve alçalan yörünge doğu-batı hareketini zıt işaretle
  görür; fark haritasındaki doğu eteği deseni bununla da açıklanabilir → Q22.
- Sunumda söylenebilecek cümle: "Two independent NISAR orbits agree on where the ground is sinking: in the areas
  where one orbit sees more than 6 cm of sinking, the other sees about 5.7 cm (median), and the sign agrees in 85 %
  of strongly moving areas."
- Track 114 tek başına en büyük değeri bbox'un güneydoğu köşesinde (13 km SE of McFarland, −10.8 cm LOS) buluyor;
  track 34 bu köşeyi tam kapsamıyor. Başlık sayısını (`summary.json`) değiştirmiyorum: ana katman track 34.

**Sınırlamalar:** LOS → dikey dönüşümü yatay hareketi sıfır varsayar; iki yörünge arasında 6 günlük uç farkları
doğrusal enterpolasyonla kapatıldı; atmosfer modeli uygulanmadı.
