# PC6 · BUGFIX (Mehmet'in Antigravity'si, klasör `aseltech-gemini2`, commit öneki `[PC6]`)

> Cmt 22:10: Eski görevlerin (atlas sayfası (`web/atlas.*`), demo videosu, oyun, GNSS/risk paketleri) bu dosyadan **silindi**. Bitmemiş olanlar `tasks/QUEUE.md` → "ORTAK İŞLER" bölümüne PC belirtilmeden taşındı; onları **sen alma**, sadece aşağıdaki bugfix işini yap.

# 🔴 EN GÜNCEL — Cmt 22:00 · BUGFIX (Mehmet kararı, koordinatör PC3) — yukarıdaki her şeyin ÜSTÜNDE
Sen artık atlas ekibinde değilsin. Atlas sayfası (`web/atlas.*`) ve demo videosu işi **DURDU**; onlara dokunma. PC3 ve PC6/PC8 sitenin hatalarını düzeltiyor; atlas ekibi (PC1, PC2, PC4, PC5, PC9, PC10) ayrı çalışıyor, **onların dosyalarına ve işlerine karışma**.

**İşin:** `tasks/QUEUE.md` → "BUGFIX" bölümünde **sana atanmış B16–B29** maddeleri, yukarıdan aşağı. Her maddenin ayrıntısı `docs/SORUN_KAYDI.md`'de (madde numarası S-xx).

**Her madde için:**
1. `git pull --rebase origin main` → QUEUE'da kendi satırını `- [ ]` → `- [~PC6]` yap → status/PC6.md'ye "çalışıyor: Bxx (S-xx)" → commit + push.
2. Önce kontrol et: sorun hâlâ var mı? (dosyayı oku, gerekirse `python -m http.server 8765` ile siteyi aç). Zaten düzeltilmişse satırı QUEUE'dan sil, `docs/qa/PC6.md`'ye "Bxx zaten düzeltilmiş" yaz ve sıradakine geç.
3. Düzelt. Sayıları sadece `data/*/summary.json`, `validation.json`, `assets.json` gibi dosyalardan al; uydurma.
4. Siteyi tarayıcıda aç, konsol 0 hata olsun. Kısa not → `docs/qa/PC6.md` ("Bxx: ne yaptım, nasıl test ettim").
5. Bitince QUEUE'daki satırını **SİL**, yaptığını `docs/qa/PC6.md` ve `status/PC6.md`'ye yaz → commit + push. **En geç 5 dakikada bir commit + push** (iş yarım olsa da, bozuk olmayan bir ara durumda).

**Yazma alanı (bu iş için):** `data/central_valley/`, `data/karapinar/` (yeni `disp_smooth/` dahil), `analysis/pc6/`, `risk/`, `validation/`, `docs/story/key_findings.md`, `docs/story/uncertainty.md`, `docs/story/media/cv_subsidence.*`, `docs/story/media/kp_subsidence.*`, `web/index.html` ve `web/app.js` (SADECE B16, B17, B23 için, küçük değişiklik), `web/science.html` (SADECE B20), `docs/qa/PC6.md`, `status/PC6.md`, QUEUE'da sadece kendi B satırların.
**Kurallar:** `git add` sadece değiştirdiğin dosyalar (`git add -A` YASAK) · indirme yok · `docs/story/key_findings_public.md`'ye dokunma · başka PC'nin satırını alma · PC6 ve PC8 aynı dosyaya (`web/index.html`, `web/app.js`) yazabilir: düzenlemeden hemen önce pull, küçük değişiklik, hemen push · git çakışmasında hiçbir şeyi silme/zorlama, status'a **BLOCKED: <sebep>** yaz ve PC3'ü bekle.
**Liste bitince:** status'a "BUGFIX bitti" yaz. Sonra 3 dakikalık sayaç başlat; sayaç bitince `git pull` yap ve bu dosyanın en altını kontrol et. Yeni görev varsa başla; yoksa sayacı yeniden başlat. Asla durma, başkasının işini yapma.
- Ek (22:15): atlas yan panelinde `docs/story/atlas_cities/<id>.md` varsa "City card" bağlantısı; Data sayfasında `docs/story/atlas_data_dictionary.md` ve `atlas_methods.md` bağlantısı (PC4 yazıyor; yoksa bağlantıyı gizle).

