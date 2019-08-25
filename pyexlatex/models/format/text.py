from typing import Optional
from pyexlatex.models.item import SimpleItem


class Text(SimpleItem):
    """
    Gets back to raw text, useful to have normal text formatting inside of equations.
    """
    name = 'text'

    def __init__(self, env: str, modifiers: Optional[str] = None):
        self.env = env
        super().__init__(self.name, env, modifiers)
