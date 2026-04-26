import sqlite3
import os

DB_NAME = "appointments_poc.db"


def get_conn():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_conn()
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id            INTEGER PRIMARY KEY,
            full_name     TEXT NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            phone         TEXT,
            password_hash TEXT NOT NULL,
            auth_token    TEXT,
            created_at    TEXT DEFAULT (datetime('now'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments(
            id               INTEGER PRIMARY KEY,
            user_id          INTEGER,
            patient_name     TEXT,
            doctor_name      TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            patient_email    TEXT,
            status           TEXT,
            created_at       TEXT DEFAULT (datetime('now'))
        )
    """)

    existing = [row[1] for row in cur.execute("PRAGMA table_info(appointments)").fetchall()]
    for col in ["appointment_date", "appointment_time", "patient_email", "user_id", "created_at"]:
        if col not in existing:
            cur.execute(f"ALTER TABLE appointments ADD COLUMN {col} TEXT")

    conn.commit()
    conn.close()