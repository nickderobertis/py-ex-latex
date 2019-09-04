from typing import Optional
import pyexlatex as pl


class Education(pl.Template):

    def __init__(self, school: str, school_location: str, degree: str, expected: str, gpa: Optional[str] = None):
        self.school = school
        self.school_location = school_location
        self.degree = degree
        self.expected = expected
        self.gpa = gpa

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
            self.school_location
        ]
        items = [item for item in possible_items if item is not None]
        return items
