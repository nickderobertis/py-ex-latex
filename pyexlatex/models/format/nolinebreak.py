from pyexlatex.models.item import SimpleItem
from pyexlatex.models.section.base import TextAreaMixin


class NoLineBreak(TextAreaMixin, SimpleItem):
    """
    Prevents a line break within text, where a hyphen would normally be placed.
    """
    name = 'mbox'

    def __init__(self, contents, **kwargs):
        super().__init__(self.name, contents, **kwargs)
