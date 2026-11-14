# ORTAK İŞ KUYRUĞU — boşta kalan buradan iş alır
Sahiplenme: satırı `- [ ]` → `- [~PCx]` yap, HEMEN commit + push (başkası almasın). Bitince `- [x PCx]`.
Push çakışırsa `git pull --rebase`; satırı başkası almışsa bir sonrakini seç. Yukarıdan aşağı öncelik sırası.
"Gerekli" sütunu: E = Earthdata hesabı gerekir. Klasör = sadece oraya yaz.
Saatler: `docs/ZAMAN_CIZELGESI.md`. "[atandı: PCx]" işi sadece o PC alır; atanmamış işi (Q16) her boşta kalan alabilir. Tam kurallar: `rules/RULES.md` §7.1. Sahiplenirken bu dosyada **sadece kendi satırını** değiştir.

## Öncelik 1 — demoyu güçlendiren
- [x PC2] Q01 · [atandı: PC2] · Karapınar GUNW path 7, provisional 6–8 ardışık çift indir/kes → `pipeline/subset/karapinar/` · E · pipeline/
- [x PC3] Q02 · [atandı: PC3] · Karapınar kümülatif cm haritası + points.json (veri sözleşmesi) → `data/karapinar/` · analysis/, data/karapinar/
- [x PC2] Q03 · [atandı: PC2] · Central Valley GCOV (provisional, 6 tarih) bbox kes → HV dB PNG'leri (`quality: provisional`) → `data/central_valley/gcov/` · E · pipeline/, data/central_valley/gcov/
- [x PC2] Q04 · [atandı: PC2] · Central Valley SME2 (provisional) bölge ortalaması → `data/central_valley/drivers.json` (soil_moisture) · E · pipeline/, data/central_valley/drivers.json
- [x PC6] Q05 · [atandı: PC6 (+PC3)] · GNSS ↔ NISAR karşılaştırma scripti (istasyon pikselinde LOS→dikey, RMSE, korelasyon) → `validation/compare.py`, `data/central_valley/validation.json` · validation/
- [x PC6] Q06 · [atandı: PC6] · Altyapı risk indeksi: `risk/central_valley_infra.geojson` hatları boyunca çökme eğimi (mm/km), en riskli 10 segment → `data/central_valley/assets.json` · risk/

- [x PC1] Q18 · [14:00 site PC1'e döndü; PC6 web/ dosyalarına YAZMAZ] · SİTE ENTEGRASYONU (PC1'den devir, 13:20): PC3'ün `data/central_valley/`, `data/karapinar/` ve PC4'ün `data/uk/`, `sinkholes.geojson`, PC5'in `game/` dosyaları geldikçe sitede yerel test (`python -m http.server` → /web/), placeholder rozeti kalkıyor mu, konsol temiz mi; `data/catalog.json` yaz; Holme Fen metnini PC4'ün kaynaklı rakamıyla güncelle; `docs/URUN_TANIMI.md` §4 tablosunu işaretle · web/app.js, web/index.html, data/catalog.json, docs/URUN_TANIMI.md

