from mixins.repr import ReprMixin
from pyexlatex.table.models.mixins.addvalues.row import RowAddMixin
from pyexlatex.texgen.replacements.file import general_latex_replacements


class DataItem(ReprMixin, RowAddMixin):
    repr_cols = ['value']

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{general_latex_replacements(str(self.value))}'

    def _add_class(self, other):
        from pyexlatex.table.models.table.row import Row
        from pyexlatex.table.models.data.row import DataRow
        # keep same class if both are same class
        # otherwise, default to Row class
        self_class = type(self)
        other_class = type(other)
        klass = DataRow if self_class == other_class else Row

        return klass

    def __len__(self):
        return 1