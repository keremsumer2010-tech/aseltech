# PC2 durum

- Görev: 1 (Hesap, liste, ilk dosya, gunw_structure.md) — **TAMAMLANDI**
- Görev: 2 (Central Valley provisional çiftleri) — **TAMAMLANDI (7/7 tam `ion` katmanıyla push edildi)**
- Görev: Q01 (Karapınar GUNW Path 7 Frame 69 provisional zinciri) — **TAMAMLANDI (8/8 tam `ion` katmanıyla `pipeline/subset/karapinar/` altına push edildi — PC3 için hazır!)**
- Görev: Q04 (Central Valley SME2 toprak nemi → `data/central_valley/drivers.json`) — **TAMAMLANDI** (8 provisional SME2 granülü, `lag_corr=0.654`)
- Görev: Q03 (Central Valley GCOV 6 provisional tarih HV dB → `data/central_valley/gcov/`) — **TAMAMLANDI (8 provisional tarih HV dB PNG + `meta.json` `data/central_valley/gcov/` altına push edildi)**
- Görev: Q09 (UK kil bölgesi Londra GUNW provisional zinciri → `pipeline/subset/uk_clay/`), Karapınar Path 172 (`pipeline/subset/karapinar_p172/`), Q07 (Central Valley tam yıl zinciri → `pipeline/subset/central_valley_beta/`) ve 15:05 Ek İş (`pipeline/subset/fens_gcov/`) — **TAMAMLANDI**
- Çıktılar:
  - `pipeline/search.py`, `pipeline/download.py` (PCQ `docs/code_review.md` bulgusu düzeltildi: `netrc` üzerinden `urs.earthdata.nasa.gov` ve `EARTHDATA_TOKEN` desteği), `pipeline/inspect_gunw.py`, `pipeline/subset.py`, `pipeline/sme2_drivers.py`, `pipeline/gcov_subset.py`
  - `data/central_valley/gcov/meta.json` + 8 adet `*.png` (`2026-06-28` → `2026-10-14`, `vmin=-28 dB`, `vmax=-10 dB`, `mean_dB=[-19.80..-19.09] dB`)
  - `data/central_valley/drivers.json` (Q04: 8 provisional `P05023` SME2 Path 34 Frame 20 tarihinin bölge ortalaması toprak nemi `[0.1555..0.1844] m³/m³`, HV dB `[-18.624..-18.169] dB`, `irrigation_index` ve `lag_corr=0.654`)
  - `pipeline/central_valley_p114_gunw.csv` (PC3 Q21 desteği: Central Valley Path 114 Frame 70 — 24 GUNW ürünü, 8 provisional `P05023` çifti `2026-06-22 → 2026-10-20` hazır; ek destek gerekirse bildirin)
  - `pipeline/central_valley_gunw.csv` (27 Path 34 Frame 20 ürünü; 7 provisional `P05023`, 20 beta-precal)
  - `pipeline/karapinar_gunw.csv` (15 Path 7 Frame 69 ürünü; 8 benzersiz provisional `P05023` çifti: `2026-06-26` → `2026-10-12`)
  - `docs/gunw_structure.md` (gerçek `2026-09-08 → 2026-09-20` P05023 HDF5'inden üretildi; λ = 0.24196324 m)
  - `pipeline/subset/central_valley/2026-06-28_2026-07-10.npz` (14.99 MB, shape=(1473, 1438), NaN=3.15%, `ion=(1473, 1438) full`, ham `.h5` silindi)
  - `pipeline/subset/central_valley/2026-07-10_2026-07-22.npz` (15.38 MB, shape=(1473, 1438), NaN=4.49%, `ion=(1473, 1438) full`, ham `.h5` silindi)
  - `pipeline/subset/central_valley/2026-07-22_2026-08-15.npz` (15.76 MB, shape=(1473, 1438), NaN=6.99%, `ion=(1473, 1438) full`, ham `.h5` silindi)
  - `pipeline/subset/central_valley/2026-08-15_2026-08-27.npz` (15.49 MB, shape=(1473, 1438), NaN=4.58%, `ion=(1473, 1438) full`, ham `.h5` silindi)
  - `pipeline/subset/central_valley/2026-08-27_2026-09-08.npz` (15.19 MB, shape=(1473, 1438), NaN=4.07%, `ion=(1473, 1438) full`, ham `.h5` silindi)
  - `pipeline/subset/central_valley/2026-09-08_2026-09-20.npz` (15.32 MB, shape=(1473, 1438), NaN=4.95%, `ion=(1473, 1438) full`, ham `.h5` silindi)
  - `pipeline/subset/central_valley/2026-09-20_2026-10-14.npz` (15.72 MB, shape=(1473, 1438), NaN=8.24%, `ion=(1473, 1438) full`, ham `.h5` silindi)
  - `pipeline/subset/karapinar/2026-06-26_2026-07-08.npz` (1.64 MB, shape=(470, 603), NaN=51.25%, `ion=(470, 603) full`, epsg=32636, ham `.h5` silindi)
  - `pipeline/subset/karapinar/2026-07-08_2026-07-20.npz` (1.61 MB, shape=(470, 603), NaN=52.49%, `ion=(470, 603) full`, epsg=32636, ham `.h5` silindi)
  - `pipeline/subset/karapinar/2026-09-18_2026-09-30.npz` (1.80 MB, shape=(470, 603), NaN=33.50%, `ion=(470, 603) full`, epsg=32636)
  - `pipeline/subset/karapinar/2026-07-20_2026-08-13.npz` (1.28 MB, shape=(470, 603), NaN=69.74%, `ion=(470, 603) full`, epsg=32636, ham `.h5` silindi)
  - `pipeline/subset/karapinar/2026-08-13_2026-08-25.npz` (1.79 MB, shape=(470, 603), NaN=27.97%, `ion=(470, 603) full`, epsg=32636, ham `.h5` silindi)
  - `pipeline/subset/karapinar/2026-08-25_2026-09-06.npz` (1.99 MB, shape=(470, 603), NaN=19.45%, `ion=(470, 603) full`, epsg=32636, ham `.h5` silindi)
  - `pipeline/subset/karapinar/2026-09-06_2026-09-18.npz` (1.78 MB, shape=(470, 603), NaN=35.47%, `ion=(470, 603) full`, epsg=32636, ham `.h5` silindi)
  - `pipeline/subset/karapinar/2026-09-30_2026-10-12.npz` (1.83 MB, shape=(470, 603), NaN=29.07%, `ion=(470, 603) full`, epsg=32636, ham `.h5` silindi)
- İndirme hızları:
  - `2026-09-08 → 2026-09-20`: 10.32 MB/s / yenileme 12.43 MB/s (2236.0 MB)
  - `2026-06-28 → 2026-07-10`: 12.71 MB/s / yenileme 11.23 MB/s (2192.0 MB)
  - `2026-07-10 → 2026-07-22`: 16.79 MB/s / yenileme 14.20 MB/s (2200.0 MB)
  - `2026-07-22 → 2026-08-15`: 16.92 MB/s / yenileme 15.49 MB/s (2212.0 MB)
  - `2026-08-15 → 2026-08-27`: 15.66 MB/s (2192.0 MB)
  - `2026-08-27 → 2026-09-08`: 11.82 MB/s (2236.0 MB)
  - `2026-09-20 → 2026-10-14`: 11.28 MB/s (2232.0 MB)
- Doğrulama:
  - `2026-06-28_2026-07-10.npz`: `np.load` ile açıldı; `unw` [-0.592, 13.344] rad, `ion` [34.341, 42.572] rad (`(1473, 1438)` float32), `coh` ort=0.604, `inc` [37.73, 45.31]°, `epsg=32611`.
  - `2026-07-10_2026-07-22.npz`: `np.load` ile açıldı; `unw` [-11.713, 3.400] rad, `ion` [-26.943, -20.056] rad (`(1473, 1438)` float32), `coh` ort=0.592, `inc` [37.73, 45.30]°, `epsg=32611`, `λ=0.24196324 m`.
  - `2026-07-22_2026-08-15.npz`: `np.load` ile açıldı; `unw` [-4.163, 14.352] rad, `ion` [15.966, 25.666] rad (`(1473, 1438)` float32), `coh` ort=0.495, `epsg=32611`, `λ=0.24196324 m`.
  - `2026-08-15_2026-08-27.npz`: `np.load` ile açıldı; `unw` [-2.746, 8.647] rad, `ion` [3.204, 4.981] rad (`(1473, 1438)` float32), `coh` ort=0.578, `inc` [37.73, 45.31]°, `epsg=32611`, `λ=0.24196324 m`.
  - `2026-08-27_2026-09-08.npz`: `np.load` ile açıldı; `unw` [-1.671, 8.058] rad, `ion` [9.110, 11.247] rad (`(1473, 1438)` float32), `coh` ort=0.626, `inc` [37.73, 45.31]°, `epsg=32611`, `λ=0.24196324 m`.
  - `2026-09-08_2026-09-20.npz`: `np.load` ile açıldı; `unw` [-3.776, 6.936] rad, `ion` [17.922, 22.193] rad (`(1473, 1438)` float32), `coh` ort=0.626, `inc` [37.73, 45.31]°, `epsg=32611`.
  - `2026-09-20_2026-10-14.npz`: `np.load` ile açıldı; `unw` [-4.230, 7.051] rad, `ion` [-8.020, -4.661] rad (`(1473, 1438)` float32), `coh` ort=0.579, `epsg=32611`, `λ=0.24196324 m`.
- BLOCKED: yok (GitHub push oturumu doğrulandı)
- AI: Antigravity (Gemini) → `pipeline/*.py` veri arama/indirme/inceleme/kesme scriptleri ve `docs/gunw_structure.md` üretimi

## 15:45 Güncelleme — Q07 (18/18), Q09 (9/9), Karapınar Path 172 (8/8) ve fens_gcov (8/8) TAMAMLANDI

- **15:05 Ek İş (PC7 için) — fens_gcov hazır:**
  - `pipeline/subset/fens_gcov/<YYYY-MM-DD>.npz` altında 8 adet `provisional` GCOV alt kümesi push edildi (`16c1219`, `7828c74`).
  - Orbit: **Path 124 Descending Frame 62** (ör. `NISAR_L2_PR_GCOV_023_124_D_062_2005_DHDH_A_20260622T192240_20260622T192316_P05023_N_F_J_001`); Fens bbox `(-0.3, 52.4, 0.4, 52.9)` için tam kapsama sağlar (`shape=(1440, 1243)`, `epsg=32630`, `quality="provisional"`, anahtarlar: `hh_db`, `hv_db`, `x`, `y`, `epsg`, `date`, `granule`, `quality`).
  - Tarihler ve boyutlar (8/8): `2026-06-22.npz` (6.49 MB), `2026-07-04.npz` (6.48 MB), `2026-07-16.npz` (6.47 MB), `2026-08-21.npz` (6.60 MB), `2026-09-02.npz` (6.58 MB), `2026-09-14.npz` (6.57 MB), `2026-09-26.npz` (6.52 MB), `2026-10-08.npz` (6.54 MB).

- **Q07 (Central Valley tam yıl zinciri, P05023) — TAMAMLANDI (18/18 `beta-precal` + 7 `provisional`):**
  - `pipeline/subset/central_valley_beta/` altında `2025-11-24 → 2026-06-28` arası kesintisiz **18/18** `beta-precal` alt kümesi push edildi (`1cd9ad9`, `5c289ba`, `2c23e3b`, `d176a84`, `b3cba45`, `a9250d7`; `shape=(1473, 1438)`, dosya boyutları `14.55–16.12 MB`).
  - Devamındaki `2026-06-28 → 2026-10-14` arası **7 adet** `provisional` çift (`Path 34 Frame 20`, aynı kesit) `pipeline/subset/central_valley/` altında hazırdır; ikisi birlikte `2025-11-24 → 2026-10-14` tam yıl zincirini oluşturur (`PC9` Q08 için hazır).

- **Q09 (UK kil / Londra provisional GUNW zinciri) — TAMAMLANDI (9/9):**
  - `pipeline/uk_clay_gunw.csv` + `pipeline/subset/uk_clay/` altında `2026-06-21 → 2026-10-19` arası **9/9** `provisional` çift push edildi (`629011f`; dosya boyutları `2.85–3.20 MB`).

- **Karapınar ikinci geçiş (Path 172 Frame 21, provisional GUNW) — TAMAMLANDI (8/8):**
  - `pipeline/karapinar_p172_gunw.csv` + `pipeline/subset/karapinar_p172/` altında `2026-06-26 → 2026-10-12` arası **8/8** `provisional` çift push edildi (`4136995`; dosya boyutları `1.93–2.14 MB`).

## 17:37 Güncelleme — 15:50 BÜYÜK PAKET Madde 1 (Sacramento–San Joaquin Delta) TAMAMLANDI

- **Delta GUNW (Path 42 Descending, Frame 69, provisional) — TAMAMLANDI (9/9):**
  - `pipeline/delta_gunw.csv` + `pipeline/subset/delta/` altında `2026-06-17 → 2026-10-15` arası kesintisiz **9/9** `provisional` çift (`shape=(403, 493)`, `1.22–1.43 MB`, tam `ion` katmanlı) push edildi (`d0c52d8`, `4ee15c0`, `68b4920`).
  - `pipeline/pc2/run_cumulative.py delta --data-dir data/delta` ile `data/delta/` (`disp/*.png`, `meta.json`, `points.json`, `summary.json`) üretildi ve push edildi (`5b4b6dd`): 1 km blok medyan tepe çökmesi `-1.3 cm` LOS (`range_cm=[-1.3, -1.1]`, 120 gün, dikey tahmin `-1.6 cm`).
  - `pipeline/pc2/delta_levees.py` ile OSM set hatları boyunca profil çıkarıldı (`N=87` örnek, p10=`-3.48 cm`, en belirgin 4.09 km set hattında min `-11.36 cm`); `docs/story/media/pc2_delta.png` ve `docs/story/delta.md` (A5, A11, Levees and Dams + StoryMap atıflı) oluşturuldu.
- **Sıradaki iş:** Madde 2 (**Konya Ovası'nın tamamı**, `konya_plain`, Path 7 Frame 69).

## 18:39 Güncelleme — 15:50 BÜYÜK PAKET Madde 2 (Konya Ovası'nın Tamamı) TAMAMLANDI

- **Konya Ovası GUNW (Path 7 Descending, Frame 69, provisional) — TAMAMLANDI (8/8):**
  - `pipeline/konya_plain_gunw.csv` + `pipeline/subset/konya_plain/` altında `2026-06-26 → 2026-10-12` arası kesintisiz **8/8** `provisional` çift (`shape=(1025, 1710)`, `6.46–8.74 MB`, tam `ion` katmanlı) push edildi (`e3fedbb`, `f47fa63`, `2222966`).
  - `pipeline/pc2/run_cumulative.py konya_plain --data-dir data/konya_plain` ile `data/konya_plain/` (`disp/*.png`, `meta.json`, `points.json`, `summary.json`) üretildi: 1 km blok medyan tepe çökmesi `-9.6 cm` LOS (`range_cm=[-14.0, -9.6]`, 108 gün, dikey tahmin `-12.1 cm` @ `37.6°`, konum `32.6278°E, 37.8161°N`).
  - `pipeline/pc2/konya_plain_plot.py` ile `docs/story/media/pc2_konya_plain.png` ve `docs/story/konya_plain.md` (A5, A11, Sinkholes + StoryMap atıflı) oluşturuldu.

## Güncel Durum — Madde 3 ve Madde 4 TAMAMLANDI (15:50 BÜYÜK PAKET 1–4 BİTTİ)

- **Madde 4 — Karapınar Sebep Verisi (`data/karapinar/drivers.json`) — TAMAMLANDI (`c48bbc1`):**
  - `pipeline/pc2/karapinar_drivers.py` ile `2026-06-26 → 2026-10-12` arası **9** `provisional` SME2 granülü HTTP Range üzerinden okundu (`0 GB` disk kullanımı); `data/karapinar/drivers.json` üretildi (`lag_corr=0.481`).
- **Madde 3 — Karapınar Tam Yıl (`karapinar_fullyear`, Path 7 Frame 69) — TAMAMLANDI:**
  - Kış `beta-precal` (`2025-10-17 → 2026-01-09`): **6/6** indirildi ve push edildi (`e8ceece`, `962ac07`, `f44435c`, `b9520fd`); her `.npz` içinde `quality="beta-precal"` etiketli.
  - Yaz `provisional` (`2026-06-26 → 2026-10-12`): **8/8** `pipeline/subset/karapinar_fullyear/` altına push edildi (`f44435c`), her `.npz` içinde `quality="provisional"` etiketli.
  - ASF arşivinde `2026-01-09 → 2026-06-26` arası Karapınar için GUNW granülü bulunmuyor (zincir boşluğu).
  - `pipeline/pc2/run_cumulative.py karapinar_fullyear --mixed --data-dir data/karapinar_fullyear` ile `data/karapinar_fullyear/` (`quality: "mixed"`, `disp/*.png`, `meta.json`, `points.json`, `summary.json`) üretildi: kış `beta-precal` segmenti (6 çift, 84 gün) tepe `-4.7 cm` LOS (`range_cm=[-5.5, -4.7]`, dikey `-6.4 cm`), yaz `provisional` segmenti (`data/karapinar/`, 8 çift, 108 gün) `-5.9 cm` LOS (dikey `-8.0 cm`); iki segment `data/karapinar_fullyear/segments.json` içinde özetlendi.
- **Sıradaki iş (`docs/CALISMA_HARITASI.md`):**
  - **#3 Delta:** 9/9 `provisional` çift (`2026-06-17 → 2026-10-15`, Path 42 Frame 69) ve set profili (`pc2_delta.png`, `delta.md`) güncel ve tam.
  - **#4 Konya Ovası ikinci path çapraz kontrolü:** TAMAMLANDI → `docs/qa/PC2.md` (`konya_plain` Path 7 Descending vs `karapinar` Path 7 Descending vs `karapinar_p172` Path 172 Ascending; `2 km W of Karapınar`'da `-6.30`, `-5.93`, `-4.73 cm` LOS uyumlu).
  - **#6 `pipeline/README.md`:** TAMAMLANDI (tüm `pipeline/*.py` ve `pipeline/pc2/*.py` kullanım notları eklendi).
  - **#5 Central Valley Path 114 tam yıl (`central_valley_p114_fullyear`) — `p114_fullyear hazır`:**
    - **22/22** çift (`2025-11-30 → 2026-10-20`) `pipeline/subset/central_valley_p114/` altına indirildi ve push edildi (`b2d7837`).
    - `2026-05-17` geçişinde Frame 70 %97.7–100 NaN olduğu için zincir iki temiz 10'ar çiftlik segmentte `cumulative.py` ile işlendi (`quality: "mixed"`):
      - Yaz/Sonbahar (`data/central_valley_p114_fullyear/`, `2026-05-29 → 2026-10-20`, 144 gün, 10 çift): tepe **`-9.8 cm` LOS** (`range_cm=[-9.8, -5.4]`, dikey `-13.3 cm` @ `42.5°`).
      - Kış/İlkbahar (`data/central_valley_p114_fullyear/winter/`, `2025-11-30 → 2026-05-05`, 156 gün, 10 çift): tepe **`-6.7 cm` LOS** (`range_cm=[-7.3, -6.3]`, dikey `-8.7 cm` @ `40.1°`).
    - Segment özeti `data/central_valley_p114_fullyear/segments.json` içinde; PC9 iki geçişli tam yıl kıyası yapabilir.
- **Özgün Katkı O3 (`NISAR Pulse` CLI) — TAMAMLANDI + Kalite Standardı:**
  - `pipeline/nisarpulse/` (`__main__.py`, `search.py`, `fetch.py`, `process.py`, `catalog.py`, `README.md`, `tests/test_nisarpulse.py`) oluşturuldu; mevcut `pipeline/*.py` ve `analysis/*.py` dosyaları değiştirilmeden sarmalandı.
  - `docs/ATLAS_PLANI.md` Kalite Standardı eklendi: `--center` + `--box-deg 0.25` varsayılanı, `summary.json`'a `p2_cm`, `rate_cm_per_100d`, `valid_fraction`, `confidence`, havza dışı `--ref-lonlat` desteği, `coverage.json` ve `--data-dir`. Ağsız `8/8` birim testi geçti (`0.053s`); `.github/workflows/tests.yml` eklendi (`pages.yml`'e dokunulmadı).
  - Delta (`--dry-run` `1.20s`, `--resume` uçtan uca `6.9s`, `max_subsidence_cm=-1.3`) kanıtı `docs/story/engine.md`'ye yazıldı.
- **Küresel Atlas (`docs/ATLAS_PLANI.md` — PC2 A Önceliği):**
  - **1/5 `isfahan`** (Path 56 Frame 18, `2026-06-18 → 2026-10-16`, 9/9 `provisional` çift): `data/global/isfahan/` hazır — `max_subsidence_cm=-2.5`, `p2_cm=-2.9`, `rate_cm_per_100d=-2.08`, `valid_fraction=0.325`, `confidence=medium`.
  - **2/5 `rafsanjan`** (Path 128 Frame 17, `2026-06-23 → 2026-10-21`, 9/9 `provisional` çift, `--ref-lonlat 56.23647,30.64582`): `data/global/rafsanjan/` hazır — `max_subsidence_cm=-5.8`, `p2_cm=-4.3`, `rate_cm_per_100d=-4.83`, `valid_fraction=0.847`, `confidence=medium`.
  - **3/5 `mashhad`** (Path 78 Frame 70, `2026-06-19 → 2026-10-17`, 9/9 `provisional` çift): `data/global/mashhad/` hazır — `max_subsidence_cm=-8.6`, `p2_cm=-6.68`, `rate_cm_per_100d=-7.17`, `valid_fraction=0.705`, `confidence=medium`.
  - **4/5 `quetta`** (Path 41 Frame 17, `2026-06-17 → 2026-10-15`, 9/9 `provisional` çift): `data/global/quetta/` hazır — `max_subsidence_cm=-3.8`, `p2_cm=-2.5`, `rate_cm_per_100d=-3.17`, `valid_fraction=0.713`, `confidence=medium`.
  - **5/5 `delhi`** (Path 106 Frame 74, `2026-06-21 → 2026-10-19`, 8/8 `provisional` çift): `data/global/delhi/` hazır — `max_subsidence_cm=-4.3`, `p2_cm=-4.45`, `rate_cm_per_100d=-3.58`, `valid_fraction=0.053`, `confidence=low` (muson dönemi dekorelasyonu; tüm 5 PC2 A-önceliği şehri tamamlandı, `atlas.json`'a dokunulmadı).
- **Şu an (`KENDİ KENDİNİ DENETLEYEN MOTOR` #3 — Paz 03:35):** **Kerman** (`57.07, 30.28`) `2/9` çift indirildi/subsetlendi (`3/9` iniyor) ve **Tianjin** (`117.20, 39.10`, `8` çift) paralel başlatıldı; ikisi de `--qc` ile tamamlanınca `uncertainty/` ve `results_registry.json` güncellenecek.
