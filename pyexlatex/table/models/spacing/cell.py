

from pyexlatex.table.models.labels.label import Label

class CellSpacer(Label):

    def __init__(self, width=1):
        super().__init__(' ', span=width)

    def __repr__(self):
        return f'<CellSpacer(width={self.span})>'

    def __str__(self):
        if len(self) == 1:
            return str(self.value)
        else:
            return ' & '.join([self.value for i in range(len(self))])