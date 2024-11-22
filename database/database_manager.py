import sqlite3

class DatabaseConnection:
    def __init__(self, database_path):
        self.database_path = database_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()  
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()  


database_connection = DatabaseConnection('database/mydb.db')

def init_database():
    with database_connection as cursor:
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
            survey_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        ''')

