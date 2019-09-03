from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.item import SimpleItem


class SmallCaps(TextAreaMixin, SimpleItem):
    """
    Makes text all caps, but with originally capital letters slightly larger than other letters.
    """
    name = 'textsc'

    def __init__(self, contents, **kwargs):
        super().__init__(self.name, contents, **kwargs)
