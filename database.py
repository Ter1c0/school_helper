# === database.py ===
import sqlite3

def connect_db():
    try:
        return sqlite3.connect('school_bot.db', check_same_thread=False)
    except sqlite3.Error:
        return None

def save_homework(subject, task):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO homework (subject, task) VALUES (?, ?)", (subject, task))
            conn.commit()
        except sqlite3.Error:
            pass
        finally:
            conn.close()

def get_homework(subject):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT task FROM homework WHERE subject = ?", (subject,))
            return cursor.fetchall()
        except sqlite3.Error:
            return []
        finally:
            conn.close()
    return []

def get_demo(subject):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT demo_task FROM demo WHERE subject = ?", (subject,))
            return cursor.fetchall()
        except sqlite3.Error:
            return []
        finally:
            conn.close()
    return []