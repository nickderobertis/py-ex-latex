from typing import Sequence
from pyexlatex.models.item import MultiOptionSimpleItem


class SetBeamerColor(MultiOptionSimpleItem):
    name = 'setbeamercolor'

    def __init__(self, beamer_item: str, color_options: Sequence[str], **kwargs):
        color_options_str = ', '.join(color_options)
        super().__init__(self.name, beamer_item, color_options_str, **kwargs)
