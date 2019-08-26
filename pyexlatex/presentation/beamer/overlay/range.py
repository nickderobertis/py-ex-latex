from mixins.repr import ReprMixin
from pyexlatex.presentation.beamer.overlay.overlay_param import OverlayParameter


class Range(ReprMixin, OverlayParameter):
    """
    Option to be passed to Overlay which says object should exist on the frame on a certain range of slides
    e.g. slide 1-3 of the frame.
    """
    repr_cols = ['low', 'high']

    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high

    def __str__(self) -> str:
        return f'{self.low}-{self.high}'