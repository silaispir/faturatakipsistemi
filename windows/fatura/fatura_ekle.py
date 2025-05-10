from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, 
                            QPushButton, QMessageBox, QFileDialog, QHBoxLayout, 
                            QSizePolicy, QCalendarWidget, QComboBox)
from PyQt5.QtCore import QDate, QCoreApplication, Qt
import os
from datetime import datetime

class FaturaEkleWindow(QMainWindow):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("Fatura Ekle")
        self.resize(600, 600)
        self.center()
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3eafc, stop:1 #a8c0ff);
            }
            QWidget#main_card {
                background-color: #fff;
                border-radius: 28px;
                padding: 36px 48px;
                min-width: 420px;
                min-height: 480px;
                max-width: 520px;
                margin: 60px auto;
                box-shadow: 0 8px 32px rgba(31,58,147,0.10);
            }
            QLabel#title {
                color: #1F3A93;
                font-family: Arial;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 8px;
            }
            QLabel#subtitle {
                color: #222;
                font-family: Arial;
                font-size: 15px;
                margin-bottom: 24px;
            }
            QLineEdit, QLabel#file_label {
                font-size: 16px;
                border-radius: 10px;
                padding: 12px;
                border: 1.5px solid #e0e0e0;
                background: #f8fbff;
                margin-bottom: 16px;
            }
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #1F3A93;
                color: white;
                border-radius: 10px;
                padding: 14px;
                margin-bottom: 14px;
                box-shadow: 0 4px 16px rgba(31,58,147,0.08);
                transition: background 0.3s, color 0.3s;
            }
            QPushButton:hover {
                background-color: #2E7D32;
                color: #fff;
            }
            QPushButton#ana_menu {
                background-color: #8B0000;
            }
            QPushButton#ana_menu:hover {
                background-color: #A52A2A;
            }
            QComboBox {
                font-size: 15px;
                border-radius: 8px;
                padding: 8px;
                border: 1.5px solid #e0e0e0;
                background: #f8fbff;
                min-width: 80px;
                min-height: 35px;
            }
            QComboBox:hover {
                border: 1.5px solid #1F3A93;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QComboBox QAbstractItemView {
                font-size: 15px;
                padding: 6px;
                selection-background-color: #1F3A93;
                selection-color: white;
            }
        """)

        # Ana kart
        main_card = QWidget()
        main_card.setObjectName("main_card")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        # Başlık ve açıklama
        title_label = QLabel("Fatura Ekle")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        subtitle_label = QLabel("Yeni bir fatura ekleyin ve son ödeme tarihini seçin.")
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)

        self.tur_input = QLineEdit()
        self.tur_input.setPlaceholderText("Fatura Türü (Elektrik, Su, Doğalgaz vb.)")
        layout.addWidget(self.tur_input)

        self.miktar_input = QLineEdit()
        self.miktar_input.setPlaceholderText("Miktar (TL)")
        layout.addWidget(self.miktar_input)

        self.aciklama_input = QLineEdit()
        self.aciklama_input.setPlaceholderText("Açıklama")
        layout.addWidget(self.aciklama_input)

        # Son ödeme tarihi: başlık ve seçiciler
        date_section = QVBoxLayout()
        date_section.setSpacing(4)
        date_label = QLabel("Son Ödeme Tarihi:")
        date_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-bottom: 4px;")
        date_label.setAlignment(Qt.AlignCenter)
        date_section.addWidget(date_label)

        # Tarih seçici combobox'lar
        date_combos_layout = QHBoxLayout()
        date_combos_layout.setSpacing(8)
        
        # Gün seçici
        self.day_combo = QComboBox()
        self.day_combo.addItems([str(i).zfill(2) for i in range(1, 32)])
        date_combos_layout.addWidget(self.day_combo)
        
        # Ay seçici
        self.month_combo = QComboBox()
        self.month_combo.addItems([str(i).zfill(2) for i in range(1, 13)])
        date_combos_layout.addWidget(self.month_combo)
        
        # Yıl seçici
        current_year = datetime.now().year
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(i) for i in range(current_year, current_year + 5)])
        date_combos_layout.addWidget(self.year_combo)
        
        date_combos_layout.addStretch()
        date_section.addLayout(date_combos_layout)
        layout.addLayout(date_section)

        # Dosya ekleme
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Dosya eklenmedi")
        self.file_label.setObjectName("file_label")
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
        self.ana_menu_button.setObjectName("ana_menu")
        self.ana_menu_button.clicked.connect(self.close)
        layout.addWidget(self.ana_menu_button)

        main_card.setLayout(layout)

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

    def get_selected_date(self):
        day = self.day_combo.currentText()
        month = self.month_combo.currentText()
        year = self.year_combo.currentText()
        return f"{day}.{month}.{year}"

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
        son_odeme_tarihi = self.get_selected_date()
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
        try:
            self.db.add_fatura(self.user_id, tur, miktar, aciklama, son_odeme_tarihi, durum, dosya)
            QMessageBox.information(self, "Başarılı", "Fatura başarıyla eklendi!")
            self.tur_input.clear()
            self.miktar_input.clear()
            self.aciklama_input.clear()
            self.selected_file_path = None
            self.file_label.setText("Dosya eklenmedi")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Fatura eklenirken bir hata oluştu: {str(e)}")
