from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.item import NoBracesItem
from pyexlatex.models.section.base import TextAreaMixin
from mixins.repr import ReprMixin


class ListItem(TextAreaMixin, NoBracesItem, ReprMixin):
    name = 'item'
    repr_cols = ['contents']

    def __init__(self, contents, overlay: Optional['Overlay'] = None):
        super().__init__(self.name, contents, overlay=overlay)