from pyexlatex.models.item import SimpleItem


class PageStyle(SimpleItem):
    name = 'pagestyle'

    def __init__(self, contents):
        super().__init__(self.name, contents)