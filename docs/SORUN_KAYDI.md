# NISAR Pulse — Sorun Kaydı (S-01 … S-30)

Kaynak: `NISAR_Pulse_Sorun_Kaydi.docx` (14 Kas 2026, 17:15 TR), Mehmet tarafından paylaşıldı. Bu dosya sadece bugfix ekibi (PC3, PC6, PC8) içindir.
Görev dağılımı: `tasks/QUEUE.md` → "BUGFIX" bölümü. S-21 (simülatör tasarımı) yapıldı, listede yok.

Öncelik: **Kritik** = jüri görürse güveni bozar · **Yüksek** = anlaşılırlığı belirgin artırır · **Orta** = cila · **Düşük** = küçük · **En son** = her şey bittikten sonra.


## S-01 · CV animasyonu (docs/story/media/cv_subsidence.mp4): "Peak P01" etiketi yanıltıcı
*Öncelik: Orta · Yer: Video · Sahip: PC3*
- Nerede: video, sağ üst kutu ("EPOCH 5/8 … Peak P01: −4.60 cm")
- Sorun: O karede en derin nokta P03 (−6.37 cm); P01 yalnızca son tarihte en derin.
- Öneri: Karedeki gerçek minimumu göster ya da "P01 (deepest at end)".
- Sahip: PC3 (videoyu üreten). Sitede yok, sadece videoda.

## S-02 · Videoda siyah alanlar açıklanmamış
*Öncelik: Yüksek · Yer: Video · Sahip: PC3, PC1*
- Nerede: video haritası; site metninde de sadece "red = sinking" yazıyor.
- Sorun: Siyah = maskelenmiş piksel (tüm çiftlerde koherens < 0.3 / güvenilmez; alanın ~%37'si, Tulare Gölü yatağı dahil). İzleyici "veri bozuk" sanabilir.
- Durum: Yöntem science.html'de teknik dille var ("coherence < 0.3 … masked"); video altyazısında ve ana sayfada sade açıklama yok. Site haritasında maskeli pikseller şeffaf (sorun yok).
- Öneri: Videoda siyah yerine açık gri + gösterge: "Grey = no reliable radar signal (fields changed between passes)". Ana sayfa video altyazısına aynı cümle.
- Sahip: PC3 (video), PC1 (altyazı metni).

## S-03 · Mavi alanlar açıklanmamış
*Öncelik: Yüksek · Yer: Harita/Video · Sahip: PC1, PC3*
- Nerede: video ve site haritası; ana sayfa metni sadece kırmızıyı anlatıyor.
- Sorun: Mavi (+1…+3 cm) çoğunlukla "referanstan daha az çöktü" ve atmosfer gürültüsü; gerçek yükselme gibi okunabilir.
- Durum: Sitede hiçbir yerde açıklanmamış ("rebound" sadece akifer şemasında geçiyor).
- Öneri: Altyazı/gösterge: "Blue = less sinking than the stable reference area; changes under about ±2 cm are within the noise."
- Sahip: PC1 (metin), PC3 (gösterge).

## S-04 · Bölge adı tutarsız
*Öncelik: Orta · Yer: Video · Sahip: PC3*
- Nerede: video başlığı "San Joaquin Valley, CA"; site, veri ve sunum "Central Valley".
- Öneri: Tek isim. "Central Valley (San Joaquin Valley), CA" ya da sadece "Central Valley".
- Sahip: PC3.

## S-05 · Videonun alt kaynak satırı okunmuyor
*Öncelik: Orta · Yer: Video · Sahip: PC3*
- Nerede: video, en alt satır ("Source: NISAR L2 GUNW …").
- Sorun: Tarayıcının video kontrol çubuğunun altında kalıyor.
- Öneri: Satırı yukarı al veya kaynağı video dışına, altyazıya yaz.
- Sahip: PC3.

## S-06 · Ana sayfadaki "−7.8 cm" aralıksız veriliyor
*Öncelik: Kritik · Yer: Ana sayfa · Sahip: PC1, PC4, PC3*
- Nerede: index.html hero kartı ("−7.8 cm Largest sinking …").
- Sorun: summary.json'a göre referans seçimine bağlı aralık −4.7 … −7.8 cm (3 referans). Science sayfası bunu söylüyor, ana sayfa söylemiyor. PC3 status'unda eski aralık (−6.2 … −7.8) duruyor; pitch/project_page hangi aralığı kullanıyor kontrol edilmeli.
- Öneri: Hero altına küçük satır: "range −4.7 to −7.8 cm depending on reference area". Tüm metinlerde aynı aralık.
- Sahip: PC1 (site), PC4 (pitch/project_page eşleme, Q30), PC3 (status güncelle).

## S-07 · Nokta okumasındaki gürültü eşiği iyimser olabilir
*Öncelik: Orta · Yer: Ana sayfa · Sahip: PC1, PC5/PC3*
- Nerede: web/app.js NOISE_CM = 1.0 (tıkla-oku cümlesi: |değer| < 1 cm ise "no clear change").
- Sorun: Kendi belgelerimiz çift başına 1-3 cm atmosfer gürültüsü, toplamda birikme ve Londra için 3σ ≈ 3.6 cm diyor. 1-3 cm arası değerler sitede "sank X cm" diye kesin değişim gibi sunuluyor.
- Öneri: Eşiği docs/story/uncertainty.md'deki kümülatif belirsizlikle eşle (ör. 2 cm) veya 1-3 cm arası için "small change, close to the noise" ifadesi.
- Sahip: PC1 (app.js), PC5/PC3 (uncertainty değeri).

## S-08 · UK sahnesi: arka plan haritası bulutsuz, hikâyeyle çelişiyor (EN ÖNEMLİ)
*Öncelik: Kritik · Yer: UK (Bölüm 2) · Sahip: PC1*
- Nerede: index.html Chapter 2 "Seeing the Fens through cloud", büyük harita.
- Sorun: Metin "kameralar sadece bulut gördü" diyor ama radar PNG'si, bulutsuz uydu mozaiği (altlık harita) üzerine konmuş. İzleyici radarın hemen yanında net bir optik görüntü görüyor; "radar bulutun altını görür" mesajı görsel olarak çürüyor.
- Doğrulama: data/uk/optical_2026-10-20.jpg gerçekten bulutlu (~%99 bulut benzeri piksel, kontrol edildi).
- Öneri: Bu bölümde büyük haritada aynı günün VIIRS bulutlu görüntüsünü bbox'a oturtup radarla sürüklenebilir çizgi ile karşılaştır (Figure 1'in büyük hali), ya da altlığı bu bölümde koyu/sade yap ve "basemap: cloud-free mosaic from other dates" notu ekle.
- Sahip: PC1 (web/app.js).

