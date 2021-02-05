from typing import Optional, List, Union
from pandas.core.indexes.base import Index as PandasIndex
from itertools import zip_longest
import warnings

from pyexlatex.logic.tools import _max_len_or_zero
from mixins.repr import ReprMixin
from pyexlatex.table.models.labels.collection import LabelCollection
from pyexlatex.table.models.labels.row import LabelRow
from pyexlatex.table.models.table.section import TableSection
from pyexlatex.table.models.texgen.lines import TableLineSegment, TableLineOfSegments


class LabelTable(TableSection, ReprMixin):
    """
    A set of label rows to apply to a DataTable.

    Example:

    >>>import pyexlatex.table as lt
    >>>data_table = lt.DataTable.from_df(some_df)
    >>>col_label_table = lt.LabelTable.from_list_of_lists([['One header'],['More','Headers']])
    >>>row_label_table = lt.LabelTable.from_list_of_lists([['Some','Row','Labels']]).T
    >>>data_table.column_labels = col_label_table
    """
    repr_cols = ['label_collections']

    def __init__(self, label_collections: List[LabelCollection], break_size_adjustment: Optional[str] = None):
        self.label_collections = label_collections
        self.break_size_adjustment = break_size_adjustment

    def __add__(self, other):
        # Import here to avoid circular imports
        from pyexlatex.table.models.data.table import DataTable
        from pyexlatex.table.models.spacing.columntable import ColumnPadTable

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
        if isinstance(other, ColumnPadTable):
            self.pad(self.num_columns + other.width)
            return self
        else:
            return super().__add__(other)

    def __iter__(self):
        for collection in self.label_collections:
            yield collection

    def __getitem__(self, item):
        return self.label_collections[item]

    def __contains__(self, item):
        return item in self.label_collections

    @property
    def length(self):
        return len(self.label_collections)

    @property
    def rows(self):
        try:
            return self._rows
        except AttributeError:
            self._rows = self._create_rows()

        return self._rows

    def _create_rows(self):
        len_rows = _max_len_or_zero(self.label_collections)

        rows = []
        label_collection: LabelCollection
        for label_collection in self.label_collections:
            rows.append(
                LabelRow(label_collection)
            )
            if label_collection.underlines is not None:
                rows.append(
                    TableLineOfSegments.from_list_of_ints(label_collection.underlines, num_columns=len(label_collection))
                )

        return rows

    # Following property/setter exist to recreate rows if user overrides labels

    @property
    def label_collections(self):
        return self._label_collections

    @label_collections.setter
    def label_collections(self, label_collections: List[LabelCollection]):
        self._label_collections = label_collections
        self._recreate_rows_if_created()

    @classmethod
    def from_list_of_lists(cls, list_of_lists: List[List[str]]):
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
        """
        Note: use to compare strings inside LabelTables. Use regular equality comparison to compare objects
        :param other:
        :return:
        """
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

    def contains(self, item):
        """
        Note: use to compare strings inside LabelCollections. Use label_collection in LabelTable to compare objects
        :param item:
        :return:
        """

        if not isinstance(item, (str, list, LabelCollection)):
            warnings.warn(f'LabelTable.contains() called on type {type(item)}. Will always return False')
            return False

        item: LabelCollection = LabelCollection.parse_unknown_type(item)

        label_collection: LabelCollection
        for label_collection in self:
            if label_collection.matches(item):
                return True # as soon as one match, return true

        # went through all label collections without a match. no match
        return False

    def begins_with(self, item: Union[str, list, LabelCollection]):
        if not isinstance(item, (str, list, LabelCollection)):
            warnings.warn(f'LabelTable.begins_with() called on type {type(item)}. Will always return False')
            return False

        label: LabelCollection = LabelCollection.parse_unknown_type(item)
        begin_label_collection = LabelCollection([self.label_collections[0][0]])
        return begin_label_collection.matches(label)

    def pad(self, length: int, direction='right'):
        """
        Expand table out to the right or left with blanks, until it is length passed (apply to every row)
        :param length:
        :param direction:
        :return:
        """
        [collection.pad(length=length, direction=direction) for collection in self.label_collections]

    def append(self, item):
        item: LabelCollection = LabelCollection.parse_unknown_type(item)

        # add rather than append directly to activate setter
        self.label_collections = self.label_collections + [item]

    def insert(self, item, index):
        item: LabelCollection = LabelCollection.parse_unknown_type(item)

        # add rather than append directly to activate setter
        self.label_collections.insert(item, index)