from pyexlatex.models.item import NoOptionsNoContentsItem


class VFill(NoOptionsNoContentsItem):
    """
    Vertical fill, put between items to put spacing between them.
    """
    name = 'vfill'

    def __init__(self):
        super().__init__(self.name)