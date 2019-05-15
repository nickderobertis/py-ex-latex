from typing import List
from dero.latex.typing import ListOrDictOrItem, BytesListOrNone, BytesList, AnyItem
from dero.latex.logic.extract.docitems import is_latex_item


def get_binaries_from_items(content: ListOrDictOrItem) -> BytesListOrNone:
    binaries = []
    if isinstance(content, (list, tuple)):
        for item in content:
            if is_latex_item(item):
                binaries += _get_binaries(item)
    elif isinstance(content, dict):
        for name, item in content.items():
            if is_latex_item(item):
                binaries += _get_binaries(item)
    elif is_latex_item(content):
        if is_latex_item(content):
            binaries += _get_binaries(content)

    if not binaries:
        return None

    return binaries

def _get_binaries(item: AnyItem) -> BytesList:
    binary = getattr(item, 'binary', None)
    if binary is not None:
        return [binary]

    binaries = getattr(item, 'binaries', None)
    if binaries is not None:
        return binaries

    return []