## S-09 · Radar renkleri açıklanmamış
*Öncelik: Orta · Yer: UK (Bölüm 2) · Sahip: PC4, PC1*
- Nerede: UK radar katmanı (yeşil/pembe/siyah).
- Sorun: Granül DHDH (çift polarizasyon); browse PNG renkleri polarizasyon kanallarından gelen yanlış renk. Ne anlama geldiği yazmıyor; izleyici "ne olduğu anlaşılmıyor".
- Öneri: Küçük gösterge: renklerin hangi kanaldan geldiği (ASF browse açıklamasından doğrulanarak) + sade cümle: "Bright = rough surfaces and buildings (towns), dark = smooth water and bare fields". Doğrulanamazsa sadece sade cümle.
- Sahip: PC4 (kaynak/açıklama), PC1 (gösterge).

## S-10 · Radar görüntüsü düşük çözünürlüklü önizleme; yakınlaştırınca pikselleşiyor
*Öncelik: Orta · Yer: UK (Bölüm 2) · Sahip: PC1, PC2/PC4*
- Nerede: data/uk/radar_2026-10-20.png (700×500 px, ~70×110 m/piksel), harita üstüne serilmiş.
- Sorun: Browse PNG, harita zoomuyla büyütülünce bulanık/pikselli; "yapıştırılmış PNG" gibi duruyor.
- Öneri: Bu katman için maxZoom sınırı (görüntü 1:1'i geçmesin) ya da harita yerine sabit karşılaştırma figürü. Uzun vadede: GCOV gerçek verisinden (Q10 / HV dB) daha yüksek çözünürlüklü PNG.
- Sahip: PC1 (zoom sınırı), PC2/PC4 (daha iyi görüntü, vakit varsa).

## S-11 · Katman kenarları sert, haritaya karışmıyor
*Öncelik: Orta · Yer: UK (Bölüm 2) · Sahip: PC4, PC1*
- Nerede: UK radar katmanı (RGB, saydamlık yok).
- Sorun: Kare kenarlar ve siyah veri-yok alanları opak; yer isimleri ve bağlam yok, nereye bakıldığı anlaşılmıyor.
- Öneri: Veri-yok pikselleri şeffaf (RGBA), ince çerçeve; haritaya "The Wash", "Peterborough", "King's Lynn", "Holme Fen" etiketleri/işaretleri.
- Sahip: PC4 (PNG), PC1 (etiketler).

## S-12 · Figure 1 küçük karşılaştırma görseli kontrol edilmeli
*Öncelik: Orta · Yer: UK (Bölüm 2) · Sahip: PC1*
- Nerede: sol paneldeki Figure 1.
- Sorun: Ekran görüntüsünde sadece radar görünüyor; alt köşelerdeki iki koyu etiket kutusu boş/okunmuyor. Sürüklenebilir çizgi en solda başlıyorsa optik görüntü hiç görünmüyor.
- Öneri: Çizgiyi ortada başlat, etiketler okunur olsun ("VIIRS 20 Oct · cloud" / "NISAR 20 Oct · radar").
- Sahip: PC1.

## S-13 · Central Valley haritasında büyük boşluklar açıklanmamış
*Öncelik: Kritik · Yer: CV (Bölüm 3) · Sahip: PC1, PC3*
- Nerede: index.html Chapter 3 haritası (data/central_valley/disp/*.png).
- Sorun: Sadece 7 çiftin hepsinde güvenilir olan pikseller gösteriliyor (%62.9). Boşluklarda altlık harita (tarlalar) görünüyor; izleyici "burada çökme yok" ya da "harita yarım kalmış" sanabilir. Haritada bunu anlatan gösterge yok (S-02'nin site versiyonu).
- Ölçüm: Corcoran / Tulare Gölü yatağı kutusunda (lon −119.75…−119.45, lat 35.95…36.20) geçerli piksel sadece %40. Metin "broad bowls around Tulare and Corcoran" diyor; Kaliforniya'nın en bilinen çökme çanağı haritada büyük ölçüde boş.
- Öneri: Göstergeye satır: "Gaps: no reliable radar signal (fields ploughed, irrigated or flooded between passes), not 'no sinking'". Metni "around Corcoran (partly hidden by gaps)" gibi dürüstleştir. Vakit varsa: o tarihe kadarki çiftlerde geçerli pikselleri göster (ilerleyen maske).
- Sahip: PC1 (gösterge/metin), PC3 (ilerleyen maske, opsiyonel).

## S-14 · p04 "15 km W of Corcoran" noktası boşluğun kenarında
*Öncelik: Yüksek · Yer: CV (Bölüm 3) · Sahip: PC3*
- Nerede: points.json p04, haritada beyaz nokta.
- Ölçüm: Noktanın 1 km çevresinde geçerli piksel %50 (eşik tam sınırda); haritada nokta boşluğun içinde duruyor gibi görünüyor, ama değeri −7.0 cm.
- Öneri: p04'ü yakındaki %90+ geçerli bir bloğa taşı ya da tıklayınca "estimated from surrounding pixels" notu ekle.
- Sahip: PC3.

## S-15 · Başlık değeri (−7.8 cm, p01 Terra Bella) haritanın kenarında
*Öncelik: Yüksek · Yer: CV (Bölüm 3) · Sahip: PC3, PC1/PC4*
- Nerede: summary.json max_subsidence_location (−119.022, 36.011).
- Ölçüm: bbox doğu kenarına ~2 km. Sierra eteğindeki meyve bahçesi kuşağında; PC3 kendi raporunda bu kuşak için "düşük güven" diyor. Çanak kenarda kesiliyor olabilir.
- Not: p02 "21 km S of Lemoore" −7.78 cm, 1 km çevresi %100 geçerli, vadi tabanında; başlığı aynı büyüklükte destekleyen daha sağlam nokta.
- Öneri: Başlıkta iki yeri birlikte an ("near Terra Bella and south of Lemoore") ya da p02'yi birincil göster; vakit varsa bbox'ı doğuya ~0.1° genişlet.
- Sahip: PC3 (değerlendirme), PC1/PC4 (metin).

## S-16 · Zaman kaydırıcısı ile grafik/okuma eşleşmiyor (küçük)
*Öncelik: Düşük · Yer: CV (Bölüm 3) · Sahip: PC1*
- Nerede: Chapter 3, kaydırıcı 22 Jul'deyken okuma ve grafik tüm dönemi (28 Jun–14 Oct) gösteriyor.
- Öneri: Grafikte seçili tarihi dikey çizgiyle işaretle.
- Sahip: PC1.

## S-17 · Çökme haritası: daha saydam + yumuşatılmış gösterim (KARAR: yapılacak)
*Öncelik: Yüksek · Yer: CV + Karapınar · Sahip: PC3, PC1*
- Nerede: Chapter 3 (Central Valley) ve Karapınar haritaları; şu an piksel bazlı PNG, %80-85 opak.
- Takım kararı: saydamlık artırılacak VE yumuşatılacak; görüntü "kare kare" olmamalı.
- Yöntem: blok/kare yerine kayan pencere (~560 m = 7×7 piksel) NaN-duyarlı ortalama, pencerenin ≥%50'si geçerliyse; ardından hafif Gauss yumuşatma. Kenarlar yuvarlak, kare görünmüyor (önizleme: cv_smoothing_preview.png).
- Ölçüm (önizleme, son tarih): dolu alan ham %63 → 560 m %65 → 1 km %66. Yani yumuşatma küçük delikleri kapatıyor ve gürültüyü azaltıyor, büyük boşlukları (Tulare Gölü yatağı vb.) kapatmıyor. Bu yüzden S-13 göstergesi yine şart.
- Görünüm: raster-opacity ~0.6-0.65; "Detailed / Smoothed" düğmesi, varsayılan Smoothed.
- Not: Önizleme ortalama kullanıyor; üretimde PC3 noktalarla tutarlılık için medyan da seçebilir.
- UK için geçerli değil (bkz. S-08).
- Sahip: PC3 (PNG üretimi, mevcut _cum_stack.npz'den, yeni veri gerekmez, ~20-30 dk), PC1 (saydamlık + düğme).

## S-18 · Açılış (hero) ekranında çökme katmanı görünmesin
*Öncelik: Kritik · Yer: Açılış · Sahip: PC1*
- Nerede: web/app.js hero() fonksiyonu (addSource/addLayer 'h' + updateImage döngüsü) ve index.html .hero-caption paragrafı ("Live background: …").
- Sorun: Katman başlığın arkasına kayıyor (harita sürekli dönüyor: bearing her 60 ms'de +0.04°), yarısı metnin altında kalıyor; kenarları sert, boşluklu ham görüntü ilk izlenimi bozuyor. Takım kararı: açılışta gösterilmeyecek.
- Yapılacak: hero()'da 'h' kaynağını, katmanını ve görüntü döngüsünü kaldır (sadece uydu altlığı kalsın); index.html'deki "Live background" altyazısını sil veya "Background: Central Valley, California" yap.
- Sahip: PC1.

## S-19 · GPS doğrulama bölümü: sabit istasyonlarda sistematik sapma metinde yok
*Öncelik: Kritik · Yer: GPS (Bölüm 4) · Sahip: PC1, PC3/PC6*
- Nerede: index.html Chapter 4 "Checking our work"; data/central_valley/validation.json.
- Doğru olan: Çöken 5 istasyonda (CAHA, HANF, QCAP, TLBN, P056) r = 0,66–0,90, RMSE 0,75–1,17 cm → "about a centimetre" iddiası tutuyor.
- Sorun 1: Sabit istasyonlarda (CAD1, P564, P565, P566) GPS dönem sonu −0,7…+0,2 cm, NISAR +1,2…+1,9 cm. Rastgele değil, sistematik pozitif sapma (~+1,5 cm); metin bunu "sinyal gürültüden küçük" diye açıklıyor. Muhtemel kaynak: referans / atmosfer-düzlem düzeltmesi kalıntısı; haritadaki mavi alanlarla (S-03) aynı etki olabilir.
- Öneri: Metne bir cümle: "At stable stations NISAR reads about 1–2 cm higher than GPS, a known bias from the reference area and residual atmosphere." PC3 sapmanın kaynağını kontrol etsin (referans penceresi, deramp).
- Sorun 2: P566 yeşil görünüyor (r = 0,42, eşik 0,4) ama sabit istasyon; yeşil = "uyumlu" yanıltıcı. Eşik 0,6 önerilir.
- Sorun 3: Tablo başlığı "Diff." belirsiz → "RMSE (cm)" veya "Avg. difference (cm)".
- Sahip: PC1 (metin, eşik, başlık), PC3/PC6 (sapma analizi).

## S-20 · Karapınar bölümü: sonuç zayıf ama sitede kesin gibi sunuluyor
*Öncelik: Kritik · Yer: Karapınar (Bölüm 6) · Sahip: PC3, PC6, PC1*
- Nerede: index.html Chapter 6 (Karapınar), data/karapinar/*, assets.json (obruk halka analizi).
**Ölçüm/olgu:**
- Haritanın sadece %14'ü ölçülebiliyor (tarlalar 12 günde koherens kaybediyor). Obrukların çoğu (29'un 19'u) veri olmayan ovada; harita verisi çoğunlukla doğudaki volkanik yayla ve ilçe çevresinde.
- Yaylada (hareket etmemesi beklenen yer) ±3–4 cm'lik mavi/kırmızı geniş lekeler var; tüm sahnede p2/p98 = −4,2 / +2,5 cm. Yani gürültü düzeyi ~3–4 cm; başlık değeri −5,9 cm bu zarfın sadece ~1,5 cm dışında.
- Tek referans; ≥30 km'de alternatif referans yok → referans duyarlılık testi yapılamadı (summary.json range = null). PC3 kendi raporunda güveni "DÜŞÜK-ORTA" diyor.
- Yıllık hız tahmini −20 cm/yıl; literatürde Konya havzası zirve ~9 cm/yıl (Sentinel-1). Yaz sezonu uzatması olduğu için abartılı.
- "Obruğa 1 km içinde 4,2 cm, 5 km ötesinde 0,6 cm" karşılaştırması konumla karışık (confounded): yakın halkalar ova/ilçe çevresi, uzak halka büyük ölçüde yayla (farklı yükseklik, arazi örtüsü, atmosfer). Metin "örüntü, nedensellik değil" diyor (iyi) ama bu karışıklığı söylemiyor.
**Öneri:**
- Metne güven etiketi: "Low confidence: NISAR could measure only 14 % of this area; noise here is about ±3–4 cm."
- −5,9 cm'yi "up to about 6 cm, close to the noise level" diye yumuşat; yıllık hızı sitede gösterme.
- Çubuk grafiğe her halkadaki piksel sayısı ve hata çubuğu (std) ekle; ">5 km" halkasının yayla olduğunu not et. Mümkünse karşılaştırmayı sadece ova piksellerine sınırla.
- Haritada veri-yok ovayı açıkla (S-13 ile aynı gösterge).
- Sahip: PC3 (güven/istatistik), PC6 (halka analizi, Q28), PC1 (metin).

## S-21 · Simülatör (game/index.html, "Valley Under Pressure") çok karmaşık ve site tasarımına uymuyor
*Öncelik: Yüksek · Yer: Simülatör · Sahip: PC6, PC1*
- Ne yapıyor: Oyuncu 24 ay boyunca her ay yeraltı suyu pompalama, kanal suyu ve tarla nadasa bırakma oranını ayarlıyor; model 7 bölge için çökmeyi (geri dönen + kalıcı kil çökmesi), yeraltı suyu seviyesini, kanal kapasite kaybını, kuruyan kuyuları ve çiftlik gelirini hesaplıyor; NISAR 2026 ölçümüyle (summary.json) karşılaştırıyor.
- Sorun 1 (karmaşıklık): 26 düğme, 3 kaydırıcı, 7 bölge, 3 harita modu (Live / Blend / NISAR raster), Classroom Mode, ses, model testleri, olay günlüğü, 6 gösterge kutusu. Jüri/izleyici 30 saniyede ne yapacağını anlamıyor; açılış metni bile 5 satır.
- Sorun 2 (tasarım): Site açık tema (beyaz zemin, lacivert #0b3d91 vurgu, kırmızı #c8321f, Inter yazı tipi, web/style.css değişkenleri); simülatör koyu lacivert + camgöbeği + monospace rozetler, ayrı bir uygulama gibi duruyor. Üst menü (Story / Simulator / Science / Data / FAQ) yok, sadece "← Story Map".
- Sorun 3 (dil/doğruluk): "Baseline water levels calibrated against NISAR" ifadesi kalibrasyon kuralıyla (RULES §4) çelişiyor → "tuned to match". "Water level −48.0 m, Low −48.3 m", kuyu derinlikleri, gelir eğrileri temsili; görünür "illustrative" etiketi yalnızca küçük dipnotta.
**Öneri (sadeleştirme):**
- Varsayılan ekran: tek havza (Tulare), tek bölge, tek ana kaydırıcı (pumping) + "Advance 1 year" (24 ay yerine 10 yıl, yıllık adım), 3 sonuç: toplam çökme, kalıcı kısım, kanal hasarı + yan kesit animasyonu.
- Kanal suyu, nadas, 7 bölge, Konya, Classroom Mode, ses, model testleri, harita modları → "Advanced" açılır bölümüne.
- Açılış: tek cümle ("Pump more, earn more today — but sink the ground forever. Can you keep the farms going for 10 years?") + "Start".
- Tasarım: web/style.css'i doğrudan kullan (aynı renk değişkenleri, Inter, beyaz kartlar), sitenin üst menüsünü ekle.
- "calibrated" → "tuned to match NISAR 2026"; model sayılarının yanına "illustrative".
- Sahip: PC6 (game/, Q29), PC1 (style.css/menü uyumu onayı).
- Simülatör yeniden tasarım şartnamesi (takım kararı: herkesin anlayacağı şekilde baştan tasarlanacak)
- Hedef kitle: Hiç bilgisi olmayan biri (jüri, öğrenci, çiftçi). 10 saniyede ne yapacağını, 1 dakikada dersi anlamalı. Teknik terim yok (h_pc, elastic, LOS, interbed yok).
- Tek cümlelik ders: "Pumping groundwater earns money today, but too much makes the ground sink, and some of that sinking never comes back."
**Akış (3 ekran):**
- Başlangıç: Başlık + tek cümle + büyük "Start" düğmesi. Altında küçük: "Based on real NISAR measurements: up to 7.8 cm of sinking in 108 days (2026)".
**Oyun (10 yıl, her tıklama 1 yıl):**
- Tek kontrol: büyük pompalama kaydırıcısı, 3 durak ve ikonlar: "Save water / Normal / Pump hard". Yanında o seçimin anlamı tek satır ("Farms earn more, aquifer drops faster").
- Büyük görsel: yan kesit çizimi — yüzeyde çiftlik, kanal, kuyu; altında su seviyesi ve kil katmanı. Pompaladıkça su iner, kil sıkışır, yüzey ve kanal eğilir, kuyu kurur. Renk: site paleti.
- Sadece 3 gösterge, ikon + sade dil: 💰 Farm income · ⬇️ Ground sunk (cm) · 🔒 Lost forever (cm). Kanal/kuyu hasarı görselde gösterilsin, kutuda değil.
- Büyük düğme: "Next year →". Her yıl başında rastgele yıl tipi tek kelimeyle: "Wet year" / "Dry year" (yağmur ikonu).
- Kritik anlarda tek cümlelik uyarı balonu: "Water fell below its lowest level ever — this sinking is now permanent."
- Sonuç: 10 yıl özeti: toplam gelir, toplam çökme, kalıcı kısım; tek cümle değerlendirme ("Your farms earned well, but 18 cm of ground is gone for good.") + gerçek dünya bağlantısı: "In 2026, NISAR measured up to 7.8 cm in one summer in this valley." + "Try again" + "Back to the story".
**Kurallar:**
- Görünür "illustrative model" etiketi; tek gerçek sayı NISAR değeri, summary.json'dan okunur (elle yazılmaz).
- "calibrated" kelimesi yok → "starting point taken from NISAR 2026".
- Tasarım: web/style.css değişkenleri (beyaz kart, lacivert #0b3d91, kırmızı #c8321f, Inter), sitenin üst menüsü; koyu tema yok.
- Mobilde tek sütun, büyük dokunma alanları; klavye: Space = next year.
- Gelişmiş özellikler (7 bölge, Konya, kanal suyu, nadas, sınıf modu, model testleri) tek "Advanced / For teachers" bağlantısının arkasında; varsayılanda görünmez.
- Bitti sayılır eğer: Projeyi bilmeyen biri (ör. aileden biri) yardım almadan 1 dakikada 10 yılı bitirip dersi kendi cümlesiyle söyleyebiliyor; telefonda çalışıyor; konsol temiz; site ile aynı görünüyor.
- Sahip: PC6 (game/), tasarım onayı PC1. Tahmini süre: 1,5–2 saat (mevcut model hesapları yeniden kullanılır).

## S-22 · Site yavaş açılıyor: optimizasyon yok (harita + görseller)
*Öncelik: Kritik · Yer: Tüm site · Sahip: PC1, PC3*
**Ölçümler (main @ 276ef75):**
- Açılış haritası sürekli dönüyor: app.js hero() her 60 ms'de setBearing → harita sürekli yeniden çiziliyor ve uydu (Esri World Imagery) karoları sürekli yükleniyor. Aynı anda 1,4 sn'de bir çökme karesi değiştiriyor → açılışta 8 karenin hepsi (12,6 MB) iniyor. Yavaşlığın büyük ihtimalle ana sebebi.
- Sayfada 2 MapLibre haritası sayfa açılır açılmaz başlatılıyor (hero + ana harita), ikisi de uydu karosu çekiyor.
- Çökme kareleri ağır: data/central_valley/disp/*.png 1200×1000, karesi ~1,4 MB, toplam 12,6 MB. Test: WebP (q80, saydamlık korunur) → 2,2 MB (−%83); 128 renkli PNG → 2,7 MB.
- Önbellek kapalı: tüm veri istekleri fetch(..., {cache: 'no-cache'}) → her ziyarette yeniden doğrulama.
- Medya: docs/story/media 23 MB (mp4'ler 0,9–4,4 MB; cv_subsidence.gif 4,4 MB ve kp_subsidence.gif 1,4 MB — mp4 karşılıkları varken GIF gereksiz); 20 küçük PNG (~100–465 KB).
- Açılışta 13 JSON paralel çekiliyor (toplam ~260 KB; sorun değil).
**Öneri (etki sırasıyla):**
- Hero'yu hafiflet: çökme katmanını kaldır (S-18) ve sürekli dönmeyi kapat; en iyisi hero'da canlı harita yerine tek bir sabit görsel (WebP, ~150 KB).
- Ana haritayı tembel başlat: IntersectionObserver ile bölüme yaklaşınca new maplibregl.Map. fadeDuration: 0, renderWorldCopies: false.
- Kareleri sadece gerektiğinde yükle: önce ilk kare, oynat'a basılınca/kaydırıcı ilerledikçe sıradaki 1–2 kare.
- Görselleri otomatik optimize et (kalıcı çözüm): Pages yayın akışına (.github/workflows/pages.yml, "Assemble site" sonrasına) optimizasyon adımı ekle → repo'daki orijinallere dokunmadan sadece yayınlanan kopyada PNG→WebP (veya pngquant + oxipng), JPG sıkıştırma, yeniden boyutlandırma. Alternatif: GitHub Action calibreapp/image-actions (her push/PR'da görselleri otomatik sıkıştırır). Sitedeki .png yolları .webp olacaksa app.js'te uzantı tek değişkenden okunmalı.
- cache: 'no-cache' kaldır (Pages zaten doğru önbellek başlıkları gönderiyor).
- Videolar: preload="none" + poster görseli; 720p, H.264 CRF ~28 ile yeniden kodla; siteden GIF'leri kaldır.
- Hedef: ilk açılışta indirilen toplam < 3 MB; Lighthouse Performance ≥ 80 (mobil).
- Sahip: PC1 (web/app.js, workflow), PC3 (disp karelerini WebP/küçük üretme seçeneği).

## S-23 · TR / EN dil desteği (EN SON yapılacak — takım kararı)
*Öncelik: En son · Yer: Tüm site · Sahip: PC1 + çevirmen*
- Ne zaman: tüm içerik ve düzeltmeler bittikten sonra (metin değişirse çeviri boşa gider).
**Yöntem:**
- Her metin öğesine data-i18n="anahtar"; metinler web/i18n/en.json ve web/i18n/tr.json dosyalarında.
- Üst menüye "EN | TR" düğmesi; varsayılan tarayıcı dili (navigator.language), seçim localStorage'da (try/catch ile).
- app.js'te üretilen cümleler (tıkla-oku, GPS özeti vb.) şablon + sözlükten; sayılar Intl.NumberFormat (TR'de virgül: 7,8).
- Kapsam: index, science, data, faq, panel sayfaları + simülatör (game/) + harita göstergeleri + rozetler.
- Kurallar: Jüriye giden teslim ve varsayılan dil İngilizce kalır (RULES K-14). Bilimsel terimler (LOS, NISAR, GUNW) çevrilmez. Çeviri bir insan tarafından (Türkçesi iyi olan biri) gözden geçirilir; makine çevirisi doğrudan yayınlanmaz.
- Not: Ekran görüntülerinde görülen Türkçe, tarayıcının otomatik çevirisiydi; jüriye gösterirken kapatılmalı.
- Sahip: PC1 (altyapı), bir Antigravity ajanı (çeviri), insan kontrol.

## S-24 · Yörünge yönü: key_findings.md'de "neighboring ascending Track 114" yanlış
*Öncelik: Kritik · Yer: Science · Sahip: key_findings sahibi*
- Kaynak: dış inceleme PDF'i (madde 2.1) + repo doğrulaması.
- Doğrulama: data/central_valley/vertical.json yöntemi "track 34 ascending + track 114 descending"; LOS doğu bileşenleri zıt işaretli (+0,64 / −0,60). judge_faq.md de "Track 114 descending" diyor. Yani iki geçiş gerçekten zıt yönden bakıyor; ana sayfadaki "from the other direction" ve science.html'deki "opposite sides" DOĞRU.
- Hata: docs/story/key_findings.md satır 15 (science.html'de gösteriliyor) Track 114'ü "neighboring ascending" diye yazıyor → "descending" olmalı. (PDF düzeltmeyi ters yönde öneriyor; onu uygulamayın.)
- Sahip: key_findings.md'nin sahibi (PC1 onayıyla).

## S-25 · Çift aralığı: science.html "12 to 36 days", ana sayfa "12 to 24 days"
*Öncelik: Yüksek · Yer: Science · Sahip: PC1*
- Doğrulama: Track 34 tarihleri arası günler = 12, 12, 24, 12, 12, 12, 24 (toplam 108). En uzun aralık 24 gün; ana sayfa doğru, science.html yanlış. (PDF "en az bir çift 36 gün olmalı" diyor; bu hesap yanlış: 5×12 + 2×24 = 108.)
- Not: Cümle track 114'ü de kapsıyorsa onun aralıklarını kontrol edin; değilse "12 to 24 days" yapın.
- Sahip: PC1 (science.html).

## S-26 · Karapınar obruk farkında aritmetik hata
*Öncelik: Yüksek · Yer: Science (Karapınar) · Sahip: PC6*
- Doğrulama: −4,152 − (−0,647) = −3,505 cm; −4,030 − (−0,647) = −3,383 cm. key_findings.md "3.45 cm ve 3.33 cm" yazıyor → 3.51 cm ve 3.38 cm olmalı (PDF doğru).
- Sahip: PC6 (Q28 analizi) / key_findings.md sahibi.

## S-27 · Altyapı "High risk" tanımı iki yerde farklı
*Öncelik: Yüksek · Yer: Science (Risk) · Sahip: PC6, PC1*
- Doğrulama: key_findings.md: "gradient ≥ 10 mm/km with subsidence ≤ −2 cm, or ≤ −10 cm total"; science.html Bölüm 5: "gradient ≥ 10 mm/km or sinking ≥ 10 cm" (−2 cm koşulu yok, işaret de farklı yazılmış).
- Öneri: assets.json'u üreten koddaki (risk/compute_risk.py) gerçek kuralı esas alıp iki metni ona eşitle.
- Sahip: PC6 (kural), PC1 (science.html).

## S-28 · GPS doğruluk aralığı eksi işaretli yazılmış
*Öncelik: Yüksek · Yer: Science (GPS) · Sahip: key_findings sahibi*
- Doğrulama: key_findings.md satır 13: "confirm -0.75 to -1.17 cm accuracy". RMSE negatif olamaz → "0.75 to 1.17 cm (RMSE)".
- Sahip: key_findings.md sahibi.

## S-29 · Referans aralığı science.html içinde iki farklı değer
*Öncelik: Yüksek · Yer: Science · Sahip: PC1*
- PDF'e göre science.html özetinde −4,7…−7,8, Bulgu #1'de −6,2…−7,8 cm geçiyor. summary.json güncel değeri: −4,7…−7,8 (3 referans). S-06 ile birlikte: tüm sayfalarda tek aralık.
- Sahip: PC1 / key_findings.md sahibi.

## S-30 · science.html'de ham Markdown/LaTeX görünüyor olabilir (kontrol edilmeli)
*Öncelik: Orta · Yer: Science · Sahip: PC1*
- PDF: Bölüm 2.1–2.2'de "$n$", "$r$", "**Moving (`" gibi işlenmemiş metin. science.html, docs/story/*.md dosyalarını basit bir md() fonksiyonuyla gösteriyor; tablo ve $…$ desteklemiyorsa ham metin kalır.
- Yapılacak: Sayfayı tarayıcıda açıp kontrol et; varsa md dosyalarında $…$ yerine düz metin kullan veya md() fonksiyonuna tablo desteği ekle.
- Sahip: PC1.

## S-31 · Açılış arka planı: canlı harita ve kırmızı filtre yerine hazır döngü videosu
*Öncelik: Yüksek · Yer: Açılış · Sahip: PC6 (video), PC8 (sayfa)*
- Nerede: `web/index.html` hero (`#heroMap`), `web/app.js` `hero()`.
- Sorun: Canlı MapLibre haritası açılışta uydu karosu indiriyor ve sürekli çiziliyor (yavaşlık, batarya, mobilde takılma). Üstündeki kırmızı-mavi çökme katmanı sert kenarlı ve ilk izlenimi bozuyor. Mehmet kararı: sürekli oynayan canlı harita yerine hazır, hareketli bir arka plan olsun ve **kırmızı çökme filtresi hiç olmasın**.
- Öneri: Koyu, sade uydu görüntüsü üzerinde yavaş kayma/yakınlaşma yapan dikişsiz, sessiz, ≤1.5 MB döngü videosu (MP4+WebM) ve ≤150 KB poster (WebP). GIF önerilmez (S-22: 4 MB+), PDF hareket etmez. Sayfa videoyu `autoplay muted loop playsinline` ile oynatır; reduced-motion ve yükleme hatasında poster. Başlık için sol taraf koyu kalır. Çökme verisi, renk çubuğu, yazı yok (S-18 ile uyumlu).
- Görevler: B30 (video), B31 (sayfa).

## S-32 · Takım adı: "Team Taykut" → "Team Aseltech"
*Öncelik: Yüksek · Yer: Kapak ve site · Sahip: PC8*
- Nerede: `web/index.html` hero `.byline`, Figure 6 kredisi, sayfa sonu satırı; `web/data.html`, `web/faq.html`, `web/science.html` alt bilgi.
- Sorun: Takım adı Aseltech oldu; kapakta ve alt bilgilerde Taykut yazıyor.
- Öneri: Web sayfalarındaki tüm geçişleri değiştir (grep ile 0'a indir). `docs/story/*`, `analysis/*` içindeki grafik kredileri başka PC'lerin; ayrıca karar verilecek.
- Görev: B32.

## Uygulanmaması gerekenler (dış inceleme PDF'inden)
- "#findings çapası yok": yanlış; index.html ve science.html'de id="findings" var.
- "Haritalar, grafikler, tablolar, Data/Explore satırları boş; href=\"#\" bağlantılar çalışmıyor": Bu öğeler JavaScript ile dolduruluyor (app.js gameOpen/view3d bağlantılarını ve videoyu sonradan atıyor). İnceleme büyük ihtimalle JavaScript çalıştırmayan bir araçla yapılmış. Ekran görüntülerimizde veri yükleniyor. Yine de: canlı siteyi telefonda ve gizli pencerede bir kez açıp kontrol edin; JS kapalıyken en azından "Loading…" / açıklama metni gösterilmesi iyi olur.
- "Yolları ./data/ yap": app.js zaten ROOT = './' kullanıyor (yayında göreli).
