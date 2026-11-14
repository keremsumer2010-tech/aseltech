---
type: kural
status: kapali
date: 2026-11-14
owner: PC1
---

# Çalışma kuralları

Bu dosyadaki kurallar hackathon boyunca değişmez. Aynı repoda aynı anda **6 ajan** (4 kişi,
3 bilgisayar, Claude Code + Antigravity) çalışıyor. Kuralların çoğu bu yüzden var: bir ajanın
"sorunu çözmek" için attığı tek yanlış adım, başka birinin saatlerce işini silebilir.

Yeni bir hata yapıldığında §9'a eklenir, silinmez.

---

## 1. Değişmez kurallar

| # | Kural |
|---|---|
| K-1 | Çalıştırılmamış kod "çalışıyor", koşulmamış test "geçti" diye raporlanmaz |
| K-2 | Ölçülmemiş sayı ölçülmüş gibi sunulmaz. Bilimsel her cümlenin kaynağı (link) olur. Tahmin "estimate", örnek değer "illustrative" diye etiketlenir |
| K-3 | Hangi veri sınıfından konuşulduğu (`provisional` / `beta-precal` / `preview`) her zaman yazılır; sınıflar aynı hesapta birleşmez |
| K-4 | `git add -A` ve `git add .` yok. Dosyalar tek tek, sadece kendi yollarından eklenir |
| K-5 | Yıkıcı git komutu yok (liste §2.3). Git hata verirse çözmeye çalışma: BLOCKED yaz, dur |
| K-6 | Tek dal: `main`. Dal açılmaz, yeni remote eklenmez. Push hedefi her zaman `origin main` |
| K-7 | Sadece kendi alanına yaz (`docs/GOREV_DAGILIMI.md` §2). Script'ler klasör silmez veya yeniden oluşturmaz; sadece kendi dosya adlarını yazar/üzerine yazar |
| K-8 | İş, `status/PCx.md` güncellenip push edilmeden bitmiş sayılmaz |
| K-9 | Şifre, token, `.netrc` içeriği asla repoya, status dosyasına, commit mesajına veya sohbete yazılmaz |
| K-10 | Görevde belirsizlik varsa tahmin yok: `BLOCKED:` yaz, push et, **o işi bırak ve sıradaki işe geç** (§7.1). Git hatasında ise git'e hiç dokunma, insana haber ver (§2.4) |
| K-11 | AI ile üretilen görsel/video asla veri gibi gösterilmez; üzerinde "AI-generated illustration" yazar |
| K-12 | Repoya giren tek dosya ≤ 20 MB. `.h5` ve ham veri asla girmez |
| K-13 | Başkasının beklediği bir çıktı bittiği anda push edilir (bağımlılıklar: `docs/GOREV_DAGILIMI.md` §4) |
| K-14 | Ürün metni (site, oyun, sunum, teslim) İngilizce. İç belgeler Türkçe olabilir |
| K-15 | **Hiç boş kalma:** iş bitince sormadan sıradakine geç (§7.1). Her 30-45 dakikada bir `git pull` |

---

## 2. Git: tek doğru akış

### 2.1 Her görevin başında
```bash
git status                 # temiz olmalı; değilse önce kendi dosyalarını commit et
git pull --rebase origin main
```

### 2.2 Her bitmiş çıktıda
```bash
git add <kendi/yolun/dosya1> <kendi/yolun/dosya2> status/PCx.md
git commit -m "[PCx] kısa açıklama"
git pull --rebase origin main
git push origin main
```
Push reddedilirse (`rejected`, `non-fast-forward`): bir kez daha `git pull --rebase origin main`, sonra push.
İkinci denemede de olmazsa → §2.4.

