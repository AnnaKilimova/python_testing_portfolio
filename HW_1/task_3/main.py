from typing import List, Union, Optional
from collections import Counter
from collections.abc import Hashable

def list_avg_value(list_arg: List[Union[int, float]]) -> Optional[float]:
    """A function to calculate the average value of a list of numbers.

    Args:
        list_arg (List[Union[int, float]]): List of numbers.

    Returns:
        float: The average of the list values, or None if the list is empty.
    """
    if not list_arg:
        return None
    return sum(list_arg) / len(list_arg)


def lists_common_elements(list_1: List[Hashable], list_2: List[Hashable]) -> List[Hashable]:
    """A function that takes two lists and returns a list containing the common elements of both lists.

    Args:
        list_1 (List[Hashable]): A list containing hasable type elements.
        list_2 (List[Hashable]): A list containing hasable type elements.

    Returns:
        List[Hashable]: A list containing the common elements of both input lists.
    """
    counter_1 = Counter(list_1)
    counter_2 = Counter(list_2)
    common = counter_1 & counter_2

    return list(common.elements())

# from typing import List, Any

# def lists_common_elements_loop(list_1: List[Any], list_2: List[Any]) -> List[Any]:
#     """A function that takes two lists and returns a list containing the common elements of both lists.

#     Args:
#         list_1 (List[Any]): A list containing elements of any type.
#         list_2 (List[Any]): A list containing elements of any type.

#     Returns:
#         List[Any]: A list containing the common elements of both input lists.
#     """
#     common_list: List[Any]=[]
#     temporary_list = list_2.copy() # In order not to mess up the original list.

#     for element_of_list_1 in list_1:
#         for element_of_list_2 in temporary_list:
#             if element_of_list_1 == element_of_list_2:
#                 common_list.append(element_of_list_1)
#                 temporary_list.remove(element_of_list_2) # Remove to account for multiplicity.
#                 break # To avoid unnecessary duplicates.

#     return common_list


# from typing import List
# from collections.abc import Hashable

# def lists_common_elements_set(list_1: List[Hashable], list_2: List[Hashable]) -> List[Hashable]:
#     """A function that takes two lists and returns a list containing the common elements of both lists without dublicate.
    
#     Args:
#         list_1 (List[Hashable]): A list containing hasable type elements.
#         list_2 (List[Hashable]): A list containing hasable type elements.

#     Returns:
#         List[Hashable]: A list containing the common elements of both input lists.
#     """

#     return list(set(list_1).intersection(set(list_2)))


    
    

