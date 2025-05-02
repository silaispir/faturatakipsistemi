from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QCalendarWidget, QMessageBox, QFileDialog, QHBoxLayout
from PyQt5.QtCore import QDate, QCoreApplication
from windows.config import APP_STYLE
import os

class FaturaEkleWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Fatura Ekle")
        self.resize(450, 450)
        self.center()
        self.setStyleSheet(APP_STYLE)

        fatura_ekle_page = QWidget()
        layout = QVBoxLayout()

        self.tur_input = QLineEdit()
        self.tur_input.setPlaceholderText("Fatura Türü (Elektrik, Su, Doğalgaz vb.)")
        layout.addWidget(self.tur_input)

        self.miktar_input = QLineEdit()
        self.miktar_input.setPlaceholderText("Miktar (TL)")
        layout.addWidget(self.miktar_input)

        self.aciklama_input = QLineEdit()
        self.aciklama_input.setPlaceholderText("Açıklama")
        layout.addWidget(self.aciklama_input)

        layout.addWidget(QLabel("Son Ödeme Tarihi:"))
        self.takvim = QCalendarWidget()
        self.takvim.setStyleSheet("background-color: white;")
        self.takvim.setMinimumDate(QDate.currentDate())
        layout.addWidget(self.takvim)

        # Dosya ekleme
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Dosya eklenmedi")
        self.file_btn = QPushButton("Dosya Ekle (PDF/Resim)")
        self.file_btn.clicked.connect(self.dosya_sec)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_btn)
        layout.addLayout(file_layout)
        self.selected_file_path = None

        self.kaydet_button = QPushButton("Kaydet")
        self.kaydet_button.clicked.connect(self.kaydet_fatura)
        layout.addWidget(self.kaydet_button)

        self.ana_menu_button = QPushButton("Ana Menüye Dön")
        self.ana_menu_button.clicked.connect(self.close)
        layout.addWidget(self.ana_menu_button)

        fatura_ekle_page.setLayout(layout)
        self.setCentralWidget(fatura_ekle_page)

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def dosya_sec(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "PDF ve Resimler (*.pdf *.png *.jpg *.jpeg *.bmp)")
        if dosya_yolu:
            self.selected_file_path = dosya_yolu
            self.file_label.setText(os.path.basename(dosya_yolu))
        else:
            self.selected_file_path = None
            self.file_label.setText("Dosya eklenmedi")

    def kaydet_fatura(self):
        tur = self.tur_input.text()
        miktar = self.miktar_input.text()
        aciklama = self.aciklama_input.text()
        son_odeme_tarihi = self.takvim.selectedDate().toString("dd.MM.yyyy")
        dosya = self.selected_file_path if self.selected_file_path else ""

        if not tur or not miktar or not aciklama:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            miktar = float(miktar)
        except ValueError:
            QMessageBox.warning(self, "Hata", "Miktar geçerli bir sayı olmalıdır!")
            return

        durum = "Bekliyor"
        # Veritabanı add_fatura fonksiyonuna dosya parametresi eklenecek!
        try:
            self.db.add_fatura(tur, miktar, aciklama, son_odeme_tarihi, durum, dosya)
        except TypeError:
            # Eski fonksiyon desteği için
            self.db.add_fatura(tur, miktar, aciklama, son_odeme_tarihi, durum)
        QMessageBox.information(self, "Başarılı", "Fatura başarıyla eklendi!")
        self.tur_input.clear()
        self.miktar_input.clear()
        self.aciklama_input.clear()
        self.selected_file_path = None
        self.file_label.setText("Dosya eklenmedi")