---
## 🔴 Cmt 22:45 — PC3'ten EK GÖREV (PC8'in sırasından sana devredildi)
B16–B30 ve B35 bitti, teşekkürler. Sıradaki işlerin: `tasks/QUEUE.md` BUGFIX bölümünde **`[atandı: PC6]` yazan B31 ve B32** (ayrıntı: `docs/SORUN_KAYDI.md` S-31 ve S-32). B31: hero'yu senin ürettiğin `hero_loop` videosuna bağla. B32: web sayfalarında "Team Taykut" → "Team Aseltech".
**Bu iki madde için yazma alanına eklendi:** `web/index.html`, `web/app.js`, `web/style.css`, `web/data.html`, `web/faq.html`, `web/science.html`. PC8 aynı dosyalarda B13/B14 üzerinde çalışıyor: **her düzenlemeden hemen önce `git pull --rebase origin main`, küçük değişiklik, hemen push.** Sadece B31 ve B32'ye dokun; B33 ve B34 PC8'in. Diğer kurallar aynı. Bitince satırı sil, `docs/qa/PC6.md` ve `status/PC6.md`'ye yaz.

## 🟢 Cmt 23:00 — İŞ ALMA KURALI (Mehmet kararı; yukarıdaki "dokunma" cümlelerinin yerine geçer)
Kendi atanmış maddelerin bitince **sormadan** `tasks/QUEUE.md`'den yeni iş al, yukarıdan aşağı ilk uygun satırı:
- **Uygun:** `- [ ]` ile başlayan ve `[atandı: ...]` içermeyen satırlar (ORTAK İŞLER C01–C06 dahil), ya da `[atandı: PCx]` yazıp **sana** ait olanlar. **Alma:** `- [~PCy]` (başkası almış) ve `[atandı: başka PC]` satırları.
- **Almak için:** `git pull --rebase origin main` → satırı `- [~PCx]` yap ve satırın sonuna `(PCx aldı HH:MM)` notu ekle (PCx = senin numaran, HH:MM = saat) → **sadece o satırı** değiştir → hemen commit + push. Push reddedilirse `git pull --rebase origin main`; satırı o arada başkası aldıysa onu BIRAK, bir sonrakini seç. Push geçmeden işe başlama.
- **Bitince:** satırı kuyruktan SİL, `status/PCx.md` ve `docs/qa/PCx.md`'ye log yaz → commit + push. Boş kalma, sıradakini al.
- Atlas sayfası (C01–C04) ve bülten/depolama işleri (C05, C06) artık serbest; ilk boşta kalan alır.


# 🌍 ATLAS FİNAL — PC6 (Paz 00:20, PC1) · plan: `docs/ATLAS_FINAL.md`
PC6 artık PC1 koordinasyonunda (Kerem kararı). Atlas sayfası (`web/atlas.html`, `atlas.js`, `atlas.css`) SENİN. Video beklemede (Paz 16:00 opsiyonel final). Sırayla, sormadan:
1. **Zaman kaydırıcı animasyon (en önemli):** şehre tıklayınca yan panelde `data/<yol>/disp/*.png` serisi tarih kaydırıcıyla oynasın (oynat/durdur, tarih etiketi, cm renk ölçeği, PROVISIONAL rozeti). Haritada seçili şehrin son kümülatif PNG'si `meta.json` bbox'ına şeffaf katman olarak otursun.
2. **Katmanlar (NASA Worldview tarzı):** Çökme / Belirsizlik σ (`data/global/<şehir>/uncertainty/sigma_cm.png`) / Güven sınıfı; tek tıkla, lejant değişsin.
3. **Vital Signs kartları (NASA Climate tarzı):** 4 büyük sayı: Cities measured · Fastest-sinking place (cm/100d) · Area sinking > 5 cm (km²) · People living on sinking ground. Veri `data/global/vital_signs.json` (PC8 üretir); alan yoksa kartı gizle.
4. **Sunum turu ("Tour" düğmesi, NASA Eyes tarzı):** küre ilk 5 şehre sırayla uçsun (her biri 6 sn, altyazı: şehir, hız, güven). Lincoln sunumunda tek tıkla.
5. **Çevrimdışı yedek (kritik):** maplibre-gl 5.3.0 js/css'i `web/vendor/`'a kopyala; internet yoksa NASA Blue Marble (kamu malı, NASA Visible Earth) `web/assets/bluemarble_2k.jpg` ile yedek görünüm. Test: ağ kapalıyken sayfa açılıyor mu.
6. **Paylaşılabilir link:** `atlas.html#mexico_city` o şehri açsın.
7. **Kalite:** telefon 375 px, projektör 1920, konsol 0 hata; `indicative_only` şehirler soluk + "indicative only"; her sayının yanında dönem ve LOS. REVIEW_1500, emoji yok. Sonuç `docs/qa/PC6.md`.
8. PC10 yeni alanları (`detectable`, `robustness_spread`, `people_exposed`, `opera_check`) yan panele; PC4 şehir kartları ve PC8 bültenleri panelden bağlı.
9. Paz 16:00 (opsiyonel): video v2'yi final atlasla yeniden üret.
Yazma alanı: `web/atlas.*`, `web/vendor/`, `web/assets/bluemarble*`, `docs/story/media/pc6_*`, `docs/qa/PC6.md`, `status/PC6.md`; diğer site dosyalarında sadece menü/kart satırı. Önce commit → pull --rebase → push.


