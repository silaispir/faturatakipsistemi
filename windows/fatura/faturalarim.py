from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QMessageBox, QFileDialog, QLineEdit, QLabel, QHBoxLayout, QDialog
from PyQt5.QtCore import Qt, QCoreApplication
from windows.config import APP_STYLE
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

class FaturalarimWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Faturalarım")
        self.resize(900, 600)
        self.center()
        self.setStyleSheet(APP_STYLE)

        faturalarim_page = QWidget()
        ana_layout = QVBoxLayout()

        # Toplam borç ve ödenen
        self.toplam_borc_label = QLabel()
        self.toplam_odenen_label = QLabel()
        toplam_layout = QHBoxLayout()
        toplam_layout.addWidget(self.toplam_borc_label)
        toplam_layout.addWidget(self.toplam_odenen_label)
        ana_layout.addLayout(toplam_layout)

        # Arama kutusu
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Fatura Ara (Tür, Açıklama, Tarih, Durum)")
        self.search_input.textChanged.connect(self.ara)
        ana_layout.addWidget(self.search_input)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Tür", "Miktar (TL)", "Açıklama", "Son Ödeme Tarihi", "Durum"])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 140)
        self.table.setColumnWidth(5, 100)
        self.table.cellDoubleClicked.connect(self.detay_goster)
        ana_layout.addWidget(self.table)

        self.filtre_combobox = QComboBox()
        self.filtre_combobox.addItem("Tüm Faturalar")
        self.filtre_combobox.addItem("Ödenmemiş Faturalar")
        self.filtre_combobox.addItem("Ödenen Faturalar")
        self.filtre_combobox.currentIndexChanged.connect(self.filtrele)
        ana_layout.addWidget(self.filtre_combobox)

        button_layout = QHBoxLayout()

        self.guncelle_button = QPushButton("Durumu Güncelle")
        self.guncelle_button.clicked.connect(self.durum_guncelle)
        button_layout.addWidget(self.guncelle_button)

        self.sil_button = QPushButton("Fatura Sil")
        self.sil_button.clicked.connect(self.fatura_sil)
        button_layout.addWidget(self.sil_button)

        self.pdf_button = QPushButton("PDF Olarak İndir")
        self.pdf_button.clicked.connect(self.pdf_olustur)
        button_layout.addWidget(self.pdf_button)

        self.ana_menu_button = QPushButton("Ana Menüye Dön")
        self.ana_menu_button.clicked.connect(self.close)
        button_layout.addWidget(self.ana_menu_button)

        ana_layout.addLayout(button_layout)
        faturalarim_page.setLayout(ana_layout)
        self.setCentralWidget(faturalarim_page)
        self.load_data()

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_data(self):
        self.faturalar = self.db.get_all_faturalar()
        self.table.setRowCount(len(self.faturalar))
        toplam_borc = 0
        toplam_odenen = 0
        for i, fatura in enumerate(self.faturalar):
            self.table.setItem(i, 0, QTableWidgetItem(str(fatura["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(fatura["tur"]))
            self.table.setItem(i, 2, QTableWidgetItem(str(fatura["miktar"])))
            self.table.setItem(i, 3, QTableWidgetItem(fatura["aciklama"]))
            self.table.setItem(i, 4, QTableWidgetItem(fatura["son_odeme_tarihi"]))
            self.table.setItem(i, 5, QTableWidgetItem(fatura["durum"]))
            # Satır arka planı
            for j in range(6):
                if fatura["durum"] == "Bekliyor":
                    self.table.item(i, j).setBackground(Qt.red)
                elif fatura["durum"] == "Ödendi":
                    self.table.item(i, j).setBackground(Qt.green)
            # Toplamlar
            if fatura["durum"] == "Bekliyor":
                toplam_borc += float(fatura["miktar"])
            elif fatura["durum"] == "Ödendi":
                toplam_odenen += float(fatura["miktar"])
        self.toplam_borc_label.setText(f"Toplam Borç: {toplam_borc:.2f} TL")
        self.toplam_odenen_label.setText(f"Toplam Ödenen: {toplam_odenen:.2f} TL")
        self.ara()

    def ara(self):
        aranan = self.search_input.text().lower()
        for i, fatura in enumerate(self.faturalar):
            row_visible = (
                aranan in str(fatura["id"]).lower() or
                aranan in fatura["tur"].lower() or
                aranan in fatura["aciklama"].lower() or
                aranan in fatura["son_odeme_tarihi"].lower() or
                aranan in fatura["durum"].lower()
            )
            self.table.setRowHidden(i, not row_visible)

    def filtrele(self):
        filtre = self.filtre_combobox.currentIndex()
        for i, fatura in enumerate(self.faturalar):
            if filtre == 0:
                self.table.setRowHidden(i, False)
            elif filtre == 1:
                self.table.setRowHidden(i, fatura["durum"] != "Bekliyor")
            elif filtre == 2:
                self.table.setRowHidden(i, fatura["durum"] != "Ödendi")

    def durum_guncelle(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Hata", "Lütfen bir fatura seçin!")
            return
        fatura_id = int(self.table.item(selected_row, 0).text())
        current_status = self.table.item(selected_row, 5).text()
        new_status = "Ödendi" if current_status == "Bekliyor" else "Bekliyor"
        self.db.update_fatura_durum(fatura_id, new_status)
        QMessageBox.information(self, "Başarılı", f"Fatura durumu {new_status} olarak güncellendi!")
        self.load_data()

    def fatura_sil(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Hata", "Lütfen bir fatura seçin!")
            return
        fatura_id = int(self.table.item(selected_row, 0).text())
        reply = QMessageBox.question(self, 'Onay', 'Faturayı silmek istediğinize emin misiniz?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_fatura(fatura_id)
            QMessageBox.information(self, "Başarılı", "Fatura başarıyla silindi!")
            self.load_data()

    def pdf_olustur(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Hata", "Lütfen bir fatura seçin!")
            return
        fatura = {
            "id": self.table.item(selected_row, 0).text(),
            "tur": self.table.item(selected_row, 1).text(),
            "miktar": self.table.item(selected_row, 2).text(),
            "aciklama": self.table.item(selected_row, 3).text(),
            "son_odeme_tarihi": self.table.item(selected_row, 4).text(),
            "durum": self.table.item(selected_row, 5).text()
        }
        dosya_yolu, _ = QFileDialog.getSaveFileName(self, "PDF Olarak Kaydet", f"fatura_{fatura['id']}.pdf", "PDF Files (*.pdf)")
        if not dosya_yolu:
            return
        try:
            c = canvas.Canvas(dosya_yolu, pagesize=A4)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(200, 800, "Fatura Bilgileri")
            c.setFont("Helvetica", 12)
            c.drawString(100, 760, f"Fatura ID: {fatura['id']}")
            c.drawString(100, 740, f"Tür: {fatura['tur']}")
            c.drawString(100, 720, f"Miktar: {fatura['miktar']} TL")
            c.drawString(100, 700, f"Açıklama: {fatura['aciklama']}")
            c.drawString(100, 680, f"Son Ödeme Tarihi: {fatura['son_odeme_tarihi']}")
            c.drawString(100, 660, f"Durum: {fatura['durum']}")
            c.save()
            QMessageBox.information(self, "Başarılı", f"PDF başarıyla kaydedildi: {os.path.basename(dosya_yolu)}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"PDF oluşturulamadı: {str(e)}")

    def detay_goster(self, row, column):
        fatura = self.faturalar[row]
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Fatura Detayı - ID: {fatura['id']}")
        dialog.resize(400, 350)
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(f"<b>Tür:</b> {fatura['tur']}"))
        vbox.addWidget(QLabel(f"<b>Miktar:</b> {fatura['miktar']} TL"))
        vbox.addWidget(QLabel(f"<b>Açıklama:</b> {fatura['aciklama']}"))
        vbox.addWidget(QLabel(f"<b>Son Ödeme Tarihi:</b> {fatura['son_odeme_tarihi']}"))
        vbox.addWidget(QLabel(f"<b>Durum:</b> {fatura['durum']}"))
        pdf_btn = QPushButton("PDF Önizle")
        pdf_btn.clicked.connect(lambda: self.pdf_olustur_detay(fatura))
        vbox.addWidget(pdf_btn)
        dialog.setLayout(vbox)
        dialog.exec_()

    def pdf_olustur_detay(self, fatura):
        dosya_yolu, _ = QFileDialog.getSaveFileName(self, "PDF Olarak Kaydet", f"fatura_{fatura['id']}.pdf", "PDF Files (*.pdf)")
        if not dosya_yolu:
            return
        try:
            c = canvas.Canvas(dosya_yolu, pagesize=A4)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(200, 800, "Fatura Bilgileri")
            c.setFont("Helvetica", 12)
            c.drawString(100, 760, f"Fatura ID: {fatura['id']}")
            c.drawString(100, 740, f"Tür: {fatura['tur']}")
            c.drawString(100, 720, f"Miktar: {fatura['miktar']} TL")
            c.drawString(100, 700, f"Açıklama: {fatura['aciklama']}")
            c.drawString(100, 680, f"Son Ödeme Tarihi: {fatura['son_odeme_tarihi']}")
            c.drawString(100, 660, f"Durum: {fatura['durum']}")
            c.save()
            QMessageBox.information(self, "Başarılı", f"PDF başarıyla kaydedildi: {os.path.basename(dosya_yolu)}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"PDF oluşturulamadı: {str(e)}")
