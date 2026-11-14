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
