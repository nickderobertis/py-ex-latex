from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.typing import PyexlatexItems


class Closing(TextAreaMixin, SimpleItem):
    name = 'closing'

    def __init__(self, closing: PyexlatexItems):
        self.closing = closing
        super().__init__(self.name, self.closing)
