# PC3 durum

- Görev 1: BİTTİ (insar.py + testler + Karapınar kontrol haritası)
- Görev 2: BİTTİ — **Central Valley kümülatif harita + points + summary + _cum.npz PUSH edildi** (13:30 TR)
- Q02 Karapınar kümülatif: BİTTİ (13:55 TR) — aşağıda
- Sıradaki: 17:00 QA (sitedeki sayılar = çıktılarım mı) → Q08 hazırlığı
- **14:11 Mehmet talimatı:** PC3, PC5'in Görev 1'ini (`analysis/decomp/decompose.py` + testler) devraldı. PC5 bu işi TEKRARLAMASIN; PC5 game_model.md ve belirsizlik bütçesiyle devam edebilir.
- Güncelleme: 2026-11-14 13:55 TR

## Bağımsız yeniden üretim (14:05)
PC2 iyonosferli 7 npz'yi push etti; `cumulative.py` artık onları kullanıyor (`pair_stats.json` → `pipeline/...`). Sonuç birebir aynı: −7.8 cm, aralık −6.2…−7.8 → PC2 ve PC3 kesimleri tutarlı. Önceki NOT (PC2 npz'de `ion` boş) artık geçersiz.

## Referans duyarlılığı (YENİ, önemli)
Mutlak değer referans seçimine bağlı. `summary.json`'a eklendi: `max_subsidence_range_cm` + `reference_sensitivity`
(≥30 km uzaktaki en iyi ikinci referansla aynı nokta yeniden hesaplanıyor).
- Central Valley: Woodlake referansı −7.8 cm; alternatif referans (−120.059, 35.763) ile aynı noktada −6.2 cm → **aralık −6.2 … −7.8 cm LOS**. Çanakların YERİ değişmiyor.
- Referans artık bbox içinde seçilmek zorunda (bbox dışına kaymıştı, düzeltildi).
- Sunum önerisi: "about 6–8 cm (line of sight) in 3.5 months".

## Q02 · Karapınar kümülatif → `data/karapinar/` (sinkholes.geojson'a dokunulmadı)
| | |
|---|---|
| Dönem | 2026-06-26 → 2026-10-12 (108 gün), 8 ardışık provisional çift, path 7 descending frame 69 |
| Maks çökme (LOS) | **−5.9 cm**, 2 km W of Karapınar (33.531E, 37.718N), dikey ≈ −8 cm (tahmin) |
| Diğer noktalar | hepsi −2.6 … +0.5 cm (gürültü düzeyine yakın) |
| Referans | 33.744E, 37.747N, 21×21 px pencere (~1.7 km). 7×7 pencerede son çiftte sahne geneli −2.1 cm ortak mod hatası vardı; büyük pencereyle çift medyanları ≤ 0.9 cm |
| Kapsama | **tüm çiftlerde geçerli piksel sadece %14** (12 günlük L-bant, tarım alanı dekorelasyonu); kalan alan ilçe merkezi + doğu volkanik yayla |
| Güven | **DÜŞÜK-ORTA**: tek belirgin sıcak nokta; ≥30 km alternatif referans yok (sahne dar) |

Literatür: Konya havzasında Sentinel-1 InSAR (2014–2022) zirve hız ~9 cm/yıl; obruklar Karapınar'da yoğun (Orhan vd. 2024, Geosciences): https://zaguan.unizar.es/record/132155 · Karapınar çok-sensörlü InSAR+GNSS çalışması (Orhan vd. 2021, Sensors): https://www.mdpi.com/1424-8220/21/3/774 → mertebe tutuyor (bizimki yaz sezonu).
Çıktılar: `data/karapinar/{meta,points,summary}.json`, `data/karapinar/disp/<9 tarih>.png`, `analysis/out/karapinar_cum.npz` (0.2 MB), `karapinar_cum_stack.npz` (0.7 MB), `karapinar_pair_stats.json`.
Komut: `python analysis/cumulative.py karapinar --ref-radius 10`

## Central Valley sonucu (PC1 / PC5 / PC6 için)
| | |
|---|---|
| Dönem | **2026-06-28 → 2026-10-14** (108 gün), 7 ardışık provisional çift, zincirde boşluk yok |
| Maks çökme (LOS) | **−7.8 cm**, 6 km N of Terra Bella (−119.022, 36.011) — ~1 km blok medyanı |
| Dikey tahmin | −10.1 cm (LOS / cos 44°; tamamen dikey hareket varsayımı) |
| Yıllık hız | **−26.4 cm/yıl `estimate`** — yaz sezonunun doğrusal uzatılması; kışın kısmi geri dönüş olduğundan yıllık net hızı muhtemelen ABARTIR |
| Diğer çanaklar | 21 km S of Lemoore −7.8 · 10 km SW of Huron −7.2 · 15 km W of Corcoran −7.0 · Alpaugh/Earlimart B'si geniş çanak ≈ −5.4 |
| Referans | −119.1456, 36.4532 (Woodlake KB, Sierra eteği; 7×7 pencere ort. koherens 0.97; tüm çiftlerde aynı) |
| Renk | RdBu, vmin/vmax = −6/+6 cm tüm tarihlerde sabit; kırmızı = çökme |

