"""
Trait Data Access Object (DAO) module for the Personality Analysis System.

This module provides database access operations for trait-related data, including
CRUD operations, database schema management, and performance optimizations.
It implements the Data Access Object pattern with a base DAO class for common functionality.

Classes:
    BaseDAO: Abstract base class defining the interface for all DAO operations.
    TraitDAO: Concrete implementation for trait database operations with full CRUD support.

The DAO provides functionality for:
- Creating and managing trait database tables with proper indexing
- Adding, updating, and retrieving personality traits
- Input validation and data normalization
- Database reset and recreation capabilities
- Error handling for database constraint violations
"""

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
        # Note: Implementations differ (Dict vs List). Consider refining BaseDAO contract.
        pass


class TraitDAO(BaseDAO):
    """Data Access Object for Trait-related database operations."""
    def __init__(self):
        super().__init__('traits.db')

    def create_tables(self):
        """Creates the traits table if it doesn't exist."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS traits (
                    trait TEXT PRIMARY KEY,
                    friendliness REAL,
                    dominance REAL
                )
            ''')
            # Add indexes for better query performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_trait_name ON traits(trait)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_trait_friendliness ON traits(friendliness)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_trait_dominance ON traits(dominance)')
            conn.commit()

    def get_all(self) -> Dict[str, personality_models.Personality]:
        """Retrieves all traits as a dictionary keyed by trait name."""
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT trait, friendliness, dominance FROM traits')
            return {
                row[0]: personality_models.Personality(row[1], row[2])
                for row in cursor.fetchall()
            }

    def get_trait(self, name: str) -> Optional[personality_models.Personality]:
        """Retrieves a single trait by name."""
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT friendliness, dominance FROM traits WHERE trait=?', (name,))
            row = cursor.fetchone()
            # print(f"TraitDAO.get_trait('{name}') - row: {row}") # Debug print removed
            if row is None:
                return None
            # Assuming row[0] is friendliness, row[1] is dominance
            return personality_models.Personality(row[0], row[1])

    def add_trait(self, name: str, personality: personality_models.Personality):
        """Adds a new trait to the database."""
        # Input validation
        if not isinstance(name, str):
            raise TypeError("Trait name must be a string")
        if not name.strip():
            raise ValueError("Trait name cannot be empty")
        if not isinstance(personality, personality_models.Personality):
            raise TypeError("Personality must be a Personality object")

        name = name.strip().lower()  # Normalize trait names
        if len(name) > 50:  # Reasonable limit
            raise ValueError("Trait name cannot exceed 50 characters")

        # Validate personality scores
        if not (-10 <= personality.friendliness <= 10) or not (-10 <= personality.dominance <= 10):
            raise ValueError("Personality scores must be between -10 and 10")

        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            try:
                cursor.execute(
                    'INSERT INTO traits (trait, friendliness, dominance) VALUES (?, ?, ?)',
                    (name, personality.friendliness, personality.dominance)
                )
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError(f"Trait '{name}' already exists.")

    def update_trait(self, name: str, personality: personality_models.Personality):
        """Updates an existing trait in the database."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute(
                'UPDATE traits SET friendliness=?, dominance=? WHERE trait=?',
                (personality.friendliness, personality.dominance, name)
            )
            conn.commit() # Consider checking cursor.rowcount to ensure update occurred

    def get_all_traits(self) -> List[Dict]:
        """Returns all traits as a list of dictionaries."""
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT trait, friendliness, dominance FROM traits')
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def reset_database(self):
        """Resets the traits database by dropping and recreating the table."""
        try:
            with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
                cursor.execute("DROP TABLE IF EXISTS traits")
                conn.commit()
        except sqlite3.OperationalError as e:
            # Provide more context for the error
            print(f"Database lock error during traits reset: {e}. Ensure no other processes are accessing traits.db.")
        self.create_tables() # Recreate the tables