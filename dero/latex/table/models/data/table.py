import pandas as pd

from dero.latex.table.models.data.valuestable import ValuesTable
from dero.latex.table.models.table.section import TableSection
from dero.latex.table.models.data.row import DataRow
from dero.latex.table.models.labels.row import LabelRow
from dero.latex.table.models.labels.table import LabelTable
from dero.latex.table.models.labels.label import Label
from dero.latex.models.mixins import ReprMixin


class DataTable(TableSection, ReprMixin):
    repr_cols = ['values_table', 'column_labels', 'row_labels']

    def __init__(self, values_table: ValuesTable, column_labels: LabelTable=None, row_labels: LabelTable=None,
                 top_left_corner_label: Label = None):
        self.values_table = values_table
        self.column_labels = column_labels
        self.row_labels = row_labels
        self.top_left_corner_label = top_left_corner_label \
            if top_left_corner_label is not None else Label(' ')
        self.should_add_top_left = (column_labels is not None) and (row_labels is not None)
        super().__init__()

    @property
    def rows(self):
        try:
            return self._rows
        except AttributeError:
            self._rows = self._create_rows()

        return self._rows

    def _create_rows(self):

        rows = []

        if self.column_labels is not None:
            for i, row in self.column_labels.rows:
                if self.should_add_top_left:
                    # first row should start with top left corner label
                    if i == 0:
                        out_row = self.top_left_corner_label + row
                    # other label rows, blank top left label
                    else:
                        out_row = Label(' ') + row
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
    def from_df(cls, df: pd.DataFrame, include_columns=True, include_index=False, *args, **kwargs):
        values_table = ValuesTable.from_df(df)

        if include_columns:
            column_label_table = LabelTable.from_df_index(df.columns)
        else:
            column_label_table = None

        if include_index:
            row_label_table = LabelTable.from_df_index(df.index)
        else:
            row_label_table = None

        return cls(
            values_table,
            column_labels=column_label_table,
            row_labels=row_label_table,
            *args,
            **kwargs,
        )

