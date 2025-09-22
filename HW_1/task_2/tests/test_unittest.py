from parameterized import parameterized
import unittest
from ..main import square_of_number, sum_of_numbers, numbers_division



class NumberOperations(unittest.TestCase):
    """Sets of tests to check the functions."""

    @parameterized.expand([
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
        (None, TypeError) 
    ])

    def test_square_of_number(self, given_param: object, expected: object) -> None:
        """Verify that the square_of_number function returns the correct result.

        Args:
            given_param (object): Input value to test.
            expected (object): int | float if the squaring should succeed, or an Exception class if an error is expected.
        """

        if isinstance(expected, type) and issubclass(expected, Exception):
            with self.assertRaises(expected):
                square_of_number(given_param)
        else:
            self.assertEqual(square_of_number(given_param), expected)

    @parameterized.expand([
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
    ])

    def test_sum_of_numbers(self, given_param_1: object, given_param_2: object, expected: object) -> None:
        """Verify that the sum_of_numbers function returns the correct result.

        Args:
            given_param_1 (object): Input value to test.
            given_param_2 (object): Input value to test.
            expected (object): int | float if the summation should succeed, or an Exception class if an error is expected.
        """

        if isinstance(expected, type) and issubclass(expected, Exception):
            with self.assertRaises(expected):
                sum_of_numbers(given_param_1, given_param_2)
        else:
            self.assertEqual(sum_of_numbers(given_param_1, given_param_2), expected)
            
    @parameterized.expand([
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
        (1e-10, 2, 5e-11, 0.0, 1e-10), 
    ])

    def test_numbers_division(self, dividend: int, divisor: int, exp_division_res: float, exp_quotient: int, exp_remainder: int) -> None:
        """Verify that numbers_division returns correct division results.

        Args:
            dividend (int): Dividend input.
            divisor (int): Divisor input.
            exp_division_res (float): Expected result of division as float.
            exp_quotient (int): Expected integer quotient.
            exp_remainder (int): Expected integer remainder.
        
        Note:
            This test assumes divisor != 0. Division by zero is tested separately.
        """

        division_res, quotient, remainder = numbers_division(dividend, divisor)
        self.assertEqual(division_res, exp_division_res)
        self.assertEqual(quotient, exp_quotient)
        self.assertEqual(remainder, exp_remainder)

    def test_numbers_division_zero_divisor(self) -> None:
        """Verify that numbers_division raises ZeroDivisionError when divisor is 0."""
        with self.assertRaises(ZeroDivisionError):
            numbers_division(5, 0)