# ORTAK İŞ KUYRUĞU — boşta kalan buradan iş alır
Sahiplenme: satırı `- [ ]` → `- [~PCx]` yap, HEMEN commit + push (başkası almasın). Bitince satırı kuyruktan **SİL** (yapılanı `status/PCx.md` ve `docs/qa/PCx.md`'ye yaz).
Push çakışırsa `git pull --rebase`; satırı başkası almışsa bir sonrakini seç. Yukarıdan aşağı öncelik sırası.
"Gerekli" sütunu: E = Earthdata hesabı gerekir. Klasör = sadece oraya yaz.
Saatler: `docs/ZAMAN_CIZELGESI.md`. "[atandı: PCx]" işi sadece o PC alır; atanmamış işi (Q16) her boşta kalan alabilir. Tam kurallar: `rules/RULES.md` §7.1. Sahiplenirken bu dosyada **sadece kendi satırını** değiştir.

## Öncelik 2 — Pazar katkıları
- [~PC7] Q10 · [atandı: PC7] · Fens GCOV ekin ritmi (HV zaman serisi, 3–5 tarla) → `data/fens/crops.json` · E

## Öncelik 4 — vitrin (sadece her şey bittiyse)
- [ ] Q17 · [atandı: PC7] · Göl/baraj su alanı değişimi (GCOV, Cookbook inundation yöntemi) bir bölge için → `data/water/`

## ORTAK İŞLER (Cmt 22:10, PC belirtilmeden — boşta kalan herkes alabilir)
PC6 ve PC8'in eski, bitmemiş işleri buraya taşındı. Ayrıntı: `docs/ATLAS_PLANI.md`. Sahiplen: `- [ ]` → `- [~PCx]`; bitince satırı sil.
- [ ] C01 · Atlas sayfası: `web/atlas.html` + `web/atlas.js` + `web/atlas.css` — MapLibre küre (sabit sürüm), `../data/global/atlas.json` noktaları, renk/sıra `rate_cm_per_100d`, güven rozeti (low → "indicative only"), tıklayınca yan panel (dönem, çift sayısı, kalite, kaynak, PNG, bülten `docs/bulletins/`) · web/atlas.*
- [ ] C02 · Atlas sayfasına "Fastest-sinking places in our 2026 NISAR atlas" tablosu: güvenilir ve indicative iki liste, dönem, "LOS", provisional uyarısı (C01'den sonra) · web/atlas.*
- [ ] C03 · Tüm sayfaların menüsüne "Atlas" bağlantısı + ana sayfaya tek özet kartı + Data sayfasına `data/global/atlas.json` bağlantısı (C01'den sonra; küçük değişiklik) · web/*.html
- [ ] C04 · Atlas sayfası testi: telefon 375 px, dizüstü, konsol 0 hata, NaN/boş alan sayfayı bozmasın → `docs/qa/PCx.md` · web/atlas.*
- [ ] C05 · `atlas.json`'a yeni şehir eklendikçe `tools/bulletin.py` ile o şehrin bültenini üret (şu an 8/8 bölgede bülten var) · docs/bulletins/
- [ ] C06 · O1 Karapınar kalıcı depolama kaybı: `data/karapinar_fullyear/decomp.json` oluşunca `analysis/pc8/storage_loss.py` ile → `data/karapinar_fullyear/storage_loss.json` · data/karapinar_fullyear/

## BUGFIX — Sorun Kaydı (Cmt 22:00, Mehmet kararı) · SADECE PC6 ve PC8
Ayrıntılar: `docs/SORUN_KAYDI.md` (her maddenin "Nerede / Sorun / Öneri" kısmı). Yeni eklenen her satırda **Sorun** ve **Çözüm** kısa yazılır (koordinatör kuralı). Koordinatör: PC3. Atlas ekibi (PC1, PC2, PC4, PC5, PC9, PC10) bu bölüme dokunmaz.
Her PC sadece kendi `[atandı]` satırlarını yukarıdan aşağı yapar: `- [ ]` → `- [~PCx]` (commit+push) → bitince satırı kuyruktan **SİL** ve yaptığını `docs/qa/PCx.md`'ye yaz. Madde zaten düzeltilmişse satırı sil, qa'ya "zaten düzeltilmiş" yaz, sıradakine geç.

### PC8 — site (web/index.html, web/app.js, web/science.html, web/style.css, .github/workflows/pages.yml)
- [ ] B34 · [atandı: PC8] · S-34 Yüksek · Sekme değiştirip dönünce sayfa kaydırması çalışmıyor. **Sorun:** başka sekmeye/uygulamaya geçip siteye dönünce fare tekerleği/dokunmatik kaydırma tepki vermiyor; sayfada bir yere tıklayınca sayfa bir anda kayıp gidiyor (kullanıcı "site dondu" sanıyor). **Olası sebepler (sırayla dene):** (1) `html{scroll-behavior:smooth}` (`web/style.css`) + ağır yeniden çizim kaydırmayı kuyruğa alıyor; (2) sekme gizliyken zamanlayıcı/`requestAnimationFrame` döngüleri (hero, story haritası `flyTo`) birikiyor, görününce hepsi birden çalışıyor; (3) MapLibre haritası fare tekerleğini yakalıyor (`scrollZoom`) ve sayfa kaymıyor; (4) açık iframe (simülatör) odağı alıyor (`f.focus()`); (5) videolar. **Çözüm:** önce Chrome'da yeniden üret (sekme değiştir → geri dön → tekerlek, tuş, dokunma; harita üstünde ve dışında ayrı dene), sebebi bul. Olası düzeltmeler: `scroll-behavior:smooth` sadece bağlantı tıklamalarında JS ile; `document.visibilitychange` ile döngüleri/animasyonları durdur-başlat; haritalarda `scrollZoom: false` ya da `cooperativeGestures: true`; iframe'e `f.focus()` yerine odak verme. Düzeltince aynı adımlarla masaüstünde ve telefonda test et ve `docs/qa/PC8.md`'ye hangi sebep çıktığını yaz · web/app.js, web/style.css, web/index.html
- [ ] B15 · [atandı: PC8] · S-23 En son · TR/EN dil desteği — SADECE B01–B14 ve PC6 listesi bitince; önce PC3'e sor

### PC6 — veri, analiz, metin, video (data/, analysis/pc6/, risk/, validation/, docs/story/*.md, docs/story/media/)
*(BUGFIX listesi tamamlandı)*
