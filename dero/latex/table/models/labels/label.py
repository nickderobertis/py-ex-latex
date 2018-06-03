from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.mixins.addvalues.row import RowAddMixin


class Label(ReprMixin, RowAddMixin):
    repr_cols = ['value']

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if hasattr(other, 'value'):
            return self.value == other.value
        else:
            return self.value == other

    def __str__(self):
        return str(self.value)