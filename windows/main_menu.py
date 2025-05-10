from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QSizePolicy
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QFont
from windows.fatura.fatura_ekle import FaturaEkleWindow
from windows.fatura.faturalarim import FaturalarimWindow
from windows.fatura.fatura_ode import FaturaOdeWindow
from windows.kullanici.ayarlar import AyarlarWindow
from windows.config import APP_STYLE

class MainMenuWindow(QMainWindow):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("Ana Menü")
        self.resize(900, 600)
        kullanici = self.db.get_kullanici_bilgileri(user_id)
        kullanici_adi = kullanici["ad"] if kullanici else "Kullanıcı"
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3eafc, stop:1 #a8c0ff);
            }
            QWidget#main_card {
                background-color: #ffffff;
                border-radius: 32px;
                padding: 36px 48px;
                min-width: 480px;
                min-height: 480px;
                max-width: 600px;
                margin: 60px auto;
                box-shadow: 0 8px 32px rgba(31,58,147,0.10);
            }
            QLabel#title {
                color: #1F3A93;
                font-family: Arial;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 8px;
            }
            QLabel#welcome {
                color: #222;
                font-family: Arial;
                font-size: 18px;
                font-weight: 500;
                margin-bottom: 32px;
            }
            QPushButton.menu_card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8fbff, stop:1 #e9f0fa);
                border-radius: 28px;
                border: 1.5px solid #e0e0e0;
                box-shadow: 0 4px 16px rgba(31,58,147,0.08);
                font-size: 18px;
                font-weight: bold;
                color: #1F3A93;
                padding: 0;
                margin: 18px;
                min-width: 180px;
                min-height: 140px;
                transition: all 0.2s cubic-bezier(.4,2,.6,1);
            }
            QPushButton.menu_card:hover {
                background: #1F3A93;
                color: #fff;
                box-shadow: 0 8px 32px rgba(31,58,147,0.18);
                transform: scale(1.06);
            }
            QPushButton#cikis.menu_card {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #fff0f0, stop:1 #fbeaea);
                color: #8B0000;
                border: 1.5px solid #f5cccc;
            }
            QPushButton#cikis.menu_card:hover {
                background: #8B0000;
                color: #fff;
                border: 1.5px solid #8B0000;
            }
            QLabel.card_icon {
                font-size: 38px;
                margin-bottom: 8px;
            }
            QLabel.card_title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 4px;
            }
            QLabel.card_desc {
                font-size: 13px;
                color: #555;
            }
        """)

        # Ana kart (tek panel)
        main_card = QWidget()
        main_card.setObjectName("main_card")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(18)
        card_layout.setContentsMargins(30, 30, 30, 30)

        # Küçük başlık
        title_label = QLabel("Fatura Takip Sistemi")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # Kullanıcıya özel hoş geldin mesajı
        welcome_label = QLabel(f"Hoş geldin, {kullanici_adi}!")
        welcome_label.setObjectName("welcome")
        welcome_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(welcome_label)

        # Grid şeklinde menü kartları
        grid = QGridLayout()
        grid.setSpacing(24)
        grid.setContentsMargins(10, 10, 10, 10)

        # Kartlar: (ikon, başlık, açıklama, buton fonksiyonu, objectName)
        cards = [
            ("🧾", "Fatura Ekle", "Yeni fatura ekleyin", self.open_fatura_ekle, "fatura_ekle"),
            ("📄", "Faturalarım", "Tüm faturalarınızı görüntüleyin", self.open_faturalarim, "faturalarim"),
            ("💳", "Fatura Öde", "Faturalarınızı ödeyin", self.open_fatura_ode, "fatura_ode"),
            ("⚙️", "Ayarlar", "Hesap ayarlarınızı yönetin", self.ayarlar_ac, "ayarlar"),
            ("🚪", "Çıkış Yap", "Güvenli çıkış yapın", self.close, "cikis"),
        ]
        positions = [(0,0), (0,1), (1,0), (1,1), (2,0,1,2)]
        for i, (icon, title, desc, func, objname) in enumerate(cards):
            btn = QPushButton()
            btn.setObjectName(objname)
            btn.setProperty("class", "menu_card")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(func)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            # Kart içeriği
            vbox = QVBoxLayout()
            vbox.setAlignment(Qt.AlignCenter)
            icon_label = QLabel(icon)
            icon_label.setObjectName("icon")
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setProperty("class", "card_icon")
            vbox.addWidget(icon_label)
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setProperty("class", "card_title")
            vbox.addWidget(title_label)
            desc_label = QLabel(desc)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setProperty("class", "card_desc")
            vbox.addWidget(desc_label)
            btn.setLayout(vbox)
            if len(positions[i]) == 2:
                grid.addWidget(btn, positions[i][0], positions[i][1])
            else:
                grid.addWidget(btn, positions[i][0], positions[i][1], positions[i][2], positions[i][3])

        card_layout.addLayout(grid)
        main_card.setLayout(card_layout)

        # Ortalamak için ana layout
        outer = QWidget()
        outer_layout = QVBoxLayout()
        outer_layout.addStretch()
        outer_layout.addWidget(main_card, alignment=Qt.AlignCenter)
        outer_layout.addStretch()
        outer.setLayout(outer_layout)
        self.setCentralWidget(outer)

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_fatura_ekle(self):
        self.fatura_ekle_window = FaturaEkleWindow(self.db, self.user_id)
        self.fatura_ekle_window.show()

    def open_faturalarim(self):
        self.faturalarim_window = FaturalarimWindow(self.db, self.user_id)
        self.faturalarim_window.show()

    def open_fatura_ode(self):
        self.fatura_ode_window = FaturaOdeWindow(self.db, self.user_id)
        self.fatura_ode_window.show()

    def ayarlar_ac(self):
        self.ayarlar_window = AyarlarWindow(self.db, self.user_id)
        self.ayarlar_window.show()
