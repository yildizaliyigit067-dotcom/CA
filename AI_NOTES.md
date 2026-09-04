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

# Hafta 3 - Başlangıç Koşullarına Duyarlılık

Bu haftaki `03_sensitivity.ipynb` dosyasını daha önce tamamlamıştım, ancak yerel kopyam silindiği için notebook'u yeniden oluştururken Claude'dan (Anthropic) sınırlı ölçüde yardım aldım. AI desteğini ağırlıklı olarak önceki çalışmamın yapısını yeniden kurmak, bazı kod parçalarını kontrol etmek ve sonuçların yorumlanmasında ikinci bir görüş almak için kullandım.

## AI'dan aldığım yardım

- Dört alıştırmadaki TODO fonksiyonlarının (`make_perturbed_pair`, `difference_field`, `hamming_distance`, `damage_radius`) yeniden oluşturulması sırasında kod önerileri aldım ve bunları mevcut şablon testleriyle kontrol ettim.
- Deneylerin yeniden çalıştırılması ve elde edilen sayısal sonuçların düzenlenmesi sırasında yardımcı olarak kullandım.
- Bazı tablo ve yorumların daha açık ifade edilmesi için metin önerileri aldım.

## Kendi çalışmam ve kontrolüm

- Notebook'u `Restart Kernel and Run All Cells` ile baştan çalıştırarak tüm testleri ve deney sonuçlarını kendim doğrulayacağım.
- Kullanılan her fonksiyonun mantığını anlayıp kendi kelimelerimle açıklayabildiğimden emin olacağım. Özellikle `damage_radius` fonksiyonunda değişen hücrelerin başlangıçtaki pertürbasyon noktasına olan uzaklıklarının nasıl hesaplandığını tekrar inceleyeceğim.
- Tahminleri, grafiklerde gözlemlediğim davranışları ve `D(t)` / `R(t)` değerlerini karşılaştırarak yorumları kendi değerlendirmeme göre düzenleyeceğim.
- Bölüm 6-8'deki yorumları ve görüşme için hazırlanan soruları Levent Hoca ile görüşmeden önce yeniden değerlendireceğim.

## Not

Bu hafta AI'ı, silinen notebook'un yeniden oluşturulmasını hızlandırmak ve çalışmamı kontrol etmek amacıyla yardımcı bir araç olarak kullandım. Nihai kodu, sonuçları ve yorumları anlamak ve doğrulamak benim sorumluluğumdadır.
