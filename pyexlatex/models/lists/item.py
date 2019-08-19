from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.models.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.item import NoBracesItem
from pyexlatex.models.containeritem import ContainerItem
from mixins.repr import ReprMixin


class ListItem(ContainerItem, NoBracesItem, ReprMixin):
    name = 'item'
    repr_cols = ['contents']

    def __init__(self, contents, overlay: Optional['Overlay'] = None):
        super().__init__(self.name, contents, overlay=overlay)