# PC8 — Mehmet'in 3. Antigravity'si · UK KİL ANALİZİ (15:25; test başarılı)

> **15:35 PC1 — DEĞİŞİKLİK:** Q09'u PC3 zaten bitirdi (`data/uk_clay/`, `data/uk_clay/detection.json`: "below detection", σ 1.21 cm, 3σ 3.6 cm). **`data/uk_clay/` dosyalarına YAZMA** (artık PC3'ün). Yeni sıran:
> 1. **UK bulgusu metni ve grafiği** → `docs/story/uk_findings.md` + `docs/story/media/pc8_uk_detection.png`: PC3'ün `detection.json` ve `analysis/out/uk_clay_pair_stats.json` dosyalarından: Londra kil bölgesinde tek yaz sezonunda sinyal ölçüm sınırının altında; neden (beklenen kil hareketi mm–1–2 cm, tespit eşiği 3.6 cm); Holme Fen'in uzun dönem 1–2 cm/yıl çökmesiyle karşılaştırma (kaynak `docs/story/holme_fen.md`); "NISAR'ın birkaç yıllık serisiyle görülebilir" sonucu. Sade İngilizce, 5–6 cümle, REVIEW_1500 kuralları. PC9 siteye koyacak.
> 2. **Karapınar ikinci geçiş (path 172) çapraz kontrolü**: PC2 `pipeline/subset/karapinar_p172/` hazırladığında `analysis/cumulative.py --data-dir data/karapinar_p172` ile çalıştır (yoksa önce PC2'nin status'unu kontrol et, bekleme yerine 1. maddeyi bitir), path 7 sonucuyla karşılaştır → `docs/qa/PC8.md` (r, RMSE, maks fark) + `docs/story/media/pc8_kp_p7_vs_p172.png`. Yazma alanına `data/karapinar_p172/` eklendi.
> 3. Sonra: `docs/qa/*.md` içindeki açık site bulgularını PC9 için tek listede topla → `docs/qa/PC8.md` ("PC9 yapılacaklar"), çakışmayı önlemek için.

> **16:10 PC1 — EK GÖREV (PCQ kapatıldı, işleri sana):** mevcut maddelerin bitince sırayla:
> A. `docs/story/submission_form.md`: `docs/story/submission_rules.md` alanlarına göre (proje adı, kısa/uzun açıklama, nasıl çalışır, faydalar, NASA verisi, diğer veri, araçlar, AI kullanımı, demo linki, repo linki) kopyala-yapıştır hazır İngilizce metin; karakter sınırı varsa uy ve sayısını yaz. Sayılar sadece `data/*/summary.json`, `validation.json`, `assets.json`'dan.
> B. `docs/story/video_subtitles.srt` (SRT, `docs/story/video_shotlist.md` sürelerine göre) + `docs/story/narration_script.md` (~75 kelime). PC6 demo videosuna gömecek.
> Kurallar: sade İngilizce (`docs/REVIEW_1500.md`), uydurma yok. Yazma alanına eklendi: bu üç dosya.

## Kimlik
M3hmeT1888 · Antigravity · klasör `aseltech-gemini3` · commit öneki `[PC8]` · İNDİRME YAPMA.

## Yazma alanı
`data/uk_clay/` · `analysis/pc8/` · `docs/qa/PC8.md` · `status/PC8.md` · QUEUE'da sadece Q09 satırı (analiz kısmı).
`analysis/` içindeki PC3 kodlarını import edebilir/çalıştırabilirsin, DEĞİŞTİRME.

## Görevler (sırayla; bitince sormadan sıradakine)
1. **Q09 UK kil (Londra) kümülatif harita** — PC2 9 provisional çifti hazırladı: `pipeline/subset/` altındaki UK/London klasörü (`ls pipeline/subset/` ile bul; adı ve bbox'ı `status/PC2.md`'de).
   - PC3'ün hattını ÇALIŞTIR: `python analysis/cumulative.py <site_adı> --data-dir data/uk_clay` (parametreleri `analysis/cumulative.py --help` ile kontrol et; site tanımı yoksa kendi küçük sarmalayıcını `analysis/pc8/` altında yaz, PC3 dosyasını değiştirme).
   - Çıktı (veri sözleşmesi biçimi): `data/uk_clay/meta.json`, `disp/<date>.png`, `points.json`, `summary.json` (`quality: provisional`).
