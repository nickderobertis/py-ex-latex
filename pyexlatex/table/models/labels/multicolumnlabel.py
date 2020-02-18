from pyexlatex.models.item import MultiOptionSimpleItem


class MultiColumnLabel(MultiOptionSimpleItem):
    """
    A label which spans multiple columns in a table
    """
    name = 'multicolumn'

    def __init__(self, contents: str, span: int, align: str='c', add_table_line_break: bool = True):
        self.add_table_line_break = add_table_line_break
        self.span = span
        super().__init__(self.name, span, align, contents)

    def __len__(self):
        return self.span

    def __str__(self) -> str:
        from pyexlatex.models.format.breaks import TableLineBreak
        orig_str = super().__str__()
        if self.add_table_line_break:
            return orig_str + str(TableLineBreak())
        return orig_str

