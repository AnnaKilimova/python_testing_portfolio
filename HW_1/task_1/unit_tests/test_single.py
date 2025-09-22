import unittest
from ..main import str_len, concatenated_str


class StringOperations(unittest.TestCase):
    """Class with tests to check the functions."""

    def test_str_len(self) -> None:
        """Verify that the str_len function returns the correct string length."""

        data = str_len("hello")
        self.assertEqual(data, 5)

    def test_conc_str(self) -> None:
        """Verify that the concatenated_str function returns the correct result."""
        
        data = concatenated_str("Py", "thon")
        self.assertEqual(data, "Python")

        with self.assertRaises(TypeError):
            concatenated_str(" ", 4)


if __name__ == "__main__":
    unittest.main()


