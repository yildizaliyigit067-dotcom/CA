
# Emergent Complexity in Cellular Automata

Bu depo, Levent Hoca'nın yaz projesi kapsamında hazırlanan 1., 2., 3., 4., 5. ve 6. hafta çalışmalarını içerir.

Fork kaynağı: subasilevent/CA.

## Haftalık Çalışmalar

### Hafta 1: Temel Hücresel Otomatlar
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/01_elementary_CA.ipynb)

### Hafta 2: Belirme ve Hücresel Otomatların Sınıflandırılması
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/02_rule_classification.ipynb)

### Hafta 3: Başlangıç Koşullarına Duyarlılık
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/03_sensitivity.ipynb)

### Hafta 4: Conway'in Yaşam Oyunu
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/04_game_of_life.ipynb)

### Hafta 5: Rastgele Başlangıç Koşulları
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/05_random_initial_conditions.ipynb)

### Hafta 6: Stochastic Game of Life
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/06_stochastic_life.ipynb)

## Dosyalar

- `01_elementary_CA.ipynb`: Tek boyutlu hücresel otomatların sıfırdan yazılması (Kural 0, 30, 90, 110), gözlem ve karşılaştırma tablosu, Kural 90 için N1(t) formülü ve çıkış sorusu.

- `02_rule_classification.ipynb`: 256 temel hücresel otomat kuralının incelenmesi, Wolfram'ın dört nitel sınıfı, yoğunluk ρ(t) ve etkinlik a(t) ölçümleriyle davranışların sınıflandırılması.

- `03_sensitivity.ipynb`: Tek hücrelik başlangıç farklılıklarının beş kuralda (0, 4, 30, 90, 110) yayılması, Hamming uzaklığı D(t), sapma yarıçapı R(t), 10 tohumluk tekrar deneyi ve Kural 90'ın doğrusallığı üzerine araştırma.

- `04_game_of_life.ipynb`: Conway'in Yaşam Oyunu'nun B3/S23 kurallarıyla uygulanması, still life, oscillator ve spaceship örneklerinin incelenmesi.

- `05_random_initial_conditions.ipynb`: Game of Life'ta rastgele başlangıç koşullarının incelenmesi. Başlangıç yoğunluğu p değiştirilerek yoğunluk ve etkinlik grafiklerinin oluşturulması, bağımsız tekrarlar, ortalama ve standart sapma hesaplamaları. Ek olarak M = 100 ve M = 300 için karşılaştırmalar, q parametresinin etkisi ve farklı ızgara boyutlarıyla deneyler.

- `06_stochastic_life.ipynb`: Game of Life modeline rastgele ölüm olasılığının eklenmesi. Bağımsız ve kümelenmiş ölümlerin karşılaştırılması, yoğunluk, etkinlik ve sönme sürelerinin incelenmesi. L = 60, 80, 100 ve 200 değerleriyle, farklı ölüm olasılıklarında 3.000 adıma kadar toplam 480 simülasyon yapılması.

- `AI_NOTES.md`: Çalışmalarda yapay zekâdan hangi konularda yardım alındığının kaydı.

## Ana Fikir

Basit yerel kurallarla çalışan hücresel otomatlar, farklı başlangıç koşullarında oldukça karmaşık davranışlar gösterebiliyor.

Hafta 1 ve 2'de temel hücresel otomat kurallarını ve bu kuralların oluşturduğu farklı davranışları inceledim.

Hafta 3'te başlangıçta yapılan küçük bir değişikliğin zamanla nasıl yayıldığına baktım. Aynı kural altında başlangıç koşullarındaki küçük farklılıkların farklı sonuçlar oluşturabildiğini gördüm.

Hafta 4'te iki boyutlu Game of Life modeline geçtim. Basit komşuluk kurallarından sabit, tekrarlayan ve hareket eden yapıların nasıl oluştuğunu inceledim.

Hafta 5'te rastgele başlangıç koşullarını araştırdım. Farklı başlangıç yoğunluklarıyla deneyler yaparak sistemin yoğunluğunu ve etkinliğini karşılaştırdım. Tekrar sayısını artırarak ortalama ve standart sapma değerlerini inceledim. Ayrıca farklı M, q ve ızgara boyutlarının sonuçlara etkisine baktım.

Hafta 6'da modele rastgele ölüm olasılığı ekledim. Önce bağımsız ölümlerin sistem üzerindeki etkisini inceledim. Daha sonra aynı ölüm olasılığını koruyarak ölümlerin birbirine yakın hücrelerde kümelendiği ikinci bir model üzerinde çalıştım.

İki modeli karşılaştırmak için L değerlerini 60, 80, 100 ve 200 olarak belirledim. Daha uzun süreli davranışları görebilmek için simülasyonları 3.000 adıma çıkardım ve toplam 480 simülasyon çalıştırdım.

Özellikle düşük ölüm olasılıklarında iki modelin farklı davrandığını gördüm. Kümelenmiş ölümler bazı koşullarda sistemin daha hızlı sönmesine neden oldu. Bu sonuç, yalnızca ölüm olasılığının değil, ölümlerin uzaydaki dağılımının da önemli olabileceğini gösteriyor.

Bu farkın neden oluştuğunu ve farklı parametrelerde de devam edip etmediğini araştırmak istiyorum.
