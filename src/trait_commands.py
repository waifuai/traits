import dao
import models

def create_trait(args):
    # Add validation before creating trait
    try:
        friendliness = float(args.friendliness)
        dominance = float(args.dominance)
    except ValueError:
        print("Error: Friendliness and dominance must be numeric values")
        return

    if not (-10 <= friendliness <= 10) or not (-10 <= dominance <= 10):
        print("Error: Trait values must be between -10 and 10")
        return

    trait_dao = dao.TraitDAO()
    trait_dao.create_tables()
    trait_dao.add_trait(args.name, models.Personality(friendliness, dominance))
    print(f"Trait '{args.name}' created")

def list_traits(args):
    trait_dao = dao.TraitDAO()
    trait_dao.create_tables()
    traits = trait_dao.get_all_traits()
    if traits:
        for trait in traits:
            print(f"{trait['trait']}: Friendliness={trait['friendliness']} Dominance={trait['dominance']}")
    else:
        print("No traits found.")