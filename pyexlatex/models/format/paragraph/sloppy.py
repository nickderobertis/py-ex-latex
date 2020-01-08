from pyexlatex.models.item import NoOptionsNoContentsItem


class Sloppy(NoOptionsNoContentsItem):
    name = 'sloppy'

    def __init__(self, **kwargs):
        super().__init__(self.name, **kwargs)