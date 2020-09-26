from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.typing import PyexlatexItems


class Opening(TextAreaMixin, SimpleItem):
    name = 'opening'

    def __init__(self, opening: PyexlatexItems):
        self.opening = opening
        super().__init__(self.name, self.opening)
