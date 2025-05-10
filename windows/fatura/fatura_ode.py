from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, 
                            QLineEdit, QPushButton, QCheckBox, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QFont
from windows.config import APP_STYLE

class FaturaOdeWindow(QMainWindow):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("Fatura Öde")
        self.resize(800, 800)
        self.center()
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3eafc, stop:1 #a8c0ff);
            }
            QWidget#main_card {
                background-color: #fff;
                border-radius: 28px;
                padding: 36px 48px;
                min-width: 620px;
                min-height: 680px;
                max-width: 720px;
                margin: 60px auto;
                box-shadow: 0 8px 32px rgba(31,58,147,0.10);
            }
            QLabel#title {
                color: #1F3A93;
                font-family: Arial;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 8px;
            }
            QLabel#subtitle {
                color: #222;
                font-family: Arial;
                font-size: 16px;
                margin-bottom: 24px;
            }
            QLabel#detail_label {
                color: #1F3A93;
                font-family: Arial;
                font-size: 16px;
                padding: 20px;
                background: #f8fbff;
                border-radius: 12px;
                border: 2px solid #e0e0e0;
                margin: 20px 0;
                min-height: 200px;
            }
            QLineEdit {
                font-size: 15px;
                border-radius: 8px;
                padding: 12px;
                border: 1.5px solid #e0e0e0;
                background: #f8fbff;
                margin-bottom: 16px;
            }
            QLineEdit:hover {
                border: 1.5px solid #1F3A93;
            }
            QPushButton {
                font-size: 15px;
                font-weight: bold;
                background-color: #1F3A93;
                color: white;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 12px;
                min-width: 120px;
                border: 1px solid rgba(31,58,147,0.08);
            }
            QPushButton:hover {
                background-color: #2E7D32;
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
                padding: 12px;
                border: 1.5px solid #e0e0e0;
                background: #f8fbff;
                min-width: 150px;
                margin-bottom: 16px;
            }
            QComboBox:hover {
                border: 1.5px solid #1F3A93;
            }
            QCheckBox {
                font-size: 14px;
                color: #1F3A93;
                margin-bottom: 16px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1.5px solid #e0e0e0;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #1F3A93;
                border: 1.5px solid #1F3A93;
            }
            QMessageBox {
                background-color: white;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                padding: 8px;
            }
            QMessageBox QPushButton[text="Hayır"] {
                background-color: #8B0000;
                color: white;
            }
            QMessageBox QPushButton[text="Hayır"]:hover {
                background-color: #A52A2A;
            }
            QMessageBox QPushButton[text="Evet"] {
                background-color: #1F3A93;
                color: white;
            }
            QMessageBox QPushButton[text="Evet"]:hover {
                background-color: #2E7D32;
            }
        """)

        # Ana kart
        main_card = QWidget()
        main_card.setObjectName("main_card")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        # Başlık ve açıklama
        title_label = QLabel("Fatura Öde")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        subtitle_label = QLabel("Faturanızı güvenle ödeyin.")
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)

        # Fatura seçimi
        fatura_label = QLabel("Fatura Seçiniz:")
        fatura_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1F3A93;")
        layout.addWidget(fatura_label)
        
        self.fatura_combobox = QComboBox()
        self.fatura_combobox.addItem("Fatura Seçiniz")
        self.fatura_combobox.currentIndexChanged.connect(self.fatura_secildi)
        layout.addWidget(self.fatura_combobox)

        # Fatura detayları
        self.fatura_detay_label = QLabel("")
        self.fatura_detay_label.setObjectName("detail_label")
        self.fatura_detay_label.setWordWrap(True)
        layout.addWidget(self.fatura_detay_label)

        # Ödeme yöntemi
        odeme_label = QLabel("Ödeme Yöntemi:")
        odeme_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1F3A93;")
        layout.addWidget(odeme_label)
        
        self.odeme_yontemi = QComboBox()
        self.odeme_yontemi.addItem("Banka Kartı")
        self.odeme_yontemi.addItem("Kredi Kartı")
        self.odeme_yontemi.addItem("Havale/EFT")
        self.odeme_yontemi.currentTextChanged.connect(self.odeme_yontemi_degisti)
        layout.addWidget(self.odeme_yontemi)

        # Kart bilgileri
        self.kart_no_input = QLineEdit()
        self.kart_no_input.setPlaceholderText("Kart Numarası (16 haneli)")
        self.kart_no_input.setVisible(True)
        layout.addWidget(self.kart_no_input)

        self.son_kullanim_input = QLineEdit()
        self.son_kullanim_input.setPlaceholderText("Son Kullanma Tarihi (MM/YY)")
        self.son_kullanim_input.setVisible(True)
        layout.addWidget(self.son_kullanim_input)

        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("CVV (3 haneli)")
        self.cvv_input.setVisible(True)
        layout.addWidget(self.cvv_input)

        # Havale/EFT bilgileri
        self.banka_combobox = QComboBox()
        self.banka_combobox.addItem("Banka Seçiniz")
        self.banka_combobox.addItems(["Ziraat Bankası", "İş Bankası", "Garanti BBVA", "Akbank", "Yapı Kredi"])
        self.banka_combobox.setVisible(False)
        layout.addWidget(self.banka_combobox)

        self.iban_input = QLineEdit()
        self.iban_input.setPlaceholderText("IBAN (TR...)")
        self.iban_input.setVisible(False)
        layout.addWidget(self.iban_input)

        # Onay kutusu
        self.onay_checkbox = QCheckBox("Ödeme işlemini onaylıyorum")
        layout.addWidget(self.onay_checkbox)

        # Butonlar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.ode_button = QPushButton("Ödemeyi Tamamla")
        self.ode_button.clicked.connect(self.fatura_ode)
        button_layout.addWidget(self.ode_button)

        self.ana_menu_button = QPushButton("Ana Menüye Dön")
        self.ana_menu_button.setObjectName("ana_menu")
        self.ana_menu_button.clicked.connect(self.close)
        button_layout.addWidget(self.ana_menu_button)

        layout.addLayout(button_layout)
        main_card.setLayout(layout)

        # Ana widget
        self.setCentralWidget(main_card)
        self.faturalari_yukle()

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def faturalari_yukle(self):
        self.fatura_combobox.clear()
        self.fatura_combobox.addItem("Fatura Seçiniz")
        for fatura in self.db.get_all_faturalar(self.user_id):
            if fatura["durum"] == "Bekliyor":
                self.fatura_combobox.addItem(
                    f"{fatura['id']} - {fatura['tur']} - {fatura['miktar']} TL",
                    fatura["id"]
                )

    def fatura_secildi(self):
        fatura_id = self.fatura_combobox.currentData()
        if fatura_id:
            for fatura in self.db.get_all_faturalar(self.user_id):
                if fatura["id"] == fatura_id:
                    self.fatura_detay_label.setText(
                        f"Fatura Detayları:\n\n"
                        f"Fatura ID: {fatura['id']}\n"
                        f"Tür: {fatura['tur']}\n"
                        f"Miktar: {float(fatura['miktar']):.2f} TL\n"
                        f"Son Ödeme Tarihi: {fatura['son_odeme_tarihi']}\n"
                        f"Açıklama: {fatura['aciklama']}\n"
                        f"Durum: {fatura['durum']}"
                    )
                    break

    def odeme_yontemi_degisti(self):
        yontem = self.odeme_yontemi.currentText()
        kart_gerekli = yontem in ["Banka Kartı", "Kredi Kartı"]
        self.kart_no_input.setVisible(kart_gerekli)
        self.son_kullanim_input.setVisible(kart_gerekli)
        self.cvv_input.setVisible(kart_gerekli)
        self.banka_combobox.setVisible(yontem == "Havale/EFT")
        self.iban_input.setVisible(yontem == "Havale/EFT")

    def fatura_ode(self):
        fatura_id = self.fatura_combobox.currentData()
        if not fatura_id:
            QMessageBox.warning(self, "Hata", "Lütfen bir fatura seçiniz!")
            return
        if not self.onay_checkbox.isChecked():
            QMessageBox.warning(self, "Hata", "Ödeme işlemini onaylamanız gerekmektedir!")
            return
        yontem = self.odeme_yontemi.currentText()
        if yontem in ["Banka Kartı", "Kredi Kartı"]:
            if not all([self.kart_no_input.text(), self.son_kullanim_input.text(), self.cvv_input.text()]):
                QMessageBox.warning(self, "Hata", "Lütfen tüm kart bilgilerini doldurunuz!")
                return
        elif yontem == "Havale/EFT":
            if self.banka_combobox.currentIndex() == 0:
                QMessageBox.warning(self, "Hata", "Lütfen bir banka seçiniz!")
                return
            if not self.iban_input.text().startswith("TR"):
                QMessageBox.warning(self, "Hata", "Geçerli bir IBAN giriniz (TR ile başlamalı)!")
                return

        reply = QMessageBox.question(self, 'Onay', 'Faturayı ödemek istediğinize emin misiniz?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.db.update_fatura_durum(fatura_id, "Ödendi", self.user_id)
            QMessageBox.information(self, "Başarılı", "Fatura başarıyla ödendi!")
            self.faturalari_yukle()
            self.fatura_detay_label.setText("")
            self.onay_checkbox.setChecked(False)
