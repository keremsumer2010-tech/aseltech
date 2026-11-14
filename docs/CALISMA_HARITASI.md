# ÇALIŞMA HARİTASI — teslime kadar (Cmt 19:45 → Paz 22:00 TR) · PC1
Bu dosya herkesin TEK sırasıdır. Her ajan kendi sütununu yukarıdan aşağı yapar; bir madde bitince SORMADAN sıradakine geçer.
Liste biterse en alttaki "ASLA BOŞ KALMA" maddelerini döngüyle yapar. PC1 kredi tasarrufu için seyrek kontrol eder; bekleme yok.
Kurallar değişmedi: REVIEW_1500 dili, kalite etiketleri (beta = mixed), uydurma yok, `git add <yol>`, her adımda commit + push.
Sabit saatler: **Paz 20:00 veri dondurma** (yeni veri/özellik yok) · **Paz 21:00 son kontrol** · **Paz 22:00 teslim**.

## PC2 — Memir · veri
1. Karapınar tam yıl zinciri (6 çift) → `data/karapinar_fullyear/` (mixed).
2. Karapınar sebep verisi (SME2 + GCOV HV) → `data/karapinar/drivers.json`.
3. Delta: kalan provisional çiftler varsa tamamla, set profilini güncelle.
4. Konya Ovası ikinci path ile çapraz kontrol → `docs/qa/PC2.md`.
5. Central Valley path 114 tam yıl (beta+provisional) → `data/central_valley_p114_fullyear/` (PC9 iki geçişli tam yıl kıyası yapacak).
6. Tüm `pipeline/` scriptlerine kısa kullanım notu (README bölümü `pipeline/README.md`).

## PC3 — Mehmet · site
1. Henüz bağlı olmayan her şeyi bağla: delta, konya_plain, global_showcase, cross_sensor, exposure, polarization, uk_findings, lesson_plan, fullyear (Karapınar gelince).
2. Explorer'a yeni bölgeler (Delta, Konya Ovası, Mexico City, diğer şehirler) — `data/catalog.json`.
3. Ana sayfa "Key numbers": tam yıl sonucunu (mixed etiketiyle) ve küresel karşılaştırmayı ekle; en fazla 4 sayı kalsın.
4. Tüm sayfalarda telefon (375 px), dizüstü, projektör testi; konsol sıfır hata; yavaş bağlantıda açılış süresi.
5. Erişilebilirlik: alt metin, kontrast, klavye; SEO: başlık/açıklama/og etiketleri her sayfada.
6. `team_story.md` ekip onaylayınca Konya bölümüne.
7. Paz 20:00 sonrası sadece hata düzeltme.

## PC4 — İbrahim · metin ve sunum
1. `project_page.md`: tüm yeni sonuçlarla son hâl (tam yıl, Delta, Konya Ovası, küresel, C-band, maruziyet); challenge anahtar ifadeleri.
2. `slides.html` (≤7 slayt, teslim için video yerine kullanılabilir): her slayt tek mesaj, gerçek görsel, kaynak satırı; PDF'ye yazdırılabilir.
3. `judge_faq.md`: yeni sorular (tam yıl beta neden kullanıldı, Delta, küresel şehirler, C-band).
4. `team_story.md`: ekiple birlikte gerçek cümlelerle son hâl.
5. Tüm `docs/story/*.md` için son İngilizce okuma (REVIEW_1500) → düzeltmeleri kendi dosyalarında yap, başkalarınınkini `docs/qa/PC4.md`'ye yaz.

## PC5 — Mehmet AG-1 · bilim kontrolü
1. Yeni tüm sayıları bağımsız kontrol: Delta, Konya Ovası, küresel şehirler, cross_sensor, exposure, tam yıl → `docs/qa/PC5.md`.
2. `key_findings_public.md` ve `key_findings.md` güncelle (yeni sonuçlar, belirsizlik).
3. Karapınar tam yıl gelince kalıcı/geri dönen sonucunu PC9 ile çapraz kontrol.
4. Küresel şehirler için belirsizlik haritası (`uncertainty_map.py` ile) → `data/global/<şehir>/uncertainty/`.
5. Literatür tablosuna küresel şehirler ve Delta satırları.

