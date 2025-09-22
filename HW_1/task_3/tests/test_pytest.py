import pytest
from ..main import list_avg_value, lists_common_elements
from typing import List, Tuple, Union, Type, Callable
from collections.abc import Hashable

Numeric = Union[int, float]
AvgValTestCase = Tuple[List[Union[Numeric, str, None]], Union[float, None, Type[Exception]]]
ComEllTestCase = Tuple[List[Hashable], List[Hashable], Union[List[Hashable], Type[Exception], Callable[[List[Hashable]], bool]]]

# ---------------- Fixtures ----------------
@pytest.fixture
def list_avg_value_test_cases() -> List[AvgValTestCase]:
    """Fixture that provides test cases for the list_avg_value function.

    Returns:
        List[AvgValTestCase]: 
            A list of tuples, where each tuple contains:
            - an input list of numbers (or invalid values),
            - and either the expected average result (float or None) or the expected exception type.
    """
    return [
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
        (["a", 1, 2], TypeError),
    ]

@pytest.fixture
def lists_common_elements_test_cases() -> List[ComEllTestCase]:
    """Fixture providing test cases for the lists_common_elements function.

    Returns:
        List[ListsCommonElementsTestCase]: 
            A list of tuples, where each tuple contains:
            - first input list of Hashable elements,
            - second input list of Hashable elements,
            - expected result, which can be:
                - List[Hashable] for a normal outcome,
                - Exception class if an error is expected,
                - Callable[[List[Hashable]], bool] for large lists or custom checks.
    """
    return [
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
        ([[1, 2], [3, 4]], [[1, 2], [5, 6]], TypeError), # Lists with mutable objects inside.
    ]

class TestListFunctionsWithFixtures:
    """Grouped tests using fixtures for input data."""

    def test_list_avg_value(self, list_avg_value_test_cases: List[AvgValTestCase]) -> None:
        """Test list_avg_value using fixture-provided test cases.

        Args:
            list_avg_value_test_cases (List[AvgValTestCase]): 
                A list of test cases, where each tuple contains an input list 
                and either the expected average result or the expected exception type.
        """

        for given_param, expected in list_avg_value_test_cases:
            if isinstance(expected, type) and issubclass(expected, Exception):
                with pytest.raises(expected):
                    list_avg_value(given_param)
            else:
                result = list_avg_value(given_param)
                if isinstance(expected, float):
                    # Safer comparison for floating-point results
                    assert result == pytest.approx(expected)
                elif expected is None:
                    assert result is None
                else:
                    assert result == expected

    def test_lists_common_elements(self, lists_common_elements_test_cases: List[AvgValTestCase]) -> None:
        """Test lists_common_elements using fixture-provided test cases.

        Args:
            lists_common_elements_test_cases (List[ListsCommonElementsTestCase]): 
                A list of test cases, each tuple contains:
                - first input list of Hashable elements,
                - second input list of Hashable elements,
                - expected result, which can be:
                    - List[Hashable] for normal output,
                    - Exception class if an error is expected,
                    - Callable[[List[Hashable]], bool] for large lists or custom validation.
        """
        for param_1, param_2, expected in lists_common_elements_test_cases:
            if isinstance(expected, type) and issubclass(expected, Exception):
                with pytest.raises(expected):
                    lists_common_elements(param_1, param_2)
            else:
                result = lists_common_elements(param_1, param_2)
                if callable(expected):
                    assert expected(result)
                else:
                    assert result == expected
