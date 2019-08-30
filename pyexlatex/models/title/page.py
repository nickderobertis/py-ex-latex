from typing import List
from pyexlatex.models.documentitem import DocumentItem
from pyexlatex.models.title.title import Title
from pyexlatex.models.credits.author import Author
from pyexlatex.models.date import Date
from pyexlatex.models.section.abstract import Abstract
from pyexlatex.texgen import _maketitle_str
from pyexlatex.logic.format.and_join import join_with_commas_and_and

class TitlePage(DocumentItem):

    def __init__(self, title: str = None, authors: List[str] = None, date: str = None, abstract: str = None):
        from pyexlatex.logic.builder import _build

        author = join_with_commas_and_and(authors)

        contents = [
            Title(title) if title is not None else None,
            Author(author, short_author=None) if author is not None else None,
            Date(date) if date is not None else Date(),
            _maketitle_str() if title is not None else None,
            Abstract(abstract) if abstract is not None else None
        ]

        self.contents = [content for content in contents if content is not None]

        self._output = _build(self.contents)

    def __str__(self):
        return self._output