from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.mixins.addvalues.row import RowAddMixin


class Label(ReprMixin, RowAddMixin):
    repr_cols = ['value']

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value