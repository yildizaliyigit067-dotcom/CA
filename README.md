# Emergent Complexity in Cellular Automata

Bu depo, Levent Hoca'nın yaz projesi kapsamında hazırlanan, Hafta 1: Temel Hücresel Otomatlar (Elementary CA), Hafta 2: Belirme ve Hücresel Otomatların Sınıflandırılması ve Hafta 3: Başlangıç Koşullarına Duyarlılık ödevlerini içerir. Fork kaynağı: subasilevent/CA.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/01_elementary_CA.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/02_rule_classification.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yildizaliyigit067-dotcom/CA/blob/main/03_sensitivity.ipynb)

## İçerik

- `01_elementary_CA.ipynb`: Tek boyutlu hücresel otomatların sıfırdan yazılması (Kural 0, 30, 90, 110), gözlem/karşılaştırma tablosu, küçük araştırma (Kural 90 için N1(t) formülü) ve çıkış sorusu.
- `02_rule_classification.ipynb`: 256 temel hücresel otomat kuralının sistematik incelenmesi, Wolfram'ın dört nitel sınıfı, yoğunluk ρ(t) ve etkinlik a(t) ölçümleriyle büyük ölçekli davranışın sınıflandırılması.
- `03_sensitivity.ipynb`: Tek hücrelik başlangıç sapmalarının beş kuralda (0, 4, 30, 90, 110) yayılması; fark alanı, normalize Hamming uzaklığı D(t) ve sapma yarıçapı R(t) ölçümleri, nedensel etki yarıçapıyla karşılaştırma, 10 tohumluk tekrar deneyi ve Kural 90'ın doğrusallığı üzerine isteğe bağlı araştırma.
- `AI_NOTES.md`: 1., 2. ve 3. haftanın AI'dan hangi konularda yardım alındığının kaydı.

## Ana fikir

Basit yerel etkileşimler (üç hücrelik komşuluk kuralları), belirlenimci olmasına rağmen nitel olarak çok farklı büyük ölçekli davranışlar üretebiliyor. Bu, hücresel otomatlarda belirme olgusunun somut bir örneği. Hafta 3, buna bir boyut daha ekliyor: Aynı kural altında neredeyse aynı iki başlangıçtan yola çıkıldığında bile kurala bağlı olarak bilgi hızla sönebiliyor. Işık konisi hızında yayılabiliyor ya da ikisi arasında kısmi bir davranış sergileyebiliyor.
