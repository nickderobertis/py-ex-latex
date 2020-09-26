from typing import Optional, Sequence, Union, List
import pyexlatex as pl
from pyexlatex.models.template import Template


class Reference(Template):
    SPACE_BETWEEN_ADJUSTMENT = '-8pt'

    def __init__(self, name: str, title_lines: Optional[Sequence[str]] = None, company: Optional[str] = None,
                 contact_lines: Optional[Sequence[str]] = None, email: Optional[str] = None,
                 prevent_page_break: bool = True):
        self.name = name
        self.title_lines = title_lines
        self.company = company
        self.contact_lines = contact_lines
        self.email = email
        self.prevent_page_break = prevent_page_break
        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        if self.contact_lines:
            contact_lines = self.contact_lines
        else:
            contact_lines = []
        if self.title_lines:
            title_lines = [pl.Italics(line) for line in self.title_lines]
        else:
            title_lines = []

        possible_contents = [
            pl.SmallCaps(pl.Bold(self.name)),
            *title_lines,
            self.company,
            *contact_lines,
            self.email,
            pl.OutputLineBreak(size_adjustment=self.SPACE_BETWEEN_ADJUSTMENT),
        ]

        out_contents = []
        for content in possible_contents:
            out_contents.append(content)
            out_contents.append(pl.OutputLineBreak())  # force line breaks in content
        del out_contents[-1]  # remove last line break

        if self.prevent_page_break:
            out_contents = pl.NoPageBreak(out_contents)

        return out_contents
