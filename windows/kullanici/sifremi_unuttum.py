from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
                            QPushButton, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont, QIcon

class SifremiUnuttumWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Şifre Sıfırlama")
        self.resize(400, 200)
        self.center()
        self.setup_styles()
        self.create_main_widgets()

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a237e, stop:1 #0d47a1);
            }
            QWidget#main_card {
                background-color: #fff;
                border-radius: 28px;
                min-width: 600px;
                min-height: 500px;
                max-width: 800px;
                margin: 20px auto;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            }
            QLabel#title {
                color: #1a237e;
                font-family: Arial;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 12px;
            }
            QLabel#subtitle {
                color: #424242;
                font-family: Arial;
                font-size: 16px;
                margin-bottom: 24px;
            }
            QLineEdit {
                font-size: 14px;
                border-radius: 8px;
                padding: 12px;
                border: 2px solid #e0e0e0;
                background: white;
                margin-bottom: 12px;
                min-height: 36px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #1a237e;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                min-width: 200px;
                min-height: 44px;
                border: none;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            QPushButton:hover {
                background-color: #283593;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            QPushButton:pressed {
                background-color: #0d47a1;
                transform: translateY(0px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            QPushButton#ana_menu {
                background-color: #c62828;
                margin-top: 32px;
            }
            QPushButton#ana_menu:hover {
                background-color: #d32f2f;
            }
            QPushButton#ana_menu:pressed {
                background-color: #b71c1c;
            }
        """)

    def create_main_widgets(self):
        # Ana kart oluşturma
        main_card = QWidget()
        main_card.setObjectName("main_card")
        
        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setAlignment(Qt.AlignTop)

        # Başlık ve açıklama
        self.title_label = QLabel("Şifre Sıfırlama")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("E-posta adresinizi girin.")
        self.subtitle_label.setObjectName("subtitle")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.subtitle_label)

        # E-posta widget'ı
        self.email_widget = QWidget()
        email_layout = QVBoxLayout()
        
        # E-posta girişi
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta Adresi")
        email_layout.addWidget(self.email_input)

        # E-posta doğrulama butonu
        self.email_dogrula_button = QPushButton("E-postayı Doğrula")
        self.email_dogrula_button.clicked.connect(self.email_dogrula)
        email_layout.addWidget(self.email_dogrula_button)

        self.email_widget.setLayout(email_layout)
        main_layout.addWidget(self.email_widget)

        # Şifre widget'ı (başlangıçta gizli)
        self.sifre_widget = QWidget()
        sifre_layout = QVBoxLayout()
        
        # Yeni şifre girişi
        self.yeni_sifre_input = QLineEdit()
        self.yeni_sifre_input.setPlaceholderText("Yeni Şifre")
        self.yeni_sifre_input.setEchoMode(QLineEdit.Password)
        sifre_layout.addWidget(self.yeni_sifre_input)

        # Şifre tekrarı
        self.sifre_tekrar_input = QLineEdit()
        self.sifre_tekrar_input.setPlaceholderText("Yeni Şifre (Tekrar)")
        self.sifre_tekrar_input.setEchoMode(QLineEdit.Password)
        sifre_layout.addWidget(self.sifre_tekrar_input)

        # Şifre sıfırlama butonu
        self.sifre_sifirla_button = QPushButton("Şifreyi Kaydet")
        self.sifre_sifirla_button.clicked.connect(self.sifre_sifirla)
        sifre_layout.addWidget(self.sifre_sifirla_button)

        self.sifre_widget.setLayout(sifre_layout)
        self.sifre_widget.hide()  # Başlangıçta gizli
        main_layout.addWidget(self.sifre_widget)

        # Ana menü butonu
        self.ana_menu_button = QPushButton("Ana Menüye Dön")
        self.ana_menu_button.setObjectName("ana_menu")
        self.ana_menu_button.clicked.connect(self.close)
        main_layout.addWidget(self.ana_menu_button)

        main_card.setLayout(main_layout)
        self.setCentralWidget(main_card)

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def email_dogrula(self):
        """E-posta doğrulama işlemi"""
        email = self.email_input.text().strip()
        
        if not email:
            QMessageBox.warning(self, "Hata", "Lütfen e-posta adresinizi girin!")
            return

        # E-posta ile kullanıcıyı kontrol et
        kullanici = self.db.get_user_by_email(email)
        if kullanici:
            # E-posta doğruysa e-posta widget'ını gizle, şifre widget'ını göster
            self.email_widget.hide()
            self.sifre_widget.show()
            self.title_label.setText("Yeni Şifre Belirleme")
            self.subtitle_label.setText("Lütfen yeni şifrenizi belirleyin.")
            QMessageBox.information(self, "Başarılı", "E-posta doğrulandı. Lütfen yeni şifrenizi belirleyin.")
        else:
            QMessageBox.warning(self, "Hata", "Bu e-posta adresi ile kayıtlı kullanıcı bulunamadı!")

    def sifre_sifirla(self):
        """Şifre sıfırlama işlemi"""
        yeni_sifre = self.yeni_sifre_input.text()
        sifre_tekrar = self.sifre_tekrar_input.text()
        email = self.email_input.text().strip()

        if not all([yeni_sifre, sifre_tekrar]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        if yeni_sifre != sifre_tekrar:
            QMessageBox.warning(self, "Hata", "Girdiğiniz şifreler eşleşmiyor!")
            return

        # Şifreyi güncelle
        if self.db.reset_password(email, yeni_sifre):
            QMessageBox.information(self, "Başarılı", 
                "Şifreniz başarıyla güncellendi!\n\nYeni şifrenizle giriş yapabilirsiniz.")
            self.close()
        else:
            QMessageBox.critical(self, "Hata", "Şifre güncelleme işlemi başarısız oldu!") 