# AI Kullanım Notları - Hafta 1 (Elementary CA)

Bu dosya, ''01_elementary_CA.ipynb'' üzerinde çalışırken AI'dan (Claude,ChatGPT) hangi konularda destek aldığımı şeffaf biçimde kaydetmek için tutuluyor.

## Ne için yardım istedim

- Ödevdeki fonksiyonları kendim tamamladım. Takıldığım veya anlamını netleştirmek istediğim bazı noktalarda AI'dan destek aldım.
- `rule_output` fonksiyonundaki bit kaydırma (`>>`) ve bit maskeleme (`&`) işlemlerinin nasıl çalıştığını anlamak için AI'dan açıklama istedim.
- Kural 110 tablosunun neden belirli bir sırayla listeye yazıldığını anlamak için AI'dan kısa bir açıklama aldım.
- Gözlem tablosundaki bazı değerleri kontrol etmek ve sonuçları karşılaştırmak için AI'dan destek aldım.
- Küçük araştırma bölümünde Kural 90 ve $$N_1(t) = 2^{\text{popcount}_2(t)}$$ hipoteziyle ilgili yaklaşımı anlamak ve kendi sonuçlarımı kontrol etmek için AI'dan yararlandım.

## Kendi anlayışımı nasıl kontrol edeceğim

- Notebook'taki her fonksiyonu ve "Hafta 1 Hazırlık Soruları" listesindeki soruları kendi başıma tekrar gözden geçireceğim.
- Özellikle bit işlemleri ile Pascal üçgeni ve Kural 90 arasındaki ilişkiyi kendim açıklayabildiğimden emin olacağım.
- Anlamadığım kısımları haftalık toplantıda Levent Hoca'ya soracağım.

## Not

Bu hafta AI'ı ağırlıklı olarak kodu benim yerime yazdırmak için değil, takıldığım noktaları anlamak, teknik kavramları açıklığa kavuşturmak ve bazı sonuçları kontrol etmek amacıyla kullandım. Notebook'taki kodun mantığını kendim anlayıp açıklayabildiğimden emin olmak için kodu satır satır gözden geçireceğim.

## Hafta 2 (Rule Classification), 1. yarı

Bu bolumde mevcut `AI_NOTES.md` dosyasina ek yapiliyor.

### Ne icin yardim istedim

- 1. haftadaki `rule_output`/`update_row_student` fonksiyonlarinin Levent Hoca'nin istedigi genel `(rule_number >> index) & 1` mantigini gercekten dogru kullanip kullanmadigini AI ile birlikte dogruladim (elle kontrol + otomatik test). Sonuc: zaten dogruydu, degisiklik gerekmedi.
- `random_initial_state` fonksiyonunun kodunu (Alistirma 1) AI yazdi; `rng.random(width) < density` mantigini neden kullandigimizi AI'dan ogrendim.
- 256 kuralin galerisini AI calistirip uretti. Bu asamada AI kurallara kesin sinif etiketi (Class I-IV) vermedi -- notebook'un kendi talimatina uygun bicimde bilincli olarak ikinci yariya birakildi.

### Kendi anlayisimi nasil kontrol edecegim

- Rule 30 ve Rule 100 icin elle cikardigimiz index/bit tablolarini tekrar kendi basima yeniden turetecegim.
- `random_initial_state` fonksiyonunu satir satir okuyup mantigini kendi cumlelerimle aciklayabildigimden emin olacagim.
- Galerideki gozlemlerimi kendi gozumle tekrar kontrol edecegim.

### Not

Bu ilk yarida AI kodu yazip notebook'u calistirdi; ben bunu anlayip sahiplenmekle yukumluyum. Ikinci yarida (yogunluk, etkinlik, siniflandirma tablosu) da ayni seffaflik ilkesiyle devam edecegiz.
