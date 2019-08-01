from typing import Optional
from dero.latex.models.item import SimpleItem


class Author(SimpleItem):
    name = 'author'

    def __init__(self, authors, short_author: Optional[str] = None):
        self.authors = authors
        self.short_author = short_author
        if short_author is not None:
            from dero.latex.logic.format.contents import format_contents
            short_author_str = f'[{format_contents(short_author)}]'
        else:
            short_author_str = None
        super().__init__(self.name, authors, modifiers=short_author_str)