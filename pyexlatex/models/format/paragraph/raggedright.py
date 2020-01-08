from pyexlatex.models.item import NoOptionsNoContentsItem


class RaggedRight(NoOptionsNoContentsItem):
    name = 'raggedright'

    def __init__(self, **kwargs):
        super().__init__(self.name, **kwargs)