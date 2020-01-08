from pyexlatex.models.lists.base import ListBase


class UnorderedList(ListBase):
    """
    Bullet point items.
    """
    name = 'itemize'
    is_ListBase = True  # so that passing within lists will treat as a list

