from typing import Optional

from pyexlatex.typing import ListOrDictOrItem, StrListOrNone, AnyItem
from pyexlatex.logic.extract.docitems import is_latex_item


def get_attr_from_items_or_collection(content: ListOrDictOrItem, attr: str, unique: bool = False,
                                      collected_attr_values: Optional[list] = None) -> StrListOrNone:
    if unique:
        extend_func = _extend_with_items_not_in_list
    else:
        extend_func = _extend

    if collected_attr_values is None:
        collected_attr_values = []
        
    if isinstance(content, (list, tuple)):
        for item in content:
            get_attr_from_items_or_collection(item, attr, unique=unique, collected_attr_values=collected_attr_values)
    elif isinstance(content, dict):
        for name, item in content.items():
            get_attr_from_items_or_collection(item, attr, unique=unique, collected_attr_values=collected_attr_values)
    elif is_latex_item(content):
        if _is_item_and_has_attr(content, attr):
            extend_func(collected_attr_values, _get_from_item_or_item_data(content, attr))

    if not collected_attr_values:
        return None

    return collected_attr_values


def _is_item_and_has_attr(item: AnyItem, attr: str) -> bool:
    return is_latex_item(item) and _has_attr_or_data_attr_and_is_not_none(item, attr)


def _get_from_item_or_item_data(item: AnyItem, attr: str):
    if hasattr(item, attr):
        return getattr(item, attr)

    if hasattr(item, 'data'):
        return getattr(item.data, attr)

    raise ValueError(f'Could not get {attr} from {item} or .data of that object')
    

def _extend_with_items_not_in_list(orig_list: list, extend_with: list) -> None:
    for item in extend_with:
        if item not in orig_list:
            orig_list.append(item)


def _extend(orig_list: list, extend_with: list) -> None:
    orig_list.extend(extend_with)


def _has_attr_and_is_not_none(item: AnyItem, attr: str) -> bool:
    return hasattr(item, attr) and getattr(item, attr) is not None


def _has_attr_or_data_attr_and_is_not_none(item: AnyItem, attr: str) -> bool:
    return _has_attr_and_is_not_none(item, attr) or (
        _has_attr_and_is_not_none(item, 'data') and _has_attr_and_is_not_none(item.data, attr)
    )