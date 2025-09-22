import pytest
from ..main import str_len, concatenated_str


@pytest.mark.parametrize("param, expected", [
    ("hello", 5),
    ("world", 5),
    ("", 0),
    ("Python", 6),
])

def test_str_len(param: str, expected: int) -> None:
    """Test that str_len returns the correct length of a string.

    Args:
        param (str): the input string to measure.
        expected (int): the expected length of the input string.

    Returns:
        None: This is a test function; result is checked via assertion.
    """
    assert str_len(param) == expected


@pytest.mark.parametrize("param_1, param_2, expected", [
    ("Py", "thon", "Python"),
    (" ", 4, TypeError),
])

def test_conc_str(param_1: str, param_2: str, expected: object) -> None:
    """Test that concatenated_str returns the correct concatenated string, or 
    raises a TypeError when invalid types are provided.

    Args:
        param_1 (str): The first input string.
        param_2 (str): The second input string.
        expected (Union[str, Type[Exception]]): The expected result:
            - a string if the concatenation should succeed,
            - an exception class if an error is expected.

    Returns:
        None: This is a test function; result is checked via assertion or exception.
    """
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            concatenated_str(param_1, param_2)
    else:
        assert concatenated_str(param_1, param_2) == expected