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
