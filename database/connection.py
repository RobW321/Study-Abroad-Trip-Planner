import os
import sqlite3


DATA_DIR = os.environ.get("DATA_DIR", ".")
DATABASE_NAME = os.path.join(DATA_DIR, "studytrip.db")


def get_connection():
    os.makedirs(DATA_DIR, exist_ok=True)
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            destination TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            planned_budget REAL NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY (trip_id) REFERENCES trips(id)
        )
    """)

    connection.commit()
    connection.close()