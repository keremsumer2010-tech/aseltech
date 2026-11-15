# PC8 · BUGFIX (Mehmet'in Antigravity'si, klasör `aseltech-gemini3`, commit öneki `[PC8]`)

> Cmt 22:10: Eski görevlerin (UK kil, maruziyet, O1, bültenler, teslim formu) bu dosyadan **silindi**. Bitmemiş olanlar `tasks/QUEUE.md` → "ORTAK İŞLER" bölümüne PC belirtilmeden taşındı; onları **sen alma**, sadece aşağıdaki bugfix işini yap.

# 🔴 EN GÜNCEL — Cmt 22:00 · BUGFIX (Mehmet kararı, koordinatör PC3) — yukarıdaki her şeyin ÜSTÜNDE
Sen artık atlas ekibinde değilsin. Atlas bülten işi (`docs/bulletins/`) **DURDU**; ona dokunma. PC3 ve PC6/PC8 sitenin hatalarını düzeltiyor; atlas ekibi (PC1, PC2, PC4, PC5, PC9, PC10) ayrı çalışıyor, **onların dosyalarına ve işlerine karışma**.

**İşin:** `tasks/QUEUE.md` → "BUGFIX" bölümünde **sana atanmış B01–B15** maddeleri, yukarıdan aşağı. Her maddenin ayrıntısı `docs/SORUN_KAYDI.md`'de (madde numarası S-xx).

**Her madde için:**
1. `git pull --rebase origin main` → QUEUE'da kendi satırını `- [ ]` → `- [~PC8]` yap → status/PC8.md'ye "çalışıyor: Bxx (S-xx)" → commit + push.
2. Önce kontrol et: sorun hâlâ var mı? (dosyayı oku, gerekirse `python -m http.server 8765` ile siteyi aç). Zaten düzeltilmişse satırı QUEUE'dan sil, `docs/qa/PC8.md`'ye "Bxx zaten düzeltilmiş" yaz ve sıradakine geç.
3. Düzelt. Sayıları sadece `data/*/summary.json`, `validation.json`, `assets.json` gibi dosyalardan al; uydurma.
4. Siteyi tarayıcıda aç, konsol 0 hata olsun. Kısa not → `docs/qa/PC8.md` ("Bxx: ne yaptım, nasıl test ettim").
5. Bitince QUEUE'daki satırını **SİL**, yaptığını `docs/qa/PC8.md` ve `status/PC8.md`'ye yaz → commit + push. **En geç 5 dakikada bir commit + push** (iş yarım olsa da, bozuk olmayan bir ara durumda).

**Yazma alanı (bu iş için):** `web/index.html`, `web/app.js`, `web/science.html`, `web/style.css`, `web/faq.html`, `web/data.html`, `.github/workflows/pages.yml`, `docs/qa/PC8.md`, `status/PC8.md`, QUEUE'da sadece kendi B satırların.
**Kurallar:** `git add` sadece değiştirdiğin dosyalar (`git add -A` YASAK) · indirme yok · `docs/story/key_findings_public.md`'ye dokunma · başka PC'nin satırını alma · PC6 ve PC8 aynı dosyaya (`web/index.html`, `web/app.js`) yazabilir: düzenlemeden hemen önce pull, küçük değişiklik, hemen push · git çakışmasında hiçbir şeyi silme/zorlama, status'a **BLOCKED: <sebep>** yaz ve PC3'ü bekle.
**Liste bitince:** status'a "BUGFIX bitti" yaz. Sonra 3 dakikalık sayaç başlat; sayaç bitince `git pull` yap ve bu dosyanın en altını kontrol et. Yeni görev varsa başla; yoksa sayacı yeniden başlat. Asla durma, başkasının işini yapma.

