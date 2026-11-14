# PC5 — Oyun + sunum metni

## Kimlik
M3hmeT1888 · Antigravity (Gemini) · klasör `aseltech-gemini`

## Yazma alanı
`game/`, `docs/story/pitch.md`, `docs/game_v1.png`, `status/PC5.md`

## En kritik iş
16:00 TR'ye kadar oynanabilir `game/index.html`.

## Görevler
1. **(12:00–16:00) Aquifer Manager** — `game/index.html`, saf HTML/CSS/JS (CDN kullanırsan sabit sürüm), İngilizce.
   - 10 yıl; her yıl pompalama %0–150 seçilir; yıl tipi rastgele: wet / normal / drought.
   - Model tek `CONFIG` nesnesinde: `subsidence_cm = base_rate_cm_per_yr * (pumping/100) * year_factor`;
     `base_rate_cm_per_yr = 10` → ekranda "placeholder — will be replaced by our NISAR measurement".
   - Yan kesit görsel: yüzey, tarlalar, kanal, yol, altında akifer. Çökme arttıkça yüzey iner, kanal eğilir, çatlaklar çıkar.
   - Sonuç ekranı: toplam çökme, basit çiftçi geliri, "what this means" cümlesi, tekrar oyna.
   - Alt bilgi: "Rates are illustrative until replaced with NISAR-derived values. NISAR data are provisional; calibration is done by the NISAR project (NASA-JPL/ISRO), not by our team."
   - Mobil uyumlu, konsol temiz; ekran görüntüsü `docs/game_v1.png`.
2. **(16:00–17:30) Sunum metni** — `docs/story/pitch.md`: 30 sn video senaryosu (sahne sahne, İngilizce altyazı) + en fazla 7 slayt metni,
   `docs/MASTER_PLAN.md` §3 ve §7'ye göre. Sayı yazma → `{CV_MAX_CM}`, `{HOLME_FEN_DROP_M}` gibi yer tutucu.
3. **(17:30 sonrası)** QUEUE Q13/Q15.

## Bitti sayılır eğer
Oyun baştan sona oynanıyor, 10. yılda sonuç ekranı çıkıyor · CONFIG tek yerde · konsolda hata yok · telefonda düzgün · pitch.md'de sayı yok, yer tutucu var.

## B planı
Kesit animasyonu yetişmezse: basit çubuk/grafik görünümüyle oyunu bitir, animasyonu sonra ekle.

## Yapma listesi
Gerçek veri gibi görünen sayı uydurma · yapay zekâ görselini etiketsiz koyma · `web/`'e yazma.

## Rapor (`status/PC5.md`)
Ne bitti, nasıl test edildi (tarayıcı, telefon), bilinen eksikler.
