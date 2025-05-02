from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
from windows.config import APP_STYLE

class AyarlarWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Ayarlar")
        self.setGeometry(100, 100, 400, 550)
        self.setStyleSheet(APP_STYLE)

        ayarlar_page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Kullanıcı Bilgileri:"))
        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Ad")
        layout.addWidget(self.ad_input)

        self.soyad_input = QLineEdit()
        self.soyad_input.setPlaceholderText("Soyad")
        layout.addWidget(self.soyad_input)

        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı")
        layout.addWidget(self.kullanici_adi_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta")
        layout.addWidget(self.email_input)

        self.load_kullanici_bilgileri()

        layout.addWidget(QLabel("Şifre Değiştir:"))
        self.eski_sifre_input = QLineEdit()
        self.eski_sifre_input.setPlaceholderText("Eski Şifre")
        self.eski_sifre_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.eski_sifre_input)

        self.yeni_sifre_input = QLineEdit()
        self.yeni_sifre_input.setPlaceholderText("Yeni Şifre")
        self.yeni_sifre_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.yeni_sifre_input)

        self.yeni_sifre_tekrar_input = QLineEdit()
        self.yeni_sifre_tekrar_input.setPlaceholderText("Yeni Şifre (Tekrar)")
        self.yeni_sifre_tekrar_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.yeni_sifre_tekrar_input)

        self.sifre_degistir_button = QPushButton("Şifreyi Değiştir")
        self.sifre_degistir_button.clicked.connect(self.sifre_degistir)
        layout.addWidget(self.sifre_degistir_button)

        layout.addWidget(QLabel("Bildirim Ayarları:"))
        self.bildirim_checkbox = QCheckBox("Fatura hatırlatıcıları almak istiyorum")
        self.bildirim_checkbox.setChecked(True)
        layout.addWidget(self.bildirim_checkbox)

        self.hatirlatma_gun_input = QLineEdit()
        self.hatirlatma_gun_input.setPlaceholderText("Ödeme tarihinden kaç gün önce hatırlatılsın?")
        self.hatirlatma_gun_input.setText("3")
        layout.addWidget(self.hatirlatma_gun_input)

        self.ayarlari_kaydet_button = QPushButton("Ayarları Kaydet")
        self.ayarlari_kaydet_button.clicked.connect(self.ayarlari_kaydet)
        layout.addWidget(self.ayarlari_kaydet_button)

        self.ana_menu_button = QPushButton("Ana Menüye Dön")
        self.ana_menu_button.clicked.connect(self.close)
        layout.addWidget(self.ana_menu_button)

        ayarlar_page.setLayout(layout)
        self.setCentralWidget(ayarlar_page)

    def load_kullanici_bilgileri(self):
        user_info = self.db.get_kullanici_bilgileri()
        if user_info:
            self.ad_input.setText(user_info["ad"])
            self.soyad_input.setText(user_info["soyad"])
            self.kullanici_adi_input.setText(user_info["kullanici_adi"])
            self.email_input.setText(user_info["email"])

    def sifre_degistir(self):
        eski_sifre = self.eski_sifre_input.text()
        yeni_sifre = self.yeni_sifre_input.text()
        yeni_sifre_tekrar = self.yeni_sifre_tekrar_input.text()
        user_info = self.db.get_kullanici_bilgileri()
        if not user_info or eski_sifre != user_info["sifre"]:
            QMessageBox.warning(self, "Hata", "Eski şifre yanlış!")
            return
        if yeni_sifre != yeni_sifre_tekrar:
            QMessageBox.warning(self, "Hata", "Yeni şifreler uyuşmuyor!")
            return
        if len(yeni_sifre) < 4:
            QMessageBox.warning(self, "Hata", "Yeni şifre en az 4 karakter olmalıdır!")
            return
        self.db.update_kullanici_sifre(yeni_sifre)
        QMessageBox.information(self, "Başarılı", "Şifre başarıyla değiştirildi!")
        self.eski_sifre_input.clear()
        self.yeni_sifre_input.clear()
        self.yeni_sifre_tekrar_input.clear()

    def ayarlari_kaydet(self):
        ad = self.ad_input.text()
        soyad = self.soyad_input.text()
        kullanici_adi = self.kullanici_adi_input.text()
        email = self.email_input.text()
        if not ad or not soyad or not kullanici_adi or not email:
            QMessageBox.warning(self, "Hata", "Lütfen tüm kullanıcı bilgilerini doldurun!")
            return
        self.db.update_kullanici_bilgileri(ad, soyad, kullanici_adi, email)
        QMessageBox.information(self, "Başarılı", "Ayarlar kaydedildi!")
