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
- **PC2–PC5 = işçi.** Başlarken: `git pull` → `tasks/PCx.md` oku → yap → `status/PCx.md` güncelle → commit + push.
- Sadece KENDİ klasöründe yaz (tasks dosyasında yazar). Başkasının klasörüne dokunma.
- Görevde belirsizlik varsa tahmin etme: `status/PCx.md` içine "BLOCKED: ..." yaz, push et, dur.
- Commit mesajı: `[PCx] kısa açıklama`. Push öncesi `git pull --rebase`.

## Veri kuralları
- `.h5` ve ham dosyalar repoya GİRMEZ (.gitignore). Ham veriyi `raw/` altına koy.
- Repoya sadece küçük çıktılar: PNG, JSON, küçük GeoTIFF (<20 MB).
- Veri kaynağı: ASF SearchAPI / `asf_search`, parametre `platform=NISAR` (dataset=NISAR ÇALIŞMIYOR).
- İndirme için Earthdata hesabı gerekebilir (her PC kendi hesabı). Kimlik bilgisi asla repoya yazılmaz.
- NISAR L-band dalga boyu ≈ 0.2384 m. LOS yer değiştirme = -λ/(4π) × unwrapped phase (işaret konvansiyonunu ürün dokümanından DOĞRULA).

## Bölgeler (lon_min, lat_min, lon_max, lat_max)
- central_valley: -120.2, 35.6, -119.0, 36.6  (GUNW path 34 ve 114, Kas 2025–Eki 2026)
- konya: 32.3, 37.5, 33.2, 38.1  (GUNW path 7/100/108/172, Eki 2025–Eki 2026)
- fens: -0.3, 52.4, 0.4, 52.9  (GCOV/SME2, Haz–Kas 2026)

## Veri sözleşmesi (web bunu okur — değiştirmek için PC1'e sor)
```
data/<site>/meta.json        {site, bbox:[w,s,e,n], dates:[YYYY-MM-DD...], units:"cm", vmin, vmax, source, notes}
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
