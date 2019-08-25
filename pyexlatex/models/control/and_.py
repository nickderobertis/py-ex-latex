from pyexlatex.models.item import NoOptionsNoContentsItem


class And(NoOptionsNoContentsItem):
    """
    Used internally for writing multiple institutions.
    """
    name = 'and'

    def __init__(self):
        super().__init__(self.name)