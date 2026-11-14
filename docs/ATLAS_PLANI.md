# BÜYÜK GÖREV — "NISAR Küresel Çökme Atlası 2026" (Cmt 20:50 → Paz 20:00 TR)
Mevcut küçük işlerini bitiren her ajan SORMADAN buraya geçer. Sırası aşağıda; kendi bölümünü yukarıdan aşağı yap.
Jüri mesajı: *"NISAR'ın ilk kamuya açık aylarındaki veriyle dünyanın ~20 yeraltı suyu çökme bölgesini aynı yöntemle, tek komutlu kendi aracımızla ölçtük ve sıraladık."* ("İlk" iddiası ancak PC5 literatür kontrolünden sonra "to our knowledge" ile kullanılır.)
Kurallar: sadece provisional (her iki tarih ≥ 2026-06-17, P05023); her şehir `data/global/<şehir>/` (veri sözleşmesi); ham .h5 kesince sil; aynı bilgisayarda aynı anda tek indirme; REVIEW_1500 dili; `git add <yol>`; her adımda commit + push.
Sabit saatler: gece indirme (bilgisayarlar açık, uyku kapalı) · Paz 14:00 atlas veri sonu · Paz 20:00 dondurma · 22:00 teslim.

> **NOT (PC1, 21:25): PC3, PC6 ve PC8'e görevleri Mehmet (M3hmeT1888) kendisi veriyor.** Bu dosyadaki PC3/PC6/PC8 maddeleri sadece öneridir; PC1 bu üç ajana görev atamaz. Atlas sayfası (`web/atlas.html`) için sahip Mehmet'in kararıdır.

## 🔬 KALİTE STANDARDI (PC1 inceleme, 21:05) — sıralama adil ve savunulabilir olsun diye ZORUNLU
PC1 planı inceledi; 4 zayıflık düzeltildi. Bu bölüm diğer her şeyin önündedir.
1. **Aynı kutu, aynı ölçüt:** her şehir için bbox = merkez ± 0.25° (≈ 55 × 55 km; kıyı/şehir dışı alan çoksa merkezi kaydır, boyutu değil). Başlık değeri = 1 km blok medyanlarının en negatifi (PC3 yöntemi) **ve** 2. yüzdelik (p2) — ikisi de `summary.json`'da. Farklı kutu boyu sıralamayı bozar.
2. **Dönemden bağımsız hız:** şehirlerin tarih aralıkları farklı → atlasta sıralama ölçütü **`rate_cm_per_100d` = başlık değeri / gün × 100** (LOS). Yıllık değer sadece "estimate" etiketiyle, sıralamada kullanılmaz.
3. **Referans bölgesi çökme havzasının DIŞINDA:** referans yüksek koherenslı ve bilinen sabit bir alanda (kaya zemin/havza kenarı; literatürden veya o bölgede GPS istasyonu varsa onun yakını). Havza içindeki referans çökmeyi küçük gösterir — **Mexico City −4.4 cm büyük olasılıkla bu yüzden düşük;** PC10 Mexico City'yi bu kuralla yeniden çalıştırır.
4. **Güven sınıfı:** her şehirde `confidence` = high / medium / low: geçerli piksel oranı (≥ %40 high), referans duyarlılığı (3 referans aralığı / başlık < %30 high), literatürle büyüklük mertebesi uyumu (PC5). Atlas sıralamasında low olanlar ayrı listede, "indicative only" etiketiyle. Tropikal/kıyı şehirlerinde (Bangkok, Ho Chi Minh, Semarang, Lagos, Cakarta) düşük koherens beklenir — dürüstçe göster.
**Öncelik:** önce A (kuru iklim, yüksek bilinen çökme → temiz sinyal), sonra B.
- A: Isfahan, Rafsanjan, Mashhad, Quetta, Delhi, Eloy, Cangzhou, Gorgan, Mexico City (yeniden)
- B: Bangkok, Ho Chi Minh City, Semarang, Hanoi, Yunlin, Houston, Lagos
**Daha az ama sağlam > çok ama gürültülü:** 12 güvenilir şehir, 20 şüpheli şehirden iyidir.
**Gösterim (PC3, PC4, PC6, PC8):** sıralama ve küre rengi `rate_cm_per_100d` ile; her şehirde güven rozeti (high/medium/low); low olanlar "indicative only". Konya Ovası (−9.6 cm) dahil hiçbir başlık sayısı PC5 kontrolünden önce basın özetine/videoya girmez.

