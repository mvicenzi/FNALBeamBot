import sqlite3
from scripts.config import db_file

def init_db():

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            timestamp INTEGER PRIMARY KEY,
            date TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_timestamp_in_db(timestamp):

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT timestamp FROM messages WHERE timestamp = ?', (timestamp,))
    result = c.fetchone()
    conn.close()
    return result is not None

def insert_message(timestamp, date, message):

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('INSERT INTO messages (timestamp, date, message) VALUES (?, ?, ?)', 
              (timestamp, date, message))
    conn.commit()
    conn.close()

def remove_timestamp_in_db(timestamp):

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('DELETE FROM messages WHERE timestamp = ?', (timestamp,))
    conn.commit()
    conn.close()
