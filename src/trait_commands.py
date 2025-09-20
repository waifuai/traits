"""
Trait command-line interface module for the Personality Analysis System.

This module contains functions that handle CLI commands related to trait operations,
including creating new personality traits and listing all available traits with
their friendliness and dominance scores.

Functions:
    create_trait: Handles the 'trait create' command to create new personality traits.
    list_traits: Handles the 'trait list' command to display all available traits.
"""

from typing import Any
from trait_dao import TraitDAO
from personality_models import Personality # Import the correct Personality model

def create_trait(args: Any) -> None:
    """Handles the 'trait create' command."""
    # Input validation
    if not isinstance(args.name, str) or not args.name.strip():
        print("Error: Trait name must be a non-empty string.")
        return

    # Validation
    try:
        friendliness = float(args.friendliness)
        dominance = float(args.dominance)
    except ValueError:
        print("Error: Friendliness and dominance must be numeric values.")
        return

    if not (-10 <= friendliness <= 10) or not (-10 <= dominance <= 10):
        print("Error: Trait values must be between -10 and 10.")
        return

    # Instantiate DAO directly
    trait_dao = TraitDAO()
    # Table creation might be better handled centrally (e.g., on app startup or via a setup command)
    trait_dao.create_tables()
    try:
        # Create Personality object from validated data
        personality = Personality(friendliness, dominance)
        trait_dao.add_trait(args.name.strip(), personality)
        print(f"Trait '{args.name}' created successfully.")
    except Exception as e:  # Catch potential DB errors (e.g., UNIQUE constraint)
        print(f"Error creating trait '{args.name}': {str(e)}")


def list_traits(args: Any) -> None:
    """Handles the 'trait list' command."""
    trait_dao = TraitDAO()
    # trait_dao.create_tables() # Removed: Listing should not create tables
    try:
        traits = trait_dao.get_all_traits()  # This method returns List[Dict]
        if traits:
            print("Available Traits:")
            for trait in traits:
                # Handle missing data gracefully
                trait_name = trait.get('trait', 'Unknown')
                friendliness = trait.get('friendliness', 0.0)
                dominance = trait.get('dominance', 0.0)
                print(f"- {trait_name}: Friendliness={friendliness:.2f}, Dominance={dominance:.2f}")
        else:
            print("No traits found.")
    except Exception as e:
        print(f"Error listing traits: {str(e)}")