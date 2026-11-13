# PC2 — Veri hattı (klasör: pipeline/)

## Görev 1 — KONTROL NOKTASI (en yüksek öncelik, hedef 2 saat)
1. Earthdata hesabı aç; `pip install asf_search h5py numpy matplotlib rasterio pyyaml`.
2. `pipeline/sites.yaml`: CLAUDE.md'deki 3 bölge (bbox, GUNW path'leri, tarih aralığı).
3. `pipeline/search.py <site>`: `platform=NISAR`, `processingLevel=GUNW` (ve GCOV, SME2) listesi → `pipeline/<site>_<ürün>.csv`.
   Central Valley için path 34.
4. En kısa aralıklı TEK GUNW'yi `raw/` altına indir.
5. Resmi hazırlık notebook'unu incele: https://github.com/nisar-solid/ATBD/blob/main/prep/NISAR_prep.ipynb
   GUNW HDF5 ağacını çıkar → `docs/gunw_structure.md` (unwrapped phase, coherence, x/y, EPSG, dalga boyu, LOS cube yolları).
6. `docs/checkpoint_phase.png` (unwrapped phase, bbox kesilmiş).

## Görev 2 (Görev 1 bitince)
Central Valley path 34 TÜM GUNW'lerini sırayla indir → sadece bbox'ı kes (`pipeline/subset.py`, çıktı `raw/subset/*.h5` veya GeoTIFF) → orijinali sil.
Paralel: aynı bölge için 6–8 tarihlik GCOV ve tüm SME2'yi kes.

## Kabul
`docs/gunw_structure.md` + PNG push edildi; status'ta dosya boyutu, indirme süresi, giriş gerekip gerekmediği. Hata → BLOCKED + hata metni.
