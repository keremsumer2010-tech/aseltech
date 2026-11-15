# PC2 QA Notları — Konya Ovası İkinci Path Çapraz Kontrolü

Tarih: 2026-11-14 · Yazar: PC2 (Memir) · Kapsam: `data/konya_plain/`, `data/karapinar/`, `data/karapinar_p172/`

## 1. Kapsama Özeti (Konya Ovası `[32.4, 37.4, 33.9, 38.1]`)

- **Ana seri (`data/konya_plain/`, Path 7 Descending, Frame 69, `provisional`):** `2026-06-26 → 2026-10-12` (8 çift, 108 gün). Ovanın tamamını %100 kapsar.
  - Tepe çökme (batı tarım kuşağı, `32.6278°E, 37.8161°N`): **`-9.60 cm` LOS** (dikey tahmin **`-12.1 cm`** @ `37.6°`, referans aralığı `[-14.0, -9.6] cm`).
- **İkinci path — ters geometri (`data/karapinar_p172/`, Path 172 Ascending, `provisional`):** Aynı tarih penceresi `2026-06-26 → 2026-10-12` (8 çift, 108 gün). Ovanın doğu/Karapınar kesimini (`[33.3, 37.6, 33.8, 37.9]`) bağımsız yükselen yörüngeden kapsar.
  - Tepe çökme (`4 km W of Yağmapınar`, `33.6733°E, 37.8393°N`): **`-6.54 cm` LOS** (dikey tahmin **`-8.8 cm`** @ `41.8°`).
- **Not (Path 108 Descending Frame 69):** `lon=[29.82, 33.42]` aralığını kapsadığı için batı (`32.63°E`) kesimini görür fakat doğudaki Karapınar (`33.53°E–33.9°E`) kesimini keser; bu nedenle ova genelinde ana seri Path 7 seçilmiştir.

## 2. Nokta ve Bölge Çapraz Kontrolü (`2026-06-26 → 2026-10-12`)

| Seri / Path | Yön | Kutu | Karapınar (`33.53°E, 37.72°N`) LOS | Bölge Tepe LOS | Dikey Tahmin |
|---|---|---|---:|---:|---:|
| `konya_plain` (Path 7) | Descending | `[32.4, 37.4, 33.9, 38.1]` | `-6.30 cm` (`p04`, `33.5251°E, 37.7218°N`) | `-9.60 cm` | `-12.1 cm` |
| `karapinar` (Path 7) | Descending | `[33.3, 37.6, 33.8, 37.9]` | `-5.93 cm` (`p01`, `33.5306°E, 37.7182°N`) | `-5.90 cm` | `-8.0 cm` |
| `karapinar_p172` (Path 172) | Ascending | `[33.3, 37.6, 33.8, 37.9]` | `-4.73 cm` (`p03`, `33.5306°E, 37.7182°N`) | `-6.54 cm` | `-8.8 cm` |

## 3. Bulgular ve Sonuç

1. **Geniş vs. dar kutu tutarlılığı (Path 7):** Aynı yörünge üzerinde geniş `konya_plain` (`-6.30 cm`) ve yerel `karapinar` (`-5.93 cm`) serileri `2 km W of Karapınar` noktasında **`0.37 cm`** farkla uyumludur.
2. **Alçalan vs. yükselen yörünge tutarlılığı (Path 7 vs. Path 172):** Bağımsız yükselen yörünge (`karapinar_p172`), aynı noktada aynı işarette (**`-4.73 cm` LOS**, fark `1.20 cm` / ~%20) güçlü çökme doğrular; fark, alçalan/yükselen bakış açısı projeksiyonu ve bağımsız referans penceresi seçiminden kaynaklanmaktadır.
3. **Veri kalitesi:** Tüm üç seri `provisional` etiketlidir; iyonosfer düzeltmesi tamdır (`ion=full`).

---

# Delhi `2026-09-01` QC İncelemesi (`data/global/delhi/`, Path 106 Frame 74)

Tarih: 2026-11-15 · Yazar: PC2 (Memir) · İlgili görev: `tasks/PC2.md` (`PC1 BAĞIMSIZ KONTROL SONUCU` & `YENİ ATAMA`)

## 1. İyonosfer ve Unwrapping Kontrolü

`2026-09-01` tarihini içeren iki interferogram çifti komşu çiftlerle karşılaştırıldığında şiddetli iyonosferik bozulma ve unwrapping sıçraması doğrulanmıştır (`pipeline/subset/delhi/*.npz`):

