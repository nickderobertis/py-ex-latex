from dero.latex.models.item import SimpleItem


class Ref(SimpleItem):
    name = 'ref'

    def __init__(self, contents):
        super().__init__(self.name, contents)