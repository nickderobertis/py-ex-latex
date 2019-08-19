from typing import Optional
from pyexlatex.models.item import SimpleItem


class Title(SimpleItem):
    name = 'title'

    def __init__(self, main_title: str, short_title: Optional[str] = None):
        self.main_title = main_title
        self.short_title = short_title
        super().__init__(self.name, main_title, pre_modifiers=self._wrap_with_bracket(short_title))