# ♻️ SÜREKLİ KURAL (Paz 00:45, PC1)
`tasks/SUREKLI.md` zorunlu: **her 3 dakikada bir** commit → pull --rebase → push, bu dosyanın sonuna yeni bölüm var mı bak, status tek satır. Asla durma; listen biterse SUREKLI.md tablosundaki kendi sürekli işin.

# ➕ TAKVİYE (Paz 00:55, PC1) — FİNAL 1–8 bitti, sıradakiler (uydu animasyonu PC1'de: `web/atlas_sat.js`/`.css` dosyalarına DOKUNMA; `atlas.js`'de `window.atlasSelect(id)` / `atlas:select` olayı varsa koru)
1. **Zaman serisi grafiği:** yan panelde seçili şehrin en çok çöken noktası (`points.json` p01) için tarih–cm çizgi grafiği (SVG, kütüphanesiz), belirsizlik bandı (±2σ).
2. **İki şehri karşılaştır:** "Compare" ile iki şehir yan yana: hız, güven, grafik üst üste.
3. **Arama ve filtre:** şehir arama kutusu; güven sınıfı ve ülke filtresi; liste ve küre birlikte filtrelensin.
4. **LOS / dikey tahmin anahtarı:** sayılar `max_cm_los` ↔ `max_cm_vertical_est`, "estimate" etiketiyle.
5. **Veri indir paneli:** `atlas.geojson`, `atlas.csv`, `atlas.json`, bülten ve şehir kartı linkleri; NASA tarzı "Data & citation" kutusu (PC4 `sources.md`).
6. **GNSS doğrulama katmanı:** Central Valley için `validation/gnss_stations.csv` istasyonları küçük üçgen, tıklayınca r/RMSE.
7. **Performans:** ilk açılış < 3 sn (lazy PNG, küçük görseller), Lighthouse erişilebilirlik ≥ 90; sonuç `docs/qa/PC6.md`.
Her adımda commit + push; 3 dk döngüsü (`tasks/SUREKLI.md`).


# 🛰️ NOT (Paz 01:30, PC1)
`web/nisar3d.js`, `web/atlas_sat.js`, `web/atlas_sat.css`, `web/vendor/three/`, `web/vendor/satellite.min.js`, `data/nisar_tle.json` PC1in (NISAR 3D yörünge görünümü). Dokunma; atlas.html içindeki iki script satırını ve atlas-toolbar düğmesini koru.


# ⭐ ATLAS KUSURSUZLUK (Paz 01:00, PC1) · `docs/ATLAS_MUKEMMEL.md`
1. Atlas sayfası: eksik dosya yoklamalarında (HEAD) konsola 404 düşmesin — bilinen dosya listesini `docs/qa/ATLAS_COMPLETENESS.md` yerine `atlas.json` alanlarından türet veya yoklamayı sessiz yap; konsol 0 hata.
2. NISAR 3D görünümü varsayılan açılıyor (PC1): `web/nisar3d.js`, `atlas_sat.*` dosyalarına dokunma; 3D açıkken sol panel listesi, filtreler ve yan panel düzgün çalışıyor mu test et, sorunları `docs/qa/PC6.md`'ye yaz.
3. Mobil (375 px) ve projektör (1920) son test.


