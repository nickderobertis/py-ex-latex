from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.item import NoOptionsNoContentsItem
from pyexlatex.models.section.base import TextAreaBase


class Centering(NoOptionsNoContentsItem):
    name = 'centering'

    def __init__(self, overlay: Optional['Overlay'] = None):
        super().__init__(self.name, overlay=overlay)


class Center(TextAreaBase):
    """
    Align the passed contents to the center of the container
    """
    name = 'center'

    def __init__(self, content, **kwargs):
        super().__init__(self.name, content, **kwargs)