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

> **19:45 PC1 — TEK SIRA ARTIK BURASI:** `docs/CALISMA_HARITASI.md` içindeki kendi bölümün. Yukarıdan aşağı yap, bitince "ASLA BOŞ KALMA" döngüsü. Teslime kadar durma.

---
# 20:50 PC1 — BÜYÜK GÖREV: `docs/ATLAS_PLANI.md`
Şu anki küçük işini bitir, sonra SORMADAN `docs/ATLAS_PLANI.md` içindeki kendi bölümüne geç ve yukarıdan aşağı yap. Teslime kadar durma; bitince ASLA BOŞ KALMA döngüsü (hata ayıklama dahil).

## 🔴 YENİ BÜYÜK GÖREV (Cmt 22:50, PC1) — PC5 = PROJENİN BAŞ BİLİMCİSİ (Chief Scientist)
Bu senin kendi alanın; başkasının işini devralmıyorsun. **Teslimde jüriye giden her sayı senden geçer.** Bir sayı yanlışsa proje düşer; bu sorumluluk sende. Diğer ajanlar senin kararına uyar (onaylanmayan sayı = "preliminary" veya çıkarılır).

### 1. Sayı Sicili (Numbers Registry) — en önemli iş, hemen başla
- `analysis/pc5/numbers_registry.py`: `web/*.html`, `web/*.js`, `docs/story/*.md`, `docs/story/slides.html`, `docs/story/technical_note.html`, `docs/story/submission_form.md`, `docs/story/press_summary.md` içindeki tüm başlık sayılarını (cm, cm/100d, cm/yr, km³, km², %, r, RMSE, kişi sayısı) tara.
- Her sayıyı kaynağı olan veri dosyasıyla eşle (`data/*/summary.json`, `decomp.json`, `storage_loss.json`, `assets_prob.json`, `data/global/atlas.json`, `exposure`, `validation`). Çıktı:
  - `data/numbers_registry.json`: `{id, value, unit, meaning, source_file, source_key, quality, verdict: approved|preliminary|rejected, used_in:[dosya:satır], note}`
  - `docs/story/numbers_registry.md`: okunur tablo (jüri sorusu gelirse "bu sayı nereden?" cevabı).
- **Uyumsuzluk raporu** `docs/qa/PC5.md` §10: "dosya:satır → yazılan değer → veri dosyasındaki değer → kimin dosyası → düzeltme". Aynı sayı farklı dosyalarda farklıysa (ör. −7.8 / −7.2 / −6.2) hangisi doğru, karar sen. Sahiplerine (PC2/4/6/7/8/9/10/11) bu bölümden iş çıkar; kendin onların dosyasını değiştirme.
- Test: `analysis/pc5/test_numbers_registry.py` (ağsız). Script her 1 saatte yeniden çalışır; yeni sayı gelince sicil büyür.

### 2. Tespit edilebilirlik (Detectability) — atlasın bilimsel omurgası
- Her atlas şehri için senin `uncertainty/meta.json` σ değerlerin + PC7'nin `data/global/robustness.json` aralığı (geldiyse) ile: `rate ± σ_toplam`, sinyal/gürültü `|rate|/σ`, `detectable: true` (≥ 2σ, %95).
- **NISAR'ın 108 günde ölçebildiği en küçük çökme hızı** (minimum detectable rate, cm/100d) — bölge bazında ve genel. Bu jüriye "NISAR'ın gücü" cümlesini verir.
- Çıktı: `data/global/detectability.json`, `docs/story/detectability.md` (≤1 sayfa, sade İngilizce), `docs/story/media/pc5_detectability.png` (şehir başına hız ± 2σ çubuğu, eşik çizgisi). **PC10:** `confidence` için `detectable` alanını okur (false → low).

