import unittest
import main
import dao
import models
import db_connection
import sys
import populate_traits_db

class TestMainPart1(unittest.TestCase): # Renamed class to avoid conflict
    def setUp(self):
        self.person_db = dao.PersonDAO()
        self.trait_db = dao.TraitDAO()
        self.person_db.reset_database() # Reset persons database
        self.trait_db.reset_database() # Reset traits database
        self.person_db.create_tables()
        self.trait_db.create_tables() # Ensure traits tables are created for testing
        # populate_traits_db.populate_traits_db() # Remove populate_traits_db() from setUp

    def test_add_person_and_traits(self):
        person_name = "Alice"
        description = "friendly dominant"

        # Create traits "friendly" and "dominant" if they don't exist
        trait_dao = dao.TraitDAO()
        if not trait_dao.get_trait("friendly"):
            trait_dao.add_trait("friendly", models.Personality(7.0, 6.0)) # Example personality values
        if not trait_dao.get_trait("dominant"):
            trait_dao.add_trait("dominant", models.Personality(6.0, 8.0)) # Example personality values


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
        person1 = models.Person("Alice") # Removed extra argument
        person1.add_description("friendly", self.trait_db)
        person2 = models.Person("Bob") # Removed extra argument
        person2.add_description("dominant", self.trait_db)

        company_name = "TestCo"
        company_description = "friendly and dominant"

        # Simulate command line arguments for querying a company
        sys.argv = ["main.py", "company"] # Simplified test_query_company test
        main.main()

        # In a real test, you might want to capture stdout to assert the output
        # For now, we'll just check that the command runs without errors

    def test_calculate_personality_distance(self):
        company = models.Company("TestCo")
        p1 = models.Personality(3.0, 4.0)
        p2 = models.Personality(0.0, 0.0)
        distance = company._calculate_distance(p1, p2)
        self.assertAlmostEqual(distance, 5.0)  # 3² + 4² = 25 → sqrt(25) = 5

    def test_create_trait_via_cli(self):
        # Simulate: python main.py trait create "strict" 2.0 8.0
        sys.argv = ["main.py", "trait", "create", "strict", "2.0", "8.0"]
        main.main()
        # Verify trait exists
        # Assuming TraitDAO is accessible or you adjust accordingly
        trait = dao.TraitDAO().get_trait("strict")
        self.assertEqual(trait.friendliness, 2.0)
        self.assertEqual(trait.dominance, 8.0)

    def test_calculate_weighted_average(self):
        company = models.Company("TestCo")
        traits = {
            "friendly": models.Personality(2.0, 3.0),
            "dominant": models.Personality(4.0, 5.0)
        }
        weights = {
            "friendly": 0.6,
            "dominant": 0.4
        }
        average_personality = company._weighted_average(traits, weights)
        expected_friendliness = 2.0 * 0.6 + 4.0 * 0.4
        expected_dominance = 3.0 * 0.6 + 5.0 * 0.4
        self.assertAlmostEqual(average_personality.friendliness, expected_friendliness)
        self.assertAlmostEqual(average_personality.dominance, expected_dominance) # Fixed typo here

    def test_analyze_description(self):
        company = models.Company("TestCo")
        description = "friendly dominant strict"
        trait_weights = company._analyze_description(description)
        expected_weights = {"friendly": 1.0, "dominant": 1.0, "strict": 1.0}
        self.assertEqual(trait_weights, expected_weights)
