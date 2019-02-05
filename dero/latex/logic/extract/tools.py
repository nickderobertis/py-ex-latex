from typing import Iterable


def _is_collection(collection, desired_obj_types):
    if isinstance(collection, str):
        return False
    if isinstance(collection, desired_obj_types):
        return False
    return isinstance(collection, Iterable)