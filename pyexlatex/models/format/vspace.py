from pyexlatex.models.item import SimpleItem


class VSpace(SimpleItem):
    """
    Manually insert vertical spacing, of a given height.
    """
    name = 'vspace'

    def __init__(self, height: float = 0.5):
        super().__init__(self.name, contents=f'{height}cm')
