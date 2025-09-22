from parameterized import parameterized
import unittest
from ..main import str_len, concatenated_str


class StringOperations(unittest.TestCase):
    """Sets of tests to check the functions."""

    @parameterized.expand([
        ("hello", 5),
        ("world", 5),
        ("", 0),
        ("Python", 6)
    ])
    
    def test_str_len(self, input_str: str, expected: int) -> None:
        """Verify that the str_len function returns the correct string length.

        Args:
            input_str (str): input string.
            expected (int): expected string length.
        """
        self.assertEqual(str_len(input_str), expected)

    @parameterized.expand([
        ("Py", "thon", "Python"),
        (" ", 4, TypeError),
    ])

    def test_conc_str(self, input_str_1: str, input_str_2: str, expected: str) -> None:
        """Verify that the concatenated_str function returns the correct result.

        Args:
            input_str_1 (str): the first input string.
            input_str_2 (str): the second input string.
            expected (str): a concatenated string.
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            with self.assertRaises(expected):
                concatenated_str(input_str_1, input_str_2)
        else:
            self.assertEqual(concatenated_str(input_str_1, input_str_2), expected)

    
  

