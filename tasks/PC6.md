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
