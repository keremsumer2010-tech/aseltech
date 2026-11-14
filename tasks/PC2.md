# PC2 — memir-erdogmus — Veri (klasör: pipeline/)  ·  BUGÜN: docs/TODAY_PLAN.md
Önce CLAUDE.md'deki "Veri kalitesi ve kalibrasyon" kuralını oku.

## Görev 1 — HEMEN (12:00–13:30 TR)
1. https://urs.earthdata.nasa.gov adresinden hesap aç. Şifreyi SEN gir, Claude'a verme.
   Claude'a `~/.netrc` şablonunu hazırlat; kullanıcı adı ve şifreyi o dosyaya SEN yaz. `.netrc` asla repoya girmez.
2. `pip install asf_search h5py numpy matplotlib`
3. `pipeline/search.py`: Central Valley GUNW path 34 listesi → `pipeline/central_valley_gunw.csv`
   (granule, iki tarih, sürüm kodu, URL, boyut, `quality` sütunu: her iki tarih ≥ 2026-06-17 ise "provisional", değilse "beta-precal").
4. İLK dosya: 2026-09-08 → 2026-09-20 çifti. İndir, HDF5 ağacını `docs/gunw_structure.md`'ye yaz
   (unwrapped phase, coherence, x/y, EPSG, dalga boyu, incidence yolları; dosya içindeki kalite/sürüm/kalibrasyon attr'ları da).
   HEMEN push et → PC3 bunu bekliyor.

## Görev 2 — (13:30–16:00 TR) — SADECE provisional çiftler
Şu 6 ardışık çifti sırayla indir, `pipeline/subset.py` ile central_valley bbox'ını kes, orijinali sil (sadece "P05023"):
2026-06-28→07-10, 07-10→07-22, 07-22→08-15, 08-15→08-27, 08-27→09-08, 09-08→09-20

Her alt küme: `pipeline/subset/central_valley/<t1>_<t2>.npz` içinde `unw`, `coh`, `x`, `y`, `epsg`, `wavelength`, `incidence` (varsa), `quality`.
Her dosya bitince push et.

## Görev 3 — (Pazar) beta-precal dahil tam yıl zinciri (2025-11-24 → 2026-10-14) — AYRI klasör:
`pipeline/subset/central_valley_beta/` ; + SME2 → `data/central_valley/drivers.json`

## Rapor
status/PC2.md: kaç dosya bitti, indirme hızı, hata varsa BLOCKED + hata metni.
