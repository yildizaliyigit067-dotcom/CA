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
- 256 kuralın galerisini oluşturma aşamasında AI'dan yardımcı oldum.

AI'ı ağırlıklı olarak kodun mantığını kontrol etmek ve bazı noktaları anlamak için kullandım. Sonuçları ve testleri kendim kontrol ettim.

Bu aşamada kurallara Class I-IV etiketi vermedim. Sınıflandırma ve ölçümlere dayalı değerlendirme 2. haftanın ikinci yarısında yapacağım.
