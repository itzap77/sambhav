import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'store.db')
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), 'schema.sql')

def initialize():
    print("Initializing database...")
    connection = sqlite3.connect(DB_FILE)
    
    with open(SCHEMA_FILE) as f:
        connection.executescript(f.read())
        
    connection.commit()
    connection.close()
    print(f"Database created successfully at {DB_FILE}")

if __name__ == '__main__':
    initialize()
