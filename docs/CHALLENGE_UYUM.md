# CHALLENGE UYUMU — "Dancing with the SARs" sayfasının her maddesi → bizim karşılığımız (16:15)
Kaynak: https://www.spaceappschallenge.org/2026/challenges/dancing-with-the-sars/ (Details + Resources sekmeleri, PC1 okudu). Jüri bu maddelere göre bakacak; her PC kendi satırını kapatmaktan sorumlu.

## A. Zorunlu hedef (OBJECTIVES)
| # | Challenge ne istiyor | Durum | Sorumlu |
|---|---|---|---|
| A1 | NISAR radar verisiyle bir veya daha fazla yüzey değişimini izleyen **etkileşimli uygulama** | ✅ site + simülatör | PC3, PC6 |
| A2 | **Dünyanın farklı yerlerinde** ("at locations around the world") | ✅ ABD, Türkiye, İngiltere · 🟡 Mexico City/Tahran/Cakarta, Delta, Konya Ovası | PC10, PC2 |
| A3 | Sezgisel araçlar, yenilikçi görselleştirme: **değişim haritası, zaman serisi animasyonu, dashboard** | ✅ harita, animasyon · ❌ **dashboard/explorer sayfası yok** | PC3 |
| A4 | Geniş kitleye erişilebilir, **açık kaynak, kullanıcı dostu** | ✅ MIT, sade dil (sürüyor) | PC3, PC4 |
| A5 | **Eyleme dönük içgörü**: bilim insanı, kaynak yöneticisi, eğitimci, karar verici, halk | 🟡 risk listesi var · ❌ **kitleye göre "kim nasıl kullanır" bölümü yok · ❌ eğitimci materyali yok** | PC4, PC3 |
| A6 | Yüzeyin **"desenleri ve ritimleri", farklı zaman adımlarında** | ✅ 108 gün · 🟡 tam yıl kış–yaz ritmi (Q08) | PC9, PC2 |
| A7 | **Çalışma alanı seç (memleket olabilir)** | ✅ Konya/Karapınar · ❌ **ekibin kişisel bağlamı/hikâyesi yok** | PC4 (taslak) + insanlar |
| A8 | NISAR verisini kaynaklardan indir | ✅ ASF/Earthdata | — |
| A9 | **Ek veri: optik görüntü, CBS katmanları** | ✅ VIIRS optik, OSM altyapı | — |
| A10 | Bulguları etkileşimli dijital ortamda sun (rapor, video, slayt, story map) | ✅ site, slayt · 🟡 30 sn video | PC6, PC4 |
| A11 | **Gördüğünün (veya göremediğinin) fiziksel nedenini hipotez et** | ✅ pompalama/kil · ✅ UK "below detection" açıklaması | PC8, PC5 |
| A12 | **Hangi polarizasyon değişimi gösteriyor?** | ❌ **HH/HV/oran karşılaştırması yok** | PC7 |
| A13 | **NISAR'ın gelecekteki uygulamaları** | ❌ **bölüm yok** | PC4 → PC3 |

## B. İsteğe bağlı (POTENTIAL CONSIDERATIONS) — jüri bunları "ekstra" diye puanlar
| # | Öneri | Durum | Sorumlu |
|---|---|---|---|
| B1 | Farklı polarizasyonlar ve/veya **diğer sensörlerden farklı frekanslar** | ❌ **C-band (Sentinel-1, OPERA DISP) karşılaştırması yok** | PC5 |
| B2 | Farklı tarihlerle zaman serisi | ✅ | — |
| B3 | **Ek veri: nüfus, bitki örtüsü/ürün türü** | ❌ **nüfus ve ürün türü maruziyeti yok** | PC8 |
| B4 | İnsan etkisi (tarım, sanayi) doğal kaynaklarda | ✅ tarım/yeraltı suyu | — |
| B5 | Veri görselleştirmeyle güçlü hikâye | ✅ | PC3 |
| B6 | Memleketse **kişisel bağlam ve hikâye** | ❌ (A7 ile aynı) | PC4 + insanlar |
| B7 | **Etkileşimli özet (görüntü kaydırıcı, web harita)** | ✅ | — |

## C. Resources sekmesindeki kaynaklar — siteye/kaynaklara bağlanacak
NASA Earthdata Search · ASF Vertex · **NISAR Data User Guide** (nisar-docs.asf.alaska.edu) · Intro to Remote Sensing · **Intro to SAR** · **NASA ARSET** · **NISAR StoryMaps** (land subsidence) · **NISAR Applications White Papers** · UAVSAR Postcards · (ortak ajans: RCM, RADARSAT-1, SAOCOM, CSA SAR Python tutorial).
→ PC4: sources.md + Science/FAQ'te "Learn more" listesi; özellikle NISAR StoryMaps (subsidence) ve Applications White Papers (groundwater/subsidence, infrastructure) ile bağ kur.

## D. Challenge'ın arka plan metninden: sitede açıkça söylenmesi gerekenler
- SAR aktif algılama: kendi sinyalini gönderir, **gece ve bulutta** çalışır (UK sahnesi ✅).
- Radar en çok **pürüzlülük ve dielektrik sabitine** duyarlı; su yüksek dielektrik → toprak nemi, su kütleleri (polarizasyon/GCOV bölümünde bir cümle — PC7/PC3).
- **Santim ölçeğinde hareket** (çökme) ✅.
