from typing import Optional, Dict
from pyexlatex.models.references.bibtex.base import BibTexEntryBase


class BibTexArticle(BibTexEntryBase):
    """
    Biblography document which is an article.
    """
    item_type = 'article'
    required_attrs = ['author', 'title', 'journal', 'year']
    optional_attrs = ['volume', 'number', 'pages', 'month', 'note']

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
