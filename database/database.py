import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("faturalar.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Kullanıcılar tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                soyad TEXT NOT NULL,
                kullanici_adi TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                sifre TEXT NOT NULL,
                bildirim_istiyor BOOLEAN DEFAULT 1,
                bildirim_sayisi INTEGER DEFAULT 1
            )
        """)
        
        # Mevcut tabloya sütunları ekle
        try:
            cursor.execute("ALTER TABLE kullanicilar ADD COLUMN bildirim_istiyor BOOLEAN DEFAULT 1")
        except sqlite3.OperationalError:
            pass  # Sütun zaten varsa hata vermesini engelle
            
        try:
            cursor.execute("ALTER TABLE kullanicilar ADD COLUMN bildirim_sayisi INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            pass  # Sütun zaten varsa hata vermesini engelle
        
        # Son giriş tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS son_giris (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT,
                sifre TEXT,
                beni_hatirla BOOLEAN DEFAULT 0
            )
        """)
        
        # Faturalar tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faturalar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER NOT NULL,
                tur TEXT NOT NULL,
                miktar REAL NOT NULL,
                aciklama TEXT NOT NULL,
                son_odeme_tarihi TEXT NOT NULL,
                durum TEXT NOT NULL,
                dosya TEXT,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id)
            )
        """)
        
        # Varsayılan kullanıcı kontrolü
        cursor.execute("SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = ?", ("user",))
        if cursor.fetchone()[0] == 0:
            try:
                cursor.execute("""
                    INSERT INTO kullanicilar (ad, soyad, kullanici_adi, email, sifre)
                    VALUES (?, ?, ?, ?, ?)
                """, ("name", "surname", "user", "user@example.com", "1234"))
                self.conn.commit()
            except sqlite3.IntegrityError:
                # Eğer e-posta zaten varsa, farklı bir e-posta ile tekrar dene
                cursor.execute("""
                    INSERT INTO kullanicilar (ad, soyad, kullanici_adi, email, sifre)
                    VALUES (?, ?, ?, ?, ?)
                """, ("name", "surname", "user", f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com", "1234"))
                self.conn.commit()
        
        self.conn.commit()

    def son_giris_kaydet(self, kullanici_adi, sifre, beni_hatirla):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM son_giris")  # Önceki kayıtları temizle
        cursor.execute("""
            INSERT INTO son_giris (kullanici_adi, sifre, beni_hatirla)
            VALUES (?, ?, ?)
        """, (kullanici_adi, sifre, beni_hatirla))
        self.conn.commit()

    def son_giris_bilgilerini_al(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT kullanici_adi, sifre, beni_hatirla FROM son_giris LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {
                "kullanici_adi": row[0],
                "sifre": row[1],
                "beni_hatirla": bool(row[2])
            }
        return None

    def add_fatura(self, kullanici_id, tur, miktar, aciklama, son_odeme_tarihi, durum, dosya=None):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO faturalar (kullanici_id, tur, miktar, aciklama, son_odeme_tarihi, durum, dosya)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (kullanici_id, tur, miktar, aciklama, son_odeme_tarihi, durum, dosya))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_faturalar(self, kullanici_id=None):
        cursor = self.conn.cursor()
        if kullanici_id:
            cursor.execute("SELECT * FROM faturalar WHERE kullanici_id = ?", (kullanici_id,))
        else:
            cursor.execute("SELECT * FROM faturalar")
        rows = cursor.fetchall()
        return [{"id": row[0], "kullanici_id": row[1], "tur": row[2], "miktar": row[3], "aciklama": row[4],
                 "son_odeme_tarihi": row[5], "durum": row[6], "dosya": row[7] if len(row) > 7 else ""} for row in rows]

    def update_fatura_durum(self, fatura_id, durum, kullanici_id=None):
        cursor = self.conn.cursor()
        if kullanici_id:
            cursor.execute("UPDATE faturalar SET durum = ? WHERE id = ? AND kullanici_id = ?", 
                         (durum, fatura_id, kullanici_id))
        else:
            cursor.execute("UPDATE faturalar SET durum = ? WHERE id = ?", (durum, fatura_id))
        self.conn.commit()

    def delete_fatura(self, fatura_id, kullanici_id=None):
        cursor = self.conn.cursor()
        if kullanici_id:
            cursor.execute("DELETE FROM faturalar WHERE id = ? AND kullanici_id = ?", (fatura_id, kullanici_id))
        else:
            cursor.execute("DELETE FROM faturalar WHERE id = ?", (fatura_id,))
        self.conn.commit()

    def get_kullanici_bilgileri(self, kullanici_id=None):
        cursor = self.conn.cursor()
        if kullanici_id:
            cursor.execute("SELECT ad, soyad, kullanici_adi, email, sifre FROM kullanicilar WHERE id = ?", (kullanici_id,))
        else:
            cursor.execute("SELECT ad, soyad, kullanici_adi, email, sifre FROM kullanicilar WHERE id = 1")
        row = cursor.fetchone()
        if row:
            return {"ad": row[0], "soyad": row[1], "kullanici_adi": row[2], "email": row[3], "sifre": row[4]}
        return None

    def update_kullanici_bilgileri(self, ad, soyad, kullanici_adi, email, kullanici_id=None):
        cursor = self.conn.cursor()
        try:
            if kullanici_id:
                cursor.execute("""
                    UPDATE kullanicilar SET ad = ?, soyad = ?, kullanici_adi = ?, email = ? WHERE id = ?
                """, (ad, soyad, kullanici_adi, email, kullanici_id))
            else:
                cursor.execute("""
                    UPDATE kullanicilar SET ad = ?, soyad = ?, kullanici_adi = ?, email = ? WHERE id = 1
                """, (ad, soyad, kullanici_adi, email))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Kullanıcı bilgileri güncelleme hatası: {e}")
            return False

    def update_kullanici_sifre(self, sifre, kullanici_id=None):
        cursor = self.conn.cursor()
        try:
            if kullanici_id:
                cursor.execute("UPDATE kullanicilar SET sifre = ? WHERE id = ?", (sifre, kullanici_id))
            else:
                cursor.execute("UPDATE kullanicilar SET sifre = ? WHERE id = 1", (sifre,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Şifre güncelleme hatası: {e}")
            return False

    def get_kullanici_by_credentials(self, kullanici_adi, sifre):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, ad, soyad, kullanici_adi, email, sifre FROM kullanicilar WHERE kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "ad": row[1], "soyad": row[2], "kullanici_adi": row[3], "email": row[4], "sifre": row[5]}
        return None

    def kullanici_adi_var_mi(self, kullanici_adi):
        try:
            self.conn.cursor().execute("SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = ?", (kullanici_adi,))
            return self.conn.cursor().fetchone()[0] > 0
        except Exception as e:
            print(f"Kullanıcı adı kontrolü hatası: {e}")
            return False

    def email_var_mi(self, email):
        try:
            self.conn.cursor().execute("SELECT COUNT(*) FROM kullanicilar WHERE email = ?", (email,))
            return self.conn.cursor().fetchone()[0] > 0
        except Exception as e:
            print(f"E-posta kontrolü hatası: {e}")
            return False

    def kullanici_ekle(self, ad, soyad, email, kullanici_adi, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO kullanicilar (ad, soyad, email, kullanici_adi, sifre)
                VALUES (?, ?, ?, ?, ?)
            """, (ad, soyad, email, kullanici_adi, password))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Kullanıcı ekleme hatası: {e}")
            return False

    def get_all_usernames(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT kullanici_adi FROM kullanicilar")
        return [row[0] for row in cursor.fetchall()]

    def get_all_passwords(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT sifre FROM kullanicilar")
        return [row[0] for row in cursor.fetchall()]

    def update_bildirim_ayarlari(self, kullanici_id, bildirim_istiyor, bildirim_sayisi):
        try:
            cursor = self.conn.cursor()
            # Önce kullanıcının var olup olmadığını kontrol et
            cursor.execute("SELECT id FROM kullanicilar WHERE id = ?", (kullanici_id,))
            if not cursor.fetchone():
                print(f"Kullanıcı bulunamadı: {kullanici_id}")
                return False
                
            # Bildirim ayarlarını güncelle
            cursor.execute("""
                UPDATE kullanicilar 
                SET bildirim_istiyor = ?, bildirim_sayisi = ?
                WHERE id = ?
            """, (1 if bildirim_istiyor else 0, bildirim_sayisi, kullanici_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Bildirim ayarları güncellenirken hata oluştu: {str(e)}")
            return False

    def reset_password(self, email, yeni_sifre):
        """Kullanıcının şifresini sıfırlar"""
        try:
            cursor = self.conn.cursor()
            # E-posta ile kullanıcıyı bul ve şifresini güncelle
            cursor.execute("""
                UPDATE kullanicilar 
                SET sifre = ? 
                WHERE email = ?
            """, (yeni_sifre, email))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Şifre sıfırlama hatası: {str(e)}")
            return False

    def get_user_by_email(self, email):
        """E-posta ile kullanıcı bilgilerini getirir"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM kullanicilar 
                WHERE email = ?
            """, (email,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Kullanıcı bulma hatası: {str(e)}")
            return None

    def close(self):
        self.conn.close()