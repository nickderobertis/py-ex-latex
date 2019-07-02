from typing import Optional
from dero.latex.models.item import SimpleItem


class Begin(SimpleItem):
    name = 'begin'

    def __init__(self, env: str, modifiers: Optional[str] = None):
        self.env = env
        super().__init__(self.name, env, modifiers)
