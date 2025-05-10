from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

class BildirimYoneticisi:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.timer = QTimer()
        self.timer.timeout.connect(self.bildirimleri_kontrol_et)
        self.timer.start(60000)

    def bildirimleri_kontrol_et(self):
        for fatura in self.db.get_all_faturalar():
            if fatura["durum"] == "Bekliyor":
                QMessageBox.information(self.parent, "Hatırlatıcı",
                    f"Ödenmemiş fatura: {fatura['tur']} - {fatura['miktar']} TL\n"
                    f"Son Ödeme Tarihi: {fatura['son_odeme_tarihi']}\n"
                    f"Açıklama: {fatura['aciklama']}")