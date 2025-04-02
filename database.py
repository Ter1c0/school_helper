
import sqlite3
from datetime import datetime

def get_db():
    conn = sqlite3.connect('school_bot.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS homework 
                    (subject TEXT, task TEXT, due_date TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS demo 
                    (subject TEXT, task TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS schedule 
                    (day TEXT, subject TEXT, time TEXT)''')
    return conn

def save_homework(subject, task, due_date):
    with get_db() as db:
        db.execute('INSERT INTO homework VALUES (?, ?, ?)', 
                  (subject, task, due_date))

def save_demo(subject, task):
    with get_db() as db:
        db.execute('INSERT INTO demo VALUES (?, ?)', (subject, task))

def save_schedule(day, subject, time):
    with get_db() as db:
        db.execute('INSERT INTO schedule VALUES (?, ?, ?)', 
                  (day, subject, time))

def get_homework(subject=None):
    with get_db() as db:
        query = '''SELECT subject, task, due_date FROM homework 
                  ORDER BY date(due_date)'''
        if subject:
            query = '''SELECT subject, task, due_date FROM homework 
                      WHERE subject = ? ORDER BY date(due_date)'''
            return db.execute(query, (subject,)).fetchall()
        return db.execute(query).fetchall()

def get_demo():
    with get_db() as db:
        return db.execute('SELECT subject, task FROM demo').fetchall()

def get_schedule():
    with get_db() as db:
        return db.execute('SELECT day, subject, time FROM schedule').fetchall()
