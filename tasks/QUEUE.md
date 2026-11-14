# ORTAK İŞ KUYRUĞU — boşta kalan buradan iş alır
Sahiplenme: satırı `- [ ]` → `- [~PCx]` yap, HEMEN commit + push (başkası almasın). Bitince `- [x PCx]`.
Push çakışırsa `git pull --rebase`; satırı başkası almışsa bir sonrakini seç. Yukarıdan aşağı öncelik sırası.
"Gerekli" sütunu: E = Earthdata hesabı gerekir. Klasör = sadece oraya yaz.
Tam kurallar: `rules/RULES.md` §7.1. Sahiplenirken bu dosyada **sadece kendi satırını** değiştir.

## Öncelik 1 — demoyu güçlendiren
- [ ] Q01 · Karapınar GUNW path 7, provisional 6–8 ardışık çift indir/kes → `pipeline/subset/karapinar/` · E · pipeline/
- [ ] Q02 · Karapınar kümülatif cm haritası + points.json (veri sözleşmesi) → `data/karapinar/` · analysis/, data/karapinar/
- [ ] Q03 · Central Valley GCOV (provisional, 6 tarih) bbox kes → HV dB PNG'leri (`quality: provisional`) → `data/central_valley/gcov/` · E · pipeline/, data/central_valley/gcov/
- [ ] Q04 · Central Valley SME2 (provisional) bölge ortalaması → `data/central_valley/drivers.json` (soil_moisture) · E · pipeline/, data/central_valley/drivers.json
- [ ] Q05 · GNSS ↔ NISAR karşılaştırma scripti (istasyon pikselinde LOS→dikey, RMSE, korelasyon) → `validation/compare.py`, `data/central_valley/validation.json` · validation/
- [ ] Q06 · Altyapı risk indeksi: `risk/central_valley_infra.geojson` hatları boyunca çökme eğimi (mm/km), en riskli 10 segment → `data/central_valley/assets.json` · risk/

## Öncelik 2 — Pazar katkıları
- [ ] Q07 · Central Valley tam yıl zinciri (2025-11-24→2026-10-14, P05023) indir/kes → `pipeline/subset/central_valley_beta/` (beta-precal ayrı!) · E · pipeline/
- [ ] Q08 · Kalıcı vs geri dönen ayrımı (trend + yıllık sinüs) → `data/central_valley_fullyear/decomp.json` + 2 PNG, `quality: mixed` · analysis/
- [ ] Q09 · UK kil bölgesi (Londra) GUNW provisional zincir → tek kümülatif harita; sinyal yoksa "below detection" raporu → `data/uk_clay/` · E · pipeline/, analysis/
- [ ] Q10 · Fens GCOV ekin ritmi (HV zaman serisi, 3–5 tarla) → `data/fens/crops.json` · E

## Öncelik 3 — teslim ve kalite
- [ ] Q11 · Space Apps proje sayfası metni taslağı (İngilizce; özet, nasıl çalışır, faydalar, araçlar, NASA verisi, AI kullanımı) → `docs/story/project_page.md`
- [ ] Q12 · Space Apps 2026 kurallarında AI kullanım açıklaması ve demo şartları — resmi sayfadan doğrula → `docs/story/submission_rules.md`
- [ ] Q13 · README.md: kurulum, veri hattı nasıl çalıştırılır, lisans, kaynaklar (sadece README.md)
- [ ] Q14 · Tüm data/*/meta.json'ları kontrol et: quality alanı, vmin/vmax, bbox tutarlı mı → `docs/qa/PCx.md` (her PC kendi dosyası; düzeltme gerekirse sahibinin status'una değil, kendi QA dosyana not)
- [ ] Q15 · Repo kodlarını gözden geçir: testler çalışıyor mu, hardcoded yol var mı → `docs/code_review.md`
