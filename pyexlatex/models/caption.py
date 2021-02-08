from typing import Optional

from pyexlatex.models.item import SimpleItem
from pyexlatex.typing import PyexlatexItems


class Caption(SimpleItem):
    name = 'caption'

    def __init__(self, contents: PyexlatexItems, short_caption: Optional[str] = None):
        pre_modifiers: Optional[str] = None
        if short_caption is not None:
            pre_modifiers = self._wrap_with_bracket(short_caption)
        super().__init__(self.name, contents, pre_modifiers=pre_modifiers)


