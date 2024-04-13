"""
Database handlers for the inventory table.
"""

import sqlite3
from db.database import DB_FILE


def insert_record(name, price, details, date):
    """Insert a new record into the inventory table."""

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inventory (name, price, details, date)
                VALUES (?, ?, ?, ?)
            """, (name, price, details, date))
            conn.commit()
        return True
    except sqlite3.Error:
        return False


def delete_record(record_id):
    """Delete a record from the inventory table."""

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM inventory
                WHERE id = ?
            """, (record_id,))
            conn.commit()
        return True
    except sqlite3.Error:
        return False


def get_records_by_date_range(start_date, end_date):
    """Retrieve records from the inventory table within a date range."""

    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM inventory
                WHERE date BETWEEN ? AND ?
            """, (start_date, end_date))
            records = cursor.fetchall()
            records_as_dicts = [dict(record) for record in records]
            return records_as_dicts

    except sqlite3.Error:
        return False
