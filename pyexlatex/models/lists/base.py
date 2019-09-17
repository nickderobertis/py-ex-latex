from typing import Optional, Union, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay import Overlay
from pyexlatex.models.item import Item
from mixins.repr import ReprMixin
from pyexlatex.models.lists.item import ListItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.format.fills import VFill


class VerticalFillMixin:
    vertical_fill = False

    def vertically_space_content(self, items):
        output = []
        for item in items:
            if not _can_be_included_directly_in_list(item):
                output.append(ListItem(item))
            else:
                output.append(item)
            if self.vertical_fill:
                output.append(VFill())
        if self.vertical_fill:
            output = output[:-1]  # strip final vertical fill, only fill inbetween items

        return output


class ListBase(TextAreaMixin, VerticalFillMixin, Item, ReprMixin):
    name = 'list'
    repr_cols = ['contents']

    def __init__(self, items: Sequence, overlay: Optional['Overlay'] = None,
                 vertical_fill: bool = False, **kwargs):
        self.items = items
        self.overlay = overlay
        self.vertical_fill = vertical_fill
        self.add_data_from_content(items)
        self.content = self.vertically_space_content(items)
        env_modifier_overlay = f'[{overlay}]' if overlay is not None else None
        super().__init__(self.name, self.content, env_modifiers=env_modifier_overlay, **kwargs)


def _can_be_included_directly_in_list(item) -> bool:
    if hasattr(item, 'is_SetCounter') and item.is_SetCounter:
        return True
    return _item_is_list_or_list_base(item)


def _item_is_list_or_list_base(item) -> bool:
    if hasattr(item, 'is_ListItem') and item.is_ListItem:
        return True
    if hasattr(item, 'is_ListBase') and item.is_ListBase:
        return True

    return False


