from pyexlatex.models.item import SimpleItem


class RightFooter(SimpleItem):
    name = 'rfoot'

    def __init__(self, contents):
        super().__init__(self.name, contents)

class CenterFooter(SimpleItem):
    name = 'cfoot'

    def __init__(self, contents):
        super().__init__(self.name, contents)