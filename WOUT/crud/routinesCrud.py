# ...existing code...
def create_routine(conn, user_id, name, notes=None):
    cur = conn.cursor()
    cur.execute("INSERT INTO routines (user_id, name, notes) VALUES (?, ?, ?)", (user_id, name, notes))
    conn.commit()
    return cur.lastrowid

def get_routine(conn, routine_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM routines WHERE id = ?", (routine_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_routines(conn, user_id=None):
    cur = conn.cursor()
    if user_id:
        cur.execute("SELECT * FROM routines WHERE user_id = ? ORDER BY id DESC", (user_id,))
    else:
        cur.execute("SELECT * FROM routines ORDER BY id DESC")
    rows = cur.fetchall()
    return [dict(r) for r in rows]

def update_routine(conn, routine_id, name=None, notes=None):
    cur = conn.cursor()
    if name and notes is not None:
        cur.execute("UPDATE routines SET name = ?, notes = ? WHERE id = ?", (name, notes, routine_id))
    elif name:
        cur.execute("UPDATE routines SET name = ? WHERE id = ?", (name, routine_id))
    elif notes is not None:
        cur.execute("UPDATE routines SET notes = ? WHERE id = ?", (notes, routine_id))
    conn.commit()

def delete_routine(conn, routine_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM routines WHERE id = ?", (routine_id,))
    conn.commit()
# ...existing code...