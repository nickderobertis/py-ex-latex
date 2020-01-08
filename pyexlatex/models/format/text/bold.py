from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.item import SimpleItem


class Bold(TextAreaMixin, SimpleItem):
    """
    Makes text bold.
    """
    name = 'textbf'

    def __init__(self, contents, **kwargs):
        super().__init__(self.name, contents, **kwargs)
