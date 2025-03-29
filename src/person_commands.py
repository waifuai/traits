# import dao - No longer needed if importing specific DAOs
# import company - No longer needed
# import models - No longer needed
from person_dao import PersonDAO
from trait_dao import TraitDAO
from services.person_service import PersonService
from personality_models import Personality # Still needed for add_description calculation

def create_person(args):
    """Handles the 'person create' command."""
    # DAO instantiation happens here for now
    person_dao = PersonDAO()
    # Table creation might be better handled centrally
    person_dao.create_tables()
    try:
        # Basic validation might occur in DAO or service later
        person_dao.add_person(args.name)
        print(f"Person '{args.name}' created.")
    except Exception as e: # Catch potential DB errors (e.g., UNIQUE constraint)
        print(f"Error creating person '{args.name}': {e}")

def add_description_to_person(args):
    """Handles the 'person add_desc' command."""
    # Instantiate DAOs and Service
    person_dao = PersonDAO()
    trait_dao = TraitDAO()
    # PersonService instantiation might not be needed if logic remains here temporarily
    # person_service = PersonService(person_dao, trait_dao)

    # TODO: Refactor this command to use PersonService.
    # This requires deciding how description analysis is handled (in PersonService,
    # CompanyService, or a dedicated AnalysisService). The current implementation
    # calculates average personality directly here, bypassing the service layer's
    # intended role and the weighted averaging logic in PersonService.add_trait.

    # --- Start of logic needing refactoring ---
    person = person_dao.get_person(args.name)
    if not person:
        print(f"Error: Person '{args.name}' not found.")
        return

    # Temporary direct analysis (should move)
    words = args.description.lower().split()
    valid_traits = []
    for word in words:
        trait = trait_dao.get_trait(word)
        if trait:
            valid_traits.append(trait)

    if not valid_traits:
        print("No valid traits found in the provided description.")
        return

    # Direct calculation (should use service logic)
    if len(valid_traits) > 0:
        avg_friendliness = sum(p.friendliness for p in valid_traits) / len(valid_traits)
        avg_dominance = sum(p.dominance for p in valid_traits) / len(valid_traits)
        avg_personality = Personality(avg_friendliness, avg_dominance)

        # Direct update (should use service logic)
        # This overwrites existing personality instead of using weighted average.
        # Using len(valid_traits) for n_* is likely incorrect.
        person_dao.update_personality(
            args.name,
            avg_personality,
            person['n_friendliness'] + len(valid_traits), # Incorrectly updating n counts
            person['n_dominance'] + len(valid_traits)  # Incorrectly updating n counts
        )
        print(f"Description '{args.description}' processed for person '{args.name}'. "
              f"(Note: Personality updated via simple average, not weighted trait addition).")
    else:
        print("No valid traits identified in the description.")
    # --- End of logic needing refactoring ---


def list_persons(args):
    """Handles the 'person list' command."""
    person_dao = PersonDAO()
    # Table creation might be better handled centrally
    # person_dao.create_tables() # Avoid creating tables on list command
    try:
        persons = person_dao.get_all()
        if persons:
            print("Persons:")
            for person in persons:
                # Print more details?
                print(f"- {person['name']} (F:{person['friendliness']:.2f}, D:{person['dominance']:.2f})")
        else:
            print("No persons found.")
    except Exception as e:
        print(f"Error listing persons: {e}")