---
type: gorev
id: PC4
owner: İbrahim (acikgozibrahim032-hub)
tool: Antigravity (Gemini)
status: acik
date: 2026-11-14
depends_on: []
feeds: [PC1, PC5]
---

# PC4 · Hikâye: UK görselleri, obruklar, kaynaklar

> **Saat saat sıra ve iş bitince sıradaki iş: `docs/ZAMAN_CIZELGESI.md`.** Atanmış QUEUE işlerin orada.

> **16:05 PC1 — ACİL (17:30 Lincoln provası için), diğer her şeyden önce:**
> 1. `docs/story/presentation_cues.md`: 3 dakikalık Lincoln konuşması, 30 sn'lik 6 blok; her blokta konuşan kişi (Kerem anlatır; demo sürücüsü Memir; sorular Mehmet ve İbrahim), söylenecek 1–2 cümle (sade İngilizce), aynı anda canlı sitede tıklanacak yer (https://keremsumer2010-tech.github.io/aseltech/ — güncel bölüm adlarını siteden oku). Sonda en olası 5 jüri sorusu için tek cümlelik cevap (`judge_faq.md`'den). Sayılar `data/*/summary.json`'dan.
> 2. `docs/story/rehearsal_checklist.md`: internet kesilirse yedek (`docs/story/media/demo_30s.mp4` veya `cv_subsidence.mp4` yerel kopya, slides.html çevrimdışı), sekme sırası, ekran paylaşımı, ses, süre tutma, kim ne yapar.
> 3. 17:00'ye kadar push. (Bu işler PCQ'daydı; PCQ sessiz olduğu için sana geçti. Teslim formu ve altyazı PCQ'da kalıyor.)
> Yazma alanına eklendi: `docs/story/presentation_cues.md`, `docs/story/rehearsal_checklist.md`.

## Kimlik
İbrahim'in bilgisayarı, Antigravity. Ana hattan bağımsız; bugün kimseyi beklemiyorsun.

## Yazma alanın
`data/uk/` · `data/karapinar/sinkholes.geojson` · `docs/story/sources.md` · `docs/story/calibration_note.md` · `status/PC4.md`

**Dikkat:** `data/karapinar/` içindeki diğer dosyalar PC3'ün. Sadece `sinkholes.geojson`'a yaz.

## Başlamadan
- [ ] `rules/RULES.md` (K-2 uydurma yok) ve `rules/VERI_SOZLESMESI.md` §3-§4 okundu
- [ ] Kural: **uydurma koordinat, sayı veya link yasak.** Her linki aç, içeriğin iddiayı desteklediğini gör.

---

## Görev 1 · UK "bulutun altı" görsel çifti (12:00-13:30)

1. Fens bbox için NISAR GCOV tarihlerini ASF'den listele (`platform=NISAR`, `processingLevel=GCOV`).
2. Bu tarihlerden **optik görüntüde bulutlu** bir gün seç: NASA Worldview Snapshots / GIBS (girişsiz),
   o günün MODIS veya VIIRS true color görüntüsü. Birkaç gün dene, en bulutlusunu seç.
