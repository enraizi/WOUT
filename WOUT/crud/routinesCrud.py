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

def favorite_routine(db_conn, routine_id, user_id):
    """Toggle favorite status for a routine"""
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT is_favorited FROM routines WHERE id = ? AND user_id = ?", 
                      (routine_id, user_id))
        result = cursor.fetchone()
        
        if result:
            current_status = result[0]
            new_status = 1 - current_status
            cursor.execute("UPDATE routines SET is_favorited = ? WHERE id = ? AND user_id = ?",
                          (new_status, routine_id, user_id))
            db_conn.commit()
            return new_status
        return 0
    except Exception as e:
        print(f"Error toggling favorite: {e}")
        return 0

def get_favorite_routines(db_conn, user_id):
    """Get all favorited routines for a user"""
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM routines WHERE user_id = ? AND is_favorited = 1 ORDER BY name", 
                      (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting favorite routines: {e}")
        return []