# PCQ — 16:10 KAPATILDI. İşleri: sunum kartları + prova listesi → PC4; teslim formu + altyazı + seslendirme → PC8.

# PCQ ek görevler (15:00)
1. Site yeniden tasarlandı (index, science, data, faq): tüm sayıları veri dosyalarıyla yeniden karşılaştır → docs/qa/PCQ.md.
2. Oyun modeli denetimi: game/model.js ve docs/story/game_model.md birimleri, kalibrasyon (−10 cm dikey / 108 gün) ve parametre kaynakları tutarlı mı → docs/qa/PCQ.md.
3. docs/REVIEW_1500.md yazım kurallarına göre tüm docs/story/*.md dosyalarında AI kokan ifadeleri listele (dosyalara dokunma).
4. Bitince 30 dk'da bir yeni commit'leri kontrol etmeye devam et.

# 15:10 PC8 kaldırıldı — işleri PCQ'ya (sırayla, 15:10 sonrası öncelik bunlar)
Yazma alanına eklendi: docs/story/submission_form.md, video_subtitles.srt, narration_script.md, presentation_cues.md, rehearsal_checklist.md, docs/qa/PCQ.md
## Görevler (sırayla; bitince sormadan sıradakine)
1. **Teslim formu** → `docs/story/submission_form.md`: `docs/story/submission_rules.md` içindeki alanlara göre (proje adı, kısa açıklama, uzun açıklama, nasıl çalışır, faydalar, kullanılan NASA verisi, diğer veri, araçlar/diller, AI kullanımı, demo linki, repo linki) her alan için kopyala-yapıştır hazır İngilizce metin. Karakter sınırı varsa uy ve karakter sayısını yaz. Sayılar SADECE `data/*/summary.json`, `validation.json`, `assets.json`'dan.
2. **30 sn video altyazısı** → `docs/story/video_subtitles.srt` (SRT biçimi, `docs/story/video_shotlist.md` sahne sürelerine göre) + `docs/story/narration_script.md` (aynı metnin seslendirme için düz hâli, ~70–80 kelime, sahne başına süre).
3. **Lincoln sunum kartları** → `docs/story/presentation_cues.md`: 3 dakikalık konuşma, 30 sn'lik bloklar hâlinde; her blokta konuşan kişi, söylenecek 1–2 cümle (İngilizce), aynı anda sitede tıklanacak yer (https://keremsumer2010-tech.github.io/aseltech/ — bölüm adları: Story bölümleri 1–6, Simulator, Science, Data, FAQ). Sonda en olası 5 jüri sorusu için tek cümlelik cevaplar (`judge_faq.md`'den kısalt).
4. **Prova ve teknik kontrol listesi** → `docs/story/rehearsal_checklist.md`: internet kesilirse yedek (indirilmiş video, ekran görüntüleri), tarayıcı sekmeleri sırası, ekran paylaşımı, ses, süre tutma, kim ne yapar.
5. **Tutarlılık kontrolü** → `docs/qa/PC8.md`: pitch.md, project_page.md, slides.html, judge_faq.md ve senin dosyalarındaki her sayıyı `data/*/summary.json` ile karşılaştır; tablo hâlinde "OK / FARKLI (dosya → değer → doğrusu)". Başkasının dosyasını düzeltme, sadece raporla.

