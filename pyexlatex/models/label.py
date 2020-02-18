from pyexlatex.models.item import SimpleItem


class Label(SimpleItem):
    """
    A label which can later be referred to by Ref
    """
    name = 'label'

    def __init__(self, contents):
        super().__init__(self.name, contents)