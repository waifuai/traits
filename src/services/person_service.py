from typing import Dict
from personality_models import Personality, PersonStats
from person_dao import PersonDAO
from trait_dao import TraitDAO
# Import Company potentially needed if description analysis stays coupled, or move analysis logic
# from company import Company

class PersonService:
    """Handles business logic related to Person entities."""

    def __init__(self, person_dao: PersonDAO, trait_dao: TraitDAO):
        """
        Initializes the PersonService with data access objects.

        Args:
            person_dao: An instance of PersonDAO.
            trait_dao: An instance of TraitDAO.
        """
        self.person_dao = person_dao
        self.trait_dao = trait_dao

    def add_trait_to_person(self, person_name: str, trait_name: str):
        """Adds a trait to a person and updates their personality."""
        trait = self.trait_dao.get_trait(trait_name)
        if not trait:
            raise ValueError(f"Trait '{trait_name}' not found in database")

        person_dict = self.person_dao.get_person(person_name)
        if not person_dict:
            # Consider creating the person or raising a specific error
            raise ValueError(f"Person '{person_name}' not found.")

        # Map dictionary to PersonStats object
        person_stats = PersonStats(
            name=person_dict['name'],
            personality=Personality(person_dict['friendliness'], person_dict['dominance']),
            n_friendliness=person_dict['n_friendliness'],
            n_dominance=person_dict['n_dominance']
        )

        # Calculate new personality
        new_personality = self._calculate_new_personality(person_stats, trait)

        # Update via DAO
        self.person_dao.update_personality(
            person_name,
            new_personality,
            person_stats.n_friendliness + 1,
            person_stats.n_dominance + 1
        )

    def add_description_to_person(self, person_name: str, description: str):
        """Adds a description and updates personality based on contained traits."""
        # Input validation
        if not isinstance(person_name, str):
            raise TypeError("Person name must be a string")
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        if not person_name.strip():
            raise ValueError("Person name cannot be empty")
        if not description.strip():
            raise ValueError("Description cannot be empty")

        person_name = person_name.strip()
        description = description.strip()

        trait_weights = self._analyze_description_for_traits(description)

        if not trait_weights:
            raise ValueError("No valid traits found in the provided description.")

        added_traits = []
        for trait_name in trait_weights:
            try:
                self.add_trait_to_person(person_name, trait_name)
                added_traits.append(trait_name)
            except ValueError as e:
                print(f"Warning: {e}")  # Log missing traits but continue

        if not added_traits:
            raise ValueError("No valid traits could be added from the description.")

        return added_traits

    def _calculate_new_personality(
        self,
        person: PersonStats,
        trait: Personality
    ) -> Personality:
        """Calculates the new personality based on existing stats and a new trait."""
        # Ensure inputs are valid
        if not isinstance(person, PersonStats) or not isinstance(trait, Personality):
             raise TypeError("Invalid input types for personality calculation.")

        new_friendliness = self._weighted_average(
            person.personality.friendliness,
            trait.friendliness,
            person.n_friendliness
        )
        new_dominance = self._weighted_average(
            person.personality.dominance,
            trait.dominance,
            person.n_dominance
        )
        return Personality(friendliness=new_friendliness, dominance=new_dominance)

    @staticmethod
    def _weighted_average(current: float, new: float, n: int) -> float:
        """Calculates the weighted average of a value."""
        if n < 0:
            raise ValueError("Number of existing values (n) cannot be negative.")
        # Ensure values are floats
        current = float(current)
        new = float(new)
        return ((current * n) + new) / (n + 1)

    def _analyze_description_for_traits(self, description: str) -> Dict[str, float]:
        """Extracts trait names and assigns weights from a description string."""
        if not isinstance(description, str):
            raise TypeError("Description must be a string")

        words = description.lower().split()
        trait_weights = {}
        for word in words:
            if self.trait_dao.get_trait(word):  # Check existence via injected DAO
                trait_weights[word] = 1.0  # Assign weight 1.0 for now
        return trait_weights