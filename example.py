# Створіть функцію, яка приймає список чисел і повертає новий список, що містить тільки парні числа.

def even_odd_check(list_of_numbers: list[int]) -> list[int]:
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


print(even_odd_check(list(range(0, 11))))
print(even_odd_check([1, 2, 3, 4, 5]))  # [2, 4]
print(even_odd_check([2, 4, 6]))  # [2, 4, 6]
print(even_odd_check([1, 3, 5]))  # []
print(even_odd_check([]))  # []
print(even_odd_check([-5, -4, -3, -2, -1, 0]))  # [-4, -2, 0]
print(even_odd_check([10**6, 10**6 + 1]))  # [1000000]