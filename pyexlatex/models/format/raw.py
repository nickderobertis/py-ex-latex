from pyexlatex.models.item import IsLatexItemMixin, IsSpecificClassMixin


class Raw(IsSpecificClassMixin, IsLatexItemMixin):
    r"""
    Don't replace latex characters in this blocks such as \ or %, useful for adding latex commands or comments manually.
    """

    def __init__(self, contents):
        self.contents = contents
        super().__init__()

    def __str__(self):
        return self.contents
