from typing import Optional
from dero.latex.models.item import NoBracesItem
from dero.mixins.repr import ReprMixin


class ListItem(NoBracesItem, ReprMixin):
    name = 'item'
    repr_cols = ['contents']

    def __init__(self, contents):
        super().__init__(self.name, contents)