import pytest
from ..main import str_len, concatenated_str
from typing import Union, Type


class TestStringFunctions:
    """Grouped tests for string utility functions."""

    @pytest.mark.parametrize("param, expected", [
        ("hello", 5),
        ("world", 5),
        ("", 0),
        ("Python", 6),
    ])
    def test_str_len(self, param: str, expected: int) -> None:
        """
        Test that str_len returns the correct length of a string.

        Args:
            param (str): The input string to measure.
            expected (int): The expected length of the input string.

        Returns:
            None: Test passes if assertion is True.
        """
        assert str_len(param) == expected

    @pytest.mark.parametrize("param_1, param_2, expected", [
        ("Py", "thon", "Python"),          # normal case
        ("Hello", "World", "HelloWorld"),  # normal case
        (" ", 4, TypeError),               # expected error
        (5, "abc", TypeError),             # expected error
        (None, "xyz", TypeError),          # expected error
    ])
    def test_conc_str(self, param_1: str, param_2: str, expected: Union[str, Type[Exception]]) -> None:
        """
        Test that concatenated_str returns the correct concatenated string,
        or raises a TypeError when invalid types are provided.

        Args:
            param_1 (str): The first input string.
            param_2 (str): The second input string.
            expected (Union[str, Type[Exception]]): The expected result:
                - a string if the concatenation should succeed,
                - an exception class if an error is expected.

        Returns:
            None: Test passes if assertion succeeds or exception is raised.
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                concatenated_str(param_1, param_2)
        else:
            assert concatenated_str(param_1, param_2) == expected

