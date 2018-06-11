from dero.latex.models.mixins import StringAdditionMixin, ReprMixin

class Break(StringAdditionMixin):
    pass

class LineBreak(Break):

    def __init__(self):
        pass

    def __str__(self):
        return '\n'

class TableRowBreak(Break, ReprMixin):
    repr_cols = ['size_adjustment']

    def __init__(self, size_adjustment: str=None):
        self.size_adjustment = size_adjustment

    def __str__(self):
        return _table_break_str(self.size_adjustment)


def _table_break_str(size_adjustment: str=None):
    if size_adjustment:
        size_adjustment_str = f'[{size_adjustment}]'
    else:
        size_adjustment_str = ''

    return r'\\' + size_adjustment_str + LineBreak()