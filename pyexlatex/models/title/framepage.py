from pyexlatex.models.item import NoOptionsNoContentsItem


class MakeFrameTitle(NoOptionsNoContentsItem):
    name = 'titlepage'

    def __init__(self):
        super().__init__(self.name)