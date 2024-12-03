import sqlite3

def setup_database():
    conn = sqlite3.connect("time_series.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_series_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

def insert_record(cursor, timestamp, value):
    cursor.execute("INSERT INTO time_series_data (timestamp, value) VALUES (?, ?)", (timestamp, value))

def search_exact_time(cursor, timestamp):
    cursor.execute("SELECT * FROM time_series_data WHERE timestamp = ?", (timestamp,))
    return cursor.fetchall()

def range_query(cursor, start_time, end_time):
    cursor.execute("SELECT * FROM time_series_data WHERE timestamp BETWEEN ? AND ?", (start_time, end_time))
    return cursor.fetchall()
