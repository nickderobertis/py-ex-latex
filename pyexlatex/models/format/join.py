from typing import Sequence
from pyexlatex.models.item import ItemBase
from pyexlatex.models.section.base import TextAreaMixin


class Joined(TextAreaMixin, ItemBase):
    """
    Applies string.join on contents when output string is created, but retains content objects.
    """

    def __init__(self, contents, join_with=''):

        if not isinstance(contents, (list, tuple)):
            contents = [contents]

        self.orig_contents = contents
        self.join_with = join_with
        super().__init__(None, contents)

    def __str__(self):
        return self.join_with.join([str(content) for content in self.orig_contents])
