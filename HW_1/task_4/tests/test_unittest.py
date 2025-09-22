from parameterized import parameterized
import unittest
from typing import Union, List, Dict, Any, Type
from ..main import dict_keys_output, merged_dictionary


class DictOperations(unittest.TestCase):
    """Grouped unit tests for input data."""

    @parameterized.expand([
        ({"brand": "Ford", "model": "Mustang", "year": 1964}, ['brand', 'model', 'year']),  # Dict with keys of the same type.
        ({"a": 1, 2: "b", (3, 4): "tuple_key"}, ['a', 2, (3, 4)]), # Dictionary with mixed key types.
        ({}, []), # Empty dict.
        ({None: "nothing", "something": 123}, [None, 'something']), # Dictionary with None as a key
    ])
    
    def test_dict_keys_output(self, given_param: object, expected: Union[List[Any], Type[Exception]]) -> None:
        """Test that dict_keys_output returns the expected list of keys or raises an exception.

        Args:
            given_param: The input dictionary to test.
            expected: A list of keys for valid inputs, or an Exception type if an error is expected.
        """
        self.assertEqual(dict_keys_output(given_param), expected)

    @parameterized.expand([
        ({}, {}, {}), # Both dictionaries are empty.
        ({"x": 1}, {}, {'x': [1]}), # One dictionary is empty.
        ({"x": 1}, {"y": 2}, {'x': [1], 'y': [2]}), # Without overlapping keys.
        ({"x": 1, "y": 2}, {"y": 3, "z": 4}, {'x': [1], 'y': [2, 3], 'z': [4]}), # With overlapping keys.
        ({"x": 1, "y": 2}, {"x": 3, "y": 4}, {'x': [1, 3], 'y': [2, 4]}), # Multiple overlapping keys.
        ({1: True, "y": "text"}, {"x": [10], True: 1}, {1: [True, 1], 'y': ['text'], 'x': [[10]]}), # Different types of keys and values.
        ({"a": {"x": 1}}, {"a": {"y": 2}}, {'a': [{'x': 1}, {'y': 2}]}), # Nested dictionaries as values.
        ({"x": None}, {"x": 1}, {'x': [None, 1]}), # None value.
    ])
    
    def test_merged_dictionary(self, given_param_1: Dict[Any, Any], given_param_2: Dict[Any, Any], expected: Dict[Any, Any]) -> None:
        """Verify that lists_merged_dictionary returns the expected result.

        Args:
            given_param_1: First input dictionary.
            given_param_2: Second input dictionary.
            expected: A new dictionary where each key maps to a list of values collected from both dictionaries.
        """
        result = merged_dictionary(given_param_1, given_param_2)
        self.assertEqual(result, expected)