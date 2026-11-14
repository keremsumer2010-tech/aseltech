# aseltech — çalışma kuralları (TÜM Claude oturumları okur)

## Proje
NASA Space Apps 2026, görev "Dancing with the SARs". Ürün: **NISAR Pulse — Follow the Water**.
Ana cümle: "NISAR Handbook'un kendi uygulama sorularını (§2.4) gerçek veriyle cevaplıyoruz."
Hikâye: sulama → toprak nemi → yeraltı suyu pompalama → yer çöküyor (yazın iner, kışın kısmen kalkar).
Bölgeler (öncelik sırası): 1) California Central Valley 2) Konya 3) UK (kil şişme-büzülme, Holme Fen).

## Resmi kaynaklar (algoritmayı YENİDEN İCAT ETME — uyarlayıp kaynak göster)
- NISAR Science Users' Handbook 2. baskı (Ekim 2025). §2.4 uygulama soruları, §5 ürünler, §6 algoritmalar, §7 hata kaynakları.
- Solid Earth ATBD notebook'ları: https://github.com/nisar-solid/ATBD (MintPy tabanlı; `prep/NISAR_prep.ipynb`, `methods/secular|transient`)
- L3 ATBD Cookbook: https://github.com/ASFOpenSARlab/NISAR_ATBD_Cookbook (crop area, inundation, disturbance, biomass, sea ice, solid earth)
- Ürün notları: GUNW 80 m UTM grid; GCOV = gamma0 (terrain corrected); metadata cube'larda LOS birim vektörü/incidence var.
- MintPy Windows'ta kurulmazsa: WSL veya ASF OpenSARLab.

## BİZİM özgün katkılarımız (resmi kodun ÜSTÜNE)
1. **Kalıcı vs geri dönen çökme:** zaman serisini trend (kalıcı, akifer sıkışması) + mevsimsel genlik (geri dönen) olarak ayır → "Permanent Loss Map".
2. **Sebep-sonuç füzyonu:** aynı piksel/bölgede çökme hızı × SME2 toprak nemi × GCOV sulama sinyali zaman çizelgesi ve gecikmeli korelasyon.
3. **Altyapı risk indeksi:** OSM kanal/set/yol/demiryolu hatları boyunca çökme EĞİMİ (diferansiyel çökme) → riskli segment sıralaması. Konya'da obruk yakınlığı.
4. **Bağımsız doğrulama:** GNSS istasyon zaman serileriyle otomatik karşılaştırma (RMSE, korelasyon).
5. **Tercüman katmanı:** LOS→dikey dönüşüm, belirsizlik etiketi, kurallarla üretilen sade İngilizce cümle + insan ölçeği karşılaştırma (LLM ile sayı üretme YOK).
6. **Tek motor:** `sites.yaml` → aynı hat her bölgede çalışır; web `data/catalog.json` okur.
Teslim: Paz 15 Kas 23:59 UK (= Pzt 02:59 TR). Tüm çıktı metni İNGİLİZCE.

## Rol sistemi
- **PC1 = yönetmen** (Kerem'in Claude'u). Görev yazar, denetler, birleştirir.
- **PC2–PC6 = işçi.** Aynı bilgisayarda iki ajan varsa AYRI klon klasörü kullanır; sadece kendi dosyalarını commit eder (`git add <kendi yolların>`, asla `git add -A`).
- **İşçiler:** Başlarken: `git pull` → `tasks/PCx.md` oku → yap → `status/PCx.md` güncelle → commit + push.
- Ekip: PC1 keremsumer2010-tech · PC2 memir-erdogmus (veri, Antigravity/Gemini ile) · PC3 M3hmeT1888 (çökme analizi) · PC4 acikgozibrahim032-hub (UK görselleri, obruklar, kaynaklar; Antigravity/Gemini ile) · PC5 M3hmeT1888 bilgisayarında Antigravity (oyun + sunum metni) · PC6 M3hmeT1888 bilgisayarında 2. Antigravity (GNSS doğrulama + altyapı verisi).
- Sadece KENDİ klasöründe yaz (tasks dosyasında veya sahiplendiğin QUEUE işinde yazar). Başkasının klasörüne dokunma.
- Görevde belirsizlik varsa tahmin etme: `status/PCx.md` içine "BLOCKED: ..." yaz, push et, başka bir işe geç.

## ⚡ HİÇ BOŞ KALMA PROTOKOLÜ (herkes, her zaman)
Hedef: teslime kadar hiçbir ajan boşta durmaz. Bir görev bitince SORMADAN sıradakine geç:
1. Kendi `tasks/PCx.md` dosyandaki bitmemiş bir sonraki görev.
2. Yoksa `tasks/QUEUE.md`'den en üstteki sahiplenilmemiş iş (kurallar dosyanın başında; sahiplen → hemen push).
3. Kuyruk boşsa: kendi çıktılarını test et/iyileştir, başkalarının çıktısını kontrol et (`docs/qa_report.md`'ye not yaz,
   onların dosyasına dokunma), dokümantasyon ve kaynak doğrulama.
