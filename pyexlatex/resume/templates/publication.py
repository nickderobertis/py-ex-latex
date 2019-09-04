from typing import Optional, Sequence, Union
import pyexlatex as pl
from pyexlatex.logic.format.and_join import join_with_commas_and_and
from pyexlatex.models.format.hangindent import HangIndent


class Publication(pl.Template):

    def __init__(self, title: str, co_authors: Optional[Sequence[str]], journal_info: Optional[str] = None,
                 href: Optional[str] = None, extra_info: Optional[str] = None):
        self.title = title
        self.co_authors = co_authors
        self.journal_info = journal_info
        self.href = href
        self.extra_info = extra_info

        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        possible_items = [
            HangIndent(1),
            self._title_str,
            pl.Italics(self.journal_info) if self.journal_info is not None else None,
            self._with_coauthors,
            self.extra_info
        ]
        items = [item for item in possible_items if item is not None]
        return items

    @property
    def _title_obj(self) -> Union[pl.Bold, pl.Hyperlink]:
        if self.href is None:
            title = pl.Bold(self.title)
        else:
            # Handle hyperlink
            styled_title = pl.TextColor(self.title, color=pl.RGB(50, 82, 209, color_name='darkblue'))
            styled_title = pl.Underline(styled_title)
            title = pl.Hyperlink(self.href, styled_title)
            self.add_data_from_content(title)
        return title

    @property
    def _title_str(self) -> str:
        title_str = str(self._title_obj)
        if any([item is not None for item in [self.co_authors, self.journal_info, self.extra_info]]):
            title_str += ','
        return title_str


    @property
    def _with_coauthors(self) -> Optional[str]:
        if self.co_authors is None:
            return None

        return f' with {join_with_commas_and_and(self.co_authors)}'
