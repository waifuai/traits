"""
Person Data Access Object (DAO) module for the Personality Analysis System.

This module provides database access operations for person-related data, including
CRUD operations and database schema management. It implements the Data Access Object
pattern with a base DAO class for common functionality.

Classes:
    BaseDAO: Abstract base class defining the interface for all DAO operations.
    PersonDAO: Concrete implementation for person database operations.
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
        pass

class PersonDAO(BaseDAO):
    """Data Access Object for Person-related database operations."""
    def __init__(self):
        super().__init__('persons.db')
        # Removed TraitDAO import and instantiation

    def create_tables(self):
        """Creates the persons table and indexes if they don't exist."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS persons (
                    person TEXT PRIMARY KEY,
                    friendliness REAL DEFAULT 0.0,
                    dominance REAL DEFAULT 0.0,
                    n_friendliness INTEGER DEFAULT 0,
                    n_dominance INTEGER DEFAULT 0
                )
            ''')
            # Add indexes for better query performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_friendliness ON persons(friendliness)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_dominance ON persons(dominance)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_person_name ON persons(person)')
            conn.commit()

    def get_all(self) -> List[Dict]:
        """Retrieves all persons from the database."""
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT person, friendliness, dominance, n_friendliness, n_dominance FROM persons')
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_person(self, name: str) -> Optional[Dict]:
        """Retrieves a single person by name."""
        with db_connection.DatabaseConnection(self.db_name) as (_, cursor):
            cursor.execute('SELECT person, friendliness, dominance, n_friendliness, n_dominance FROM persons WHERE person=?', (name,))
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None

    def update_personality(self, name: str, personality: personality_models.Personality,
                         n_friendliness: int, n_dominance: int):
        """Updates the personality scores and counts for a given person."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute('''
                UPDATE persons
                SET friendliness=?, dominance=?, n_friendliness=?, n_dominance=?
                WHERE person=?
            ''', (personality.friendliness, personality.dominance,
                 n_friendliness, n_dominance, name))
            conn.commit()

    def reset_database(self):
        """Drops and recreates the persons table."""
        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            cursor.execute("DROP TABLE IF EXISTS persons")
            conn.commit()
        self.create_tables() # Recreate the tables

    def add_person(self, name: str):
        """Adds a new person to the database with default personality values."""
        # Input validation
        if not isinstance(name, str):
            raise TypeError("Person name must be a string")
        if not name.strip():
            raise ValueError("Person name cannot be empty")

        name = name.strip()
        if len(name) > 100:  # Reasonable limit
            raise ValueError("Person name cannot exceed 100 characters")

        with db_connection.DatabaseConnection(self.db_name) as (conn, cursor):
            try:
                cursor.execute(
                    # Ensure default values are set correctly if not provided
                    'INSERT INTO persons (person, friendliness, dominance, n_friendliness, n_dominance) VALUES (?, 0.0, 0.0, 0, 0)',
                    (name,)
                )
                conn.commit()
            except sqlite3.IntegrityError:
                # Handle cases where the person might already exist
                raise ValueError(f"Person '{name}' already exists.")

    # Removed add_trait_to_person method - logic moved to PersonService