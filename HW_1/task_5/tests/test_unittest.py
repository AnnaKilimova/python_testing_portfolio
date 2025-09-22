from parameterized import parameterized
import unittest
from typing import Any
from ..main import set_union, set_subset

class SetOperations(unittest.TestCase):
    """Grouped unit tests for set operations."""

    @parameterized.expand([
        ({1, 2}, {3, 4}, {1, 2, 3, 4}),  # Two sets without intersection
        ({1, 2, 3}, {3, 4, 5}, {1, 2, 3, 4, 5}),  # Two sets with intersection
        (set(), {1, 2}, {1, 2}),  # One empty, the other non-empty
        (set(), set(), set()),  # Both sets are empty
        ({1, "a"}, {2, "b"}, {1, 2, 'b', 'a'}),  # Different types of elements
    ])

    def test_set_union(self, given_param_1: set[Any], given_param_2: set[Any], expected: set[Any]) -> None:
        """Verify that the set_union function returns the expected union of two sets.
        
        Args:
            given_param_1: First input set.
            given_param_2: Second input set.
            expected: the union set of two sets.
        """
        result = set_union(given_param_1, given_param_2)
        self.assertEqual(result, expected)
    
    @parameterized.expand([
        # Positive cases.
        ({1, 2}, {1, 2}, True),           # Equal sets.
        ({1}, {1, 2, 3}, True),           # set_1 is a subset of set_2.
        ({1, 2, 3}, {2, 3}, True),        # set_2 is a subset of set_1.
        (set(), {1, 2, 3}, True),         # Empty set - subset of any set.
        (set(), set(), True),             # Two empty sets.
        # Negative cases.
        ({1, 2}, {3, 4}, False),          # Non-intersecting sets.
        ({1, 2}, {2, 3}, False),          # Sets intersect but are not nested.
    ])

    def test_set_subset(self, given_param_1: set[Any], given_param_2: set[Any], expected: bool) -> None:
        """Verify that the set_subset function correctly identifies subset relationships.
        Args:
            given_param_1: First input set.
            given_param_2: Second input set.
            expected: The union set of two sets.
        """
        result = set_subset(given_param_1, given_param_2)
        self.assertEqual(result, expected)