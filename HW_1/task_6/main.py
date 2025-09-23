def even_odd_check(number: int) -> None:
    """A function that checks whether a number is even or odd.

    Args:
        number: Input number

    Returns: None
    """
    if number % 2 == 0:
        print("Even")
    else:
        print("Odd")

even_odd_check(0)  # Even
even_odd_check(2)  # Even
even_odd_check(3)  # Odd
even_odd_check(-4)  # Even
even_odd_check(-7)  # Odd
even_odd_check(10**6)  # Even
even_odd_check(10**6 + 1)  # Odd

def even_only_check(list_of_numbers: list[int]) -> list[int]:
    """A function that takes a list of numbers and returns a new list containing only even numbers.

    Args:
        list_of_numbers: Input list of numbers.

    Returns: A new list containing only even numbers.
    """
    new_list = []

    for element in list_of_numbers:
        if element % 2 == 0:
            new_list.append(element)

    return new_list

print(even_only_check(list(range(0, 11)))) # [0, 2, 4, 6, 8, 10]
print(even_only_check([1, 2, 3, 4, 5]))  # [2, 4]
print(even_only_check([2, 4, 6]))  # [2, 4, 6]
print(even_only_check([1, 3, 5]))  # []
print(even_only_check([]))  # []
print(even_only_check([-5, -4, -3, -2, -1, 0]))  # [-4, -2, 0]
print(even_only_check([10**6, 10**6 + 1]))  # [1000000]