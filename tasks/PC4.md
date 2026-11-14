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
NASA teknik rapor tarzı, 4–6 sayfa: Abstract (150 kelime) · 1 Data (ürünler, tarihler, kalite sınıfları) · 2 Methods (faz→cm, düzeltmeler, zincir, ayrıştırma) · 3 Validation (10 GPS, ikinci geçiş p114, C-band OPERA) · 4 Uncertainty (piksel σ, referans duyarlılığı, atmosfer) · 5 Results (108 gün, tam yıl, Delta, Konya, küresel) · 6 Original contributions (O1 depolama kaybı, O2 olasılıksal mühendislik riski, O3 NISAR Pulse aracı) · 7 Limitations · References (hepsi doğrulanmış link).
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
