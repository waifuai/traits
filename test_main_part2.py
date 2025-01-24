import unittest
from dao import PersonDAO, TraitDAO
from models import Person, Personality # Import Personality
from db_connection import DatabaseConnection # Import DatabaseConnection
import sys
from populate_traits_db import populate_traits_db
from main import main

class TestMainPart2(unittest.TestCase): # Renamed class to avoid conflict
    def setUp(self):
        self.person_db = PersonDAO()
        self.trait_db = TraitDAO()
        self.person_db.create_tables()
        self.trait_db.create_tables() # Ensure traits tables are created for testing
        self.person_db.reset_database() # Reset person database
        # self.trait_db.reset_database() # Reset traits database
        populate_traits_db() # Populate traits database

    def test_person_dao_get_all(self):
        person_dao = PersonDAO() # Use PersonDAO instead of PersonDatabase
        person_dao.create_tables()
        person1 = Person("Alice") # Removed extra argument
        person1.save()
        person2 = Person("Bob") # Removed extra argument
        person2.save()
        persons = person_dao.get_all()
        self.assertEqual(len(persons), 2)
        self.assertTrue(any(p['name'] == "Alice" for p in persons)) # Access 'name' key
        self.assertTrue(any(p['name'] == "Bob" for p in persons)) # Access 'name' key

    def test_person_dao_update_personality(self):
        person_dao = PersonDAO()
        person_dao.create_tables()
        person = Person("Alice") # Removed extra argument
        person.save()

    def test_add_nonexistent_trait(self):
        person = Person("TestPerson")
        with self.assertRaises(ValueError):
            person.add_trait("nonexistent_trait")
        print("This line should not be printed if ValueError is raised!") # Debug print after add_trait



    def test_trait_dao_get_trait(self):
        trait_dao = TraitDAO()
        trait_dao.create_tables()
        populate_traits_db()
        trait = trait_dao.get_trait("friendly")
        self.assertIsNotNone(trait)
        self.assertGreater(trait.friendliness, 0)

    def test_trait_dao_update_trait(self):
        trait_dao = TraitDAO()
        trait_dao.create_tables()
        populate_traits_db()
        trait_dao.update_trait("friendly", Personality(10.0, 10.0))
        updated_trait = trait_dao.get_trait("friendly")
        self.assertEqual(updated_trait.friendliness, 10.0)
        self.assertEqual(updated_trait.dominance, 10.0)

    def test_cli_list_persons(self):
        # Simulate: python main.py person list
        person_dao = PersonDAO()
        person_dao.reset_database()
        person1 = Person("Alice") # Removed extra argument
        person1.save()
        person2 = Person("Bob") # Removed extra argument
        person2.save()
        sys.argv = ["main.py", "person", "list"]
        main()
        # In a real test, you might want to capture stdout to assert the output
        # For now, we'll just check that the command runs without errors

    def test_cli_list_traits(self):
        # Simulate: python main.py trait list
        trait_dao = TraitDAO()
        trait_dao.create_tables()
        populate_traits_db()
        sys.argv = ["main.py", "trait", "list"]
        main()
        # In a real test, you might want to capture stdout to assert the output
        # For now, we'll just check that the command runs without errors

    def test_integration_workflow(self):
        # Create a trait
        sys.argv = ["main.py", "trait", "create", "test_trait", "3.0", "7.0"]
        main()

        # Add the trait to a person
        sys.argv = ["main.py", "person", "add_desc", "TestPerson", "test_trait"] # Corrected to person add_desc
        main()

        # Verify company matches
        sys.argv = ["main.py", "company", "query", "TestCo", "test_trait"]
        main()
        # In a real test, you might want to capture stdout to assert the output
        # For now, we'll just check that the command runs without errors

    def test_database_connection_context_manager(self):
        # Test the DatabaseConnection context manager
        db_name = 'test_db.db'
        try:
            with DatabaseConnection(db_name) as (conn, cursor):
                self.assertIsNotNone(conn)
                self.assertIsNotNone(cursor)
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.assertEqual(result, (1,))
        except Exception as e:
            self.fail(f"DatabaseConnection context manager failed: {e}")
        finally:
            # Clean up the test database file
            import os
            if os.path.exists(db_name):
                os.remove(db_name)


    def tearDown(self): # Added tearDown to part2 to avoid conflict if both parts are run
        # self.person_db.close() # Removed close calls as PersonDAO and TraitDAO don't have close methods
        # self.trait_db.close()
        pass

# if __name__ == '__main__':
#    unittest.main()
