from pandas.core.indexes.base import Index as PandasIndex

from dero.latex.logic.tools import _max_len_or_zero
from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.labels.collection import LabelCollection
from dero.latex.table.models.labels.row import LabelRow
from dero.latex.table.models.table.section import TableSection


class LabelTable(TableSection, ReprMixin):
    repr_cols = ['label_collections']

    def __init__(self, label_collections: [LabelCollection]):
        self.label_collections = label_collections

    def __iter__(self):
        for collection in self.label_collections:
            yield collection

    def __getitem__(self, item):
        return self.label_collections[item]

    @property
    def rows(self):
        try:
            return self._rows
        except AttributeError:
            self._rows = self._create_label_rows()

        return self._rows

    def _create_label_rows(self):
        len_rows = _max_len_or_zero(self.label_collections)

        rows = []
        for label_collection in self.label_collections:
            rows.append(
                LabelRow(label_collection, length=len_rows)
            )

        return rows

    @classmethod
    def from_list_of_lists(cls, list_of_lists: [[str]]):
        label_collections = []
        for label_list in list_of_lists:
            label_collections.append(
                LabelCollection.from_str_list(label_list)
            )

        return cls(label_collections)

    @classmethod
    def from_df_index(cls, df_columns: PandasIndex):
        column_list = [col for col in df_columns]

        return cls.from_list_of_lists([column_list])

    @property
    def is_empty(self):
        return len(self.label_collections) == 0

    def remove(self, item):
        self.label_collections.remove(item)


