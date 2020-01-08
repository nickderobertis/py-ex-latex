from pyexlatex.models.item import SimpleItem


class Footnote(SimpleItem):
    """
    Creates a footnote at the bottom of the page, with a mark next to where the object itself is placed to
    reference the footnote.
    """
    name = 'footnote'

    def __init__(self, contents):
        super().__init__(self.name, contents)
