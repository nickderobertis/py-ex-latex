from dero.latex.models.item import IsLatexItemMixin, IsSpecificClassMixin


class Raw(IsSpecificClassMixin, IsLatexItemMixin):
    """
    don't replace latex characters in this block
    """

    def __init__(self, contents):
        self.contents = contents
        super().__init__()

    def __str__(self):
        return self.contents
