from personality_models import Personality, PersonStats
from dao import PersonDAO, TraitDAO, DatabaseConnection
from dao import PersonDAO, TraitDAO, DatabaseConnection

class Person:
    """Represents a person with personality traits and interactions."""
    def __init__(self, name: str):
        self.name = name
        self.dao = PersonDAO()
        self._ensure_in_database()

    def _ensure_in_database(self):
        if not self.dao.get_person(self.name):
            self.dao.create_tables()
            with DatabaseConnection('persons.db') as (conn, cursor):
                cursor.execute(
                    'INSERT INTO persons VALUES (?, ?, ?, ?, ?)',
                    (self.name, 0, 0, 0, 0)
                )
                conn.commit()

    def add_trait(self, trait_name: str):
        trait_dao = TraitDAO()
        trait = trait_dao.get_trait(trait_name)
        print(f"Trait '{trait_name}' retrieved: {trait}") # Debug print

        if not trait:
            print("Inside if not trait block!") # Debug print inside if block
            print("About to raise ValueError!") # Debug print just before raise
            raise ValueError(f"Trait '{trait_name}' not found in database")

        person_dict = self.dao.get_person(self.name) # Get dictionary
        if not person_dict:
            return
        person_stats = PersonStats( # Create PersonStats object
            name=person_dict['name'],
            personality=Personality(person_dict['friendliness'], person_dict['dominance']),
            n_friendliness=person_dict['n_friendliness'],
            n_dominance=person_dict['n_dominance']
        )

        new_personality = self._calculate_new_personality(person_stats, trait)
        self.dao.update_personality(
            self.name,
            new_personality,
            person_stats.n_friendliness + 1,
            person_stats.n_dominance + 1
        )

    def _calculate_new_personality(
        self,
        person: PersonStats,
        trait: Personality
    ) -> Personality:
        """Calculate new personality values after adding a trait."""
        return Personality(
            friendliness=self._weighted_average(
                person.personality.friendliness,
                trait.friendliness,
                person.n_friendliness
            ),
            dominance=self._weighted_average(
                person.personality.dominance,
                trait.dominance,
                person.n_dominance
            )
        )

    @staticmethod
    def _weighted_average(
        current: float,
        new: float,
        n: int
    ) -> float:
        """Calculate weighted average when adding a new value."""
        return ((current * n) + new) / (n + 1)