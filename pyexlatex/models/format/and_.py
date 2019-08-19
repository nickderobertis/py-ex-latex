from pyexlatex.models.item import NoOptionsNoContentsItem


class And(NoOptionsNoContentsItem):
    name = 'and'

    def __init__(self):
        super().__init__(self.name)