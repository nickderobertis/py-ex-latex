from dero.latex.models.item import NoOptionsNoContentsItem


class VFill(NoOptionsNoContentsItem):
    name = 'vfill'

    def __init__(self):
        super().__init__(self.name)