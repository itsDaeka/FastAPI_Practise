# data/__init__.py
import sqlite3


DB_PATH = "data/spendings.db"

def create_table(db = DB_PATH):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spendings (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            merchant_id INTEGER NOT NULL,
            amount REAL NOT NULL
        );
    """)
    conn.commit()
    conn.close()