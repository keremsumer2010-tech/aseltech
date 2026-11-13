# PC3 — Çökme zaman serisi + özgün analiz (klasör: analysis/)

## Görev 1 — Ortam + dönüşüm (PC2 verisi gelene kadar)
1. MintPy kurulumu: https://github.com/nisar-solid/ATBD/blob/main/docs/installation.md (Windows'ta olmazsa WSL; BLOCKED yaz).
2. Konya path 108 için TEK GUNW indir (kendi `raw/`), `analysis/insar.py`:
   `phase_to_cm`, `mask_coherence`, `reference`, `los_to_vertical(los_cm, incidence_deg)` (metadata cube'dan incidence).
   İşaret konvansiyonunu ürün dokümanı/ATBD'den doğrula, kaynağı yorumda yaz.
3. `analysis/test_insar.py` sentetik testler (pytest geçmeli).
4. `docs/konya_checkpoint_cm.png` (renk çubuğu cm).

## Görev 2 — Zaman serisi (PC2 Görev 2 sonrası)
ATBD `methods/secular` akışını Central Valley GUNW yığınına uygula (MintPy) → kümülatif dikey çökme.
Çıktı: veri sözleşmesine göre `data/central_valley/meta.json`, `disp/<date>.png`, `points.json`.

## Görev 3 — ÖZGÜN: Kalıcı vs geri dönen
Her piksel: doğrusal trend + yıllık sinüs uydur → `permanent_cm_per_yr`, `seasonal_amp_cm` → `data/central_valley/decomp.json` + 2 PNG.

## Kabul
Testler geçiyor; PNG'ler push; status'ta yöntem, referans noktası, kullanılan GUNW sayısı.
