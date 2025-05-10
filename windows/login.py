from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QCheckBox, QCompleter, QHBoxLayout)
from PyQt5.QtCore import Qt, QCoreApplication, QStringListModel, QEvent, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from windows.main_menu import MainMenuWindow
from windows.kullanici.sifremi_unuttum import SifremiUnuttumWindow
from windows.kullanici.kayit_ol import KayitOlWindow
from windows.config import APP_STYLE
from datetime import datetime

class LoginWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Fatura Takip Sistemi")
        self.resize(900, 600)
        self.center()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QLabel {
                color: #1a1a1a;
            }
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
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
            }
            QCheckBox {
                font-size: 13px;
                color: #666666;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)

        # Ana widget
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Sol taraf - Görsel ve başlık
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setStyleSheet("""
            QWidget {
                background-color: #1F3A93;
                border-radius: 15px;
            }
        """)
        left_widget.setFixedWidth(400)

        # Logo ve başlık
        title_label = QLabel("Fatura Takip\nSistemi")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        left_layout.addWidget(title_label)

        # Alt başlık
        subtitle_label = QLabel("Faturalarınızı kolayca yönetin")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #ffffff; opacity: 0.8;")
        left_layout.addWidget(subtitle_label)

        left_layout.addStretch()
        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget)

        # Sağ taraf - Giriş formu
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
            }
        """)
        right_layout.setContentsMargins(40, 40, 40, 40)
        right_layout.setSpacing(20)

        # Hoş geldiniz mesajı
        welcome_label = QLabel("Hoş Geldiniz")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setStyleSheet("color: #1F3A93; margin-bottom: 10px;")
        right_layout.addWidget(welcome_label)

        # Giriş formu
        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı")
        self.kullanici_adi_input.setMinimumHeight(45)
        self.kullanici_adi_input.installEventFilter(self)
        right_layout.addWidget(self.kullanici_adi_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.installEventFilter(self)
        right_layout.addWidget(self.password_input)

        # Beni hatırla ve şifremi unuttum satırı
        bottom_row = QHBoxLayout()
        self.remember_me = QCheckBox("Beni Hatırla")
        bottom_row.addWidget(self.remember_me)
        
        self.forgot_password_button = QPushButton("Şifremi Unuttum")
        self.forgot_password_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #1F3A93;
                text-decoration: underline;
                font-size: 13px;
            }
            QPushButton:hover {
                color: #2c4db3;
            }
        """)
        self.forgot_password_button.clicked.connect(self.show_forgot_password)
        bottom_row.addWidget(self.forgot_password_button)
        right_layout.addLayout(bottom_row)

        # Giriş yap butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setMinimumHeight(45)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #1F3A93;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2c4db3;
            }
        """)
        self.login_button.clicked.connect(self.login)
        right_layout.addWidget(self.login_button)

        # Kayıt ol butonu
        self.kayit_ol_button = QPushButton("Hesabınız yok mu? Kayıt olun")
        self.kayit_ol_button.setMinimumHeight(45)
        self.kayit_ol_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1F3A93;
                border: 2px solid #1F3A93;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1F3A93;
                color: white;
            }
        """)
        self.kayit_ol_button.clicked.connect(self.kayit_ol)
        right_layout.addWidget(self.kayit_ol_button)

        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget)

        self.setCentralWidget(main_widget)
        
        # Son giriş bilgilerini yükle
        self.load_last_login()
        
        # Hayali metin için değişkenler
        self.ghost_username = ""
        self.ghost_password = ""
        self.is_ghost_text = False

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            if (obj == self.kullanici_adi_input or obj == self.password_input) and not self.is_ghost_text:
                # Son giriş bilgilerini al
                last_login = self.db.son_giris_bilgilerini_al()
                if last_login and last_login["beni_hatirla"]:
                    # Hayali metin olarak göster
                    self.ghost_username = last_login["kullanici_adi"]
                    self.ghost_password = last_login["sifre"]
                    
                    # Hayali metin stilini ayarla
                    ghost_style = "color: #999999;"
                    self.kullanici_adi_input.setStyleSheet(ghost_style)
                    self.password_input.setStyleSheet(ghost_style)
                    
                    # Hayali metni göster
                    self.kullanici_adi_input.setText(self.ghost_username)
                    self.password_input.setText(self.ghost_password)
                    
                    # Tıklama olayını dinle
                    self.kullanici_adi_input.mousePressEvent = self.on_input_click
                    self.password_input.mousePressEvent = self.on_input_click
                    
        return super().eventFilter(obj, event)

    def on_input_click(self, event):
        # Tıklandığında hayali metni gerçek metin yap
        if not self.is_ghost_text:
            # Metin rengini siyah yap
            self.kullanici_adi_input.setStyleSheet("color: #000000;")
            self.password_input.setStyleSheet("color: #000000;")
            
            # Bilgileri kalıcı olarak doldur
            self.kullanici_adi_input.setText(self.ghost_username)
            self.password_input.setText(self.ghost_password)
            
            # Hayali metin durumunu güncelle
            self.is_ghost_text = True
            
            # Tıklama olayını kaldır
            self.kullanici_adi_input.mousePressEvent = None
            self.password_input.mousePressEvent = None
            
        # Orijinal mousePressEvent'i çağır
        QLineEdit.mousePressEvent(self.kullanici_adi_input, event)

    def load_last_login(self):
        # Son giriş bilgilerini kontrol et
        last_login = self.db.son_giris_bilgilerini_al()
        if last_login and last_login["beni_hatirla"]:
            # Sadece beni hatırla checkbox'ını işaretle
            self.remember_me.setChecked(True)

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        kullanici_adi = self.kullanici_adi_input.text().strip()
        password = self.password_input.text().strip()

        # Varsayılan kullanıcı kontrolü
        if kullanici_adi == "user" and password == "1234":
            user = self.db.get_kullanici_by_credentials(kullanici_adi, password)
            if not user:
                # Varsayılan kullanıcı yoksa oluştur
                try:
                    self.db.kullanici_ekle("name", "surname", f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com", "user", "1234")
                    user = self.db.get_kullanici_by_credentials(kullanici_adi, password)
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Varsayılan kullanıcı oluşturulurken bir hata oluştu: {str(e)}")
                    return

        # Normal giriş kontrolü
        else:
            user = self.db.get_kullanici_by_credentials(kullanici_adi, password)

        if user:
            # Beni hatırla seçeneği işaretliyse bilgileri kaydet
            if self.remember_me.isChecked():
                self.db.son_giris_kaydet(kullanici_adi, password, True)
            else:
                self.db.son_giris_kaydet("", "", False)
                
            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
            self.main_menu_window = MainMenuWindow(self.db, user["id"])
            self.main_menu_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")

    def kayit_ol(self):
        self.kayit_window = KayitOlWindow(self.db)
        self.kayit_window.show()

    def show_forgot_password(self):
        """Şifremi unuttum penceresini göster"""
        self.forgot_password_window = SifremiUnuttumWindow(self.db)
        self.forgot_password_window.show()

    def forgot_password_button_clicked(self):
        """Şifremi unuttum butonuna tıklandığında"""
        self.show_forgot_password()