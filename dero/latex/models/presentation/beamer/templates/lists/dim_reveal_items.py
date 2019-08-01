from typing import Sequence, List
from dero.latex.models.lists.item import ListItem
from dero.latex.models.format.textcolor import TextColor
from dero.latex.models.presentation.beamer.overlay.overlay import Overlay
from dero.latex.models.presentation.beamer.overlay.until_end import UntilEnd
from dero.latex.models.presentation.beamer.overlay.next import NextWithIncrement, NextWithoutIncrement
from dero.latex.models.containeritem import ContainerItem
from dero.latex.models.item import ItemBase


class DimAndRevealListItem(ListItem):

    def __init__(self, contents, dim: bool = True, opacity: float = 0.3, **kwargs):
        dim_ov = Overlay([UntilEnd(NextWithoutIncrement(1))])
        next_ov = Overlay([UntilEnd(NextWithIncrement())])

        if dim:
            contents = TextColor(contents, 'black', opacity=opacity, overlay=dim_ov)

        super().__init__(contents, overlay=next_ov, **kwargs)


class DimAndRevealListItems(ContainerItem, ItemBase):
    name = '<dim and reveal container, should not enter latex output>'

    def __init__(self, contents: Sequence, dim_last_item: bool = False, opacity: float = 0.3, **item_kwargs):
        self.orig_contents = contents
        self.dim_last_item = dim_last_item
        self.opacity = opacity
        self.item_kwargs = item_kwargs
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
        from dero.latex.logic.builder import _build
        return _build(self.contents)
