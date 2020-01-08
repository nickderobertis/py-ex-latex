from typing import Sequence, Type

from pyexlatex.models.lists.base import ListBase
from pyexlatex.presentation.beamer.frame.frame import Frame
from pyexlatex.presentation.beamer.templates.lists.dim_reveal_items import DimAndRevealListItems
from pyexlatex.models.lists.ordered import OrderedList
from pyexlatex.models.lists.unordered import UnorderedList


class DimRevealMixin:

    def __init__(self, content: Sequence[str], ordered_list: bool = False, **frame_kwargs):
        list_class: Type[ListBase]
        if ordered_list:
            list_class = OrderedList
        else:
            list_class = UnorderedList
        content = list_class([DimAndRevealListItems(content, vertical_fill=True)])
        super().__init__(content, **frame_kwargs)  # type: ignore


class DimRevealListFrame(DimRevealMixin, Frame):
    """
    A Frame where the content is bulleted or numbered dim and reveal items
    """

    def __init__(self, content: Sequence[str], ordered_list: bool = False, **frame_kwargs):
        super().__init__(content, ordered_list=ordered_list, **frame_kwargs)