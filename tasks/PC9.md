# PC9 — SİTE SAHİBİ (15:35'te PC1'den devralındı) · hedef: jüri 30 saniyede anlasın, NASA kalitesi, AI görünümü sıfır

## Kimlik
M3hmeT1888 · ikinci bilgisayar · Antigravity (Gemini) · klon klasörü `aseltech-pc9` · commit öneki `[PC9]` · İndirme yapma.

## Yazma alanı (artık senin; PC1 sadece denetler)
`web/` (index.html, style.css, app.js, science.html, data.html, faq.html, docs.js, assets/, mock/) — **`web/panel.html` HARİÇ (PC1'in)** · `data/catalog.json` · `docs/qa/PC9.md` · `status/PC9.md`
Yayın: `main`'e push → GitHub Actions 1–2 dk'da https://keremsumer2010-tech.github.io/aseltech/ adresine yayınlar. Yerel test: repo kökünde `python -m http.server 8765` → http://localhost:8765/web/
Veriyi okuyorsun, değiştirmiyorsun: `data/*` (PC3, PC4, PC6, PC2), `docs/story/*` (PC4, PC5, PCQ), `game/` (PC6).

## Önce oku
`docs/REVIEW_1500.md` (yazım kuralları) · `docs/qa/PC4.md` (PC4'ün metin önerileri — uygula) · `docs/qa/PC7.md`, `docs/qa/PCQ.md`, `docs/qa/PC5.md` (site bulguları — düzelt) · mevcut `web/` kodu.

## Sorunlar ve yapılacaklar (sırayla; her madde ayrı commit + push)
1. **"Bu ne?" sorusu ilk ekranda cevaplanmıyor.** Hero'yu sadeleştir: başlık + TEK cümle alt başlık ("NASA-ISRO's NISAR satellite measured farmland in California sinking up to 7.8 cm in 108 days. We checked it against GPS and mapped what is at risk.") + hemen altında 3 kutulu şerit: **Measure** (NISAR radar → cm haritası) · **Check** (10 GPS istasyonu, 2 bağımsız uydu geçişi) · **Explain** (risk altındaki kanallar, obruklar, simülatör). Kutularda basit SVG ikon (emoji yok).
2. **Jargon ana sayfadan çıkacak.** "line of sight / LOS / GUNW / coherence / track / interferogram" ana sayfada geçmesin; yerine "movement measured by the satellite", "radar image pairs" vb. Teknik terimler sadece Science sayfasında. Grafik etiketleri de sade.
3. **Anahtar sayılar şeridi bağlamsız.** Her sayının altına "neye göre" ekle (ör. "−7.8 cm · largest sinking in 108 days (Jun–Oct 2026)"). 6 yerine 4 sayı yeter: en büyük çökme, etkilenen alan (PC5 `data/central_valley/area_stats.json` gelince), GPS uyumu, yüksek riskli segment.
4. **"Ne bulduk" bölümü ekle** (hikâyeden önce): PC5'in `docs/story/key_findings_public.md` dosyasındaki 8 sade maddeyi kart olarak göster (dosyadan otomatik oku; dosya yoksa bölüm gizli).
5. **Hikâye bölümleri:** pasif kartlar soluk (opacity) görünmesin, hepsi okunur olsun; her bölümün başına tek cümlelik "Key point" kutusu; harita uçuşları projektörde (1366×768) ve telefonda test edilsin.
6. **Simülatör bölümü AI gibi duruyor ve anlaşılmıyor.** Bölümü yeniden yaz: solda "What you decide / What happens / What you learn" (3 madde, sade), sağda büyük, net bir ekran görüntüsü (`docs/game_v3.png` veya güncel) + "Play" düğmesi; iframe sadece düğmeye basınca açılsın (sayfa hızlanır). PC6 oyunu geliştiriyor; sen sadece sitedeki sunumunu yap.
7. **Konya bölümü güçlensin:** PC6/PC5'in obruk halka sonucunu (obruklara 0–2 km mesafede ~3.4 cm daha fazla çökme; `data/karapinar/assets.json` / `docs/story/sinkhole_stats.md`) sade cümleyle ve küçük bir grafikle ekle.
8. **AI izlerini temizle:** `web/assets/*_ai.jpg` dosyaları hiçbir sayfada kullanılmıyorsa sil; "AI-generated" etiketi gerektiren hiçbir görsel kalmasın. Metinlerde abartı/klişe yok (REVIEW_1500).
9. **Science sayfası:** en üste 5 maddelik sade özet; uzun Markdown bölümleri katlanabilir (`<details>`) olsun.
10. **Erişilebilirlik ve kalite:** tüm görsellerde alt metin, kontrast, klavye ile gezinme, konsol hatası sıfır, Lighthouse benzeri kontrol (performans: büyük dosyalar lazy). Telefon (375 px), dizüstü, projektör.
11. **Sürekli:** her 30 dk `git pull`; `docs/qa/*.md` dosyalarında site hakkındaki her yeni bulguyu düzelt; yeni veri dosyaları (tam yıl, Fens, area_stats) geldiğinde siteye bağla.

## Bitti sayılır eğer
Jüri testi: siteyi hiç bilmeyen biri ilk ekranda "ne ölçüldü, nerede, ne kadar, nasıl doğrulandı" sorularını 30 saniyede cevaplayabiliyor. Konsol temiz, telefonda düzgün, her sayı veri dosyasından.

## Yapma listesi
`web/panel.html`'e dokunma · veri dosyalarını değiştirme · sayı uydurma · AI görseli · `git add -A`.

## Rapor (`status/PC9.md`)
Her madde sonrası: ne değişti, nasıl test edildi (ekran görüntüsü yolu `docs/site_v3.png`).
