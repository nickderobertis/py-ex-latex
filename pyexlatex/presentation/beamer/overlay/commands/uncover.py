from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.item import SimpleItem


class Uncover(SimpleItem):
    name = 'uncover'

    def __init__(self, contents, overlay: Optional['Overlay'] = None):
        super().__init__(self.name, contents, overlay=overlay)