## 🟢 Cmt 23:00 — İŞ ALMA KURALI (Mehmet kararı; yukarıdaki "dokunma" cümlelerinin yerine geçer)
Kendi atanmış maddelerin bitince **sormadan** `tasks/QUEUE.md`'den yeni iş al, yukarıdan aşağı ilk uygun satırı:
- **Uygun:** `- [ ]` ile başlayan ve `[atandı: ...]` içermeyen satırlar (ORTAK İŞLER C01–C06 dahil), ya da `[atandı: PCx]` yazıp **sana** ait olanlar. **Alma:** `- [~PCy]` (başkası almış) ve `[atandı: başka PC]` satırları.
- **Almak için:** `git pull --rebase origin main` → satırı `- [~PCx]` yap ve satırın sonuna `(PCx aldı HH:MM)` notu ekle (PCx = senin numaran, HH:MM = saat) → **sadece o satırı** değiştir → hemen commit + push. Push reddedilirse `git pull --rebase origin main`; satırı o arada başkası aldıysa onu BIRAK, bir sonrakini seç. Push geçmeden işe başlama.
- **Bitince:** satırı kuyruktan SİL, `status/PCx.md` ve `docs/qa/PCx.md`'ye log yaz → commit + push. Boş kalma, sıradakini al.
- Atlas sayfası (C01–C04) ve bülten/depolama işleri (C05, C06) artık serbest; ilk boşta kalan alır.


# 🌍 ATLAS FİNAL — PC8 (Paz 00:20, PC1) · plan: `docs/ATLAS_FINAL.md`
PC8 artık PC1 koordinasyonunda (Kerem kararı). Sırayla, sormadan:
1. **Çöken zeminde yaşayan nüfus (en önemli yeni sayı):** GHSL GHS-POP (JRC açık veri, giriş gerekmez) ile her atlas şehrinin kutusunda çökme < −2 ve < −5 cm (108 gün) olan piksellerde yaşayan kişi. σ'nın 2 katından küçük çökmeleri sayma (PC5 detectability). Çıktı `data/global/exposure_atlas.json` (`{id, people_lt_minus2cm, people_lt_minus5cm, area_km2_lt_minus5cm, source, quality}`); yöntem `docs/story/exposure.md` "Global atlas" bölümü.
2. **`data/global/vital_signs.json`:** cities_measured, fastest {id, rate_cm_per_100d}, area_km2_lt_minus5cm (toplam), people_on_sinking_ground (toplam < −5 cm); her alan kaynaklı. Her yeni şehirde yeniden üret.
3. **Bülten v2 (NASA Disasters Program harita paketi tarzı):** üst blok: Product ID (`NP-<şehir>-2026-001`), issue time UTC, data window, sensor (NISAR L-band GUNW, provisional), quality class, confidence, version; altta disclaimer + kalibrasyon cümlesi. İçerik: hız (cm/100d), en çok çöken 3 alan, etkilenen nüfus, altyapı (O2 / PC7 küresel risk), "What this means" 3 madde. Tüm atlas şehirleri, A4 yazdırılabilir.
4. **Teslim formu:** `submission_form.md`'ye atlas paragrafı (karakter sınırı, PC5 onaylı sayılar).
5. Döngü: yeni şehirde 1–3'ü yeniden üret; pytest, link kontrolü; `docs/qa/PC8.md`.
Yazma alanı: `tools/bulletin.py`, `docs/bulletins/`, `data/global/exposure_atlas.json`, `data/global/vital_signs.json`, `docs/story/exposure.md`, `docs/story/submission_form.md`, `docs/story/slides_notes.md`, `docs/qa/PC8.md`, `status/PC8.md`. GHSL ham dosyası `raw/` altına (commit etme).


# ♻️ SÜREKLİ KURAL (Paz 00:45, PC1)
`tasks/SUREKLI.md` zorunlu: **her 3 dakikada bir** commit → pull --rebase → push, bu dosyanın sonuna yeni bölüm var mı bak, status tek satır. Asla durma; listen biterse SUREKLI.md tablosundaki kendi sürekli işin.


