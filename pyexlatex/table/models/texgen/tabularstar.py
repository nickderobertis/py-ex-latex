from typing import Optional, Union, Any

from mixins.repr import ReprMixin

from pyexlatex.models.item import Item
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.sizes.textwidth import TextWidth
from pyexlatex.table import ColumnsAlignment
from pyexlatex.table.models.texgen.tabularbase import BaseTabular


class TabularStar(ContainerItem, Item, ReprMixin, BaseTabular):
    """
    tabular* environment, allows for controlling width. Gives additional column alignment X to fill available area
    """
    name = 'tabular*'
    repr_cols = ['align']

    def __init__(self, content, align: Optional[Union[ColumnsAlignment, str]] = None, width: Optional[Any] = None,
                 fill_between: bool = True):
        if not isinstance(content, (list, tuple)):
            content = [content]
        self.align = self._get_columns_alignment_from_passed_align(content, align)

        if width is None:
            width = TextWidth()
        self.width = width
        self.fill_between = fill_between

        # TODO [#21]: move booktabs requirement to cmidrule and others, not TabularStar and Tabular
        #
        # Need to get all nested table structure aggregating data to do this.
        self.add_package('booktabs')
        self.add_data_from_content(self.align)
        super().__init__(self.name, content, env_modifiers=self._modifier_str)

    @property
    def _modifier_str(self) -> str:
        return self._wrap_with_braces(self.width) + self._align_str  # type: ignore

    @property
    def _align_str(self) -> str:
        base_str = str(self.align)
        if self.fill_between:
            # TODO [#22]: make models for extracolsep and fill
            base_str = r'@{\extracolsep{\fill}}' + base_str
        return self._wrap_with_braces(base_str)  # type: ignore