# PC9 — 15:45 YENİDEN ATANDI: TAM YIL ANALİZİ (Q08) · Mehmet'in 2. bilgisayarı, Antigravity
> Site işini Mehmet'in kararıyla PC3 yapıyor ve hızlı ilerliyor; site artık PC3'ün. PC9 = tam yıl analizi. İNDİRME YOK: veri repoda (`pipeline/subset/central_valley_beta/`, PC2 yüklüyor).

## Yazma alanı
`data/central_valley_fullyear/` · `analysis/pc9/` · `docs/story/fullyear.md` · `docs/story/media/pc9_*.png` · `docs/qa/PC9.md` · `status/PC9.md` · QUEUE'da Q08 satırı.
PC3'ün `analysis/*.py`, `analysis/decomp/*` dosyalarını ÇALIŞTIR, DEĞİŞTİRME (gerekirse `analysis/pc9/` altında sarmalayıcı).

## Görevler (sırayla; bitince sormadan sıradakine)
0. `git pull --rebase origin main` → status "çalışıyor" → commit + push. QUEUE'da Q08'i sahiplen (`[~PC9]`).
1. **Tam yıl kümülatif** (PC2 Q07 alt kümeleri geldikçe; 2025-11-24 → 2026-10-14, 25 çift): `analysis/cumulative.py central_valley --data-dir data/central_valley_fullyear` (zincirde boşluk varsa sadece kesintisiz kısım; `--help` ile parametreleri kontrol et). Çıktıda `quality: "mixed"` ve hangi çiftlerin `beta-precal` olduğu `notes`'ta. Eksik çift varsa beklemek yerine elindeki kesintisiz parçayla çalış, yeni çift gelince yeniden üret.
2. **Kalıcı vs geri dönen (Q08)**: `analysis/decomp/run_decomp.py` ile trend (cm/yıl, kalıcı) + yıllık genlik (cm, geri dönen) → `data/central_valley_fullyear/decomp.json` + 2 PNG (sözleşme §4). PC5 bağımsız kontrol edecek.
3. **Metin + grafik** → `docs/story/fullyear.md` + `docs/story/media/pc9_fullyear_point.png`: en çok çöken noktada 11 aylık seri (kış yükselişi, yaz çöküşü — "dans"), kalıcı/geri dönen oranı. Beta dönemini grafikte kesikli çizgi ve açık etiketle göster. Sade İngilizce (REVIEW_1500). PC3 siteye koyacak.
4. **Sürekli:** her 30 dk `git pull`; yeni çift geldiyse 1–3'ü yeniden üret; `docs/qa/*.md` içindeki fullyear bulgularını düzelt.

## Yapma listesi
Provisional ve beta'yı etiketsiz karıştırma (sadece `*_fullyear` klasöründe, `mixed`) · PC3 dosyalarını değiştirme · sayı uydurma · `git add -A`.

> **16:15 CHALLENGE UYUMU (A6 "patterns and rhythms at different time steps"):** fullyear.md'de bu ifadeyi açıkça karşıla: aylık adımlarla kış yükselişi / yaz çöküşü, 12 günlük ve aylık zaman adımlarında iki grafik. Mümkünse Karapınar tam yılı (PC2 hazırlarsa) için de aynı.

