from dero.latex.models.documentitem import DocumentItem
from dero.latex.models.title.title import Title
from dero.latex.models.credits.author import Author
from dero.latex.models.date import Date
from dero.latex.models.section.abstract import Abstract
from dero.latex.texgen import _maketitle_str

class TitlePage(DocumentItem):

    def __init__(self, title: str = None, author: str = None, date: str = None, abstract: str = None):
        from dero.latex.logic.builder import _build

        contents = [
            Title(title) if title is not None else None,
            Author(author) if author is not None else None,
            Date(date) if date is not None else Date(),
            _maketitle_str(),
            Abstract(abstract) if abstract is not None else None
        ]

        self.contents = [content for content in contents if content is not None]

        self._output = _build(self.contents)

    def __str__(self):
        return self._output