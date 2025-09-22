import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="HW_1/task_1/unit_tests", pattern="test_*.py", top_level_dir=".")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)