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
