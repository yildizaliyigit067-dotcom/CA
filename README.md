
# Emergent Complexity in Cellular Automata

Bu depo, Levent Hoca'nın yaz projesi kapsamında hazırlanan, Hafta 1: Temel Hücresel Otomatlar (Elementary CA), Hafta 2: Belirme ve Hücresel Otomatların Sınıflandırılması, Hafta 3: Başlangıç Koşullarına Duyarlılık, Hafta 4: Conway'in Yaşam Oyunu (Game of Life), Hafta 5: Rastgele Başlangıç Koşulları ve Hafta 6: Stochastic Game of Life ödevlerini içerir. Fork kaynağı: subasilevent/CA.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/01_elementary_CA.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/02_rule_classification.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/03_sensitivity.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/04_game_of_life.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/05_random_initial_conditions.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/06_stochastic_life.ipynb)


- `01_elementary_CA.ipynb`: Tek boyutlu hücresel otomatların sıfırdan yazılması (Kural 0, 30, 90, 110), gözlem/karşılaştırma tablosu, küçük araştırma (Kural 90 için N1(t) formülü) ve çıkış sorusu.
- `02_rule_classification.ipynb`: 256 temel hücresel otomat kuralının sistematik incelenmesi, Wolfram'ın dört nitel sınıfı, yoğunluk ρ(t) ve etkinlik a(t) ölçümleriyle büyük ölçekli davranışın sınıflandırılması.
- `03_sensitivity.ipynb`: Tek hücrelik başlangıç sapmalarının beş kuralda (0, 4, 30, 90, 110) yayılması, fark alanı, normalize Hamming uzaklığı D(t) ve sapma yarıçapı R(t) ölçümleri, nedensel etki yarıçapıyla karşılaştırma, 10 tohumluk tekrar deneyi ve Kural 90'ın doğrusallığı üzerine isteğe bağlı araştırma.
- `04_game_of_life.ipynb`: Conway'in Yaşam Oyunu'nun (B3/S23 kuralı) `np.roll` ve boolean maskeler kullanılarak uygulanması, still life, oscillator ve spaceship örneklerinin incelenmesi.
- `05_random_initial_conditions.ipynb`: Game of Life'ta rastgele başlangıç koşullarının incelenmesi, başlangıç yoğunluğu $p$ değiştirilerek yoğunluk ve etkinlik zaman serilerinin hesaplanması, bağımsız tekrarlar, geç-zaman ortalamaları ve standart sapma ile tipik davranışın araştırılması. M = 100 ve 300 karşılaştırmaları, q parametresi ve farklı ızgara boyutlarıyla ek deneyler.
- `06_stochastic_life.ipynb`: Game of Life'a rastgele ölüm olasılığının eklenmesi, yoğunluk, etkinlik ve sönme sürelerinin incelenmesi. Bağımsız ve kümelenmiş ölüm modellerinin karşılaştırılması, L = 60, 80, 100 ve 200 için 3.000 adımlık toplam 480 simülasyon.
- `AI_NOTES.md`: 1., 2., 3., 4., 5. ve 6. haftalarda AI'dan hangi konularda yardım alındığının kaydı.

## Ana fikir

Basit yerel etkileşimler, belirlenimci olmasına rağmen nitel olarak çok farklı büyük ölçekli davranışlar üretebiliyor. Bu, hücresel otomatlarda belirme olgusunun somut bir örneği.

Hafta 1'de temel hücresel otomat kuralları uygulanıyor. Kural 0, 30, 90 ve 110'un farklı başlangıç koşullarında oluşturduğu desenler inceleniyor.

Hafta 2'de 256 temel kural, Wolfram'ın dört sınıfına göre değerlendiriliyor. Yoğunluk ve etkinlik ölçümleriyle kuralların uzun vadeli davranışları karşılaştırılıyor.

Hafta 3'te başlangıç koşullarındaki tek hücrelik değişikliklerin zamanla nasıl yayıldığı inceleniyor. Hamming uzaklığı ve sapma yarıçapıyla farklı kuralların başlangıç koşullarına duyarlılığı ölçülüyor.

Hafta 4'te iki boyutlu Game of Life modeline geçiliyor. Basit komşuluk kurallarından still life, oscillator ve spaceship gibi yapıların nasıl ortaya çıktığı gösteriliyor.

Hafta 5'te rastgele başlangıç koşullarıyla çok sayıda deney yapılıyor. Farklı başlangıç yoğunluklarının sistemin davranışına etkisi, ortalama ve standart sapma kullanılarak inceleniyor. Ayrıca M, q ve ızgara boyutlarının sonuçlara etkisi karşılaştırılıyor.

Hafta 6'da modele rastgele ölüm olasılığı ekleniyor. Aynı ölüm olasılığı altında bağımsız ve kümelenmiş ölümler karşılaştırılıyor. Farklı ızgara boyutlarında 3.000 adımlık toplam 480 simülasyon yapılıyor. Özellikle düşük ölüm olasılıklarında kümelenmiş ölümlerin sistemin daha hızlı sönmesine neden olabildiği gözlemleniyor.
