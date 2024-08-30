import sqlite3
import os
DATABASE = 'users.db'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Insert a sample user (for testing purposes)
        cursor.execute("INSERT INTO users (username, password) VALUES ('shrish', 'Pa$$word')")
        conn.commit()
        conn.close()
init_db()