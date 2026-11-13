# aseltech — çalışma kuralları (TÜM Claude oturumları okur)

## Proje
NASA Space Apps 2026, görev "Dancing with the SARs". Konu: **Sinking Farmlands** — NISAR GUNW
interferogramlarından yeraltı suyu kaynaklı tarım arazisi çökmesini santime çevirip web uygulamasında göstermek.
Ana vaka: California Central Valley. İkinci: Konya. Ek: Fens (UK, sadece GCOV/SME2).
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
data/<site>/assets.json      risk altındaki altyapı (GeoJSON FeatureCollection) — sonra
```

## Kalite
- Bilimsel her cümleye kaynak (link) ekle. Uydurma sayı yok; ölçmediğini "estimate" diye işaretle.
- "Bitti" demeden önce çalıştır ve çıktıyı kontrol et; status'a nasıl doğruladığını yaz.
