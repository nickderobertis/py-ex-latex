from typing import Optional
from pyexlatex.models.template import Template
import pyexlatex as pl


class Education(Template):
    SPACE_BETWEEN_ADJUSTMENT = '-8pt'

    def __init__(self, school: str, school_location: str, degree: str, expected: str, gpa: Optional[str] = None,
                 prevent_page_break: bool = True):
        self.school = school
        self.school_location = school_location
        self.degree = degree
        self.expected = expected
        self.gpa = gpa
        self.prevent_page_break = prevent_page_break

        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        possible_items = [
            pl.Bold(self.school),
            f' (GPA {self.gpa})' if self.gpa is not None else None,
            pl.HFill(),
            pl.Bold(self.expected),
            pl.OutputLineBreak(),
            pl.Italics(self.degree),
            pl.HFill(),
            self.school_location,
            pl.OutputLineBreak(size_adjustment=self.SPACE_BETWEEN_ADJUSTMENT)
        ]
        items = [item for item in possible_items if item is not None]
        if self.prevent_page_break:
            items = pl.NoPageBreak(items)
        return items
