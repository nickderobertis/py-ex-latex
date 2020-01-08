from typing import Optional, Union, Sequence, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.item import Item
from mixins.repr import ReprMixin
from pyexlatex.models.lists.item import ListItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.format.fills import VFill
from pyexlatex.logic.type_check import item_is_in_allowed_type_strs


class VerticalFillMixin:
    vertical_fill = False

    def vertically_space_content(self, items):
        output = []
        for item in items:
            if not can_be_included_directly_in_list(item):
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


def can_be_included_directly_in_list(item) -> bool:
    check_funcs = [
        _can_be_included_directly_in_list_but_is_not_list,
        _item_is_list_or_list_base
    ]
    for func in check_funcs:
        if func(item):
            return True

    return False


def _can_be_included_directly_in_list_but_is_not_list(item) -> bool:
    allowed_values = [
        'SetCounter',
        'Raw',
        'TextSize'
    ]
    return item_is_in_allowed_type_strs(item, allowed_values)


def _item_is_list_or_list_base(item) -> bool:
    allowed_values = [
        'ListItem',
        'ListBase'
    ]
    return item_is_in_allowed_type_strs(item, allowed_values)

