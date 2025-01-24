import unittest
from test_main_part1 import TestMainPart1
from test_main_part2 import TestMainPart2

def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestMainPart1))
    suite.addTests(loader.loadTestsFromTestCase(TestMainPart2))
    return suite

if __name__ == '__main__':
    unittest.main()