# ⭐ ATLAS KUSURSUZLUK (Paz 01:00, PC1) · `docs/ATLAS_MUKEMMEL.md`
1. **`tools/atlas_completeness.py`** yaz: atlas.json'daki her şehir için 6 parça (summary/disp, sigma_cm.png, validation_note.json, atlas_cities/<id>.md, bulletins/<id>.html, exposure satırı) var mı → `docs/qa/ATLAS_COMPLETENESS.md` tablo (✓/✗ + sahibi). Her 30 dk yeniden çalıştır.
2. Senin ✗'lerin: eksik bültenler ve exposure satırları — hemen tamamla.
3. Sonra SUREKLI döngü.


# ➕ TAKVİYE (Paz 01:40, PC1) · tablo: `docs/qa/ATLAS_COMPLETENESS.md` (`python tools/atlas_completeness.py`)
1. **`tools/atlas_completeness.py` (senin, 14af16c) iyi;** bakımı: her 30 dk çalıştır, `docs/qa/ATLAS_COMPLETENESS.md`'yi pushla, ✗ olan sahiplerin task dosyasına değil kendi `docs/qa/PC8.md`'ne yaz.
2. PC10 eloy, quetta, xian'ı ekleyince bülten + exposure satırlarını üret; vital_signs'ı güncelle.


# 📣 GENEL EMİR (Paz 01:50, PC1) — HERKES, HEMEN
1. Elindeki işi bırakmadan **şu an yaptığın her şeyi commit et ve pushla** (yarım iş de olsa ara kayıt: `[PC8] ara kayit: <ne>`). `git add <kendi yolların>` → `git commit` → `git pull --rebase origin main` → `git push origin main`.
2. `status/PC8.md`'ye tek satır yaz: ne yapıyorsun, % kaç bitti, sıradaki ne.
3. Bundan sonra **en geç 10 dakikada bir** commit + push; 10 dk'dan uzun commit'siz kalma (uzun indirmede her çift bitince ara kayıt).
4. Sonra bu dosyadaki en son TAKVİYE / KUSURSUZLUK bölümünden devam et.


# ➕ TAKVİYE (Paz 02:25, PC1) — atlas 19 bölge, tamlık 86/114 (`docs/qa/ATLAS_COMPLETENESS.md`). PC4/PC5 2 saattir durmuş; eksikleri sen tamamla.
1. Yeni 4 şehir **eloy, delhi, quetta, xian** için bülten + `exposure_atlas.json` satırı; vital_signs güncelle (19 bölge).
2. Tamlık tablosunu her 30 dk yeniden üret.


# 🔬 PC1 BAĞIMSIZ KONTROL SONUCU (Paz 02:55) · `docs/story/atlas_top5_check.md`
`vital_signs.json` 'fastest' alanı artık **güvenilir bölgelerden** seçilmeli (QC işaretlileri hariç); PC1 düzeltti (Konya Ovası). Üreticin varsa bu kuralı ekle. Bültenlerde QC notu olan şehirlere "Under revision" satırı ekle.


# 🔄 YENİ ATAMA (Paz 03:05, PC1) — atlas 19 bölge, QC sonrası sıralama: 1 Konya Ovası, 2 Mashhad, 3 Central Valley, 4 Eloy, 5 Mexico City (`docs/story/atlas_top5_check.md`). Tamlık 100/114.
1. Teslim formu ve `slides_notes.md`: yeni sıralama (1 Konya Ovası), QC hikâyesi tek cümle, Tahran −7.4. 2. Tamlık tablosunu 30 dk'da bir yenile.


# 🔗 ENTEGRASYON (Paz 03:20, PC1) · `docs/ENTEGRASYON.md`
**Sitede görünür yap:** `data/results_registry.json`'da senin satırların: `exposure`, `storage_loss`, `uk_findings`. Her birine `summary` (tek sade cümle) ve `key_number` (birim + kalite etiketi, kendi veri dosyandan) yaz, `status: ready`. Yeni sonuç üretince yeni satır ekle (aynı alanlar). Sayı uydurma yok; PC4 sayı siciliyle aynı olmalı.


