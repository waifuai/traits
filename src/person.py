"""
Person entity module for the Personality Analysis System.

This module defines the Person class which represents a person entity in the system.
The Person class serves as a simple data container for person names, with business
logic and database operations handled by the PersonService and DAO layers.

Classes:
    Person: Represents a person with basic name validation and representation.
"""

# Removed imports: Personality, PersonStats, DatabaseConnection, PersonDAO, TraitDAO, Company

class Person:
    """Represents a person entity, primarily holding their name.
    Personality data and operations are managed by PersonService and DAOs.
    """
    def __init__(self, name: str):
        """Initializes a Person object.

        Args:
            name: The name of the person.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Person name must be a non-empty string.")
        self.name = name

    def __repr__(self):
        return f"Person(name='{self.name}')"

    # Business logic methods (add_trait, add_description, _calculate_new_personality, save)
    # and helper methods (_weighted_average, _ensure_in_database)
    # have been moved to PersonService or removed as responsibility shifts.
    # Direct DAO interaction has also been removed.