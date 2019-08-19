from pyexlatex.models.item import NoOptionsNoContentsItem


class LineWidth(NoOptionsNoContentsItem):
    name = 'linewidth'

    def __init__(self):
        super().__init__(self.name)