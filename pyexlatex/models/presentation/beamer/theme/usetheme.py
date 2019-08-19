from pyexlatex.models.item import SimpleItem


class UseTheme(SimpleItem):
    name = 'usetheme'

    def __init__(self, contents):
        super().__init__(self.name, contents)