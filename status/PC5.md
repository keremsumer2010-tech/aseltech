# PC5 Durum Raporu

- **Durum:** çalışıyor — Atlas §3: tüm atlas şehirleri için `data/global/<şehir>/uncertainty/` üretimi ve doğrulaması (`analysis/pc5/uncertainty_map.py`)
- **Kimlik:** M3hmeT1888 · Antigravity (Gemini) · PC5
- **Güncelleme:** 2026-11-14 22:08 TR

## `16:15 B1`, `16:25 Kaynaklar Entegrasyonu`, `Q08` ve `SONSUZ DÖNGÜ` Tur 2 (`16:48 TR`)
- **16:15 B1 — Çapraz Sensör (`cross_sensor.py`, `cross_sensor.json`, `docs/story/cross_sensor.md`, `pc5_cross_sensor.png`):**
  - Canlı NASA CMR sorgusunda `OPERA_L3_DISP-S1_V1` Central Valley `bbox` içinde toplam `2,663` ürün, 2026'da `66` ürün (7 frame, en son `2026-04-26`) bulunup **NISAR yaz penceresi (`2026-06-28 → 2026-10-14`) için `0` OPERA DISP-S1 ürünü** olduğu doğrulandı (aynı pencerede `55` ham `SENTINEL-1C_SLC`, `0` `SENTINEL-1A_SLC`). Tam kapsamlı `F38502` (`12/12` CV + `10/10` GPS) `2026-02-14`'te biterken `.nc` indirme denemesi `HTTP 401 access denied` döndürdü; geçici dosyalar silindi.
  - `10` NGL GPS istasyonunda 2026 yazı (`2026-06-28 → 2026-10-14`) için NISAR L-band dikey uç değerleri `r = 0.9239` (`RMSE = 1.37 cm`, eğim `1.54`; vadi çekirdeği 5 istasyon `RMSE = 0.82 cm`) ve `25`-çift (`324` gün) tarım çekirdeği yaz medyan koheransı `0.539` (`%80.4` geçerli) hesaplandı; `RCM / RADARSAT-1` ve `SAOCOM` bağlamı eklendi (`3 passed`).
- **16:25 Kaynaklar Entegrasyonu (`literature_comparison.md`, `drivers_analysis.md`):**
  - NASA NISAR *Land Subsidence* StoryMap (`Peacock et al. 2024`, UAVSAR `2013–2017` `> 40 in`, `Miller/Jones 2020`), `NISAR_Applications_Subsidence.pdf`, CV `[-7.8, -4.7]` spread ve `central_valley_fullyear` (`-16.8 ± 2.2 cm/yr` kalıcı vs `-26.4 cm/yr` yazlık) eklendi; `drivers_analysis.md` içine `NISAR_Applications_Drought_and_Groundwater_Withdrawal1.pdf` ve `societal-benefits` bağlamı eklendi.
- **Q08 Tam Yıl Bağımsız Doğrulaması & `SONSUZ DÖNGÜ` Tur 2 (`docs/qa/PC5.md` §6–§7):**
  - `data/central_valley_fullyear/` (`26` epok, `18 beta-precal + 7 provisional`, `324 gün`) üzerinde `_fit` yeniden çalıştırılarak `12/12` nokta ayrıştırması `≤ 0.005` hata içinde doğrulandı (`UNWRAP_SUSPECT = 0`; `2026-06-28` geçişi pürüzsüz: `-2.30` / `-0.71 cm`).
  - PC3'ün Tur-1 `web/science.html` & `web/data.html` iyileştirmeleri doğrulandı; yeni `exposure.json` (`PC8`), `mexico_city` (`PC10`), `fens/crops.json` (`PC7`) kontrolleri ve **51** URL HTTP taraması (`45` doğrudan `HTTP 200 OK`) rapora eklendi.
- **AI:** Gemini → `analysis/pc5/cross_sensor.py`, `docs/story/cross_sensor.md`, `docs/story/literature_comparison.md`, `docs/story/drivers_analysis.md`, `docs/qa/PC5.md` §6–§7

