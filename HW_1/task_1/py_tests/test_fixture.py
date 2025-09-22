import pytest
from ..main import str_len, concatenated_str
from typing import List, Tuple, Union, Type


@pytest.fixture
def str_len_test_cases() -> List[Tuple[str, int]]:
    """
    Fixture that provides test cases for the str_len function.

    Returns:
        List[Tuple[str, int]]: A list of tuples, where each tuple contains:
            - input string (str)
            - expected length (int)
    """
    return [
        ("hello", 5),
        ("world", 5),
        ("", 0),
        ("Python", 6),
    ]


@pytest.fixture
def concatenated_str_test_cases() -> List[Tuple[str, str, Union[str, Type[Exception]]]]:
    """
    Fixture that provides test cases for the concatenated_str function.

    Returns:
        List[Tuple[str, str, Union[str, Type[Exception]]]]: A list of tuples, where each tuple contains:
            - first input string (str)
            - second input string (str)
            - expected result (str if concatenation succeeds, Exception class if error expected)
    """
    return [
        ("Py", "thon", "Python"),          # positive case
        ("Hello", "World", "HelloWorld"),  # positive case
        (" ", 4, TypeError),               # negative case
        (5, "abc", TypeError),             # negative case
        (None, "xyz", TypeError),          # negative case
    ]


class TestStringFunctionsWithFixtures:
    """Grouped tests using fixtures for input data."""

    def test_str_len(self, str_len_test_cases: list) -> None:
        """
        Test str_len function using the fixture-provided test cases.

        Args:
            str_len_test_cases (List[Tuple[str, int]]): List of input strings and expected lengths.
        """
        for input_str, expected in str_len_test_cases:
            assert str_len(input_str) == expected

    def test_conc_str(self, concatenated_str_test_cases: list) -> None:
        """
        Test concatenated_str function using the fixture-provided test cases.

        Args:
            concatenated_str_test_cases (List[Tuple[str, str, Union[str, Type[Exception]]]]): 
                List of tuples containing two input strings and expected result or expected exception.
        """
        for param_1, param_2, expected in concatenated_str_test_cases:
            if isinstance(expected, type) and issubclass(expected, Exception):
                with pytest.raises(expected):
                    concatenated_str(param_1, param_2)
            else:
                assert concatenated_str(param_1, param_2) == expected
