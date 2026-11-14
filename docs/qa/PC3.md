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

## Q22 · Dikey + doğu-batı ayrıştırması (iki geometri) · 2026-11-14 14:55 TR

İki geçiş farklı yönlere bakıyor (NISAR sola bakar): track 34 yükselen LOS birim vektörü (yerden uyduya) e = +0.64, u = 0.75;
track 114 alçalan e = −0.60, u = 0.77 (GUNW `metadata/radarGrid/losUnitVectorX/Y` küplerinden, `analysis/fetch_geometry.py`).
Her pikselde d_k = E·e_k + U·u_k çözüldü (kuzey ihmal; iki geometrili standart yaklaşım, Wright vd. 2004, GRL,
https://doi.org/10.1029/2003GL018827). Dönem 06-28 → 10-14. Kod: `analysis/vertical_ew.py` (+ birim testi).
Çıktılar: `data/central_valley/vertical.json`, `vertical_up.png`, `vertical_east.png`.

| | Değer (1 km blok medyanı) |
|---|---|
| Dikey p2 / medyan / p98 | −6.0 / −1.3 / +2.4 cm |
| En çok dikey çökme | **−9.8 cm** @ −119.049, 35.729 (Richgrove ~10 km GD, Friant-Kern hattı; benekli etek kenarı → güven orta-düşük) |
| Alpaugh/Earlimart B çanağı (en temiz geniş çanak) | **−7.2 cm dikey**, doğu-batı −0.1 cm (çanak merkezinde yatay ≈ 0, fiziksel olarak beklenen) |
| Doğu-batı p2 / medyan / p98 | −2.9 / +0.7 / +3.3 cm |
| Kapsama | %49.6 (iki yörüngede de geçerli pikseller; track 114 çerçevesi güney kenarı kesiyor) |

Yorum: LOS/cos(geliş) ile yapılan tek-yörünge dikey tahmini (summary: −10.1 cm, Terra Bella K) ile iki-geometrili
çözüm aynı mertebede. Doğu-batı bileşeni çoğu yerde ±3 cm içinde; doğu etekteki kırmızı/benekli bölgeler (bahçeler)
gürültü ağırlıklı. Sunumda güvenle söylenebilecek: "Combining two orbits, the Alpaugh bowl sank about 7 cm vertically
in 3½ months, with almost no sideways motion at its centre."

## Q09 · Londra kil bölgesi: sonuç "below detection" · 2026-11-14 15:35 TR

Veri: PC2'nin `pipeline/subset/uk_clay/` (track 101 yükselen, frame 28; 9 ardışık provisional çift 2026-06-21 → 10-19,
120 gün; iyonosfer katmanlı; koherens > 0.3 olan alan %85–92). Bölge kutusu (−0.5, 51.3, 0.2, 51.7) PC2'nin
`pipeline/search.py` tanımı (veri sözleşmesi §1'de henüz yok → PC1/PC9'a not).
Hat: `analysis/cumulative.py uk_clay` (Central Valley ile aynı adımlar) + `analysis/uk_clay_detection.py`.

| Ölçüt | Değer |
|---|---|
| Çift başı gürültü (1 km blok std) | 0.31 – 0.47 cm |
| Zincir gürültüsü σ (√Σσ²) | **1.21 cm** |
| Tespit eşiği (3σ) | **3.6 cm** |
| Ham en uç blok (düzlem + yükseklik sonrası) | −5.3 cm, sahne kenarına 2 km |
| Kuadratik yüzey de çıkarılınca en uç blok | −3.6 cm, kenara 5 km (eşiğin altında) |
| Kuadratik sonrası blok p2 / p50 / p98 | −1.5 / +0.2 / +1.3 cm; blokların **%98'i ±1.5 cm içinde** |
| Kenardan ≥ 10 km uzakta eşiği aşan blok | **0** |

Neden ham −5 cm gerçek değil: en uç değerler sahne kenarında; hepsi aynı iki çiftte (07-03→07-15 ve 10-07→10-19)
birden sıçrıyor ve o çiftlerde tüm sahnenin medyanı da −0.9 cm kayıyor → atmosfer artığı; kuadratik yüzey çıkarılınca kayboluyor.

**Sonuç:** bu tek mevsimlik provisional zincirde Londra'da gürültünün üstünde yer hareketi yok. Santimetre ve altındaki
mevsimsel kil büzülmesi bu zincirin çözebileceğinin altında. Site/sunum için cümle `data/uk_clay/detection.json`
→ `statement`. `data/uk_clay/disp/` haritaları gerçek veridir ama "below detection" etiketiyle gösterilmeli; `summary.json`'daki
`max_subsidence_cm` tek başına kullanılmamalı (`detection_status: below_detection` alanına bakılmalı).
