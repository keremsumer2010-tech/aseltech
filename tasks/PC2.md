# PC2 — Veri hattı (klasör: pipeline/)

## Görev 1 — KONTROL NOKTASI (öncelik en yüksek, hedef 2 saat)
1. Earthdata hesabı aç (urs.earthdata.nasa.gov) ve `asf_search` kur: `pip install asf_search h5py numpy matplotlib rasterio`.
2. `pipeline/search.py`: central_valley bbox'ı için `platform=NISAR`, `processingLevel=GUNW`, path 34 ürünlerini listele;
   `pipeline/central_valley_gunw.csv` yaz (granule adı, başlangıç/bitiş tarihi, URL, boyut).
3. EN KISA zaman aralıklı TEK bir GUNW indir (`raw/` altına).
4. `pipeline/inspect.py`: HDF5 ağacını (grup/dataset adı, shape, dtype, attrs) çıkar → `docs/gunw_structure.md`.
   Özellikle: unwrapped phase, coherence, koordinat (x/y veya lon/lat), CRS/EPSG, dalga boyu/merkez frekans attr'ı.
5. Tek bir unwrapped phase PNG'si üret: `docs/checkpoint_phase.png`.

## Kabul
- `docs/gunw_structure.md` ve `docs/checkpoint_phase.png` push edildi; status'ta dosya boyutu ve indirme süresi yazıyor.
- İndirme giriş istiyor/başarısızsa: hatayı aynen status'a yaz (BLOCKED).
