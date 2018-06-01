import pandas as pd
from pandas.indexes.base import Index as PandasIndex

from dero.latex.table.models.table.section import TableSection
from dero.latex.table.models.labels.collection import LabelCollection
from dero.latex.table.models.labels.row import LabelRow
from dero.latex.models.mixins import ReprMixin


class LabelTable(TableSection, ReprMixin):
    repr_cols = ['label_collections']

    def __init__(self, label_collections: [LabelCollection]):
        self.label_collections = label_collections
        super().__init__()

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
        len_rows = max([len(collection) for collection in self.label_collections])

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

    def from_df_index(self, df_columns: PandasIndex):
        column_list = [col for col in df_columns]

        return LabelTable.from_list_of_lists([column_list])


