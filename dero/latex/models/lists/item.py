from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from dero.latex.models.presentation.beamer.overlay.overlay import Overlay
from dero.latex.models.item import NoBracesItem
from dero.mixins.repr import ReprMixin


class ListItem(NoBracesItem, ReprMixin):
    name = 'item'
    repr_cols = ['contents']

    def __init__(self, contents, overlay: Optional['Overlay'] = None):
        super().__init__(self.name, contents, overlay=overlay)