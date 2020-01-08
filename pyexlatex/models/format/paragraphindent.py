from typing import Sequence
from pyexlatex.models.section.base import TextAreaBase
from pyexlatex.models.item import Item


class ParagraphIndent(TextAreaBase, Item):
    """
    Used for setting paragraph indents, from the left or right.
    """
    name = 'adjustwidth'

    def __init__(self, contents, left_adjust: int = 1, right_adjust: int = 0):
        self.left_adjust = left_adjust
        self.right_adjust = right_adjust
        self.init_data()
        self.data.packages.append('changepage')
        super().__init__(self.name, contents, env_modifiers=self.options_str)

    @property
    def options_str(self) -> str:
        options_str = ''
        if self.left_adjust > 0:
            options_str += self._wrap_with_braces(f'{self.left_adjust}cm')
        else:
            options_str += '{}'
        if self.right_adjust > 0:
            options_str += self._wrap_with_braces(f'{self.right_adjust}cm')
        else:
            options_str += '{}'
        return options_str
