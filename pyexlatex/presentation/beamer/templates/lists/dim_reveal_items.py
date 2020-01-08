from typing import Sequence, List
from pyexlatex.models.lists.item import ListItem
from pyexlatex.models.lists.base import VerticalFillMixin
from pyexlatex.models.format.text.color.main import TextColor
from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.presentation.beamer.overlay.until_end import UntilEnd
from pyexlatex.presentation.beamer.overlay.next import NextWithIncrement, NextWithoutIncrement
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.item import ItemBase
from pyexlatex.models.lists.base import can_be_included_directly_in_list


class DimAndRevealListItem(ListItem):
    """
    Single list item which reveals on each slide one-by-one and as the next one reveals, the last one dims.

    Use DimAndRevealListItems to construct.
    """
    is_ListItem = True  # so that passing within lists will treat as a list item

    def __init__(self, contents, dim: bool = True, opacity: float = 0.3):
        self.dim = dim
        dim_ov = Overlay([UntilEnd(NextWithoutIncrement(1))])
        next_ov = Overlay([UntilEnd(NextWithIncrement())])

        if dim:
            contents = TextColor(contents, 'black', opacity=opacity, overlay=dim_ov)

        super().__init__(contents, overlay=next_ov)

    def convert_to_regular_item(self):
        if self.dim:
            contents = self.contents.content  # get from inside TextColor
        else:
            contents = self.contents
        item = ListItem(contents)
        self.__dict__.update(item.__dict__)
        self.__class__ = ListItem
        del self.is_DimAndRevealListItem
        del self.dim


class DimAndRevealListItems(VerticalFillMixin, ContainerItem, ItemBase):
    """
    List items which reveal on each slide one-by-one and as the next one reveals, the last one dims.

    Pass to a list class such as OrderedList or UnorderedList
    """
    name = '<dim and reveal container, should not enter latex output>'
    is_ListBase = True  # so that passing within lists will treat as a list

    def __init__(self, contents: Sequence, dim_last_item: bool = False, opacity: float = 0.3,
                 vertical_fill: bool = False, dim_earlier_items: bool = True):
        self.orig_contents = contents
        self.dim_last_item = dim_last_item
        self.dim_earlier_items = dim_earlier_items
        self.opacity = opacity
        self.vertical_fill = vertical_fill
        self.add_data_from_content(contents)
        self.contents = self._get_contents()

    def _get_contents(self) -> List[DimAndRevealListItem]:
        output = []
        for item in self.orig_contents:
            if can_be_included_directly_in_list(item):
                output.append(item)
            else:
                output.append(
                    DimAndRevealListItem(
                        item,
                        opacity=self.opacity,
                        dim=self.dim_earlier_items,
                    )
                )

        if not self.dim_last_item:
            output[-1] = DimAndRevealListItem(
                self.orig_contents[-1], dim=False, opacity=self.opacity
            )
        output = self.vertically_space_content(output)

        return output

    def __str__(self) -> str:
        from pyexlatex.logic.builder import _build
        if isinstance(self.contents, str):
            return self.contents
        return _build(self.contents)


def eliminate_dim_reveal(content):
    """
    Eliminates dim/reveal from nested content. Modifies in place by using regular list items
    """
    if hasattr(content, 'content'):
        eliminate_dim_reveal(content.content)
    if hasattr(content, 'contents'):
        eliminate_dim_reveal(content.contents)
    if hasattr(content, 'is_DimAndRevealListItem') and content.is_DimAndRevealListItem:
        content.convert_to_regular_item()
    if isinstance(content, (list, tuple)):
        [eliminate_dim_reveal(c) for c in content]
