# PC3 durum

- Görev: 1 BİTTİ (insar.py + Karapınar kontrol) → Görev 2 Central Valley (PC2 npz bekleniyor)
- Durum: çalışıyor
- Güncelleme: 2026-11-14 13:22 TR

## Bitenler
### `analysis/insar.py` + `analysis/test_insar.py`
Fonksiyonlar: `wavelength_from_frequency`, `phase_to_cm`, `coh_to_float` (uint8 0-255 → 0-1), `mask_coherence`,
`mask_components` (connectedComponents==0 → NaN), `reference` (pencere NaN-medyanı), `los_to_vertical` (cm/cos(inc)), `pair_to_cm`.

Doğrulama (`cd analysis && python -m pytest -q`):
```
.........                                                                [100%]
9 passed in 0.71s
```
Testler: λ = c/1239 MHz = 0.24196 m; 2π → 12.098 cm; işaret; koherens maskesi (uint8 ve float); connComp maskesi;
referans pikseli 0; boş referans → hata; LOS→dikey; sentetik −3 cm çanak uçtan uca.

### İşaret konvansiyonu (kaynaklı)
**disp_LOS = −λ/(4π) · unwrappedPhase; NEGATİF = uydudan uzaklaşma = çökme.**
- ISCE3 interferogram = reference · conj(secondary): https://github.com/isce-framework/isce3/blob/develop/cxx/isce3/signal/Crossmul.cpp
- MintPy NISAR GUNW'yi işaret çevirmeden okur (https://github.com/insarlab/MintPy/blob/main/src/mintpy/prep_nisar.py) ve `phase2range = -1 * WAVELENGTH / (4*pi)` uygular (https://github.com/insarlab/MintPy/blob/main/src/mintpy/ifgram_inversion.py)
- MintPy FAQ: metre cinsinden pozitif = uyduya doğru (dikeyde yükselme): https://github.com/insarlab/MintPy/blob/main/docs/FAQs.md
- NISAR ATBD (coseismic notebook): negatif = radardan uzaklaşma = çökme: https://github.com/nisar-solid/ATBD
- GUNW ürün spesifikasyonu (JPL D-102272 Rev E) işareti açıkça yazmıyor (metni tarandı). Ek kontrol: Central Valley çökme çanakları negatif çıkmalı (ampirik test, kümülatif aşamada).

### Düzeltmeler (bilgi)
https://nisar-docs.asf.alaska.edu/gunw : iyonosfer faz ekranı üründe var ama unwrappedPhase'e uygulanmamış;
troposfer/gelgit katmanları da çıkarılmamış. İlk geçişte biz de uygulamıyoruz (meta.json notes'a yazılacak).

### Karapınar kontrol haritası → `docs/karapinar_checkpoint_cm.png` (13:20 TR)
- Granül: `NISAR_L2_PR_GUNW_031_007_D_069_032_2000_SH_20260918T164007_..._20260930T164042_P05023_N_F_J_001` (path 7, frame 069, bbox'u %100 kapsıyor; 2.38 GB, 95 sn indirme, ham dosya silindi)
- quality: **provisional** (P05023, iki tarih de 2026-06-17 sonrası). Referans tarihi < ikincil tarih kontrol edildi.
- λ = c / centerFrequency = **0.24393 m** (bu çerçevede; CV'deki 0.24196'dan farklı → λ her dosyadan okunuyor)
- Maskeler: koherens ≥ 0.3 + connectedComponents ≠ 0 → geçerli piksel %44.3
- Referans: otomatik, en yüksek ortalama koherensli tam geçerli 7×7 pencere → **33.727E, 37.763N** (ort. koherens 0.89)
- Değerler (LOS cm): p2 = −2.81, medyan = −0.67, p98 = +2.43. Renk aralığı ±3 cm. Tek 12 günlük çift için makul (görev: "birkaç cm altı").
- Uç değer: max +43.6 cm birkaç pikselde → unwrapping hatası; maskeleme yetmiyor, kümülatifte ayrıca filtrelenecek.
- **Dürüst not:** haritadaki kuzey–güney geniş eğilim büyük olasılıkla atmosfer/iyonosfer. Üründeki iyonosfer ekranının bu kesitteki p1–p99 aralığı ≈ 6.5 cm LOS'a denk; uygulanmadı (ürün varsayılanı). Bu tek çift çökme kanıtı olarak sunulmamalı; işaret/ölçek kontrolüdür.
- Kod: `analysis/gunw_io.py` (h5 → sözleşme npz + conncomp, ion, incidence), `analysis/checkpoint_map.py`. Alt küme: `analysis/out/karapinar_20260918_20260930.npz` (2.9 MB)
- Testler: `10 passed` (yeni: `choose_reference`)

## AI
- AI: Claude Code (Opus) → analysis kodu, testler, kaynak taraması

## BLOCKED
-
