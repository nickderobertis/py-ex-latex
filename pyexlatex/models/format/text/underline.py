from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.item import SimpleItem


class Underline(TextAreaMixin, SimpleItem):
    name = 'underline'

    def __init__(self, contents, **kwargs):
        super().__init__(self.name, contents, **kwargs)
