from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
from windows.config import APP_STYLE

class SifremiUnuttumWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifremi Unuttum")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet(APP_STYLE)

        sifremi_unuttum_page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Şifrenizi sıfırlamak için kayıtlı kullanıcı adınızı girin:"))
        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adınız")
        layout.addWidget(self.kullanici_adi_input)

        self.gonder_button = QPushButton("Şifre Sıfırlama Linki Gönder")
        self.gonder_button.clicked.connect(self.sifre_sifirlama_gonder)
        layout.addWidget(self.gonder_button)

        self.bilgi_label = QLabel("")
        layout.addWidget(self.bilgi_label)

        self.kapat_button = QPushButton("Kapat")
        self.kapat_button.clicked.connect(self.close)
        layout.addWidget(self.kapat_button)

        sifremi_unuttum_page.setLayout(layout)
        self.setCentralWidget(sifremi_unuttum_page)

    def sifre_sifirlama_gonder(self):
        kullanici_adi = self.kullanici_adi_input.text()
        if not kullanici_adi:
            QMessageBox.warning(self, "Hata", "Lütfen kullanıcı adınızı giriniz!")
            return
        self.bilgi_label.setText(f"{kullanici_adi} kullanıcı adına şifre sıfırlama linki gönderildi!")
        QTimer.singleShot(3000, self.close) 