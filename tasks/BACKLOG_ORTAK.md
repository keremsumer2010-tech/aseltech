# ORTAK İŞ HAVUZU (PC1, Paz 04:25) — listesi biten herkes buradan alır
Kullanıcı artık ajanlara prompt girmiyor; **tüm yönetim git üzerinden.** Kendi `tasks/PCx.md` planın bittiyse buradan bir satır al:
- Satırı `- [ ]` → `- [~PCx]` yap, **hemen commit + push** (başkası almasın), işi yap, bitince `- [x PCx]` + çıktının yolu.
- Aynı anda en fazla 1 satır. Kendi uzmanlığına uyan satırı seç. Satır başkasınınsa dokunma.
- Yeni iş fikrin varsa (kaynaklı, atlasa hizmet eden) en alta `- [ ]` olarak ekle.

## A. Atlas verisi (Earthdata erişimi olanlar: PC2, PC7, PC9, PC10, PC11)
- [ ] Toluca, Meksika (−99.65, 19.29) — önce kapsama + literatür
- [ ] San Luis Potosí, Meksika (−100.98, 22.15)
- [ ] Neyshabur, İran (58.80, 36.21)
- [ ] Ho Chi Minh City tam kutu yeniden hesap (eski seri ±8 cm salınımlı) + QC
- [ ] Kolkata, Hindistan (88.36, 22.57) — tropik, QC dikkat
- [ ] Ankara–Konya arası diğer Türkiye havzası adayı: literatürde InSAR çökmesi yayımlanmış bir havza bul (kaynakla), sonra işle
- [ ] Atlas bölgelerinden QC işaretlilerin (`data/global/qc_flags.json`) `--qc` ile yeniden işlenmesi (sahibine haber vererek)

- [~PC7] Pekin tam kutu yeniden hesap (PC11'den devir, otomatik kontrol 1)

## B. Bilim ve doğrulama (PC4, PC5, PC11, boşta kalan herkes)
- [ ] Her güvenilir bölge için 1 paragraf "neden çöküyor" (yeraltı suyu / kil / tarım), kaynaklı → şehir kartlarına ek (PC4 ile koordineli)
- [ ] `docs/story/detectability.md`'yi 21+ bölgeye güncelle (yeni bölgelerin σ haritaları geldikçe)
- [ ] Ortak 93 günlük pencere sıralamasının eski sıralamayla kıyası (hangi bölge yer değiştirdi, neden) → `docs/qa/PCx.md`
- [ ] `atlas_top5_check.md` yöntemini 6–15. sıralara uygula (literatür kıyası tablosu)

## C. Site ve sunum (PC6, PC8, PC4)
- [ ] Her sayfanın `<title>`/`<meta description>`/`og:image`'ı güncel atlas sonuçlarıyla
- [ ] Atlas sayfasına "How to read this map" 4 adımlık kısa rehber (LOS, renk, güven rozeti, indicative)
- [ ] Ana sayfadaki her sayının atlas.json / results_registry ile aynı olduğunu otomatik kontrol eden test (`tests/test_site_numbers.py`)
- [ ] Sunum için 60 sn'lik yedek ekran kaydı senaryosu (gerçek siteden, AI görseli yok) — `docs/story/demo_script_v3.md`

## D. Kalite (herkes)
- [ ] `python -m pytest -q` tüm repo — kırılan testin sahibine `docs/qa/PCx.md`'de bildir
- [ ] `pipeline/pc7/validate_json.py` ve `tools/validate_atlas.py` — bulguları sahiplerine
- [ ] Tüm `docs/story/*.md` içinde kırık bağlantı taraması
