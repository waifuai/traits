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

class PersonDAO(BaseDAO):
    """Data Access Object for Person-related database operations."""
    def __init__(self):
        super().__init__('persons.db')
        from trait_dao import TraitDAO # Import TraitDAO here to avoid circular dependency
        self.trait_dao = TraitDAO() # Create TraitDAO instance

    def create_tables(self):
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS persons (
                    person TEXT PRIMARY KEY,
                    friendliness REAL,
                    dominance REAL,
                    n_friendliness INTEGER,
                    n_dominance INTEGER
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_friendliness ON persons(friendliness)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_dominance ON persons(dominance)')
            conn.commit()

    def get_all(self) -> List[Dict]:
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT * FROM persons')
            return [
                {
                    'name': row[0],
                    'friendliness': row[1],
                    'dominance': row[2],
                    'n_friendliness': row[3],
                    'n_dominance': row[4]
                }
                for row in cursor.fetchall()
            ]

    def get_person(self, name: str) -> Optional[Dict]:
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT * FROM persons WHERE person=?', (name,))
            row = cursor.fetchone()
            if row:
                return {
                    'name': row[0],
                    'friendliness': row[1],
                    'dominance': row[2],
                    'n_friendliness': row[3],
                    'n_dominance': row[4]
                }
            return None

    def update_personality(self, name: str, personality: personality_models.Personality,
                         n_friendliness: int, n_dominance: int):
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute('''
                UPDATE persons 
                SET friendliness=?, dominance=?, n_friendliness=?, n_dominance=?
                WHERE person=?
            ''', (personality.friendliness, personality.dominance,
                 n_friendliness, n_dominance, name))
            conn.commit()
            
    def reset_database(self): # Added reset_database method
        """Resets the persons database by dropping and recreating the table."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute("DROP TABLE IF EXISTS persons")
            conn.commit()
        self.create_tables() # Recreate the tables

    def add_person(self, name: str):
        """Adds a new person to the database."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute(
                'INSERT INTO persons (person) VALUES (?)',
                (name,)
            )
            conn.commit()

    def add_trait_to_person(self, person_name: str, trait_name: str): # Pass trait_name instead of Trait object
        """Adds a trait to a person and updates the person's personality."""
        from trait_dao import TraitDAO # Import TraitDAO here to avoid circular dependency
        trait_dao = TraitDAO() # Create TraitDAO instance here
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            # Get current person data
            cursor.execute('SELECT friendliness, dominance, n_friendliness, n_dominance FROM persons WHERE person=?', (person_name,))
            row = cursor.fetchone()
            current_friendliness, current_dominance, n_friendliness, n_dominance = row if row else (0.0, 0.0, 0, 0)

            # Get trait personality
            trait_personality = trait_dao.get_trait(trait_name) # Get Trait object using trait_name

            if trait_personality is None:
                print(f"Trait '{trait_name}' not found.")
                return

            # Calculate new weighted average personality
            total_friendliness = (current_friendliness or 0.0) * (n_friendliness or 0) + trait_personality.friendliness
            total_dominance = (current_dominance or 0.0) * (n_dominance or 0) + trait_personality.dominance
            new_n_friendliness = (n_friendliness or 0) + 1
            new_n_dominance = (n_dominance or 0) + 1
            new_friendliness = total_friendliness / new_n_friendliness
            new_dominance = total_dominance / new_n_dominance
            
            # Update person's personality in database
            cursor.execute('''
                UPDATE persons 
                SET friendliness=?, dominance=?, n_friendliness=?, n_dominance=?
                WHERE person=?
            ''', (new_friendliness, new_dominance, new_n_friendliness, new_n_dominance, person_name))
            conn.commit()