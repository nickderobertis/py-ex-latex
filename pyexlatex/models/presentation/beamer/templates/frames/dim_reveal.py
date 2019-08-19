from typing import Sequence, List, Union
from pyexlatex.models.presentation.beamer.frame.frame import Frame
from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.models.format.vfill import VFill
from pyexlatex.models.presentation.beamer.templates.lists.dim_reveal_items import DimAndRevealListItems
from pyexlatex.models.lists.ordered import OrderedList
from pyexlatex.models.lists.unordered import UnorderedList


class DimRevealMixin:

    def __init__(self, content: Sequence[str], ordered_list: bool = False, **frame_kwargs):
        if ordered_list:
            list_class = OrderedList
        else:
            list_class = UnorderedList
        content = list_class([DimAndRevealListItems(content, vertical_fill=True)])
        super().__init__(content, **frame_kwargs)


class DimRevealListFrame(DimRevealMixin, Frame):

    def __init__(self, content: Sequence[str], ordered_list: bool = False, **frame_kwargs):
        super().__init__(content, ordered_list=ordered_list, **frame_kwargs)