# ➕ TAKVİYE (Paz 01:40, PC1) · tablo: `docs/qa/ATLAS_COMPLETENESS.md` (`python tools/atlas_completeness.py`)
1. 45 dk commit yok: "TAKVİYE (00:55)" ve "ATLAS KUSURSUZLUK (01:00)" maddelerini yap (konsol 0 hata, 3D açıkken liste/filtre testi, mobil).


# 📣 GENEL EMİR (Paz 01:50, PC1) — HERKES, HEMEN
1. Elindeki işi bırakmadan **şu an yaptığın her şeyi commit et ve pushla** (yarım iş de olsa ara kayıt: `[PC6] ara kayit: <ne>`). `git add <kendi yolların>` → `git commit` → `git pull --rebase origin main` → `git push origin main`.
2. `status/PC6.md`'ye tek satır yaz: ne yapıyorsun, % kaç bitti, sıradaki ne.
3. Bundan sonra **en geç 10 dakikada bir** commit + push; 10 dk'dan uzun commit'siz kalma (uzun indirmede her çift bitince ara kayıt).
4. Sonra bu dosyadaki en son TAKVİYE / KUSURSUZLUK bölümünden devam et.


# ➕ TAKVİYE (Paz 02:05, PC1 otomatik kontrol)
Atlas işlerin bitti; yeni iş (NISAR 3D dosyalarına dokunma):
1. **Atlas yazdırma görünümü:** `@media print` ile atlas sayfası A4'te tek sayfa sıralama posteri (başlık, ilk 15 tablo, güven rozeti, kalibrasyon cümlesi, kaynak); jüriye PDF olarak verilecek. `docs/qa/PC6.md`'ye ekran görüntüsü yolu.
2. **"Updated" rozeti:** atlas.json'da `note` "recomputed" içeren şehirlerde (Tahran) yan panelde "Recomputed with off-basin reference — old value −3.5 cm" satırı.
3. **Ana sayfa "Key numbers":** `data/global/vital_signs.json`'dan (şehir sayısı, en hızlı, alan, nüfus) canlı oku; sabit sayı kalmasın.
4. Site geneli kırık link + konsol taraması (cache-bust sonrası `?v=` linkleri dahil), sonuç `docs/qa/PC6.md`.


# ➕ TAKVİYE (Paz 02:25, PC1) — atlas 19 bölge, tamlık 86/114 (`docs/qa/ATLAS_COMPLETENESS.md`). PC4/PC5 2 saattir durmuş; eksikleri sen tamamla.
1. **Şehir kartları (PC4 durdu, sana geçti):** `docs/story/atlas_cities/{semarang,eloy,delhi,quetta,hanoi,xian}.md` — mevcut kartların biçiminde (örn. `konya_plain.md`), ≤150 kelime: neden çöküyor (kaynaklı), kim etkileniyor, yayımlanmış hız (kaynak+yıl), bizim değerimiz (cm/100d, dönem, güven, atlas.json'dan), NISAR'ın kattığı. Uydurma yok.
2. Atlas sayfasında yeni 4 şehrin (eloy, delhi, quetta, xian) panel/animasyon/filtrede doğru göründüğünü test et.


# 🔄 YENİ ATAMA (Paz 03:05, PC1) — atlas 19 bölge, QC sonrası sıralama: 1 Konya Ovası, 2 Mashhad, 3 Central Valley, 4 Eloy, 5 Mexico City (`docs/story/atlas_top5_check.md`). Tamlık 100/114.
1. **Kalite kontrolü görünür olsun:** atlas sayfasında `qc_flags` olan bölgelerin yan panelinde gerekçe kutusu (atlas.json `note` + `qc_flags`), sıralama tablosunun altına tek satır "Quality control: N regions flagged (time-series check) — see method" ve `docs/story/atlas_top5_check.md` bağlantısı. Science sayfasının listesine `atlas_top5_check.md` ekle.
2. Konsol 0 hata, mobil kontrol.


# 🔗 ENTEGRASYON (Paz 03:20, PC1) · `docs/ENTEGRASYON.md`
**Sitede görünür yap:** `data/results_registry.json`'da senin satırların: `validation_report`. Her birine `summary` (tek sade cümle) ve `key_number` (birim + kalite etiketi, kendi veri dosyandan) yaz, `status: ready`. Yeni sonuç üretince yeni satır ekle (aynı alanlar). Sayı uydurma yok; PC4 sayı siciliyle aynı olmalı.

**Senin ana işin (Paz 10:00):** 1) `web/science.html` en üstüne kayıttan otomatik "Results" kart ızgarası (gruplar, anahtar sayı + kalite rozeti, küçük grafik, Read/Data). 2) `web/data.html` Downloads tablosu kayıttan otomatik. 3) Atlas yan paneline: detectable, robustness aralığı, OPERA, nüfus, QC gerekçesi, doğrulama notu özeti (yoksa gizle). 4) Ana sayfa Key numbers kayıttan/vital_signs'tan. Konsol 0 hata, mobil test.


