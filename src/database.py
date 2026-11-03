import sqlite3
from pathlib import Path

def connect(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db

def init_db(db_path):
    with connect(db_path) as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS service_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            predicted_category TEXT NOT NULL,
            final_category TEXT NOT NULL,
            confidence REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")

def create_service_request(db_path, description, predicted, final_category, confidence):
    with connect(db_path) as db:
        cur = db.execute("""
        INSERT INTO service_requests
        (description, predicted_category, final_category, confidence)
        VALUES (?, ?, ?, ?)
        """, (description, predicted, final_category, confidence))
        return cur.lastrowid

def get_service_requests(db_path):
    with connect(db_path) as db:
        rows = db.execute("SELECT * FROM service_requests ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]
