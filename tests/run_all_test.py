import unittest
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_all_tests():
    test_dir = os.path.dirname(__file__)
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(test_dir, pattern="test_*.py")

    print(f"Running all tests in {test_dir}...")
    start_time = time.time()
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    end_time = time.time()
    duration = end_time - start_time

    print("\nTotal test execution time: {:.3f} seconds".format(duration))
    if result.wasSuccessful():
        print("All tests passed.")
        exit(0)
    else:
        print("Some tests failed.")
        exit(1)

if __name__ == '__main__':
    run_all_tests()
