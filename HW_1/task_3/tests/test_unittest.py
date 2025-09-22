from parameterized import parameterized
import unittest
from typing import Union, Type, List, Callable
from collections.abc import Hashable
from ..main import list_avg_value, lists_common_elements


class ListOperations(unittest.TestCase):
    """Grouped unit tests for input data."""

    @parameterized.expand([
        # Positive cases.
        ([0, 1, 2, 3, 4, 5], 2.5), 
        ([1, 2, 3], 2.0), 
        ([-1, 0, 1], 0.0), 
        ([5], 5.0), 
        ([-1.5, 2.5, 3.5], 1.5), 
        ([1, 2.5], 1.75), 
        ([10**10, 1e-1, 4], 3333333334.7000003), 
        (list(range(1_000_000)), 499999.5),
        ([], None), 
        # Negative cases.

        (["a", 1, 2], TypeError) 
    ])
    
    def test_list_avg_value(self, given_param: object, expected: Union[float, None, Type[Exception]]) -> None:
        """Verify that the list_avg_value function returns the expected result.

        Args:
            given_param (object): Input value to test, usually a list of numbers.
            expected (Union[float, None, Type[Exception]]): a float for valid inputs, 
            None if the list is empty, or an Exception type if an error is expected.
        """

        if isinstance(expected, type) and issubclass(expected, Exception):
            with self.assertRaises(expected):
                list_avg_value(given_param)
        else:
            self.assertEqual(list_avg_value(given_param), expected)

    @parameterized.expand([
        # Positive cases.
        ([1, 2, 3], [2, 3, 4], [2, 3]), # The usual case with intersection.
        ([1, 2, 3, 4, 5], [3], [3]), # Lists of varying lengths.
        ([1, 2, 3], [4, 5, 6], []), # No common elements.
        ([1, 2, 3], [1, 2, 3], [1, 2, 3]), # Full coincidence.
        ([], [1, 2, 3], []), # Empty list + non-empty.
        ([], [], []), # Both lists are empty.
        ([1, 1, 2, 2], [2, 2, 3], [2, 2]), # Duplicates within lists.
        ([1, "a", 2.0], ["a", 2, 2.0], ["a", 2.0]), # Different types of data.
        ([None, 1, 2], [None, 3], [None]), # Lists with None.
        (list(range(1_000_000)), list(range(500_000, 1_500_000)), lambda result: set(result) == set(range(500_000, 1_000_000))), # Very large lists.
        # Negative cases.
        ([[1, 2], [3, 4]], [[1, 2], [5, 6]], TypeError) # Lists with mutable objects inside.
    ])
    
    def test_lists_common_elements(self, given_param_1: object, given_param_2: object, expected: Union[List[Hashable], Type[Exception], "Callable[[List[Hashable]], bool]"]) -> None:
        """Verify that lists_common_elements returns the expected result.

        Args:
            given_param_1 (object): First input list.
            given_param_2 (object): Second input list.
            expected (Union[List[Hashable], Type[Exception], Callable[[List[Hashable]], bool]]):
                - List[Hashable] if the function should succeed and return common elements,
                - Exception class if the function should raise an error,
                - Callable (e.g., lambda) that accepts the result list and returns True if it is correct (used for large lists).
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            with self.assertRaises(expected):
                lists_common_elements(given_param_1, given_param_2)
        else:
            result = lists_common_elements(given_param_1, given_param_2)
            if callable(expected):
                self.assertTrue(expected(result))
            else:
                self.assertEqual(result, expected)