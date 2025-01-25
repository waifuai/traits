import sqlite3
from typing import Tuple

# Constants
DB_TIMEOUT = 5

class DatabaseConnection:
    """Context manager for database connections."""
    def __init__(self, db_name: str):
        self.db_name = db_name
        
    def __enter__(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        self.conn = sqlite3.connect(self.db_name, timeout=DB_TIMEOUT)
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()