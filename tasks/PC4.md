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
