from typing import Sequence


def item_is_in_allowed_type_strs(item, allowed_values: Sequence[str]) -> bool:
    is_allowed_attrs = [f'is_{value}' for value in allowed_values]
    for allowed_attr in is_allowed_attrs:
        if hasattr(item, allowed_attr) and getattr(item, allowed_attr):
            return True

    return False