### 2.3 Yasak komutlar (K-5)
`git reset --hard` · `git push --force` / `-f` / `--force-with-lease` · `git clean` ·
`git checkout -- .` / `git restore .` · `git rebase -i` · `git stash drop` / `git stash clear` ·
`git branch -D` · `git filter-branch` · `git commit --amend` (push edilmiş commit'te) · `rm -rf` (kendi klasörün dışında)

### 2.4 Çakışma veya beklenmeyen git hatası olursa
1. Hiçbir şeyi silme, geri alma, zorlama.
2. `git rebase --abort` (rebase ortasındaysan; bu güvenli, işini geri getirir).
3. `status/PCx.md` dosyasına: `BLOCKED: git <komut> → <hata metninin ilk 3 satırı>`.
4. Dur ve insana haber ver. PC1 çözer.

### 2.5 Ne sıklıkla push?
- Başkası seni bekliyorsa (PC2 → PC3, PC3 → PC1/PC5/PC6): **her çıktıda hemen** (K-13).
- Bekleyen yoksa: her bitmiş alt görevde, en geç **saatte bir**.
- Yarım, çalışmayan kod push edilmez. Çalışan küçük adım > yarım büyük adım.

Herkes farklı dosyaya yazdığı sürece `pull --rebase` değişiklikleri kendiliğinden birleştirir;
çakışma ancak iki kişi **aynı dosyaya** yazınca olur. Dosya sahipliği (K-7) bu yüzden en önemli kural.

### 2.6 Satır sonları
Repoda `.gitattributes` var (`* text=auto eol=lf`). Windows editörünün dosyayı CRLF'e çevirmesi
sahte "tüm dosya değişti" diff'i üretmez. Bu dosyayı değiştirme.

---

## 3. Dosya sahipliği

- Her yolun tek sahibi var. Tablo: `docs/GOREV_DAGILIMI.md` §2.
- Başkasının dosyasında hata görürsen **düzeltme**; kendi status dosyana `NOT: <dosya> içinde <sorun>` yaz.
- Ortak klasörlerde (`data/<site>/`, `docs/story/`) birden çok kişi yazar ama **her dosyanın tek sahibi** var.
  Script'in o klasörü temizlerse başkasının dosyasını silersin (K-7).
- Aynı bilgisayarda birden çok ajan: her biri **ayrı klon klasöründe** çalışır.

---

## 4. Veri kalitesi ve kalibrasyon (zorunlu)

- **Kalibrasyon bizim işimiz değil.** Kalibrasyon ve doğrulamayı NISAR projesi (NASA-JPL ve ISRO) yapar.
  Ürünleri yayınlandığı hâliyle kullanırız; "kalibre ettik" ya da "düzelttik" demeyiz.
- Her katman/dosya `quality` etiketi taşır. Sınıflar ve kuralları: `rules/VERI_SOZLESMESI.md` §3.
- Web'de her veri katmanında rozet ve sabit dipnot:
  *"NISAR data are provisional. Calibration and validation are carried out by the NISAR project (NASA-JPL and ISRO), not by our team."*

## 5. Bilimsel doğruluk

- Algoritma yeniden icat edilmez: resmi kaynaktan uyarlanır, kaynak yorum satırına yazılır
  (NISAR Science Users' Handbook, https://github.com/nisar-solid/ATBD, https://github.com/ASFOpenSARlab/NISAR_ATBD_Cookbook).
- İşaret konvansiyonu (çökme negatif mi pozitif mi) ürün dokümanından doğrulanır, kaynağı yazılır.
- Sonuç literatürle kıyaslanır (Central Valley için USGS/JPL çökme hızları). Bir büyüklük mertebesi fark varsa yayınlanmaz, BLOCKED.
- Sade İngilizce cümleler **kuralla** üretilir (şablon + ölçülmüş sayı). LLM sayı üretmez.

## 6. Yapay zekâ ile üretilen medya

- Higgsfield/Gemini vb. görsel ve videolar sadece süs ve anlatım içindir.
- Her birinde görünür "AI-generated illustration" etiketi. Haritalarda sadece gerçek veri. NASA logosu kullanılmaz.
- Kullanılan tüm AI araçları teslimde açıklanır: her PC kendi status dosyasına `AI: <araç> → <ne için>` satırı ekler.

## 7. "Bitti" tanımı

Bir görev ancak şunların hepsi doğruysa bitmiştir:
1. Çıktı dosyaları görev dosyasındaki yolda ve formatta (`rules/VERI_SOZLESMESI.md`).
2. Kod çalıştırıldı, çıktı açılıp gözle kontrol edildi (PNG açıldı, JSON parse edildi, sayfa tarayıcıda açıldı).
3. `status/PCx.md` güncellendi: ne bitti, **nasıl doğrulandı**, sayılar ve kaynakları.
4. Push edildi.

### 7.1 Bittikten sonra: hiç boş kalma protokolü

Hedef: teslime kadar hiçbir ajan boşta durmaz. Bir görev bitince **sormadan** sıradakine geç:
1. Kendi `tasks/PCx.md` dosyandaki bitmemiş bir sonraki görev.
2. Yoksa `tasks/QUEUE.md`'den en üstteki sahiplenilmemiş iş:
   - Satırı `- [ ]` → `- [~PCx]` yap, **sadece o satırı** değiştir, hemen commit + push (başkası almasın).
   - Push çakışırsa `git pull --rebase origin main`; satırı başkası almışsa bir sonrakini seç.
   - Sahiplendiğin işte yazma iznin, o satırdaki **Klasör** sütunuyla sınırlı.
   - Bitince `- [x PCx]` + commit + push.
3. Kuyruk boşsa: kendi çıktılarını test et/iyileştir; başkalarının çıktısını kontrol et ve notunu
   **`docs/qa/PCx.md`** (kendi dosyan) içine yaz, onların dosyasına dokunma; kaynak doğrulama.

Ayrıca:
- Her iş bitince: status → `git pull --rebase origin main` → commit → push → **hemen** sonraki iş.
- Her 30-45 dakikada bir `git pull`: PC1 `tasks/` altına yeni görev yazabilir.
- Verimlilik: büyük dosyayı baştan sona okuma, `grep`/özet kullan; aynı araştırmayı tekrarlama, önce `docs/` ve `status/`'a bak.
- Yeniden okuma: her `git pull` sonrası `git diff --stat HEAD@{1} HEAD -- rules tasks docs CLAUDE.md` çalıştır;
  **sadece değişen dosyayı** yeniden oku. Kendi `tasks/PCx.md` dosyanı her yeni işten önce tekrar oku (kısa).

## 8. Disk ve indirme

- Ham veri `raw/` altına iner (git dışı). İş bitince ham dosya silinir; sadece kesilmiş alt küme kalır.
- Aynı anda diskte en fazla 5 ham GUNW/GCOV dosyası tut. (Bir GUNW ≈ 2-3 GB; plan: 6 dosya ≈ 14 GB.)
- Aynı bilgisayarda iki ajan aynı anda büyük indirme yapmaz; sırayla. Status'a indirme hızını yaz.
- Boş alan 20 GB'ın altına düşerse indirme durdurulur, BLOCKED.

---

## 9. Hata kaydı

Her madde gerçekten yaşanmış bir hatadan çıkar. Şablon:

```
### E-NN · kısa başlık
**Ne oldu:** ...
**Sonuç:** ...
**Düzeltme:** ...
**Ders →** hangi K kuralı (yoksa yeni K eklenir)
```

### E-01 · ASF araması `dataset=NISAR` ile boş
**Ne oldu:** SearchAPI `dataset=NISAR` 502/boş döndü.
**Sonuç:** Veri yok sanıldı.
**Düzeltme:** `platform=NISAR` kullan.
**Ders →** K-1 (çalıştırmadan sonuç raporlanmaz)

### E-02 · `.h5` indirmede "HTTP Basic: Access denied"
**Ne oldu:** Girişsiz `.h5` isteği reddedildi; browse PNG ise girişsiz indi.
**Sonuç:** Ham veri için Earthdata şart.
**Düzeltme:** Earthdata hesabı + `~/.netrc` (insan kendisi yazar).
**Ders →** K-9

### E-03 · git commit: "Author identity unknown"
**Ne oldu:** Yeni bilgisayarda git kimliği yoktu.
**Sonuç:** Commit atılamadı.
**Düzeltme:** Repo içinde `git config user.name` ve `user.email` (GitHub noreply e-postası; kişisel e-posta değil).
**Ders →** K-9

### E-04 · ASF sonucunda `bytes` alanı sözlük
**Ne oldu:** Dosya boyutunu toplarken TypeError.
**Sonuç:** Script çöktü.
**Düzeltme:** Boyut = iç `bytes` değerlerinin toplamı.
**Ders →** K-1

### E-05 · Windows Git Bash'te heredoc/tırnak içinde backtick
**Ne oldu:** Komut satırında Markdown backtick'i komut ikamesi gibi çalıştı, metin bozuldu.
**Sonuç:** Dosya eksik yazıldı.
**Düzeltme:** Dosyaları editör/yazma aracıyla oluştur; komut satırına backtick'li metin koyma; yazdıktan sonra kontrol et.
**Ders →** K-1

### E-06 · spaceappschallenge.org sayfaları boş geliyor
**Ne oldu:** Sayfa JS ile yüklendiği için düz istek boş döndü.
**Sonuç:** Bilgi yok sanıldı.
**Düzeltme:** Tarayıcıda 5-10 sn bekleyip oku.
**Ders →** K-2 (bilgi yoksa "bulunamadı" yaz, tahmin etme)

---

## Elenen alternatifler

- **Herkes kendi dalında çalışsın, PC1 PR'larla birleştirsin:** elendi. 48 saatte 6 ajanın PR'ını
  incelemek PC1'in tüm zamanını yer; klasör sahipliği aynı güvenliği daha ucuza sağlıyor.
- **Kuralları CLAUDE.md'ye yazalım:** elendi. CLAUDE.md giriş noktası olarak kısa kalmalı; kurallar ayrı
  dosyada olunca değiştirilmesi ve izlenmesi kolay.
- **Ajanlar git hatalarını kendileri çözsün:** elendi. Bir ajanın "düzeltmek" için çalıştırdığı
  `reset --hard` geri getirilemez. Durup haber vermek her zaman daha ucuz.

## Geri alınabilir mi

Hayır. Bunlar kısıt, tercih değil.