# ➕ TAKVİYE (Paz 03:50, PC1 otomatik kontrol) — atlas 21 bölge, tamlık 122/126
1. Science sayfasında Results bölümü kayıttan çalışıyor mu kontrol et; kayıtta artık `atlas_changelog` ve yeni satırlar olabilir — otomatik görünmeli.
2. **"What changed" kutusu:** atlas sayfasında `data/global/atlas_changelog.json`'dan son 10 değişiklik (tarih, bölge, eski→yeni, neden).
3. **Hata çubukları:** sıralama tablosunda `rate_ci_cm_per_100d` varsa küçük aralık çubuğu; sıralama metriği artık ortak pencere (`rate_cm_per_100d_common`) — tablo başlığında belirt.

# 🎮 OYUN ↔ ATLAS (Paz 04:05, PC1 — Kerem onayı) · oyun 4 saattir dokunulmadı, artık yine senin
Oyun sağlam (canlıda testler 6/6, konsol 0 hata). Amaç: oyunu atlasla tek hikâyeye bağlamak. Sırayla:
1. **Konya tutarlılığı (önce bu):** oyundaki "Konya Closed Basin" `data/karapinar/summary.json`'a (−5.9 cm LOS) kalibre; atlasın 1. sırası ise **Konya Plain** (`data/konya_plain/`, −9.6 cm LOS). Jüri iki farklı sayı görüp karışmasın: oyunda bölge adını ve kartı "Karapınar sub-basin, Konya Closed Basin" yap ve kartta tek satır "Atlas: Konya Plain −9.6 cm (rank 1) → link" ekle. Kalibrasyonu değiştirme; `test_model.html` 6/6 kalmalı.
2. **Atlastan oyuna:** atlas yan panelinde `central_valley`, `konya_plain`, `karapinar` seçilince "Manage this valley in the simulator" düğmesi → `game/?basin=tulare` veya `game/?basin=konya`.
3. **Oyundan atlasa:** oyun `?basin=` parametresini okuyup o vadiyle açılsın (karşılama penceresinde seçili); bitiş ekranına "See where else the ground is sinking → atlas" bağlantısı (`atlas.html#konya_plain` / `#central_valley`).
4. **Ders planı uyumu:** `docs/story/lesson_plan.md`'deki sorulardan biri atlasla karşılaştırma olsun (PC4'e not bırak, dosya onun).
5. Test: mobil 375 px, projektör 1920, konsol 0 hata, `game/test_model.html` 6/6, `python -m pytest -q` geçer. Sonuç `docs/qa/PC6.md`.
`results_registry.json`'a `simulator` satırı ekle (group "Engagement", doc `docs/story/game_model.md`, summary + key_number "6/6 model tests, calibration error 0 %"). En geç 10 dk'da bir commit + push.


# ⏱️ 8 SAATLİK PLAN (Paz 04:15 → 12:15, PC1) — sonra 20:00 veri dondurmaya kadar SUREKLI
Bu bölüm, önceki bölümlerde bitmemiş işleri de kapsar ve geçerli olan TEK listedir. Blokları sırayla yap; bir blok erken biterse sıradakine geç. Her blok sonunda commit + push + status satırı. En geç 10 dk'da bir commit.
| Saat | Blok | Çıktı |
|---|---|---|
| 04:15–06:00 | **Oyun ↔ atlas** (önceki bölüm "OYUN ↔ ATLAS" 1–5) | game + atlas linkleri |
| 06:00–07:30 | **Results bölümü cilası** (kayıttan, gruplar, rozet, grafik), **"What changed"** kutusu (`atlas_changelog.json`), sıralama tablosunda **hata çubukları** ve "ranked by common 93-day window" başlığı | science.html, atlas |
| 07:30–09:00 | **Ortak ölçekli küçük haritalar** (PC10 `thumb.png`) atlas listesinde ve Results kartlarında; "en hızlı / en geniş" anahtarı (PC10 `area_km2_lt_minus5cm_common`) | atlas |
| 09:00–10:30 | **Sunum modu:** `web/present.html` — Lincoln demosu için tek tıkla bölüm turu (ana sayfa → atlas → Konya → Results → simülatör), ok tuşları, büyük yazı, internet yoksa yerel kopya çalışır | present.html |
| 10:30–12:15 | **Site geneli denetim:** her sayfada konsol 0 hata, kırık link 0, alt metinler, kontrast, ilk açılış < 3 sn (görsel boyutları), mobil 375 / projektör 1920; sonuç tablosu `docs/qa/PC6.md` | QA raporu |
| 12:15–20:00 | SUREKLI: PC4'ün `docs/qa/PC4.md` site metni bulgularını düzelt; yeni alanları panele ekle; 20:00 sonrası sadece hata düzeltme | — |
NISAR 3D dosyalarına (`nisar3d.js`, `atlas_sat.*`) dokunma.


