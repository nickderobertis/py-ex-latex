from dero.latex.models.item import SimpleItem


class Caption(SimpleItem):
    name = 'caption'

    def __init__(self, contents):
        super().__init__(self.name, contents)


