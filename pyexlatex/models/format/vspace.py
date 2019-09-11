from pyexlatex.models.item import SimpleItem


class VSpace(SimpleItem):
    """
    Manually insert vertical spacing, of a given height.
    """
    name = 'vspace'

    def __init__(self, height: float = 0.5, units: str = 'cm'):
        self.height = height
        self.units = units
        super().__init__(self.name, contents=f'{height}{units}')
