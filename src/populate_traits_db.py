import sqlite3
from db_connection import DB_TIMEOUT

def populate_traits_db():
    """Populate the traits database with default values."""
    conn = sqlite3.connect('traits.db', timeout=DB_TIMEOUT)
    cursor = conn.cursor()

    # Create traits table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traits (
            trait TEXT PRIMARY KEY,
            friendliness REAL,
            dominance REAL
        )
    """)

    # Insert default traits
    traits = [
        ('friendly', 7.0, 6.0),
        ('helpful', 6.0, 4.0),
        ('collaborative', 8.0, 5.0),
        ('outgoing', 9.0, 5.0),
        ('enthusiastic', 8.5, 4.0),
        ('quiet', 3.0, 2.0),
        ('reserved', 2.0, 3.0),
        ('dominant', 6.0, 8.0), # Corrected friendliness for 'dominant' trait
        ('assertive', 7.5, 7.5),
        ('leader', 9.0, 9.0),
        ('strict', 2.0, 8.0), # Added 'strict' trait
        ('agile', 8.0, 7.0), # Added 'agile' trait
        ('innovative', 9.0, 6.0), # Added 'innovative' trait
    ]
    for trait in traits:
        try:
            cursor.execute("INSERT INTO traits VALUES (?, ?, ?)", trait)
        except sqlite3.IntegrityError:
            # Ignore integrity errors, likely due to duplicate entries from previous runs
            pass

    conn.commit()
    conn.close()
    print("Successfully populated traits database with default values.")

if __name__ == '__main__':
    populate_traits_db()