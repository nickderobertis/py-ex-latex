from pyexlatex.models.item import NoOptionsNoContentsItem


class TextWidth(NoOptionsNoContentsItem):
    name = 'textwidth'

    def __init__(self):
        super().__init__(self.name)