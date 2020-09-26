from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.typing import PyexlatexItems


class PS(TextAreaMixin, SimpleItem):
    name = 'ps'

    def __init__(self, ps: PyexlatexItems):
        self.ps = ps
        super().__init__(self.name, self.ps)
