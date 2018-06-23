from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.mixins.addvalues.row import RowAddMixin
from dero.latex.table.models.labels.multicolumn import MultiColumn
from dero.latex.texgen import general_latex_replacements


class Label(ReprMixin, RowAddMixin):
    """
    Only necessary to use if need to set span or alignment manually. Can construct LabelCollection objects from Labels.

    Useful for constructing custom multicolumn labels.

    >>>import dero.latex.table as lt
    >>>data_table = lt.DataTable.from_df(some_df)
    >>>label = lt.Label('Long label', span=5, align='r')
    >>>long_label_collection = lt.LabelCollection([label], underline='1-5')
    >>>
    >>>data_table.column_labels.insert(long_label_collection, 0)
    """
    repr_cols = ['value', 'span']

    def __init__(self, value, span: int=1, align='c'):
        self.value = value
        self.span = span
        self.align = _set_align(align)

    def __eq__(self, other):
        if hasattr(other, 'value'):
            return self.value == other.value
        else:
            return self.value == other

    def __str__(self):
        latex_valid_value = general_latex_replacements(str(self.value))
        if len(self) == 1:
            return str(latex_valid_value)
        else:
            return str(MultiColumn(latex_valid_value, span=self.span, align=self.align))

    def __len__(self):
        return self.span

    def _add_class(self, other):
        from dero.latex.table.models.table.row import Row
        from dero.latex.table.models.labels.row import LabelRow
        # keep same class if both are same class
        # otherwise, default to Row class
        self_class = type(self)
        other_class = type(other)
        klass = LabelRow if self_class == other_class else Row

        return klass

def _set_align(align: str):
    align = align.lower().strip()

    assert align in ('l', 'c', 'r')

    return align