# PCQ · Bağımsız kontrol notları

Kural: dosyaları düzeltmiyorum, sadece raporluyorum. Biçim: `OK` veya `HATA: dosya → ne yanlış → doğrusu`. Kritik olanlar üstte.
Not (şeffaflık): PCQ bu oturumda daha önce PC3 rolünde `analysis/` ve `data/<site>/` çıktılarını üretti. Bu çıktıları kontrol ederken bağımsızlık sınırlı; hesapları yeniden yürüttüm ve çapraz dosya tutarlılığına baktım.

## Tur 1 · 2026-11-14 14:20 TR (HEAD 6136c3f)

### KRİTİK / ÖNCELİKLİ
- HATA: `docs/story/pitch.md:43` → "Click the hotspot south-southeast of Tulare Lake (`max_subsidence_location`)" yazıyor ama `summary.json` maks noktası **6 km N of Terra Bella (−119.022, 36.011)**, yani vadinin doğu kenarı (Friant-Kern Kanalı bölgesi), Tulare Gölü'nün GGD'si değil → "Click the hotspot near Terra Bella on the east side of the valley (Friant-Kern Canal area)" olmalı. Demo sırasında yanlış yere tıklanır. (Sahip: PC6/PC5 pitch)
- HATA: `web/app.js` `humanScale()` → en küçük ölçek banka kartı (8.56 cm). |v| < ~4 cm olan her nokta için cümle yine "about the width of a bank card" diyor; örn. referans yakını 0.2 cm → "bank card" (43 kat abartı) → küçük değerler için ölçek ekle (ör. 1 cm ≈ "a fingernail", 2.5 cm ≈ "a coin's diameter") ya da |v| < 1 cm ise karşılaştırma yapma. (Sahip: PC1)
- HATA: `web/app.js` `select()` → v < 0 olan her değer "sank" diyor; ±1 cm içindeki değerler gürültü düzeyinde (çift başı ~1–3 cm atmosfer artığı, `status/PC3.md`). → |v| < 1 cm için "no clear change (within measurement noise)" yazılmalı. (Sahip: PC1)
- HATA: `web/app.js` cümle → "this spot sank 7.8 cm" ama değer **LOS** (bakış yönü). Grafik etiketi doğru ("line of sight"), cümle değil → "moved 7.8 cm away from the satellite (≈ sinking)" ya da "sank about 7.8 cm (line of sight)". (Sahip: PC1)
- HATA: `web/index.html` Konya sahnesi → NISAR kümülatif çökme katmanı (`data/karapinar/disp/`) haritada gösteriliyor ama **renk lejantı, birim, tarih aralığı yok**; kullanıcı rengin ne anlama geldiğini bilemez → Central Valley'deki gibi lejant (`meta.vmin`/`vmax` cm) + "26 Jun – 12 Oct 2026, line of sight" satırı eklenmeli. (Sahip: PC1)

### ORTA
- HATA: `data/central_valley/meta.json` + `web` lejantı → renk aralığı vmin −6 cm, ama başlık değeri −7.8 cm; −6'nın altındaki değerler aynı koyu kırmızıya kesiliyor. Karapınar: vmin −5, maks −5.9. → Lejantın sol ucu "≤ −6 cm" (Karapınar "≤ −5 cm") yazılmalı ya da vmin ≥ |maks| seçilmeli. (Sahip: PC3 vmin / PC1 lejant)
- HATA: `web/index.html:47` Holme Fen kartı → hâlâ "Exact figure and source being verified" diyor; `docs/story/sources.md:13` artık "approximately 4 metres" + kaynak veriyor → karta kaynaklı sayı ve link eklenmeli. (Sahip: PC1)
- HATA: `data/catalog.json` → `karapinar` ve `uk` girişleri `quality: "pending"`, `layers: []`; oysa `data/karapinar/{meta,points,summary}.json` + 9 PNG + sinkholes ve `data/uk/meta.json` mevcut → katmanlar ve gerçek quality (`provisional` / `preview`) yazılmalı. Site `catalog.json`'u okumadığı için görünür etki yok, ama sözleşme belgesi olarak yanlış. (Sahip: PC1)
- HATA: `web/app.js` `select()` ay sayısı → `Math.round(108 gün / 30.4)` = **4 months**; gerçek süre 3.5 ay. Pitch/project_page "3.5 months" derse çelişir → "about 3½ months" ya da hafta/gün kullanılmalı. (Sahip: PC1)
- HATA: `docs/story/sources.md` → başlık değerinin yeri olan Terra Bella / Friant-Kern Kanalı için kaynak yok. → KVPR (2017) Friant-Kern kapasite kaybı ve "deepest sinking near Terra Bella": https://www.kvpr.org/environment/2017-08-03/friant-kern-canal-slows-by-60-percent-subsidence-to-blame (HTTP 200 kontrol edilmeli). (Sahip: PC4)
- HATA: `data/karapinar/points.json` → 9 nokta; sözleşme (§4.2) 10–15 diyor. Geçerli piksel oranı %14 olduğu için "medyan" noktalardan sadece 2 bulunabildi → ya sözleşmeye istisna notu ya da eşik gevşetme. (Sahip: PC3)
- BİLGİ: `docs/story/project_page.md` → Karapınar için sadece 12 günlük kontrol çifti istatistikleri var; artık 8 çiftlik kümülatif sonuç mevcut (`data/karapinar/summary.json`: −5.9 cm LOS, 108 gün, 2 km W of Karapınar, güven düşük-orta). Güncellenmesi önerilir. (Sahip: PC4)

