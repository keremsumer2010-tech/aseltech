# BUGÜN — Lincoln yerel sunumu (Cmt 14 Kas) için hedef

Lincoln programı tek gün: final sunum + jüri + ödül BUGÜN (saat belirtilmemiş).
**Hedef: 17:30 TR'de (14:30 UK) çalışan demo GitHub Pages'te.** 17:30'dan sonra sadece cila.

## Demo: "NISAR Pulse — Follow the Water" (tek web sayfası, kaydırmalı hikâye + oyun)

| Sahne | Mesaj | Veri | B planı |
|---|---|---|---|
| 1. Britain under clouds (UK) | "Kamera uyduları İngiltere'yi çoğu gün göremez; NISAR radarı bulutun içinden görür." Bulutlu optik ↔ NISAR radar kaydırmalı karşılaştırma (Lincolnshire/Fens, aynı gün). Holme Fen direği kartı. | NASA GIBS true color (girişsiz) + NISAR GCOV browse PNG (girişsiz) | Risk düşük |
| 2. The dancing ground (USA) | "Central Valley Haziran sonu–Eylül arası X cm çöktü." Zaman kaydırıcılı cm haritası + tıkla-grafik + sade cümle. | GUNW path 34, SADECE provisional 6 ardışık çift (2026-06-28 → 2026-09-20), zincir toplamı | GUNW browse PNG animasyonu ("preview, not calibrated" etiketli) |
| 3. Konya's sinkholes (TR) | "Karapınar'da obruklar açılıyor; NISAR yeri izliyor." Doğrulanmış obruk noktaları + NISAR katmanı. | GUNW path 7 (Karapınar, Haz–Eki), kaynaklı obruk koordinatları | GUNW/GCOV browse |
| 4. Aquifer Manager (oyun) | Pompalama ↔ çökme; 10 yıl sonrası. | Sahne 2'nin ölçtüğü hız (yoksa kaynaklı literatür değeri) | — |
| Kapanış | How we know + Pazar planı: tam yıl zinciri, kalıcı/geri dönen ayrımı, GNSS doğrulama | — | — |

## Veri kalitesi
Bugünkü demo sadece `provisional` veriyi kullanır. Browse PNG'ler `preview` rozetiyle gösterilir. Haziran öncesi (beta-precal) veri Pazar günü AYRI katman ve uyarıyla eklenir. Kalibrasyon NISAR projesinin işidir, bizim değil; sunumda ve sayfada bu açıkça yazar.

## Kim ne yapıyor (bugün)
- **PC1 (Kerem/yönetmen):** oyun, Sahne 1 verisi, obruk ve Holme Fen kaynakları, birleştirme, GitHub Pages, slayt/video.
- **PC2 (memir-erdogmus):** Earthdata + Central Valley 8 GUNW indir/kes → küçük alt kümeleri repoya.
- **PC3 (M3hmeT1888):** cm dönüşümü; Central Valley kümülatif harita + noktalar; sonra Karapınar.
- **PC4 (acikgozibrahim032-hub):** kaydırmalı hikâye web sayfası (sahte veriyle başla).

## Saatler (TR)
- 12:00 başla
- 13:30 ilk GUNW açıldı mı? (değilse B planı)
- 15:30 ilk gerçek cm haritası
- 17:30 demo canlı → sonra sunum provası