## PC6 — Mehmet AG-2 · oyun
1. Oyun son testi: 20 strateji otomatik, sonuçlar ve hatalar → `docs/qa/PC6.md`, hataları düzelt.
2. Sınıf modu kontrolü; ders planı (`lesson_plan.md`) ile uyum.
3. Oyunu telefonda ve projektörde test; dokunmatik hedefler ≥ 44 px.
4. Oyunda "Sources" sekmesi: StoryMap, white papers, game_model kaynakları güncel mi.
5. Demo videosu DURDURULDU — dokunma.

## PC7 — Kerem · Codex · kalite
1. Yeni sayfa ve dosyalar için çevrimdışı QA: linkler, veri sözleşmesi, metin kuralları → `docs/qa/PC7.md`.
2. Fens: `crops.json` için mevsimsel yorum metni (hasat/sürüm) → `docs/story/polarization.md` ek bölüm (sadece kendi dosyan).
3. `data/` altındaki tüm JSON'lar için şema doğrulama scriptini her 2 saatte yeniden çalıştır, sonuçları ekle.
4. Paz 18:00 son QA turu.

## PC8 — Mehmet AG-3 · teslim
1. `submission_form.md`: yeni sonuçlarla, karakter sınırlarıyla son hâl; her sayı kaynağıyla.
2. Video yerine slayt kullanılırsa teslim için gereken metin/altyazı uyarlaması (`docs/story/slides_notes.md`).
3. Maruziyet (`exposure.md`) için Karapınar ve Konya Ovası ekle.
4. Teslim kontrol listesi (`docs/MASTER_PLAN.md` §9) maddelerini tek tek doğrula → `docs/qa/PC8.md`.

## PC9 — Mehmet 2. bilgisayar · tam yıl
1. Karapınar tam yıl gelince kalıcı/geri dönen ayrımı → `data/karapinar_fullyear/decomp.json` + `fullyear.md` Türkiye bölümü.
2. Central Valley path 114 tam yılı (PC2 hazırlarsa) ile path 34 tam yılını karşılaştır → iki geçişli tam yıl doğrulaması.
3. Tam yıl sonucunu GPS istasyonlarıyla karşılaştır (11 ay) → `docs/qa/PC9.md`.
4. Kalıcı çökme haritası için alan istatistiği (km², yılda > 5 / > 10 cm).

## PC10 — Memir AG-2 · küresel
1. 4. şehir (NISAR kapsaması olan, yayımlanmış çökme bölgesi; ör. Beijing, Bangkok, Hanoi, Taipei — önce ASF'de kontrol).
2. Küresel şehirler için GPS veya yayımlanmış ölçümle kıyas notu.
3. `global_showcase.md` son okuma, PC3'e site için kısa metin.
4. Mexico City için kalıcı/geri dönen ayrımı (tam yıl veri varsa).

## ASLA BOŞ KALMA (liste biten herkes, döngüyle)
a) `git pull`; `docs/qa/*.md` dosyalarında KENDİ dosyaların hakkındaki her bulguyu düzelt.
b) Kendi çıktılarını yeniden çalıştır, test et, sayıları veri dosyalarıyla karşılaştır.
c) Kendi alanındaki metinleri REVIEW_1500 kurallarına göre sadeleştir.
d) Başkasının çıktısında hata görürsen kendi `docs/qa/PCx.md` dosyana yaz (dosyasına dokunma).
e) **HATA AYIKLAMA (boşta kalan herkes):** repo genelinde `python -m pytest -q` (analysis, analysis/decomp, analysis/pc5…), sitede yerel test (`python -m http.server 8765` → /web/, tüm sayfalar, konsol hataları), oyunda strateji testleri, `data/*` JSON'larında şema/NaN/boş değer kontrolü, kırık link taraması. Kendi dosyandaki hatayı düzelt; başkasınınkini `docs/qa/PCx.md`'ye "dosya → hata → nasıl tekrar edilir" biçiminde yaz.
f) status dosyana o an ne yaptığını yaz; "görev bekleniyor" deme.
