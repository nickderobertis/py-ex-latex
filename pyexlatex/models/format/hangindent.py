from pyexlatex.models.item import EqualsItem


class HangIndent(EqualsItem):
    name = 'hangindent'

    def __init__(self, hang_by: float = 1):
        self.hang_by = hang_by
        super().__init__(self.name, f'{self.hang_by}cm')
