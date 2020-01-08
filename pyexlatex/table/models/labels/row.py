from typing import Union

from pyexlatex.table.models.table.row import Row
from pyexlatex.table.models.labels.collection import LabelCollection, Label


class LabelRow(Row):
    repr_cols = ['values', 'length']

    def __init__(self, values: Union[LabelCollection, Label]):
        super().__init__(values)

    @property
    def length(self):
        return len(self)

    def _add_class(self, other):
        if isinstance(other, (LabelCollection, Label)):
            return LabelRow
        else:
            return super()._add_class(other)
