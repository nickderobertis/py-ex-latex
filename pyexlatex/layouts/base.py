from typing import Any

from pyexlatex.models.item import ItemBase
from pyexlatex.models.section.base import TextAreaMixin


class LayoutBase(TextAreaMixin, ItemBase):
    content: Any = None  # should be overridden in the subclass

    def __init__(self, content, **kwargs):
        super().__init__(None, content, **kwargs)

    def __str__(self):
        from pyexlatex.logic.builder import _build
        if isinstance(self.content, str):
            return self.content
        elif isinstance(self.content, (list, tuple)):
            return _build(self.content)
        else:
            return str(self.content)