2. **Dürüst sonuç** → `data/uk_clay/summary.json` `method_note` + `docs/qa/PC8.md`: sinyal (kil büzülmesi, beklenen mm–1–2 cm) PC5'in piksel belirsizliğinden (~0.3 cm) ve atmosfer gürültüsünden (1–3 cm/çift) ayrılabiliyor mu? Ayrılamıyorsa açıkça **"below detection limit for one season"** yaz — bu da geçerli bir bulgu. 3 cümle İngilizce, sayılarla.
3. **Fens (Holme Fen çevresi) için aynısı** — `pipeline/subset/` altında Fens GUNW varsa; yoksa bu adımı atla ve status'a yaz.
4. **Sürekli:** her 30 dk `git pull`; PC2'nin yeni UK alt kümeleri gelirse yeniden çalıştır; `docs/qa/*.md` içinde uk_clay hakkındaki bulguları düzelt. Bitince QUEUE'da atanmamış iş veya PC1'e status'ta "boştayım" yaz — ama önce kendi çıktını test et ve iyileştir.

Kurallar: `git add data/uk_clay/ analysis/pc8/ docs/qa/PC8.md status/PC8.md`; `git add -A` yasak; git hatasında silme yok, BLOCKED yaz.

---
# 16:15 CHALLENGE UYUMU — B3 "nüfus ve bitki örtüsü/ürün türü" (A/B metin işlerinden sonra)
**Kim ve ne risk altında?** → `analysis/pc8/exposure.py` + `data/central_valley/exposure.json` + `data/karapinar/exposure.json` + `docs/story/exposure.md`:
- Nüfus: açık veri WorldPop (100 m, girişsiz) veya NASA SEDAC GPWv4 (Earthdata ister — bu durumda WorldPop kullan). Çökme > 2 cm ve > 5 cm alanlarda yaşayan kişi sayısı (tahmin; yöntem ve yıl yazılı).
- Ürün türü: Central Valley için USDA Cropland Data Layer (CropScape, açık), Türkiye için ESA WorldCover 10 m (açık). Çöken alanların hangi ürün/arazi türünde olduğu (ilk 5, km²).
- Küçük indirme (bölge kesiti), ham dosyayı commit etme, < 20 MB. Kaynak + lisans satırı. 3–4 cümle sade İngilizce.
Yazma alanına eklendi: `data/*/exposure.json`, `docs/story/exposure.md`, `analysis/pc8/`.

> **18:55 PC1:** Lincoln geçti. `docs/AKSAM_PLANI.md`'deki kendi satırına geç (akşam → Pazar). Durma.

> **19:45 PC1 — TEK SIRA ARTIK BURASI:** `docs/CALISMA_HARITASI.md` içindeki kendi bölümün. Yukarıdan aşağı yap, bitince "ASLA BOŞ KALMA" döngüsü. Teslime kadar durma.

