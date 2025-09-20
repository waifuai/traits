"""
Database initialization script for the Personality Analysis System.

This script resets and populates the traits database with default personality traits
by calling the TraitDAO reset functionality and the populate_traits_db module.

This script is typically run during system setup or when databases need to be
reinitialized with default data.
"""

import populate_traits_db
from trait_dao import TraitDAO

if __name__ == '__main__':
    trait_db = TraitDAO()
    trait_db.reset_database()
    populate_traits_db.populate_traits_db()