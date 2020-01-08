from pyexlatex.presentation.beamer.overlay.offset import Offset
from pyexlatex.presentation.beamer.overlay.overlay_param import OverlayParameter


class NextBase(OverlayParameter):
    next_char = '<invalid, use subclass, not NextBase directly>'

    def __init__(self, offset: int = 0):
        self.offset = Offset(offset)

    def __str__(self) -> str:
        return f'{self.next_char}{self.offset}'


class NextWithIncrement(NextBase):
    """
    Option to be passed to Overlay which makes object appear on the next slide of the frame, and creates an additional
    slide
    """
    next_char = '+'


class NextWithoutIncrement(NextBase):
    """
        Option to be passed to Overlay which makes object appear on the next slide of the frame, and does not creates
        an additional slide
        """
    next_char = '.'
