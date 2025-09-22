from typing import Tuple

def square_of_number(number: int | float) -> int | float:
    """A function that takes a number and returns its square.

    Args:
        number (int | float): The number to be squared.

    Returns:
        int | float: The square of a given number.
    Raises:
        TypeError: If number is not int or float.
    """
    if not isinstance(number, (int, float)):
        raise TypeError("Input must be int or float")
    return number ** 2

def sum_of_numbers(number_1: int | float, number_2: int | float) -> int | float:
    """A function that takes two numbers and returns their sum.

    Args:
        number_1 (int | float): The first addend.
        number_2 (int | float): The second addend.

    Returns:
        int | float: Sum of the two numbers.
    Raises:
        TypeError: If either argument is not int or float.
    """
    if not isinstance(number_1, (int, float)) or not isinstance(number_2, (int, float)):
        raise TypeError("Both inputs must be int or float")
    return sum([number_1, number_2])

def numbers_division(dividend: int, divisor: int) -> Tuple[float, int, int]:
    """A function that takes two int numbers, performs a division operation, and returns the quotient and remainder.

    Args:
        dividend (int): Dividend.
        divisor (int): Divisor.

    Returns:
        Tuple[float, int, int]: (float division, quotient, remainder).

    Raises:
        ZeroDivisionError: If divisor is 0.
    """
    division_res = dividend / divisor
    quotient = dividend // divisor
    remainder = dividend % divisor
    return division_res, quotient, remainder

