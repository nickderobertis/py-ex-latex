from typing import Optional, Union, Sequence, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from dero.latex.models.presentation.beamer.overlay.overlay import Overlay
from dero.latex.models.item import Item, ItemBase
from dero.mixins.repr import ReprMixin
from dero.latex.models.lists.item import ListItem
from dero.latex.models.containeritem import ContainerItem

ListItemDefinition = Union[str, ListItem]


class ListBase(ContainerItem, Item, ReprMixin):
    name = 'list'
    repr_cols = ['contents']

    def __init__(self, items: Sequence[ListItemDefinition], overlay: Optional['Overlay'] = None, **kwargs):
        self.items = items
        self.overlay = overlay
        self.add_data_from_content(items)
        self.content = self.generate_content(items)
        env_modifier_overlay = f'[{overlay}]' if overlay is not None else None
        super().__init__(self.name, self.content, env_modifiers=env_modifier_overlay, **kwargs)

    @staticmethod
    def generate_content(items):
        from dero.latex.logic.builder import _build
        return _build([ListItem(item) if isinstance(item, str) else item for item in items])

