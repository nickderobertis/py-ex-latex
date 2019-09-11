from pyexlatex.models.item import SimpleItem


class HSpace(SimpleItem):
    """
    Manually insert horizontal spacing, of a given length.
    """
    name = 'hspace'

    def __init__(self, height: float = 0.5, units: str = 'cm'):
        self.height = height
        self.units = units
        super().__init__(self.name, contents=f'{height}{units}')
