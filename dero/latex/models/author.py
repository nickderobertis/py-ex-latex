from dero.latex.models.item import SimpleItem


class Author(SimpleItem):
    name = 'author'

    def __init__(self, contents):
        super().__init__(self.name, contents)