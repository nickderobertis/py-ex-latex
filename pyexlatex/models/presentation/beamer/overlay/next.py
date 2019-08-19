from pyexlatex.models.presentation.beamer.overlay.offset import Offset
from pyexlatex.models.presentation.beamer.overlay.overlay_param import OverlayParameter


class NextBase(OverlayParameter):
    next_char = '<invalid, use subclass, not NextBase directly>'

    def __init__(self, offset: int = 0):
        self.offset = Offset(offset)

    def __str__(self) -> str:
        return f'{self.next_char}{self.offset}'


class NextWithIncrement(NextBase):
    next_char = '+'


class NextWithoutIncrement(NextBase):
    next_char = '.'