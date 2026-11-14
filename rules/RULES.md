# RULES — tüm ajanlar için bağlayıcı kurallar (K-1 … K-14)

## K-1 Okuma ve yeniden okuma
- Başlarken okuma sırası: `CLAUDE.md` → `rules/RULES.md` → `rules/VERI_SOZLESMESI.md` → `docs/GOREV_DAGILIMI.md` → `tasks/PCx.md`.
- Gerektiğinde: `docs/URUN_TANIMI.md`, `docs/DEPO_HARITASI.md`, `docs/SOZLUK.md`, `docs/MASTER_PLAN.md`, `tasks/QUEUE.md`.
- **Her `git pull` sonrası** şunu çalıştır: `git diff --stat HEAD@{1} HEAD -- rules tasks docs CLAUDE.md`
  Değişen dosya varsa SADECE onu yeniden oku. Değişmeyeni tekrar okuma (token israfı).
- Her iş başlamadan önce kendi `tasks/PCx.md` dosyanı yeniden oku (kısa, ucuz).

## K-2 Yazma alanı ve sahiplik
- Sadece `tasks/PCx.md` içindeki "Yazma alanı"na veya sahiplendiğin QUEUE işinin klasörüne yaz.
- Başkasının dosyasını DEĞİŞTİRME. Hata görürsen `docs/qa_report.md`'ye not yaz (bu dosya herkese açık, sadece ekleme yap).
- Sahiplik tablosu: `docs/GOREV_DAGILIMI.md`. Formatlar: `rules/VERI_SOZLESMESI.md`.

## K-3 Git akışı
1. `git pull --rebase`
2. İşini yap, test et.
3. `git add <sadece kendi yolların>`
4. `git commit -m "[PCx] kısa açıklama"`
5. `git pull --rebase` → `git push`
- Küçük ve sık commit at (en az her tamamlanan alt adımda). Başkası senin çıktını bekliyorsa İLK çıktıyı hemen push et.

## K-4 Yasak komutlar
`git add -A` / `git add .` · `git push --force` · `git reset --hard` · `git rebase -i` · `git checkout -- <başkasının dosyası>` ·
`git clean -fd` · `rm -rf` (sadece kendi `raw/` alt klasörün hariç) · `.h5`, `.netrc`, şifre, token commit etmek ·
başka branch açıp main dışında çalışmak · `tasks/`, `rules/`, `CLAUDE.md` dosyalarını değiştirmek (sadece PC1; QUEUE.md sahiplenme satırı hariç).

## K-5 Çakışmada ne yapılır
- `git pull --rebase` çakışırsa ve çakışan dosya SENİN dosyan değilse: `git rebase --abort`, status'a `BLOCKED: conflict <dosya>` yaz, PC1'e bırak, başka iş al.
- `tasks/QUEUE.md` çakışması: uzaktaki hâli al (`git rebase --abort` → `git pull` → satırı tekrar kontrol et); iş başkasınınsa bir sonrakini sahiplen.
- Kendi dosyanda çakışma: iki tarafı birleştir, test et, devam et.

## K-6 "Bitti" tanımı
Bir iş ancak şunların HEPSİ doğruysa bitmiştir:
1. Kod çalıştı, hata yok; test varsa geçti.
2. Çıktı `rules/VERI_SOZLESMESI.md` formatında ve doğru yolda.
3. Çıktıya en az bir kez gözle baktın (PNG açıldı, JSON geçerli, değerler makul aralıkta).
4. `status/PCx.md` güncellendi: ne yapıldı, nasıl doğrulandı, sınırlamalar.
5. Push edildi.

## K-7 Hiç boş kalma
Bir iş bitince SORMADAN: (1) `tasks/PCx.md`'deki sonraki görev → (2) `tasks/QUEUE.md`'den en üstteki boş iş (sahiplen → hemen push) →
(3) kendi çıktını test et/iyileştir, başkalarını kontrol et (`docs/qa_report.md`), kaynak doğrula. Her 30–45 dk `git pull`.
Engellenirsen: `BLOCKED` yaz, push et, engelden bağımsız başka işe geç.

## K-8 Veri kalitesi ve kalibrasyon
- Kalibrasyon ve doğrulama NISAR projesinin (NASA-JPL, ISRO) işidir. Biz ürünleri yayınlandığı hâliyle kullanırız; "kalibre ettik/düzelttik" denmez.
- Kalite sınıfları (`provisional` / `beta-precal` / `preview` / `mixed`) ve kuralları: `rules/VERI_SOZLESMESI.md`. Sınıflar aynı hesapta karıştırılmaz.

## K-9 Yapay zekâ medyası
Higgsfield/Gemini vb. ile üretilen görsel/video sadece anlatım içindir, veri gibi gösterilmez; görünür "AI-generated illustration" etiketi zorunlu. NASA logosu yok.

## K-10 Uydurma yok
Sayı, koordinat, istasyon, link, alıntı uydurma. Her bilimsel cümleye kaynak. Ölçmediğin değer "illustrative/estimate" diye işaretlenir.
Doğrulayamadığını status'a "doğrulanmadı" diye yaz.

## K-11 Disk kuralları
- Ham veri sadece `raw/` (git dışı). `.h5` kesildikten sonra SİL. Diskte en az 10 GB boş yer bırak.
- Bir bilgisayarda aynı anda tek büyük indirme. Repoya giren dosya < 20 MB.

## K-12 Kimlik bilgisi
Ajan şifre/token istemez, görmez, yazdırmaz. Earthdata şifresini insan `~/.netrc` dosyasına kendisi yazar. `.netrc` asla repoya girmez.

## K-13 Dil
Sitede, verilerde, sunumda görünen her metin İNGİLİZCE. `status/` ve iç notlar Türkçe olabilir.

## K-14 Hata kaydı
Bilinen hatalar aşağıda (E-NN). Yeni bir hatayı çözersen `status/PCx.md`'ye "E-YENİ: belirti → çözüm" yaz; PC1 buraya taşır.
| Kod | Belirti | Çözüm |
|---|---|---|
| E-01 | ASF araması `dataset=NISAR` ile boş/502 | `platform=NISAR` kullan |
| E-02 | `.h5` indirirken "HTTP Basic: Access denied" | Earthdata hesabı + `~/.netrc` (insan yazar) |
| E-03 | git commit: "Author identity unknown" | Repo içinde `git config user.name/user.email` (GitHub noreply e-postası) |
| E-04 | ASF sonucunda `bytes` alanı sözlük | Boyut = iç `bytes` değerlerinin toplamı |
| E-05 | Browse PNG'yi veri gibi kullanma isteği | Browse = `preview`, nicel değil; rozetle göster |
| E-06 | Windows Git Bash'te heredoc/tırnak içinde backtick hatası | Dosyayı editör/Write aracıyla yaz, komut satırında backtick kullanma |
| E-07 | spaceappschallenge.org sayfaları boş geliyor | Sayfa JS ile yükleniyor; tarayıcıda 5–10 sn bekleyip oku |
