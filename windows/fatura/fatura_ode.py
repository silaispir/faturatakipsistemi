from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtCore import QCoreApplication
from windows.config import APP_STYLE

class FaturaOdeWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Fatura Öde")
        self.resize(500, 500)
        self.center()
        self.setStyleSheet(APP_STYLE)

        fatura_ode_page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Fatura Seçiniz:"))
        self.fatura_combobox = QComboBox()
        self.fatura_combobox.addItem("Fatura Seçiniz")
        self.fatura_combobox.currentIndexChanged.connect(self.fatura_secildi)
        layout.addWidget(self.fatura_combobox)

        self.fatura_detay_label = QLabel("")
        layout.addWidget(self.fatura_detay_label)

        layout.addWidget(QLabel("Ödeme Yöntemi:"))
        self.odeme_yontemi = QComboBox()
        self.odeme_yontemi.addItem("Banka Kartı")
        self.odeme_yontemi.addItem("Kredi Kartı")
        self.odeme_yontemi.addItem("Havale/EFT")
        self.odeme_yontemi.currentTextChanged.connect(self.odeme_yontemi_degisti)
        layout.addWidget(self.odeme_yontemi)

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

        self.banka_combobox = QComboBox()
        self.banka_combobox.addItem("Banka Seçiniz")
        self.banka_combobox.addItems(["Ziraat Bankası", "İş Bankası", "Garanti BBVA", "Akbank", "Yapı Kredi"])
        self.banka_combobox.setVisible(False)
        layout.addWidget(self.banka_combobox)

        self.iban_input = QLineEdit()
        self.iban_input.setPlaceholderText("IBAN (TR...)")
        self.iban_input.setVisible(False)
        layout.addWidget(self.iban_input)

        self.onay_checkbox = QCheckBox("Ödeme işlemini onaylıyorum")
        layout.addWidget(self.onay_checkbox)

        self.ode_button = QPushButton("Ödemeyi Tamamla")
        self.ode_button.clicked.connect(self.fatura_ode)
        layout.addWidget(self.ode_button)

        self.ana_menu_button = QPushButton("Ana Menüye Dön")
        self.ana_menu_button.clicked.connect(self.close)
        layout.addWidget(self.ana_menu_button)

        fatura_ode_page.setLayout(layout)
        self.setCentralWidget(fatura_ode_page)
        self.faturalari_yukle()

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def faturalari_yukle(self):
        self.fatura_combobox.clear()
        self.fatura_combobox.addItem("Fatura Seçiniz")
        for fatura in self.db.get_all_faturalar():
            if fatura["durum"] == "Bekliyor":
                self.fatura_combobox.addItem(
                    f"{fatura['id']} - {fatura['tur']} - {fatura['miktar']} TL",
                    fatura["id"]
                )

    def fatura_secildi(self):
        fatura_id = self.fatura_combobox.currentData()
        if fatura_id:
            for fatura in self.db.get_all_faturalar():
                if fatura["id"] == fatura_id:
                    self.fatura_detay_label.setText(
                        f"Fatura Detayları:\n"
                        f"Tür: {fatura['tur']}\n"
                        f"Miktar: {fatura['miktar']} TL\n"
                        f"Son Ödeme Tarihi: {fatura['son_odeme_tarihi']}\n"
                        f"Açıklama: {fatura['aciklama']}"
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
        self.db.update_fatura_durum(fatura_id, "Ödendi")
        QMessageBox.information(self, "Başarılı", "Fatura başarıyla ödendi!")
        self.faturalari_yukle()
        self.fatura_detay_label.setText("")
        self.onay_checkbox.setChecked(False)
