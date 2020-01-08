from pyexlatex.logic.extract.tools import _is_collection


def extract_objs_of_type_from_ambiguous_collection(collection, obj_types):
    collected_objs = []
    if isinstance(collection, dict):
        collected_objs += _extract_objs_of_type_from_dict(collection, obj_types)
    elif _is_collection(collection, obj_types):
        collected_objs += _extract_objs_of_type_from_normal_iterable(collection, obj_types)
    elif isinstance(collection, obj_types):
        collected_objs.append(collection)
    else:
        raise ValueError(f'could not extract objs from {collection} of type {type(collection)}')

    return collected_objs


def _extract_objs_of_type_from_dict(collection, obj_types):
    collected_objs = []
    for key, obj in collection.items():
        if isinstance(collection, dict):
            collected_objs += _extract_objs_of_type_from_dict(collection, obj_types)
        elif _is_collection(obj, obj_types):
            collected_objs += extract_objs_of_type_from_ambiguous_collection(obj, obj_types)
        elif isinstance(obj, obj_types):
            collected_objs.append(obj)
        # else, skip the object

    return collected_objs


def _extract_objs_of_type_from_normal_iterable(collection, obj_types):
    collected_objs = []
    for obj in collection:
        if isinstance(collection, dict):
            collected_objs += _extract_objs_of_type_from_dict(collection, obj_types)
        elif _is_collection(obj, obj_types):
            collected_objs += extract_objs_of_type_from_ambiguous_collection(obj, obj_types)
        elif isinstance(obj, obj_types):
            collected_objs.append(obj)
        # else, skip the object

    return collected_objs


