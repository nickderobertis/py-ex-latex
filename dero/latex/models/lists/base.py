from typing import Optional
from dero.latex.models.item import Item
from dero.mixins.repr import ReprMixin
from dero.latex.models.lists.item import ListItem


class ListBase(Item, ReprMixin):
    name = 'list'
    repr_cols = ['contents']

    def __init__(self, items):
        self.items = items
        self.content = self.generate_content(items)
        super().__init__(self.name, self.content)

    @staticmethod
    def generate_content(items):
        from dero.latex.logic.builder import _build
        return _build([ListItem(item) for item in items])

