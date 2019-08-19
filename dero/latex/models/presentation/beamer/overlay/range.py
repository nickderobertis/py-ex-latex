from mixins.repr import ReprMixin
from dero.latex.models.presentation.beamer.overlay.overlay_param import OverlayParameter


class Range(ReprMixin, OverlayParameter):
    repr_cols = ['low', 'high']

    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high

    def __str__(self) -> str:
        return f'{self.low}-{self.high}'