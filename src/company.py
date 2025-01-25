from personality_models import Personality
from dao import TraitDAO, PersonDAO
from scipy.spatial import distance
from dao import TraitDAO, PersonDAO
from scipy.spatial import distance
from typing import Dict, Optional, List

from models import Company as CompanyModel
from trait_dao import TraitDAO

class Company(CompanyModel):
    """Represents a company searching for people with specific personalities."""
    def __init__(self, name: str):
        self.name = name
        self.person_dao = PersonDAO()

    def find_matches(self, description: str) -> List[str]:
        """Find people matching a personality description."""
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        target_personality = self._analyze_description(description)
        person_dicts = self.person_dao.get_all() # Get list of dictionaries
        
        distances = [
            (person_dict['name'], self._calculate_distance(
                Personality(person_dict['friendliness'], person_dict['dominance']), # Create Personality object
                target_personality
            ))
            for person_dict in person_dicts
        ]
        
        return [name for name, _ in sorted(distances, key=lambda x: x[1])]

    def _analyze_description(self, description: str) -> Dict[str, float]:
        """Analyze text description to determine trait weights."""
        trait_dao = TraitDAO()
        words = description.lower().split()
        trait_weights = {}
        for word in words:
            trait = trait_dao.get_trait(word)
            if trait:
                trait_weights[word] = 1.0  # Assign weight 1.0 for valid traits
        return trait_weights

    @staticmethod
    def _calculate_distance(
        p1: Personality,
        p2: Personality
    ) -> float:
        """Calculate distance between two personalities."""
        return distance.euclidean(
            (p1.friendliness, p1.dominance),
            (p2.friendliness, p2.dominance)
        )

    def _weighted_average(self, traits: Dict[str, Personality], weights: Dict[str, float]) -> Personality:
        """Calculate weighted average personality from traits and weights."""
        avg_friendliness = sum(traits[trait].friendliness * weights[trait] for trait in traits)
        avg_dominance = sum(traits[trait].dominance * weights[trait] for trait in traits)
        return Personality(avg_friendliness, avg_dominance)
