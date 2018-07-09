from typing import List

from dero.latex.logic.extract.extract import extract_objs_of_type_from_ambiguous_collection
from dero.latex.models.documentitem import DocumentItem

def extract_document_items_from_ambiguous_collection(collection) -> List[DocumentItem]:
    return extract_objs_of_type_from_ambiguous_collection(collection, DocumentItem)