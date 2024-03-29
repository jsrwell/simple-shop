import sqlite3

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect('my_database.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn