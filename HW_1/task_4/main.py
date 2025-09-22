from typing import Any, Dict
from collections import defaultdict

def dict_keys_output(dict_param: dict[Any, Any]) -> list[str]:
    """A function that takes a dictionary and outputs all the keys in that dictionary.

    Args:
        dict_val: Input dictionary.

    Returns:
        The list of keys from the dictionary.
    """
    return list(dict_param)

def merged_dictionary(dict_1: Dict[Any, Any], dict_2: Dict[Any, Any]) -> Dict[Any, Any]:
    """Merge two dictionaries into a new dictionary.

    If a key appears in both input dictionaries, the resulting value
    will be a list containing all values for that key.

    Args:
        dict_1: First input dictionary.
        dict_2: Second input dictionary.

    Returns:
        A new dictionary where each key maps to a list of values collected from both dictionaries.
    """
    merged_dict = defaultdict(list)

    for source_dict in (dict_1, dict_2):
        for key, value in source_dict.items():
            merged_dict[key].append(value)

    return dict(merged_dict)



