# Hamming SEC-DED Kod Simülatörü

Bu proje, Hamming Kodlama tekniğinin **SEC (Single Error Correction - Tek Hata Düzeltme)** ve **SEC-DED (Single Error Correction - Double Error Detection)** modlarını simüle eden, Python ve PyQt5 ile geliştirilmiş bir masaüstü uygulamasıdır. Uygulama, kullanıcıların hata düzeltme ve tespit algoritmalarının çalışma prensiplerini interaktif bir şekilde anlamalarını sağlar.



## Özellikler

-   **İki Farklı Mod:**
    -   **SEC:** Tek bitlik hataları tespit eder ve otomatik olarak düzeltir.
    -   **SEC-DED:** Tek bitlik hataları düzeltir ve çift bitlik hataları tespit eder.
-   **Esnek Veri Girişi:** 8, 16 ve 32 bitlik veri uzunluklarını destekler.
-   **İnteraktif Hata Simülasyonu:** Kullanıcı tarafından belirlenen pozisyonlara hata ekleyerek algoritmayı test etme imkânı.
-   **Detaylı Analiz:** Adım adım sonuçlar sunar:
    -   Belleğe yazılan orijinal kodlanmış kelime.
    -   Hata eklenmiş (okunan) kelime.
    -   Hatanın konumunu belirten sendrom kelimesi.
    -   Hatanın durumunu açıklayan analiz metni (Hata yok, düzeltildi, düzeltilemez vb.).
    -   Düzeltilmiş nihai kod kelimesi.
-   **Kullanıcı Dostu Arayüz:** PyQt5 ile oluşturulmuş sekmeli, modern ve anlaşılır bir grafiksel arayüz.
-   **Görsel Geri Bildirim:** Analiz sonucuna göre (hata yok, düzeltildi, tespit edildi) arayüz renklenerek anlık geri bildirim sağlar.

## Gereksinimler

-   Python 3.x
-   PyQt5

## Kurulum

1.  Projeyi bilgisayarınıza klonlayın veya ZIP olarak indirin:
    ```bash
    git clone https://github.com/tanercinar/bmSecDedSim
    ```
2.  Proje dizinine gidin:
    ```bash
    cd proje-repo-adi
    ```
3.  Gerekli kütüphaneyi `pip` kullanarak yükleyin:
    ```bash
    pip install PyQt5
    ```

## Kullanım

Uygulamayı başlatmak için terminalde aşağıdaki komutu çalıştırın:
```bash
python main.py
```

**Arayüzde:**

1.  İstediğiniz modu seçin (**SEC** veya **SEC-DED** sekmesi).
2.  **Veri Boyutu** menüsünden (8-bit, 16-bit, 32-bit) seçiminizi yapın.
3.  **Veri (Binary)** alanına seçtiğiniz boyutta ikili sayı girin (örn: "10110010").
4.  `Kodu Hesapla ve Belleğe Yaz` butonuna tıklayarak verinizin Hamming koduna çevrilmesini sağlayın.
5.  Hata simülasyonu için **Hata Pozisyonu** alanına hata eklemek istediğiniz bit pozisyonunu/pozisyonlarını (1-tabanlı, sağdan başlayarak) girin.
6.  `Hata Oluştur ve Kontrol Et` butonuna tıklayın.
7.  Sonuçları alt kısımdaki analiz panelinden inceleyin.

## Modlar

#### SEC (Single Error Correction) Modu
Bu mod, bir kod kelimesindeki tek bir bit hatasını hem tespit etme hem de düzeltme yeteneğine sahiptir.
-   Hesaplanan **sendrom kelimesinin** ondalık değeri, doğrudan hatalı bitin pozisyonunu verir.
-   Eğer sendrom sıfır ise, hata olmadığı anlaşılır.
-   Hatalı pozisyon bulunduğunda, o bitteki değer (0 ise 1, 1 ise 0) ters çevrilerek düzeltme yapılır.

#### SEC-DED (Double Error Detection) Modu
Bu mod, SEC'in yeteneklerine ek olarak çift bit hatalarını tespit etme özelliği sunar. Bu, kod kelimesinin tamamı için hesaplanan ekstra bir **genel parite biti** ile sağlanır.
-   **Tek Hata:** Sendrom sıfırdan farklıdır ve genel parite kontrolü başarısız olur. Hata, SEC modundaki gibi düzeltilir.
-   **Çift Hata:** Sendrom sıfırdan farklıdır ancak genel parite kontrolü başarılı olur (çünkü iki hata birbirini parite açısından dengeler). Bu durum, sistemin bir çift hata olduğunu anlamasını sağlar, ancak konumlarını belirleyemediği için **"Düzeltilemez"** olarak raporlar.
-   **Hata Yok:** Hem sendrom hem de genel parite kontrolü sıfırdır.

## Teknik Detaylar

#### Hamming Kodu Hesaplama
-   Girilen `k` bitlik veri için gerekli parite biti sayısı (`p`), `2^p >= k + p + 1` formülü ile bulunur.
-   Parite bitleri, kod kelimesinde pozisyon numarası 2'nin kuvveti olan (1, 2, 4, 8, ...) konumlara yerleştirilir.
-   Her parite biti, kontrol ettiği pozisyonlardaki '1' bitlerinin **XOR (dışlamalı VEYA)** işlemi ile hesaplanır.

#### Hata Tespiti ve Düzeltme
-   Alınan (hatalı olabilecek) kelime üzerinden parite bitleri yeniden hesaplanır.
-   Bu yeni hesaplanan parite bitlerinin, alınan kelimedeki orijinal parite bitleriyle XOR'lanması sonucu **sendrom kelimesi** elde edilir.
-   Sendromun yorumlanması, yukarıda açıklanan modlara göre yapılır.
