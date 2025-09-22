import pytest
from ..main import square_of_number, sum_of_numbers, numbers_division
from typing import List, Tuple, Union, Type

Numeric = Union[int, float]
SquareTestCase = Tuple[Union[Numeric, str, None], Union[Numeric, Type[Exception]]]
SumTestCase = Tuple[Union[Numeric, str, None], Union[Numeric, str, None], Union[Numeric, Type[Exception]]]
DivTestCase = Tuple[int, int, float, int, int]

# ---------------- Fixtures ----------------
@pytest.fixture
def square_of_number_test_cases() -> List[SquareTestCase]:
    """Fixture that provides test cases for the square_of_number function.

    Returns:
        List[SquareTestCase]: A list of tuples, where each tuple contains:
            - input parameter.
            - either the expected squared result (Numeric) or the expected exception type.
    """
    return [
        # Positive cases.
        (3, 9),
        (0, 0),
        (-4, 16),
        (2.5, 6.25),
        (-1.5, 2.25),
        (10**10, 100000000000000000000),
        (1e-10, 1.0000000000000001e-20),
        # Negative cases.
        ("3", TypeError),
        (None, TypeError),
    ]

@pytest.fixture
def sum_of_numbers_test_cases() -> List[SumTestCase]:
    """Fixture that provides test cases for the sum_of_numbers function.

    Returns:
        List[TestCase]: A list of tuples, where each tuple contains:
            - two input parameters.
            - either the expected summed result (Numeric) or the expected exception type.
    """
    return [
        # Positive cases.
        (5, 3, 8), 
        (10, -4, 6), 
        (-7, -2, -9), 
        (0, 9, 9), 
        (3.5, 2.5, 6.0), 
        (3.5, -3, 0.5), 
        (1e10, 1e10, 20000000000.0), 
        (1e-10, 1e-10, 2e-10), 
        # Negative cases.
        (None, 5, TypeError), 
        ("5", 3, TypeError)
    ]

@pytest.fixture
def numbers_division_test_cases() -> List[SumTestCase]:
    """Fixture that provides test cases for the numbers_division function.

    Returns:
        List[TestCase]: A list of tuples, where each tuple contains:
            - two input parameters.
            - either three expected results or ZeroDivisionError.
    """
    return [
        # Positive cases.
        (10, 3, 3.3333333333333335, 3, 1), 
        (20, 5, 4.0, 4, 0), 
        (7, 7, 1.0, 1, 0), 
        (0, 5, 0.0, 0, 0), 
        (5, 10, 0.5, 0, 5), 
        (-10, 3, -3.3333333333333335, -4, 2), 
        (10, -3, -3.3333333333333335, -4, -2), 
        (-10, -3, 3.3333333333333335, 3, -1), 
        (10**10, 3, 3333333333.3333335, 3333333333, 1), 
        (1e-10, 2, 5e-11, 0.0, 1e-10)
    ]

# ---------------- Tests ----------------
class TestNumberFunctionsWithFixtures:
    """Grouped tests using fixtures for input data."""

    def test_square_of_number(self, square_of_number_test_cases: List[SquareTestCase]) -> None:
        """Test square_of_number function using the fixture-provided test cases.

        Args:
            square_of_number_test_cases (List[SquareTestCase]): 
            A list of test cases, where each tuple contains an input parameter 
            and either the expected squared result or an expected exception type.
        """

        for given_param, expected in square_of_number_test_cases:
            if isinstance(expected, type) and issubclass(expected, Exception):
                with pytest.raises(expected):
                    square_of_number(given_param)
            else:
                result = square_of_number(given_param)
                if isinstance(expected, float):
                    # Safer comparison for floating-point results
                    assert result == pytest.approx(expected)
                else:
                    assert result == expected

    def test_sum_of_numbers(self, sum_of_numbers_test_cases: List[SumTestCase]) -> None:
        """Test sum_of_numbers function using the fixture-provided test cases.

        Args:
            sum_of_numbers_test_cases (List[SumTestCase]): 
            A list of test cases, where each tuple contains two input parameters 
            and either the expected summed result or an expected exception type.
        """

        for given_param_1, given_param_2, expected in sum_of_numbers_test_cases:
            if isinstance(expected, type) and issubclass(expected, Exception):
                with pytest.raises(expected):
                    sum_of_numbers(given_param_1, given_param_2)
            else:
                result = sum_of_numbers(given_param_1, given_param_2)
                if isinstance(expected, float):
                    # Safer comparison for floating-point results
                    assert result == pytest.approx(expected)
                else:
                    assert result == expected

    def test_numbers_division(self, numbers_division_test_cases: List[DivTestCase]) -> None:
        """Test numbers_division function using the fixture-provided test cases.

        Args:
           numbers_division_test_cases (List[DivTestCase]): 
           A list of test cases, where each tuple contains two input parameters and the expected three results.

        Note:
            This test assumes divisor != 0. Division by zero is tested separately.
        """
        for dividend, divisor, exp_div_res, exp_quot, exp_rem in numbers_division_test_cases:
            division_res, quotient, remainder = numbers_division(dividend, divisor)
            assert division_res == pytest.approx(exp_div_res)
            assert quotient == exp_quot
            assert remainder == exp_rem

    def test_numbers_division_zero_divisor(self) -> None:
        """Verify that numbers_division raises ZeroDivisionError for divisor = 0."""
        with pytest.raises(ZeroDivisionError):
            numbers_division(5, 0)
