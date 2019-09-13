from pyexlatex.models.lists.base import ListBase


class OrderedList(ListBase):
    """
    Numbered, ordered items.
    """
    name = 'enumerate'
    is_ListBase = True  # so that passing within lists will treat as a list

