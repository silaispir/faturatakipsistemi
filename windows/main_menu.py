from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QCoreApplication
from windows.fatura.fatura_ekle import FaturaEkleWindow
from windows.fatura.faturalarim import FaturalarimWindow
from windows.fatura.fatura_ode import FaturaOdeWindow
from windows.kullanici.ayarlar import AyarlarWindow
from windows.config import APP_STYLE

class MainMenuWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Ana Menüm")
        self.resize(500, 350)
        self.center()
        self.setStyleSheet(APP_STYLE)

        main_menu_page = QWidget()
        layout = QVBoxLayout()

        self.fatura_ekle_button = QPushButton("Fatura Ekle")
        self.fatura_ekle_button.clicked.connect(self.open_fatura_ekle)
        layout.addWidget(self.fatura_ekle_button)

        self.faturalarim_button = QPushButton("Faturalarım")
        self.faturalarim_button.clicked.connect(self.open_faturalarim)
        layout.addWidget(self.faturalarim_button)

        self.fatura_ode_button = QPushButton("Fatura Öde")
        self.fatura_ode_button.clicked.connect(self.open_fatura_ode)
        layout.addWidget(self.fatura_ode_button)

        self.ayarlar_button = QPushButton("Ayarlar")
        self.ayarlar_button.clicked.connect(self.open_ayarlar)
        layout.addWidget(self.ayarlar_button)

        main_menu_page.setLayout(layout)
        self.setCentralWidget(main_menu_page)

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_fatura_ekle(self):
        self.fatura_ekle_window = FaturaEkleWindow(self.db)
        self.fatura_ekle_window.show()

    def open_faturalarim(self):
        self.faturalarim_window = FaturalarimWindow(self.db)
        self.faturalarim_window.show()

    def open_fatura_ode(self):
        self.fatura_ode_window = FaturaOdeWindow(self.db)
        self.fatura_ode_window.show()

    def open_ayarlar(self):
        self.ayarlar_window = AyarlarWindow(self.db)
        self.ayarlar_window.show()
