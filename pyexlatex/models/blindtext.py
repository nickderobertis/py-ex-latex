from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.item import NoOptionsNoContentsItem


class BlindText(NoOptionsNoContentsItem):
    """
    Produces lorem ipsum dolor... etc. example text
    """
    name = 'blindtext'

    def __init__(self, overlay: Optional['Overlay'] = None):
        self.init_data()
        self.data.packages.append('blindtext')
        super().__init__(self.name, overlay=overlay)
