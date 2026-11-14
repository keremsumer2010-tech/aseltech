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
Ayrıntılar: `docs/SORUN_KAYDI.md` (her maddenin "Nerede / Sorun / Öneri" kısmı). Koordinatör: PC3. Atlas ekibi (PC1, PC2, PC4, PC5, PC9, PC10) bu bölüme dokunmaz.
Her PC sadece kendi `[atandı]` satırlarını yukarıdan aşağı yapar: `- [ ]` → `- [~PCx]` (commit+push) → bitince satırı kuyruktan **SİL** ve yaptığını `docs/qa/PCx.md`'ye yaz. Madde zaten düzeltilmişse satırı sil, qa'ya "zaten düzeltilmiş" yaz, sıradakine geç.

### PC8 — site (web/index.html, web/app.js, web/science.html, web/style.css, .github/workflows/pages.yml)
- [~PC8] B04 · [atandı: PC8] · S-13 Kritik · Central Valley haritası göstergesine boşluk açıklaması + Corcoran metnini dürüstleştir
- [ ] B05 · [atandı: PC8] · S-08 Kritik · UK bölümü: bulutsuz altlık hikâyeyle çelişiyor → bulutlu VIIRS görüntüsünü haritaya oturt ya da altlığı sadeleştir + not
- [ ] B06 · [atandı: PC8] · S-03 Yüksek · Mavi alanların anlamı: göstergeye ve video altyazısına tek cümle
- [ ] B07 · [atandı: PC8] · S-25 Yüksek · science.html "12 to 36 days" → "12 to 24 days" (track 114 aralıklarını da kontrol et)
- [ ] B08 · [atandı: PC8] · S-07 Orta · `web/app.js` `NOISE_CM` eşiği: 1–3 cm arası için "small change, close to the noise"
- [ ] B09 · [atandı: PC8] · S-12 Orta · UK Figure 1: çizgi ortada başlasın, etiketler okunur olsun
- [ ] B10 · [atandı: PC8] · S-09 Orta · UK radar renklerinin anlamı (tek sade cümle)
- [ ] B11 · [atandı: PC8] · S-10 Orta · UK radar katmanına maxZoom sınırı (pikselleşmesin)
- [ ] B12 · [atandı: PC8] · S-11 Orta · UK radar katmanı: yer adı etiketleri (The Wash, Peterborough, King's Lynn, Holme Fen), sert kenar
- [ ] B13 · [atandı: PC8] · S-30 Orta · science.html'de ham Markdown/LaTeX (`$n$`, `**`) var mı: tarayıcıda bak, düzelt
- [ ] B14 · [atandı: PC8] · S-16 Düşük · CV grafiğinde seçili tarihi dikey çizgiyle işaretle
- [ ] B15 · [atandı: PC8] · S-23 En son · TR/EN dil desteği — SADECE B01–B14 ve PC6 listesi bitince; önce PC3'e sor

### PC6 — veri, analiz, metin, video (data/, analysis/pc6/, risk/, validation/, docs/story/*.md, docs/story/media/)
- [~PC6] B19 · [atandı: PC6] · S-26 Yüksek · key_findings.md Karapınar farkı: 3.45 / 3.33 cm → 3.51 / 3.38 cm
- [ ] B20 · [atandı: PC6] · S-27 Yüksek · "High risk" tanımı: `risk/compute_risk.py`'deki gerçek kural → key_findings.md ve science.html aynı cümle
- [ ] B21 · [atandı: PC6] · S-28 Yüksek · key_findings.md "-0.75 to -1.17 cm accuracy" → "0.75 to 1.17 cm (RMSE)"
- [ ] B22 · [atandı: PC6] · S-29 Yüksek · Referans aralığı her yerde tek değer (`summary.json` `range_cm`). `docs/story/key_findings_public.md`'ye DOKUNMA (Mehmet'in metni; PC3 bakıyor)
- [ ] B23 · [atandı: PC6] · S-17 Yüksek · Yumuşatılmış çökme PNG'leri (7×7 NaN-duyarlı ortalama + hafif Gauss) → `data/central_valley/disp_smooth/`, `data/karapinar/disp_smooth/`; sitede saydamlık 0.6–0.65 + "Detailed / Smoothed" düğmesi
- [ ] B24 · [atandı: PC6] · S-14 Yüksek · p04 noktası boşluk kenarında: %90+ geçerli bloğa taşı ya da "estimated from surrounding pixels" notu
- [ ] B25 · [atandı: PC6] · S-15 Yüksek · Başlık değeri haritanın kenarında: p02 (Lemoore'un 21 km güneyi) ile birlikte anılacak metin önerisi
- [ ] B26 · [atandı: PC6] · S-02 Yüksek · Videoda siyah alanlar → açık gri + gösterge ("Grey = no reliable radar signal"), `analysis/pc6/make_animation.py`
- [ ] B27 · [atandı: PC6] · S-01 Orta · Videodaki "Peak P01" etiketi → karedeki gerçek en derin nokta
- [ ] B28 · [atandı: PC6] · S-04 Orta · Video başlığı "Central Valley (San Joaquin Valley), CA"
- [ ] B29 · [atandı: PC6] · S-05 Orta · Videonun alt kaynak satırını yukarı al (kontrol çubuğunun altında kalmasın)
