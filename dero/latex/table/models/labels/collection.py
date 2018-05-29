from dero.latex.table.models.labels.label import Label
from dero.latex.models.mixins import ReprMixin


class LabelCollection(ReprMixin):
    repr_cols = ['labels']

    def __init__(self, labels: [Label]):
        self.labels = labels