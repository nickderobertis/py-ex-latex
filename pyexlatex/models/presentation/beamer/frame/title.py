from typing import Optional
from pyexlatex.models.item import SimpleItem


class FrameTitle(SimpleItem):
    name = 'frametitle'

    def __init__(self, title: str, modifiers: Optional[str] = None):
        self.title = title
        super().__init__(self.name, title, modifiers)