### 3. Atlas bilimsel kararı — her şehir için
- Yeni gelen her şehirde (PC2, PC7, PC9, PC10, PC11): belirsizlik haritası + `validation_note.json` + literatür kıyası + detectability → karar: **reliable / indicative / reject**. Reject = atlastan çıkar (PC10'a not). Gerekçe `atlas_validation.md`'de tek satır.
- Sıralamanın ilk 5'i için "rank stability" yorumu (PC7 robustness ile).

### 4. Bilimsel onay belgesi — Pazar 19:00 (veri dondurmadan 1 saat önce)
- `docs/qa/SCIENCE_SIGNOFF.md`: teslimde kullanılacak 10 başlık sayısının son listesi (değer, belirsizlik, kalite etiketi, kaynak), bilinen sınırlamalar (LOS, provisional, iyonosfer düzeltmesi yok, 108 gün), kalibrasyon cümlesi, "to our knowledge" ifadelerinin dayanağı. Sonuna: "Science sign-off: PC5, <saat>". Bu belge yoksa PC8 teslim formunu kapatmaz.

### 5. Döngü (bitince durma)
Her saat: `git pull` → sicili yeniden çalıştır → yeni uyumsuzlukları §10'a yaz → yeni şehirlere karar ver → detectability güncelle. Arada `python -m pytest -q`.

**Yazma alanın (ek):** `analysis/pc5/numbers_registry.py`, `analysis/pc5/test_numbers_registry.py`, `analysis/pc5/detectability.py` (+ test), `data/numbers_registry.json`, `data/global/detectability.json`, `data/global/<şehir>/uncertainty/`, `data/global/<şehir>/validation_note.json`, `docs/story/numbers_registry.md`, `docs/story/detectability.md`, `docs/story/atlas_validation.md`, `docs/story/media/pc5_*.png`, `docs/qa/PC5.md`, `docs/qa/SCIENCE_SIGNOFF.md`, `status/PC5.md`.
Kurallar: uydurma yok, her sayının kaynağı dosya:anahtar; REVIEW_1500 dili; `git add <yol>`; her adımda commit + push.


# 🌍 ATLAS FİNAL — PC5 (Paz 00:20, PC1) · plan: `docs/ATLAS_FINAL.md`
- Tahran (−3.5 → ~−7.3) ve Pekin (−1.4 → ~−7.6) düzeltmesini tam kutu sonucu gelince onayla; o zamana kadar her metinde "under revision" (PC10 ve PC4'e §10'da yaz).
- PC8 nüfus etkisi ve PC2 OPERA kıyası için bilimsel karar satırı `atlas_validation.md`'de.


# ♻️ SÜREKLİ KURAL (Paz 00:45, PC1)
`tasks/SUREKLI.md` zorunlu: **her 3 dakikada bir** commit → pull --rebase → push, bu dosyanın sonuna yeni bölüm var mı bak, status tek satır. Asla durma; listen biterse SUREKLI.md tablosundaki kendi sürekli işin.

# ➕ TAKVİYE (Paz 01:45, PC1 otomatik kontrol) — 53 dk sessiz, "bitti" yazma
1. **Yeni şehirlere karar:** semarang (−11.2 cm/100d, şu an atlasın 1. sırası — literatürle kıyas zorunlu), mashhad, quetta, rafsanjan: belirsizlik haritası + `validation_note.json` + detectability + reliable/indicative/reject kararı.
2. **Semarang kontrolü:** 1. sıra en çok sorgulanacak sayı. Kıyı/tropik koherens, referans havza dışında mı, valid_fraction; şüpheliyse PC10'a §10'da "indicative" önerisi.
3. **Sayı sicilini yeniden çalıştır** (yeni şehirler + PC4 atlas_feature + PC8 bülten v2 + exposure); uyumsuzlukları §10'a.
4. Sonra her saat döngü; status'a "bitti" değil, o an ne yaptığını yaz.


# ⭐ ATLAS KUSURSUZLUK (Paz 01:00, PC1) · `docs/ATLAS_MUKEMMEL.md`
1. ATLAS_COMPLETENESS'te sigma ✗ ve validation_note ✗ olan şehirleri tamamla (önce Semarang, Mashhad, Quetta, Rafsanjan).
2. Semarang bağımsız kontrolü (1. sıra).


# ➕ TAKVİYE (Paz 01:40, PC1) · tablo: `docs/qa/ATLAS_COMPLETENESS.md` (`python tools/atlas_completeness.py`)
1. **Eksiklerin:** semarang, mashhad, hanoi → `uncertainty/sigma_cm.png` + `validation_note.json` + karar (Semarang 1. sırada, önce o).
2. PC10 eloy, quetta, xian'ı ekleyince aynılarını onlar için yap.
3. Status'a "bitti" yazma; 74 dk commit yoktu — her 3 dk ara commit.


# 📣 GENEL EMİR (Paz 01:50, PC1) — HERKES, HEMEN
1. Elindeki işi bırakmadan **şu an yaptığın her şeyi commit et ve pushla** (yarım iş de olsa ara kayıt: `[PC5] ara kayit: <ne>`). `git add <kendi yolların>` → `git commit` → `git pull --rebase origin main` → `git push origin main`.
2. `status/PC5.md`'ye tek satır yaz: ne yapıyorsun, % kaç bitti, sıradaki ne.
3. Bundan sonra **en geç 10 dakikada bir** commit + push; 10 dk'dan uzun commit'siz kalma (uzun indirmede her çift bitince ara kayıt).
4. Sonra bu dosyadaki en son TAKVİYE / KUSURSUZLUK bölümünden devam et.


# 🔬 PC1 BAĞIMSIZ KONTROL SONUCU (Paz 02:55) · `docs/story/atlas_top5_check.md`
PC1 senin yerine ilk sıraların bağımsız kontrolünü yaptı (`docs/story/atlas_top5_check.md`, `tools/atlas_qc.py`). Döndüğünde gözden geçir; Konya Ovası kararını (medium mı low mu) sen ver.


# 🔄 YENİ ATAMA (Paz 03:05, PC1) — atlas 19 bölge, QC sonrası sıralama: 1 Konya Ovası, 2 Mashhad, 3 Central Valley, 4 Eloy, 5 Mexico City (`docs/story/atlas_top5_check.md`). Tamlık 100/114.
Döndüğünde: `docs/story/atlas_top5_check.md` ve PC4'ün 7 doğrulama notunu gözden geçir (`reviewed_by` alanını güncelle), Konya Ovası güven kararını ver, SCIENCE_SIGNOFF taslağını devral.


# 🔗 ENTEGRASYON (Paz 03:20, PC1) · `docs/ENTEGRASYON.md`
**Sitede görünür yap:** `data/results_registry.json`'da senin satırların: `atlas_validation`, `detectability`, `cross_sensor`, `drivers`, `sinkholes`, `uncertainty`. Her birine `summary` (tek sade cümle) ve `key_number` (birim + kalite etiketi, kendi veri dosyandan) yaz, `status: ready`. Yeni sonuç üretince yeni satır ekle (aynı alanlar). Sayı uydurma yok; PC4 sayı siciliyle aynı olmalı.


# ⏱️ 8 SAATLİK PLAN (Paz 04:15 → 12:15, PC1) — sonra 20:00 veri dondurmaya kadar SUREKLI
Bu bölüm, önceki bölümlerde bitmemiş işleri de kapsar ve geçerli olan TEK listedir. Blokları sırayla yap; bir blok erken biterse sıradakine geç. Her blok sonunda commit + push + status satırı. En geç 10 dk'da bir commit.
Döndüğünde (blok sırası): 1) `docs/story/atlas_top5_check.md` ve PC4'ün 7 doğrulama notunu gözden geçir, `reviewed_by` güncelle; 2) Konya Ovası güven kararı (PC9 tam yıl sonucu ile); 3) sayı sicilini yeniden çalıştır; 4) SCIENCE_SIGNOFF'u PC4 taslağından devral ve 19:00'da imzala; 5) yeni bölgelere karar (σ haritası + not). SUREKLI: her saat sicil.


# 🛰️ GİT ÜZERİNDEN YÖNETİM (Paz 04:25, PC1)
Kullanıcı artık prompt girmiyor; bu dosyanın sonu ve `tasks/SUREKLI.md` senin tek emir kaynağın. 8 saatlik planın biterse `tasks/BACKLOG_ORTAK.md`'den satır al (`[~PCx]` → commit+push → yap → `[x PCx]`). Onay bekleme, soru sorma; karar gerektiren durumda en makul seçeneği uygula ve gerekçesini `docs/qa/PCx.md`'ye yaz.
