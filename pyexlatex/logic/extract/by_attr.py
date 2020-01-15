from typing import Iterable, Any

# TODO [#8]: refactor extract logic to simplify
#
# logic.extract.by_attr and logic.extract.by_type are very similar, could be refactored

class CouldNotExtractObjsWithAttrException(Exception):
    pass

def extract_objs_with_attr_from_ambiguous_collection(collection, attr: str, attr_value: Any):
    if hasattr(collection, attr) and getattr(collection, attr) == attr_value:
        return collection
    if isinstance(collection, dict):
        return _extract_objs_with_attr_from_dict(collection, attr, attr_value)
    elif isinstance(collection, Iterable):
        return _extract_objs_of_type_from_normal_iterable(collection, attr, attr_value)
    else:
        raise CouldNotExtractObjsWithAttrException(f'could not extract objs from {collection} with attr {attr}={attr_value}')


def _extract_objs_with_attr_from_dict(collection, attr: str, attr_value: Any):
    collected_objs = []
    for key, obj in collection.items():
        if hasattr(obj, attr) and getattr(obj, attr) == attr_value:
            collected_objs.append(obj)
        elif isinstance(obj, dict):
            collected_objs += _extract_objs_with_attr_from_dict(collection, attr, attr_value)
        elif isinstance(obj, Iterable):
            collected_objs += _extract_objs_of_type_from_normal_iterable(obj, attr, attr_value)
        # else, skip the object

    return collected_objs


def _extract_objs_of_type_from_normal_iterable(collection, attr: str, attr_value: Any):
    collected_objs = []
    for obj in collection:
        if hasattr(obj, attr) and getattr(obj, attr) == attr_value:
            collected_objs.append(obj)
        elif isinstance(obj, dict):
            collected_objs += _extract_objs_with_attr_from_dict(collection, attr, attr_value)
        elif isinstance(obj, Iterable):
            collected_objs += _extract_objs_of_type_from_normal_iterable(obj, attr, attr_value)
        # else, skip the object

    return collected_objs
