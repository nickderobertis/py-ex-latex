from pyexlatex.models.item import SimpleItem

class Caption(SimpleItem):
    name = 'caption'

    def __init__(self, contents):
        if contents is None:
            contents = ' '
        super().__init__(self.name, contents)
