from typing import Sequence, Optional
from pyexlatex.models.item import Item
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.graphics.tikz.item import TikzOptionHandler


class Scope(TextAreaMixin, Item, TikzOptionHandler):
    name = 'scope'

    def __init__(self, contents, options: Optional[Sequence[str]] = None):
        self.options = options
        super().__init__(self.name, contents, env_modifiers=self.options_str)

