from typing import Optional, Sequence, Union, List, Any
import pyexlatex as pl
from pyexlatex.models.template import Template
from pyexlatex.models.format.text.bold import Bold
from pyexlatex.models.hyperlinks import Hyperlink
from pyexlatex.logic.format.and_join import join_with_commas_and_and_output_list
from pyexlatex.models.format.hangindent import HangIndent
from pyexlatex.models.format.paragraph.justifying import Justifying


class Publication(Template):
    SPACE_BETWEEN_ADJUSTMENT = 0.2

    def __init__(self, title: str, co_authors: Optional[Sequence[str]] = None, journal_info: Optional[str] = None,
                 href: Optional[str] = None, extra_info: Optional[str] = None, prevent_page_break: bool = True,
                 description: Optional[Any] = None):
        self.title = title
        self.co_authors = co_authors
        self.journal_info = journal_info
        self.href = href
        self.extra_info = extra_info
        self.prevent_page_break = prevent_page_break
        self.description = description

        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        possible_items = [
            HangIndent(1),
            self._title_str,
            pl.Italics(self.journal_info) if self.journal_info is not None else None,
            self._with_coauthors,
            self.extra_info,
            *self._description_content,
            pl.VSpace(self.SPACE_BETWEEN_ADJUSTMENT),
        ]
        items = [item for item in possible_items if item is not None]
        if self.prevent_page_break:
            items = pl.NoPageBreak(items)
        return items

    @property
    def _title_obj(self) -> Union[Bold, Hyperlink]:
        if self.href is None:
            title = Bold(self.title)
        else:
            # Handle hyperlink
            styled_title = pl.TextColor(self.title, color=pl.RGB(50, 82, 209, color_name='darkblue'))
            styled_title = pl.Underline(styled_title)
            title = Hyperlink(self.href, styled_title)
            self.add_data_from_content(title)
        return title

    @property
    def _title_str(self) -> str:
        title_str = str(self._title_obj)
        if any([item is not None for item in [self.co_authors, self.journal_info, self.extra_info]]):
            title_str += ','
        return title_str


    @property
    def _with_coauthors(self) -> Optional[List[str]]:
        if self.co_authors is None:
            return None

        return [' with ', *join_with_commas_and_and_output_list(self.co_authors)]

    @property
    def _description_content(self) -> List:
        if self.description is None:
            return []

        return [
            '',  # separate paragraph
            Justifying(),  # return to justifying on both sides
            self.description,
            pl.VSpace(0.2)  # extra spacing looks good when description is included
        ]

