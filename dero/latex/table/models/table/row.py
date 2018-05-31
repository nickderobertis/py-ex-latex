from typing import Union

from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.data.dataitem import DataItem
from dero.latex.table.models.labels.collection import LabelCollection
from dero.latex.table.models.mixins import RowAddMixin
from dero.latex.texparser.clean import _remove_backslashes


class Row(ReprMixin, RowAddMixin):
    repr_cols = ['values']

    def __init__(self, values: Union([DataItem], LabelCollection)):
        self.values = values

    def __len__(self):
        return len(self.values)

    def __str__(self):
        return sum(self.values)

    def pad(self, length: int, direction='right'):
        """
        Expand row out to the right or left with blanks, until it is length passed
        :param length:
        :return:
        """
        num_values_to_add = length - len(self)
        direction = direction.lower().strip()

        if direction == 'right':
            self.values += [' '] * num_values_to_add
        elif direction == 'left':
            self.values = [' '] * num_values_to_add + self.values
        else:
            raise ValueError(f'must pass left or right for direction. got {direction}')

    @classmethod
    def from_latex_row_str(cls, latex_row_str):
        latex_row_str = _remove_backslashes(latex_row_str)
        str_values = latex_row_str.split(' & ')
        values = [DataItem(value) for value in str_values]
        return cls(values)