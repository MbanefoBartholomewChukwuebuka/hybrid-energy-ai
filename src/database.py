import sqlite3
from datetime import datetime

DB_NAME = "energy_monitoring.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        energy_kwh REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_energy(user_id, energy_kwh):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO energy_usage (user_id, energy_kwh, date)
        VALUES (?, ?, ?)
    """, (
        user_id,
        energy_kwh,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()


def get_energy_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT energy_kwh, date
        FROM energy_usage
        WHERE user_id = ?
        ORDER BY date ASC
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()

    return data