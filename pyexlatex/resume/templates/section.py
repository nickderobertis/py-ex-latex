from typing import Optional, Union, List
from pyexlatex.models.template import Template
import pyexlatex as pl
from pyexlatex.models.format.paragraph.multicol import MultiColumn


class SpacedSection(Template):
    """
    A section which appropriately spaces content for a resume.
    """

    def __init__(self, contents, title: str, end_adjustment: float = -0.2,
                 num_cols: int = 1):
        self.end_adjustment = end_adjustment
        self.num_cols = num_cols

        if not isinstance(contents, (list, tuple)):
            contents = [contents]

        all_contents: Union[List[Union[pl.VSpace, str]], MultiColumn] = [pl.VSpace(0.2)]
        for content in contents:
            all_contents.append(content)
            all_contents.append('')
        all_contents[-1] = pl.VSpace(end_adjustment)  # replace final spacing

        if self.num_cols > 1:
            all_contents = MultiColumn(all_contents, num_cols=self.num_cols)

        self.contents = pl.Section(all_contents, title=title)
        super().__init__()
