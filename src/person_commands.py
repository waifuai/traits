from typing import Any
from person_dao import PersonDAO
from trait_dao import TraitDAO
from services.person_service import PersonService

def create_person(args: Any) -> None:
    """Handles the 'person create' command."""
    # Input validation
    if not isinstance(args.name, str) or not args.name.strip():
        print("Error: Person name must be a non-empty string.")
        return

    # DAO instantiation happens here for now
    person_dao = PersonDAO()
    # Table creation might be better handled centrally
    person_dao.create_tables()
    try:
        # Basic validation might occur in DAO or service later
        person_dao.add_person(args.name.strip())
        print(f"Person '{args.name}' created successfully.")
    except Exception as e:  # Catch potential DB errors (e.g., UNIQUE constraint)
        print(f"Error creating person '{args.name}': {str(e)}")

def add_description_to_person(args: Any) -> None:
    """Handles the 'person add_desc' command."""
    # Input validation
    if not isinstance(args.name, str) or not args.name.strip():
        print("Error: Person name must be a non-empty string.")
        return
    if not isinstance(args.description, str) or not args.description.strip():
        print("Error: Description must be a non-empty string.")
        return

    # Instantiate DAOs and Service
    person_dao = PersonDAO()
    trait_dao = TraitDAO()
    person_service = PersonService(person_dao, trait_dao)

    try:
        # Use the service layer for proper business logic handling
        added_traits = person_service.add_description_to_person(args.name.strip(), args.description.strip())
        print(f"Description processed for person '{args.name}'.")
        if added_traits:
            print(f"Added traits: {', '.join(added_traits)}")
        print("Personality updated using weighted averaging.")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred while processing description: {str(e)}")


def list_persons(args: Any) -> None:
    """Handles the 'person list' command."""
    person_dao = PersonDAO()
    # Table creation might be better handled centrally
    # person_dao.create_tables() # Avoid creating tables on list command
    try:
        persons = person_dao.get_all()
        if persons:
            print("Persons:")
            for person in persons:
                # Handle missing personality data gracefully
                friendliness = person.get('friendliness', 0.0)
                dominance = person.get('dominance', 0.0)
                print(f"- {person['name']} (F:{friendliness:.2f}, D:{dominance:.2f})")
        else:
            print("No persons found.")
    except Exception as e:
        print(f"Error listing persons: {str(e)}")