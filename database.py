import sqlite3

DB_NAME = "users.db"

def get_db():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            api_key TEXT PRIMARY KEY,
            credits INTEGER NOT NULL
        )
    """)
    db.commit()
    db.close()

def get_user(api_key: str):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT credits FROM users WHERE api_key = ?", (api_key,))
    row = cur.fetchone()
    db.close()
    return row

def deduct_credit(api_key: str):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE users SET credits = credits - 1 WHERE api_key = ?",
        (api_key,)
    )
    db.commit()
    db.close()

def add_user(api_key: str, credits: int):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO users (api_key, credits) VALUES (?, ?)",
        (api_key, credits)
    )
    db.commit()
    db.close()