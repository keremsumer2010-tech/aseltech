# PC5 — Bilimsel güvenilirlik paketi (14:40'ta yenilendi)

> Eski PC5 işleri (decompose, error_budget, game_model) PC3 tarafından yapıldı. Bu dosya TAMAMEN yenidir; aşağıdaki sırayla çalış, iş bitince sormadan sıradakine geç (RULES §7.1). İNDİRME YAPMA (aynı bilgisayarda PC3 indiriyor): sadece repodaki veriyle çalış.

## Kimlik
M3hmeT1888 · Antigravity (Gemini) · klasör `aseltech-gemini` · commit öneki `[PC5]`

## Yazma alanı
`analysis/pc5/` (kodun) · `data/central_valley/uncertainty/` · `data/karapinar/uncertainty/` · `docs/story/literature_comparison.md` · `docs/story/key_findings.md` · `docs/story/game_sensitivity.md` · `docs/story/risk_sensitivity.md` · `docs/qa/PC5.md` · `status/PC5.md` · QUEUE'da sadece Q26/Q27 satırları.
`analysis/` içindeki diğer dosyalar PC3'ün: import edebilirsin, DEĞİŞTİRME.

## En kritik iş
Görev 1 (belirsizlik haritası) ve Görev 2 (literatür kıyası): jüri "bu sayılara neden güvenelim?" diye sorduğunda cevabımız bunlar.

## Görevler
0. **ŞİMDİ (5 dk):** `git pull --rebase origin main` → status/PC5.md'ye "Durum: çalışıyor, Görev 1" yaz → commit + push. Hiç commit atmadın; ilk iş bu.

