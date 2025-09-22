from typing import Any

def set_union(set_1: set[Any], set_2: set[Any]) -> set[Any]:
    """A function that takes two sets and returns their union.

    Args:
        set_1: First input set.
        set_2: Second input set.

    Return the union of two sets.
    """
    return set_1.union(set_2)



def set_subset(set_1: set[Any], set_2: set[Any]) -> bool:
    """A function that checks whether one set is a subset of another.

    Args:
        set_1: First input set.
        set_2: Second input set.

    Returns:
        bool: True if either set_1 is a subset of set_2, or set_2 is a subset of set_1. False otherwise.
    """
    return set_1.issubset(set_2) or set_2.issubset(set_1)

