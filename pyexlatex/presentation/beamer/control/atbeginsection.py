from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin


class AtBeginSection(TextAreaMixin, SimpleItem):
    name = 'AtBeginSection'

    def __init__(self, contents, **kwargs):
        super().__init__(self.name, contents, **kwargs)