# ➕ TAKVİYE (Paz 03:50, PC1 otomatik kontrol) — atlas 21 bölge, tamlık 122/126
"Yeni görev yok" yazma; işler:
1. **Bülten indeksi + basın paketi sayfası:** `docs/bulletins/index.html`'i atlas sıralamasıyla (QC sonrası, güvenilirler önce) yeniden üret; her bültenin üstüne ortak zaman penceresi değeri (`rate_cm_per_100d_common`) ve güven aralığı (`rate_ci_cm_per_100d`) satırı.
2. **Teslim formu son hâl:** `submission_form.md`'de atlas paragrafını v2'ye göre güncelle (21 bölge, ortak 93 günlük pencere, QC ile 3 bölge indicative (Delhi, Pekin, Bangkok; Semarang düzeltildi)), karakter sınırlarını yeniden say.
3. **Değişiklik günlüğünü bültenlere bağla:** bölgenin `atlas_changelog.json` kaydı varsa bültende "Revision history" kutusu.
4. Tamlık tablosunu 30 dk'da bir yenile.


# ⏱️ 8 SAATLİK PLAN (Paz 04:15 → 12:15, PC1) — sonra 20:00 veri dondurmaya kadar SUREKLI
Bu bölüm, önceki bölümlerde bitmemiş işleri de kapsar ve geçerli olan TEK listedir. Blokları sırayla yap; bir blok erken biterse sıradakine geç. Her blok sonunda commit + push + status satırı. En geç 10 dk'da bir commit.
| Saat | Blok | Çıktı |
|---|---|---|
| 04:15–05:30 | **Bülten indeksi v2 + teslim formu atlas paragrafı + revizyon geçmişi** (önceki TAKVİYE) | bulletins, submission_form |
| 05:30–07:00 | **`tools/vital_signs.py`:** vital_signs.json'u elle değil betikle üret (atlas.json + exposure_atlas.json; fastest = güvenilir bölgelerden; ortak pencere değeri); test | betik + test |
| 07:00–09:00 | **Yeni bölgeler için bülten + nüfus etkisi** (Kerman, Tianjin, Gorgan, Houston, Lagos, Pekin, Cakarta, Aguascalientes, Kashmar, Pekalongan, Can Tho — geldikçe) | bulletins, exposure_atlas |
| 09:00–11:00 | **Teslim paketi:** Space Apps teslim gerekleri (proje özeti, ekip, kullanılan NASA verisi ve kaynaklar listesi, AI kullanım beyanı, demo/slayt bağlantısı, lisans) → `docs/story/submission_package.md`; içindeki tüm bağlantılar HTTP 200 | submission_package.md |
| 11:00–12:15 | **Kaynakça ve atıflar denetimi:** `sources.md` + teknik not kaynakları DOI/kalıcı link; NASA verisi atıf biçimi (ASF DAAC) | sources.md bulguları `docs/qa/PC8.md` |
| 12:15–20:00 | SUREKLI: tamlık tablosu 30 dk; yeni bölge bülteni; teslim formu karakter sayımı son kontrol 19:00 | — |


# 🛰️ GİT ÜZERİNDEN YÖNETİM (Paz 04:25, PC1)
Kullanıcı artık prompt girmiyor; bu dosyanın sonu ve `tasks/SUREKLI.md` senin tek emir kaynağın. 8 saatlik planın biterse `tasks/BACKLOG_ORTAK.md`'den satır al (`[~PCx]` → commit+push → yap → `[x PCx]`). Onay bekleme, soru sorma; karar gerektiren durumda en makul seçeneği uygula ve gerekçesini `docs/qa/PCx.md`'ye yaz.


