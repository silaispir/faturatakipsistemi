from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont
from windows.config import APP_STYLE

class KayitOlWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Kayıt Ol")
        self.resize(500, 650)
        self.center()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QLabel {
                color: #1a1a1a;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #e1e1e1;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #1F3A93;
            }
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                background-color: #1F3A93;
                color: white;
                border: none;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #1A3278;
            }
            QPushButton:pressed {
                background-color: #142865;
            }
        """)

        kayit_page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(40, 30, 40, 30)

        self.title_label = QLabel("Yeni Hesap Oluştur")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 22, QFont.Bold))
        self.title_label.setStyleSheet("color: #1F3A93; margin-bottom: 10px;")
        layout.addWidget(self.title_label)

        # Input alanları
        input_style = """
            QLineEdit {
                padding: 12px;
                border: 2px solid #e1e1e1;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #1F3A93;
            }
        """

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Ad")
        self.ad_input.setMinimumHeight(40)
        self.ad_input.setStyleSheet(input_style)
        layout.addWidget(self.ad_input)

        self.soyad_input = QLineEdit()
        self.soyad_input.setPlaceholderText("Soyad")
        self.soyad_input.setMinimumHeight(40)
        self.soyad_input.setStyleSheet(input_style)
        layout.addWidget(self.soyad_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta")
        self.email_input.setMinimumHeight(40)
        self.email_input.setStyleSheet(input_style)
        layout.addWidget(self.email_input)

        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı")
        self.kullanici_adi_input.setMinimumHeight(40)
        self.kullanici_adi_input.setStyleSheet(input_style)
        layout.addWidget(self.kullanici_adi_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet(input_style)
        layout.addWidget(self.password_input)

        self.password_confirm_input = QLineEdit()
        self.password_confirm_input.setPlaceholderText("Şifre Tekrar")
        self.password_confirm_input.setEchoMode(QLineEdit.Password)
        self.password_confirm_input.setMinimumHeight(40)
        self.password_confirm_input.setStyleSheet(input_style)
        layout.addWidget(self.password_confirm_input)

        # Kayıt butonu
        self.kayit_button = QPushButton("Kayıt Ol")
        self.kayit_button.setMinimumHeight(42)
        self.kayit_button.setStyleSheet("""
            QPushButton {
                background-color: #1F3A93;
                color: white;
                font-weight: bold;
                font-size: 15px;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #1A3278;
            }
            QPushButton:pressed {
                background-color: #142865;
            }
        """)
        self.kayit_button.clicked.connect(self.kayit_ol)
        layout.addWidget(self.kayit_button)

        kayit_page.setLayout(layout)
        self.setCentralWidget(kayit_page)

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def kayit_ol(self):
        ad = self.ad_input.text().strip()
        soyad = self.soyad_input.text().strip()
        email = self.email_input.text().strip()
        kullanici_adi = self.kullanici_adi_input.text().strip()
        password = self.password_input.text()
        password_confirm = self.password_confirm_input.text()

        if not all([ad, soyad, email, kullanici_adi, password, password_confirm]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        if password != password_confirm:
            QMessageBox.warning(self, "Hata", "Şifreler eşleşmiyor!")
            return

        if len(password) < 4:
            QMessageBox.warning(self, "Hata", "Şifre en az 4 karakter olmalıdır!")
            return

        if self.db.kullanici_adi_var_mi(kullanici_adi):
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten kullanılıyor!")
            return

        if self.db.email_var_mi(email):
            QMessageBox.warning(self, "Hata", "Bu e-posta adresi zaten kayıtlı!")
            return

        if self.db.kullanici_ekle(ad, soyad, email, kullanici_adi, password):
            QMessageBox.information(self, "Başarılı", "Kayıt işlemi başarıyla tamamlandı!")
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Kayıt işlemi sırasında bir hata oluştu!")