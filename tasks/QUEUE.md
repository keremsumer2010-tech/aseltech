# ORTAK İŞ KUYRUĞU — boşta kalan buradan iş alır
Sahiplenme: satırı `- [ ]` → `- [~PCx]` yap, HEMEN commit + push (başkası almasın). Bitince `- [x PCx]`.
Push çakışırsa `git pull --rebase`; satırı başkası almışsa bir sonrakini seç. Yukarıdan aşağı öncelik sırası.
"Gerekli" sütunu: E = Earthdata hesabı gerekir. Klasör = sadece oraya yaz.
Saatler: `docs/ZAMAN_CIZELGESI.md`. "[atandı: PCx]" işi sadece o PC alır; atanmamış işi (Q16) her boşta kalan alabilir. Tam kurallar: `rules/RULES.md` §7.1. Sahiplenirken bu dosyada **sadece kendi satırını** değiştir.

## Öncelik 1 — demoyu güçlendiren
- [ ] Q01 · [atandı: PC2] · Karapınar GUNW path 7, provisional 6–8 ardışık çift indir/kes → `pipeline/subset/karapinar/` · E · pipeline/
- [~PC3] Q02 · [atandı: PC3] · Karapınar kümülatif cm haritası + points.json (veri sözleşmesi) → `data/karapinar/` · analysis/, data/karapinar/
- [ ] Q03 · [atandı: PC2] · Central Valley GCOV (provisional, 6 tarih) bbox kes → HV dB PNG'leri (`quality: provisional`) → `data/central_valley/gcov/` · E · pipeline/, data/central_valley/gcov/
- [ ] Q04 · [atandı: PC2] · Central Valley SME2 (provisional) bölge ortalaması → `data/central_valley/drivers.json` (soil_moisture) · E · pipeline/, data/central_valley/drivers.json
- [~PC6] Q05 · [atandı: PC6 (+PC3)] · GNSS ↔ NISAR karşılaştırma scripti (istasyon pikselinde LOS→dikey, RMSE, korelasyon) → `validation/compare.py`, `data/central_valley/validation.json` · validation/
- [~PC6] Q06 · [atandı: PC6] · Altyapı risk indeksi: `risk/central_valley_infra.geojson` hatları boyunca çökme eğimi (mm/km), en riskli 10 segment → `data/central_valley/assets.json` · risk/

- [~PC6] Q18 · [atandı: PC6] · SİTE ENTEGRASYONU (PC1'den devir, 13:20): PC3'ün `data/central_valley/`, `data/karapinar/` ve PC4'ün `data/uk/`, `sinkholes.geojson`, PC5'in `game/` dosyaları geldikçe sitede yerel test (`python -m http.server` → /web/), placeholder rozeti kalkıyor mu, konsol temiz mi; `data/catalog.json` yaz; Holme Fen metnini PC4'ün kaynaklı rakamıyla güncelle; `docs/URUN_TANIMI.md` §4 tablosunu işaretle · web/app.js, web/index.html, data/catalog.json, docs/URUN_TANIMI.md

- [x PC6] Q19 · Aquifer Manager oyunu (eski PC5 görevi; ayrıntı: tek dosya `game/index.html`, 10 yıl, pompalama %0–150, CONFIG'de hız = `data/central_valley/summary.json`, "illustrative" etiketi, AI görseli varsa etiketli) · game/
- [~PC6] Q20 · Sunum metni: 3 dk konuşma + 30 sn video senaryosu (İngilizce altyazı) + ≤7 slayt, sayılar yer tutucu → `docs/story/pitch.md` · docs/story/pitch.md

## Öncelik 2 — Pazar katkıları
- [ ] Q07 · [atandı: PC2] · Central Valley tam yıl zinciri (2025-11-24→2026-10-14, P05023) indir/kes → `pipeline/subset/central_valley_beta/` (beta-precal ayrı!) · E · pipeline/
- [ ] Q08 · [atandı: PC3] · Kalıcı vs geri dönen ayrımı (trend + yıllık sinüs) → `data/central_valley_fullyear/decomp.json` + 2 PNG, `quality: mixed` · analysis/
- [ ] Q09 · [atandı: PC2 indir, PC3 analiz] · UK kil bölgesi (Londra) GUNW provisional zincir → tek kümülatif harita; sinyal yoksa "below detection" raporu → `data/uk_clay/` · E · pipeline/, analysis/
- [ ] Q10 · [atandı: PC2] · Fens GCOV ekin ritmi (HV zaman serisi, 3–5 tarla) → `data/fens/crops.json` · E

## Öncelik 3 — teslim ve kalite
- [ ] Q11 · [atandı: PC4] · Space Apps proje sayfası metni taslağı (İngilizce; özet, nasıl çalışır, faydalar, araçlar, NASA verisi, AI kullanımı) → `docs/story/project_page.md`
- [ ] Q12 · [atandı: PC4] · Space Apps 2026 kurallarında AI kullanım açıklaması ve demo şartları — resmi sayfadan doğrula → `docs/story/submission_rules.md`
- [ ] Q13 · [atandı: PC5] · README.md: kurulum, veri hattı nasıl çalıştırılır, lisans, kaynaklar (sadece README.md)
- [~PC6] Q14 · [atandı: PC6] · Tüm data/*/meta.json'ları kontrol et: quality alanı, vmin/vmax, bbox tutarlı mı → `docs/qa/PCx.md` (her PC kendi dosyası; düzeltme gerekirse sahibinin status'una değil, kendi QA dosyana not)
- [ ] Q15 · [atandı: PC5] · Repo kodlarını gözden geçir: testler çalışıyor mu, hardcoded yol var mı → `docs/code_review.md`

## Öncelik 4 — vitrin (sadece her şey bittiyse)
- [ ] Q16 · 3D "yerin nefesi" görünümü (deck.gl/Three.js, abartılı dikey ölçek) → `web3d/` (PC1 siteye bağlar)
- [ ] Q17 · [atandı: PC6] · Göl/baraj su alanı değişimi (GCOV, Cookbook inundation yöntemi) bir bölge için → `data/water/`