## 15:30 Paketi Görev 5 & `SONSUZ DÖNGÜ` Tur 1 — Bağımsız Kontrol ve QA Denetimi (`docs/qa/PC5.md`)
- `Q08` tam yıl (`data/central_valley_fullyear/`) henüz üretilmemiş; ancak `pipeline/subset/central_valley_beta/` içinde `15` adet `beta-precal` `.npz` çifti (`2025-11-24 → 2026-05-23`) indiği ve provisional zincirle (`2026-06-28`) arada **36 günlük boşluk** olduğu tespit edilip `docs/qa/PC5.md` §4'e işlendi. Yeni `central_valley_p114_cum.npz` (`vertical.json`) ve `uk_clay/` (`9` çift, `below_detection`, `3.62 cm` eşik) doğrulandı.
- `SONSUZ DÖNGÜ` Tur 1 (`a–d`):
  - `a)` `analysis/out/{central_valley,karapinar}_cum.npz` sabit, `uncertainty` + `area_stats.json` güncel.
  - `b)` `web/index.html` tüm sayılarla tutarlı; `web/science.html` içinde 3 tutarsızlık (`-6.2..-7.8 cm` yerine `-4.7..-7.8 cm`, `12-day` yerine `12–24 day`, `SME2 (in progress)`) ve `web/data.html` eksik indirme bağlantıları `docs/qa/PC5.md` §5'te listelendi.
  - `c)` `literature_comparison.md` + `sources.md` içindeki **29 / 29** benzersiz URL HTTP `200 OK`.
  - `d)` `web/science.html` için 4 bilimsel yöntem geliştirme önerisi eklendi.
- `C:\Users\celik\AppData\Local\Programs\Python\Python312\python.exe -m pytest analysis/pc5 -q` → `19 passed`.
- **AI:** Gemini → `docs/qa/PC5.md` §4–§5

## 15:30 Paketi Görev 4 — Hidro-Tarımsal Sürücü ve Gecikmeli Korelasyon Analizi (`drivers_analysis.md`, `pc5_drivers.png`)
- `analysis/pc5/drivers_analysis.py` ve `analysis/pc5/test_drivers_analysis.py` ile `data/central_valley/drivers.json` (`2026-06-28 – 2026-10-14`, `N = 8` epok) üzerinde `lag 0` (`n=8`), `lag 1` (`12–24 g`, `n=7`) ve `lag 2` (`24–36 g`, `n=6`) Pearson `r`, Spearman `rho`, Fisher-`z` %95 GA, Student-`t` `p` ve tüm `n!` permütasyonlar üzerinden kesin permütasyon `p` değerleri hesaplandı.
- `drivers.json` ön korelasyonları (`soil_moisture` `lag 0`: `0,573`, `irrigation_index` `lag 0`: `0,654`, `soil_moisture` `lag 1`: `0,638`) doğrulandı; ancak `N = 8` kritik eşiği (`|r_krit| = 0,707`–`0,811`, %80 güç alt sınırı `|r| ≥ 0,849`) altında hiçbiri `alpha = 0,05` düzeyinde anlamlı çıkmadı ve trendden arındırılmış `7` aralık hızında (`cm/gün`) eşzamanlı korelasyon `0,01`–`0,17` (`p ≥ 0,75`) düzeyine indi.
- `pc5_drivers.png` görsel kontrolü temiz.
- `C:\Users\celik\AppData\Local\Programs\Python\Python312\python.exe -m pytest analysis/pc5/test_drivers_analysis.py -q` → `2 passed`.
- **AI:** Gemini → `analysis/pc5/drivers_analysis.py`, `docs/story/drivers_analysis.md`, `docs/story/media/pc5_drivers.png`

