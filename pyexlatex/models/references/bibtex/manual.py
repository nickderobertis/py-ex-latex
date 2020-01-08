from typing import Optional, Dict
from pyexlatex.models.references.bibtex.base import BibTexEntryBase


class BibTexManual(BibTexEntryBase):
    """
    Biblography document which is a manual.
    """
    item_type = 'manual'
    required_attrs = ['title']
    optional_attrs = ['author', 'organization', 'address', 'edition', 'month', 'year', 'note']

    def __init__(self, item_accessor: str, title: str, author: Optional[str] = None, organization: Optional[str] = None,
                 address: Optional[str] = None, edition: Optional[str] = None,
                 month: Optional[str] = None, year: Optional[str] = None,
                 note: Optional[str] = None):
        self.author = author
        self.title = title
        self.organization = organization
        self.address = address
        self.edition = edition
        self.year = year
        self.month = month
        self.note = note

        super().__init__(item_accessor)
