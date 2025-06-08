import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFrame, QGridLayout, QTabWidget)
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp

#hesaplamaların yapıldığı fonksiyonlar
def p_sayisi_hesapla(k):
    #gerekli parite biti sayısını hesaplar
    p = 0
    while 2 ** p < k + p + 1:
        p += 1
    return p
def sec_kodla(veri_bitleri):
    #verilen veriyi sec koduna çevirir
    k = len(veri_bitleri)
    p = p_sayisi_hesapla(k)
    n = k + p
    sec_word = [None] * n
    parite_pozisyonlari = {2 ** i for i in range(p)}
    veri_idx = 0
    for i in range(n, 0, -1):
        if i not in parite_pozisyonlari:
            sec_word[n - i] = veri_bitleri[veri_idx]
            veri_idx += 1
    for parite_derecesi in range(p):
        parite_pos = 2 ** parite_derecesi
        xor_sum = 0
        for i in range(1, n + 1):
            if i & parite_pos and i != parite_pos:
                if sec_word[n - i] == '1':
                    xor_sum ^= 1
        sec_word[n - parite_pos] = str(xor_sum)
    return "".join(sec_word)
def sec_coz(alinan_kelime):
    #sec kodundaki hatayı bulur ve düzeltir
    n = len(alinan_kelime)
    p = 0
    while 2 ** p < n + 1:
        p += 1
    sendrom = 0
    for parite_derecesi in range(p):
        parite_pos = 2 ** parite_derecesi
        xor_sum = 0
        for i in range(1, n + 1):
            if i & parite_pos:
                if alinan_kelime[n - i] == '1':
                    xor_sum ^= 1
        if xor_sum != 0:
            sendrom += parite_pos
    duzeltilmis_kelime = list(alinan_kelime)
    if sendrom == 0:
        analiz = "Hata bulunamadı."
    else:
        analiz = f"Tek bit hatası bulundu: Pozisyon {sendrom}. Hata düzeltildi."
        hata_index = n - sendrom
        if 0 <= hata_index < n:
            duzeltilmis_kelime[hata_index] = '1' if duzeltilmis_kelime[hata_index] == '0' else '0'
    return analiz, bin(sendrom)[2:].zfill(p), "".join(duzeltilmis_kelime)
def secded_kodla(veri_bitleri):
    #verilen veriyi sec-ded koduna çevirir
    sec_kodu = sec_kodla(veri_bitleri)
    return sec_kodu + str(sec_kodu.count('1') % 2)
def secded_coz(alinan_kelime):
    #sec-ded kodundaki hatayı analiz eder
    n_secded = len(alinan_kelime)
    p = 0
    while 2 ** p < n_secded:
        p += 1
    n_sec = n_secded - 1
    sec_kismi = alinan_kelime[:n_sec]
    gelen_genel_parite = int(alinan_kelime[n_sec])
    _, sendrom_str, _ = sec_coz(sec_kismi)
    sendrom = int(sendrom_str, 2)
    hesaplanan_genel_parite = sec_kismi.count('1') % 2
    parite_kontrol = hesaplanan_genel_parite ^ gelen_genel_parite
    duzeltilmis_kelime = list(alinan_kelime)
    if sendrom == 0 and parite_kontrol == 0:
        analiz = "Hata bulunamadı."
    elif sendrom != 0 and parite_kontrol == 1:
        analiz = f"Tek bit hatası bulundu: Pozisyon {sendrom}. Hata düzeltildi."
        hata_index = n_sec - sendrom
        if 0 <= hata_index < n_sec:
            duzeltilmis_kelime[hata_index] = '1' if duzeltilmis_kelime[hata_index] == '0' else '0'
    elif sendrom != 0 and parite_kontrol == 0:
        analiz = "Çift bit hatası tespit edildi (Düzeltilemez)."
        return analiz, bin(sendrom)[2:].zfill(p), alinan_kelime
    elif sendrom == 0 and parite_kontrol == 1:
        analiz = f"Tek bit hatası bulundu: Genel Parite Biti (Pozisyon {n_secded}). Hata düzeltildi."
        duzeltilmis_kelime[n_secded - 1] = str(hesaplanan_genel_parite)
    else:
        analiz = "Analiz hatası"
        return analiz, "N/A", alinan_kelime
    return analiz, bin(sendrom)[2:].zfill(p), "".join(duzeltilmis_kelime)
