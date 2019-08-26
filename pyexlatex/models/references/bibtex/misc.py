from typing import Optional, Dict
from pyexlatex.models.references.bibtex.base import BibTexEntryBase


class BibTexMisc(BibTexEntryBase):
    """
    Biblography document which is of miscellaneous type.
    """
    item_type = 'misc'
    optional_attrs = ['author', 'title', 'howpublished', 'month', 'year', 'note']

    def __init__(self, item_accessor: str, author: Optional[str] = None, title: Optional[str] = None,
                 howpublished: Optional[str] = None, month: Optional[str] = None, year: Optional[str] = None,
                 note: Optional[str] = None):
        self.author = author
        self.title = title
        self.howpublished = howpublished
        self.year = year
        self.month = month
        self.note = note

        self._validate()

        super().__init__(item_accessor)

    def _validate(self):
        all_values = [getattr(self, attr) for attr in self.optional_attrs]
        if all([value is None for value in all_values]):
            raise ValueError('must pass something non-None to BibTexMisc, got all None')