## 15:30 Paketi Görev 3 — Obruk–Çökme İstatistiksel Testi (`sinkhole_stats.md`, `pc5_sinkhole_perm.png`)
- `analysis/pc5/sinkhole_stats.py` ve `analysis/pc5/test_sinkhole_stats.py` ile Karapınar `40.194` geçerli `80 m` pikseli (`data/karapinar/sinkholes.geojson`, `29` obruğun `16`'sında `0–2 km` kapsama) üzerinde dört katmanlı anlamlılık testi çalıştırıldı:
  - Piksel düzeyi (`n_near = 236` vs `n_bg = 38.973`): fark `-3,41 cm`, %95 bootstrap GA `[-3,58, -3,24] cm`, `10.000` permütasyon `p = 0,0001`, Welch `t = -39,66`.
  - Ayrık `1,04 km` (`13×13` piksel) blokları (`14` vs `362`): fark `-3,04 cm` (`-3,68` vs `-0,64 cm`), %95 GA `[-3,59, -2,41] cm`, permütasyon `p = 0,0001`, Welch `t = -9,70` (`p = 9,7×10⁻⁸`).
  - Ayrık `2,08 km` (`26×26` piksel) makro-blokları (`8` vs `111`): fark `-2,93 cm`, permütasyon `p = 0,0001`, Welch `p = 3,0×10⁻⁴`.
  - Katı `29`-obruk kümesi mekânsal kaydırma testi (`3.423` geçerli kaydırma): gözlenen `-3,41 cm` null medyan `+0,13 cm`'e karşı `p = 0,0207`.
- `docs/story/sinkhole_stats.md` içinde mekânsal otokorelasyon uyarısı ve halk dilinde 3 cümlelik sonuç yayımlandı; `pc5_sinkhole_perm.png` görsel kontrolü temiz.
- `C:\Users\celik\AppData\Local\Programs\Python\Python312\python.exe -m pytest analysis/pc5/test_sinkhole_stats.py -q` → `3 passed`.
- **AI:** Gemini → `analysis/pc5/sinkhole_stats.py`, `docs/story/sinkhole_stats.md`, `docs/story/media/pc5_sinkhole_perm.png`

## 15:30 Paketi Görev 2 — Etkilenen Alan Zaman Serisi (`area_stats.json`, `pc5_area_cv.png`)
- `analysis/pc5/area_stats.py` ve `analysis/pc5/test_area_stats.py` ile Central Valley (`7.704,7 km²` geçerli ayak izi) ve Karapınar (`212,3 km²` geçerli ayak izi) için tüm epoklarda `<-2 cm` ve `<-5 cm` eşikli etkilenen alan zaman serisi üretildi.
- Central Valley (`2026-10-14` final): `<-2 cm` = `1.578,3 km²`, `<-5 cm` = `239,5 km²`, tepe `1 km` blok-medyan = `-7,80 cm`.
- Karapınar (`2026-10-12` final): `<-2 cm` = `28,7 km²`, `<-5 cm` = `3,1 km²`, tepe `1 km` blok-medyan = `-5,93 cm`.
- `docs/story/key_findings.md` ve `docs/story/key_findings_public.md` içindeki alan sayıları bbox-kırpılmış `area_stats.json` değerleriyle senkronize edildi.
- `C:\Users\celik\AppData\Local\Programs\Python\Python312\python.exe -m pytest analysis/pc5/test_area_stats.py -q` → `2 passed`.
- **AI:** Gemini → `analysis/pc5/area_stats.py`, `data/central_valley/area_stats.json`, `data/karapinar/area_stats.json`, `docs/story/media/pc5_area_cv.png`

## 15:30 Paketi Görev 1 — Halk Dilinde Anahtar Bulgular (`docs/story/key_findings_public.md`)
- `docs/story/key_findings.md` içindeki 8 ana bulgu `docs/REVIEW_1500.md` kurallarına göre ana sayfa için tek cümlelik, jargonsuz (`LOS`, `Cramér–Rao`, `Pearson`, `RMSE`, `coherence` içermeyen), sayı + birim + tarih + kaynak dosya içeren 8 maddeye dönüştürüldü.
- **AI:** Gemini → `docs/story/key_findings_public.md`

---

## Görev 7 & `docs/REVIEW_1500.md` Uyumu (`docs/qa/PC5.md` §3, `docs/story/key_findings.md`, `docs/story/game_sensitivity.md`)
- `docs/qa/PC5.md` §3'e tam yıl zinciri (`Q07`/`Q08`) geldiğinde çalıştırılacak komut sırası, beklenen çıktılar (`decomp.json`, `decomp_permanent.png`, `decomp_seasonal.png`, `sigma_cm.png`), kalite kapıları (`--quality mixed`, `suspect_ids == []`) ve `pyproj` ortam uyarısı eklendi.
- `tasks/PC5.md` 15:00 notu ve `docs/REVIEW_1500.md` yazım kuralları gereği tüm İngilizce metinler (`docs/story/key_findings.md`, `game_sensitivity.md`) sade NASA Earth Observatory üslubuna çekildi; terimler (LOS, coherence, Cramér–Rao) ilk geçişte açıklandı, tarihsiz sayı bırakılmadı ve `Figure 1.` kredisi eklendi.
- **Doğrulama:** `pytest analysis/pc5 -q` → **12 passed** (`test_uncertainty_map.py`, `test_risk_sensitivity.py`, `test_game_sensitivity.py`); `pytest analysis/decomp -q` → **16 passed, 2 failed** (`test_run_decomp_*` yerel Python 3.12'de `pyproj` kurulu olmadığı için `analysis/cumulative.py` içinde başarısız — kontrol listesinde belgelendi).
- **AI:** Gemini → `analysis/pc5/{uncertainty_map.py,risk_sensitivity.py,game_sensitivity.py}`, `test_*.py`, `data/*/uncertainty/`, `docs/story/{literature_comparison.md,key_findings.md,risk_sensitivity.md,game_sensitivity.md,game_sensitivity.png}`, `docs/qa/PC5.md`

---

## Görev 6 — Oyun Modeli Monte Carlo Duyarlılığı (`analysis/pc5/game_sensitivity.py`, `docs/story/game_sensitivity.md`, `.png`)
- `game/model.js` (`ValleyModel` v2) denklemleri değiştirilmeden Python'a aktarıldı; Terra Bella (`p01`) kalibrasyon noktasında kalibresiz çıktı `d_model(k=1) = -17.18 cm`, kalibre çarpan `k_cal = 0.6232` ile 108 gün hedefi `-10.10 cm` (`%0.00` artık).
- `N = 1,000` Monte Carlo denemesinde (`S_skv`, `S_ske`, `b0`): 24 aylık dikey çökme sabit su yılında `p10 = -25.32 cm / p50 = -14.30 cm / p90 = -7.62 cm`, stokastik 2. yıl su yılında `p10 = -27.10 cm / p50 = -13.70 cm / p90 = -6.23 cm`; 108 günlük `-10.1 cm` NISAR hedefi örneklerin `%30.0` diliminde (`%14.9` `±%10` bandında) ve `b0 · S_skv = 0.02356` eş-çökme hiperbolü üzerinde yer almaktadır. `pytest analysis/pc5/test_game_sensitivity.py -q` → **4 passed**.

## Görev 5 — Altyapı Risk Eşiği Duyarlılığı (`analysis/pc5/risk_sensitivity.py`, `docs/story/risk_sensitivity.md`)
- `risk/compute_risk.py` değişmeden doğrudan yeniden kullanıldı; 645 segmentin tamamı baz eşiklerde (`10.0 mm/km`, `10.0 cm`) `81` yüksek / `131` orta / `433` düşük risk ile `data/central_valley/assets.json` özetini birebir doğruladı.
- ±25% taramasında (`7.5 / 10.0 / 12.5 mm/km` × `7.5 / 10.0 / 12.5 cm`) yüksek riskli segment sayısı `72–115` arasında değişirken ilk 10 koridor ve sırası (`Tulare Irrigation District Canal` `57.01 mm/km` ... `CA 65` `42.34 mm/km`) tüm 9 eşik kombinasyonunda **%100 sabit** kaldı. `pytest analysis/pc5/test_risk_sensitivity.py -q` → **3 passed**.

## Görev 3 & 4 — Q26 + Q27 + `docs/story/key_findings.md`
- **Q26:** `python -m analysis.decomp.point_quality` çalıştırılarak `docs/qa/PC5.md` §2 tabloları doğrulandı (`suspect_ids=[]`, `elevated_ids=["p03", "p08"]`, `watch_ids=["p01", "p02", "p04", "p05"]`).
- **Görev 4 + Q27 (`docs/story/key_findings.md`):** Repodaki tüm sayısal çıktılarla doğrudan hesaplanıp çapraz kontrol edilen 8 anahtar bulgu + Q27 GNSS istatistiksel yorumu (10 istasyon genel medyan RMSE `1.004 cm` / `r=0.541`; hareketli `>2 cm` 5 istasyon medyan RMSE `0.834 cm` / `r=0.820` [havza içi 4 istasyon `r=0.793–0.896`]; durağan `<=2 cm` 5 istasyon medyan RMSE `1.570 cm` / `r=-0.101`; 3 cümle İngilizce yorum) yazıldı (yetki kuralı gereği PC3'ün `docs/story/uncertainty.md` dosyasına dokunulmadan `docs/story/key_findings.md` §2 altına yerleştirildi). `tasks/QUEUE.md` üzerinde Q26 ve Q27 `- [x PC5]` olarak işaretlendi.

## Görev 2 — Literatür Karşılaştırması (`docs/story/literature_comparison.md`)
- Central Valley (`Neely et al. 2021`, `Ojha et al. 2019`, `Farr & Jones / NASA Earth Observatory 2017`, `Sneed et al. / USGS SIR 2018-5144`) ve Karapınar/Konya (`Orhan et al. 2021`, `Üstün et al. 2010`, `Canaslan Çomut et al. 2015`) çalışmalarının tamamı HTTP 200 ile canlı olarak doğrulandı.
- `data/*/summary.json` verilerindeki 108 günlük yaz dönemi kestirimlerinin (`-26.4 cm/yr` LOS Central Valley, `-20.0 cm/yr` LOS Karapınar) neden çok yıllık ortalama hızların üzerinde kaldığı (yaz zirve sulama pompajı vs. kış elastik geri sıçraması `S_ke`) İngilizce teknik paragrafla açıklandı.

## Görev 1 — Piksel Bazında Belirsizlik Haritası (`analysis/pc5/uncertainty_map.py`)
- **Yöntem:** Cramér–Rao / Rodriguez & Martin (1992) faz standart sapması $\sigma_\phi = \frac{\sqrt{1-\gamma^2}}{\gamma\sqrt{2L}}$, $\sigma_d = \frac{\lambda}{4\pi}\sigma_\phi \cdot 100$ ve $N$ ardışık `provisional` çift üzerinden kare-toplam ($\sigma_{\text{toplam}} = \sqrt{\sum \sigma_{d,i}^2}$).
- **Bakış Sayısı ($L$) Kaynağı:** `docs/gunw_structure.md` §2 içinde gerçek HDF5 üstverisinden (`numberOfAzimuthLooks=16`, `numberOfRangeLooks=13` → nominal $L = 208$). RSLC aşırı örnekleme / `2000_SH` (Karapınar) nedeniyle etkin bakış $L_{\text{eff}} = 100$'e düşerse ölçek çarpanı $1.442\times$ olarak `meta.json`'da ayrıca raporlandı (`--looks` parametresi açık).
- **Varsayımlar:** (1) Çiftler arası istatistiksel bağımsızlık, (2) yalnızca kısa ölçekli koherens/beneklenme faz gürültüsünü kapsar; **atmosferik su buharı türbülansı, rampa kalıntısı ve faz açma hatalarını KAPSAMAZ**.
- **Sayılar:**
  - **Central Valley** (`data/central_valley/uncertainty/`, 7 çift, PNG `1200x1000` RGBA, `vmin=0.0`, `vmax=1.0 cm`, geçerli `%64.69`): medyan **`0.294 cm`**, p90 **`0.471 cm`**, min–max `0.027–0.763 cm` ($L=100$ duyarlılığı: medyan `0.424 cm`, p90 `0.679 cm`).
  - **Karapınar** (`data/karapinar/uncertainty/`, 8 çift, PNG `500x300` RGBA, `vmin=0.0`, `vmax=1.0 cm`, geçerli `%15.44`): medyan **`0.326 cm`**, p90 **`0.548 cm`**, min–max `0.068–0.765 cm` ($L=100$ duyarlılığı: medyan `0.470 cm`, p90 `0.790 cm`).
- **Doğrulama:** `pytest analysis/pc5/test_uncertainty_map.py -q` → **5 passed**, her iki `sigma_cm.png` dosyası açılıp saydamlık ve bbox hizalaması kontrol edildi.
- **AI:** Gemini → `analysis/pc5/uncertainty_map.py`, `test_uncertainty_map.py`
