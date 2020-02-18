from pyexlatex.models.mixins import StringAdditionMixin
from mixins.repr import ReprMixin


class Break(StringAdditionMixin):
    pass

class LineBreak(Break):

    def __init__(self):
        pass

    def __str__(self):
        return '\n'


class TableLineBreak(Break, ReprMixin):
    """
    A line break character to be used in LaTeX tables
    """
    repr_cols = ['size_adjustment']

    def __init__(self, size_adjustment: str=None):
        self.size_adjustment = size_adjustment

    def __str__(self):
        return _table_break_str(self.size_adjustment, add_line_break=True)


class OutputLineBreak(Break, ReprMixin):
    """
    Create an intentional line break in text
    """
    repr_cols = ['size_adjustment']

    def __init__(self, size_adjustment: str=None):
        self.size_adjustment = size_adjustment

    def __str__(self):
        return _table_break_str(self.size_adjustment)


def _table_break_str(size_adjustment: str=None, add_line_break: bool = False):
    if size_adjustment:
        size_adjustment_str = f'[{size_adjustment}]'
    else:
        size_adjustment_str = ''
    output_str = r'\\' + size_adjustment_str
    if add_line_break:
        output_str += LineBreak()
    return  output_str