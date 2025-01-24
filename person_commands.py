import dao
import company
import models

def create_person(args):
    person_dao = dao.PersonDAO()
    person_dao.create_tables()
    person_dao.add_person(args.name)
    print(f"Person '{args.name}' created.")

def add_description_to_person(args):
    try:
        person = models.Person(args.name)
    except ValueError as e:
        print(f"Error: {str(e)}")
        return

    person_dao = dao.PersonDAO()
    person = person_dao.get_person(args.name)
    if not person:
        print(f"Person '{args.name}' not found.")
        return

    company_instance = company.Company("DefaultCompany")
    trait_weights = company_instance._analyze_description(args.description)

    trait_dao = dao.TraitDAO()
    personalities = []
    for trait_name in trait_weights:
        trait = trait_dao.get_trait(trait_name)
        if trait:
            personalities.append(trait)

    if not personalities:
        print("No valid traits found in description.")
        return

    # Calculate average personality
    avg_friendliness = sum(p.friendliness for p in personalities) / len(personalities)
    avg_dominance = sum(p.dominance for p in personalities) / len(personalities)
    avg_personality = models.Personality(avg_friendliness, avg_dominance)

    # Update person's personality in database
    person_dao.update_personality(args.name, avg_personality, len(personalities), len(personalities)) # Use len(personalities) for n_friendliness and n_dominance

    print(f"Description '{args.description}' added to person '{args.name}'.")

def list_persons(args):
    person_dao = dao.PersonDAO()
    person_dao.create_tables()
    persons = person_dao.get_all()
    if persons:
        for person in persons:
            print(person['name'])
    else:
        print("No persons found.")