## ⚡ PARALEL BAŞLANGIÇ — 8 ajan AYNI ANDA, kimse kimseyi beklemez (21:00)
İlke "sözleşme önce": `data/global/atlas.json` biçimi sabit ve **PC1 tarafından 8 mevcut bölgeyle tohumlandı** (Konya Ovası −9.6, Central Valley −7.8, Cakarta −6.8, Karapınar −5.9, Mexico City −4.4, Tahran −3.5, Pekin −1.4, Delta −1.3 cm LOS). Görsel/metin işleri bu tohum dosyayla HEMEN başlar; yeni şehirler geldikçe dosya büyür, sayfalar kendiliğinden güncellenir.
| PC | İLK işi (bağımlılık yok, şimdi başla) | Sonra |
|---|---|---|
| PC2 | NISAR Pulse aracına §1–§3 kurallarını ekle (`--box-deg 0.25` varsayılan, p2 ve rate_cm_per_100d çıktısı, `--ref-lonlat` ile havza dışı referans) → kendi bölgeleri (A önce) | araç iyileştirme |
| PC10 | **Mexico City'yi kalite standardı §3 ile yeniden çalıştır** → kendi bölgeleri (önce A önceliği olanlar); `build_atlas.py`: §1–§4 alanları (`rate_cm_per_100d`, `p2_cm`, `confidence`, `valid_fraction`, `ref_range_cm`) + iki liste (güvenilir / indicative) | atlas.json'u her şehirde güncelle |
| PC9 | Earthdata kurulumu (Mehmet) → kendi 5 bölgesi | — |
| PC3 | `web/atlas.html` küre + sıralama, **tohum atlas.json ile** | yeni şehirler kendiliğinden görünür |
| PC6 | Sinematik video: Central Valley 3D arazi bölümü (DEM + tam yıl verisi zaten var) | küre bölümü (tohum atlas.json) |
| PC8 | `tools/bulletin.py` Central Valley, Karapınar, Konya Ovası, Delta için (veri hazır) | atlas şehirleri |
| PC5 | **Güven sınıfı girdileri (§4)**: her şehir için literatür hızı + uyum notu → `data/global/<şehir>/validation_note.json` (PC10 birleştirir); mevcut 8 bölge + "ilk mi?" taraması. **Öncelik: Mexico City −4.4 cm (108 gün) yayımlanmış hızlara göre düşük görünüyor — neden (koherens, bbox, referans) incele, PC10'a not** | yeni şehirler |
| PC4 | Basın özeti + atlas slaytı + teknik not bölümü, **tohum atlas.json ile** | yeni şehirlerle güncelle |
| PC7 | O2 olasılıksal risk | `validate_atlas.py` |
| PC11 (21:40, yeni) | **Tahran, Cakarta, Pekin'i kalite standardıyla yeniden hesapla** (PC10'dan devredildi) → Celaya, Tianjin, Kerman, Bulacan (`tasks/PC11.md`) | PC10'a "hazır" notu |
Çakışma kuralı: `data/global/atlas.json` dosyasını SADECE PC10 (build_atlas.py) yazar; diğerleri okur.

## Bölgeler (merkez lon, lat — bbox'ı ±0.25–0.35° olarak sen kur, önce ASF'de provisional GUNW kapsamasını kontrol et; kapsama yoksa "no coverage" diye atlasa yaz ve sıradakine geç)
| Kim indirir/işler | Bölgeler |
|---|---|
| **PC10** (Memir, AG-2) | Bangkok 100.55, 13.70 · Ho Chi Minh City 106.70, 10.78 · Semarang 110.42, −6.97 · Hanoi 105.83, 21.00 · Yunlin (Tayvan) 120.35, 23.70 |
| **PC2** (Memir) | Isfahan 51.67, 32.65 · Rafsanjan 55.99, 30.40 · Mashhad 59.60, 36.30 · Quetta 67.00, 30.18 · Delhi (Kapashera) 77.08, 28.55 |
| **PC9** (Mehmet 2. bilgisayar) | Houston/Katy −95.80, 29.80 · Eloy (Arizona) −111.55, 32.75 · Lagos 3.39, 6.45 · Gorgan 54.43, 36.84 · Cangzhou (Kuzey Çin Ovası) 116.85, 38.30 |
Mevcut: Mexico City, Tahran, Cakarta, Pekin (PC10), Central Valley, Karapınar, Konya Ovası, Delta.

## PC10 — atlas veri sahibi
1. Kendi 5 bölgen: `python -m pipeline.nisarpulse run --name <şehir> --bbox ... --start 2026-06-17 --end 2026-10-31 --quality provisional` (önce `--dry-run`). Çıktı `data/global/<şehir>/`.
2. **`data/global/atlas.json`** üreticisi: `pipeline/pc10/build_atlas.py` — tüm `data/global/*/summary.json` + Central Valley, Karapınar, Konya Ovası, Delta → her kayıt `{id, name, country, lon, lat, max_cm_los, max_cm_vertical_est, period, n_pairs, quality, rate_cm_per_yr_estimate, coverage:"ok|partial|none", note}` + sıralama (en çok çökenden). Her yeni şehirden sonra yeniden çalıştır.
3. `docs/story/global_atlas.md`: atlasın sade anlatımı (yöntem aynı, dönem ~108 gün, provisional, LOS uyarısı), ilk 10 tablo.

## PC2 — bölgeler + araç
1. Kendi 5 bölgen (PC10 ile aynı bilgisayar: sırayla, aynı anda en fazla 1 indirme).
2. NISAR Pulse aracını atlas sırasında iyileştir: hata yakalama, `--resume`, kapsama raporu (`coverage.json`); `docs/story/engine.md`'ye "20 bölgede çalıştı" kanıtı.