#arayüz sınıfı
class HammingSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.Ui()
    def Ui(self):
        #ana pencere ve sekmeli yapı oluşturulur
        self.setWindowTitle('Hamming Kod Simülatörü')
        self.setGeometry(100, 100, 950, 600)
        self.setStyleSheet("font-size: 11pt;")
        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        self.sec_ekrani()
        self.secded_ekrani()
    def sec_ekrani(self):
        #sec modu için sekme arayüzü oluşturulur
        self.tab_sec = QWidget()
        self.tabs.addTab(self.tab_sec, "SEC (Tek Hata Düzeltme)")
        layout = QVBoxLayout(self.tab_sec)
        grup_giris = self.input_bolumu(self.sec_hesapla)
        self.boyut_secici_sec = grup_giris["boyut"]
        self.veri_giris_kutusu_sec = grup_giris["veri"]
        layout.addWidget(grup_giris["widget"])
        self.orijinal_kod_sec = QLineEdit()
        self.orijinal_kod_sec.setReadOnly(True)
        self.orijinal_kod_sec.setFont(QFont("Courier", 11))
        layout.addWidget(QLabel("<b>Bellekteki Kodlanmış Kelime:</b>"))
        layout.addWidget(self.orijinal_kod_sec)
        self.hata_pozisyon_sec = QLineEdit()
        self.hata_pozisyon_sec.setPlaceholderText("Örn: 5 (1-tabanlı, sağdan)")
        self.kontrol_et_butonu_sec = QPushButton("Hata Oluştur ve Kontrol Et")
        hata_layout = QHBoxLayout()
        hata_layout.addWidget(QLabel("<b>Hata Pozisyonu:</b>"))
        hata_layout.addWidget(self.hata_pozisyon_sec)
        hata_layout.addWidget(self.kontrol_et_butonu_sec)
        layout.addLayout(hata_layout)
        grup_sonuc = self.cikis_bolumu()
        self.sonuc_okunan_sec = grup_sonuc["okunan"]
        self.sonuc_sendrom_sec = grup_sonuc["sendrom"]
        self.sonuc_analiz_sec = grup_sonuc["analiz"]
        self.sonuc_duzeltilmis_sec = grup_sonuc["duzeltilmis"]
        layout.addWidget(grup_sonuc["widget"])
        self.kontrol_et_butonu_sec.clicked.connect(self.sec_kontrol)
        self.boyut_secici_sec.currentIndexChanged.connect(lambda: self.veri_girisi_guncelle(self.boyut_secici_sec, self.veri_giris_kutusu_sec, self.tab_sec))
        self.veri_girisi_guncelle(self.boyut_secici_sec, self.veri_giris_kutusu_sec, self.tab_sec)
    def secded_ekrani(self):
        #sec-ded modu için sekme arayüzü oluşturulur
        self.tab_secded = QWidget()
        self.tabs.addTab(self.tab_secded, "SEC-DED (Çift Hata Tespiti)")
        layout = QVBoxLayout(self.tab_secded)
        grup_giris = self.input_bolumu(self.secded_hesapla)
        self.boyut_secici_secded = grup_giris["boyut"]
        self.veri_giris_kutusu_secded = grup_giris["veri"]
        layout.addWidget(grup_giris["widget"])
        self.orijinal_kod_secded = QLineEdit()
        self.orijinal_kod_secded.setReadOnly(True)
        self.orijinal_kod_secded.setFont(QFont("Courier", 11))
        layout.addWidget(QLabel("<b>Bellekteki Kodlanmış Kelime:</b>"))
        layout.addWidget(self.orijinal_kod_secded)
        self.hata_pozisyon_1_secded = QLineEdit()
        self.hata_pozisyon_1_secded.setPlaceholderText("Örn: 3")
        self.hata_pozisyon_2_secded = QLineEdit()
        self.hata_pozisyon_2_secded.setPlaceholderText("Örn: 7")
        self.kontrol_et_butonu_secded = QPushButton("Hata Oluştur ve Kontrol Et")
        hata_layout = QHBoxLayout()
        hata_layout.addWidget(QLabel("<b>1. Hata Pozisyonu:</b>"))
        hata_layout.addWidget(self.hata_pozisyon_1_secded)
        hata_layout.addWidget(QLabel("<b>2. Hata Pozisyonu:</b>"))
        hata_layout.addWidget(self.hata_pozisyon_2_secded)
        hata_layout.addWidget(self.kontrol_et_butonu_secded)
        layout.addLayout(hata_layout)
        grup_sonuc = self.cikis_bolumu()
        self.sonuc_okunan_secded = grup_sonuc["okunan"]
        self.sonuc_sendrom_secded = grup_sonuc["sendrom"]
        self.sonuc_analiz_secded = grup_sonuc["analiz"]
        self.sonuc_duzeltilmis_secded = grup_sonuc["duzeltilmis"]
        layout.addWidget(grup_sonuc["widget"])
        self.kontrol_et_butonu_secded.clicked.connect(self.secded_kontrol)
        self.boyut_secici_secded.currentIndexChanged.connect(lambda: self.veri_girisi_guncelle(self.boyut_secici_secded, self.veri_giris_kutusu_secded, self.tab_secded))
        self.veri_girisi_guncelle(self.boyut_secici_secded, self.veri_giris_kutusu_secded, self.tab_secded)
    def input_bolumu(self, hesapla_fonksiyonu):
        #tekrarı önlemek için ortak giriş paneli oluşturur
        widget = QWidget()
        layout = QVBoxLayout(widget)
        ust_layout = QHBoxLayout()
        boyut_secici = QComboBox()
        boyut_secici.addItems(['8-bit', '16-bit', '32-bit'])
        veri_giris_kutusu = QLineEdit()
        hesapla_butonu = QPushButton("Kodu Hesapla ve Belleğe Yaz")
        ust_layout.addWidget(QLabel("<b>Veri Boyutu:</b>"))
        ust_layout.addWidget(boyut_secici)
        ust_layout.addWidget(QLabel("<b>Veri (Binary):</b>"))
        ust_layout.addWidget(veri_giris_kutusu)
        layout.addLayout(ust_layout)
        layout.addWidget(hesapla_butonu)
        hesapla_butonu.clicked.connect(hesapla_fonksiyonu)
        return {"widget": widget, "boyut": boyut_secici, "veri": veri_giris_kutusu}
    def cikis_bolumu(self):
        #tekrarı önlemek için ortak sonuç paneli oluşturur
        widget = QFrame()
        widget.setFrameShape(QFrame.StyledPanel)
        layout = QGridLayout(widget)
        okunan = QLineEdit()
        okunan.setReadOnly(True)
        okunan.setFont(QFont("Courier", 11))
        sendrom = QLineEdit()
        sendrom.setReadOnly(True)
        analiz = QLineEdit()
        analiz.setReadOnly(True)
        duzeltilmis = QLineEdit()
        duzeltilmis.setReadOnly(True)
        duzeltilmis.setFont(QFont("Courier", 11))
        layout.addWidget(QLabel("Hatalı Kelime:"), 0, 0)
        layout.addWidget(okunan, 0, 1)
        layout.addWidget(QLabel("Sendrom Kelimesi (Binary):"), 1, 0)
        layout.addWidget(sendrom, 1, 1)
        layout.addWidget(QLabel("<b>Hata Analizi Sonucu:</b>"), 2, 0)
        layout.addWidget(analiz, 2, 1)
        layout.addWidget(QLabel("<b>Düzeltilmiş Kod Kelimesi:</b>"), 3, 0)
        layout.addWidget(duzeltilmis, 3, 1)
        return {"widget": widget, "okunan": okunan, "sendrom": sendrom, "analiz": analiz, "duzeltilmis": duzeltilmis}
    def veri_girisi_guncelle(self, boyut_secici, veri_giris_kutusu, tab_widget):
        #veri giriş kutusunu seçilen boyuta göre günceller
        boyut_str = boyut_secici.currentText()
        boyut = int(boyut_str.replace('-bit', ''))
        validator = QRegExpValidator(QRegExp("[01]*"))
        veri_giris_kutusu.setValidator(validator)
        veri_giris_kutusu.setMaxLength(boyut)
        self.alanlari_temizle(tab_widget)
        veri_giris_kutusu.setPlaceholderText(f"{boyut} bitlik binary veri girin")
    def alanlari_temizle(self, tab):
        #ilgili sekmedeki tüm metin kutularını temizler
        for widget in tab.findChildren(QLineEdit):
            widget.clear()
            if widget.isReadOnly():
                widget.setStyleSheet("")
    def sec_hesapla(self):
        #sec modunda kodu hesaplar
        boyut = int(self.boyut_secici_sec.currentText().replace('-bit', ''))
        veri = self.veri_giris_kutusu_sec.text()
        if len(veri) != boyut:
            self.sonuc_analiz_sec.setText("Geçersiz veri uzunluğu!")
            return
        self.alanlari_temizle(self.tab_sec)
        self.veri_giris_kutusu_sec.setText(veri)
        self.orijinal_kod_sec.setText(sec_kodla(veri))
    def secded_hesapla(self):
        #sec-ded modunda kodu hesaplar
        boyut = int(self.boyut_secici_secded.currentText().replace('-bit', ''))
        veri = self.veri_giris_kutusu_secded.text()
        if len(veri) != boyut:
            self.sonuc_analiz_secded.setText("Geçersiz veri uzunluğu!")
            return
        self.alanlari_temizle(self.tab_secded)
        self.veri_giris_kutusu_secded.setText(veri)
        self.orijinal_kod_secded.setText(secded_kodla(veri))
    def sec_kontrol(self):
        #sec modunda hata kontrolü yapar
        orijinal_kod = self.orijinal_kod_sec.text()
        if not orijinal_kod:
            return
        hatali_kelime_list = list(orijinal_kod)
        try:
            poz_str = self.hata_pozisyon_sec.text().strip()
            if poz_str:
                poz = int(poz_str)
                if 1 <= poz <= len(hatali_kelime_list):
                    idx = len(hatali_kelime_list) - poz
                    hatali_kelime_list[idx] = '1' if hatali_kelime_list[idx] == '0' else '0'
        except ValueError:
            self.sonuc_analiz_sec.setText("Geçersiz pozisyon girişi!")
            return
        hatali_kelime = "".join(hatali_kelime_list)
        self.sonuc_okunan_sec.setText(hatali_kelime)
        analiz, sendrom, duzeltilmis = sec_coz(hatali_kelime)
        self.sonuc_sendrom_sec.setText(sendrom)
        self.sonuc_analiz_sec.setText(analiz)
        self.sonuc_duzeltilmis_sec.setText(duzeltilmis)
        self.renklendir_sonuc(self.sonuc_analiz_sec, analiz)
    def secded_kontrol(self):
        #sec-ded modunda hata kontrolü yapar
        orijinal_kod = self.orijinal_kod_secded.text()
        if not orijinal_kod:
            return
        hatali_kelime_list = list(orijinal_kod)
        pozisyonlar = []
        try:
            poz_str_1 = self.hata_pozisyon_1_secded.text().strip()
            if poz_str_1:
                pozisyonlar.append(int(poz_str_1))
            poz_str_2 = self.hata_pozisyon_2_secded.text().strip()
            if poz_str_2:
                pozisyonlar.append(int(poz_str_2))
            for poz in set(pozisyonlar):
                if 1 <= poz <= len(hatali_kelime_list):
                    idx = len(hatali_kelime_list) - poz
                    hatali_kelime_list[idx] = '1' if hatali_kelime_list[idx] == '0' else '0'
        except ValueError:
            self.sonuc_analiz_secded.setText("Geçersiz pozisyon girişi!")
            return
        hatali_kelime = "".join(hatali_kelime_list)
        self.sonuc_okunan_secded.setText(hatali_kelime)
        analiz, sendrom, duzeltilmis = secded_coz(hatali_kelime)
        self.sonuc_sendrom_secded.setText(sendrom)
        self.sonuc_analiz_secded.setText(analiz)
        self.sonuc_duzeltilmis_secded.setText(duzeltilmis)
        self.renklendir_sonuc(self.sonuc_analiz_secded, analiz)
    def renklendir_sonuc(self, analiz_kutusu, analiz_metni):
        #analiz sonucuna göre arayüzü renklendirir
        if "Hata bulunamadı" in analiz_metni:
            analiz_kutusu.setStyleSheet("background-color: lightgreen;")
        elif "düzeltildi" in analiz_metni:
            analiz_kutusu.setStyleSheet("background-color: orange;")
        elif "Düzeltilemez" in analiz_metni:
            analiz_kutusu.setStyleSheet("background-color: lightcoral;")
        else:
            analiz_kutusu.setStyleSheet("")
if __name__ == '__main__':
    #uygulama başlangıç noktası
    app = QApplication(sys.argv)
    sim = HammingSimulator()
    sim.show()
    sys.exit(app.exec_())
