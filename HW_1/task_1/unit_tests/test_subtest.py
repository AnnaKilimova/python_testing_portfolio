import unittest
from ..main import str_len, concatenated_str


class StringOperations(unittest.TestCase):
    """A set of tests to check the str_len function."""

    def test_multiple_strings(self) -> None:
        """Verify that the str_len function returns the correct string length."""
        
        test_cases = [
            ("hello", 5),
            ("world", 5),
            ("", 0),
            ("Python", 6)
        ]

        # subTest is a method of the unittest.TestCase class.
        # When testing multiple values, if a simple loop was written without a subTest string, and if one of the cases fails, the loop will stop, and unittest will only show the first error.
        # With subTest, each case is considered separately. If one fails, the others continue to run, and unittest will show a detailed report: which one failed the test.
        for param, expected in test_cases:
            with self.subTest(param=param):
                self.assertEqual(str_len(param), expected)

    
    def test_conc_str(self) -> None:
        """Verify that the concatenated_str function returns the correct result."""
        
        test_cases = [
            ("Py", "thon", "Python"),
            (" ", 4, TypeError)
        ]

        for param_1, param_2, expected in test_cases:
            with self.subTest(param_1=param_1, param_2=param_2):
                if isinstance(expected, type) and issubclass(expected, Exception):
                    with self.assertRaises(expected):
                        concatenated_str(param_1, param_2)
                else:
                    self.assertEqual(concatenated_str(param_1, param_2), expected)
