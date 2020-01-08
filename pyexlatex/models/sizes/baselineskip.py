from pyexlatex.models.item import NoOptionsNoContentsItem


class BaselineSkip(NoOptionsNoContentsItem):
    name = 'baselineskip'

    def __init__(self):
        super().__init__(self.name)