3. Aynı günün NISAR GCOV **browse PNG**'sini indir (girişsiz).
4. Çıktılar (aynı bbox'a kırp/hizala):
   - `data/uk/optical_<YYYY-MM-DD>.jpg`, `data/uk/radar_<YYYY-MM-DD>.png`
   - `data/uk/meta.json` (sözleşme §4.2, `quality: "preview"`)

**Bitti sayılır eğer:** iki görüntü aynı alanı gösteriyor (kıyı çizgisi/The Wash hizalı), optikte bulut açıkça görünüyor, meta.json'daki iki URL açılıyor.

## Görev 2 · Karapınar obruk noktaları (13:30-15:30)

`data/karapinar/sinkholes.geojson`: sadece bir **kaynakta koordinatı verilen** veya adı ve yeri net tanımlanmış obruklar.
- properties: `name`, `year_formed` (varsa), `source_title`, `source_url`, `coord_source` (`paper table` / `official` / `wikipedia` / ...)
- Öncelik: hakemli makale, AFAD, MTA, üniversite.
- **Koordinatı tahmin etme.** En az 5, ideal 10+. Bulamadığın sayıyı status'a yaz, uydurma.

**Bitti sayılır eğer:** geojson geçerli (geojson.io'da açılıyor), her noktanın `source_url`'si açılıyor ve o obruğu anlatıyor.

## Görev 3 · Kaynak listesi ve kalibrasyon notu (15:30-17:00)

`docs/story/sources.md`: her kaynak için başlık, link, 1 cümle bulgu, varsa sayı (birimiyle).
- Holme Fen direği: ne zaman dikildi, zemin ne kadar alçaldı
- Central Valley çökmesi (NASA/JPL, USGS) · Sacramento Delta setleri
- Karapınar/Konya çökme ve obruklar
- UK kil şişme-büzülme (BGS)
- NISAR görevi (nasa.gov / jpl.nasa.gov) · NISAR veri sürümleri ve kalibrasyon durumu (ASF NISAR Data User Guide)

`docs/story/calibration_note.md`: ASF/JPL ürün notlarına göre 2026-06-17 öncesi ürünlerin durumu (beta / pre-calibration), kısa ve kaynaklı.

**Bitti sayılır eğer:** her satırın linki açıldı ve sayı sayfada geçiyor.

---

## En kritik iş
Doğrulanmış kaynak. Jüri tek bir uydurma sayı yakalarsa tüm projenin Validity puanı düşer.

## B planı
- Bulutlu gün + GCOV eşleşmesi bulunamazsa: en yakın iki gün (±1 gün), `note` alanına farkı yaz.
- 5 kaynaklı obruk bulunamazsa: bulunanları koy, eksik sayıyı status'a yaz. Uydurma yok.

## Yapma
- `data/karapinar/` klasörünü silme/temizleme. Başka dosyaya yazma.

## Rapor
`status/PC4.md`: ne bitti, hangi kaynaklar, doğrulanamayanlar, `AI:` satırı.

---
# 14:10 YENİ PAKET (öncelik sırası; harika iş çıkardın — devam)
1. **Q30** sayı eşleme (pitch.md, project_page.md ↔ data/*/summary.json).
2. **Q31** Holme Fen tek cümle + kaynak → `docs/story/holme_fen.md`.
3. **Jüri soru-cevap kartı** → `docs/story/judge_faq.md`: en olası 15 soru (kalibrasyon? LOS/dikey? atmosfer/iyonosfer? 108 günden yıllık hız? neden Central Valley? Karapınar'da obrukları NISAR öngörebilir mi? GNSS ile uyum? veri açık mı? AI kullanımı? …) — her biri 2–3 cümle İngilizce, kaynaklı, repodaki gerçek sayılarla.
4. **Slaytlar (≤7)** → `docs/story/slides.html` (tek dosya, gerçek ekran görüntüleri ve grafikler; AI görseli yok; tıklayınca ilerleyen). İçerik: pitch.md'den.
5. **30 sn video çekim listesi** → `docs/story/video_shotlist.md`: siteden hangi ekran kaydı, kaç saniye, altyazı metni (İngilizce), sıra. (Kaydı Kerem/PC1 yapacak.)
6. **Son İngilizce okuma**: `web/index.html` metinleri için düzeltme önerilerini `docs/qa/PC4.md`'ye yaz (web/ dosyasına dokunma, PC1 uygular).

---
# 15:00 YENİ PAKET — "NASA makalesi" dili (öncelik sırası)
1. `docs/REVIEW_1500.md` yazım kurallarını oku. `web/index.html`, `science.html`, `data.html`, `faq.html` metinlerini satır satır gözden geçir; her değişiklik için "eski → yeni" önerisini `docs/qa/PC4.md`'ye yaz (PC1 uygular; web/ dosyalarına DOKUNMA). Başlıkları olgusal yap, abartıyı ve AI kokan kelimeleri ayıkla, figür kredilerini öner.
2. Aynı kuralları kendi dosyalarına uygula: `pitch.md`, `project_page.md`, `judge_faq.md`, `slides.html` (FAQ sitede birebir gösteriliyor — iç not/"Usage" blokları kaldır, sadece soru-cevap kalsın).
3. `slides.html`: PC6'nın `docs/story/media/` gerçek veri görselleri geldikçe slaytlara yerleştir; AI görseli kullanma; her görselde kaynak satırı.
4. `video_shotlist.md`: yeni site bölümlerine (Story 1–6, Simulator, Science) göre güncelle.

---
# 16:15 CHALLENGE UYUMU (docs/CHALLENGE_UYUM.md) — acil sunum kartlarından SONRA, sırayla
1. **A5** `docs/story/audiences.md`: 5 kitle (scientists, water & canal managers, educators, decision-makers, public) için her biri 2 cümle: ne bulur, ne yapabilir. Somut ve kaynaklı.
2. **A13** `docs/story/future_applications.md`: NISAR'ın gelecekteki uygulamaları — kanal/set erken uyarısı, obruk izleme, yeraltı suyu yönetimi (California SGMA gibi), tam yıllık seriyle kalıcı kaybın izlenmesi, küresel şehirler. Kaynak: NISAR Applications White Papers (https://nisar.jpl.nasa.gov/applications/societal-benefit/), Handbook §2.4. 6–8 madde, sade.
3. **A7/B6** `docs/story/team_story.md`: "Why Konya matters to us" taslağı (Ankara'daki ekip, Konya Ovası'nın Türkiye tarımındaki yeri, obrukların haberlerde olması — kaynaklı). En üste: "TASLAK — ekip kendi cümleleriyle düzeltecek". Uydurma kişisel anı YAZMA.
4. **A5** `docs/story/lesson_plan.md`: eğitimciler için 40 dk ders planı (lise): hedefler, simülatörle etkinlik, 5 soru, cevap anahtarı.
5. **C** `sources.md` + "Learn more" listesi: challenge Resources sekmesindeki bağlantıların hepsi (NISAR Data User Guide, Intro to SAR, ARSET, NISAR StoryMaps, Applications White Papers, UAVSAR Postcards, Earthdata Search, Vertex) — her biri 1 cümle açıklama, linkler açılarak doğrulanmış.
6. `project_page.md` ve `pitch.md`'yi challenge metnindeki anahtar ifadelere göre hizala: "interactive application", "track and visualize surface change", "actionable insights", "patterns and rhythms", "physical drivers", "future applications".

> **16:25 PC1 — KAYNAKLAR ENTEGRASYONU:** `docs/KAYNAKLAR_ANALIZI.md`'yi oku; §4'te senin satırındaki işleri mevcut işine ek olarak yap (özellikle §1 NASA Land Subsidence StoryMap çerçevesi). Kendi cümlenle özetle, link ve atıf ver.

> **18:55 PC1:** Lincoln geçti. `docs/AKSAM_PLANI.md`'deki kendi satırına geç (akşam → Pazar). Durma.

> **19:45 PC1 — TEK SIRA ARTIK BURASI:** `docs/CALISMA_HARITASI.md` içindeki kendi bölümün. Yukarıdan aşağı yap, bitince "ASLA BOŞ KALMA" döngüsü. Teslime kadar durma.

---
# 20:00 PC1 — SIRA (3 saattir commit yok; teslime kadar bu sırayla, durmadan)
1. `docs/story/project_page.md` son hâl: tüm yeni sonuçlar (tam yıl −20.3 cm / 11 ay "mixed", Delta, Konya Ovası, Mexico City + Tahran + Cakarta + Pekin, C-band karşılaştırması, maruziyet, İngiltere "below detection"); challenge ifadeleri ("interactive application", "track and visualize surface change", "actionable insights", "patterns and rhythms", "physical drivers", "future applications"). Sayılar sadece `data/*/summary.json` vb.
2. `docs/story/slides.html` — teslimde video YERİNE kullanılacak (video durduruldu): tam 7 slayt, her slayt tek mesaj + gerçek görsel + kaynak satırı; tarayıcıdan PDF'ye yazdırınca düzgün (yazdırma CSS'i); son slaytta site ve repo linki.
3. `docs/story/judge_faq.md`: yeni 5 soru (tam yılda neden beta veri var, Delta, küresel şehirler, C-band ile fark, maruziyet tahmininin sınırları).
4. `docs/story/team_story.md`: ekiple birlikte gerçek cümlelerle son hâl (ekip yazmazsa TASLAK etiketi kalsın).
5. Tüm `docs/story/*.md` İngilizce son okuma (REVIEW_1500); kendi dosyalarını düzelt, diğerlerini `docs/qa/PC4.md`'ye yaz.
6. Sonra "ASLA BOŞ KALMA" döngüsü.

---
# 20:10 PC1 — TEKNİK NOT (sahibi sensin; `docs/OZGUN_KATKILAR.md` §T) — 20:00 madde 1–2'den sonra
`docs/story/technical_note.md` + yazdırılabilir `docs/story/technical_note.html` (tek dosya, A4 yazdırma CSS'i):
NASA teknik rapor tarzı, 4–6 sayfa: Abstract (150 kelime) · 1 Data (ürünler, tarihler, kalite sınıfları) · 2 Methods (faz→cm, düzeltmeler, zincir, ayrıştırma) · 3 Validation (10 GPS, ikinci geçiş p114, C-band OPERA) · 4 Uncertainty (piksel σ, referans duyarlılığı, atmosfer) · 5 Results (108 gün, tam yıl, Delta, Konya, küresel) · 6 Original contributions (O1 depolama kaybı, O2 olasılıksal mühendislik riski, O3 NISAR Vision aracı) · 7 Limitations · References (hepsi doğrulanmış link).
Her sayı `data/*` dosyasından; O1/O2/O3 sonuçları gelmeden önce yerlerine "[pending PC8/PC7/PC2]" yaz, gelince doldur. `slides.html`'e 1 slayt: "What is new in our work" (O1–O3).
Yazma alanına eklendi: `docs/story/technical_note.md`, `docs/story/technical_note.html`.

---
# 20:50 PC1 — BÜYÜK GÖREV: `docs/ATLAS_PLANI.md`
Şu anki küçük işini bitir, sonra SORMADAN `docs/ATLAS_PLANI.md` içindeki kendi bölümüne geç ve yukarıdan aşağı yap. Teslime kadar durma; bitince ASLA BOŞ KALMA döngüsü (hata ayıklama dahil).

## 🔴 YENİ (Cmt 22:15, PC1) — Atlas ikinci tur
`docs/ATLAS_PLANI.md` → "PC4 — anlatım" altında **madde 5–9**: şehir kartları (`docs/story/atlas_cities/<id>.md`), `atlas_methods.md`, `atlas_data_dictionary.md`, judge_faq atlas zor soruları, yeni şehir senkronu.
Yazma alanın genişledi: `docs/story/atlas_cities/` · `docs/story/atlas_methods.md` · `docs/story/atlas_data_dictionary.md`. REVIEW_1500 dili, her sayı kaynaklı, PC5 onayı olmayan sayı "preliminary". Her dosyada commit + push. Teslime kadar durma.


# 🌍 ATLAS FİNAL — PC4 (Paz 00:20, PC1) · plan: `docs/ATLAS_FINAL.md`
1. **NASA Earth Observatory "Image of the Day" tarzı öne çıkan hikâye:** `docs/story/atlas_feature.md` — "Where the ground is sinking fastest in 2026", 3 paragraf, ilk 3 şehrin açıklamalı görseli, kaynak satırı; sade İngilizce ≤450 kelime; PC5 onaylı sayılar.
2. **Veri atıfları:** `docs/story/sources.md`'ye NISAR GUNW (ASF DAAC önerilen biçim), OPERA DISP-S1, Copernicus DEM, GHSL, OSM, NGL GNSS; DOI veya kalıcı link.
3. Atlas 20+ şehre çıktıkça press_summary, slides atlas slaytı, technical_note §5.1, şehir kartları senkron; Tahran/Pekin düzeltmesi gelince eski −3.5/−1.4 her yerde güncellenir (o zamana kadar "under revision").


# ♻️ SÜREKLİ KURAL (Paz 00:45, PC1)
`tasks/SUREKLI.md` zorunlu: **her 3 dakikada bir** commit → pull --rebase → push, bu dosyanın sonuna yeni bölüm var mı bak, status tek satır. Asla durma; listen biterse SUREKLI.md tablosundaki kendi sürekli işin.

# ➕ TAKVİYE (Paz 01:45, PC1 otomatik kontrol) — 61 dk sessizdin
1. **Yeni şehirleri senkronla:** atlas 14 şehre çıktı (Semarang −11.2 cm/100d 1. sıra, Mashhad, Quetta yolda). press_summary, slides atlas slaytı, technical_note §5.1, `atlas_feature.md` ilk 3'ü güncel atlas.json'a göre; Tahran/Pekin "under revision".
2. **Şehir kartı eksikleri:** `docs/story/atlas_cities/` içinde semarang, mashhad, quetta, isfahan, rafsanjan kartları (kaynaklı, ≤150 kelime).
3. **NISAR 3D görünümü anlatımı:** atlas sayfasına eklenen "NISAR 3D orbit" (gerçek CelesTrak TLE + SGP4, sol bakışlı 33–47° swath, sonraki gerçek geçiş) için `docs/story/presentation_cues.md`'ye 20 sn'lik sunum cümlesi ve `judge_faq.md`'ye 2 soru ("Uydu konumu gerçek mi?", "Model neden büyük çizildi?"). Kaynak: `data/nisar_tle.json`.
4. Sonra SUREKLI.md döngüsü (3 dk).


# ⭐ ATLAS KUSURSUZLUK (Paz 01:00, PC1) · `docs/ATLAS_MUKEMMEL.md`
1. `docs/qa/ATLAS_COMPLETENESS.md`'de (PC8) şehir kartı ✗ olan her şehir için kart yaz (semarang, mashhad, quetta, rafsanjan, ho_chi_minh dahil).
2. Atlas metinleri: 1. sıra Semarang; Tahran/Pekin "under revision".


# ➕ TAKVİYE (Paz 01:40, PC1) · tablo: `docs/qa/ATLAS_COMPLETENESS.md` (`python tools/atlas_completeness.py`)
1. **Eksiklerin:** `docs/story/atlas_cities/semarang.md`, `hanoi.md`; ardından eloy, quetta, xian kartları (kaynaklı, ≤150 kelime).
2. 82 dk commit yoktu — her 3 dk ara commit.


# 📣 GENEL EMİR (Paz 01:50, PC1) — HERKES, HEMEN
1. Elindeki işi bırakmadan **şu an yaptığın her şeyi commit et ve pushla** (yarım iş de olsa ara kayıt: `[PC4] ara kayit: <ne>`). `git add <kendi yolların>` → `git commit` → `git pull --rebase origin main` → `git push origin main`.
2. `status/PC4.md`'ye tek satır yaz: ne yapıyorsun, % kaç bitti, sıradaki ne.
3. Bundan sonra **en geç 10 dakikada bir** commit + push; 10 dk'dan uzun commit'siz kalma (uzun indirmede her çift bitince ara kayıt).
4. Sonra bu dosyadaki en son TAKVİYE / KUSURSUZLUK bölümünden devam et.


# 🔬 PC1 BAĞIMSIZ KONTROL SONUCU (Paz 02:55) · `docs/story/atlas_top5_check.md`
Atlas metinleri: 1. sıra artık **Konya Ovası** (dikkat notuyla); Semarang başlıktan çıktı (faz açma hatası şüphesi), Bangkok/Delhi/Pekin indicative. `docs/story/atlas_top5_check.md`'yi press_summary, slides ve technical_note'a kaynak olarak bağla.


# 🔄 YENİ ATAMA (Paz 03:05, PC1) — atlas 19 bölge, QC sonrası sıralama: 1 Konya Ovası, 2 Mashhad, 3 Central Valley, 4 Eloy, 5 Mexico City (`docs/story/atlas_top5_check.md`). Tamlık 100/114.
PC5 (baş bilimci) 2 saattir durmuş; teslim belgelerinin bilimsel tutarlılığı artık **senin sorumluluğunda**. Sırayla:
1. **Doğrulama notları (7 şehir):** `data/global/{semarang,mashhad,eloy,delhi,quetta,hanoi,xian}/validation_note.json` — mevcut notların biçiminde (örn. `data/global/rafsanjan/validation_note.json`): atlas değeri, dönem, yayımlanmış hız + DOI/kalıcı link, uyum notu, önerilen güven, `"reviewed_by": "pending PC5"`. Semarang/Delhi/Bangkok/Pekin için `data/global/qc_flags.json` gerekçesini nota ekle. Kaynak bulamazsan "no published rate found". (Belirsizlik haritaları şehri işleyen ajanlarda; sen sadece notları yaz.)
2. **Sayı senkronu:** `python analysis/pc5/numbers_registry.py` çalışıyorsa çalıştır; tüm `docs/story/*.md`, `slides.html`, `technical_note.*`, `press_summary.md`, `submission_form.md` içinde eski sıralama/değer kalmasın: Semarang artık 1. değil (faz açma hatası şüphesi, indicative), Tahran −7.4 cm, 1. sıra Konya Ovası (dikkat notuyla). Uyumsuzlukları kendi dosyalarında düzelt, başkalarınınkini `docs/qa/PC4.md`'ye yaz.
3. **Jüri hikâyesi — kendi hatamızı yakaladık:** `judge_faq.md`'ye "How do you know your ranking is right?" sorusu: zaman serisi QC (faz döngüsü sıçraması 12.1 cm, tek tarih aykırı), Semarang örneği, literatür kıyası. `slides.html`'de atlas slaytına tek satır "Quality-controlled: 4 regions flagged and moved to indicative". Sunum notlarına (`presentation_cues.md`) 15 sn'lik cümle.
4. **`docs/qa/SCIENCE_SIGNOFF.md` taslağı (Paz 19:00 hedef):** teslimde kullanılacak 10 başlık sayısı (değer, belirsizlik, kalite etiketi, kaynak dosya:anahtar), bilinen sınırlamalar (LOS, provisional, 108–120 gün yaz, iyonosfer düzeltmesi uygulanmadı), kalibrasyon cümlesi, "to our knowledge" ifadelerinin dayanağı. Başlık: "DRAFT by PC4 — PC1 review". 
En geç 10 dakikada bir commit + push. Sonra SUREKLI döngü.


# 🔗 ENTEGRASYON (Paz 03:20, PC1) · `docs/ENTEGRASYON.md`
**Sitede görünür yap:** `data/results_registry.json`'da senin satırların: `atlas_feature`, `calibration`, `technical_note`. Her birine `summary` (tek sade cümle) ve `key_number` (birim + kalite etiketi, kendi veri dosyandan) yaz, `status: ready`. Yeni sonuç üretince yeni satır ekle (aynı alanlar). Sayı uydurma yok; PC4 sayı siciliyle aynı olmalı.

Ayrıca kayıttaki tüm `summary` cümlelerini en sonda REVIEW_1500'e göre tek elden düzelt (sahibinin yazdığını sadeleştir, sayıları değiştirme).


# ➕ TAKVİYE (Paz 03:50, PC1 otomatik kontrol) — atlas 21 bölge, tamlık 122/126
PC5 durduğu için `data/results_registry.json`'da PC5 satırlarının özetlerini de sen doldur: **atlas_validation, detectability, cross_sensor, drivers, sinkholes, uncertainty** — tek sade cümle + anahtar sayı, ilgili md/json dosyasından aynen (sayı uydurma yok). Sonra SCIENCE_SIGNOFF taslağına devam.


# ⏱️ 8 SAATLİK PLAN (Paz 04:15 → 12:15, PC1) — sonra 20:00 veri dondurmaya kadar SUREKLI
Bu bölüm, önceki bölümlerde bitmemiş işleri de kapsar ve geçerli olan TEK listedir. Blokları sırayla yap; bir blok erken biterse sıradakine geç. Her blok sonunda commit + push + status satırı. En geç 10 dk'da bir commit.
| Saat | Blok | Çıktı |
|---|---|---|
| 04:15–05:30 | **results_registry özetleri:** PC5 satırları (atlas_validation, detectability, cross_sensor, drivers, sinkholes, uncertainty) + tüm satırları REVIEW_1500 ile tek elden sadeleştir (sayıları değiştirme) | `data/results_registry.json` |
| 05:30–07:30 | **Teknik not son sürüm:** atlas v2 (ortak 93 günlük pencere, belirsizlik, QC, değişiklik günlüğü), OPERA açıklaması (PC2), bağımsız kontrol (`atlas_top5_check.md`); `technical_note.html` yazdırılabilir; sayılar atlas.json'dan | `technical_note.md/html` |
| 07:30–09:00 | **Slaytlar son hâl (≤7)** + konuşmacı notları; 3 dk konuşma metni (`presentation_cues.md`) atlas + "kendi hatamızı yakaladık" hikâyesiyle; prova kontrol listesi güncel | `slides.html`, `presentation_cues.md`, `rehearsal_checklist.md` |
| 09:00–10:30 | **Jüri SSS — 30 soru:** bilim (LOS, provisional, 108 gün, iyonosfer), atlas (ortak pencere, QC, OPERA uyumsuzluğu), etki (nüfus, altyapı), ekip/AI kullanımı | `judge_faq.md` |
| 10:30–12:15 | **`docs/qa/SCIENCE_SIGNOFF.md` taslağını tamamla:** 10 başlık sayısı (değer, belirsizlik, kalite, kaynak dosya:anahtar), sınırlamalar, kalibrasyon cümlesi; PC1 onayına hazır | SIGNOFF |
| 12:15–20:00 | SUREKLI: tüm `docs/story/*.md` son dil okuması; site metinlerindeki sorunları `docs/qa/PC4.md`'ye (PC6 düzeltir); PC9 yıllıklaştırma gelince metinlere ekle | — |


# 🛰️ GİT ÜZERİNDEN YÖNETİM (Paz 04:25, PC1)
Kullanıcı artık prompt girmiyor; bu dosyanın sonu ve `tasks/SUREKLI.md` senin tek emir kaynağın. 8 saatlik planın biterse `tasks/BACKLOG_ORTAK.md`'den satır al (`[~PCx]` → commit+push → yap → `[x PCx]`). Onay bekleme, soru sorma; karar gerektiren durumda en makul seçeneği uygula ve gerekçesini `docs/qa/PCx.md`'ye yaz.


# ⏳ PLAN SONU SİNYALİ (Paz 04:35, PC1)
Son bloğa geldiğinde `status/PC4.md` ilk satırına `PLAN_SONU_YAKIN` yaz, pushla. PC1 20 dk içinde bu dosyanın sonuna yeni 6–8 saatlik plan ekler; o arada `tasks/BACKLOG_ORTAK.md`. Teslime (Paz 22:00) kadar durmak yok.


# ▶ DEVAM (PC1 otomatik kontrol, Paz kontrol 1)
48 dk commit yok. 8 SAATLİK PLAN'da kaldığın bloktan devam et; uzun iş sürüyorsa ara kayıt commit'i at ve `status/PC4.md`'ye hangi blokta olduğunu yaz. Planın son bloğundaysan ilk satıra `PLAN_SONU_YAKIN` yaz.


# ⛔ DURMUŞ SAYILDI (PC1 otomatik kontrol 2)
60 dk'dan uzun commit yok; kritik işlerin PC10 (results_registry) ve PC7 (teknik not, slayt) tarafına devredildi. Dönersen `tasks/BACKLOG_ORTAK.md`'de `[ ]` kalan kendi işlerini geri al (`[~PC4]`), başkasının aldığına dokunma.

# 🚀 YENİ PLAN — PC4 (PC1, Paz 09:30 TR) · tekrar hoş geldin; son 15 dk'daki işlerin çok iyi (SSS 30, teslim paketi, literatür tablosu, sıralama kıyası)
Şu an çalışan tek ajan sensin: teslim belgelerinin son hâli sende. Bloklar sırayla; her blok sonunda commit + push, status satırı. Atlas sayıları için `python tools/sync_atlas_text.py` (teknik not tablosunu ve bölge sayılarını atlas.json'dan günceller) — elle sayı yazma.

| Saat (TR) | Blok | Çıktı |
|---|---|---|
| 09:30–11:00 | **Sunum paketi son hâli:** `slides.html` (≤7 slayt; atlas slaytında 29 bölge / 16 güvenilir, QC hikâyesi tek cümle, Konya caution notu), `presentation_cues.md` 3 dk konuşma metni (Kerem anlatır; açılış → atlas → "kendi hatamızı yakaladık" → Central Valley GNSS → etki → kapanış), `rehearsal_checklist.md` güncel | slides, cues, checklist |
| 11:00–12:00 | **60 sn yedek demo senaryosu:** `docs/story/demo_script_v3.md` — gerçek siteden ekran kaydı adımları (ana sayfa → atlas → Konya paneli → Results → simülatör), her adımın süresi ve altyazısı; AI görseli yok (BACKLOG §C) | demo_script_v3.md |
| 12:00–13:00 | **Atlas okuma rehberi + sayfa başlıkları:** atlas sayfasına 4 adımlık "How to read this map" kutusu (LOS, renk ölçeği, güven rozeti, indicative) — `web/atlas.html` içinde yalnız bu kutu; tüm sayfaların `<title>`/`<meta name="description">` güncel atlas sonuçlarıyla (BACKLOG §C). NISAR 3D dosyalarına dokunma. | web değişiklikleri, `docs/qa/PC4.md` |
| 13:00–14:30 | **Teknik not son okuma:** `technical_note.md/.html` — Konya tam yıl arşiv boşluğu (Şub–Haz 2026, `data/konya_plain_fullyear/summary.json`), Pekin tam kutu sonucu ve 11 Temmuz aykırısı, bağımsız doğrulama kuralı (`data/global/independent_validation.json`), sınırlamalar; özet paragrafı tek sayfa | technical_note |
| 14:30–15:30 | **"Neden çöküyor" paragrafları:** güvenilir 16 bölgenin şehir kartlarına kaynaklı 1 paragraf (yeraltı suyu / kil / tarım), `literature_rates.json` kaynaklarıyla (BACKLOG §B) | atlas_cities/*.md |
| 15:30–17:00 | **Basın özeti + proje sayfası + teslim formu son okuma:** sayıların `SCIENCE_SIGNOFF.md` ile aynı olduğunu satır satır kontrol et; karakter sınırları; AI kullanım beyanı | press_summary, project_page, submission_form |
| 17:00–18:30 | **REVIEW_1500 son dil geçişi:** tüm `docs/story/*.md` + site metinleri; bulguları kendi dosyalarında düzelt, web'de küçük metin düzeltmeleri | `docs/qa/PC4.md` FINAL |
| 18:30–19:30 | **SCIENCE_SIGNOFF son kontrol (PC1 ile):** atlas son hâliyle 10 satırı yeniden doğrula; 20:00 veri dondurma | SIGNOFF |
Son bloğa gelince `status/PC4.md` ilk satırına `PLAN_SONU_YAKIN`.


# ▶ DEVAM (PC1 otomatik kontrol)
35 dk commit yok. Blok 4 (teknik not son okuma) uzunsa bolum bolum ara commit at; status a blok yaz. Atlas sayilari icin: python tools/sync_atlas_text.py

# 🚀 YENİ PLAN 2 — PC4 (PC1, Paz 10:30 TR) · 8 bloğu 50 dakikada bitirdin, mükemmel
Durmuş PC6'nın (site) ve havuzun indirme gerektirmeyen işleri. Sırayla; her blok sonunda commit + push + status. Web dosyalarında NISAR 3D (`nisar3d.js`, `atlas_sat.*`) dosyalarına dokunma. Her web değişikliğinden sonra yerel test: `python -m http.server 8765` → ilgili sayfa, konsol 0 hata.

| Saat (TR) | Blok | Çıktı |
|---|---|---|
| 10:30–12:00 | **Sunum modu (Lincoln demosu):** `web/present.html` — tam ekran, ok tuşlarıyla 6 durak: ana sayfa özeti → atlas (sıralama) → Konya paneli → "kendi hatamızı yakaladık" (QC, Semarang) → Results kartları → simülatör; her durakta büyük tek cümle + kaynak; internet yokken de açılır (yerel dosyalar). `presentation_cues.md`'ye bağlantı | present.html |
| 12:00–13:30 | **Oyun ↔ atlas** (`tasks/PC6.md` "OYUN ↔ ATLAS" 1–3): oyundaki Konya kartına "Karapınar sub-basin" adı + "Atlas: Konya Plain (rank 1) →" bağlantısı; atlas panelinde central_valley / konya_plain / karapinar için "Manage this valley in the simulator" → `game/?basin=...`; oyun `?basin=` okusun. `game/test_model.html` 6/6 kalmalı | game + atlas |
| 13:30–14:30 | **"What changed" kutusu + hata çubukları:** atlas sayfasında `data/global/atlas_changelog.json`'dan son 10 değişiklik; sıralama tablosunda `rate_ci_cm_per_100d` varsa aralık; başlıkta "ranked by common 93-day window" | atlas |
| 14:30–16:00 | **Bağımsız kontrolü 6–16. sıralara genişlet:** `docs/story/atlas_rank_check_6_16.md` — her güvenilir bölge için bizim değer vs `literature_rates.json` (büyüklük mertebesi), zaman serisi QC sonucu, karar (tutarlı / dikkat / şüpheli); şüpheli varsa `data/global/qc_manual.json`'a gerekçe+kaynakla ekleme önerisini `docs/qa/PC4.md`'ye yaz (PC1 uygular) | rank_check md |
| 16:00–17:00 | **Otomatik tutarlılık testleri:** `tests/test_site_numbers.py` — ana sayfa / atlas / vital_signs sayıları atlas.json ile aynı mı (pytest); `tools/vital_signs.py` — vital_signs.json'u atlas.json + exposure_atlas.json'dan üretir (fastest = güvenilir bölgelerden) | test + betik |
| 17:00–18:15 | **Site son QA:** tüm sayfalar (index, atlas, science, data, faq, game, present) konsol 0 hata, kırık link 0, mobil 375 px, projektör 1920; bulgular + düzeltmeler `docs/qa/PC4.md` FINAL | QA |
| 18:30–19:30 | **SIGNOFF son tur (PC1 ile):** atlas son hâliyle yeniden doğrula; `python tools/sync_atlas_text.py`; 20:00 veri dondurma — sonrasında yalnız hata düzeltme | SIGNOFF |
Son bloğa gelince `status/PC4.md` ilk satırına yine `PLAN_SONU_YAKIN`.

# 🚀 YENİ PLAN 3 — PC4 (PC1, Paz 10:50 TR) · Plan 2 de bitti ve PC1 test etti: present.html 6 durak, konsol 0 hata; pytest 97/97 — teşekkürler
| Saat (TR) | Blok | Çıktı |
|---|---|---|
| 10:50–12:00 | **Jüri için depo README'si:** kök `README.md` — tek paragraf özet, ana sonuçlar (SIGNOFF'taki 10 sayı), siteye/atlasa/sunum moduna bağlantılar, "atlası tek komutla yeniden üret" (`python pipeline/pc10/build_atlas.py`, `python tools/atlas_qc.py`, `python tools/sync_atlas_text.py`), veri kaynakları ve lisanslar, AI kullanım beyanı, klasör haritası | README.md |
| 12:00–13:00 | **Atlas veri sözleşmesi:** `data/global/atlas.schema.json` (JSON Schema; her alan, birim, zorunlu/opsiyonel) + `tests/test_atlas_schema.py` (pytest); `atlas_data_dictionary.md` ile tutarlı | şema + test |
| 13:00–14:30 | **Nüfus etkisi eksikleri (8 bölge):** `docs/qa/ATLAS_COMPLETENESS.md`'de 6. sütun ✗ olan bölgeler için GHSL GHS-POP (JRC açık veri, giriş gerekmez) ile `exposure_atlas.json` satırı — mevcut satırların yöntemiyle (σ'nın 2 katından küçük çökme sayılmaz). İndirme mümkün değilse yöntemi ve listeyi `docs/qa/PC4.md`'ye yaz, geç | exposure_atlas.json |
| 14:30–15:30 | **Sonuç kaydı yeni satırlar:** `results_registry.json`'a `presentation_mode`, `simulator`, `rank_check_6_16`, `literature_atlas`, `submission_package` (özet + anahtar sayı); science sayfasında göründüğünü test et | registry |
| 15:30–16:30 | **Erişilebilirlik:** atlas, present, index, science — alt metin, klavye ile gezinme, kontrast; bulgu + düzeltme | web, `docs/qa/PC4.md` |
| 16:30–17:30 | **Soru-cevap kartları + zamanlı prova:** `docs/story/qa_cards.md` (yazdırılabilir tek sayfa, en olası 12 jüri sorusu ve 2 cümlelik cevaplar); `present.html` ile 3 dk zamanlı prova notları | qa_cards.md |
| 17:30–18:30 | **Sürüm notları ve dondurma listesi:** `docs/RELEASE_NOTES.md` (neler var, bilinen sınırlamalar, değişiklik günlüğü özeti) + 20:00 dondurma kontrol listesi | RELEASE_NOTES.md |
| 18:30–19:30 | **SIGNOFF son tur (PC1 ile)**; `python tools/sync_atlas_text.py`; 20:00'dan sonra yalnız hata düzeltme | SIGNOFF |
Son bloğa gelince `status/PC4.md` ilk satırına `PLAN_SONU_YAKIN`.


# 🏁 FİNAL — TOPLAMA VE BİRLEŞTİRME (PC1, Paz 11:15 TR) · önce `docs/JURI_3DK.md`'yi oku
Jüri siteyi 3 dakika inceleyecek. Yeni veri/özellik yok; toparla, sadeleştir, tutarlı yap. Ana sayfayı PC1 kuruyor. Bu bölüm önceki tüm planların ÜSTÜNDEDİR. Her blok sonunda commit + push (önce kendi dosyaların → pull --rebase → push), status satırı. Veri dondurma 20:00, teslim 22:00.
**Rol: 3 dakikalık metin.** (Önceki Plan 3'ten README ve soru-cevap kartları bloklarını koru, diğerlerini bu listeyle değiştir.)
1. (11:15–12:30) **`docs/story/three_minute_story.md`:** JURI_3DK'daki 6 bölümün her biri için: başlık (≤8 kelime), tek cümle (≤25 kelime), büyük sayı + birim + kalite etiketi + kaynak dosya:anahtar, görsel önerisi, bağlantı. Dil sade İngilizce; LOS gibi terimleri bir kelimeyle açıkla. PC1 ana sayfayı bundan kuracak — **PC1 için önce bunu bitir.**
2. (12:30–13:30) **Kök `README.md`** (Plan 3 blok 1) — tek cümlelik özümüzle başlasın.
3. (13:30–15:00) **Slayt ve konuşma metnini 3 dk akışına hizala:** `slides.html` (6 slayt = 6 bölüm), `presentation_cues.md` süreleriyle; `present.html` duraklarının metinleri aynı cümleler (web dosyasında yalnız metin).
4. (15:00–16:00) **Soru-cevap kartları** (`qa_cards.md`, 12 soru, 2 cümle cevap).
5. (16:00–18:00) **Kesip atma:** `docs/story/*.md` içinde ana hikâyeyle çelişen/eski sayı içeren cümleleri bul (`python tools/sync_atlas_text.py` + elle); proje sayfası ve teslim formunun ilk paragrafı tek cümlelik özle aynı.
6. (18:30–19:30) SIGNOFF son tur (PC1 ile).


# ℹ️ FİNAL güncelleme (PC1)
Ana sayfanın 3 dakikalık bölümleri PC1 tarafından kuruldu (`web/index.html` üst kısım, `web/home3.js`, sayılar `data/global/home_summary.json`). FİNAL madde 1'i şöyle yap: `three_minute_story.md`'yi **ana sayfadaki mevcut metinden** çıkar, her cümleyi REVIEW_1500 ve kaynaklarla kontrol et; düzeltme önerilerini `docs/qa/PC4.md`'ye yaz (PC1 uygular) veya yalnız metin düzeltmesini doğrudan `web/index.html`'de yap (sayılara dokunma — sayılar JS ile `home_summary.json`'dan geliyor). `slides.html` ve `present.html` aynı 6 bölümü aynı cümlelerle anlatsın.


# ⚠️ PC1 DÜZELTME (OPERA iddiası) — ÖNCELİKLİ
Mexico City OPERA kıyası (r = 0.912) **10 noktaya** dayanıyor ve dönemler FARKLI: OPERA 2025-12-25 → 2026-03-25 (kış), NISAR 2026-06-22 → 2026-10-20 (yaz); eğim 1.28, sabit fark +5.65 cm/100d (`data/global/opera_check.json`, `docs/story/media/pc2_opera_mexico_city.png`). Bu yüzden **manşet/ana sayı olarak kullanma** — ana sayfadan PC1 çıkardı.
Şu dosyalarda "same summer season one year earlier" veya manşet r = 0.91 geçen yerleri düzelt: `three_minute_story.md`, `slides.html`, `present.html`, `judge_brief.html`, `press_summary.md`, `submission_form.md`, `README.md`.
Doğru ifade: *Over Mexico City the spatial pattern matches NASA JPL's OPERA product at 10 points (r = 0.91), although OPERA covers winter and NISAR summer; in the Central Valley and at Eloy the agreement is weak (r = 0.40 and 0.09) because seasons and viewing geometry differ.* Ana doğrulama: GPS r = 0.924.


# 🏁 SON PLAN — PC4 (PC1, Paz 12:00 → 20:00) · ana sayfa artık "giriş + 9 numaralı bölüm" (web/index.html)
| Saat | Blok |
|---|---|
| 12:00–13:00 | **OPERA düzeltmesi (yukarıdaki PC1 DÜZELTME notu):** present.html, three_minute_story.md, judge_brief.html, submission_form.md (+ README, slides, press_summary varsa) |
| 13:00–14:30 | **Sunum = ana sayfa:** `present.html` ve `slides.html` duraklarını ana sayfanın akışına hizala (giriş/atlas → 2 kendi hatamızı yakaladık → 3 GPS → 4–5 kişi ve kalıcı su kaybı → 6–7 altyapı ve bülten → 8–9 simülatör ve açık motor); aynı cümleler, aynı sayılar (`home_summary.json`) |
| 14:30–16:00 | **Science ve Data sayfaları eski bilgi taraması:** 1.48 M, 21/19 bölge, "same season", Semarang −12.1 gibi eski ifadeler; metin düzeltmesi yap (sayılar atlas/home_summary ile) |
| 16:00–17:30 | **README son okuma** (tek cümlelik öz, 9 iş listesi, nasıl çalıştırılır) + `qa_cards.md` son hâl |
| 17:30–19:00 | Zamanlı prova notları (3 dk, present.html), son dil geçişi |
| 19:00–19:30 | SIGNOFF son tur (PC1 ile); 20:00 dondurma |

# ▶ PC1 NOT — Science sayfası eski sayı
`web/science.html` kartında "3 of 21 regions flagged" yazıyor → güncel: **5 of 29** (atlas.json / qc_flags.json). 14:30–16:00 eski bilgi taramasında öncelikli.


# ℹ️ PC1 (12:15)
`status/PC4.md` başındaki `PLAN_SONU_YAKIN` artık eski: 12:00–20:00 SON PLAN'ındasın (sıradaki blok: sunum = ana sayfa hizalaması). Başlığı sil, bloklara devam et.


# 🆕 YENİ PLAN — PC4 (PC1, Paz 12:30 → 20:00) · "yeni görev yok" deme: aşağıdakiler senin
| Saat | Blok | Çıktı |
|---|---|---|
| 12:30–14:00 | **present.html = ana sayfanın 9 işi:** 6 durağı ana sayfa sırasına çevir (giriş/atlas → 02 kendi hatamızı yakaladık → 03 GPS → 04 insan + 05 su → 06 altyapı + 07 bülten → 08 simülatör + 09 açık motor); her durakta ana sayfadaki büyük sayı | `web/present.html` |
| 14:00–15:00 | **slides.html** aynı akış; `tools/check_site.py` 0 kırık | `docs/story/slides.html` |
| 15:00–16:30 | **Final QA (PC7'den devir, 60 dk sessiz):** canlı sitede her sayfa: konsol hatası, mobil 375 px yatay kaydırma, tüm butonlar | `docs/qa/FINAL_QA.md` |
| 16:30–17:30 | **README son hâl:** üstte site linki + logo (`web/assets/logo_mark_192.png`, PC1 koydu), tek cümle, 9 iş listesi (ana sayfayla aynı), çalıştırma komutları | `README.md` |
| 17:30–19:00 | 3 dk prova metni `docs/JURI_3DK.md` ile present.html birebir; süre tablosu | `docs/story/three_minute_story.md` |
| 19:00–20:00 | SIGNOFF son tur (PC1 ile), dondurma |

# 🆕 YENİ GÖREV — PC4 (PC1, Paz 13:45 → 20:00) · 12:30 planın bitti, 5-dk kontrol döngüsünü BIRAK, bunları yap
Ad artık **NISAR Vision**, motor `pipeline/nisarvision`. Push öncesi her seferinde: `python tools/check_site.py && python -m pytest -q`. PC6'nın alanına (atlas/simülatör tasarımı, ekran görüntüleri, link listesi) girme.

| Saat | Blok | Çıktı |
|---|---|---|
| 13:45–15:15 | **Başvuru formu metinleri (EN, en kritik iş):** Space Apps formunun 6 sorusu — *What does it do / Benefits / Intended impact / Tools & languages / Creativity / Factors considered* — ana sayfadaki 9 işe göre yeniden yaz. Kurallar: ad NISAR Vision; ana iş = 29 havzalık küresel atlas + kendi hatasını yakalayan QC + GPS r = 0.92 (medyan 1.0 cm) + 1.20 M kişi + 0.32 km³/yr + 81/645 altyapı (ön tarama, güvenlik değerlendirmesi DEĞİL) + 29 bülten + simülatör + açık motor. **Doğruluk:** GUNW'yi JPL açar (biz açmıyoruz); Copernicus DEM yalnızca yüksekliğe bağlı troposfer düzeltmesi; ana ölçüm LOS, dikey yalnızca tahmin; "matematiksel kanıt / kırılmadan önce kesin" gibi abartı yok; kalibrasyon cümlesi aynen; AI kullanımı (Claude Code, Gemini/Antigravity, OpenAI Codex) ve "sitede AI görseli yok". Dil yüzdeleri: Python 68.8 / JS 17.1 / HTML 8.4 / CSS 5.7 | `docs/story/submission_form.md` ilgili bölümler + `tools/sync_submission_form.py` uyumu |
| 15:15–16:00 | Aynı 6 cevabın **Türkçe** kopyası (Kerem forma bakarken kullanacak) | `docs/story/submission_form_tr.md` |
| 16:00–17:15 | **Jüri SSS yenile:** `docs/story/judge_faq.md` (FAQ sayfası bunu gösterir) → NASA mühendisinin soracağı en olası 12 soru, her biri ≤3 cümle: neden LOS, neden 93 gün ortak pencere, QC nasıl çalışır (Semarang ve **Pekin −10.1 cm sıçrama** örneği), OPERA neden manşet değil, provisional ne demek, Konya %11.6 kapsama uyarısı, GHSL nüfus yöntemi, kalıcı su kaybı nasıl ayrıldı, Querétaro neden atlasta yok, tekrar üretilebilirlik | `docs/story/judge_faq.md` |
| 17:15–18:15 | **Science sayfası kart denetimi:** `web/science.html` kartlarının her sayısı `data/global/atlas.json`/`home_summary.json`/`results_registry.json` ile aynı mı (ör. "12/12 detectable", "Konya −9.6 LOS"); eskiyse kaynağı düzelt | `data/results_registry.json` + `docs/qa/PC4.md` tablo |
| 18:15–19:00 | **29 bültenin son okuması:** ad NISAR Vision, kalibrasyon cümlesi, güven/QC notu atlasla aynı; 3 rastgele bülten telefonda (375 px) yatay kayma 0 | `docs/qa/PC4.md` |
| 19:00–19:30 | SIGNOFF son tur PC1 ile (`docs/qa/SCIENCE_SIGNOFF.md`) | imza satırı |
| 19:30–20:00 | Dondurma sonrası `check_site` + pytest; teslime kadar yalnızca yazım düzeltmesi | — |


# 🧊 ÖZELLİK DONDURMA (Kerem kararı, PC1 duyurusu, Paz 13:50) — HERKES
**Artık yeni bir şey eklenmiyor:** yeni bölge, yeni sayfa, yeni özellik, yeni grafik YOK. Sadece var olanı en iyi hâle getir (hata, yazım, tutarlılık, görünüm, hız) ve **sunuma** geç (present.html, slides, 3 dk anlatım, başvuru metni, SSS).
- Yeni veri indirmeyi durdur. Atlas 29 bölgede kalır; 19:15'te PC1 dondurur.
- Planında "yeni" bir şey varsa atla, yerine kendi alanındaki mevcut işi cilala.
- Push öncesi: `python tools/check_site.py && python -m pytest -q`.

# ⚠️ PC1 (jüri denetimi sonrası) — ÖNCELİKLİ metin güncellemesi
Atlas değişti: Konya kendi doğrulama notumuz gereği **gösterge** (−11.0 korunur ama sıralamada yok). **#1 Eloy −8.6**, **15 güvenilir / 14 gösterge**, nüfus **1,167,429 / 477.72 km²**, güven aralıkları artık 93 günlük hıza ait. Şu dosyalardaki eski ifadeleri ("Konya fastest/#1", "16 reliable", "1.20 M / 1,200,716 / 511.65") düzelt: `docs/story/three_minute_story.md`, `press_summary.md`, `qa_cards.md`, `slides_notes.md`, `presentation_cues.md`, `demo_script_v3.md`, `exposure.md`, `docs/JURI_3DK.md`, `README.md`, başvuru formu cevapların. Konya'yı "en güçlü sinyal, kendi incelememiz gösterge tuttu" diye **dürüstlük örneği** olarak anlat.
