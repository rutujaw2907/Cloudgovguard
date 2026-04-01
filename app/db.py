import sqlite3
from app.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT,
        resource_type TEXT,
        resource_name TEXT,
        raw_data TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_id TEXT,
        policy_name TEXT,
        framework TEXT,
        control_id TEXT,
        severity TEXT,
        resource_name TEXT,
        resource_type TEXT,
        reason TEXT,
        remediation TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_score INTEGER,
        critical_count INTEGER,
        high_count INTEGER,
        medium_count INTEGER,
        low_count INTEGER
    )
    """)

    conn.commit()
    conn.close()