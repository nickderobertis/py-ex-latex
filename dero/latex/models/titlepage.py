from dero.latex.models.documentitem import DocumentItem
from dero.latex.models.title import Title
from dero.latex.models.author import Author
from dero.latex.models.date import Date
from dero.latex.texgen import _maketitle_str

class TitlePage(DocumentItem):

    def __init__(self, title=None, author=None, date=None):
        from dero.latex.logic.builder import _build

        self.contents = [
            Title(title) if title is not None else None,
            Author(author) if author is not None else None,
            Date(date) if date is not None else Date(),
            _maketitle_str()
        ]

        self._output = _build(self.contents)

    def __str__(self):
        return self._output