### 1a · data/central_valley ve data/karapinar tutarlılığı
- OK: `meta.dates` = `disp/*.png` adları (CV 8, KP 9) = `points[*].dates` = `_cum.npz` `dates`.
- OK: `summary.period` = [ilk, son] meta tarihi (CV 2026-06-28→10-14, KP 06-26→10-12).
- OK: `quality` her üç JSON'da ve `_cum.npz`'de `provisional`; `quality_note` standart dipnot.
- OK: `summary.max_subsidence_cm` = en negatif nokta (`p01`) son değeri ve konumu birebir (CV −7.8 @ −119.02173, 36.01119; KP −5.93→−5.9 @ 33.53056, 37.71818).
- OK: `rate_cm_per_yr_estimate` = maks/gün×365.25 (CV −26.4, KP −20.0); "estimate" ve abartı uyarısı `method_note`'ta.
- OK: `reference_point` meta = summary.
- OK: Tüm noktalar bbox içinde.
- OK: Dikey tahmin −7.8/cos(39.1°) = −10.05 ≈ −10.1 ✔; CV geliş açısı aralığı 37.8–45.3°.
- BİLGİ: `_cum.npz` piksel minimumu −29.0 cm (CV), −9.1 cm (KP); bunlar tekil artefakt pikseller (başlık 1 km blok medyanı). Site piksel değeri göstermediği için sorun değil; PC6 risk indeksi tekil piksele değil segment istatistiğine dayanmalı.
- BİLGİ: `summary.max_subsidence_range_cm` CV'de [−7.8, −6.2]; KP'de `null` (30 km'den uzak ikinci referans yok).

### 1b · web/app.js sayılar ve cümleler
- OK: Site sayıları doğrudan JSON'dan okuyor; app.js/index.html'de elle yazılmış ölçüm sayısı yok.
- OK: Lejant `meta.vmin`/`vmax`'tan; badge `quality`'den; tarih kaydırıcısı `meta.dates`'ten.
- OK: Grafik etiketi "Ground motion (cm, line of sight)".
- (HATA'lar yukarıda: insan ölçeği, gürültü eşiği, LOS ifadesi, ay yuvarlaması, Konya lejantı)

### 1c · pitch.md, project_page.md, sources.md
- OK: `pitch.md` ölçüm sayılarını `{PLACEHOLDER}` olarak tutuyor (K-2 uyumlu); tablo summary.json alanlarına bağlanıyor.
- OK: `project_page.md` CV satırı: −7.8 cm LOS, −10.1 cm dikey @ 39.1°, 6 km N of Terra Bella, −26.4 cm/yr "overstates" notuyla = summary.json.
- OK: 8.5 m (28 ft) 1920'lerden beri, 0.6 m/yıl Chowchilla/Corcoran → `sources.md:29` (USGS/NASA) kaynaklı.
- OK: 104 obruk / 86 Karapınar / 43 yeni (1972–2014) → `sources.md:45,50` (Tapur & Bozyiğit 2015/2016).
- OK: £540 milyon / %350 / £64 milyon / >10 000 → `sources.md:58`.
- OK: Holme Fen ~4 m, 1851 → `sources.md:13` (pitch'te `{HOLME_FEN_M}` yer tutucu).
- OK: "L-band 24 cm" → ürün λ 0.242–0.244 m ✔.
- HATA (yukarıda): pitch hotspot konumu; sources.md'de Terra Bella kaynağı eksik.

### 1d · Kalite etiketleri
- OK: CV `meta/points/summary/validation/assets` ve `web3d/surfaces.json` → `provisional`; `data/uk/meta.json` → `preview`.
- OK: provisional/beta karışımı yok: CV ve KP zincirlerindeki tüm çiftler ≥ 2026-06-17 (06-16→06-28 beta-precal çifti atlanmış, `meta.notes`'ta yazıyor).
- OK: Kalibrasyon dipnotu `web/index.html:152` ve her katmanın `quality_note`'unda.
- OK: AI etiketleri: hero, 4 arka plan, Holme Fen, obruk, oyun posteri → hepsinde "AI-generated (background) illustration". Footnote AI kullanımını açıklıyor. Kesit SVG'si "Illustrative diagram (not to scale)".
- HATA (yukarıda): `catalog.json` karapinar/uk `pending`.

### 1e · data/karapinar/sinkholes.geojson
- OK: 29 nokta, hepsi bbox [33.3, 37.6, 33.8, 37.9] içinde, yinelenen koordinat yok.
- OK: Her noktada `name, year_formed, source_title, source_url, coord_source` var (+ `depth_m, diameter_m, status`).
- OK: Tek kaynak: Tapur & Bozyiğit (2015) https://dergipark.org.tr/tr/download/article-file/3454 → HTTP 200.
- BİLGİ: `coord_source = "paper table"`; koordinatların makaledeki tabloyla tek tek eşleşmesi bu turda doğrulanmadı (PDF tablo karşılaştırması sonraki tur).

### Ek · GNSS doğrulaması (`data/central_valley/validation.json`, PC6)
- OK: 10 istasyon, 8 tarih (06-28→10-14, CV ile aynı). Vadi tabanında güçlü uyum: CAHA r=0.90 RMSE 0.75 cm, HANF r=0.90/0.83, QCAP 0.82/0.77, TLBN 0.79/1.17, P056 0.66/0.79.
- BİLGİ: Vadi kenarı / etek istasyonları (CAD1, P564, P565, CAFP) zayıf veya negatif korelasyon (r −0.41…0.07), RMSE 1.6–2.8 cm; bunlar az hareketli yerler, sinyal gürültü düzeyinde. Sunumda "valley-floor stations agree to within ~1 cm" denebilir; tüm istasyonların ortalaması verilirse kenar istasyonları da belirtilmeli.

## Tur 2 · 2026-11-14 14:55 TR (HEAD b3bfb26, d1bb6ed'den bu yana 34 yeni commit)

### Tur 1 bulgularının durumu
- OK (düzeldi): `docs/story/pitch.md` → yanlış "south-southeast of Tulare Lake" hotspot ifadesi kaldırıldı (PC4, 0bc348f).
- OK (düzeldi): `docs/story/sources.md` → Terra Bella / Friant-Kern kaynağı eklendi (3 eşleşme).
- OK (düzeldi): `.github/workflows/pages.yml` → `web3d/` ve `docs/story/` artık yayına kopyalanıyor (PC1, 669b7e8).
- OK (düzeldi): `game/game.js:927` → `../risk/...geojson` sadece yerelde çekiliyor, Pages'te `assets.json` kullanılıyor; hatada `console.warn` (PC6).
- OK (düzeldi): oyun kutusu artık "Model check against NISAR"; `S_y` 0.10 (kaynaklı); `S_ske` ve su yılı olasılıkları `illustrative: true` (PC6, `docs/story/game_model.md` ile uyumlu).
- OK (kısmen): `pipeline/download.py` → `.netrc` artık `urs.earthdata.nasa.gov` makinesine göre okunuyor + `EARTHDATA_TOKEN` desteği. Hâlâ `Authorization: Bearer <password>` gönderiyor: `.netrc`'de gerçek parola varsa 401 alır; README/E-07 ile çelişki sürüyor → token kullanılıyorsa README'ye "EARTHDATA_TOKEN" satırı eklenmeli. (Sahip: PC2)
- OK (düzeldi): Konya haritası artık lejantlı (`web/app.js:56` `kp: legend: true`).
- HATA (sürüyor): `web/app.js:15-16,151` → site v2 cümlesi hâlâ (a) en küçük ölçek banka kartı (0.2 cm → "bank card"), (b) gürültü eşiği yok (±1 cm'de de "sank/rose"), (c) "sank" diyor ama değer LOS, (d) `Math.round(108 gün / 30.4)` = "4 months" (gerçek 3.5). → küçük ölçekler (≈1 cm "a fingernail", ≈2.4 cm "a coin") + |v| < 1 cm için "no clear change (within noise)" + "moved … away from the satellite" + "3½ months". (Sahip: PC1)
- HATA (sürüyor): `web/app.js:117` lejant `−6` / `+6` → başlık değeri −7.8 cm kesiliyor; "≤ −6" yazılmalı. (Sahip: PC1)
- HATA (sürüyor): `data/catalog.json` → `karapinar` ve `uk` hâlâ `quality: "pending"`, `layers: []`; Karapınar'da artık meta/points/summary/disp + `assets.json` + sinkholes, UK'de `meta.json` var. (Sahip: PC1)
- BİLGİ (sürüyor): `game/model.js:138` yorum "Deep Corcoran Clay lacustrine member" ama `clayThicknessM: 82` > USGS'te Corcoran Kili için verilen en büyük ~61 m (`docs/story/game_model.md` §2). Yorum "total compressible interbeds" olmalı. (Sahip: PC6)

### Yeni içerik kontrolü
- OK: `python -m pytest analysis -q` → 36 passed; `python -m pytest analysis/decomp -q` → 18 passed (PC5'in `error_budget`, `point_quality` testleri dahil).
- OK: `data/central_valley/drivers.json` (PC2, Q04) ve `data/karapinar/assets.json` (PC6, 64 öğe) → `quality: provisional` var.
- OK: `docs/story/uncertainty.md` (PC5) çapraz kontrol: zincir gürültüsü 1.7–2.9 cm (σ_çift·√7) ↔ Q21 iki yörünge RMSE 2.6 cm (iki bağımsız zincirin farkı için beklenen ≈ √2 × 1.9 ≈ 2.7 cm) → **tutarlı**. GNSS medyan RMSE 1.00 cm ↔ `validation.json` (0.64–2.79) ✔.
- OK: `data/central_valley/vertical.json` (Q22) `quality`, `quality_note`, renk anlamı ve yöntem alanları var; Alpaugh çanağı −7.2 cm dikey, en uç blok −9.8 cm (güven notuyla).
- BİLGİ: Q21 sonucu (r 0.49, yerel 0.60, işaret uyumu %85) PC4 tarafından hikâye belgelerine işlenmiş (efb9350); sayılar `analysis/out/cv_p34_vs_p114.json` ile eşleşmeli — sonraki turda satır satır kontrol.

## Tur 3 · Uçtan uca çalışma testi · 2026-11-14 15:25 TR (HEAD 8c1da2a)

Yöntem: tüm testler + tüm veri dosyaları + site gerçek tarayıcıda (yerel `/web/` ve `pages.yml`'nin birebir kopyası,
`/aseltech/` alt yolunda — GitHub Pages ile aynı yapı). Masaüstü ve telefon (375 px) genişliği.

### Çalışıyor (OK)
- OK: `python -m pytest analysis -q` → **49 passed**; `validation/compare.py --self-test` ✔; `risk/compute_risk.py --self-test` ✔.
- OK: 31 JSON/GeoJSON dosyası parse ediliyor; `data/` altındaki tüm PNG/JPG açılıyor; repoda 20 MB üstü takipli dosya yok.
- OK: Ana sayfa, Science, Data, FAQ → **konsolda hata yok, başarısız istek yok** (yerel ve Pages kopyası). Data sayfasındaki 17 indirme linki 200.
- OK: Pages kopyasında tüm veri dosyaları, 8 tarih PNG'si, Karapınar katmanı, UK görsel çifti, animasyon videosu yükleniyor.
- OK: Sitedeki sayılar veriyle tutarlı: −7.8 cm LOS / ≈−10.1 dikey, 6/10 GPS istasyonu r ≥ 0.4 (tablodan sayıldı), 81 yüksek riskli segment (645 içinde), Karapınar −5.9 cm, 29 obruk.
- OK: Oyun ("Valley Under Pressure") Pages kopyasında açılıyor; "Model check against NISAR: PASS, error 0 %, k = 0.623"; aşırı pompalama ile 24 ay sonuna kadar oynandı, NaN/undefined yok, sonuç ekranı geliyor (−37.6 cm / 2 yıl, kuraklık dönemi literatür zirvesi ~60 cm/yıl ile çelişmiyor).
- OK: 3D görüntüleyici (`web3d/`) Pages kopyasında açılıyor, canvas çiziliyor, başlık sayıları summary ile aynı; geri linkleri çalışıyor.
- OK: `game.js` `../risk/...` isteği sadece `localhost/127.0.0.1`'de yapılıyor; gerçek Pages'te 404 olmayacak (yerel testte görülen tek 404 bu).

### Bulgular
- HATA (orta): referans aralığı 15:00'te **−4.7 … −7.8 cm** oldu (`summary.json` `range_cm`, 3 referans), ama şu yerlerde eski **−6.2 … −7.8** kaldı:
  `game/game.js:942` (oyun açılış kutusu, sabit metin → `summary.range_cm`'den okunmalı, Sahip: PC6) ·
  `docs/story/uncertainty.md:16,60` (Sahip: PC5) · `docs/story/key_findings.md:7` (Sahip: PC5/PC1).
  Düzeltildi: `README.md` (PCQ), `docs/story/game_model.md` (PC3).
- HATA (sürüyor, PC1): ana sayfa cümlesi "6 km N of Terra Bella sank 7.8 cm in **4 months**" → gerçek süre 108 gün = 3½ ay; "sank" yerine LOS ifadesi; küçük değerler için banka kartı ölçeği ve gürültü eşiği (Tur 1–2).
- BİLGİ (PC1): ana sayfa "Two independent satellite tracks (34 and 114) show the same subsidence bowl" → Q21 verisi bunu destekliyor ama "aynı" güçlü; daha doğru: "largely agree (sign agrees in 85 % of strongly moving areas)".
- BİLGİ (PC1): "consecutive 12-day pairs summed" → zincirde 24 günlük (07-22→08-15) bir çift var; "consecutive pairs (mostly 12 days)" daha doğru.
- BİLGİ (PC1, kullanılabilirlik): telefonda (375 px) üst menüde "Data" ve "FAQ" ekran dışında kalıyor; menü kaydırılabilir (`overflow-x:auto`) ama kaydırma çubuğu gizli olduğu için ipucu yok → küçük ekranda menüyü sarmak ya da kenarda solma gölgesi.
- BİLGİ (PC1): `.gitignore` → `analysis/out/subset/` (yerel alt kümeler, dosya başı 21–23 MB) listede yok; biri yanlışlıkla `git add` yaparsa K-12 ihlali olur → satır eklenmesi önerilir.

**Sonuç: proje uçtan uca çalışıyor; yayını bozacak (kırık link, JS hatası, eksik dosya) bir sorun bulunmadı.** Kalanlar metin/tutarlılık düzeltmeleri.

## Tur 4 · 2026-11-14 15:23 TR (HEAD 86cdaa2)
- Yeni commit'ler: PC9 açıldı (site sahipliği PC1 → **PC9**; site bulgularının yeni muhatabı PC9), PC2 Q09 Londra alt kümeleri (9/9), PC6 önceliği.
- OK: `python -m pytest analysis -q` → 49 passed; değişen JSON'lar parse ediliyor.
- Sürüyor (PC9 / PC6 / PC5): eski referans aralığı `game/game.js:942`, `docs/story/uncertainty.md`, `docs/story/key_findings.md:7`; `web/app.js:150` "4 months"; `data/catalog.json` karapinar/uk `pending`; `.gitignore`'da `analysis/out/subset/` yok.
