from typing import Union, Iterable

from dero.latex.table.models.data.dataitem import DataItem
from dero.latex.table.models.labels.collection import LabelCollection
from dero.latex.table.models.labels.label import Label
from dero.latex.table.models.spacing.cell import CellSpacer
from dero.latex.table.models.table.rowbase import RowBase
from dero.latex.texparser.clean import _remove_backslashes


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
        latex_row_str = _remove_backslashes(latex_row_str)
        str_values = latex_row_str.split(' & ')
        values = [DataItem(value) for value in str_values]
        return cls(values)