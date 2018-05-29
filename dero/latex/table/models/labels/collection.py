from dero.latex.table.models.labels.label import Label
from dero.latex.models.mixins import ReprMixin


class LabelCollection(ReprMixin):
    repr_cols = ['labels']

    def __init__(self, labels: [Label]):
        self.labels = labels

    def __str__(self):
        return sum(self.labels)

    def __len__(self):
        return len(self.labels)

    @classmethod
    def from_str_list(cls, str_list):
        labels = [Label(value) for value in str_list]
        return cls(labels)