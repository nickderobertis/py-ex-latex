from typing import Dict, List
from pyexlatex.texgen import bibtex_str
from pyexlatex.models.documentitem import DocumentItem
from mixins.repr import ReprMixin
from mixins.attrequals import EqOnAttrsMixin

class BibTexEntryBase(DocumentItem, EqOnAttrsMixin, ReprMixin):
    is_BibTexEntry = True
    item_type = 'notimplemented'
    repr_cols = ['item_accessor', 'fields']
    equal_attrs = ['item_accessor', 'fields']
    required_attrs: List[str] = []
    optional_attrs: List[str] = []

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

    @property
    def fields(self) -> Dict[str, str]:
        fields_dict = {arg: getattr(self, arg) for arg in self.required_attrs}

        for attr in self.optional_attrs:
            self_attr = getattr(self, attr)
            if self_attr:
                fields_dict.update({attr: self_attr})

        return fields_dict