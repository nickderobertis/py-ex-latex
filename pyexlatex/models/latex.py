from pyexlatex.models.item import SimpleItem


class LaTeX(SimpleItem):
    """
    Displays the string "LaTeX" with special formatting
    """
    name = 'LaTeX'

    def __init__(self, **kwargs):
        super().__init__(self.name, '', **kwargs)
