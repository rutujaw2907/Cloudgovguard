import sqlite3

DB_PATH = "cloudgov.db"


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
        resource_type TEXT,
        resource_name TEXT,
        metadata TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_name TEXT,
        resource_name TEXT,
        severity TEXT,
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