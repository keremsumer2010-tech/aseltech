# ÖZGÜN KATKILAR 2.0 — NASA mühendislerinin ciddiye alacağı üç çıktı (PC1, Cmt 20:10)
Hedef: "güzel bir harita" değil, **bir su yöneticisinin ve bir mühendisin yarın kullanabileceği sayılar ve bir araç.** Hepsi bizim verimizden, standart yöntemlerle, belirsizliğiyle.

## O1 — Kalıcı akifer depolama kaybı (km³/yıl) · sahibi PC8
**Soru:** "Bu bir yılda yeraltındaki su deposunun ne kadarı kalıcı olarak kayboldu?"
**Neden özgün ve değerli:** USGS, kalıcı (inelastik) kil sıkışmasının hacminin, akiferin kalıcı depolama kaybına yaklaşık eşit olduğunu kullanır (Galloway et al., USGS Circular 1182; Poland 1984 UNESCO). California'nın SGMA yasası çökmeyi "istenmeyen sonuç" olarak izletiyor. Bizim tam yıl ayrıştırmamız (PC9, `data/central_valley_fullyear/decomp.json`) kalıcı hızı piksel piksel veriyor → hacme çevirmek doğrudan bir yönetim sayısı.
**Yöntem:** V_kayıp = Σ (kalıcı çökme hızı_dikey × piksel alanı), sadece güvenilir pikseller; LOS→dikey (cos θ); belirsizlik = standart hata yayılımı + referans duyarlılığı aralığı; sonucu "estimate" ve `quality: mixed` etiketiyle ver. Karşılaştırma: aynı birimde yayımlanmış San Joaquin/Tulare depolama kaybı tahminleri (kaynaklı).
**Çıktı:** `data/central_valley_fullyear/storage_loss.json`, `docs/story/storage_loss.md`, `docs/story/media/pc8_storage_loss.png`. Karapınar tam yıl gelince aynısı.

## O2 — Mühendislik standardıyla, belirsizliği hesaba katan altyapı riski · sahibi PC7
**Soru:** "Hangi kanal ve yol segmenti, mühendislerin kullandığı hasar ölçütünü aşıyor — ve bundan ne kadar eminiz?"
**Neden özgün:** mevcut indeks gradyan eşiğiyle çalışıyor. Mühendisler **açısal distorsiyon** β = Δ(çökme)/mesafe kullanır (Boscardin & Cording 1989; Skempton & MacDonald 1956: ~1/300–1/500 hasar sınırları) ve kanallar için **serbest yükseklik (freeboard) kaybı** önemlidir (California Aqueduct/Friant-Kern kapasite kaybı DWR/USBR raporlarında). Ölçüm belirsizliğini (PC5 σ haritası) Monte Carlo ile yayarak **"eşiği aşma olasılığı"** vermek InSAR risk ürünlerinde nadir ve değerli.
**Yöntem:** her segment için 1 km örnekleme; β ve kanallarda segment boyunca maks diferansiyel çökme (cm); σ_piksel ile 1000 Monte Carlo → P(β > eşik), P(Δ > 10 cm). Eşikler kaynaklı ve parametre. Kısa doğrulama: California Aqueduct kilometreleri için yayımlanmış çökme/kapasite bilgisiyle niteliksel kıyas.
**Çıktı:** `risk/probabilistic_risk.py`, `data/central_valley/assets_prob.json` (her segment: beta, p_exceed, ci), `docs/story/engineering_risk.md`, `docs/story/media/pc7_risk_prob.png`. (İndirme yok.)

## O3 — "NISAR Vision" komut satırı aracı: herhangi bir bölge için tek komut · sahibi PC2
**Soru:** "Başka bir mühendis bunu kendi bölgesi için yarın çalıştırabilir mi?"
**Neden özgün:** hackathon projelerinin çoğu bir kerelik notebook. Bizim hattımız (arama → indirme → kesme → faz→cm → kümülatif → kalite etiketli veri sözleşmesi → site kataloğu) 7 bölge + 4 şehirde zaten çalıştı. Bunu tek, test edilmiş, belgeli bir araca çevirmek = "operasyonel" ürün.
**Yöntem:** `python -m nisarpulse run --name <ad> --bbox w,s,e,n --start YYYY-MM-DD --end YYYY-MM-DD [--track N] [--quality provisional]` → `data/<ad>/` sözleşme dosyaları + `data/catalog.json` güncellemesi. Mevcut PC2/PC3 kodlarını sarmalar (değiştirmez). `--dry-run` (sadece arama ve plan), `--resume`. Ağ gerektirmeyen birim testleri + GitHub Actions'ta test çalıştırma.
**Çıktı:** `nisarpulse/` paketi (veya `pipeline/nisarpulse/`), `nisarpulse/README.md` (5 dakikada başla), `.github/workflows/tests.yml` (sadece testler), `docs/story/engine.md`.

## T — Teknik not (NASA teknik rapor tarzı) · sahibi PC4
4–6 sayfa, `docs/story/technical_note.md` (+ yazdırılabilir HTML/PDF): Abstract · Data · Methods · Validation (GPS, ikinci geçiş, C-band) · Uncertainty · Results (108 gün, tam yıl, kalıcı kayıp O1, risk O2, küresel) · Limitations · Original contributions (O1–O3) · References. Jüriden NASA mühendisi okuyacak belge bu.

## Site entegrasyonu (PC3)
O1, O2, O3 ve teknik not hazır oldukça: ana sayfaya "What is new in our work" (3 kart), Science'a O1/O2 bölümleri, Data'ya `nisarpulse` kurulumu, teknik not indirme bağlantısı.
