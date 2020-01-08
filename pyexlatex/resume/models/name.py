from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin


class Name(TextAreaMixin, SimpleItem):
    name = 'name'

    def __init__(self, author: str):
        self.author = author
        super().__init__(self.name, self.author)
