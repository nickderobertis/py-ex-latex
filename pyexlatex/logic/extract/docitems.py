from typing import List

from pyexlatex.logic.extract.by_type import extract_objs_of_type_from_ambiguous_collection
from pyexlatex.logic.extract.by_attr import extract_objs_with_attr_from_ambiguous_collection
from pyexlatex.models.documentitem import DocumentItem


def extract_document_items_from_ambiguous_collection(collection) -> List[DocumentItem]:
    return extract_objs_with_attr_from_ambiguous_collection(collection, 'is_DocumentItem', True)


def extract_document_items_from_ambiguous_collection_by_type(collection) -> List[DocumentItem]:
    return extract_objs_of_type_from_ambiguous_collection(collection, DocumentItem)


def is_latex_item(item) -> bool:
    return hasattr(item, 'is_LatexItem') and getattr(item, 'is_LatexItem')