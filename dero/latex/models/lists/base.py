from typing import Optional, Union, Sequence, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from dero.latex.models.presentation.beamer.overlay.overlay import Overlay
from dero.latex.models.item import Item
from dero.mixins.repr import ReprMixin
from dero.latex.models.lists.item import ListItem

ListItemDefinition = Union[str, ListItem]


class ListBase(Item, ReprMixin):
    name = 'list'
    repr_cols = ['contents']

    def __init__(self, items: Sequence[ListItemDefinition], overlay: Optional['Overlay'] = None):
        self.items = items
        self.overlay = overlay
        self.content = self.generate_content(items)
        env_modifier_overlay = f'[{overlay}]' if overlay is not None else None
        super().__init__(self.name, self.content, env_modifiers=env_modifier_overlay)

    @staticmethod
    def generate_content(items):
        from dero.latex.logic.builder import _build
        return _build([ListItem(item) if isinstance(item, str) else item for item in items])

