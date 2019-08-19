from pyexlatex.models.item import NoOptionsNoContentsItem


class TextHeight(NoOptionsNoContentsItem):
    name = 'textheight'

    def __init__(self):
        super().__init__(self.name)