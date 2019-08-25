from typing import Sequence
from pyexlatex.models.layouts.base import LayoutBase
from pyexlatex.models.presentation.beamer.columns.columns import Columns
from pyexlatex.models.presentation.beamer.columns.column import Column


class MultiCol(LayoutBase):

    def __init__(self, content: Sequence, **kwargs):
        self.orig_content = content
        super().__init__(content, **kwargs)
        self.content = self._get_column_content(self.contents)

    def _get_column_content(self, content: Sequence) -> Columns:
        num_cols = len(content)
        output = Columns(
            [Column(c, frac_of_page_height=None, frac_of_text_width=self.column_width) for c in content]
        )
        return output

    @property
    def column_width(self) -> float:
        num_cols = len(self.orig_content)
        spacing = (num_cols - 1) * 0.1
        split_width = 1 - spacing
        return split_width/num_cols
