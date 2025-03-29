import unittest
import main
from person_dao import PersonDAO
from trait_dao import TraitDAO
from person import Person
from company import Company
from personality_models import Personality
from services.company_service import CompanyService
import db_connection
import sys
import populate_traits_db

class TestMainPart1(unittest.TestCase): # Renamed class to avoid conflict
    def setUp(self):
        self.person_db = PersonDAO()
        self.trait_db = TraitDAO()
        self.person_db.reset_database() # Reset persons database
        self.trait_db.reset_database() # Reset traits database
        self.person_db.create_tables()
        self.trait_db.create_tables() # Ensure traits tables are created for testing
        populate_traits_db.populate_traits_db() # Populate traits for tests

    def test_add_person_and_traits(self):
        person_name = "Alice"
        description = "friendly dominant"

        # Create traits "friendly" and "dominant" if they don't exist
        trait_dao = TraitDAO()
        if not trait_dao.get_trait("friendly"):
            trait_dao.add_trait("friendly", Personality(7.0, 6.0)) # Example personality values
        if not trait_dao.get_trait("dominant"):
            trait_dao.add_trait("dominant", Personality(6.0, 8.0)) # Example personality values


        # Simulate command line arguments for creating a person
        sys.argv = ["main.py", "person", "create", person_name]
        main.main()

        # Simulate command line arguments for adding a description to the person
        sys.argv = ["main.py", "person", "add_desc", person_name, description]
        main.main()

        # Verify person is added and traits are updated
        with db_connection.DatabaseConnection(self.person_db.db_name) as (conn, cursor): # Use DatabaseConnection context manager
            cursor.execute('SELECT friendliness, dominance FROM persons WHERE person = ?', (person_name,))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            friendliness, dominance = result
            self.assertIsNotNone(friendliness) # Assert not None
            self.assertIsNotNone(dominance) # Assert not None
            self.assertGreater(friendliness, 0)
            self.assertGreater(dominance, 0)

    def test_query_company_command(self):
        # Add some persons to the database for querying
        # TODO: Refactor test setup to use services or CLI commands for adding descriptions
        person1 = Person("Alice") # Create Person object
        # person1.add_description("friendly", self.trait_db) # Commented out - add_description removed from Person
        self.person_db.add_person("Alice") # Add person directly via DAO for now
        person2 = Person("Bob") # Create Person object
        # person2.add_description("dominant", self.trait_db) # Commented out - add_description removed from Person
        self.person_db.add_person("Bob") # Add person directly via DAO for now

        company_name = "TestCo"
        company_description = "friendly and dominant"

        # Simulate command line arguments for querying a company
        sys.argv = ["main.py", "company"] # Simplified test_query_company test
        main.main()

        # In a real test, you might want to capture stdout to assert the output
        # For now, we'll just check that the command runs without errors

    def test_calculate_personality_distance(self):
        # Instantiate service with DAOs from setUp
        company_service = CompanyService(self.person_db, self.trait_db)
        p1 = Personality(3.0, 4.0)
        p2 = Personality(0.0, 0.0)
        # Call the static method on the service class (or an instance)
        distance = company_service._calculate_distance(p1, p2)
        self.assertAlmostEqual(distance, 5.0)  # 3² + 4² = 25 → sqrt(25) = 5

    def test_create_trait_via_cli(self):
        # Simulate: python main.py trait create "strict" 2.0 8.0
        sys.argv = ["main.py", "trait", "create", "strict", "2.0", "8.0"]
        main.main()
        # Verify trait exists
        # Assuming TraitDAO is accessible or you adjust accordingly
        trait = TraitDAO().get_trait("strict")
        self.assertEqual(trait.friendliness, 2.0)
        self.assertEqual(trait.dominance, 8.0)

    def test_calculate_weighted_average(self):
        # Instantiate service with DAOs from setUp
        company_service = CompanyService(self.person_db, self.trait_db)
        traits = {
            "friendly": Personality(2.0, 3.0),
            "dominant": Personality(4.0, 5.0)
        }
        weights = {
            "friendly": 0.6,
            "dominant": 0.4
        }
        # Call the method on the service instance
        average_personality = company_service._weighted_average(traits, weights)
        expected_friendliness = 2.0 * 0.6 + 4.0 * 0.4
        expected_dominance = 3.0 * 0.6 + 5.0 * 0.4
        self.assertAlmostEqual(average_personality.friendliness, expected_friendliness)
        self.assertAlmostEqual(average_personality.dominance, expected_dominance)

    def test_analyze_description(self):
        # Instantiate service with DAOs from setUp
        company_service = CompanyService(self.person_db, self.trait_db)
        description = "friendly dominant strict"
        # Call the relevant method on the service instance
        # Note: This test assumes 'strict' trait exists. Add it in setUp if needed.
        trait_weights = company_service._get_trait_weights_from_description(description)
        expected_weights = {"friendly": 1.0, "dominant": 1.0, "strict": 1.0} # Assumes strict exists
        self.assertEqual(trait_weights, expected_weights)
