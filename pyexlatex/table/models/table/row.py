from typing import Union, Iterable

from pyexlatex.table.models.data.dataitem import DataItem
from pyexlatex.table.models.labels.collection import LabelCollection
from pyexlatex.table.models.labels.label import Label
from pyexlatex.table.models.spacing.cell import CellSpacer
from pyexlatex.table.models.table.rowbase import RowBase
from pyexlatex.texparser.clean import _remove_backslashes


class Row(RowBase):
    repr_cols = ['values']

    def __init__(self, values: Union[Iterable[DataItem], LabelCollection, Label]):

        # Don't allow nested rows. If the only values passed to a Row are a Row, then use the values of that
        # row rather than the row itself as values
        if isinstance(values, Row):
            self.values = values.values
        else:
            self.values = values

    def __str__(self):
        str_list = []
        for value in self.values:
            # Handle other forms of blanks
            if isinstance(value, Iterable) and len(value) == 1 and str(value[0]).strip() == '':
                str_list.append(' ')
            # The usual case, just join string representation of items
            else:
                str_list.append(str(value))

        return ' & '.join(str_list)

    @classmethod
    def from_latex_row_str(cls, latex_row_str):
        # Split before removing backslashes so that \& doesn't get counted as &
        str_values = latex_row_str.split(' & ')
        str_values = [_remove_backslashes(val) for val in str_values]
        values = [DataItem(value) for value in str_values]
        return cls(values)