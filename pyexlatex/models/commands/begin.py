from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.item import SimpleItem


class Begin(SimpleItem):
    name = 'begin'

    def __init__(self, env: str, modifiers: Optional[str] = None, overlay: Optional['Overlay'] = None):
        self.env = env
        super().__init__(self.name, env, modifiers, overlay=overlay)
