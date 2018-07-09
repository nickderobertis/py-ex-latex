from dero.latex.models.item import SimpleItem


class Title(SimpleItem):
    name = 'title'

    def __init__(self, contents):
        super().__init__(self.name, contents)