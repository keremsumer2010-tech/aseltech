# PC8 — Mehmet'in 3. Antigravity'si · UK KİL ANALİZİ (15:25; test başarılı)

## Kimlik
M3hmeT1888 · Antigravity · klasör `aseltech-gemini3` · commit öneki `[PC8]` · İNDİRME YAPMA.

## Yazma alanı
`data/uk_clay/` · `analysis/pc8/` · `docs/qa/PC8.md` · `status/PC8.md` · QUEUE'da sadece Q09 satırı (analiz kısmı).
`analysis/` içindeki PC3 kodlarını import edebilir/çalıştırabilirsin, DEĞİŞTİRME.

## Görevler (sırayla; bitince sormadan sıradakine)
1. **Q09 UK kil (Londra) kümülatif harita** — PC2 9 provisional çifti hazırladı: `pipeline/subset/` altındaki UK/London klasörü (`ls pipeline/subset/` ile bul; adı ve bbox'ı `status/PC2.md`'de).
   - PC3'ün hattını ÇALIŞTIR: `python analysis/cumulative.py <site_adı> --data-dir data/uk_clay` (parametreleri `analysis/cumulative.py --help` ile kontrol et; site tanımı yoksa kendi küçük sarmalayıcını `analysis/pc8/` altında yaz, PC3 dosyasını değiştirme).
   - Çıktı (veri sözleşmesi biçimi): `data/uk_clay/meta.json`, `disp/<date>.png`, `points.json`, `summary.json` (`quality: provisional`).
2. **Dürüst sonuç** → `data/uk_clay/summary.json` `method_note` + `docs/qa/PC8.md`: sinyal (kil büzülmesi, beklenen mm–1–2 cm) PC5'in piksel belirsizliğinden (~0.3 cm) ve atmosfer gürültüsünden (1–3 cm/çift) ayrılabiliyor mu? Ayrılamıyorsa açıkça **"below detection limit for one season"** yaz — bu da geçerli bir bulgu. 3 cümle İngilizce, sayılarla.
3. **Fens (Holme Fen çevresi) için aynısı** — `pipeline/subset/` altında Fens GUNW varsa; yoksa bu adımı atla ve status'a yaz.
4. **Sürekli:** her 30 dk `git pull`; PC2'nin yeni UK alt kümeleri gelirse yeniden çalıştır; `docs/qa/*.md` içinde uk_clay hakkındaki bulguları düzelt. Bitince QUEUE'da atanmamış iş veya PC1'e status'ta "boştayım" yaz — ama önce kendi çıktını test et ve iyileştir.

Kurallar: `git add data/uk_clay/ analysis/pc8/ docs/qa/PC8.md status/PC8.md`; `git add -A` yasak; git hatasında silme yok, BLOCKED yaz.
