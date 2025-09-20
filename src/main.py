"""
Main entry point module for the Personality Analysis System.

This module serves as the command-line interface (CLI) for the personality analysis tool.
It provides argument parsing and command routing for all available operations including
trait management, person profile management, and company candidate matching.

The module uses subparsers to organize commands into logical groups:
- trait: Operations for creating and managing personality traits
- person: Operations for creating and updating person profiles
- company: Operations for matching candidates to job descriptions

Functions:
    main: Entry point function that sets up CLI argument parsing and routes commands.
"""

import argparse
import trait_commands
import person_commands
import company_commands


def main():
    parser = argparse.ArgumentParser(
        description="Trait-based personality analysis tool for matching candidates to job descriptions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py person create "John Doe"
  python main.py person add_desc "John Doe" "friendly and outgoing leader"
  python main.py company query "TechCorp" "innovative and collaborative team player"
  python main.py trait create "creative" 8.0 6.0
        """
    )
    parser.add_argument('--version', action='version', version='Personality Analysis Tool v1.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')

    subparsers = parser.add_subparsers(title='commands', dest='command', help='Available commands')

    # Trait commands
    trait_parser = subparsers.add_parser('trait', help='Trait operations')
    trait_subparsers = trait_parser.add_subparsers(title='trait_commands', dest='trait_command', help='Trait sub-commands')

    # Trait creation
    trait_create_parser = trait_subparsers.add_parser('create', help='Create a new personality trait')
    trait_create_parser.add_argument('name', help='Name of the trait (e.g., "friendly", "creative")')
    trait_create_parser.add_argument('friendliness', help='Friendliness score (-10 to 10, where -10 is hostile, 10 is friendly)')
    trait_create_parser.add_argument('dominance', help='Dominance score (-10 to 10, where -10 is submissive, 10 is dominant)')
    trait_create_parser.set_defaults(func=trait_commands.create_trait)

    # List traits
    trait_list_parser = trait_subparsers.add_parser('list', help='List all available traits')
    trait_list_parser.set_defaults(func=trait_commands.list_traits)

    # Person commands
    person_parser = subparsers.add_parser('person', help='Person operations')
    person_subparsers = person_parser.add_subparsers(title='person_commands', dest='person_command', help='Person sub-commands')

    # Person creation
    person_create_parser = person_subparsers.add_parser('create', help='Create a new person profile')
    person_create_parser.add_argument('name', help='Full name of the person')
    person_create_parser.set_defaults(func=person_commands.create_person)

    # Add description to person
    person_add_desc_parser = person_subparsers.add_parser('add_desc', help='Add personality description to a person')
    person_add_desc_parser.add_argument('name', help='Name of the person')
    person_add_desc_parser.add_argument('description', help='Text description containing personality traits (e.g., "friendly, outgoing leader")')
    person_add_desc_parser.set_defaults(func=person_commands.add_description_to_person)

    # List persons
    person_list_parser = person_subparsers.add_parser('list', help='List all person profiles with their personality scores')
    person_list_parser.set_defaults(func=person_commands.list_persons)

    # Company query command
    company_parser = subparsers.add_parser('company', help='Company operations')
    company_subparsers = company_parser.add_subparsers(title='company_commands', dest='company_command', help='Company sub-commands')

    # Query company
    company_query_parser = company_subparsers.add_parser('query', help='Find candidates matching a job description')
    company_query_parser.add_argument('company_name', help='Name of the company or job position')
    company_query_parser.add_argument('company_description', help='Job description containing desired personality traits (e.g., "innovative, collaborative team player")')
    company_query_parser.set_defaults(func=company_commands.query_company_trait_match)

    args = parser.parse_args()

    if args.command:
        if hasattr(args, 'func'):
            args.func(args)
        else:
            print("Error: No valid subcommand provided.")
            parser.print_help()
    else:
        print("No command provided. Use --help for usage information.")
        parser.print_help()


if __name__ == '__main__':
    main()