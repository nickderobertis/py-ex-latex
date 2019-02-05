from typing import List

from dero.latex.logic.extract.by_type import extract_objs_of_type_from_ambiguous_collection
from dero.latex.logic.extract.by_attr import extract_objs_with_attr_from_ambiguous_collection
from dero.latex.models.documentitem import DocumentItem


def extract_document_items_from_ambiguous_collection(collection) -> List[DocumentItem]:
    return extract_objs_with_attr_from_ambiguous_collection(collection, 'is_DocumentItem', True)


def extract_document_items_from_ambiguous_collection_by_type(collection) -> List[DocumentItem]:
    return extract_objs_of_type_from_ambiguous_collection(collection, DocumentItem)