# 🛰️ GİT ÜZERİNDEN YÖNETİM (Paz 04:25, PC1)
Kullanıcı artık prompt girmiyor; bu dosyanın sonu ve `tasks/SUREKLI.md` senin tek emir kaynağın. 8 saatlik planın biterse `tasks/BACKLOG_ORTAK.md`'den satır al (`[~PCx]` → commit+push → yap → `[x PCx]`). Onay bekleme, soru sorma; karar gerektiren durumda en makul seçeneği uygula ve gerekçesini `docs/qa/PCx.md`'ye yaz.


# ⏳ PLAN SONU SİNYALİ (Paz 04:35, PC1)
Son bloğa geldiğinde `status/PC6.md` ilk satırına `PLAN_SONU_YAKIN` yaz, pushla. PC1 20 dk içinde bu dosyanın sonuna yeni 6–8 saatlik plan ekler; o arada `tasks/BACKLOG_ORTAK.md`. Teslime (Paz 22:00) kadar durmak yok.


# ▶ DEVAM (PC1 otomatik kontrol, Paz kontrol 1)
52 dk commit yok. 8 SAATLİK PLAN'da kaldığın bloktan devam et; uzun iş sürüyorsa ara kayıt commit'i at ve `status/PC6.md`'ye hangi blokta olduğunu yaz. Planın son bloğundaysan ilk satıra `PLAN_SONU_YAKIN` yaz.


# ⛔ DURMUŞ SAYILDI (PC1 otomatik kontrol 2)
60 dk'dan uzun commit yok; kritik işlerin BACKLOG_ORTAK (site işleri) ve PC2 (site QA) tarafına devredildi. Dönersen `tasks/BACKLOG_ORTAK.md`'de `[ ]` kalan kendi işlerini geri al (`[~PC6]`), başkasının aldığına dokunma.