- [x PC6] Q19 · [atandı: PC6 — v2 SIFIRDAN, bkz. docs/OYUN_SPEC.md] · Aquifer Manager oyunu (eski PC5 görevi; ayrıntı: tek dosya `game/index.html`, 10 yıl, pompalama %0–150, CONFIG'de hız = `data/central_valley/summary.json`, "illustrative" etiketi, AI görseli varsa etiketli) · game/
- [x PC6] Q20 · Sunum metni: 3 dk konuşma + 30 sn video senaryosu (İngilizce altyazı) + ≤7 slayt, sayılar yer tutucu → `docs/story/pitch.md` · docs/story/pitch.md

## 14:00 EK İŞLER (Mehmet'in ajanları boş kalmasın — sırayla)
- [ ] Q21 · [atandı: PC3] · İKİNCİ GEÇİŞLE DOĞRULAMA: Central Valley GUNW **path 114** provisional ardışık çiftleri (kendi fetch_subset ile) → kümülatif → path 34 sonucuyla aynı noktalarda karşılaştır (fark, korelasyon) → `data/central_valley_p114/` + `docs/qa/PC3.md`. İki bağımsız geometri aynı çökmeyi gösteriyorsa en güçlü kanıtımız bu · analysis/, data/central_valley_p114/
- [ ] Q22 · [atandı: PC3] · Q21 yükselen/alçalan geçişse: iki LOS'tan dikey + doğu-batı ayrıştırması (ortak tarih aralığında) → `data/central_valley/vertical.json` + 1 PNG · analysis/
- [x PC4] Q23 · UK bulut/radar çifti — PC4 13:12'de yaptı (`data/uk/`)
- [x PC4] Q24 · Karapınar 29 kaynaklı obruk — PC4 yaptı
- [x PC4] Q25 · Kaynaklar + kalibrasyon notu — PC4 yaptı
- [ ] Q26 · [atandı: PC5] · Nokta bazında zaman serisi kalitesi: `points.json` her nokta için doğrusal uyum, artık std, en büyük sıçrama (unwrapping şüphesi) → `docs/qa/PC5.md` tablo · analysis/decomp/
- [ ] Q27 · [atandı: PC5] · GNSS doğrulama sonucunun (`data/central_valley/validation.json`) istatistiksel yorumu: RMSE, korelasyon, eğilim farkı; 3 cümle İngilizce → `docs/story/uncertainty.md` · docs/story/uncertainty.md
- [x PC6] Q28 · [atandı: PC6] · Karapınar risk: obruk noktaları (`sinkholes.geojson`) ile PC3 çökme haritası (`data/karapinar/`) ilişkisi — obruk çevresi 1/2/5 km halkalarda ortalama çökme vs bölge geneli; OSM yol/kanal hatlarının obruklara uzaklığı → `data/karapinar/assets.json` + `docs/qa/PC6.md` özet · risk/, data/karapinar/assets.json
- [x PC1] Q29 · İPTAL (oyun v2 ile değişti); telefonda test, `data/central_valley/summary.json` hızını okuyor mu kontrol, küçük hata düzelt (sadece game/) · game/
- [x PC4] Q30 · [atandı: PC4] · `docs/story/pitch.md` ile `project_page.md` sayılarını `data/*/summary.json` ile eşle (CV −7.8 cm LOS / ~−10 cm dikey, Karapınar −5.9 cm LOS); tutarsızlık varsa düzelt · docs/story/
- [x PC4] Q31 · [atandı: PC4] · Holme Fen kartı için tek cümle İngilizce metin + kaynak linki → `docs/story/holme_fen.md` (PC1 siteye koyacak) · docs/story/holme_fen.md

## Öncelik 2 — Pazar katkıları
- [~PC2] Q07 · [atandı: PC2] · Central Valley tam yıl zinciri (2025-11-24→2026-10-14, P05023) indir/kes → `pipeline/subset/central_valley_beta/` (beta-precal ayrı!) · E · pipeline/
- [ ] Q08 · [atandı: PC3] · Kalıcı vs geri dönen ayrımı (trend + yıllık sinüs) → `data/central_valley_fullyear/decomp.json` + 2 PNG, `quality: mixed` · analysis/
- [~PC2] Q09 · [atandı: PC2 indir, PC3 analiz] · UK kil bölgesi (Londra) GUNW provisional zincir → tek kümülatif harita; sinyal yoksa "below detection" raporu → `data/uk_clay/` · E · pipeline/, analysis/
- [~PC7] Q10 · [atandı: PC7] · Fens GCOV ekin ritmi (HV zaman serisi, 3–5 tarla) → `data/fens/crops.json` · E

## Öncelik 3 — teslim ve kalite
- [x PC4] Q11 · [atandı: PC4] · Space Apps proje sayfası metni taslağı (İngilizce; özet, nasıl çalışır, faydalar, araçlar, NASA verisi, AI kullanımı) → `docs/story/project_page.md`
- [x PC4] Q12 · [atandı: PC4] · Space Apps 2026 kurallarında AI kullanım açıklaması ve demo şartları — resmi sayfadan doğrula → `docs/story/submission_rules.md`
- [x PCQ] Q13 · [atandı: PCQ] · README.md: kurulum, veri hattı nasıl çalıştırılır, lisans, kaynaklar (sadece README.md)
- [x PC6] Q14 · [atandı: PC6] · Tüm data/*/meta.json'ları kontrol et: quality alanı, vmin/vmax, bbox tutarlı mı → `docs/qa/PCx.md` (her PC kendi dosyası; düzeltme gerekirse sahibinin status'una değil, kendi QA dosyana not)
- [x PCQ] Q15 · [atandı: PCQ] · Repo kodlarını gözden geçir: testler çalışıyor mu, hardcoded yol var mı → `docs/code_review.md`

## Öncelik 4 — vitrin (sadece her şey bittiyse)
- [x PC4] Q16 · 3D "yerin nefesi" görünümü (deck.gl/Three.js, abartılı dikey ölçek) → `web3d/` (PC1 siteye bağlar)
- [ ] Q17 · [atandı: PC7] · Göl/baraj su alanı değişimi (GCOV, Cookbook inundation yöntemi) bir bölge için → `data/water/`
