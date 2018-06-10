import pandas as pd
from typing import Union

from dero.latex.table.models.data.valuestable import ValuesTable
from dero.latex.table.models.table.section import TableSection
from dero.latex.table.models.spacing.columntable import ColumnPadTable, CellSpacer
from dero.latex.table.models.labels.table import LabelTable, LabelCollection
from dero.latex.table.models.labels.label import Label
from dero.latex.models.mixins import ReprMixin


class DataTable(TableSection, ReprMixin):
    repr_cols = ['values_table', 'column_labels', 'row_labels']

    def __init__(self, values_table: ValuesTable, column_labels: LabelTable=None, row_labels: LabelTable=None,
                 top_left_corner_label: Union[Label, str] = None):
        self.values_table = values_table
        self.column_labels = column_labels
        self.row_labels = row_labels

        if isinstance(top_left_corner_label, str):
            top_left_corner_label = Label(top_left_corner_label)

        if top_left_corner_label is None:
            if row_labels is None:
                top_left_corner_label = CellSpacer()
            else:
                top_left_corner_label = CellSpacer(row_labels.num_columns)
        self.top_left_corner_label = top_left_corner_label

        self.should_add_top_left = (column_labels is not None) and (row_labels is not None)

    def __add__(self, other):
        if isinstance(other, DataTable):
            if self.row_labels.matches(other.row_labels) or other.row_labels is None:
                # if right table has same or None row labels, eliminate right row labels. Just add values
                values_table = self.values_table + other.values_table
                column_labels = _add_if_not_none(self.column_labels, other.column_labels)
            else:
                # if right table has unique row labels, absorb them into middle of values table
                values_table = self.values_table + ValuesTable(other.row_labels.rows) + other.values_table
                column_labels = _add_if_not_none(
                    self.column_labels,
                    other.top_left_corner_label,
                    other.column_labels
                )

            row_labels = self.row_labels
        elif isinstance(other, ColumnPadTable):
            values_table = self.values_table + other
            column_labels = self.column_labels + other
            row_labels = self.row_labels
        elif isinstance(other, TableSection):
            values_table = self.values_table + other
            column_labels = self.column_labels
            row_labels = self.row_labels
        else:
            raise ValueError(f'must add DataTable or TableSection to type {type(self)}. Got type {type(other)}')

        return DataTable(
            values_table=values_table,
            column_labels=column_labels,
            row_labels=row_labels,
            top_left_corner_label=self.top_left_corner_label
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
    def row_labels(self):
        return self._row_labels

    @row_labels.setter
    def row_labels(self, labels: LabelTable):
        self._row_labels = labels
        self._recreate_rows_if_created()

    @property
    def values_table(self):
        return self._values_table

    @values_table.setter
    def values_table(self, table: ValuesTable):
        self._values_table = table
        self._recreate_rows_if_created()

    def _create_rows(self):

        rows = []

        if self.column_labels is not None:
            for i, row in enumerate(self.column_labels.rows):
                if self.should_add_top_left:
                    # first row should start with top left corner label
                    if i == 0:
                        out_row = self.top_left_corner_label + row
                    # other label rows, blank top left label
                    else:
                        out_row = CellSpacer() + row
                # without top left, no need for additional processing, add to output
                else:
                    out_row = row
                rows.append(out_row)

        # need to add row labels inline with values table
        if self.row_labels is not None:
            assert len(self.row_labels.rows) == len(self.values_table.rows)
            for label_row, value_row in zip(self.row_labels.rows, self.values_table.rows):
                rows.append(label_row + value_row)
        # no row labels, add values rows as they are
        else:
            rows += self.values_table.rows

        return rows

    @classmethod
    def from_df(cls, df: pd.DataFrame, include_columns=True, include_index=False,
                extra_header: str=None,
                *args, **kwargs):
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
            *args,
            **kwargs,
        )

        if extra_header is not None:
            # create multicolumn label
            label = Label(extra_header, span=values_table.num_columns)
            header = LabelCollection([label])
            if include_columns:
                # add to existing
                dt.column_labels.label_collections.insert(0, header)
            else:
                # create column labels as extra header
                dt.column_labels = LabelTable([header])

        return dt


def _add_if_not_none(*items):
    not_none_items = [item for item in items if item is not None]
    return sum(not_none_items[1:], not_none_items[0])