import sqlite3

from database.connection import initialize_database


def test_initialize_database():
    initialize_database()

    connection = sqlite3.connect("studytrip.db")

    tables = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name='trips'
    """).fetchall()

    connection.close()

    assert ("trips",) in tables