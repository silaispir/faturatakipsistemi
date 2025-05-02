import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("faturalar.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faturalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tur TEXT NOT NULL,
                miktar REAL NOT NULL,
                aciklama TEXT NOT NULL,
                son_odeme_tarihi TEXT NOT NULL,
                durum TEXT NOT NULL,
                dosya TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                soyad TEXT NOT NULL,
                kullanici_adi TEXT NOT NULL,
                email TEXT NOT NULL,
                sifre TEXT NOT NULL
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM kullanicilar")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO kullanicilar (ad, soyad, kullanici_adi, email, sifre)
                VALUES (?, ?, ?, ?, ?)
            """, ("name", "surname", "user", "namesurname@gmail.com", "1234"))
        self.conn.commit()

    def add_fatura(self, tur, miktar, aciklama, son_odeme_tarihi, durum, dosya=None):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO faturalar (tur, miktar, aciklama, son_odeme_tarihi, durum, dosya)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tur, miktar, aciklama, son_odeme_tarihi, durum, dosya))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_faturalar(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM faturalar")
        rows = cursor.fetchall()
        return [{"id": row[0], "tur": row[1], "miktar": row[2], "aciklama": row[3],
                 "son_odeme_tarihi": row[4], "durum": row[5], "dosya": row[6] if len(row) > 6 else ""} for row in rows]

    def update_fatura_durum(self, fatura_id, durum):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE faturalar SET durum = ? WHERE id = ?", (durum, fatura_id))
        self.conn.commit()

    def delete_fatura(self, fatura_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM faturalar WHERE id = ?", (fatura_id,))
        self.conn.commit()

    def get_kullanici_bilgileri(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT ad, soyad, kullanici_adi, email, sifre FROM kullanicilar WHERE id = 1")
        row = cursor.fetchone()
        if row:
            return {"ad": row[0], "soyad": row[1], "kullanici_adi": row[2], "email": row[3], "sifre": row[4]}
        return None

    def update_kullanici_bilgileri(self, ad, soyad, kullanici_adi, email):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE kullanicilar SET ad = ?, soyad = ?, kullanici_adi = ?, email = ? WHERE id = 1
        """, (ad, soyad, kullanici_adi, email))
        self.conn.commit()

    def update_kullanici_sifre(self, sifre):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE kullanicilar SET sifre = ? WHERE id = 1", (sifre,))
        self.conn.commit()

    def get_kullanici_by_credentials(self, kullanici_adi, sifre):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "ad": row[1], "soyad": row[2], "kullanici_adi": row[3], "email": row[4], "sifre": row[5]}
        return None

    def close(self):
        self.conn.close()