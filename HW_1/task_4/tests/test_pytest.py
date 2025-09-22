import pytest
from ..main import dict_keys_output, merged_dictionary
from typing import Tuple, Dict, List, Any, Type

# ---------------- Fixtures ----------------
@pytest.fixture
def dict_keys_output_test_cases() -> List[Tuple[Dict[Any, Any], List[Any]]]:
    """Fixture that provides test cases for the dict_keys_output function.

    Returns:
        A list of tuples, where each tuple contains:
            - Input dictionary.
            - The list of keys from the dictionary..
    """

    return [
        ({"brand": "Ford", "model": "Mustang", "year": 1964}, ['brand', 'model', 'year']),  # Dict with keys of the same type.
        ({"a": 1, 2: "b", (3, 4): "tuple_key"}, ['a', 2, (3, 4)]), # Dictionary with mixed key types.
        ({}, []), # Empty dict.
        ({None: "nothing", "something": 123}, [None, 'something']), # Dictionary with None as a key
    ]

@pytest.fixture
def merged_dictionary_test_cases() -> List[Tuple[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]]:
    """Fixture providing test cases for the merged_dictionary function.

    Returns:
        A list of tuples, where each tuple contains:
            - First input dictionary.
            - Second First input dictionary.
            - Expected result as a new dictionary where each key maps to a list of values collected from both dictionaries.
    """
    return [
        ({}, {}, {}), # Both dictionaries are empty.
        ({"x": 1}, {}, {'x': [1]}), # One dictionary is empty.
        ({"x": 1}, {"y": 2}, {'x': [1], 'y': [2]}), # Without overlapping keys.
        ({"x": 1, "y": 2}, {"y": 3, "z": 4}, {'x': [1], 'y': [2, 3], 'z': [4]}), # With overlapping keys.
        ({"x": 1, "y": 2}, {"x": 3, "y": 4}, {'x': [1, 3], 'y': [2, 4]}), # Multiple overlapping keys.
        ({1: True, "y": "text"}, {"x": [10], True: 1}, {1: [True, 1], 'y': ['text'], 'x': [[10]]}), # Different types of keys and values.
        ({"a": {"x": 1}}, {"a": {"y": 2}}, {'a': [{'x': 1}, {'y': 2}]}), # Nested dictionaries as values.
        ({"x": None}, {"x": 1}, {'x': [None, 1]}), # None value.
    ]

class TestDictFunctionsWithFixtures:
    """Grouped tests using fixtures for input data."""

    def test_dict_keys_output(self, dict_keys_output_test_cases: List[Tuple[Dict[Any, Any], List[Any]]]) -> None:
        """Test dict_keys_output using fixture-provided test cases.

        Args:
            dict_keys_output_test_cases: A list of test cases, where each tuple 
            contains an input dictionary and the expected list of keys.
        """

        for given_param, expected in dict_keys_output_test_cases:
            result = dict_keys_output(given_param)
            assert result == expected

    def test_merged_dictionary(self, merged_dictionary_test_cases: List[Tuple[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]]) -> None:
        """Test merged_dictionary using fixture-provided test cases.

        Args:
            - First input dictionary.
            - Second input dictionary.
            - Expected result as a new dictionary where each key maps to a list of values collected from both dictionaries.
        """
        for param_1, param_2, expected in merged_dictionary_test_cases:
            result = merged_dictionary(param_1, param_2)
            assert result == expected