## PC9 — bölgeler
0. Bu bilgisayarda Earthdata `~/.netrc` yoksa Mehmet kursun (şifreyi kendisi yazar; biçim RULES E-07). Kurulamazsa status'a yaz ve PC2'den bir bölgeyi devral değil, aşağıdaki 3. maddeye geç.
1. Kendi 5 bölgen (NISAR Pulse aracı ile).
2. Her bölge için `summary.json` makul mü (literatür büyüklük mertebesi) — PC5'e not.
3. (Kapsama/indirme yoksa) Karapınar tam yıl kalıcı kayıp (O1 Türkiye) PC8 ile koordineli.

## PC3 — atlas sayfası (site)
1. **`web/atlas.html`**: dönen 3D küre (MapLibre GL JS 5.x globe projection, sabit sürüm; olmazsa 2D dünya haritası), `data/global/atlas.json` noktaları (boyut/renk = çökme), tıklayınca yan panelde şehrin animasyonu (disp PNG serisi, zaman kaydırıcı), küçük grafik ve kaynak. Menüye "Atlas".
2. **"Fastest-sinking places in our 2026 NISAR atlas"** sıralama tablosu (dönem ve LOS uyarısıyla), ana sayfaya özet kartı.
3. Explorer'a atlas şehirleri; Data sayfasına atlas dosyaları (catalog).
4. PC6 videosu, PC8 bültenleri, PC4 basın özeti geldikçe bağla.

## PC6 — sinematik demo videosu v2 (gerçek animasyon)
1. 3D arazi: Copernicus DEM GLO-30 (AWS açık veri, girişsiz) + Central Valley kümülatif çökme dokusu, dikey abartma; deck.gl TerrainLayer veya three.js; yerin aylık "nefesi" (tam yıl serisi, mixed etiketli).
2. Kamera senaryosu (≤30 sn): Central Valley 3D (12 sn) → küreye geri çekilme ve atlas noktaları (8 sn) → Konya/Karapınar (6 sn) → kapanış kartı, site linki (4 sn). Sade İngilizce altyazı (PC8'in SRT'si temel), "LOS" yok, büyük yazı.
3. Tarayıcıda kare kare kayıt (Puppeteer/Playwright) → ffmpeg 1080p → `docs/story/media/demo_30s_v2.mp4`. AI görseli/sesi yok.
4. Ayrıca sitede gömülebilir hafif sürüm (`web/` için 720p, PC3 bağlar).

## PC8 — erken uyarı bülteni (operasyonel ürün) + O1
1. O1 Karapınar (tam yıl decomp gelince) bitir.
2. **`tools/bulletin.py`** → `docs/bulletins/<bölge>.html` (+ yazdırılabilir): başlık "NISAR Pulse Bulletin — <bölge> — <son tarih>", son çiftteki ve toplam çökme, en riskli 5 segment (O2 olasılıkları gelince), GPS uyumu, kalite etiketi, kaynak. Central Valley, Karapınar, Konya Ovası, Delta + atlas şehirleri için tek sayfalık özet bülten.
3. `submission_form.md`'ye atlas ve bülten satırları.

## PC7 — O2 + atlas kalite kontrolü
1. O2 olasılıksal mühendislik riskini bitir (`docs/OZGUN_KATKILAR.md` §O2).
2. `pipeline/pc7/validate_atlas.py`: her `data/global/<şehir>/` sözleşmeye uygun mu, `atlas.json` sıralaması summary'lerle tutarlı mı, NaN yok mu → `docs/qa/PC7.md`; her yeni şehirde yeniden çalıştır.

## PC5 — atlas bilimsel doğrulaması
1. **Literatür kontrolü:** NISAR verisiyle yayımlanmış küresel çökme sıralaması var mı? Sonuca göre "to our knowledge, the first …" cümlesi kullanılabilir mi — `docs/story/atlas_validation.md`.
2. Her atlas şehri için yayımlanmış InSAR/GPS çökme hızı (kaynaklı) ve bizim 108 günlük değerle büyüklük mertebesi kıyası; uyuşmayanlar için olası neden (atmosfer, koherens, dönem).
3. Her şehir için belirsizlik (`analysis/pc5/uncertainty_map.py`) → `data/global/<şehir>/uncertainty/`.
4. Önceki işlerden kalan: `key_findings_public.md` güncellemesi (atlas dahil).

## PC4 — anlatım
1. `technical_note.md/html`'e "Global atlas" bölümü ve tablo (PC10 atlas.json'dan).
2. `slides.html`: 1 atlas slaytı (küre görseli + ilk 5 sıralama).
3. **`docs/story/press_summary.md`**: tek sayfalık basın bülteni tarzı özet (başlık, 3 paragraf, 3 sayı, görsel, iletişim: repo/site).
4. `project_page.md` ve `judge_faq.md`'ye atlas.
