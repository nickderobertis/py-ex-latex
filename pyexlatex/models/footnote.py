from pyexlatex.models.item import SimpleItem


class Footnote(SimpleItem):
    name = 'footnote'

    def __init__(self, contents):
        super().__init__(self.name, contents)
