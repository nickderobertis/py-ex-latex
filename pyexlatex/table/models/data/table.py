from typing import Union, List, Optional

import pandas as pd

from pyexlatex.table.models.interfaces import LabelClassOrStrs
from pyexlatex.logic.tools import _add_if_not_none
from mixins.repr import ReprMixin
from pyexlatex.table.models.data.valuestable import ValuesTable
from pyexlatex.table.models.labels.label import Label
from pyexlatex.table.models.labels.table import LabelTable, LabelCollection
from pyexlatex.table.models.spacing.columntable import ColumnPadTable, CellSpacer
from pyexlatex.table.models.table.section import TableSection
from pyexlatex.table.logic.panels.topleft import _set_top_left_corner_labels


class DataTable(TableSection, ReprMixin):
    """
    Represents a subsection in a panel, but tracks row and column labels, which may be consolidated when
    assembled into Panels then a Table

    Use DataTable.from_df to create a DataTable from a pandas DataFrame.
    """
    repr_cols = ['values_table', 'column_labels', 'row_labels']

    def __init__(self, values_table: ValuesTable, column_labels: LabelTable=None, row_labels: LabelTable=None,
                 top_left_corner_labels: LabelClassOrStrs = None, break_size_adjustment: Optional[str] = None):
        self.values_table = values_table
        self.column_labels = column_labels
        self.row_labels = row_labels
        self.top_left_corner_labels = _set_top_left_corner_labels(top_left_corner_labels)
        self.break_size_adjustment = break_size_adjustment

        self.should_add_top_left = (self.has_column_labels) and (self.has_row_labels)

    def __add__(self, other):
        if isinstance(other, DataTable):
            row_labels_match = _determine_match(self.row_labels, other.row_labels)
            if row_labels_match or other.row_labels is None:
                # if right table has same or None row labels, eliminate right row labels. Just add values
                values_table = _add_if_not_none(self.values_table, other.values_table)
                column_labels = _add_if_not_none(self.column_labels, other.column_labels)
            else:
                # if right table has unique row labels, absorb them into middle of values table
                values_table = _add_if_not_none(
                    self.values_table,
                    ValuesTable(other.row_labels.rows),
                    other.values_table
                )
                column_labels = _add_if_not_none(
                    self.column_labels,
                    other.top_left_corner_labels,
                    other.column_labels
                )

            row_labels = self.row_labels
        elif isinstance(other, ColumnPadTable):
            values_table = self.values_table + other if self.values_table is not None else None
            column_labels = self.column_labels + other if self.column_labels is not None else None
            row_labels = self.row_labels
        elif isinstance(other, TableSection):
            values_table = _add_if_not_none(self.values_table, other)
            column_labels = self.column_labels
            row_labels = self.row_labels
        else:
            raise ValueError(f'must add DataTable or TableSection to type {type(self)}. Got type {type(other)}')

        return DataTable(
            values_table=values_table,
            column_labels=column_labels,
            row_labels=row_labels,
            top_left_corner_labels=self.top_left_corner_labels
        )

    @property
    def rows(self):
        try:
            return self._rows
        except AttributeError:
            self._rows = self._create_rows()

        return self._rows

    # Following properties/setters exist to recreate rows if user overrides values table or labels

    @property
    def column_labels(self):
        return self._column_labels

    @column_labels.setter
    def column_labels(self, labels: LabelTable):
        self._column_labels = labels
        self._recreate_rows_if_created()

    @property
    def has_column_labels(self) -> bool:
        return (self.column_labels is not None and not self.column_labels.is_empty)

    @property
    def row_labels(self):
        return self._row_labels

    @row_labels.setter
    def row_labels(self, labels: LabelTable):
        self._row_labels = labels
        self._recreate_rows_if_created()

    @property
    def has_row_labels(self) -> bool:
        return (self.row_labels is not None and not self.row_labels.is_empty)

    @property
    def values_table(self):
        return self._values_table

    @values_table.setter
    def values_table(self, table: ValuesTable):
        self._values_table = table
        self._recreate_rows_if_created()

    def _create_rows(self):

        rows = []
        if self.has_column_labels:
            if self.should_add_top_left:
                column_labels = self.top_left_corner_labels + self.column_labels
            else:
                column_labels = self.column_labels
            rows += column_labels.rows

        # need to add row labels inline with values table
        if self.has_row_labels:
            assert len(self.row_labels.rows) == len(self.values_table.rows)
            for label_row, value_row in zip(self.row_labels.rows, self.values_table.rows):
                rows.append(label_row + value_row)
        # no row labels, add values rows as they are
        else:
            rows += self.values_table.rows

        return rows

    @classmethod
    def from_df(cls, df: pd.DataFrame, include_columns=True, include_index=False,
                extra_header: str=None, extra_header_underline=True,
                top_left_corner_labels: LabelClassOrStrs = None,
                **kwargs):
        """
        Use for the most fine-grained control in creating tables. Construct DataTables from
        pandas DataFrames, modify labels as needed, assemble them into Panels, then create a latex Table with
        Table.from_panel_list.

        :param df:
        :param include_columns:
        :param include_index:
        :param extra_header: extra headers to place over the existing column labels (or over values if
                             there are no column labels). Useful when placing multiple DataTables horizontally
                             in a Panel. If a str is passed, str will become a multicolumn header for the entire
                             DataTable. If a list of as many strs as there are columns is passed, these
                             will be placed above any existing column labels. LabelTable and LabelCollection objects
                             may also be passed for more control. When those objects are passed, the extra_header_underline
                             argument is ignored.
        :param extra_header_underline: whether to add an underline under the extra header, if the extre header
                                       was passed
        :param top_left_corner_labels: additional labels to place in the top left corner. pass a single string
                                       or a list of strings for convenience. a list of strings will be create labels
                                       which span the gap horizontally and go downwards, one label per row. pass
                                       LabelCollection or LabelTable for more control.
        :param kwargs: DataTable kwargs
        :return:
        """
        values_table = ValuesTable.from_df(df)

        if include_columns:
            column_label_table = LabelTable.from_df_index(df.columns)
        else:
            column_label_table = None

        if include_index:
            row_label_table = LabelTable.from_df_index(df.index).T
        else:
            row_label_table = None

        dt = cls(
            values_table,
            column_labels=column_label_table,
            row_labels=row_label_table,
            top_left_corner_labels=top_left_corner_labels,
            **kwargs,
        )

        if extra_header is not None:

            header = _create_header_label_collection_list(extra_header, values_table, extra_header_underline)

            if include_columns:
                # add to existing
                header.reverse() # need to insert end first, so they end up in original order
                [dt.column_labels.label_collections.insert(0, label_collection) for label_collection in header]
            else:
                # create column labels as extra header
                dt.column_labels = LabelTable(header)

            if include_index:  # need to add to top left
                num_spacers = len(header)

                # top left has one by default. if there were already columns, that top left is used up by the columns
                # and we need to add more. if there are not columns, then this one existing top left can be used
                # for the new header
                if not include_columns:
                    num_spacers -= 1

                for i in range(num_spacers):
                    dt.top_left_corner_labels.label_collections.insert(0, LabelCollection.from_str_list([' ']))

            # add spacer to top left corner labels to match new row of headers
            if (not include_columns) and include_index:
                # header becomes new columns, have to add top left as if there were columns
                dt.should_add_top_left = True


        return dt

