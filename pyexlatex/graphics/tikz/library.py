from pyexlatex.models.item import SimpleItem


class TikZLibrary(SimpleItem):
    name = 'usetikzlibrary'

    def __init__(self, contents):
        super().__init__(self.name, contents)