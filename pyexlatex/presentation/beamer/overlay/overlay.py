from typing import Union, Sequence
from pyexlatex.presentation.beamer.overlay.overlay_param import OverlayParameter

OverlayOption = Union[OverlayParameter, int]


class Overlay:
    """
    Creates an effect on a frame such as appearing on a later frame.
    """

    def __init__(self, overlay_options: Sequence[OverlayOption]):
        self.overlay_options = overlay_options

    @property
    def overlay_options_str(self) -> str:
        return ','.join([str(option) for option in self.overlay_options])

    def __str__(self) -> str:
        if self.overlay_options_str == '':
            return ''
        return f'<{self.overlay_options_str}>'