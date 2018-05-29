from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.mixins import AmpersandAddMixin


class Label(ReprMixin, AmpersandAddMixin):
    repr_cols = ['value']

    def __init__(self, value):
        self.value = value