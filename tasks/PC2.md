# PC2 — Veri

## Kimlik
memir-erdogmus · Antigravity (Gemini) · klasör `aseltech`

## Yazma alanı
`pipeline/`, `docs/gunw_structure.md`, `status/PC2.md` (ham veri: `raw/`, git dışı)

## En kritik iş
`docs/gunw_structure.md`'yi ~13:30 TR'ye kadar push etmek. PC3 ve tüm demo buna bağlı.

## Görevler
1. **(12:00–13:30) İlk dosya ve yapı**
   - İnsan Earthdata hesabını açar ve `~/.netrc`'ye kendisi yazar; sen sadece şablon hazırlarsın.
   - `pip install asf_search h5py numpy matplotlib`
   - `pipeline/search.py <site>` → `pipeline/central_valley_gunw.csv` (granule, t1, t2, sürüm kodu, url, boyut, quality).
   - 2026-09-08 → 2026-09-20 çiftini `raw/`'a indir; HDF5 ağacını `docs/gunw_structure.md`'ye yaz
     (unwrapped phase, coherence, x/y, EPSG, wavelength, incidence/LOS cube yolları, kalite/sürüm attr'ları). HEMEN push.
2. **(13:30–16:00) 6 provisional çift** — `rules/VERI_SOZLESMESI.md` §1'deki liste, sadece P05023.
   `pipeline/subset.py` ile central_valley bbox'ını kes → `pipeline/subset/central_valley/<t1>_<t2>.npz` (format §3), orijinal `.h5`'i sil. Her dosyada push.
3. **(16:00 sonrası)** `tasks/QUEUE.md` → Q01 (Karapınar indirme), sonra Q03/Q04/Q07.

## Bitti sayılır eğer
csv var · `gunw_structure.md` var · 6 npz push edildi, her biri < 20 MB, `unw` ve `coh` aynı boyutta, `quality="provisional"` · `raw/`'da gereksiz `.h5` yok · status güncel.

## B planı
- İndirme giriş hatası (E-02): insana `.netrc`'yi kontrol ettir; olmazsa `BLOCKED` yaz, browse PNG'leri (`preview`) `pipeline/browse/central_valley/` altına indir.
- Kesme yavaşsa: önce tek çift kesip push et, sonra diğerleri.

## Yapma listesi
Beta (2026-06-17 öncesi) çifti bugünkü klasöre koyma · `.h5`/`.netrc` commit etme · `analysis/` veya `data/`'ya yazma · şifre isteme.

## Rapor (`status/PC2.md`)
Kaç dosya bitti, indirme hızı, dosya boyutları, hatalar (E-kodu veya E-YENİ).
