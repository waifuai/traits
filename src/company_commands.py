"""
Company command-line interface module for the Personality Analysis System.

This module contains functions that handle CLI commands related to company operations,
specifically the company query command which finds and ranks candidates based on
job descriptions using personality trait matching.

Functions:
    query_company_trait_match: Handles the 'company query' command to find personality matches.
"""

from typing import Any
from person_dao import PersonDAO
from trait_dao import TraitDAO
from services.company_service import CompanyService

def query_company_trait_match(args: Any) -> None:
    """Handles the 'company query' command using the CompanyService."""
    # print("query_company_trait_match function called") # Removed debug print
    company_description = args.company_description

    # Basic input validation
    if not isinstance(company_description, str) or not company_description.strip():
        print("Error: Company description must be a non-empty string.")
        return
    if not isinstance(args.company_name, str) or not args.company_name.strip():
        print("Error: Company name must be a non-empty string.")
        return

    # Instantiate DAOs and Service
    person_dao = PersonDAO()
    trait_dao = TraitDAO()
    company_service = CompanyService(person_dao, trait_dao)

    try:
        # Delegate matching logic to the service
        ranked_persons = company_service.find_matches_for_description(company_description)

        if not ranked_persons:
            print(f"No matching persons found for company '{args.company_name}' "
                  f"based on description: '{company_description}'")
            return

        print(f"\nPersons ranked by personality match for '{args.company_name}':")
        # Output results from the service
        for person_name, distance in ranked_persons:
            print(f"- {person_name}, Distance: {distance:.2f}")

    except TypeError as e:
        # Catch type errors potentially raised by service/DAO layers
        print(f"Error during matching process: {e}")
    except Exception as e:
        # Catch unexpected errors
        print(f"An unexpected error occurred: {e}")
        # Consider logging the full traceback here for debugging