1. **Piksel bazında belirsizlik haritası** (14:45–15:45) → `analysis/pc5/uncertainty_map.py`
   - Girdi: `pipeline/subset/central_valley/*.npz` (`coh`, `unw`, `wavelength`; coh uint8 ise /255).
   - Tek çift faz std'si (Cramér-Rao / Rodriguez-Martin yaklaşımı): `σφ = sqrt(1−γ²) / (γ·sqrt(2L))`, L = etkin bakış sayısı (80 m GUNW için ürün dokümanından L'yi bul ve kaynakla; bulamazsan L'yi parametre yap, varsayımını yaz).
   - cm'ye: `σd = λ/(4π)·σφ·100`. Zincir toplamı: `σ_toplam = sqrt(Σ σd_i²)` (bağımsızlık varsayımı; atmosferi KAPSAMAZ, açıkça yaz).
   - Çıktı: `data/central_valley/uncertainty/sigma_cm.png` (bbox'a oturan, şeffaf, sabit renk aralığı), `data/central_valley/uncertainty/meta.json` (`bbox, units:"cm", vmin, vmax, median_sigma_cm, p90_sigma_cm, method, assumptions, quality:"provisional"`).
   - `analysis/pc5/test_uncertainty_map.py`: γ=1 → σ=0, γ↓ → σ↑, bilinen sayısal örnek. pytest geçmeli.
   - Aynısını Karapınar için (`pipeline/subset/karapinar/` varsa) → `data/karapinar/uncertainty/`.

2. **Literatür kıyası** (15:45–16:30) → `docs/story/literature_comparison.md`
   - Central Valley: yayımlanmış InSAR/GPS çökme hızları (NASA JPL, USGS, hakemli makaleler; Tulare/Corcoran bölgesi). Tablo: kaynak, yıl, yöntem, dönem, hız (cm/yıl), link.
   - Karapınar/Konya: yayımlanmış InSAR çökme hızları (hakemli). Aynı tablo.
   - Bizim sonuç: `data/central_valley/summary.json` ve `data/karapinar/summary.json` (108 günlük değer + yıllık "estimate"); hangi aralığa düştüğünü 3–4 cümle İngilizce yorumla. Bizim yıllık tahmin neden yüksek olabilir (yaz sezonu, elastik geri dönüş) açıkla.
   - HER LİNKİ AÇ; açamadığın kaynağı yazma.

3. **Q26 + Q27** (16:30–17:00) — tasks/QUEUE.md'de satırları sahiplen.
   - Q26: `analysis/decomp/point_quality.py` (PC3'ün) varsa onu ÇALIŞTIR, sonuç tablosunu `docs/qa/PC5.md`'ye yaz; yoksa aynı mantığı `analysis/pc5/` altında yaz.
   - Q27: `data/central_valley/validation.json` istatistiksel yorumu → `docs/story/uncertainty.md` SONUNA DEĞİL, `docs/story/key_findings.md` içine bir bölüm olarak: medyan RMSE, r dağılımı, hareketli (|GPS|>2 cm) ve sabit istasyon gruplarında ayrı ayrı. 3 cümle İngilizce.

4. **Anahtar bulgular sayfası** (17:00–17:30) → `docs/story/key_findings.md` (PC1 bunu sitenin Science sayfasına bağlayacak)
   - En fazla 8 madde, her biri: bulgu + sayı ± belirsizlik + dosya kaynağı. Örn. "Largest 108-day subsidence: −7.8 cm LOS (range −6.2…−7.8 with reference choice; per-pixel σ ≈ X cm)".
   - Sadece repodaki dosyalardaki sayılar; uydurma yok.

5. **Risk indeksi duyarlılığı** (17:30–18:30) → `analysis/pc5/risk_sensitivity.py` + `docs/story/risk_sensitivity.md`
   - `data/central_valley/assets.json` özellikleri üzerinden eşikleri ±%25 değiştir (gradyan 7.5/10/12.5 mm/km, çökme 7.5/10/12.5 cm): yüksek riskli segment sayısı nasıl değişiyor? İlk 10'daki segmentler sabit kalıyor mu? Tablo + 3 cümle.

6. **Oyun modeli duyarlılığı** (18:30–19:30) → `analysis/pc5/game_sensitivity.py` + `docs/story/game_sensitivity.md`
   - `docs/story/game_model.md` ve `game/model.js`'teki denklemleri Python'a aktar (game/ dosyalarına DOKUNMA). Monte Carlo (1000 çalıştırma): S_kv, S_ke, b0 parametrelerini kaynaktaki aralıklarda değiştir → 24 aylık toplam çökme dağılımı (p10/p50/p90). Kalibrasyon noktası (−10 cm / 108 gün) hangi parametre bölgesinde? Tablo + histogram PNG (`docs/story/game_sensitivity.png`).

7. **Pazar hazırlığı** (19:30 sonrası): tam yıl verisi (PC2 Q07) gelince `analysis/decomp/run_decomp.py`'yi çalıştırma talimatını ve beklenen çıktıları `docs/qa/PC5.md`'ye yaz; PC3 ile çakışma olmasın diye sadece kontrol listesi.

## Bitti sayılır eğer
Her görevde: kod çalıştı, testler (varsa) geçti, çıktı açılıp kontrol edildi, status/PC5.md'de yöntem + sayılar + varsayımlar yazılı, push edildi.

## Yapma listesi
İndirme yapma · başka PC'nin dosyasını değiştirme · sayı/kaynak uydurma · provisional ile beta'yı karıştırma · `git add -A`.

## Rapor (`status/PC5.md`)
Her görev bitince: ne yapıldı, sayılar, varsayımlar, `AI: Gemini → ...`.

---
# 15:00 not
Yazdığın her İngilizce metin `docs/REVIEW_1500.md` yazım kurallarına uysun. `key_findings.md` sitede Science sayfasına bağlanacak: 8 madde, sade cümle, sayı ± belirsizlik, kaynak dosya.

---
# 15:30 SÜREKLİ PAKET — PC5 HİÇ DURMAZ (7 görevin hepsi bitti, harika; sırayla devam, liste bitince "sonsuz döngü")
Yazma alanına eklendi: `data/central_valley/area_stats.json` · `data/karapinar/area_stats.json` · `docs/story/key_findings_public.md` · `docs/story/sinkhole_stats.md` · `docs/story/drivers_analysis.md` · `docs/story/media/pc5_*.png`. İndirme yok.

1. **Halk dilinde anahtar bulgular** → `docs/story/key_findings_public.md`: `key_findings.md`'nin 8 maddesini her biri TEK cümle, jargon yok (LOS, Cramér–Rao, Pearson gibi terimler yok), sayı + birim + tarih. `docs/REVIEW_1500.md` kurallarına uy. PC1 bunu ana sayfaya koyacak; en önemli iş bu.
2. **Etkilenen alan zaman serisi** → `analysis/pc5/area_stats.py` + `data/central_valley/area_stats.json`, `data/karapinar/area_stats.json`: her tarih için −2 cm ve −5 cm'den fazla çöken alan (km²), maks ve medyan çökme; `{dates, area_km2_lt_2cm:[...], area_km2_lt_5cm:[...], quality, method}`. Grafik `docs/story/media/pc5_area_cv.png`.
3. **Obruk–çökme istatistiksel testi** → `docs/story/sinkhole_stats.md`: PC6'nın halka analizine (`data/karapinar/assets.json`) ek olarak permütasyon/bootstrap testi: obruklara 0–2 km mesafedeki pikseller ile >5 km arka plan arasındaki fark tesadüf olabilir mi? p-değeri, güven aralığı, uzamsal otokorelasyon uyarısı. Sade 3 cümle sonuç.
4. **Sebep analizi** → `docs/story/drivers_analysis.md` + `docs/story/media/pc5_drivers.png`: `data/central_valley/drivers.json` (SME2 toprak nemi, HV, sulama indeksi) ile çökme zaman serisinin gecikmeli korelasyonu; 8 tarihle sınırlı olduğunu açıkça yaz.
5. **Q08 bağımsız kontrolü**: PC3 tam yıl kalıcı/geri dönen ayrımını (`data/central_valley_fullyear/`) üretince sonuçları `analysis/decomp` testleriyle ve fiziksel makullükle kontrol et → `docs/qa/PC5.md`.

## SONSUZ DÖNGÜ (teslime kadar her 30 dk)
a) `git pull`; yeni/değişen `data/*` dosyası varsa belirsizlik haritasını, alan istatistiklerini ve key_findings sayılarını yeniden üret.
b) Sitedeki (`web/*.html`, `docs/story/*.md`) her bilimsel sayıyı veri dosyalarıyla karşılaştır; farkı `docs/qa/PC5.md`'ye yaz (başkasının dosyasına dokunma).
c) `literature_comparison.md` ve `sources.md` linklerini tekrar aç (HTTP 200); kırık olanı raporla.
d) Yapacak şey kalmadıysa: yöntem metnini (Science sayfası `web/science.html`) bilimsel doğruluk açısından oku, düzeltme önerilerini `docs/qa/PC5.md`'ye yaz.
Asla "görev bekleniyor" deme; status'a o an ne yaptığını yaz.

