# PC3 — M3hmeT1888 — Çökme analizi (klasör: analysis/)  ·  BUGÜN: docs/TODAY_PLAN.md
Önce CLAUDE.md'deki "Veri kalitesi ve kalibrasyon" kuralını oku.

## Görev 1 — (12:00–14:00 TR)
1. Earthdata hesabı aç (şifreyi SEN gir), `.netrc` kur. `pip install asf_search h5py numpy matplotlib pytest`
2. `analysis/insar.py`: `phase_to_cm(unw, wavelength_m)`, `mask_coherence(arr, coh, thr=0.3)`,
   `reference(arr, (row, col))`, `los_to_vertical(cm, incidence_deg)`.
   İşaret konvansiyonunu ürün dokümanı veya https://github.com/nisar-solid/ATBD kodundan DOĞRULA, kaynağı yoruma yaz.
   `analysis/test_insar.py` (pytest geçmeli).
3. Karapınar (bbox CLAUDE.md'de) için GUNW path 7, 2026-09-18 → 09-30 çiftini indir → `docs/karapinar_checkpoint_cm.png`.

## Görev 2 — (PC2 alt kümeleri geldikçe, 14:00–17:00 TR)
`analysis/cumulative.py central_valley`: `pipeline/subset/central_valley/*.npz` → tarih sırasıyla zincir toplamı,
coherence maskesi, sabit referans bölgesi (az hareketli, yüksek koherens; seçimini status'a yaz) →
veri sözleşmesine göre `data/central_valley/meta.json` (`quality: "provisional"` + `quality_note`),
`disp/<date>.png` (renkli, şeffaf, bbox'a oturur), `points.json` (10–15 nokta). Renk aralığı tüm tarihlerde SABİT.
"Kalibre ettik" deme; ürünü NISAR projesinin işlediği hâliyle kullandığımızı yaz.

## Görev 3 — Karapınar için aynısı → `data/karapinar/` (zaman kalırsa bugün, yoksa Pazar)

## Pazar — Tam yıl (beta-precal dahil) ayrı çıktı: `data/central_valley_fullyear/` + `quality: "mixed"`; kalıcı/geri dönen ayrımı orada.

## Rapor
status/PC3.md: maks çökme (cm), referans noktası, kullanılan çift sayısı, test sonucu.
