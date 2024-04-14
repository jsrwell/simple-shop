import os
import sqlite3
import sys

if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(sys.executable)
else:
    basedir = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(basedir, "inventory.db")


def create_table():
    """Create the inventory table."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                details TEXT,
                date DATE
            )
        """)
        conn.commit()


def check_database():
    """Check if the database exists and create it if it doesn't."""
    if not os.path.exists(DB_FILE):
        create_table()


def print_tables():
    """Print all tables and their contents in the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            print(f"Table: {table_name}")
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print()


if __name__ == "__main__":
    check_database()