def _determine_match(labels1: LabelTable, labels2: LabelTable):
    # handle equality for None
    if labels1 is None:
        if labels2 is None:
            return True
        else:
            return False
    elif labels2 is None:
        # labels 1 must not be None here
        return False

    # here, both are not None
    return labels1.matches(labels2)

def _create_header_label_collection_list(extra_header: LabelClassOrStrs, values_table: ValuesTable,
                                         underline: bool) -> List[LabelCollection]:

    if isinstance(extra_header, LabelTable):
        return extra_header.label_collections

    if isinstance(extra_header, LabelCollection):
        return [extra_header]

    if isinstance(extra_header, list):
        if len(extra_header) != values_table.num_columns:
            raise ValueError(f'passed extra header has {len(extra_header)} columns, while table has '
                             f'{values_table.num_columns} columns')

        underline_str_arg: Optional[str]
        if underline:
            underline_str_arg = f'0-{len(extra_header) - 1}'
        else:
            underline_str_arg = None
        return [LabelCollection.from_str_list(extra_header, underline=underline_str_arg)]

    # Got a string or latex item

    # create multicolumn label
    label = Label(extra_header, span=values_table.num_columns)

    # set underline
    underline_int_arg: Optional[int]
    if underline:
        underline_int_arg = 0  # place an underline under the singular label
    else:
        underline_int_arg = None  # no underline
    return [LabelCollection([label], underline=underline_int_arg)]