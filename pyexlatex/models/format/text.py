from typing import Optional
from pyexlatex.models.item import SimpleItem


class Text(SimpleItem):
    name = 'text'

    def __init__(self, env: str, modifiers: Optional[str] = None):
        self.env = env
        super().__init__(self.name, env, modifiers)
