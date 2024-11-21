import sqlite3

def init_db():
    conn = sqlite3.connect('db/mydb.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS survey (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        number_of_people INTEGER NOT NULL,
        age INTEGER NOT NULL,
        time TEXT NOT NULL,
        user_ip TEXT NOT NULL,
        checked BOOLEAN NOT NULL DEFAULT 0,
        approved BOOLEAN NOT NULL DEFAULT 0,
        comment TEXT,
        time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    )
    ''')

    conn.commit()
    conn.close()

