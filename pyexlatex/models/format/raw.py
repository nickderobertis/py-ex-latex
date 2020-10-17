from mixins import EqOnAttrsMixin

from pyexlatex.models.item import IsLatexItemMixin, IsSpecificClassMixin


class Raw(IsSpecificClassMixin, IsLatexItemMixin, EqOnAttrsMixin):
    r"""
    Don't replace latex characters in this blocks such as \ or %, useful for adding latex commands or comments manually.
    """
    equal_attrs = ('contents',)

    def __init__(self, contents):
        self.contents = contents
        super().__init__()

    def __str__(self):
        return self.contents
