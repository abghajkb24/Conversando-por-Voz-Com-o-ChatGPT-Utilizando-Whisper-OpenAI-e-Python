"""
DB helper (SQLite minimal). Funções:
- init_db(path)
- save_session(session_id, data)
- get_session(session_id)
"""
import sqlite3
import json
from typing import Optional

def init_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_session(db_path: str, session_id: str, data: dict):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    js = json.dumps(data)
    cur.execute("INSERT OR REPLACE INTO sessions (id, data, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (session_id, js))
    conn.commit()
    conn.close()

def get_session(db_path: str, session_id: str) -> Optional[dict]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT data FROM sessions WHERE id = ?", (session_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return json.loads(row[0])