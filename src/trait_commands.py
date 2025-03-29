# import dao - No longer needed
# import models - No longer needed
from trait_dao import TraitDAO
from personality_models import Personality # Import the correct Personality model

def create_trait(args):
    """Handles the 'trait create' command."""
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
        trait_dao.add_trait(args.name, personality)
        print(f"Trait '{args.name}' created.")
    except Exception as e: # Catch potential DB errors (e.g., UNIQUE constraint)
        print(f"Error creating trait '{args.name}': {e}")


def list_traits(args):
    """Handles the 'trait list' command."""
    trait_dao = TraitDAO()
    # trait_dao.create_tables() # Removed: Listing should not create tables
    try:
        traits = trait_dao.get_all_traits() # This method returns List[Dict]
        if traits:
            print("Available Traits:")
            for trait in traits:
                # Access dictionary keys
                print(f"- {trait['trait']}: Friendliness={trait['friendliness']:.2f}, Dominance={trait['dominance']:.2f}")
        else:
            print("No traits found.")
    except Exception as e:
        print(f"Error listing traits: {e}")