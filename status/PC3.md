# PC3 durum

- Görev: 1 (insar.py + testler BİTTİ) → şimdi Karapınar kontrol haritası
- Durum: çalışıyor
- Güncelleme: 2026-11-14 13:05 TR

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

## AI
- AI: Claude Code (Opus) → analysis kodu, testler, kaynak taraması

## BLOCKED
-
