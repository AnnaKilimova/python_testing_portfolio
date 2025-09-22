import pytest
from ..main import set_union, set_subset
from typing import List, Tuple, Any

# ---------------- Fixtures ----------------
@pytest.fixture
def set_union_test_cases() -> List[Tuple[set[Any], set[Any], set[Any]]]:
    """Fixture that provides test cases for the set_union function.
    
    Returns:
        A list of tuples, where each tuple contains:
        First input set, second input set, the union set of two sets.
    """
    return [
        ({1, 2}, {3, 4}, {1, 2, 3, 4}), # Two sets without intersection
        ({1, 2, 3}, {3, 4, 5}, {1, 2, 3, 4, 5}), # Two sets with intersection
        (set(), {1, 2}, {1, 2}), # One empty, the other non-empty
        (set(), set(), set()), # Both sets are empty
        ({1, "a"}, {2, "b"}, {1, 2, 'b', 'a'}), # Different types of elements
    ]

@pytest.fixture
def set_subset_test_cases() -> List[Tuple[set[Any], set[Any], bool]]:
    """Fixture that provides test cases for the set_subset function.

    Returns:
        A list of tuples, where each tuple contains:
        First input set, second input set, the bool that shows whether one set is a subset of another.
    """
    return [
        # Positive cases.
        ({1, 2}, {1, 2}, True),           # Equal sets.
        ({1}, {1, 2, 3}, True),           # set_1 is a subset of set_2.
        ({1, 2, 3}, {2, 3}, True),        # set_2 is a subset of set_1.
        (set(), {1, 2, 3}, True),         # Empty set - subset of any set.
        (set(), set(), True),             # Two empty sets.
        # Negative cases.
        ({1, 2}, {3, 4}, False),          # Non-intersecting sets.
        ({1, 2}, {2, 3}, False),          # Sets intersect but are not nested.
    ]

class TestSetFunctionsWithFixtures:
    """Grouped pytest tests using fixtures for input data."""
    
    def test_set_union(self, set_union_test_cases: List[Tuple[set[Any], set[Any], set[Any]]]) -> None:
        """Test set_union using fixture-provided test cases.

        Args:
            A list of test cases, where each tuple contains first input set, second input set, the union set of two sets.
        """

        for param_1, param_2, expected in set_union_test_cases:
            result = set_union(param_1, param_2)
            assert result == expected

    def test_set_subset(self, set_subset_test_cases: List[Tuple[set[Any], set[Any], bool]]) -> None:
        """Test set_subset using fixture-provided test cases.

        Args:
            A list of test cases, each tuple contains first input set, second input set, 
            the bool that shows whether one set is a subset of another.
        """
        for param_1, param_2, expected in set_subset_test_cases:
            result = set_subset(param_1, param_2)
            assert result == expected