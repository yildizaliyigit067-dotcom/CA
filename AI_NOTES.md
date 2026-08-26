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

Bu bölümde `AI_NOTES.md` dosyasına kısa bir not eklenmiştir.

### AI'dan aldığım yardım

- 1. haftadaki `rule_output` ve `update_row_student` fonksiyonlarının `(rule_number >> index) & 1` mantığını doğru kullanıp kullanmadığını AI ile kontrol ettim. Elle yaptığım Rule 30 ve Rule 100 kontrolleri ve testlerle implementation'ın zaten doğru olduğunu doğruladım.
- `random_initial_state` fonksiyonunda kullanılan `rng.random(width) < density` ifadesinin mantığını anlamak için AI'dan kısa bir açıklama aldım.
- 256 kuralın galerisini oluşturma aşamasında AI'dan yardım aldım.

AI'ı ağırlıklı olarak kodun mantığını kontrol etmek ve bazı noktaları anlamak için kullandım. Sonuçları ve testleri kendim kontrol ettim.

Bu aşamada kurallara Class I-IV etiketi vermedim. Sınıflandırma ve ölçümlere dayalı değerlendirmeyi 2. haftanın ikinci yarısında yapacağım.

## Hafta 2 (Rule Classification), 2. yarı

### AI'dan aldığım yardım

- `density_time_series`, `activity_time_series` ve `compare_initial_conditions` fonksiyonlarının implementasyonunda AI'dan doğrudan yardım aldım (fonksiyonları AI yazdı, ben `check(...)` testleriyle doğruladım; testlerin hiçbiri değiştirilmedi/gevşetilmedi).
- Yoğunluk/etkinlik grafiklerini ve isteğe bağlı saçılım grafiğini oluşturan kod, mevcut notebook yapısına (referans fonksiyonlar, `gallery_initial`, `representative_rules` vb.) uygun biçimde AI tarafından tamamlandı.
- 16 kuralın geçici sınıflandırma tablosundaki ve yorum bölümlerindeki metinleri AI, notebook'u gerçekten çalıştırıp elde ettiği sayısal sonuçlara (uzun-vadeli ortalama yoğunluk/etkinlik, standart sapma vb.) ve galeri görsellerine dayanarak yazdı. Sınıf etiketleri otomatik bir algoritmayla üretilmedi; AI her kural için görsel + sayısal kanıtı birlikte değerlendirip geçici bir etiket önerdi.
- Notebook, "Restart Kernel and Run All" ile temiz bir kernelde uçtan uca çalıştırıldı; dört alıştırma testi de (`check(...)`) geçti.

### Kendi anlayışımı nasıl kontrol edeceğim

- Density ve activity formüllerini (`np.mean(axis=1)` ve `np.diff` + `np.abs` + `np.mean(axis=1)`) kendim elle küçük bir örnek üzerinde tekrar hesaplayıp doğrulayacağım.
- 16 kuralın sınıflandırma tablosundaki her satırı, galeriye tekrar bakarak kendi yorumumla karşılaştıracağım; özellikle "düşük güven" etiketli kurallarda (54, 60, 90, 150) kendi gerekçemi oluşturacağım.
- Toplantıda Levent Hoca sorarsa yoğunluk ve etkinlik formüllerini ve bit-kaydırma mantığını kendim tahtada/ekranda tekrar açıklayabileceğimden emin olacağım.

### Not

AI, bu bölümde önceki yarıya göre daha fazla kod yazdı (implementasyonlar ve yorum metinleri). Bütün bilimsel sonuçları AI tek başına "üretmedi" — sayılar gerçek kodun gerçek çalıştırılmasından geldi, ama hangi sayının hangi cümleye dönüştüğü AI tarafından yazıldı. Bunu toplantıda Levent Hoca'ya açıkça belirteceğim ve gerekirse kendi cümlelerimle yeniden ifade edeceğim.
