from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QCheckBox, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QCursor

class AyarlarWindow(QMainWindow):
    def __init__(self, db, current_user_id):
        super().__init__()
        self.db = db
        self.current_user_id = current_user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ayarlar")
        self.resize(800, 900)
        self.center()
        self.setup_styles()

        # Gerekli bileşenleri tanımlayın
        self.ad_input = QLineEdit(self)
        self.soyad_input = QLineEdit(self)
        self.kullanici_adi_input = QLineEdit(self)
        self.email_input = QLineEdit(self)

        # Ana widget'ları oluşturun
        self.create_main_widgets()

        # Kullanıcı bilgilerini yükleyin
        self.kullanici_bilgilerini_yukle()

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3eafc, stop:1 #a8c0ff);
            }
            QWidget#main_card {
                background-color: #fff;
                border-radius: 28px;
                min-width: 700px;
                min-height: 600px;
                max-width: 800px;
                margin: 20px auto;
                box-shadow: 0 8px 32px rgba(31,58,147,0.10);
            }
            QWidget#section_card {
                background-color: #f8fbff;
                border-radius: 16px;
                padding: 24px;
                margin: 16px 0;
                border: 1px solid #e0e0e0;
            }
            QLabel#title {
                color: #1F3A93;
                font-family: Arial;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 12px;
            }
            QLabel#subtitle {
                color: #222;
                font-family: Arial;
                font-size: 16px;
                margin-bottom: 24px;
            }
            QLabel#section_title {
                color: #1F3A93;
                font-family: Arial;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 16px;
            }
          /* Scroll bar stilleri */
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #1F3A93;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
           
          
        """)

    def create_main_widgets(self):
        # Ana kart oluşturma
        main_card = QWidget()
        main_card.setObjectName("main_card")
        
        # Scroll Area oluşturma
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Scroll içeriği için widget
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)  # Bilgi blokları arasındaki boşluk azaltıldı
        main_layout.setContentsMargins(24, 24, 24, 24)  # Kenar boşlukları azaltıldı
        main_layout.setAlignment(Qt.AlignTop)

        # Başlık ve açıklama ekleme
        self.add_title_section(main_layout)
        
        # Profil bilgileri bölümü
        main_layout.addWidget(self.create_profile_section())
        
        # Şifre değiştirme bölümü
        main_layout.addWidget(self.create_password_section())
        
        # Bildirim ayarları bölümü
        main_layout.addWidget(self.create_notification_section())
        
        # Ana menü butonu
        self.add_main_menu_button(main_layout)
        
        scroll_content.setLayout(main_layout)
        scroll.setWidget(scroll_content)
        
        # Ana kart layout
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.addWidget(scroll)
        main_card.setLayout(card_layout)
        
        self.setCentralWidget(main_card)

    def add_title_section(self, layout):
        title_label = QLabel("Ayarlar")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Hesap ayarlarınızı yönetin ve güncelleyin.")
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)

    def create_profile_section(self):
        section = QWidget()
        section.setObjectName("section_card")
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Başlık ve açıklama
        title_container = QWidget()
        title_layout = QVBoxLayout()
        title_layout.setSpacing(8)
        
        title = QLabel("Profil Bilgileri")
        title.setObjectName("section_title")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Kişisel bilgilerinizi güncelleyin")
        subtitle.setStyleSheet("""
            color: #666;
            font-size: 14px;
            margin-bottom: 8px;
        """)
        title_layout.addWidget(subtitle)
        
        title_container.setLayout(title_layout)
        layout.addWidget(title_container)

        # Form container
        form_container = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(16)
        
        # Kullanıcı Adı
        username_container = QWidget()
        username_layout = QVBoxLayout()
        username_layout.setSpacing(4)
        
        username_label = QLabel("Kullanıcı Adı")
        username_label.setStyleSheet("""
            color: #1a237e;
            font-size: 14px;
            font-weight: bold;
        """)
        username_layout.addWidget(username_label)
        
        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı adınızı girin")
        self.kullanici_adi_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
        """)
        username_layout.addWidget(self.kullanici_adi_input)
        username_container.setLayout(username_layout)
        form_layout.addWidget(username_container)

        # Ad
        name_container = QWidget()
        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)
        
        name_label = QLabel("Ad")
        name_label.setStyleSheet("""
            color: #1a237e;
            font-size: 14px;
            font-weight: bold;
        """)
        name_layout.addWidget(name_label)

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Adınızı girin")
        self.ad_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
        """)
        name_layout.addWidget(self.ad_input)
        name_container.setLayout(name_layout)
        form_layout.addWidget(name_container)

        # Soyad
        surname_container = QWidget()
        surname_layout = QVBoxLayout()
        surname_layout.setSpacing(4)
        
        surname_label = QLabel("Soyad")
        surname_label.setStyleSheet("""
            color: #1a237e;
            font-size: 14px;
            font-weight: bold;
        """)
        surname_layout.addWidget(surname_label)

        self.soyad_input = QLineEdit()
        self.soyad_input.setPlaceholderText("Soyadınızı girin")
        self.soyad_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
        """)
        surname_layout.addWidget(self.soyad_input)
        surname_container.setLayout(surname_layout)
        form_layout.addWidget(surname_container)

        # E-posta
        email_container = QWidget()
        email_layout = QVBoxLayout()
        email_layout.setSpacing(4)
        
        email_label = QLabel("E-posta")
        email_label.setStyleSheet("""
            color: #1a237e;
            font-size: 14px;
            font-weight: bold;
        """)
        email_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta adresinizi girin")
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
        """)
        email_layout.addWidget(self.email_input)
        email_container.setLayout(email_layout)
        form_layout.addWidget(email_container)

        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        # Kaydet butonu
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        
        self.profil_guncelle_button = QPushButton("Profil Bilgilerini Kaydet")
        self.profil_guncelle_button.setStyleSheet("""
            QPushButton {
                background-color: #1a237e;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
                min-height: 30px;
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
        """)
        self.profil_guncelle_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.profil_guncelle_button.clicked.connect(self.profil_guncelle)
        button_layout.addWidget(self.profil_guncelle_button)
        
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)
        
        section.setLayout(layout)
        return section

    def create_password_section(self):
        section = QWidget()
        section.setObjectName("section_card")
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Başlık ve açıklama
        title_container = QWidget()
        title_layout = QVBoxLayout()
        title_layout.setSpacing(8)
        
        title = QLabel("Şifre Değiştirme")
        title.setObjectName("section_title")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Hesap güvenliğiniz için şifrenizi güncelleyin")
        subtitle.setStyleSheet("""
            color: #666;
            font-size: 14px;
            margin-bottom: 8px;
        """)
        title_layout.addWidget(subtitle)
        
        title_container.setLayout(title_layout)
        layout.addWidget(title_container)

        # Form container
        form_container = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(16)
        
        # Mevcut Şifre
        current_password_container = QWidget()
        current_password_layout = QVBoxLayout()
        current_password_layout.setSpacing(4)
        
        current_password_label = QLabel("Mevcut Şifre")
        current_password_label.setStyleSheet("""
            color: #1a237e;
            font-size: 14px;
            font-weight: bold;
        """)
        current_password_layout.addWidget(current_password_label)

        self.eski_sifre_input = QLineEdit()
        self.eski_sifre_input.setPlaceholderText("Mevcut şifrenizi girin")
        self.eski_sifre_input.setEchoMode(QLineEdit.Password)
        self.eski_sifre_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
        """)
        current_password_layout.addWidget(self.eski_sifre_input)
        current_password_container.setLayout(current_password_layout)
        form_layout.addWidget(current_password_container)

        # Yeni Şifre
        new_password_container = QWidget()
        new_password_layout = QVBoxLayout()
        new_password_layout.setSpacing(4)
        
        new_password_label = QLabel("Yeni Şifre")
        new_password_label.setStyleSheet("""
            color: #1a237e;
            font-size: 14px;
            font-weight: bold;
        """)
        new_password_layout.addWidget(new_password_label)

        self.yeni_sifre_input = QLineEdit()
        self.yeni_sifre_input.setPlaceholderText("Yeni şifrenizi girin")
        self.yeni_sifre_input.setEchoMode(QLineEdit.Password)
        self.yeni_sifre_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
        """)
        new_password_layout.addWidget(self.yeni_sifre_input)
        new_password_container.setLayout(new_password_layout)
        form_layout.addWidget(new_password_container)

        # Yeni Şifre Tekrar
        confirm_password_container = QWidget()
        confirm_password_layout = QVBoxLayout()
        confirm_password_layout.setSpacing(4)
        
        confirm_password_label = QLabel("Yeni Şifre (Tekrar)")
        confirm_password_label.setStyleSheet("""
            color: #1a237e;
            font-size: 14px;
            font-weight: bold;
        """)
        confirm_password_layout.addWidget(confirm_password_label)

        self.yeni_sifre_tekrar_input = QLineEdit()
        self.yeni_sifre_tekrar_input.setPlaceholderText("Yeni şifrenizi tekrar girin")
        self.yeni_sifre_tekrar_input.setEchoMode(QLineEdit.Password)
        self.yeni_sifre_tekrar_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
        """)
        confirm_password_layout.addWidget(self.yeni_sifre_tekrar_input)
        confirm_password_container.setLayout(confirm_password_layout)
        form_layout.addWidget(confirm_password_container)

        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        # Kaydet butonu
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        
        self.sifre_degistir_button = QPushButton("Şifreyi Güncelle")
        self.sifre_degistir_button.setStyleSheet("""
            QPushButton {
                background-color: #1a237e;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 30px;
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
        """)
        self.sifre_degistir_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.sifre_degistir_button.clicked.connect(self.sifre_degistir)
        button_layout.addWidget(self.sifre_degistir_button)
        
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)
        
        section.setLayout(layout)
        return section

    def create_notification_section(self):
        section = QWidget()
        section.setObjectName("section_card")
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        title = QLabel("Bildirim Ayarları")
        title.setObjectName("section_title")
        layout.addWidget(title)

        # Bildirim açıklaması
        description = QLabel("Ödenmemiş faturalar için bildirim almak istiyorum")
        description.setStyleSheet("""
            color: #424242;
            font-size: 14px;
            margin-bottom: 16px;
        """)
        layout.addWidget(description)

        # Bildirim checkbox'ı
        self.bildirim_checkbox = QCheckBox("Ödenmemiş Faturalar İçin Bildirim Al")
        self.bildirim_checkbox.setChecked(True)
        self.bildirim_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                color: #1a237e;
                font-weight: bold;
                margin: 12px 0;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #1a237e;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #1a237e;
                border: 2px solid #1a237e;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #283593;
            }
        """)
        layout.addWidget(self.bildirim_checkbox)

        # Bildirim sıklığı seçimi
        frequency_container = QWidget()
        frequency_layout = QVBoxLayout()
        frequency_layout.setSpacing(12)

        frequency_label = QLabel("Günlük Bildirim Sayısı")
        frequency_label.setStyleSheet("""
            color: #1a237e;
                font-weight: bold;
            font-size: 15px;
            margin-top: 12px;
        """)
        frequency_layout.addWidget(frequency_label)

        # Bildirim sayısı girişi
        self.bildirim_sayisi_input = QLineEdit()
        self.bildirim_sayisi_input.setPlaceholderText("Günde kaç bildirim almak istiyorsunuz? (1-5)")
        self.bildirim_sayisi_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:hover {
                border: 2px solid #1a237e;
            }
            QLineEdit:focus {
                border: 2px solid #1a237e;
                background: #f5f5f5;
            }
        """)
        self.bildirim_sayisi_input.setText("1")  # Varsayılan değer
        frequency_layout.addWidget(self.bildirim_sayisi_input)

        frequency_container.setLayout(frequency_layout)
        layout.addWidget(frequency_container)

        # Kaydet butonu
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        
        self.bildirim_guncelle_button = QPushButton("Bildirim Ayarlarını Kaydet")
        self.bildirim_guncelle_button.setStyleSheet("""
            QPushButton {
                background-color: #1a237e;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 30px;
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
        """)
        self.bildirim_guncelle_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.bildirim_guncelle_button.clicked.connect(self.bildirim_ayarlarini_guncelle)
        button_layout.addWidget(self.bildirim_guncelle_button)
        
        layout.addLayout(button_layout)
        section.setLayout(layout)
        return section

    def bildirim_ayarlarini_guncelle(self):
        bildirim_istiyor = self.bildirim_checkbox.isChecked()
        
        if not bildirim_istiyor:
            if self.db.update_bildirim_ayarlari(self.current_user_id, False, 0):
                QMessageBox.information(self, "Başarılı", "Bildirim ayarları güncellendi!")
            else:
                QMessageBox.critical(self, "Hata", "Bildirim ayarları güncellenirken bir hata oluştu!")
            return

        try:
            bildirim_sayisi = int(self.bildirim_sayisi_input.text())
            if bildirim_sayisi < 1 or bildirim_sayisi > 5:
                QMessageBox.warning(self, "Hata", "Bildirim sayısı 1 ile 5 arasında olmalıdır!")
                return

            if self.db.update_bildirim_ayarlari(self.current_user_id, True, bildirim_sayisi):
                QMessageBox.information(self, "Başarılı", "Bildirim ayarları güncellendi!")
            else:
                QMessageBox.critical(self, "Hata", "Bildirim ayarları güncellenirken bir hata oluştu!")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir sayı girin!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Güncelleme sırasında bir hata oluştu: {str(e)}")

    def add_main_menu_button(self, layout):
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        self.ana_menu_button = QPushButton("Ana Menüye Dön")
        self.ana_menu_button.setObjectName("ana_menu")
        self.ana_menu_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.ana_menu_button.setStyleSheet("""
            QPushButton {
                background-color: darkred;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 120px;
                min-height: 30px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);

            }
            QPushButton:hover {
                background-color: red; /* Hover durumunda daha açık kırmızı */
            }
            QPushButton:pressed {
                background-color: #a00000; /* Basılı durumda daha koyu kırmızı */
            }
        """)
        self.ana_menu_button.clicked.connect(self.close)
        button_layout.addWidget(self.ana_menu_button)
        
        layout.addLayout(button_layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def kullanici_bilgilerini_yukle(self):
        # Kullanıcı bilgilerini veritabanından alın
        kullanici = self.db.get_kullanici_bilgileri(self.current_user_id)
        if kullanici:
            self.ad_input.setText(kullanici["ad"])
            self.soyad_input.setText(kullanici["soyad"])
            self.kullanici_adi_input.setText(kullanici["kullanici_adi"])
            self.email_input.setText(kullanici["email"])

    def profil_guncelle(self):
        kullanici_adi = self.kullanici_adi_input.text()
        ad = self.ad_input.text()
        soyad = self.soyad_input.text()
        email = self.email_input.text()

        if not all([kullanici_adi, ad, soyad, email]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            self.db.update_kullanici_bilgileri(self.current_user_id, ad, soyad, kullanici_adi, email)
            QMessageBox.information(self, "Başarılı", "Profil bilgileri güncellendi!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Güncelleme sırasında bir hata oluştu: {str(e)}")

    def sifre_degistir(self):
        eski_sifre = self.eski_sifre_input.text()
        yeni_sifre = self.yeni_sifre_input.text()
        yeni_sifre_tekrar = self.yeni_sifre_tekrar_input.text()

        if not all([eski_sifre, yeni_sifre, yeni_sifre_tekrar]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm şifre alanlarını doldurun!")
            return

        if yeni_sifre != yeni_sifre_tekrar:
            QMessageBox.warning(self, "Hata", "Yeni şifreler eşleşmiyor!")
            return

        try:
            if self.db.update_sifre(self.current_user_id, eski_sifre, yeni_sifre):
                QMessageBox.information(self, "Başarılı", "Şifre başarıyla değiştirildi!")
                self.clear_password_fields()
            else:
                QMessageBox.warning(self, "Hata", "Mevcut şifre yanlış!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Şifre değiştirme sırasında bir hata oluştu: {str(e)}")

    def clear_password_fields(self):
            self.eski_sifre_input.clear()
            self.yeni_sifre_input.clear()
            self.yeni_sifre_tekrar_input.clear()
