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
        password TEXT NOT NULL,
        display_name TEXT DEFAULT '',
        created_at TEXT DEFAULT '',
        weight REAL,
        weight_unit TEXT DEFAULT 'kg',
        birthdate TEXT
    );
    """)
    
    # Verify columns exist and add if missing
    cur.execute("PRAGMA table_info(users)")
    columns = {column[1]: column for column in cur.fetchall()}
    
    if 'password' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN password TEXT NOT NULL DEFAULT ''")
    
    if 'display_name' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN display_name TEXT DEFAULT ''")
    
    if 'created_at' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN created_at TEXT DEFAULT ''")
    
    if 'weight' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN weight REAL")
    
    if 'weight_unit' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN weight_unit TEXT DEFAULT 'kg'")
    
    if 'birthdate' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN birthdate TEXT")
    
    if 'workouts' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN workouts INTEGER DEFAULT 0")
    
    if 'streak' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN streak INTEGER DEFAULT 0")
    
    if 'total_time' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN total_time INTEGER DEFAULT 0")
    
    if 'last_login' not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS routines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        notes TEXT,
        is_favorited INTEGER DEFAULT 0,
        created_at TEXT DEFAULT '',
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)
    
    # Verify routines columns
    cur.execute("PRAGMA table_info(routines)")
    routine_columns = {column[1]: column for column in cur.fetchall()}
    
    if 'is_favorited' not in routine_columns:
        cur.execute("ALTER TABLE routines ADD COLUMN is_favorited INTEGER DEFAULT 0")
    
    conn.commit()
    return conn

def verify_credentials(conn, username, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        return None
    if row["password"] == _hash_password(password):
        return {"id": row["id"], "username": row["username"], "display_name": row["display_name"]}
    return None

def create_user(conn, username, password, display_name=None):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password, display_name) VALUES (?, ?, ?)",
                    (username, _hash_password(password), display_name))
        conn.commit()
        uid = cur.lastrowid
        return {"id": uid, "username": username, "display_name": display_name}
    except sqlite3.IntegrityError:
        return None