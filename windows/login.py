from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont
from windows.main_menu import MainMenuWindow
from windows.kullanici.sifremi_unuttum import SifremiUnuttumWindow
from windows.config import APP_STYLE

class LoginWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Giriş Sayfası")
        self.resize(420, 340)
        self.center()
        self.setStyleSheet(APP_STYLE)

        login_page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(18)

        self.title_label = QLabel("Fatura Takip Sistemi")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 22, QFont.Bold))
        self.title_label.setStyleSheet("color: #1F3A93; margin-bottom: 10px;")
        layout.addWidget(self.title_label)

        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı")
        self.kullanici_adi_input.setMinimumHeight(36)
        layout.addWidget(self.kullanici_adi_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(36)
        layout.addWidget(self.password_input)

        self.remember_me = QCheckBox("Beni Hatırla")
        layout.addWidget(self.remember_me)

        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setMinimumHeight(38)
        self.login_button.setStyleSheet("font-size: 15px; font-weight: bold; background-color: #1F3A93; color: white; border-radius: 8px;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.forgot_password_button = QPushButton("Şifremi Unuttum")
        self.forgot_password_button.setStyleSheet(
            "background-color: transparent; border: none; color: #8B0000; text-decoration: underline; font-size: 13px;")
        self.forgot_password_button.clicked.connect(self.show_forgot_password)
        layout.addWidget(self.forgot_password_button)

        login_page.setLayout(layout)
        self.setCentralWidget(login_page)

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        kullanici_adi = self.kullanici_adi_input.text()
        password = self.password_input.text()
        user = self.db.get_kullanici_by_credentials(kullanici_adi, password)
        if user:
            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
            self.main_menu_window = MainMenuWindow(self.db)
            self.main_menu_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")

    def show_forgot_password(self):
        self.forgot_password_window = SifremiUnuttumWindow()
        self.forgot_password_window.show()