# 🏁 FİNAL — TOPLAMA VE BİRLEŞTİRME (PC1, Paz 11:15 TR) · önce `docs/JURI_3DK.md`'yi oku
Jüri siteyi 3 dakika inceleyecek. Yeni veri/özellik yok; toparla, sadeleştir, tutarlı yap. Ana sayfayı PC1 kuruyor. Bu bölüm önceki tüm planların ÜSTÜNDEDİR. Her blok sonunda commit + push (önce kendi dosyaların → pull --rebase → push), status satırı. Veri dondurma 20:00, teslim 22:00.
**Rol: site mühendisliği ve simülatör (ana sayfa içeriği PC1'de; sen geri kalan sayfalar ve hız).**
1. (11:15–12:30) **Menü sadeleştirme (tüm sayfalarda aynı):** Home · Atlas · Simulator · Science · Data · (Present). Kırık/eski menü öğesi kalmasın. Footer'da kalibrasyon cümlesi + kaynak satırı tek tip.
2. (12:30–14:00) **Atlas sayfası jüri modu:** `atlas.html?jury=1` (veya varsayılan): açılışta güvenilir 1. bölge seçili, panel açık, "How to read" kutusu görünür; ilk ekranda (1920×1080) küre + ilk 5 + panel birlikte. NISAR 3D dosyalarına dokunma.
3. (14:00–15:30) **Simülatör 30 saniye:** karşılama penceresine "Quick demo (30 s)" düğmesi — Over-Pump senaryosunu 24 ay otomatik oynatır ve sonuçta tek cümle gösterir ("Pumping 50% more → X cm more sinking, Y cm of it permanent"); `test_model.html` 6/6 kalmalı.
4. (15:30–17:00) **Hız:** her sayfa ilk açılış < 2 sn (lazy görseller, büyük PNG/MP4'leri ilk ekrandan çıkar, video poster); ölçümleri `docs/qa/PC6.md`'ye yaz.
5. (17:00–18:30) **Son tarama:** 1920×1080 projektör, 1366×768 dizüstü, 375 px telefon; konsol 0 hata, kırık link 0; PC1'e bulgu listesi.


# 🆕 YENİ PLAN — PC6 (PC1, Paz 12:15 → 20:00) · site artık yeni görsel kimlikte (`web/theme.css`, `web/assets/logo.svg`)
Yeni veri YOK; amaç jürinin 3 dakikada gördüğü her ekranın aynı kalitede olması.
| Saat | Blok | Çıktı |
|---|---|---|
| 12:15–13:45 | **Atlas sayfası tema uyumu:** `web/atlas.html`/`atlas.css` başlık, kartlar, Top 5, detay paneli → `theme.css` fontları (Archivo/Public Sans/Plex Mono), 2–3 px köşe, gölgesiz kenarlık; ilk ekranda tek cümle "renk = 100 günde cm, kırmızı = çöküyor" | commit + `docs/qa/PC6.md` ekran görüntüsü |
| 13:45–15:15 | **Atlas mobil + performans QA:** 375 px'de yatay kaydırma 0, büyük PNG'lere `loading="lazy"`, konsol hatası 0; atlas_sat/3D dosyalarına DOKUNMA | `docs/qa/PC6.md` |
| 15:15–16:45 | **Simülatör tema uyumu:** `game/` başlığına `../assets/logo_mark_64.png` + "NISAR Vision" yazısı (yapıldı, PC1) + fontlar, "← NISAR Vision ana sayfa" bağlantısı, "Bu model NISAR ölçümüne nasıl bağlı" tek kart | commit |
| 16:45–18:15 | **Teslim ekran görüntüleri:** ana sayfa, atlas, bülten, simülatör; 1440×900 ve 375×812 → `docs/story/media/site_{home,atlas,bulletin,game}_{desk,mob}.png` | 8 PNG |
| 18:15–19:30 | **Tüm bağlantı kontrolü** (GitHub Pages canlı sitede her `href`/`src` 200) → `docs/qa/PC6_links.md`; kırıkları düzelt | rapor |
| 19:30–20:00 | Son kontrol, dondurma |


# ▶ DEVAM (PC1, 12:55)
46 dk commit yok; 12:15 YENİ PLAN'ının 1. bloğu (atlas tema uyumu). Not: PC1 atlas Top 5 kartındaki taşmayı ve tablo yatay kaymasını düzeltti (`web/atlas.css` sonu) — üstüne yaz, geri alma.


# ℹ️ PC1 (13:10)
Mehmet hesabından etiketsiz commit'ler geliyor (isim değişikliği, logo, simülatör başlığı). Bunlar sensen commit mesajına `[PC6]` ekle ki takip edilebilsin. 12:15 YENİ PLAN'ına devam: atlas/simülatör tema uyumu → teslim ekran görüntüleri (`docs/story/media/site_*`, yeni isim ve logoyla) → bağlantı kontrolü.


# 🧊 ÖZELLİK DONDURMA (Kerem kararı, PC1 duyurusu, Paz 13:50) — HERKES
**Artık yeni bir şey eklenmiyor:** yeni bölge, yeni sayfa, yeni özellik, yeni grafik YOK. Sadece var olanı en iyi hâle getir (hata, yazım, tutarlılık, görünüm, hız) ve **sunuma** geç (present.html, slides, 3 dk anlatım, başvuru metni, SSS).
- Yeni veri indirmeyi durdur. Atlas 29 bölgede kalır; 19:15'te PC1 dondurur.
- Planında "yeni" bir şey varsa atla, yerine kendi alanındaki mevcut işi cilala.
- Push öncesi: `python tools/check_site.py && python -m pytest -q`.

## PC6 için netleştirme (13:50)
12:15 planındaki işler zaten cilalama: atlas/simülatör tasarım uyumu, teslim ekran görüntüleri (`docs/story/media/site_*`, yeni ad ve logoyla), bağlantı kontrolü. Yeni düğme/katman/özellik ekleme.
