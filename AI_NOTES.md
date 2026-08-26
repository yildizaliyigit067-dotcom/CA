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

# Hafta 2 - Rule Classification

Bu hafta AI'dan bazı teknik noktaları anlamak, kodu kontrol etmek ve gerektiğinde yönlendirme almak için yararlandım.

## AI'dan aldığım yardım

- Mevcut kodların ve bazı fonksiyonların mantığını kontrol etmek için kısa açıklamalar aldım.
- 256 rule gallery ile density/activity bölümlerinde kod yapısını kontrol etmek için yardım aldım.
- Bazı grafiklerin oluşturulması ve kod hatalarının giderilmesi sırasında destek aldım.
- 16 seçilmiş rule'un sonuçlarını değerlendirirken grafikler ve sayısal ölçümler üzerinden fikir aldım.

## AI kullanımının kapsamı

AI'ı ağırlıklı olarak teknik açıklama, kod kontrolü ve gerektiğinde yönlendirme amacıyla kullandım. Elde edilen sonuçları notebook'u çalıştırarak ve mevcut testlerle kontrol ettim.

Testler değiştirilmedi, gevşetilmedi veya hard-code sonuçlarla geçilmedi.

Class I-IV sınıflandırması otomatik olarak yapılmadı. 16 rule için değerlendirmeler grafikler ile density/activity sonuçları birlikte incelenerek yapıldı.

## Kendi kontrolüm

- Density ve activity formüllerini kendim tekrar gözden geçireceğim.
- Grafiklerdeki sonuçları kendi yorumumla değerlendireceğim.
- Initial condition değişiminin sonuçlara etkisini inceleyeceğim.


## Not

AI desteğini teknik noktaları açıklığa kavuşturmak ve kodu kontrol etmek amacıyla kullandım. Sonuçlar gerçek notebook çalıştırmalarından elde edildi ve mevcut testlerle kontrol edildi.
