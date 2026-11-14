---
type: mimari
status: acik
date: 2026-11-14
owner: PC1
evidence: "challenge metni 'Dancing with the SARs' · NISAR Science Users' Handbook §2.4 · docs/MASTER_PLAN.md"
---

# Ürün tanımı: NISAR Pulse, Follow the Water

Bu not ürünün **ne olması gerektiğini** anlatır. Yeni katılan bir insan veya ajan, kodu hiç açmadan
"ne kurmaya çalışıyoruz" sorusunu buradan cevaplayabilmeli.

## 0. Tek cümle

**NISAR radarının santim hassasiyetindeki yer hareketi ölçümünü, sıradan bir insanın okuyabileceği
bir hikâyeye çeviren web uygulaması: tarlalar sulanıyor, yeraltı suyu çekiliyor, yer çöküyor.**

Ana mesaj (jüriye): *"We answered the NISAR Handbook's own application questions (§2.4) with real NISAR data."*

## 1. Challenge ne istiyor, biz ne veriyoruz

| Challenge | Karşılığımız |
|---|---|
| NISAR verisiyle yüzey değişimi izle | GUNW ile çökme (cm), GCOV ile radar görüntüsü, SME2 ile toprak nemi |
| İnteraktif uygulama | Kaydırmalı hikâye, zaman kaydırıcısı, tıkla-grafik, oyun |
| Geniş kitle için anlaşılır | Sade İngilizce cümle + insan ölçeği ("about the height of a phone") |
| Fiziksel sebepleri yorumla | Sulama → pompalama → akifer sıkışması → çökme |
| Hometown story | Konya / Karapınar obrukları; Lincoln etkinliği için UK sahnesi |
| Açık kaynak | Public GitHub, MIT |

## 2. Kullanıcının gördüğü akış (tek sayfa, aşağı kaydırarak)

```
0. Açılış            AI-etiketli giriş videosu + başlık
1. Britain under     Bulutlu optik görüntü ↔ NISAR radar (sürüklenebilir çizgi)
   clouds (UK)       Mesaj: kamera göremez, radar görür. Holme Fen kartı
2. The dancing       Central Valley kümülatif çökme haritası + zaman kaydırıcısı + oynat
   ground (USA)      Noktaya tıkla → grafik + "This spot sank X cm in N months"
3. Konya's           Kaynaklı obruk noktaları + NISAR katmanı
   sinkholes (TR)
4. Why it happens    Sulama → pompalama → çökme şeması; (Pazar) toprak nemi grafiği
5. Aquifer Manager   Pompalamayı ayarla, 10 yıl sonrasını gör
6. How we know       Ürünler, yöntem, kalite rozetleri, kalibrasyon dipnotu, GNSS (Pazar), kaynaklar, ekip
```

## 3. Özgün katkılarımız (resmi kodun üstüne)

1. **Kalıcı ve geri dönen çökme ayrımı** (trend + mevsimsel genlik). *Not: tam yıl gerekir; provisional veri Haziran'dan başlıyor, bu yüzden `mixed` kalite ile ayrı katman.*
2. **Sebep-sonuç füzyonu:** çökme × SME2 toprak nemi × GCOV sulama sinyali.
3. **Altyapı risk indeksi:** kanal/yol/demiryolu boyunca diferansiyel çökme eğimi.
4. **Bağımsız doğrulama:** GNSS istasyonlarıyla RMSE ve korelasyon.
5. **Tercüman katmanı:** LOS→dikey, belirsizlik etiketi, kuralla üretilen cümle (LLM sayı üretmez).
6. **Tek motor:** aynı hat her bölgede çalışır; web `data/catalog.json` okur.

## 4. Neyin gerçek, neyin hedef olduğu

"Kod var" ile "siteye bağlı" ayrı sütun: yazılmış ama hiçbir yerden çağrılmayan iş, yapılmamış sayılır.
**PC1 bu tabloyu her kontrol noktasında günceller.**

| Yetenek | Kod var | Siteye bağlı | Ölçüldü / doğrulandı | Gün |
|---|:---:|:---:|---|---|
| GUNW arama ve indirme | ☐ | n/a | | Cmt |
| Faz → cm dönüşümü (testli) | ☐ | n/a | | Cmt |
| Central Valley kümülatif harita | ☐ | ☐ | | Cmt |
| Tıkla-grafik + sade cümle | ☐ | ☐ | | Cmt |
| Karapınar haritası + obruklar | ☐ | ☐ | | Cmt |
| UK bulut ↔ radar sahnesi | ☐ | ☐ | | Cmt |
| Aquifer Manager | ☐ | ☐ | | Cmt |
| GitHub Pages yayını | ☐ | n/a | | Cmt |
| GNSS doğrulama | ☐ | ☐ | | Paz |
| Altyapı risk indeksi | ☐ | ☐ | | Paz |
| Kalıcı / geri dönen | ☐ | ☐ | | Paz |
| Toprak nemi grafiği | ☐ | ☐ | | Paz |
| 30 sn video / 7 slayt | ☐ | n/a | | Paz |

## 5. Kapsam dışı (bilinçli)

| Konu | Neden |
|---|---|
| Kendi kalibrasyonumuz | NISAR projesinin işi; biz ürünü yayınlandığı hâliyle kullanırız |
| Canlı veri çekme (site ASF'ye bağlanmaz) | 48 saatte güvenilir değil; veri önceden işlenir |
| Obruk **tahmini** | Bilimsel olarak iddialı ve doğrulanamaz; sadece kaynaklı obrukları gösteririz |
| UK'de kil çökmesini kesin ölçme | Sinyal mm-cm seviyesinde; bulunamazsa dürüstçe "below detection" yazılır |

## 6. Bu notun bakımı

Ürün tanımı değişirse önce burası güncellenir, sonra kod. Sahibi PC1.
