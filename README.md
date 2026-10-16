
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
- `05_random_initial_conditions.ipynb`: Game of Life'ta rastgele başlangıç koşullarının incelenmesi, başlangıç yoğunluğu $p$ değiştirilerek yoğunluk ve etkinlik zaman serilerinin hesaplanması, bağımsız tekrarlar, geç-zaman ortalamaları, örneklem ortalaması ve standart sapma ile tipik davranışın araştırılması. M = 100 ve M = 300 için karşılaştırmalar, q parametresinin etkisi ve farklı ızgara boyutlarıyla ek deneyler.
- `06_stochastic_life.ipynb`: Game of Life'a rastgele ölüm olasılığının eklenmesi, yoğunluk, etkinlik ve sönme sürelerinin incelenmesi. Bağımsız ve kümelenmiş ölümlerin karşılaştırılması, L = 60, 80, 100 ve 200 için farklı ölüm olasılıklarında 3.000 adımlık deneyler ve toplam 480 simülasyon.
- `AI_NOTES.md`: 1., 2., 3., 4., 5. ve 6. haftada AI'dan hangi konularda yardım alındığının kaydı.

## Ana fikir

Basit yerel etkileşimler (üç hücrelik komşuluk kuralları), belirlenimci olmasına rağmen nitel olarak çok farklı büyük ölçekli davranışlar üretebiliyor. Bu, hücresel otomatlarda belirme olgusunun somut bir örneği.

Hafta 3, buna bir boyut daha ekliyor: Aynı kural altında neredeyse aynı iki başlangıçtan yola çıkıldığında bile kurala bağlı olarak bilgi hızla sönebiliyor, ışık konisi hızında yayılabiliyor ya da ikisi arasında kısmi bir davranış sergileyebiliyor.

Hafta 4'te ise iki boyutlu Game of Life ile basit komşuluk kurallarından still life, oscillator ve spaceship gibi kalıcı ve hareketli yapıların nasıl ortaya çıktığı gösteriliyor.

Hafta 5'te tek tek özel başlangıç durumları yerine rastgele başlangıçlardan oluşan çok sayıda deney inceleniyor. Başlangıç yoğunluğu $p$ değiştirilerek sistemin uzun zamandaki yoğunluğu ve etkinliği ölçülüyor. Aynı $p$ değeri için bağımsız tekrarlar yapılarak ortalama ve standart sapma hesaplanıyor. Böylece tek bir simülasyonun davranışından ziyade sistemin tipik davranışını ve deneyden deneye oluşan değişkenliği incelemek mümkün oluyor. Ek olarak M = 100 ve M = 300 değerleri karşılaştırılıyor, q parametresinin sonuçlara etkisi ve farklı ızgara boyutları inceleniyor.

Hafta 6'da Game of Life modeline rastgele ölüm olasılığı ekleniyor. Ölüm olasılığı μ değiştirilerek yoğunluk, etkinlik ve sistemin tamamen sönme süresi inceleniyor. Bağımsız tekrarlarla rastgeleliğin sonuçlar üzerindeki etkisi araştırılıyor.

Buna ek olarak, aynı ölüm olasılığı korunurken ölümlerin birbirine yakın hücrelerde kümelenmesinin sistemi nasıl etkilediği karşılaştırılıyor. L = 60, 80, 100 ve 200 değerleri için üç farklı ölüm olasılığı kullanılarak 3.000 adımlık toplam 480 simülasyon yapılıyor. Özellikle düşük ölüm olasılığında bağımsız ve kümelenmiş ölüm modelleri arasında belirgin farklar gözlemleniyor. Kümelenmiş ölüm modelinin incelenen koşullarda daha hızlı sönebildiği görülüyor. Bu sonuçların farklı korelasyon uzunluklarında nasıl değiştiği ise sonraki araştırmalar için bir soru olarak kalıyor.
