from pyexlatex.models.item import SimpleItem


class Label(SimpleItem):
    name = 'label'

    def __init__(self, contents):
        super().__init__(self.name, contents)