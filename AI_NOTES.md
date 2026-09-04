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

Bu haftaki `03_sensitivity.ipynb` dosyasını daha önce kendim tamamlamıştım, fakat yerel kopyam silindiği için notebook'u yeniden oluşturmak üzere Claude'dan (Anthropic) yardım aldım. Önceki iki haftadan farklı olarak, bu hafta AI kodu ve yorum metinlerinin büyük bölümünü benim yerime yazdı; bunu şeffaf biçimde burada belirtiyorum.

## AI'dan aldığım yardım

- Dört alıştırmadaki TODO'ları (`make_perturbed_pair`, `difference_field`, `hamming_distance`, `damage_radius`) doldurdu; kod, şablon testlerinin dördünü de geçti.
- Ana deneyi (5 kural × 401 hücre × 120 adım), 10 tohumluk tekrar deneyini ve isteğe bağlı Kural 90 doğrusallık kontrolünü çalıştırıp gerçek sayısal sonuçlar (D(t), R(t), tepe/son değerler, ortalama ve standart sapma) üretti.
- Deney öncesi tahmin tablosunu, ana sonuç tablosunu, tekrarlı deney tablosunu, ışık konisi yorumunu ve bilimsel sonuç paragrafını bu gerçek sayılara dayanarak yazdı.

## Kendi kontrolüm — bunu mutlaka yapacağım

- Notebook'u `Restart Kernel and Run All Cells` ile baştan çalıştırıp dört testin de gerçekten geçtiğini kendi gözümle doğrulayacağım.
- Her fonksiyonu satır satır okuyup mantığını kendi kelimelerimle açıklayabildiğimden emin olacağım; özellikle `damage_radius` içindeki `np.abs(changed_indices - center_index)` mantığını.
- Tahmin ve yorum tablolarındaki her ifadeyi, şekillerle ve yazdırılan sayılarla karşılaştırarak gözden geçireceğim; katılmadığım ya da tam anlamadığım cümleleri kendi ifademle değiştireceğim.
- "Görüşmeye getirilecekler" bölümündeki iki soruyu ve Bölüm 6-8'deki yorumları, Levent Hoca ile görüşmeden önce kendi başıma tekrar düşünüp gerekirse revize edeceğim; bu notebook'u canlı bir tartışmada savunabilecek kadar anlamış olmam gerekiyor.

## Not

Bu hafta AI kullanımının kapsamı önceki iki haftadan belirgin biçimde daha genişti (kayıp çalışmayı yeniden oluşturma amacıyla). Bunu gizlemek yerine burada açıkça yazıyorum; teslimden önce notebook'un tamamını anlayıp sahiplenmek benim sorumluluğum.
