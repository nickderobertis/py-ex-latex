from typing import Optional, Union, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay import Overlay
from pyexlatex.models.item import Item
from mixins.repr import ReprMixin
from pyexlatex.models.lists.item import ListItem
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.format.fills import VFill

ListItemDefinition = Union[str, ListItem]


class VerticalFillMixin:
    vertical_fill = False

    def vertically_space_content(self, items):
        output = []
        for item in items:
            if isinstance(item, str):
                output.append(ListItem(item))
            else:
                output.append(item)
            if self.vertical_fill:
                output.append(VFill())
        if self.vertical_fill:
            output = output[:-1]  # strip final vertical fill, only fill inbetween items

        return output


class ListBase(VerticalFillMixin, ContainerItem, Item, ReprMixin):
    name = 'list'
    repr_cols = ['contents']

    def __init__(self, items: Sequence[ListItemDefinition], overlay: Optional['Overlay'] = None,
                 vertical_fill: bool = False, **kwargs):
        self.items = items
        self.overlay = overlay
        self.vertical_fill = vertical_fill
        self.add_data_from_content(items)
        self.content = self.vertically_space_content(items)
        env_modifier_overlay = f'[{overlay}]' if overlay is not None else None
        super().__init__(self.name, self.content, env_modifiers=env_modifier_overlay, **kwargs)


