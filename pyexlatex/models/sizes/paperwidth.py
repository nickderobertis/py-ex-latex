from pyexlatex.models.item import NoOptionsNoContentsItem


class PaperWidth(NoOptionsNoContentsItem):
    name = 'paperwidth'

    def __init__(self):
        super().__init__(self.name)
