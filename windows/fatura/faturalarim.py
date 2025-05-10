from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                            QComboBox, QPushButton, QMessageBox, QFileDialog, QLineEdit, 
                            QLabel, QHBoxLayout, QDialog, QHeaderView)
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QColor, QFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

class FaturalarimWindow(QMainWindow):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("Faturalarım")
        self.resize(900, 600)
        self.center()
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3eafc, stop:1 #a8c0ff);
            }
            QWidget#main_card {
                background-color: #fff;
                border-radius: 28px;
                padding: 36px 48px;
                min-width: 800px;
                min-height: 480px;
                margin: 60px auto;
                border: 1px solid rgba(31,58,147,0.10);
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
            QLineEdit {
                font-size: 15px;
                border-radius: 8px;
                padding: 8px;
                border: 1.5px solid #e0e0e0;
                background: #f8fbff;
                margin-bottom: 8px;
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
                padding: 10px;
                margin-bottom: 8px;
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
                padding: 8px;
                border: 1.5px solid #e0e0e0;
                background: #f8fbff;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 1.5px solid #1F3A93;
            }
            QTableWidget {
                background-color: #fff;
                border-radius: 12px;
                border: 1.5px solid #e0e0e0;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3eafc;
                color: #1F3A93;
            }
            QHeaderView::section {
                background-color: #f8fbff;
                color: #1F3A93;
                padding: 12px;
                border: none;
                border-bottom: 1.5px solid #e0e0e0;
                font-weight: bold;
            }
            QLabel#total_label {
                font-size: 16px;
                font-weight: bold;
                color: #1F3A93;
                padding: 8px;
                background: #f8fbff;
                border-radius: 8px;
                border: 1.5px solid #e0e0e0;
            }
        """)

        # Ana kart
        main_card = QWidget()
        main_card.setObjectName("main_card")
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Başlık ve açıklama
        title_label = QLabel("Faturalarım")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        subtitle_label = QLabel("Tüm faturalarınızı görüntüleyin ve yönetin.")
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)

        # Toplam borç ve ödenen
        totals_layout = QHBoxLayout()
        self.toplam_borc_label = QLabel()
        self.toplam_borc_label.setObjectName("total_label")
        self.toplam_odenen_label = QLabel()
        self.toplam_odenen_label.setObjectName("total_label")
        totals_layout.addWidget(self.toplam_borc_label)
        totals_layout.addWidget(self.toplam_odenen_label)
        layout.addLayout(totals_layout)

        # Arama ve filtreleme
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Fatura Ara (Tür, Açıklama, Tarih, Durum)")
        self.search_input.textChanged.connect(self.ara)
        filter_layout.addWidget(self.search_input)

        self.filtre_combobox = QComboBox()
        self.filtre_combobox.addItem("Tüm Faturalar")
        self.filtre_combobox.addItem("Ödenmemiş Faturalar")
        self.filtre_combobox.addItem("Ödenen Faturalar")
        self.filtre_combobox.currentIndexChanged.connect(self.filtrele)
        filter_layout.addWidget(self.filtre_combobox)
        
        layout.addLayout(filter_layout)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Tür", "Miktar (TL)", "Açıklama", "Son Ödeme Tarihi", "Durum"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.detay_goster)
        layout.addWidget(self.table)

        # Butonlar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

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
        self.ana_menu_button.setObjectName("ana_menu")
        self.ana_menu_button.clicked.connect(self.close)
        button_layout.addWidget(self.ana_menu_button)

        layout.addLayout(button_layout)
        main_card.setLayout(layout)

        # Ana widget
        self.setCentralWidget(main_card)
        self.load_data()

    def center(self):
        qr = self.frameGeometry()
        cp = QCoreApplication.instance().desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_data(self):
        # Faturaları veritabanından al
        self.faturalar = self.db.get_all_faturalar(self.user_id)
        self.table.setRowCount(len(self.faturalar))
        toplam_borc = 0
        toplam_odenen = 0
        
        # Her fatura için tabloya satır ekle
        for i, fatura in enumerate(self.faturalar):
            # ID
            id_item = QTableWidgetItem(str(fatura["id"]))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, id_item)
            
            # Tür
            tur_item = QTableWidgetItem(fatura["tur"])
            tur_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, tur_item)
            
            # Miktar
            miktar_item = QTableWidgetItem(f"{float(fatura['miktar']):.2f} TL")
            miktar_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 2, miktar_item)
            
            # Açıklama
            aciklama_item = QTableWidgetItem(fatura["aciklama"])
            aciklama_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, aciklama_item)
            
            # Son Ödeme Tarihi
            tarih_item = QTableWidgetItem(fatura["son_odeme_tarihi"])
            tarih_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 4, tarih_item)
            
            # Durum
            durum_item = QTableWidgetItem(fatura["durum"])
            durum_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 5, durum_item)

            # Satır arka planı ve yazı rengi ayarla
            for j in range(6):
                item = self.table.item(i, j)
                if item:
                    if fatura["durum"] == "Bekliyor":
                        item.setBackground(QColor(255, 0, 0))  # Kırmızı
                        item.setForeground(QColor(0, 0, 0))  # Siyah yazı
                    elif fatura["durum"] == "Ödendi":
                        item.setBackground(QColor(0, 255, 0))  # Yeşil
                        item.setForeground(QColor(0, 0, 0))  # Siyah yazı

            # Toplam borç ve ödenen tutarları hesapla
            if fatura["durum"] == "Bekliyor":
                toplam_borc += float(fatura["miktar"])
            elif fatura["durum"] == "Ödendi":
                toplam_odenen += float(fatura["miktar"])

        # Toplam tutarları göster
        self.toplam_borc_label.setText(f"Toplam Borç: {toplam_borc:.2f} TL")
        self.toplam_odenen_label.setText(f"Toplam Ödenen: {toplam_odenen:.2f} TL")

        # Tüm satırları görünür yap
        for i in range(self.table.rowCount()):
            self.table.setRowHidden(i, False)

    def ara(self):
        aranan = self.search_input.text().lower()
        if not aranan:  # Eğer arama kutusu boşsa tüm satırları göster
            for i in range(self.table.rowCount()):
                self.table.setRowHidden(i, False)
            return

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
        self.db.update_fatura_durum(fatura_id, new_status, self.user_id)
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
            self.db.delete_fatura(fatura_id, self.user_id)
            QMessageBox.information(self, "Başarılı", "Fatura başarıyla silindi!")
            self.load_data()

    def detay_goster(self, row, column):
        fatura_id = int(self.table.item(row, 0).text())
        fatura = next((f for f in self.faturalar if f["id"] == fatura_id), None)
        if fatura:
            detay_text = f"""
            Fatura Detayları:
            
            ID: {fatura['id']}
            Tür: {fatura['tur']}
            Miktar: {float(fatura['miktar']):.2f} TL
            Açıklama: {fatura['aciklama']}
            Son Ödeme Tarihi: {fatura['son_odeme_tarihi']}
            Durum: {fatura['durum']}
            """
            QMessageBox.information(self, "Fatura Detayları", detay_text)

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
            c.drawString(100, 720, f"Miktar: {fatura['miktar']}")
            c.drawString(100, 700, f"Açıklama: {fatura['aciklama']}")
            c.drawString(100, 680, f"Son Ödeme Tarihi: {fatura['son_odeme_tarihi']}")
            c.drawString(100, 660, f"Durum: {fatura['durum']}")
            c.save()
            QMessageBox.information(self, "Başarılı", f"PDF başarıyla kaydedildi: {os.path.basename(dosya_yolu)}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"PDF oluşturulamadı: {str(e)}")