- Her iş bitince: status güncelle → `git pull --rebase` → commit → push → HEMEN sonraki işe başla.
- Her 30–45 dakikada bir `git pull` yap; PC1 `tasks/` altına yeni görev yazabilir.
- Verimlilik: büyük dosyayı baştan sona okuma, `grep`/özet kullan; aynı araştırmayı tekrarlama, önce `docs/` ve `status/`'a bak.
- Commit mesajı: `[PCx] kısa açıklama`. Push öncesi `git pull --rebase`.

## BUGÜNKÜ ÖNCELİK: docs/TODAY_PLAN.md (Lincoln sunumu bugün, demo 17:30 TR)

## Veri kalitesi ve kalibrasyon (ZORUNLU)
- **Kalibrasyon bizim işimiz değil.** Kalibrasyon ve doğrulamayı NISAR projesi (NASA-JPL ve ISRO) yapar. Biz ürünleri yayınlandığı hâliyle kullanırız; "kalibre ettik" ya da "düzelttik" demeyiz.
- Her katman/dosya bir `quality` etiketi taşır:
  - `provisional`: her iki tarihi 2026-06-17 ve sonrası olan PROVISIONAL ürünler (bugünkü demo SADECE bunlar).
  - `beta-precal`: 2026-06-17 öncesi tarih içeren ürünler (kalibrasyon öncesi beta dönemi; ürün notlarından aksi doğrulanana kadar).
  - `preview`: browse PNG'ler — nicel DEĞİL, sadece görsel.
- Farklı sınıflar AYNI hesapta/katmanda birleştirilmez. Beta veriyle yapılan analiz ayrı klasörde (`*_beta`, `*_fullyear`) ve `quality: "mixed"` olarak durur.
- Web'de her katmanda rozet + sabit dipnot: "NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."

## Yapay zekâ ile üretilen medya
- Higgsfield/Gemini vb. ile üretilen görsel ve videolar SADECE süs/anlatım içindir; asla veri gibi gösterilmez.
- Her birinde görünür "AI-generated illustration" etiketi. Haritalarda sadece gerçek veri. NASA logosu kullanılmaz.
- Kullanılan tüm yapay zekâ araçları teslimde açıklanır.

## Ana plan: docs/MASTER_PLAN.md

## Veri kuralları
- `.h5` ve ham dosyalar repoya GİRMEZ (.gitignore). Ham veriyi `raw/` altına koy.
- Repoya sadece küçük çıktılar: PNG, JSON, küçük GeoTIFF/NPZ (<20 MB). Kesilmiş GUNW alt kümeleri: `pipeline/subset/<site>/<t1>_<t2>.npz`.
- .h5 indirmek Earthdata girişi İSTER (test edildi: giriş olmadan "Access denied"); browse PNG'ler girişsiz iner.
- Veri kaynağı: ASF SearchAPI / `asf_search`, parametre `platform=NISAR` (dataset=NISAR ÇALIŞMIYOR).
- İndirme için Earthdata hesabı gerekebilir (her PC kendi hesabı). Kimlik bilgisi asla repoya yazılmaz.
- NISAR L-band dalga boyu ≈ 0.2384 m. LOS yer değiştirme = -λ/(4π) × unwrapped phase (işaret konvansiyonunu ürün dokümanından DOĞRULA).

## Bölgeler (lon_min, lat_min, lon_max, lat_max)
- central_valley: -120.2, 35.6, -119.0, 36.6  (GUNW path 34 ve 114, Kas 2025–Eki 2026)
- konya: 32.4, 37.4, 33.9, 38.1  (GUNW path 7/100/108/172, Eki 2025–Eki 2026)
- karapinar (obruk): 33.3, 37.6, 33.8, 37.9  (GUNW path 7 ve 172, Haz–Eki 2026)
- fens: -0.3, 52.4, 0.4, 52.9  (GCOV/SME2, Haz–Kas 2026)

## Veri sözleşmesi (web bunu okur — değiştirmek için PC1'e sor)
```
data/<site>/meta.json        {site, bbox:[w,s,e,n], dates:[YYYY-MM-DD...], units:"cm", vmin, vmax, source, notes, quality, quality_note}
data/<site>/disp/<date>.png  o tarihe kadar kümülatif LOS çökme, renkli, şeffaf arka plan, bbox'a oturur
data/<site>/points.json      [{id, name, lon, lat, dates:[...], disp_cm:[...]}]
data/<site>/assets.json      risk altındaki altyapı (GeoJSON, her segmentte risk, gradient_mm_per_km, max_cm)
data/<site>/decomp.json      {permanent_cm_per_yr, seasonal_amp_cm} raster PNG yolları + istatistik
data/<site>/drivers.json     {dates, subsidence_cm, soil_moisture, irrigation_index, lag_corr}
data/<site>/validation.json  [{station, lon, lat, rmse_cm, corr, insar:[...], gnss:[...]}]
data/catalog.json            [{site, title, layers:[...]}]
```

## Kalite
- Bilimsel her cümleye kaynak (link) ekle. Uydurma sayı yok; ölçmediğini "estimate" diye işaretle.
- "Bitti" demeden önce çalıştır ve çıktıyı kontrol et; status'a nasıl doğruladığını yaz.
