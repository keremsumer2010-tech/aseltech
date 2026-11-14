# PC5 — Matematik / analiz (13:30'da yeniden atandı: tasarım işleri QUEUE Q19/Q20'ye alındı)

> Bu dosyadaki sıra geçerlidir (`docs/ZAMAN_CIZELGESI.md`'deki eski PC5 sütunu iptal). İş bitince durma: RULES §7.1.

## Kimlik
M3hmeT1888 · Antigravity (Gemini) · klasör `aseltech-gemini`

## Yazma alanı
`analysis/decomp/` (yeni alt klasör, sadece senin) · `docs/story/uncertainty.md` · `docs/qa/PC5.md` · `status/PC5.md`
`analysis/` içindeki diğer dosyalar PC3'ündür: okuyabilir/import edebilirsin, DEĞİŞTİRME.

## En kritik iş
Pazar günkü "kalıcı vs geri dönen çökme" (özgün katkı #1) için test edilmiş ayrıştırma kodu — PC3 tam yıl verisiyle sadece çalıştıracak.

## Görevler
1. **(13:30–15:00) Ayrıştırma modülü** — `analysis/decomp/decompose.py`
   - Her piksel: `d(t) = a + v·t + A·sin(2πt) + B·cos(2πt)` (t yıl), en küçük kareler, vektörleştirilmiş (tüm pikseller tek lstsq).
   - Çıktılar: `v` (cm/yıl, kalıcı eğilim), genlik `sqrt(A²+B²)` (cm, geri dönen), faz (en düşük ay), standart hatalar, R².
   - Geçerli nokta < 8 veya süre < 9 ay → NaN + sebep kodu.
   - `analysis/decomp/test_decompose.py`: bilinen v/A/faz + gürültü → geri bulma toleransı; boşluk/NaN testleri. `python -m pytest analysis/decomp -q` geçmeli.
2. **(15:00–16:30) Belirsizlik bütçesi** — `analysis/decomp/error_budget.py` + `docs/story/uncertainty.md`
   - Zincir toplamında gürültü: σ_toplam ≈ σ_çift·√N (bağımsızlık varsayımı açıkça yazılır).
   - σ_çift: PC3'ün sabit kontrol noktalarından; yoksa `pipeline/subset/central_valley/*.npz` yüksek koherenslı sabit bölge std'si.
   - İyonosfer ekranı (npz'de `ion` varsa) p1–p99 aralığı → cm.
   - Site "How we know" için 3–4 cümle İngilizce + tablo; ölçülen sayılar yöntemiyle, tahminler "estimate".
3. **(16:30 sonrası)** `summary.json` sayılarının bağımsız kontrolü → `docs/qa/PC5.md`; sonra QUEUE'da atanmamış en üst iş.

## Bitti sayılır eğer
Testler geçiyor · docstring'ler yöntemi ve varsayımları anlatıyor · uncertainty.md'deki her sayının hesap yolu yazılı.

## B planı
PC3 verisi gelmezse belirsizliği npz'lerden hesapla, "preliminary" etiketle.

## Yapma listesi
PC3'ün dosyalarını değiştirme · sayı uydurma · beta ile provisional'ı aynı hesapta karıştırma (K-3).

## Rapor (`status/PC5.md`)
Ne bitti, test sonucu, σ değerleri ve yöntemi.
