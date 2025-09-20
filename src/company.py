"""
Company entity module for the Personality Analysis System.

This module defines the Company class which represents a company entity in the system.
The Company class serves as a simple data container for company names, with business
logic and database operations handled by the CompanyService.

Classes:
    Company: Represents a company with basic name validation and representation.
"""

# Removed imports: Personality, PersonDAO, TraitDAO, distance, Dict, List, Tuple

class Company:
    """Represents a company entity, primarily holding its name.
    Analysis and matching operations are managed by CompanyService.
    """
    def __init__(self, name: str):
        """Initializes a Company object.

        Args:
            name: The name of the company.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Company name must be a non-empty string.")
        self.name = name

    def __repr__(self):
        return f"Company(name='{self.name}')"

    # Business logic methods (find_matches, _analyze_description_to_personality, etc.)
    # and helper methods (_calculate_distance, _weighted_average)
    # have been moved to CompanyService or removed as responsibility shifts.
    # Direct DAO interaction has also been removed.