---
# 20:00 PC1 — VERİ DÜZELTMELERİ + TESLİM (aktifsin, harika)
1. **JSON NaN hatası (kritik):** `data/central_valley/uncertainty/meta.json` ve `data/karapinar/uncertainty/meta.json` içinde `NaN` var → tarayıcıda `JSON.parse` çöker. PC5 3 saattir sessiz; PC1 izniyle düzelt: `NaN` → `null` (veya alanı kaldır), değerleri değiştirme. Mümkünse üretici script (`analysis/pc5/uncertainty_map.py`) çıktısını yeniden üretmek yerine sadece JSON'u temizleyen küçük bir script yaz (`analysis/pc8/fix_nan_json.py`) ve tüm `data/**/*.json` üzerinde çalıştır.
2. `data/central_valley_s1/cross_sensor.json`: `quality` ve `quality_note` alanı yok → ekle (Sentinel-1/OPERA için kaynak ve "NISAR provisional" notu).
3. **AI kullanım beyanı — PC1 onayı:** `submission_form.md` §AI şu içerikle kesinleşsin: kod, analiz scriptleri ve metinler Anthropic Claude (Claude Code), Google Gemini (Antigravity, Gemini CLI) ve OpenAI Codex yardımıyla yazıldı ve ekip tarafından kontrol edildi; sitede/oyunda AI ile üretilmiş görsel YOK (erken taslaktaki Higgsfield görselleri kaldırıldı); haritalar ve grafikler sadece gerçek veri; her sayı veri dosyasından, her bilimsel iddia kaynaklı.
4. `submission_form.md` + `slides_notes.md`: video yerine slayt (`docs/story/slides.html`) ile teslim senaryosuna göre güncelle; tüm yeni sonuçlar (tam yıl, Delta, Konya Ovası, küresel 4 şehir, C-band, maruziyet).
5. MASTER_PLAN §9 kontrol listesindeki "KISMEN" ve "BEKLİYOR" maddelerini kapatmak için gereken her şeyi `docs/qa/PC8.md`'ye yapılacaklar listesi olarak yaz.
6. Sonra "ASLA BOŞ KALMA" döngüsü.

---
# 20:10 PC1 — ÖZGÜN KATKI O1 (sahibi sensin; `docs/OZGUN_KATKILAR.md` §O1) — 20:00 madde 1–3'ten hemen sonra
Kalıcı akifer depolama kaybı (km³/yıl):
1. Girdi: `data/central_valley_fullyear/decomp.json` (+ PNG'ler; piksel değerleri için `analysis/out/` altındaki tam yıl npz/ızgara dosyaları — yoksa `analysis/decomp/run_decomp.py` çıktılarını bul; PC9'un status'una bak), geliş açısı (LOS→dikey), referans duyarlılığı aralığı (summary.json).
2. Hesap: V = Σ v_kalıcı,dikey × A_piksel (sadece reason=ok pikseller; havza maskesi: bbox içinde, gerekirse çökme > 1 cm/yıl olan alan). Birim km³/yıl ve milyon m³/yıl. Belirsizlik: piksel standart hatası (korelasyon uyarısıyla) + 3 referansla aralık → alt/üst sınır.
3. Bağlam: yöntemin dayanağı — USGS Circular 1182 (Galloway et al. 1999) ve kalıcı sıkışma = kalıcı depolama kaybı yaklaşımı; San Joaquin/Tulare için yayımlanmış kayıp tahminleri (kaynak, yıl, birim) ile büyüklük mertebesi kıyası. Her linki aç.
4. Çıktı: `analysis/pc8/storage_loss.py` (+ test: sabit hız × bilinen alan → bilinen hacim), `data/central_valley_fullyear/storage_loss.json` (`volume_km3_per_yr, lower, upper, area_km2, method, assumptions, quality:"mixed"`), `docs/story/storage_loss.md` (sade 5 cümle + teknik paragraf), `docs/story/media/pc8_storage_loss.png`.
5. Anlaşılır karşılaştırma ekle (ör. "X Olympic pools" veya bir barajın kapasitesiyle — kaynaklı).
6. Karapınar tam yıl `decomp` gelince aynısı → `data/karapinar_fullyear/storage_loss.json`.
Yazma alanına eklendi: `analysis/pc8/storage_loss.py`, `data/*_fullyear/storage_loss.json`, `docs/story/storage_loss.md`.

---
# 20:50 PC1 — BÜYÜK GÖREV: `docs/ATLAS_PLANI.md`
Şu anki küçük işini bitir, sonra SORMADAN `docs/ATLAS_PLANI.md` içindeki kendi bölümüne geç ve yukarıdan aşağı yap. Teslime kadar durma; bitince ASLA BOŞ KALMA döngüsü (hata ayıklama dahil).
