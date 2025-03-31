import sqlite3
from datetime import datetime
from pathlib import Path

DB_DIR = Path("data")
DB_PATH = DB_DIR / "scoreboard.db"


def init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def insert(name: str, time: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    c.execute(
        "INSERT INTO scores (name, time, date) VALUES (?, ?, ?)", (name, time, date)
    )
    conn.commit()
    conn.close()


def select(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, time, date FROM scores ORDER BY time ASC LIMIT ?", (limit,))
    results = c.fetchall()
    conn.close()
    return results
