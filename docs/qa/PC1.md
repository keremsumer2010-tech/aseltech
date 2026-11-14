# PC1 QA notları

## 2026-11-14 12:55 — Yedek GUNW incelendi (PC2/PC3 için hızlandırıcı; PC2'nin `docs/gunw_structure.md` görevi yine onda)
Dosya: `NISAR_L2_PR_GUNW_030_034_A_020_031_4000_SH_20260908T130856_..._20260920T130931_P05023_N_F_J_001.h5` (2.34 GB, PC1 diskinde `raw/`, giriş Earthdata ile çalıştı, indirme ~3 dk).

Kullanılacak yollar (`science/LSAR/GUNW/grids/frequencyA/` altında):
| Ne | Yol | Not |
|---|---|---|
| Unwrapped faz | `unwrappedInterferogram/HH/unwrappedPhase` | (4284, 4356) float32, birim `radians`, `_FillValue` NaN |
| Koherens | `unwrappedInterferogram/HH/coherenceMagnitude` | aynı ızgara |
| Bağlı bileşenler | `unwrappedInterferogram/HH/connectedComponents` | uint16; 0 = güvenilmez bölge (maskelemek için) |
| İyonosfer faz ekranı | `unwrappedInterferogram/HH/ionospherePhaseScreen` | ürün içinde; ÇIKARILMIŞ MI değil mi doğrulanmalı (ATBD/ürün spesifikasyonu) |
| Koordinatlar | `unwrappedInterferogram/HH/xCoordinates`, `yCoordinates` | UTM metre; x 83560→431960, y 4227080→3884440 (y azalan) |
| Projeksiyon | `unwrappedInterferogram/HH/projection` | **EPSG 32611** (UTM 11N) |
| Aralık | `xCoordinateSpacing` / `yCoordinateSpacing` | 80 / −80 m |
| Maske | `unwrappedInterferogram/mask` | uint32 |
| Merkez frekans | `centerFrequency` | **1 239 000 000 Hz → λ = c/f = 0.24196 m** |
| Geliş açısı (küp) | `science/LSAR/GUNW/metadata/radarGrid/incidenceAngle` | (20 yükseklik, 697, 709), kendi x/y koordinatlarıyla; enterpole et |
| LOS birim vektörü | `metadata/radarGrid/losUnitVectorX`, `losUnitVectorY` | küp |
| Troposfer/katı yer gelgiti ekranları | `metadata/radarGrid/wetTroposphericPhaseScreen`, `hydrostaticTroposphericPhaseScreen`, `slantRangeSolidEarthTidesPhase` | küp; uygulanıp uygulanmadığı doğrulanmalı |

Kimlik: `compositeReleaseId = P05023`, `productVersion = 1.0.11`, `productSpecificationVersion = 1.5.0`, `processingType = Nominal`.
Örnek faz aralığı (8'de 1 örnek): −5.7 … +8.7 rad (12 günlük çift için ≈ birkaç cm; makul).

## ⚠️ Düzeltme: dalga boyu
Belgelerde λ ≈ 0.2384 m yazıyordu. Ürün `centerFrequency` = 1239 MHz → **λ = 0.24196 m**. Kural: λ'yı sabit yazma, **her dosyadan `c / centerFrequency` ile oku**. `rules/VERI_SOZLESMESI.md` buna göre güncellendi.
