import argparse
import trait_commands
import person_commands
import company_commands


def main():
    print("main function called")
    parser = argparse.ArgumentParser(description="Trait-based personality analysis tool.")
    subparsers = parser.add_subparsers(title='commands', dest='command', help='Available commands')

    # Trait commands
    trait_parser = subparsers.add_parser('trait', help='Trait operations')
    trait_subparsers = trait_parser.add_subparsers(title='trait_commands', dest='trait_command', help='Trait sub-commands')

    # Trait creation
    trait_create_parser = trait_subparsers.add_parser('create', help='Create a new trait')
    trait_create_parser.add_argument('name', help='Trait name')
    trait_create_parser.add_argument('friendliness', help='Friendliness value')
    trait_create_parser.add_argument('dominance', help='Dominance value')
    trait_create_parser.set_defaults(func=trait_commands.create_trait)

    # List traits
    trait_list_parser = trait_subparsers.add_parser('list', help='List all traits')
    trait_list_parser.set_defaults(func=trait_commands.list_traits)

    # Person commands
    person_parser = subparsers.add_parser('person', help='Person operations')
    person_subparsers = person_parser.add_subparsers(title='person_commands', dest='person_command', help='Person sub-commands')

    # Person creation
    person_create_parser = person_subparsers.add_parser('create', help='Create a new person')
    person_create_parser.add_argument('name', help='Person name')
    person_create_parser.set_defaults(func=person_commands.create_person)

    # Add description to person
    person_add_desc_parser = person_subparsers.add_parser('add_desc', help='Add a description to a person')
    person_add_desc_parser.add_argument('name', help='Person name')
    person_add_desc_parser.add_argument('description', help='Description of the person (e.g., "friendly dominant")')
    person_add_desc_parser.set_defaults(func=person_commands.add_description_to_person)

    # List persons
    person_list_parser = person_subparsers.add_parser('list', help='List all persons')
    person_list_parser.set_defaults(func=person_commands.list_persons)

    # Company query command
    company_parser = subparsers.add_parser('company', help='Company operations')
    company_subparsers = company_parser.add_subparsers(title='company_commands', dest='company_command', help='Company sub-commands')

    # Query company
    company_query_parser = company_subparsers.add_parser('query', help='Query company personality match')
    company_query_parser.add_argument('company_name', help='Company name')
    company_query_parser.add_argument('company_description', help='Company description to analyze (e.g., "innovative agile")')
    company_query_parser.set_defaults(func=company_commands.query_company_trait_match)

    args = parser.parse_args()
    print(f"main - args: {args}")
    print(f"main - args.command: {args.command}")

    if args.command:
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()