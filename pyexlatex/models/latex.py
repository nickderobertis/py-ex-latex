from pyexlatex.models.item import SimpleItem


class LaTeX(SimpleItem):
    name = 'LaTeX'

    def __init__(self, **kwargs):
        super().__init__(self.name, '', **kwargs)
