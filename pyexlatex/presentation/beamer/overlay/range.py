from mixins.repr import ReprMixin
from pyexlatex.presentation.beamer.overlay import OverlayParameter


class Range(ReprMixin, OverlayParameter):
    repr_cols = ['low', 'high']

    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high

    def __str__(self) -> str:
        return f'{self.low}-{self.high}'