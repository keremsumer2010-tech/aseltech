# ORTAK İŞ HAVUZU (PC1, Paz 04:25) — listesi biten herkes buradan alır
Kullanıcı artık ajanlara prompt girmiyor; **tüm yönetim git üzerinden.** Kendi `tasks/PCx.md` planın bittiyse buradan bir satır al:
- Satırı `- [ ]` → `- [~PCx]` yap, **hemen commit + push** (başkası almasın), işi yap, bitince `- [x PCx]` + çıktının yolu.
- Aynı anda en fazla 1 satır. Kendi uzmanlığına uyan satırı seç. Satır başkasınınsa dokunma.
- Yeni iş fikrin varsa (kaynaklı, atlasa hizmet eden) en alta `- [ ]` olarak ekle.

## E. Durmuş ajanlardan devir (otomatik kontrol 2) — önce bunlar
- [~PC11] Cakarta tam kutu yeniden hesap (PC11 6/9'da kaldı; `pipeline/subset/global_jakarta` varsa `--resume`)
- [~PC11] Bulacan / Manila Körfezi (120.90, 14.85)
- [x PC4] Tek literatür tablosu: `data/global/literature_rates.json` + `docs/story/literature_atlas.md` (tüm 29 atlas bölgesi, DOI)
- [~PC4] Oyun ↔ atlas bağlantısı (`tasks/PC6.md` "OYUN ↔ ATLAS" 1–5)
- [~PC4] Sunum modu `web/present.html` (Lincoln demosu, ok tuşlarıyla bölüm turu)
- [~PC4] "What changed" kutusu + sıralamada hata çubukları (atlas sayfası)
- [x PC4] Teslim paketi `docs/story/submission_package.md` (Space Apps gerekleri, AI beyanı, NASA veri listesi, tüm linkler 200)
- [x PC4] Jüri SSS 30 soru (`docs/story/judge_faq.md`) — yeni sıralama, QC, OPERA, ortak pencere

- [x PC2] NISAR Pulse `--qc` motoru (`pipeline/nisarpulse/qc.py` + `tests/test_qc.py`, `15/15` test OK)
- [~PC11] Celaya, Meksika (−100.81, 20.52) — PC2'den devir
- [ ] Hamadan–Kabudarahang, İran (48.72, 35.21) — PC2'den devir
- [ ] Site son QA: canlı sitede her sayfa konsol 0 hata, kırık link 0 (PC2'den devir)

- [x PC6] results_registry boş summary/key_number alanları (PC10'dan devir) → data/results_registry.json (29/29 tam)
- [x PC6] Ortak ±10 cm ölçekli küçük haritalar `data/global/<id>/thumb.png` (PC10'dan devir) → 29 bölge (400x400 ±10 cm LOS RdBu) + meta.json thumb_scale + docs/story/media/pc10_colorbar.png
- [x PC6] İkinci sıralama ekseni: ortak pencerede < −5 cm alan km² (PC10'dan devir) → data/global/atlas.json (area_km2_lt_minus5cm_common) + web/atlas.html & web/atlas.js (Fastest Rate / Largest Area sıralama anahtarı + Top 5 + detay + tablolar)
- [~PC4] `data/global/atlas.schema.json` + `tests/test_atlas_schema.py` (PC10'dan devir)

- [ ] Pekin: 11 Temmuz 2026 görüntüsünü içeren iki çifti çıkarıp yeniden hesapla (PC7'den devir; kesitler PC7 klasöründe `pipeline/subset/global_beijing/`)
- [ ] Aguascalientes tamamla (8/9 kesit, PC7 klasörü) — PC7'den devir
- [ ] Querétaro tamamla (kesitler PC7 klasörü) — PC7'den devir
- [ ] Küresel altyapı riski Mexico City + Pekin + `global_risk.md` — PC7'den devir

- [ ] Mexico City tam yıl: 24/26 parça hazır (PC9 klasöründe `pipeline/subset/`), decomp çalıştır, eksik 2 parçayı notla (PC9'dan devir)
- [ ] `docs/story/annualization.md` + `pc9_annualization.png`: Central Valley (veri hazır) + Mexico City; Konya için Şub–Haz 2026 arşiv boşluğu notu (PC9'dan devir)

## A. Atlas verisi (Earthdata erişimi olanlar: PC2, PC7, PC9, PC10, PC11)
- [ ] Toluca, Meksika (−99.65, 19.29) — önce kapsama + literatür
- [ ] San Luis Potosí, Meksika (−100.98, 22.15)
- [ ] Neyshabur, İran (58.80, 36.21)
- [~PC11] Ho Chi Minh City tam kutu yeniden hesap (eski seri ±8 cm salınımlı) + QC
- [ ] Kolkata, Hindistan (88.36, 22.57) — tropik, QC dikkat
- [ ] Ankara–Konya arası diğer Türkiye havzası adayı: literatürde InSAR çökmesi yayımlanmış bir havza bul (kaynakla), sonra işle
- [ ] Atlas bölgelerinden QC işaretlilerin (`data/global/qc_flags.json`) `--qc` ile yeniden işlenmesi (sahibine haber vererek)

- [x PC7] Pekin tam kutu yeniden hesap → `data/global/beijing/` (11 Temmuz aykırısı kaldı)

## B. Bilim ve doğrulama (PC4, PC5, PC11, boşta kalan herkes)
- [x PC4] Her güvenilir bölge (16/16) için kaynaklı "neden çöküyor" paragrafı → `docs/story/atlas_cities/*.md` (tümü `<= 150` kelime, DOI/kaynaklı)
- [ ] `docs/story/detectability.md`'yi 21+ bölgeye güncelle (yeni bölgelerin σ haritaları geldikçe)
- [x PC4] Ortak 93 günlük pencere sıralamasının eski sıralamayla kıyası (hangi bölge yer değiştirdi, neden) → `docs/qa/PC4.md` §32
- [x PC4] `atlas_top5_check.md` yöntemini 6–15. sıralara uygula (literatür kıyası tablosu → `docs/qa/PC4.md` §33)

## C. Site ve sunum (PC6, PC8, PC4)
- [x PC4] Her sayfanın `<title>`/`<meta description>`/`og:image`'ı güncel 29-bölge atlas sonuçlarıyla (`web/*.html`)
- [x PC4] Atlas sayfasına "How to read this map" 4 adımlık kısa rehber (`web/atlas.html`)
- [~PC4] Ana sayfadaki her sayının atlas.json / results_registry ile aynı olduğunu otomatik kontrol eden test (`tests/test_site_numbers.py`)
- [x PC4] Sunum için 60 sn'lik yedek ekran kaydı senaryosu (gerçek siteden, AI görseli yok) — `docs/story/demo_script_v3.md`

## D. Kalite (herkes)
- [ ] `python -m pytest -q` tüm repo — kırılan testin sahibine `docs/qa/PCx.md`'de bildir
- [ ] `pipeline/pc7/validate_json.py` ve `tools/validate_atlas.py` — bulguları sahiplerine
- [x PC4] Tüm `docs/story/*.md` içinde kırık bağlantı taraması (0 kırık yerel bağlantı)

## PC1 KARAR — Querétaro atlasa GİRMİYOR (Paz)
`data/global/queretaro/validation_note.json`: −22.9 cm / 120 gün, literatürün (INEGI ~1.5 cm/yıl) çok üstünde, %48.6 piksel tek tarih sapması, referans bağımsız doğrulanmadı → `recommended_confidence: low`, "diagnostic". Dondurmaya 4 saat kala atlas 29 bölge kalır; Querétaro sadece teknik notta "denendi, QC geçmedi" örneği olarak anılabilir. build_atlas onu almıyorsa bu doğru davranış — DEĞİŞTİRME.

- [ ] `tests/test_atlas_schema.py`: atlas.json alan/sıra/sayım testi (PC10 durdu, PC1 12:55)
