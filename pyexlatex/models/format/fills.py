from pyexlatex.models.item import NoOptionsNoContentsItem


class VFill(NoOptionsNoContentsItem):
    """
    Vertical fill, put between items to put vertical spacing between them.
    """
    name = 'vfill'

    def __init__(self):
        super().__init__(self.name)


class HFill(NoOptionsNoContentsItem):
    """
    Horizontal fill, put between items to put horizontal spacing between them.
    """
    name = 'hfill'

    def __init__(self):
        super().__init__(self.name)