> **16:35 PC1 — ACİL (PC4 48 dk sessiz, 17:30 Lincoln provası):** tam yıl işin bitti, harika. ŞİMDİ: `docs/story/presentation_cues.md` (3 dk Lincoln konuşması, 30 sn'lik 6 blok: konuşan kişi — Kerem anlatır, Memir demo sürer, Mehmet ve İbrahim soruları alır; 1–2 cümle sade İngilizce; canlı sitede tıklanacak yer — https://keremsumer2010-tech.github.io/aseltech/ güncel bölümleri; sonda 5 jüri sorusuna tek cümlelik cevap `docs/story/judge_faq.md`'den) ve `docs/story/rehearsal_checklist.md` (internet kesilirse yerel `docs/story/media/demo_30s.mp4` ve `docs/story/slides.html`, sekme sırası, ekran paylaşımı, süre tutma, kim ne yapar). Sayılar `data/*/summary.json`'dan; tam yıl sonucunu "includes pre-calibration data" notuyla kullan. 17:05'e kadar push. PC4 bu dosyaları yazdıysa (git pull'da gör) üzerine yazma, sadece eksikleri `docs/qa/PC9.md`'ye not et.

> **18:55 PC1:** Lincoln geçti. `docs/AKSAM_PLANI.md`'deki kendi satırına geç (akşam → Pazar). Durma.

> **19:45 PC1 — TEK SIRA ARTIK BURASI:** `docs/CALISMA_HARITASI.md` içindeki kendi bölümün. Yukarıdan aşağı yap, bitince "ASLA BOŞ KALMA" döngüsü. Teslime kadar durma.

---
# 20:50 PC1 — BÜYÜK GÖREV: `docs/ATLAS_PLANI.md`
Şu anki küçük işini bitir, sonra SORMADAN `docs/ATLAS_PLANI.md` içindeki kendi bölümüne geç ve yukarıdan aşağı yap. Teslime kadar durma; bitince ASLA BOŞ KALMA döngüsü (hata ayıklama dahil).

# 🧭 PC9 UZUN GÖREV PLANI (Paz 00:05 → Paz 20:00, PC1) — sırayla, SORMADAN
Git kuralı: önce kendi dosyalarını commit et → `git pull --rebase origin main` → push. Kendi commit edilmemiş değişikliğin engel değildir.

## FAZ 1 — Atlas şehirlerin (şimdi → Paz 06:00)
Kalite standardı (`docs/ATLAS_PLANI.md` "KALİTE STANDARDI"): ±0.25° tam kutu, havza dışı referans (`--ref-lonlat`), `summary.json`'da `p2_cm` + `rate_cm_per_100d`.
1. **Eloy** −111.55, 32.75 (bitir; 1 saattir sürüyor — takıldıysa `--resume` ile devam, nedeni status'a)
2. **Cangzhou** 116.85, 38.30  3. **Gorgan** 54.43, 36.84  4. **Houston/Katy** −95.80, 29.80  5. **Lagos** 3.39, 6.45 (tropik, düşük koherens beklenir → yine de çalıştır, `confidence` notu)
Her şehirde: literatür hızı (DOI) `docs/qa/PC9.md`'ye, "hazır: <şehir>" satırı (PC10 atlasa ekler, PC5 karar verir), commit + push. Kapsama yoksa "no coverage" yaz, geç. Aynı anda 1 indirme, ham .h5'i kestikten sonra sil.

## FAZ 2 — ★ Özgün katkı: "108 gün yıllık hızı temsil eder mi?" (Paz 06:00 → 14:00)
Jürinin atlas için soracağı ilk soru bu; cevabı sadece senin tam yıl yöntemin verebilir (Central Valley'de yaptın: kalıcı −3.74 cm/yr medyan, Earlimart −16.77 cm/yr).
1. Atlasın ilk sıralarındaki 2 bölge için tam yıl (beta-precal Kas 2025 → Haz 2026 + provisional) zinciri ve `run_fullyear.py --step cumulative/decomp`:
   - **Konya Ovası** (atlas 1. sıra, `data/konya_plain/` bbox'ı) → `data/konya_plain_fullyear/`
   - **Mexico City** (merkez −99.05, 19.40; havza dışı referans PC10'un yeni referansı) → `data/global/mexico_city_fullyear/`
   Beta varsa `quality: mixed`; beta yoksa "insufficient_data" yaz, geç.
2. Her biri için: kalıcı hız (cm/yr) vs `rate_cm_per_100d × 3.65` (108 gün ekstrapolasyonu) → oran. Central Valley için de aynı oran (verin hazır).
3. Çıktı: `docs/story/annualization.md` (≤1 sayfa, REVIEW_1500): "108 günlük ekstrapolasyon kalıcı hızı X kat abartıyor/eksik gösteriyor; mevsimsel bileşen Y". Grafik `docs/story/media/pc9_annualization.png` (3 bölge, iki çubuk: ekstrapolasyon vs kalıcı). PC5 ve PC4'e "hazır" notu `docs/qa/PC9.md`'de.

## FAZ 3 — GPS doğrulaması tam yıl (Paz 14:00 → 18:00)
`docs/CALISMA_HARITASI.md` PC9 madde 3–4: Central Valley tam yıl ↔ GNSS 11 ay (`validation/gnss/*.csv`) → `docs/qa/PC9.md` tablo (istasyon, r, RMSE); kalıcı çökme alan istatistiği (km², > 5 / > 10 cm/yr).

## FAZ 4 — Paz 18:00 → 20:00
Kendi çıktılarını yeniden çalıştır, `python -m pytest -q analysis/pc9`, PC5 `docs/qa/PC5.md` §10'daki senin satırların. 20:00 sonrası sadece hata düzeltme.

Yazma alanı ek: `data/global/{eloy,cangzhou,gorgan,houston,lagos,mexico_city_fullyear}/`, `data/konya_plain_fullyear/`, `pipeline/subset/global_<bu şehirler>/`, `pipeline/subset/konya_plain_fullyear/`, `docs/story/annualization.md`, `docs/story/media/pc9_*.png`, `docs/qa/PC9.md`, `status/PC9.md`.


# 🌍 ATLAS FİNAL — PC9 (Paz 00:20, PC1) · plan: `docs/ATLAS_FINAL.md`
Mevcut uzun planın geçerli; üst plandaki zaman çizelgesine (Paz 06:00 / 14:00 / 20:00) göre ilerle.


# ♻️ SÜREKLİ KURAL (Paz 00:45, PC1)
`tasks/SUREKLI.md` zorunlu: **her 3 dakikada bir** commit → pull --rebase → push, bu dosyanın sonuna yeni bölüm var mı bak, status tek satır. Asla durma; listen biterse SUREKLI.md tablosundaki kendi sürekli işin.


# ⭐ ATLAS KUSURSUZLUK (Paz 01:00, PC1) · `docs/ATLAS_MUKEMMEL.md`
Kapsam hedefi Paz 14:00'te ≥20 şehir. Her yeni şehirde 6'lı paketin 1. parçası senin (summary/meta/points/disp); `docs/qa/ATLAS_COMPLETENESS.md`'de kendi satırların ✓ olsun.
