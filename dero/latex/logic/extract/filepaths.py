from dero.latex.typing import ListOrDictOrItem, StrListOrNone, AnyItem
from dero.latex.logic.extract.docitems import is_latex_item


def get_filepaths_from_items(content: ListOrDictOrItem) -> StrListOrNone:
    filepaths = []
    if isinstance(content, (list, tuple)):
        for item in content:
            if _has_filepaths(item):
                filepaths += item.filepaths
    elif isinstance(content, dict):
        for name, item in content.items():
            if _has_filepaths(item):
                filepaths += item.filepaths
    elif is_latex_item(content):
        if _has_filepaths(content):
            filepaths += content.filepaths

    if filepaths == []:
        return None

    return filepaths

def _has_filepaths(item: AnyItem) -> bool:
    return is_latex_item(item) and hasattr(item, 'filepaths') and item.filepaths is not None