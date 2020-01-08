from typing import Sequence
from pyexlatex.models.lists.base import ListBase
from pyexlatex.models.control.setcounter import SetCounter


class OrderedList(ListBase):
    """
    Numbered, ordered items.
    """
    name = 'enumerate'
    is_ListBase = True  # so that passing within lists will treat as a list

    def __init__(self, items: Sequence, initial_number: int = 1, **kwargs):
        self.initial_number = initial_number

        if self.initial_number != 1:
            items = [SetCounter('enumi', self.initial_number - 1)] + list(items)

        super().__init__(items, **kwargs)

