---
type: gorev
id: PC2
owner: Memir (memir-erdogmus)
tool: Antigravity (Gemini)
status: acik
date: 2026-11-14
depends_on: []
feeds: [PC3]
---

# PC2 · Veri: GUNW arama, indirme, kesme

> **Saat saat sıra ve iş bitince sıradaki iş: `docs/ZAMAN_CIZELGESI.md`.** Atanmış QUEUE işlerin orada.

## Kimlik
Memir'in bilgisayarı, Antigravity. Ana hattın ilk halkası: **PC3 senin dosyalarını bekliyor.**

## Yazma alanın
`pipeline/` (script, csv, `subset/`) · `docs/gunw_structure.md` · `data/<site>/drivers.json` (Pazar) · `status/PC2.md`

## Başlamadan
- [ ] `rules/RULES.md` (özellikle K-9 kimlik, §8 disk) ve `rules/VERI_SOZLESMESI.md` §2-§4 okundu
- [ ] Boş disk ≥ 50 GB

---

## Görev 1 · Hesap, liste, ilk dosya (12:00-13:30) · **ACİL**

1. https://urs.earthdata.nasa.gov hesabı. **Şifreyi insan girer.** Ajan `~/.netrc` şablonunu hazırlar
   (`machine urs.earthdata.nasa.gov login <BURAYA> password <BURAYA>`), değerleri insan yazar. Ajan dosyayı okumaz, yazdırmaz.
2. `pip install asf_search h5py numpy matplotlib`
3. `pipeline/search.py`: Central Valley bbox, GUNW, path 34 → `pipeline/central_valley_gunw.csv`
   Sütunlar: `granule, date1, date2, crid, url, size_mb, quality`
   (`quality` = her iki tarih ≥ 2026-06-17 ise `provisional`, değilse `beta-precal`).
4. İlk dosya: **2026-09-08 → 2026-09-20** çifti. `raw/` altına indir.
5. HDF5 ağacını `docs/gunw_structure.md`'ye yaz: unwrapped phase, coherence, x/y, EPSG, dalga boyu, incidence yolları;
   veri tipleri ve birimler; dosyadaki kalite/sürüm/kalibrasyon attribute'ları (değerleriyle).
6. **Hemen push.**

**Bitti sayılır eğer:** csv'de path 34 çiftleri listeli; `gunw_structure.md` gerçek dosyadan (`h5py` ile) üretilmiş ve push edilmiş.

## Görev 2 · 6 provisional çifti kes (13:30-16:00)

Sırayla (her biri bittikçe push, K-13):
```
2026-06-28→07-10 · 07-10→07-22 · 07-22→08-15 · 08-15→08-27 · 08-27→09-08 · 09-08→09-20
```
`pipeline/subset.py`: bbox'ı kes → `pipeline/subset/central_valley/<t1>_<t2>.npz`
- İçerik ve tip: `rules/VERI_SOZLESMESI.md` §4.1 (`unw` float32, `coh` uint8, `np.savez_compressed`, ≤ 20 MB).
- Sadece CRID `P05023` (PROVISIONAL). Kesimden sonra ham `.h5` silinir.
- Aynı anda diskte en fazla 5 ham dosya.

**Bitti sayılır eğer:** 6 npz push edildi; her biri `np.load` ile açılıp boyut ve NaN oranı status'a yazıldı.

## Görev 3 · Pazar: tam yıl ve toprak nemi

- Beta-precal dahil tam zincir (2025-11-24 → 2026-10-14) → **ayrı klasör** `pipeline/subset/central_valley_beta/`.
  Zincirde boşluk varsa (ardışık çift yok) listele, status'a yaz.
- SME2 toprak nemi → `data/central_valley/drivers.json` (sözleşme §4.2; çökme serisini PC3'ten al).

---

## En kritik iş
`docs/gunw_structure.md`'yi 13:30'dan önce push etmek. PC3 okuma kodunu buna göre yazacak.

## B planı
- `.h5` indirilemiyorsa (Access denied, yavaş bağlantı): BLOCKED + hata metni. PC1 browse PNG planına geçer;
  sen browse PNG'leri (girişsiz) `pipeline/browse/central_valley/` altına indir.
- İndirme çok yavaşsa (< 5 MB/s): çift sayısını 4'e indir, PC1'e status'ta yaz.

## Yapma
- `.h5`'i repoya ekleme. `git add -A` yok.
- Provisional ile beta'yı aynı klasöre koyma.

## Rapor
`status/PC2.md`: kaç dosya bitti, indirme hızı, her npz'nin boyutu ve NaN oranı, hata varsa `BLOCKED:` + hata metni, `AI:` satırı.
