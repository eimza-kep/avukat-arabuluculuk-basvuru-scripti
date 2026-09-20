import unittest
import os
import sys
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import server

class TestMediationSystem(unittest.TestCase):
    def setUp(self):
        server.init_db()
        self.conn = sqlite3.connect(server.DB_FILE)
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute("DELETE FROM mediations WHERE tracking_code LIKE 'ARB-TEST%'")
        self.conn.commit()

    def tearDown(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM mediations WHERE tracking_code LIKE 'ARB-TEST%'")
        self.conn.commit()
        self.conn.close()

    def test_database_table_exists(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mediations'")
        row = cur.fetchone()
        self.assertIsNotNone(row, "mediations tablosu oluşturulmuş olmalıdır.")

    def test_mediation_insert_and_retrieve(self):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO mediations (
                tracking_code, applicant_role, applicant_name, applicant_id,
                applicant_phone, applicant_email, applicant_address,
                respondent_name, respondent_id, respondent_phone, respondent_kep,
                respondent_address, dispute_type, application_category,
                claim_amount, claim_items, dispute_summary, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "ARB-TEST-001",
            "İşçi / Çalışan",
            "Ahmet Yılmaz",
            "12345678901",
            "05551112233",
            "ahmet@example.com",
            "Kadıköy, İstanbul",
            "ABC Lojistik A.Ş.",
            "1234567890",
            "02161234567",
            "abc@hs01.kep.tr",
            "Ümraniye, İstanbul",
            "İş Hukuku (İşçi - İşveren)",
            "Dava Şartı (Zorunlu) Arabuluculuk",
            95000.00,
            "Kıdem Tazminatı, İhbar Tazminatı, Fazla Mesai",
            "3 yıllık çalışma sonrası haksız fesih.",
            "Başvuru Alındı",
            "2026-09-20T10:00:00Z"
        ))
        self.conn.commit()

        cur.execute("SELECT * FROM mediations WHERE tracking_code = 'ARB-TEST-001'")
        record = cur.fetchone()
        self.assertIsNotNone(record)
        self.assertEqual(record["applicant_name"], "Ahmet Yılmaz")
        self.assertEqual(record["respondent_name"], "ABC Lojistik A.Ş.")
        self.assertEqual(record["claim_amount"], 95000.00)

    def test_status_update(self):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO mediations (tracking_code, applicant_name, status)
            VALUES (?, ?, ?)
        """, ("ARB-TEST-002", "Zeynep Kaya", "Başvuru Alındı"))
        self.conn.commit()

        cur.execute("UPDATE mediations SET status = ? WHERE tracking_code = ?", ("İlk Toplantı Belirlendi", "ARB-TEST-002"))
        self.conn.commit()

        cur.execute("SELECT status FROM mediations WHERE tracking_code = 'ARB-TEST-002'")
        updated_status = cur.fetchone()[0]
        self.assertEqual(updated_status, "İlk Toplantı Belirlendi")

    def test_files_exist(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assertTrue(os.path.exists(os.path.join(base_dir, "index.html")), "index.html bulunamadı")
        self.assertTrue(os.path.exists(os.path.join(base_dir, "admin.html")), "admin.html bulunamadı")
        self.assertTrue(os.path.exists(os.path.join(base_dir, "api.php")), "api.php bulunamadı")

if __name__ == "__main__":
    unittest.main()
