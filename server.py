import http.server
import socketserver
import json
import sqlite3
import os
import sys
import random
from urllib.parse import urlparse

PORT = 8086
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arabuluculuk.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mediations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_code TEXT UNIQUE,
            applicant_role TEXT,
            applicant_name TEXT,
            applicant_id TEXT,
            applicant_phone TEXT,
            applicant_email TEXT,
            applicant_address TEXT,
            respondent_name TEXT,
            respondent_id TEXT,
            respondent_phone TEXT,
            respondent_kep TEXT,
            respondent_address TEXT,
            dispute_type TEXT,
            application_category TEXT,
            claim_amount REAL,
            claim_items TEXT,
            dispute_summary TEXT,
            status TEXT DEFAULT 'Başvuru Alındı',
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

class MediationHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self.send_file("index.html", "text/html; charset=utf-8")
        elif path in ("/admin", "/admin.html"):
            self.send_file("admin.html", "text/html; charset=utf-8")
        elif path == "/health":
            self.send_json({"status": "ok", "app": "avukat-arabuluculuk-basvuru-scripti", "port": PORT})
        elif path == "/api/arabuluculuklar":
            self.handle_get_mediations()
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/arabuluculuk-basvur":
            self.handle_create_mediation()
        elif path == "/api/durum-guncelle":
            self.handle_update_status()
        else:
            self.send_error(404, "Endpoint not found")

    def send_file(self, filename, content_type):
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        if not os.path.exists(filepath):
            self.send_error(404, f"File {filename} not found")
            return
        with open(filepath, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def handle_create_mediation(self):
        length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(length)
        try:
            data = json.loads(post_data.decode("utf-8"))
            tracking_code = data.get("tracking_code") or f"ARB-2026-{random.randint(1000, 9999)}"

            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO mediations (
                    tracking_code, applicant_role, applicant_name, applicant_id,
                    applicant_phone, applicant_email, applicant_address,
                    respondent_name, respondent_id, respondent_phone, respondent_kep,
                    respondent_address, dispute_type, application_category,
                    claim_amount, claim_items, dispute_summary, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tracking_code,
                data.get("applicant_role", ""),
                data.get("applicant_name", ""),
                data.get("applicant_id", ""),
                data.get("applicant_phone", ""),
                data.get("applicant_email", ""),
                data.get("applicant_address", ""),
                data.get("respondent_name", ""),
                data.get("respondent_id", ""),
                data.get("respondent_phone", ""),
                data.get("respondent_kep", ""),
                data.get("respondent_address", ""),
                data.get("dispute_type", ""),
                data.get("application_category", ""),
                float(data.get("claim_amount", 0)),
                data.get("claim_items", ""),
                data.get("dispute_summary", ""),
                data.get("status", "Başvuru Alındı"),
                data.get("created_at", "")
            ))
            conn.commit()
            conn.close()

            self.send_json({"status": "success", "tracking_code": tracking_code})
        except Exception as e:
            self.send_json({"status": "error", "message": str(e)}, status=500)

    def handle_get_mediations(self):
        try:
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM mediations ORDER BY id DESC")
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            self.send_json(rows)
        except Exception as e:
            self.send_json({"status": "error", "message": str(e)}, status=500)

    def handle_update_status(self):
        length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(length)
        try:
            data = json.loads(post_data.decode("utf-8"))
            tracking_code = data.get("tracking_code")
            new_status = data.get("status")

            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("UPDATE mediations SET status = ? WHERE tracking_code = ?", (new_status, tracking_code))
            conn.commit()
            conn.close()

            self.send_json({"status": "success", "updated": tracking_code, "new_status": new_status})
        except Exception as e:
            self.send_json({"status": "error", "message": str(e)}, status=500)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", PORT))
    print(f"🚀 Arabuluculuk Portali Baslatildi: http://localhost:{port}")
    print(f"⚖️ Dosya Yonetim Paneli: http://localhost:{port}/admin")
    with socketserver.TCPServer(("", port), MediationHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu kapatildi.")
