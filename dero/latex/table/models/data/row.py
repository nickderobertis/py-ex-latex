from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.data.dataitem import DataItem
from dero.latex.table.models.mixins import AmpersandAddMixin
from dero.latex.texparser.clean import _remove_backslashes


class DataRow(ReprMixin, AmpersandAddMixin):
    repr_cols = ['values']

    def __init__(self, values: [DataItem]):
        self.values = values

    def __len__(self):
        return len(self.values)

    def __str__(self):
        return sum(self.values)

    @classmethod
    def from_latex_row_str(cls, latex_row_str):
        latex_row_str = _remove_backslashes(latex_row_str)
        str_values = latex_row_str.split(' & ')
        values = [DataItem(value) for value in str_values]
        return cls(values)