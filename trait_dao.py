import sqlite3
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Optional
import personality_models
import db_connection

# Constants
DB_TIMEOUT = 5


class BaseDAO(ABC):
    """Abstract base class for Database Access Objects."""
    def __init__(self, db_name: str):
        self.db_name = db_name

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def get_all(self):
        pass


class TraitDAO(BaseDAO):
    """Data Access Object for Trait-related database operations."""
    def __init__(self):
        super().__init__('traits.db')

    def create_tables(self):
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS traits (
                    trait TEXT PRIMARY KEY,
                    friendliness REAL,
                    dominance REAL
                )
            ''')
            conn.commit()

    def get_all(self) -> Dict[str, personality_models.Personality]: # Corrected return type annotation
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT * FROM traits')
            return {
                row[0]: personality_models.Personality(row[1], row[2])
                for row in cursor.fetchall()
            }

    def get_trait(self, name: str) -> Optional[personality_models.Personality]:
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT * FROM traits WHERE trait=?', (name,))
            row = cursor.fetchone()
            print(f"TraitDAO.get_trait('{name}') - row: {row}") # Debug print
            if row is None: # Explicitly check for None
                return None
            return personality_models.Personality(row[1], row[2])

    def add_trait(self, name: str, personality: personality_models.Personality): # Added add_trait method
        """Adds a new trait to the database."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute(
                'INSERT INTO traits VALUES (?, ?, ?)',
                (name, personality.friendliness, personality.dominance)
            )
            conn.commit()

    def update_trait(self, name: str, personality: personality_models.Personality): # Added update_trait method
        """Updates an existing trait in the database."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute(
                'UPDATE traits SET friendliness=?, dominance=? WHERE trait=?',
                (personality.friendliness, personality.dominance, name)
            )
            conn.commit()

    def get_all_traits(self) -> List[Dict]: # Modified return type to List[Dict]
        """Returns all traits from the database."""
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT trait, friendliness, dominance FROM traits')
            traits_data = cursor.fetchall()
            traits = []
            for row in traits_data:
                trait_name, friendliness, dominance = row
                traits.append({'trait': trait_name, 'friendliness': friendliness, 'dominance': dominance}) # Return dict
            return traits

    def reset_database(self): # Added reset_database method
        """Resets the traits database by dropping and recreating the table."""
        try:
            with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
                cursor.execute("DROP TABLE IF EXISTS traits")
                conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Database lock error during reset: {e}")
        self.create_tables() # Recreate the tables