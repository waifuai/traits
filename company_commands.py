import dao
import company
import personality_models

def query_company_trait_match(args):
    print("query_company_trait_match function called")
    company_instance = company.Company(args.company_name)
    company_description = args.company_description

    # Validate input type
    if not isinstance(company_description, str):
        raise TypeError("Company description must be a string.")

    trait_weights = company_instance._analyze_description(company_description)
    print(f"trait_weights: {trait_weights}")
    print(f"type(trait_weights): {type(trait_weights)}")

    if not trait_weights:
        print("No valid traits found in the company description.")
        return

    trait_dao = dao.TraitDAO()
    trait_personalities = {}
    for trait_name in trait_weights:
        trait = trait_dao.get_trait(trait_name)
        if trait:
            trait_personalities[trait_name] = trait
        else:
            print(f"Warning: Trait '{trait_name}' not found, skipping: {trait_name}")

    if not trait_personalities:
        print("No valid traits found in company description.")
        return

    company_avg_personality = company_instance._weighted_average(trait_personalities, trait_weights)

    print(f"Average company personality: Friendliness={company_avg_personality.friendliness:.2f}, Dominance={company_avg_personality.dominance:.2f}")
    print("\nPersons ranked by personality match:")

    ranked_persons = []
    person_dao = dao.PersonDAO()
    for person_obj in person_dao.get_all():
        person_dict = person_dao.get_person(person_obj['name'])
        if not person_dict:
            continue
        person_personality = personality_models.Personality(person_dict['friendliness'], person_dict['dominance'])
        distance = company_instance._calculate_distance(company_avg_personality, person_personality)
        ranked_persons.append({'person': person_obj['name'], 'distance': distance})

    ranked_persons.sort(key=lambda x: x['distance'])
    for ranked_person in ranked_persons:
        print(f"- {ranked_person['person']}, Distance: {ranked_person['distance']:.2f}")