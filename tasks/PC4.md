# PC4 — UK görselleri, obruklar, kaynaklar

## Kimlik
acikgozibrahim032-hub · Antigravity (Gemini) · klasör `aseltech`

## Yazma alanı
`data/uk/`, `data/karapinar/sinkholes.geojson`, `docs/story/sources.md`, `docs/story/calibration_note.md`, `status/PC4.md`

## En kritik iş
13:30 TR'ye kadar `data/uk/` görsel çifti (sitenin açılış sahnesi).

## Görevler  (faz planı ve saatler: docs/GOREV_DAGILIMI.md §3b — 16:30 özellik dondurma, 17:00–17:30 QA görevin orada)
1. **(12:00–13:30) UK "bulutun altı" çifti**
   - ASF'den `fens` bbox'ı için NISAR GCOV tarihlerini listele.
   - Bu tarihlerden optikte BULUTLU bir gün seç: NASA Worldview Snapshots / GIBS (girişsiz) MODIS veya VIIRS true color; birkaç günü dene.
   - Aynı günün GCOV browse PNG'sini indir (girişsiz). İkisini aynı bbox'a hizala.
   - → `data/uk/optical_<date>.jpg`, `data/uk/radar_<date>.png`, `data/uk/meta.json` (format: `rules/VERI_SOZLESMESI.md` §4, `quality:"preview"`).
2. **(13:30–15:30) Karapınar obrukları** → `data/karapinar/sinkholes.geojson`
   Sadece kaynakta koordinatı verilen veya yeri net tanımlanmış obruklar; her noktada `name, year_formed, source_title, source_url, coord_source`. En az 5, ideal 10+. Hakemli makale/resmi kurum öncelikli.
3. **(15:30–17:00) Kaynaklar** → `docs/story/sources.md` (her linki aç): Holme Fen (dikiliş tarihi, alçalma miktarı), Central Valley çökmesi (NASA/JPL, USGS), Sacramento Delta setleri, Karapınar/Konya, BGS kil şişme-büzülme, NISAR görevi.
   `docs/story/calibration_note.md`: ASF/JPL ürün notlarına göre 2026-06-17 öncesi ürünlerin kalibrasyon durumu (kaynaklı, kısa).
4. **(17:00 sonrası)** QUEUE Q11/Q12.

## Bitti sayılır eğer
İki görsel aynı bbox'ta ve açılıyor · optik gerçekten bulutlu · meta.json geçerli · geojson geçerli (bir doğrulayıcıyla kontrol) ve her noktada kaynak var · sources.md'deki her link açıldı.

## B planı
- Aynı günde bulutlu optik + radar bulunamazsa: ±1 gün kabul et, meta'da `note`'a yaz.
- Obruk koordinatı az bulunursa: bulunanları koy, kalanları "doğrulanmadı" diye status'a yaz; tahmin etme.

## Yapma listesi
Koordinat/sayı tahmin etme · radar önizlemeyi nicel veri gibi tanımlama · yapay zekâ görseli koyma · başka klasöre yazma.

## Rapor (`status/PC4.md`)
Seçilen tarih ve neden, obruk sayısı ve kaynakları, doğrulanamayanlar.
