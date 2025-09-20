"""
Company service module for the Personality Analysis System.

This module contains the business logic layer for company-related operations,
specifically candidate matching based on job descriptions and personality traits.
It implements the core matching algorithm using Euclidean distance calculations.

Classes:
    CompanyService: Handles company matching operations and personality analysis.

The service provides functionality to:
- Analyze job descriptions to extract target personality requirements
- Calculate personality compatibility using weighted averaging
- Rank candidates based on Euclidean distance from target personality
- Provide detailed matching scores and explanations
"""

from personality_models import Personality
from person_dao import PersonDAO
from trait_dao import TraitDAO
from scipy.spatial import distance
from typing import Dict, List, Tuple, Optional # Added Optional

class CompanyService:
    """Handles business logic related to company operations, like matching."""

    def __init__(self, person_dao: PersonDAO, trait_dao: TraitDAO):
        """
        Initializes the CompanyService with data access objects.

        Args:
            person_dao: An instance of PersonDAO.
            trait_dao: An instance of TraitDAO.
        """
        self.person_dao = person_dao
        self.trait_dao = trait_dao

    def find_matches_for_description(self, description: str) -> List[Tuple[str, float]]:
        """
        Finds people matching a personality description and returns a ranked list.

        Args:
            description: The textual description of the desired personality.

        Returns:
            A list of tuples, where each tuple contains (person_name, distance),
            sorted by distance (ascending). Returns empty list if no matches or
            if description yields no valid target personality.
        """
        if not isinstance(description, str):
            raise TypeError("Description must be a string")

        target_personality = self._analyze_description_to_personality(description)
        if target_personality is None:
             print("Warning: No valid traits found in description to form a target personality.")
             return []

        person_dicts = self.person_dao.get_all()
        if not person_dicts:
            return [] # No persons in the database

        distances = []
        for person_dict in person_dicts:
            # Ensure required keys exist and handle potential None values gracefully
            friendliness = person_dict.get('friendliness', 0.0)
            dominance = person_dict.get('dominance', 0.0)
            name = person_dict.get('name')

            if name is None:
                print(f"Warning: Skipping person record with missing name: {person_dict}")
                continue # Skip this record

            person_personality = Personality(
                friendliness=float(friendliness or 0.0), # Handle None/empty string
                dominance=float(dominance or 0.0)   # Handle None/empty string
            )
            dist = self._calculate_distance(person_personality, target_personality)
            distances.append((name, dist))

        # Sort by distance (ascending)
        distances.sort(key=lambda x: x[1])

        return distances

    def _analyze_description_to_personality(self, description: str) -> Optional[Personality]:
        """Analyzes text description to determine an average target personality."""
        trait_weights = self._get_trait_weights_from_description(description)
        if not trait_weights:
            return None # No valid traits found

        traits_data = {}
        for trait_name in trait_weights:
            trait = self.trait_dao.get_trait(trait_name)
            if trait:
                traits_data[trait_name] = trait
            # else: Consider logging missing traits

        if not traits_data:
             return None # No valid traits found after checking DB

        return self._weighted_average(traits_data, trait_weights)

    def _get_trait_weights_from_description(self, description: str) -> Dict[str, float]:
        """Extracts trait names and assigns weights from a description string."""
        words = description.lower().split()
        trait_weights = {}
        for word in words:
            # Check existence via injected DAO
            if self.trait_dao.get_trait(word):
                 trait_weights[word] = 1.0  # Assign weight 1.0 for now
        return trait_weights

    @staticmethod
    def _calculate_distance(p1: Personality, p2: Personality) -> float:
        """Calculates the Euclidean distance between two personalities."""
        if not isinstance(p1, Personality) or not isinstance(p2, Personality):
             raise TypeError("Inputs must be Personality objects")
        return distance.euclidean(
            (p1.friendliness, p1.dominance),
            (p2.friendliness, p2.dominance)
        )

    def _weighted_average(self, traits: Dict[str, Personality], weights: Dict[str, float]) -> Personality:
        """Calculates the weighted average personality from traits and weights."""
        total_weight = sum(weights.get(trait_name, 0) for trait_name in traits)
        if total_weight == 0:
            return Personality(0.0, 0.0) # Return neutral personality

        avg_friendliness = sum(trait.friendliness * weights[trait_name] for trait_name, trait in traits.items()) / total_weight
        avg_dominance = sum(trait.dominance * weights[trait_name] for trait_name, trait in traits.items()) / total_weight

        return Personality(avg_friendliness, avg_dominance)