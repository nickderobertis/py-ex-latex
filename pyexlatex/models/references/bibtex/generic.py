from typing import Dict
from pyexlatex.models.references.bibtex.base import BibTexEntryBase

class BibTexEntry(BibTexEntryBase):

    def __init__(self, fields_dict: Dict[str, str]):
        self.optional_attrs = []
        self.fields = fields_dict
        super().__init__(self.item_accessor)

    @BibTexEntryBase.fields.setter  # type: ignore
    def fields(self, fields_dict: Dict[str, str]):
        rename_items = {
            'ENTRYTYPE': 'item_type',
            'ID': 'item_accessor'
        }
        skip_fields_items = ['item_type', 'item_accessor']
        for attr, value in fields_dict.items():
            if attr in rename_items:
                self_attr = rename_items[attr]
            else:
                self_attr = attr
            setattr(self, self_attr, value)
            # TODO [#16]: improve BibTexEntry fields property
            #
            # Come up with cleaner way to get added to fields output property
            if self_attr not in skip_fields_items:
                self.optional_attrs.append(self_attr)
