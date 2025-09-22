def str_len(str_val: str) -> int:
    """This function takes a string and returns its length.

    Args:
        str_val (str): the input string to measure.

    Returns:
        int: the length of the string taken.
    """
    return len(str_val)

# print(str_len("hello"))
# print(str_len("world"))
# print(str_len(""))
# print(str_len("Python"))


def concatenated_str(str_1: str, str_2: str) -> str:
    """This function takes two strings and returns a concatenated string.

    Args:
        str_1 (str): the first input string.
        str_2 (str): the second input string.

    Returns:
        str: a concatenated string.
    """
    new_str = str_1 + str_2
    return new_str

# print(concatenated_str("Py", "thon"))
# print(concatenated_str("", 5))