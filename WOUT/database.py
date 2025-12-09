# ...existing code...
import sqlite3
import os
import hashlib

def _hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def connect_db(db_path=None):
    """
    Connect to sqlite DB, create file if missing, ensure schema.
    Returns sqlite3.Connection.
    """
    if db_path is None:
        db_path = os.path.join(os.path.dirname(__file__), "wout.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        display_name TEXT NOT NULL DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Add display_name column to existing tables (migration)
    try:
        cur.execute("ALTER TABLE users ADD COLUMN display_name TEXT NOT NULL DEFAULT ''")
    except:
        pass  # Column already exists
    
    # Update existing users with NULL display_name to use their username
    try:
        cur.execute(
            "UPDATE users SET display_name = username WHERE display_name IS NULL OR display_name = ''"
        )
    except:
        pass
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS routines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    conn.commit()
    return conn

def verify_credentials(conn, username, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        return None
    if row["password_hash"] == _hash_password(password):
        return {"id": row["id"], "username": row["username"], "display_name": row["display_name"]}
    return None

def create_user(conn, username, password, display_name=None):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password_hash, display_name) VALUES (?, ?, ?)",
                    (username, _hash_password(password), display_name))
        conn.commit()
        uid = cur.lastrowid
        return {"id": uid, "username": username, "display_name": display_name}
    except sqlite3.IntegrityError:
        return None