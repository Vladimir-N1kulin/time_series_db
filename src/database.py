import sqlite3

# Function to set up the database and create a table if it doesn't exist
def setup_database():
    # Connect to the SQLite database file "time_series.db" (creates it if it doesn't exist)
    conn = sqlite3.connect("time_series.db")
    cursor = conn.cursor()
    # Create a table "time_series_data" with columns:
    # - id: Auto-incremented primary key
    # - timestamp: DATETIME, represents the time of the data (cannot be NULL)
    # - value: TEXT, represents the data value (cannot be NULL)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_series_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            value TEXT NOT NULL
        )
    ''')
    # Commit the table creation operation to the database
    conn.commit()
    return conn, cursor  # Return the connection and cursor for further operations

# Function to insert a record into the "time_series_data" table
def insert_record(cursor, timestamp, value):
    # Execute an SQL INSERT statement with the provided timestamp and value
    cursor.execute("INSERT INTO time_series_data (timestamp, value) VALUES (?, ?)", (timestamp, value))

# Function to search for records that match an exact timestamp
def search_exact_time(cursor, timestamp):
    # Execute an SQL SELECT query to find all records with the given timestamp
    cursor.execute("SELECT * FROM time_series_data WHERE timestamp = ?", (timestamp,))
    # Return all matching rows as a list of tuples
    return cursor.fetchall()

# Function to perform a range query to find records between two timestamps
def range_query(cursor, start_time, end_time):
    # Execute an SQL SELECT query to find all records where the timestamp is within the specified range
    cursor.execute("SELECT * FROM time_series_data WHERE timestamp BETWEEN ? AND ?", (start_time, end_time))
    # Return all matching rows as a list of tuples
    return cursor.fetchall()
