from typing import Sequence, List
from pyexlatex.models.lists.item import ListItem
from pyexlatex.models.lists.base import VerticalFillMixin
from pyexlatex.models.format.textcolor import TextColor
from pyexlatex.models.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.presentation.beamer.overlay.until_end import UntilEnd
from pyexlatex.models.presentation.beamer.overlay.next import NextWithIncrement, NextWithoutIncrement
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.item import ItemBase


class DimAndRevealListItem(ListItem):

    def __init__(self, contents, dim: bool = True, opacity: float = 0.3, **kwargs):
        dim_ov = Overlay([UntilEnd(NextWithoutIncrement(1))])
        next_ov = Overlay([UntilEnd(NextWithIncrement())])

        if dim:
            contents = TextColor(contents, 'black', opacity=opacity, overlay=dim_ov)

        super().__init__(contents, overlay=next_ov, **kwargs)


class DimAndRevealListItems(VerticalFillMixin, ContainerItem, ItemBase):
    name = '<dim and reveal container, should not enter latex output>'

    def __init__(self, contents: Sequence, dim_last_item: bool = False, opacity: float = 0.3,
                 vertical_fill: bool = False, **item_kwargs):
        self.orig_contents = contents
        self.dim_last_item = dim_last_item
        self.opacity = opacity
        self.item_kwargs = item_kwargs
        self.vertical_fill = vertical_fill
        self.add_data_from_content(contents)

    @property
    def contents(self) -> List[DimAndRevealListItem]:
        output = [DimAndRevealListItem(item, opacity=self.opacity, **self.item_kwargs) for item in self.orig_contents]
        if not self.dim_last_item:
            output[-1] = DimAndRevealListItem(
                self.orig_contents[-1], dim=False, opacity=self.opacity, **self.item_kwargs
            )

        return output

    def __str__(self) -> str:
        return self.generate_content(self.contents)
