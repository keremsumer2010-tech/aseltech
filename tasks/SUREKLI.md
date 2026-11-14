# 📣 GENEL EMİR (Paz 01:50): herkes şu an commit + push etsin, status'a ilerleme yazsın; en geç 10 dk'da bir commit.

# SÜREKLİ ÇALIŞMA KURALI — herkes için, teslime kadar (PC1, Paz 00:45)

## 1. 3 dakika döngüsü (her ajan, her zaman)
Her 3 dakikada bir (uzun indirme/işlem arka planda sürerken de):
1. Kendi değişikliklerini commit et → `git pull --rebase origin main` → push.
2. `tasks/PCx.md` dosyanın SONUNA bak: yeni bölüm var mı? Varsa mevcut adımı bitirip ona geç.
3. `docs/qa/PC5.md` §10 ve `docs/qa/*.md` içinde senin dosyanla ilgili yeni bulgu var mı? Varsa düzelt.
4. `status/PCx.md`'ye tek satır: şu an ne yapıyorsun, sıradaki ne.
Uzun bir iş (indirme, işleme) çalışırken BEKLEME: arka planda bırak, bu sırada aşağıdaki sürekli işlerden birini yap.

## 2. Asla durma
"Bitti", "görev bekleniyor", "kullanıcıdan onay bekliyorum" deme. Listen bittiyse sırayla:
(a) kendi bölümündeki SÜREKLİ İŞ'ler (aşağıda), (b) `tasks/QUEUE.md`'den bir satır al (`[~PCx]`), (c) hata ayıklama (`python -m pytest -q`, `pipeline/pc7/validate_json.py`, `tools/validate_atlas.py`, site yerel test), (d) kendi metinlerini REVIEW_1500'e göre sadeleştir.
Gerçek engelde (yetki, şifre, çakışma) `BLOCKED: <neden>` yaz ve engelsiz bir sürekli işe geç; durma.

## 3. Rol başına SÜREKLİ İŞLER (liste biterse bunlar döngüyle)
| PC | Sürekli iş |
|---|---|
| PC2 | Yeni atlas şehri (kapsama olan, yayımlanmış çökmesi olan; önce `docs/qa/PC2.md`'ye aday + kaynak), NISAR Pulse testleri, OPERA kıyasını genişlet |
| PC4 | Atlas metinlerini (press_summary, slides, technical_note, şehir kartları, atlas_feature) son atlas.json ile senkronla; dil temizliği |
| PC5 | Sayı sicilini yeniden çalıştır, yeni uyumsuzlukları §10'a yaz, yeni şehirlere karar, detectability güncelle |
| PC6 | Atlas sayfası: performans, erişilebilirlik, mobil, projektör, çevrimdışı test; yeni atlas alanlarını panele ekle (uydu animasyonu PC1'in, `web/atlas_sat.*` dosyalarına dokunma) |
| PC7 | Robustness'i yeni şehirlerle yeniden çalıştır, validate_atlas, küresel altyapı riski (yeni şehir) |
| PC8 | Bülten + exposure + vital_signs'ı yeni şehirlerle yeniden üret; teslim formu karakter/sayı kontrolü |
| PC9 | Yeni atlas şehri veya tam yıl (annualization) için ek bölge; GPS kıyası |
| PC10 | Atlası her "hazır" notunda yeniden üret; atlas.geojson/csv; global_atlas.md tablosu |
| PC11 | Kendi şehir sırası; bitince yeni aday şehir (kaynaklı) ve robustness için tam kutu verisi |

## 4. PC1 ne yapar
PC1 düzenli kontrol eder; görevi azalan ajanın `tasks/PCx.md` sonuna yeni bölüm ekler. Senin işin 3 dakikada bir dosyanın sonuna bakmak.
