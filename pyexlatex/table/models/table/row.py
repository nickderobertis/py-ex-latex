from typing import Union, Iterable, Sequence

from pyexlatex.table.models.data.dataitem import DataItem
from pyexlatex.table.models.labels.collection import LabelCollection
from pyexlatex.table.models.labels.label import Label
from pyexlatex.table.models.spacing.cell import CellSpacer
from pyexlatex.table.models.table.rowbase import RowBase
from pyexlatex.texparser.clean import _remove_backslashes


class Row(RowBase):
    repr_cols = ['values']

    def __init__(self, values: Union[Sequence[DataItem], LabelCollection, Label]):

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

    @property
    def cell_width(self):
        return _get_cell_width(self)


def _get_cell_width(item: Union[Row, DataItem, Sequence[DataItem], LabelCollection, Label]):
    width = 0
    if isinstance(item, Row):
        for value in item.values:
            width += _get_cell_width(value)
    elif isinstance(item, DataItem):
        width += 1
    elif isinstance(item, Sequence):
        for it in item:
            width += _get_cell_width(it)
    elif isinstance(item, LabelCollection):
        for label in item.values:
            width += _get_cell_width(label)
    elif isinstance(item, Label):
        width += item.span
    else:
        raise ValueError(f'cannot determine cell width of {item} of type {type(item)}')

    return width