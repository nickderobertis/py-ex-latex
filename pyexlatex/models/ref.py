from pyexlatex.models.item import SimpleItem


class Ref(SimpleItem):
    """
    Pass a label to create an in text reference to that label.
    """
    name = 'ref'

    def __init__(self, contents):
        super().__init__(self.name, contents)