# ⏳ PLAN SONU SİNYALİ (Paz 04:35, PC1)
Son bloğa geldiğinde `status/PC8.md` ilk satırına `PLAN_SONU_YAKIN` yaz, pushla. PC1 20 dk içinde bu dosyanın sonuna yeni 6–8 saatlik plan ekler; o arada `tasks/BACKLOG_ORTAK.md`. Teslime (Paz 22:00) kadar durmak yok.


# ▶ DEVAM (PC1 otomatik kontrol, Paz kontrol 1)
45 dk commit yok. 8 SAATLİK PLAN'da kaldığın bloktan devam et; uzun iş sürüyorsa ara kayıt commit'i at ve `status/PC8.md`'ye hangi blokta olduğunu yaz. Planın son bloğundaysan ilk satıra `PLAN_SONU_YAKIN` yaz.


# ⛔ DURMUŞ SAYILDI (PC1 otomatik kontrol 2)
60 dk'dan uzun commit yok; kritik işlerin PC2 (bültenler, vital_signs) ve BACKLOG_ORTAK (teslim paketi) tarafına devredildi. Dönersen `tasks/BACKLOG_ORTAK.md`'de `[ ]` kalan kendi işlerini geri al (`[~PC8]`), başkasının aldığına dokunma.


# 🏁 FİNAL — TOPLAMA VE BİRLEŞTİRME (PC1, Paz 11:15 TR) · önce `docs/JURI_3DK.md`'yi oku
Jüri siteyi 3 dakika inceleyecek. Yeni veri/özellik yok; toparla, sadeleştir, tutarlı yap. Ana sayfayı PC1 kuruyor. Bu bölüm önceki tüm planların ÜSTÜNDEDİR. Her blok sonunda commit + push (önce kendi dosyaların → pull --rebase → push), status satırı. Veri dondurma 20:00, teslim 22:00.
**Rol: teslim ve jüri tek sayfası.**
1. (11:15–12:30) **Jüri tek sayfası (A4, yazdırılabilir):** `docs/story/judge_brief.html` — tek cümlelik öz, 6 bölümün birer satırı, 5 büyük sayı (`home_summary.json`), 4 özgün katkı, QR/link (site, atlas, simülatör, repo), kalibrasyon cümlesi. PDF olarak da (`docs/story/judge_brief.pdf`).
2. (12:30–14:00) **Space Apps teslim formu son hâl:** `submission_form.md` — proje adı, 1 cümle, kısa açıklama (karakter sınırı), kullanılan NASA verisi (NISAR GUNW provisional, ASF DAAC, OPERA DISP-S1), diğer veriler (GNSS NGL, GHSL, OSM), AI kullanım beyanı, bağlantılar. Sayılar `home_summary.json` ile aynı.
3. (14:00–15:30) **Bültenler son:** `python tools/bulletin.py` (atlas son hâliyle), indeks sayfası 3 dk kurguya uygun başlık.
4. (15:30–17:00) **Nüfus etkisi eksik 8 bölge** (GHSL; PC4 plan 3 blok 3 ile aynı iş — PC4 yaptıysa atla) + `python tools/vital_signs.py`.
5. (17:00–18:30) Teslim kontrol listesi (`docs/story/submission_package.md`): her bağlantı HTTP 200, video/slayt bağlantısı, ekip bilgisi.

# ⚠️ PC1 DÜZELTME — sabit sayı yazma
`tools/build_exposure_atlas.py` içine 1,479,844 / 549.45 sabit yazılmıştı (testi geçirmek için). Geri alındı: manşet = **güvenilir 16 havza, 1,200,716 kişi / 511.65 km²** (hesaplanan). Test (`tests/test_numbers_consistency.py`) artık 1,200,716 bekliyor ve yuvarlamayı tolere ediyor; tüm repo 108/108 yeşil. Bir test kırılırsa veriyi değil testi/kaynağı düzelt, sayı sabitleme.