Oyun/sunum için tek sayı: `data/central_valley/summary.json` → `max_subsidence_cm: -7.8` (LOS, 108 gün). Sunumda "about 8 cm in 3.5 months (line of sight), roughly 10 cm vertical" denebilir; yıllık değer sadece "estimate".

### Çıktılar
- `data/central_valley/meta.json`, `points.json` (12 nokta: 5 en çok çöken, 5 medyan, 2 referans yakını; adlar OSM yerleşimlerinden), `summary.json`
- `data/central_valley/disp/<8 tarih>.png` (RGBA, 1200×1000, bbox'a oturan lat/lon ızgarası, NaN şeffaf; toplam 12.6 MB)
- `analysis/out/central_valley_cum.npz` (5.2 MB: `cum_cm, x, y, epsg, dates, quality, incidence(f16), reference_rc`) → PC6 risk
- `analysis/out/central_valley_cum_stack.npz` (18.8 MB: tarih başına kümülatif yığın, float16) → Q05 GNSS
- `analysis/out/central_valley_pair_stats.json` (çift başına istatistik)

### Yöntem (her adım meta.json `notes` içinde)
1. faz → cm: −λ/(4π), λ her dosyanın `centerFrequency`'sinden (0.24196 m)
2. **Ürünün iyonosfer ekranı çıkarıldı** (`unw − ionospherePhaseScreen`). Test: 2 çiftte vadi geneli std 4.5→2.2 ve 5.8→3.2 cm düştü → işaret doğru.
3. Maskeler: koherens ≥ 0.3, connectedComponents ≠ 0, < 200 px kopuk adalar, 720 m blok medyanından > λ/4 sapan pikseller (unwrapping döngü hatası koruması; çift başına 0–25 piksel)
4. **Çift başına düzlem + doğrusal yükseklik terimi çıkarıldı** (Copernicus DEM GLO-90; MintPy `tropo_phase_elevation` yöntemi). Yükseklik katsayıları: +0.6, +4.9, +0.9, −8.5, +4.1, +1.4, −1.8 cm/km. Bu, vadi genelindeki yavaş bir eğimin bir kısmını da silebilir (meta'da yazıyor).
5. Hepsi aynı referans penceresine göre sıfırlandı, toplandı; sadece tüm çiftlerde geçerli pikseller gösteriliyor (%62.9).
6. Başlık sayısı: 1 km blok (13×13 px, ≥%50 geçerli, blok içi std ≤ 2 cm) medyanlarının en negatifi — tek piksel/dere yatağı artefaktları başlığı belirleyemez.

Çift başına p2/p50/p98 (cm, düzeltmeden sonra): [−2.1,−0.2,1.5] [−2.7,0.2,2.4] [−2.9,−0.8,1.6] [−2.5,0.4,2.6] [−2.0,0.4,4.3] [−3.6,−0.7,1.2] [−1.3,0.2,1.6]

### Doğrulama
- `cd analysis && python -m pytest -q` → **17 passed in 3.31s** (insar 15 + cumulative 3; sentetik çanak, deramp, yükseklik terimi, döngü koruması, zincir boşluğu, beta-precal atlama, lat/lon kuzey-yukarı)
- JSON'lar `json.load` ile açıldı; PNG'ler RGBA, gözle kontrol edildi: çöken yerler kırmızı; Tulare Gölü yatağı düşük koherensten maskeli (gri).
- **İşaret ampirik kontrolü:** bilinen çökme bölgeleri (Terra Bella/Friant-Kern, Corcoran, Alpaugh) negatif çıktı ✔
- Elenen sahte sinyaller (geliştirme sırasında yakalandı): 07-10→07-22 çiftinde tek şeritte −11 cm (bir 2π kayması), Woodlake GD'de dere yatağında −18 cm leke; ikisi de filtrelerle başlık hesabından çıktı.

### Literatür kıyası (mertebe tutuyor → yayınlandı)
- Bizim: en derin çanaklarda ~2.2 cm/ay LOS (~2.8 cm/ay dikey), sulama sezonu.
- NASA JPL (2015, kuraklık): Corcoran yakını 8 ayda ~33 cm ≈ 4 cm/ay: https://www.jpl.nasa.gov/news/nasa-california-drought-causing-valley-land-to-sink/
- LBNL 2023 (Kings/Tulare): yıllık net ≈ −6…−8 cm/yıl, Corcoran–Alpaugh çanağı yakınında artış: https://wdwagsa.specialdistrict.org/files/f1e742610/2023_Lawrence-Berkeley-National-Laboratory-Study.pdf
- Friant-Kern Kanalı: en derin çökme Terra Bella yakınında (bizim maks noktası ile aynı yer): https://www.kvpr.org/environment/2017-08-03/friant-kern-canal-slows-by-60-percent-subsidence-to-blame
- Sonuç: aynı mertebe (cm/ay). Yaz sezonu hızımız yıllık net literatür değerinden yüksek — mevsimsellik ile tutarlı.

### Dürüst sınırlamalar
- Troposfer modeli (ürün küpleri) ve katı yer gelgiti uygulanmadı; yükseklik regresyonu + düzlem ile yaklaşıldı. Çift başına ~1–3 cm atmosferik gürültü kalır.
- Kuzeydoğu etekteki (Woodlake–Ivanhoe) narenciye bahçelerinde benekli güçlü negatif değerler var: bitki örtülü alanlarda kısa aralıklı çiftleri toplamanın faz yanlılığı olabilir → **düşük güven**; p05 (5 km NE of Ivanhoe) bu bölgede.
- LOS tek geometri (yükselen yörünge, path 34); doğu-batı yatay hareket ayrılamaz.
- Kalibrasyon/doğrulama NISAR projesinin (NASA-JPL, ISRO) işidir; ürünü yayınlandığı hâliyle kullandık, kalibre etmedik.

## NOT (başkalarının dosyaları — düzeltmedim)
- NOT: `pipeline/subset/central_valley/*.npz` içinde `ion` boş (PC2). İyonosfer ekranı olmadan çift başına ~±7 cm vadi geneli hata var. Mümkünse PC2 `ionospherePhaseScreen`'i de kessin. Şimdilik aynı çift için iyonosferli kendi yedek alt kümemi (`analysis/out/subset/`, repoda değil) kullanıyorum; `cumulative.py` bunu otomatik seçiyor ve hangi dosyanın kullanıldığını `pair_stats.json`'a yazıyor.

## Görev 1 kayıtları
### `analysis/insar.py` · işaret konvansiyonu (kaynaklı)
**disp_LOS = −λ/(4π) · unwrappedPhase; NEGATİF = uydudan uzaklaşma = çökme.**
- ISCE3 interferogram = reference · conj(secondary): https://github.com/isce-framework/isce3/blob/develop/cxx/isce3/signal/Crossmul.cpp
- MintPy NISAR GUNW'yi işaret çevirmeden okur (https://github.com/insarlab/MintPy/blob/main/src/mintpy/prep_nisar.py), `phase2range = -1 * WAVELENGTH / (4*pi)` (https://github.com/insarlab/MintPy/blob/main/src/mintpy/ifgram_inversion.py)
- MintPy FAQ: metre cinsinden pozitif = uyduya doğru: https://github.com/insarlab/MintPy/blob/main/docs/FAQs.md
- NISAR ATBD (coseismic notebook): negatif = radardan uzaklaşma = çökme: https://github.com/nisar-solid/ATBD
- GUNW spesifikasyonu (JPL D-102272 Rev E) işareti açıkça yazmıyor (metni tarandı). Dosyada referans tarihinin ikincil tarihten önce olduğu kodda kontrol ediliyor.
- Düzeltme katmanları: https://nisar-docs.asf.alaska.edu/gunw — iyonosfer ekranı üründe ama varsayılan olarak uygulanmamış.

### Karapınar kontrol haritası → `docs/karapinar_checkpoint_cm.png` (12:58 TR)
- Granül: `NISAR_L2_PR_GUNW_031_007_D_069_032_2000_SH_20260918T164007_..._20260930T164042_P05023_N_F_J_001` (path 7, frame 069, bbox %100; ham dosya silindi)
- quality **provisional**; λ = **0.24393 m** (bu çerçevede; λ her dosyadan okunuyor)
- Maskeler: koherens ≥ 0.3 + connComp ≠ 0 → %44.3 geçerli. Referans 33.727E, 37.763N (koherens 0.89)
- LOS cm: p2 −2.81, medyan −0.67, p98 +2.43 (renk ±3 cm). İyonosfer bu haritada UYGULANMADI (ekranın p1–p99 aralığı ≈ 6.5 cm LOS) → bu tek çift çökme kanıtı değil, işaret/ölçek kontrolü.

## AI
- AI: Claude Code (Opus) → analysis kodu, testler, kaynak taraması, sonuç kontrolü

## BLOCKED
- (çözüldü 14:00) tasks/QUEUE.md rebase çakışması: PC2'nin Q01 satırı ile benim Q02 satırım bitişikti. Mehmet'in onayıyla iki satır da korunarak çözüldü (`[~PC2] Q01` + `[x PC3] Q02`), başka satıra dokunulmadı.
