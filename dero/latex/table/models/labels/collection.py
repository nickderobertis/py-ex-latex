from dero.latex.table.models.labels.label import Label
from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.mixins.addvalues.row import RowAddMixin


class LabelCollection(RowAddMixin, ReprMixin):
    repr_cols = ['values']

    def __init__(self, values: [Label]):
        self.values = values

    def __iter__(self):
        for label in self.values:
            yield label

    def __getitem__(self, item):
        return self.values[item]

    def __str__(self):
        return sum(self.values)

    def __len__(self):
        return len(self.values)

    def matches(self, other):
        """
        Compare on the basis of having same values, rather than same instance
        Use regular equality to test if same instance
        :param other:
        :return:
        """
        matches = [value == other[i] for i, value in enumerate(self)]
        return all(matches)

    @classmethod
    def from_str_list(cls, str_list):
        labels = [Label(value) for value in str_list]
        return cls(labels)