---
# 16:15 CHALLENGE UYUMU — B1 "farklı frekans, diğer sensör" (mevcut döngüden önce)
**L-band (NISAR) vs C-band (Sentinel-1) çökme karşılaştırması** → `analysis/pc5/cross_sensor.py` + `docs/story/cross_sensor.md` + `docs/story/media/pc5_cross_sensor.png`.
- Kaynak: NASA OPERA **DISP-S1** (Sentinel-1 yer değiştirme ürünü, Kuzey Amerika) — ASF'de arama (`asf_search`, shortName/dataset OPERA DISP-S1); Central Valley için 2026-06-28 → 2026-10-14 aralığına en yakın kümülatif değişim. Bu bilgisayarda büyük indirmeyi tek sen yap (PC3 artık indirmiyor); en fazla 1 dosya aynı anda, ham dosyayı kesince sil.
- Ürün bulunamazsa/erişilemezse: Sentinel-1 kapsamasını ve neden yapılamadığını dürüstçe yaz; alternatif olarak koherens karşılaştırması (L-band'in tarım alanında koherensi C-band'den iyi koruması) literatürden kaynaklı anlat.
- Çıktı: aynı noktalarda NISAR vs Sentinel-1 (r, RMSE, eğim), 3–4 cümle sade İngilizce: "two satellites, two radar frequencies, same subsidence".
Yazma alanına eklendi: `pipeline/subset/opera_disp/`, `data/central_valley_s1/`.

> **16:25 PC1 — KAYNAKLAR ENTEGRASYONU:** `docs/KAYNAKLAR_ANALIZI.md`'yi oku; §4'te senin satırındaki işleri mevcut işine ek olarak yap (özellikle §1 NASA Land Subsidence StoryMap çerçevesi). Kendi cümlenle özetle, link ve atıf ver.

> **18:55 PC1:** Lincoln geçti. `docs/AKSAM_PLANI.md`'deki kendi satırına geç (akşam → Pazar). Durma.
