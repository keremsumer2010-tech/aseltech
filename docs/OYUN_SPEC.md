# OYUN SPEC — "Valley Under Pressure" (Aquifer Manager v2, sıfırdan)
Sahip: **PC6** (kod, `game/`) · Model parametreleri: **PC5** (`docs/story/game_model.md`) · Onay: PC1
Eski oyun ve AI görselli tasarım İPTAL. Hedef: hakemin "bu gerçek veriyle çalışan bir simülasyon" diyeceği, profesyonel, AI görünümsüz oyun.

## İlke
- **Hiç AI görseli yok.** Görseller = gerçek veri: Esri uydu altlığı, bizim NISAR çökme haritamız (`data/central_valley/disp/*.png`), OSM kanal/yol hatları (`risk/central_valley_infra.geojson`), gerçek yer adları (`data/central_valley/points.json`). Arayüz grafikleri kodla çizilir (Canvas/SVG/WebGL), sade ve "kontrol odası / bilim aracı" estetiğinde.
- **Gerçek mekanik:** fiziksel olarak savunulabilir basit model + parametreleri kaynaklı + NISAR ölçümüyle kalibre.
- **Kıyas:** oyun sonunda oyuncunun vadisi "gerçek 2026 NISAR ölçümü" ile yan yana.

## Oyun döngüsü
- Harita: Central Valley, gerçek uydu altlığı; üstünde 6–8 **ilçe/bölge** (points.json'daki çökme merkezleri + çevresi, isimleri gerçek).
- Zaman: 1 tur = 1 ay, 24 ay (2 sulama sezonu + 2 kış). Mevsim ve yıl tipi (wet/normal/dry/critical) — yıl tipi dağılımı kaynaklı (California Water Year Index sınıfları; PC5 kaynak verir).
- Oyuncu her bölge için: **yeraltı suyu pompalama** (0–150 %), **yüzey suyu tahsisi** (kanal suyu, kurak yılda kısıtlı), **nadasa bırakma** (alan %).
- Çıktılar her tur: ürün geliri ($), yeraltı suyu seviyesi (m), **çökme (cm; elastik + kalıcı ayrı)**, kanal kapasite kaybı (%), kuyu kuruması sayısı.

## Fizik modeli (PC5 parametreleri doğrular ve kaynaklar)
- Akifer seviyesi: `Δh = (recharge − pumping_withdrawal) / (S_y · area)` (basit kova modeli, bölge başına).
- Çökme (Terzaghi/USGS yaklaşımı): seviye "önceki en düşük seviye"nin (preconsolidation head) üstündeyken **elastik** `Δb = S_ke · Δh · b0`, altına inince **inelastik/kalıcı** `Δb = S_kv · Δh · b0` (S_kv ≫ S_ke). Elastik kısım su gelince geri döner, kalıcı kısım dönmez → oyunda iki renk.
- Kalibrasyon: "normal yıl, mevcut pompalama" senaryosu 108 günde ölçtüğümüz çökmeyi (summary.json: −7.8 cm LOS / ~−10 cm dikey tahmin) vermeli. Kalibrasyon katsayısı CONFIG'de ve ekranda açıklanır.
- Altyapı: kanal segmentlerinde diferansiyel çökme eğimi (mm/km) eşiği aşınca kapasite düşer (Friant-Kern/Delta-Mendota için yayımlanmış kapasite kaybı bilgisi varsa PC5 kaynaklar; yoksa "illustrative" etiketli).
- Kuyu: seviye kuyu derinliğinin altına inerse kuyu kurur (bölge başına kuyu derinliği dağılımı; kaynak yoksa illustrative).

## Görsel ve efektler (kodla, gerçekçi)
- Uydu altlık + NISAR çökme katmanı canlı yeniden renklenir (oyuncunun simülasyonuna göre, aynı RdBu skalası).
- Kanal hatları yeşil→sarı→kırmızı; hasar anında kısa titreşim/çatlak çizgisi animasyonu (SVG stroke).
- Bölge paneli: kesit görünümü (Canvas) — yüzey, kil katmanı inceliyor, su tablası çizgisi iniyor; elastik/kalıcı ayrımı iki renk.
- Zaman çizelgesi grafiği: çökme (oyuncu) vs NISAR ölçümü (gerçek, kesikli çizgi).
- Ses: opsiyonel, çok hafif (Web Audio ile üretilmiş tık/uyarı), varsayılan kapalı.
- Tipografi: sistem fontu, mono sayılar; renkler sitenin paletiyle aynı.

## Ekranlar
1. Başlangıç: 3 cümle görev + "Your valley's real ground motion was measured by NASA-ISRO NISAR" + Başla.
2. Ana ekran: harita (sol %65) + bölge kontrolleri ve göstergeler (sağ) + alt zaman çizelgesi + "Next month".
3. Olay kartları (kuraklık ilanı, kanal kapasite düşüşü, kuyu kuruması) — metin kaynaklı/gerçekçi.
4. Sonuç: gelir, toplam/kalıcı çökme, kanal hasarı, kuruyan kuyular; **senin 24 ayın vs NISAR'ın ölçtüğü gerçek** + "What this means" + paylaşılabilir özet + tekrar oyna.

## Teknik
- Tek klasör `game/` (index.html + game.js + style.css), build yok, MapLibre 4.7.1 ve Chart.js 4.4.1 CDN (site ile aynı sürümler).
- Veri yolları: Pages'te `../data/...` değil — site kökünde oyun `game/` altında olduğundan `../data/` doğru; yerelde de `../data/` çalışır.
- 60 fps hedef, mobilde çalışır (kontroller alta iner), konsol temiz.
- Model `game/model.js` içinde ayrı ve test edilebilir; `game/test_model.html` veya node ile basit birim testi.

## Kabul
- Hiç AI görseli yok (`web/assets/*_ai.jpg` kullanılmaz).
- Kalibrasyon senaryosu ölçülen değeri ±%10 içinde üretir (ekranda gösterilir).
- Her parametrenin kaynağı `docs/story/game_model.md`'de; kaynaksız olanlar ekranda "illustrative".
- Telefonda ve masaüstünde oynanıyor; `docs/game_v2.png` ekran görüntüsü.
