from pandas.core.indexes.base import Index as PandasIndex
from itertools import zip_longest
import warnings

from dero.latex.logic.tools import _max_len_or_zero
from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.labels.collection import LabelCollection
from dero.latex.table.models.labels.row import LabelRow
from dero.latex.table.models.table.section import TableSection


class LabelTable(TableSection, ReprMixin):
    repr_cols = ['label_collections']

    def __init__(self, label_collections: [LabelCollection]):
        self.label_collections = label_collections

    def __add__(self, other):
        # Import here to avoid circular imports
        from dero.latex.table.models.data.table import DataTable

        # Return a DataTable if just adding labels to an existing DataTable
        if isinstance(other, DataTable) and not other.row_labels:
            values_table = other.values_table
            column_labels = other.column_labels
            row_labels = self

            return DataTable(
                values_table=values_table,
                column_labels=column_labels,
                row_labels=row_labels
            )
        else:
            return super().__add__(other)

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

    # Following property/setter exist to recreate rows if user overrides labels

    @property
    def label_collections(self):
        return self._label_collections

    @label_collections.setter
    def label_collections(self, label_collections: [LabelCollection]):
        self._label_collections = label_collections
        self._recreate_rows_if_created()

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

    @property
    def T(self):
        return LabelTable(list(map(LabelCollection, zip_longest(*self.label_collections))))

    def matches(self, other):
        if not isinstance(other, LabelTable):
            warnings.warn(f'LabelTable.matches() called on type {type(other)}. Will always return False')
            return False

        max_rows = max(len(self.label_collections), len(other.label_collections))

        # Go through all label collections, calling LabelCollection.matches, and returning False if any don't match
        for n_row in range(max_rows):
            if not self.label_collections[n_row].matches(other.label_collections[n_row]):
                return False

        # made it through loop, so all were matching
        return True


