from typing import Dict
from dero.latex.texgen import bibtex_str
from dero.latex.models.documentitem import DocumentItem
from dero.mixins.repr import ReprMixin

class BibTexEntryBase(DocumentItem, ReprMixin):
    is_BibTexEntry = True
    item_type = 'notimplemented'
    fields = {}
    repr_cols = ['item_accessor', 'fields']

    def __init__(self, item_accessor: str):
        self.item_accessor = item_accessor

        super().__init__()

    def __str__(self):
        str_ = bibtex_str(
            self.item_type,
            self.item_accessor,
            self.fields
        )

        return str_