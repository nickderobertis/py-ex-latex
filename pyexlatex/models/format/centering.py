from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.models.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.item import NoOptionsNoContentsItem


class Centering(NoOptionsNoContentsItem):
    name = 'centering'

    def __init__(self, overlay: Optional['Overlay'] = None):
        super().__init__(self.name, overlay=overlay)
