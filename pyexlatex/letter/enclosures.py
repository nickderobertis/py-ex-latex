from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.typing import PyexlatexItems


class Enclosures(TextAreaMixin, SimpleItem):
    name = 'encl'

    def __init__(self, encl: PyexlatexItems):
        self.encl = encl
        super().__init__(self.name, self.encl)
