from dero.latex.models.item import MultiOptionSimpleItem

class MultiColumn(MultiOptionSimpleItem):
    name = 'multicolumn'

    def __init__(self, contents: str, span: int, align: str='c'):
        self.span = span
        super().__init__(self.name, span, align, contents)

    def __len__(self):
        return self.span