| Çift | Geçerli Piksel (`coh>=0.35 & cc>0`) | Medyan Koherans | İyonosfer Std (`rad`) | İyonosfer Aralığı (`rad`) | Aykırı (`|d|>15 cm`) |
|---|---:|---:|---:|---|---:|
| `2026-07-15 → 2026-07-27` | `0.719` | `0.467` | `2.325` | `[-17.58, -8.43]` | `3` |
| `2026-07-27 → 2026-09-01` | `0.391` | `0.306` | `13.044` | `[-121.28, -70.50]` | `2517` |
| `2026-09-01 → 2026-09-13` | `0.782` | `0.525` | `11.130` | `[+54.53, +97.74]` | `3849` |
| `2026-09-13 → 2026-09-25` | `0.793` | `0.533` | `0.824` | `[+1.96, +6.10]` | `2652` |

- `2026-07-27 → 2026-09-01` çiftinde iyonosfer fazı `[-121.28, -70.50]` radyan ile negatif yönde patlamış (`std=13.044 rad`), `2026-09-01 → 2026-09-13` çiftinde ise `[+54.53, +97.74]` radyan ile ters işarette telafi etmiştir (`std=11.130 rad`). Bu durum `p01` zaman serisindeki `-10.0 cm` düşüş ve `+8.1 cm` geri sıçramanın doğrudan nedenidir; 36 günlük `07-27 → 09-01` çiftindeki muson koherans düşüşü (`medyan=0.306`) unwrapping hatalarını (`2517`–`3849` aykırı piksel) tetiklemiştir.

## 2. Köprü Granül Kontrolü ve Sonuç

- NASA CMR (`NISAR_L2_GUNW_PROVISIONAL_V1`, Path 106 Frame 74) üzerinde `2026-09-01` tarihini atlayacak bir köprü granül arandı:
  - `2026-07-27 → 2026-09-13` çifti CMR'da bulunmamaktadır.
  - Mevcut tek `2026-07-15 → 2026-09-13` granülü (`NISAR_L2_PR_GUNW_025_106_D_074_030_4000_SH_20260715T133143_20260715T133206_20260913T133129_20260913T133143_P05023_N_P_J_001`, `800.8 MB`) kısmi çerçeve (`_N_P_J_001`) olup indirilen Delhi kutusu (`76.83..77.33°E, 28.3..28.8°N`) içinde tüm `unw` ve `coh` pikselleri sıfırdır (`%0` kapsama).
- **Karar:** Köprü granül bulunamadığından `2026-09-01` çiftlerinin çıkarılması kümülatif zinciri `2026-07-27`'de koparmaktadır. Bu nedenle 8 çiftlik seri (`2026-06-21 → 2026-10-19`, `max_subsidence_cm=-4.3`, `valid_fraction=0.053`) korunmuş, `2026-09-01` tarihi QC uyarısıyla işaretlenmiş ve Delhi `confidence: "low"` sınıfında bırakılmıştır (`uncertainty/sigma_cm.png`, medyan `0.37 cm`).
- **Güncelleme (`--qc` motoru, `data/global/delhi/qc_report.json`):** `NISAR Pulse --qc` devralındıktan sonra Delhi yeniden çalıştırıldı; `2026-09-01` (`%94.2`), `2026-09-25` (`%33.8`) ve `2026-10-07` (`%45.3`) tek-tarih aykırı tarihleri komşu çiftler birleştirilerek otomatik düşürüldü (`affected_pixel_pct=67.28%`), geçerli piksel oranı `0.053 → 0.283` ve güven sınıfı `medium` oldu (`max_subsidence_cm=-22.3`, `p2_cm=-6.77`, `hazır: delhi`).

---

# Run it yourself — README ve Data Sayfası Kutu Metni (PC1 / PC6)

```bash
# 1. Clone and install dependencies (~30 s)
git clone https://github.com/keremsumer2010-tech/aseltech.git && cd aseltech && pip install -r requirements.txt
# 2. Reproduce any published atlas basin from its meta.json granule list (offline with cached subsets, 12–64 s; or --dry-run)
python -m pipeline.nisarpulse reproduce mashhad
# 3. Process any new ±0.25° basin on Earth with automatic cycle-jump & single-date QC (--qc)
python -m pipeline.nisarpulse run --name custom_basin --center 57.07,30.28 --start 2026-06-17 --end 2026-10-31
```
