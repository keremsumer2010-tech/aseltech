# ÜRÜN TANIMI — NISAR Pulse: Follow the Water

## Ne
NISAR radar verisini (bulut ve geceden etkilenmeyen, santim hassasiyetli yer hareketi ölçümü) herkesin okuyabileceği bir
kaydırmalı web hikâyesine çeviren açık kaynak uygulama. Hikâye: sulama → yeraltı suyu pompalama → yer çöküyor;
üç ülke: ABD (Central Valley), Türkiye (Karapınar/Konya obrukları), İngiltere (bulutlar altında radar, Holme Fen, kil zemin).

## Challenge'a karşılığı ("Dancing with the SARs")
| Challenge istiyor | Bizde |
|---|---|
| NISAR ile yüzey değişimini izleyen etkileşimli uygulama | Zaman kaydırıcılı çökme haritası, tıkla-grafik |
| Değişim haritası / zaman animasyonu / dashboard | Kümülatif cm animasyonu, oynat butonu |
| Geniş kitleye erişilebilir, açık kaynak | Tek link, mobil uyumlu, GitHub'da açık kod |
| Karmaşık radar gözlemini eyleme dönük içgörüye çevir | Sade cümle + insan ölçeği, altyapı riski, obruk noktaları |
| Fiziksel nedeni hipotez et | Sulama/pompalama → akifer sıkışması; toprak nemi (Pazar) |
| Polarizasyon/ürün çeşitliliği | GUNW + GCOV + SME2 |
| Gelecekteki NISAR uygulamaları | "How we know" + kapanış: altyapı izleme, obruk erken uyarı |

## Özellik durumu ("kod var / siteye bağlı")
| Özellik | Sahip | Kod var | Siteye bağlı | Not |
|---|---|---|---|---|
| Açılış videosu (AI etiketli) | PC1 | ☐ | ☐ | Higgsfield |
| Sahne 1: bulut ↔ radar kaydırıcı | PC4 → PC1 | ☐ | ☐ | preview |
| Holme Fen kartı | PC4 → PC1 | ☐ | ☐ | kaynaklı sayı |
| Sahne 2: Central Valley cm haritası | PC2 → PC3 → PC1 | ☐ | ☐ | provisional |
| Tıkla → grafik + sade cümle | PC1 | ☐ | ☐ | points.json |
| Sahne 3: Karapınar obrukları | PC4/PC3 → PC1 | ☐ | ☐ | |
| Sahne 4: neden şeması | PC1 | ☐ | ☐ | |
| Aquifer Manager | PC5 → PC1 | ☐ | ☐ | hız placeholder |
| How we know + rozetler + dipnot | PC1 | ☐ | ☐ | |
| GNSS doğrulama | PC6 → Q05 | ☐ | ☐ | Pazar |
| Altyapı riski | PC6 → Q06 | ☐ | ☐ | Pazar |
| Kalıcı vs geri dönen | Q08 | ☐ | ☐ | Pazar, mixed |
| Toprak nemi | Q04 | ☐ | ☐ | |
PC1 bu tabloyu her durum kontrolünde günceller.
