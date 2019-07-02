from dero.latex.typing import ListOrDictOrItem, StrListOrNone, AnyItem
from dero.latex.logic.extract.docitems import is_latex_item


def get_begin_document_items_from_items(content: ListOrDictOrItem, unique: bool = False) -> StrListOrNone:
    if unique:
        extend_func = _extend_with_items_not_in_list
    else:
        extend_func = _extend
    begin_document_items = []
    if isinstance(content, (list, tuple)):
        for item in content:
            if _has_begin_document_items(item):
                extend_func(begin_document_items, item.begin_document_items)
    elif isinstance(content, dict):
        for name, item in content.items():
            if _has_begin_document_items(item):
                extend_func(begin_document_items, item.begin_document_items)
    elif is_latex_item(content):
        if _has_begin_document_items(content):
            extend_func(begin_document_items, content.begin_document_items)

    if begin_document_items == []:
        return None

    return begin_document_items

def _has_begin_document_items(item: AnyItem) -> bool:
    return is_latex_item(item) and hasattr(item, 'begin_document_items') and item.begin_document_items is not None


def _extend_with_items_not_in_list(orig_list: list, extend_with: list) -> list:
    for item in extend_with:
        if item not in orig_list:
            orig_list.append(item)

def _extend(orig_list: list, extend_with: list) -> list:
    orig_list.extend(extend_with)