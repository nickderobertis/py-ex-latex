from typing import Optional
from pyexlatex.models.item import (
    StringAdditionMixin,
    IsSpecificClassMixin,
    IsLatexItemMixin,
    _basic_item_str,
    _multi_option_item_str,
    ItemBase
)

class LineSpacing(ItemBase):

    def __init__(self, line_spacing: float):
        self.logical_line_spacing = line_spacing
        self.latex_line_spacing = latex_line_spacing_from_logical_line_spacing(line_spacing)
        super().__init__()

    @property
    def name(self):
        if self.logical_line_spacing == 2:
            return 'doublespacing'
        if self.logical_line_spacing == 1.5:
            return 'onehalfspacing'
        if self.logical_line_spacing == 1:
            return 'singlespacing'
        else:
            return 'setstretch'

    @property
    def _options_str(self) -> str:
        if self.logical_line_spacing in (1, 1.5, 2):
            return ''
        return f'{self.latex_line_spacing}'

    def __str__(self):
        options = self._options_str
        if options:
            return _basic_item_str(self.name, options)
        return _multi_option_item_str(self.name)


def latex_line_spacing_from_logical_line_spacing(line_spacing: float) -> float:
    """
    Latex for some reason has 1.65 as double line spacing, 1.325 as one and a half
    line spacing, and 1 as single spacing. Take an input on a normal scale (2 is
    double spaced, 1 is single space, 1.5 is one and a half spacing, and so on), and
    convert to the latex scale.
    Args:
        line_spacing:

    Returns:

    """
    return round((line_spacing - 1) * (0.65/1) + 1, 2)
