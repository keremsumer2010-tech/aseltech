# PC8 — Gemini CLI · Teslim ve sunum paketi (15:00'te açıldı)

## Kimlik
Kerem'in bilgisayarı · Gemini CLI · klon klasörü `aseltech-pc8` · commit öneki `[PC8]`
İNDİRME YAPMA (aynı bilgisayarda PC7 indiriyor). Sadece repodaki dosyalarla çalış.

## Yazma alanı (SADECE bunlar)
`docs/story/submission_form.md` · `docs/story/video_subtitles.srt` · `docs/story/narration_script.md` · `docs/story/presentation_cues.md` · `docs/story/rehearsal_checklist.md` · `docs/qa/PC8.md` · `status/PC8.md`
Okuyabilirsin, DEĞİŞTİRME: `docs/story/pitch.md`, `project_page.md`, `submission_rules.md`, `video_shotlist.md`, `judge_faq.md`, `slides.html` (PC4'ün), `data/*/summary.json`.

## En kritik iş
Görev 1: Space Apps teslim formu metinleri — Pazar 22:00 teslimini 10 dakikaya indirir.

## Görevler (sırayla; bitince sormadan sıradakine)
1. **Teslim formu** → `docs/story/submission_form.md`: `docs/story/submission_rules.md` içindeki alanlara göre (proje adı, kısa açıklama, uzun açıklama, nasıl çalışır, faydalar, kullanılan NASA verisi, diğer veri, araçlar/diller, AI kullanımı, demo linki, repo linki) her alan için kopyala-yapıştır hazır İngilizce metin. Karakter sınırı varsa uy ve karakter sayısını yaz. Sayılar SADECE `data/*/summary.json`, `validation.json`, `assets.json`'dan.
2. **30 sn video altyazısı** → `docs/story/video_subtitles.srt` (SRT biçimi, `docs/story/video_shotlist.md` sahne sürelerine göre) + `docs/story/narration_script.md` (aynı metnin seslendirme için düz hâli, ~70–80 kelime, sahne başına süre).
3. **Lincoln sunum kartları** → `docs/story/presentation_cues.md`: 3 dakikalık konuşma, 30 sn'lik bloklar hâlinde; her blokta konuşan kişi, söylenecek 1–2 cümle (İngilizce), aynı anda sitede tıklanacak yer (https://keremsumer2010-tech.github.io/aseltech/ — bölüm adları: Story bölümleri 1–6, Simulator, Science, Data, FAQ). Sonda en olası 5 jüri sorusu için tek cümlelik cevaplar (`judge_faq.md`'den kısalt).
4. **Prova ve teknik kontrol listesi** → `docs/story/rehearsal_checklist.md`: internet kesilirse yedek (indirilmiş video, ekran görüntüleri), tarayıcı sekmeleri sırası, ekran paylaşımı, ses, süre tutma, kim ne yapar.
5. **Tutarlılık kontrolü** → `docs/qa/PC8.md`: pitch.md, project_page.md, slides.html, judge_faq.md ve senin dosyalarındaki her sayıyı `data/*/summary.json` ile karşılaştır; tablo hâlinde "OK / FARKLI (dosya → değer → doğrusu)". Başkasının dosyasını düzeltme, sadece raporla.

## Bitti sayılır eğer
Dosyalar var ve geçerli (SRT zaman damgaları sıralı, karakter sınırları sağlanmış) · her sayı kaynağıyla eşleşiyor · status/PC8.md güncel · push edildi.

## Yapma listesi
İndirme yok · başka dosyaya yazma · sayı uydurma · `git add -A` / `git add .`.

## Rapor (`status/PC8.md`)
Ne bitti, kontrol sonucu, `AI: Gemini CLI → ...`.
