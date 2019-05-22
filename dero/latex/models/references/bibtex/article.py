from typing import Optional, Dict
from dero.latex.models.references.bibtex.base import BibTexEntryBase


class BibTexArticle(BibTexEntryBase):
    item_type = 'article'

    def __init__(self, item_accessor: str, author: str, title: str, journal: str, year: str, volume: Optional[str] = None,
                 number: Optional[str] = None, pages: Optional[str] = None, month: Optional[str] = None,
                 note: Optional[str] = None):
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.number = number
        self.pages = pages
        self.month = month
        self.note = note

        super().__init__(item_accessor)

    @property
    def fields(self) -> Dict[str, str]:
        fields_dict = dict(
            author=self.author,
            title=self.title,
            journal=self.journal,
            year=self.year
        )

        optional_attrs = ['volume', 'number', 'pages', 'month', 'note']
        for attr in optional_attrs:
            self_attr = getattr(self, attr)
            if self_attr:
                fields_dict.update({attr: self_attr})

        return fields_dict