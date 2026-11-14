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
| GUNW arama ve indirme | ☑ | n/a | PC2: 7 provisional Central Valley alt kümesi | Cmt |
| Faz → cm dönüşümü (testli) | ☑ | n/a | `pytest analysis -q`: 17 passed (2.62s) | Cmt |
| Central Valley kümülatif harita | ☑ | ☑ | 7 provisional çift (`2026-06-28 → 2026-10-14`), maks `-7.8 cm` LOS | Cmt |
| Tıkla-grafik + sade cümle | ☑ | ☑ | 12 nokta + 10 GNSS istasyonu etkileşimli; yerel `http.server` 200 OK | Cmt |
| Karapınar haritası + obruklar | ☐ | ☐ | `Q02` çalışıyor (`data/karapinar/` bekleniyor) | Cmt |
| UK bulut ↔ radar sahnesi | ☐ | ☐ | `data/uk/` bekleniyor | Cmt |
| Aquifer Manager | ☑ | ☑ | `game/index.html` (`summary.json` 26.4 cm/yr provisional ile bağlı) | Cmt |
| GitHub Pages yayını | ☑ | n/a | `.github/workflows/pages.yml` hazır; yerel sunucu doğrulandı | Cmt |
| GNSS doğrulama | ☑ | ☑ | 10 NGL istasyonu (`CAHA` RMSE 0.75 cm `r=0.90`, `HANF` RMSE 0.83 cm `r=0.90`) | Paz |
| Altyapı risk indeksi | ☑ | ☑ | 645 segment, top 10 (Tulare Canal 57.01 mm/km, CA Aqueduct 49.12 mm/km) | Paz |
| Kalıcı / geri dönen | ☐ | ☐ | `Q08` bekleniyor (Pazar) | Paz |
| Toprak nemi grafiği | ☐ | ☐ | `Q04` bekleniyor (Pazar) | Paz |
| 30 sn video / 7 slayt | ☑ | n/a | `docs/story/pitch.md` (3 dk konuşma + 30 sn video `.srt` + 7 slayt) | Paz |

## 5. Kapsam dışı (bilinçli)

| Konu | Neden |
|---|---|
| Kendi kalibrasyonumuz | NISAR projesinin işi; biz ürünü yayınlandığı hâliyle kullanırız |
| Canlı veri çekme (site ASF'ye bağlanmaz) | 48 saatte güvenilir değil; veri önceden işlenir |
| Obruk **tahmini** | Bilimsel olarak iddialı ve doğrulanamaz; sadece kaynaklı obrukları gösteririz |
| UK'de kil çökmesini kesin ölçme | Sinyal mm-cm seviyesinde; bulunamazsa dürüstçe "below detection" yazılır |

## 6. Bu notun bakımı

Ürün tanımı değişirse önce burası güncellenir, sonra kod. Sahibi PC1.
