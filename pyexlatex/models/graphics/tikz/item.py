from copy import deepcopy
from typing import Sequence, Optional
from dero.latex.models.item import ItemBase
from dero.latex.models.section.base import TextAreaMixin
from dero.latex.models.presentation.beamer.overlay.overlay import Overlay
from dero.latex.models.presentation.beamer.overlay.commands.uncover import Uncover


class TikZItem(TextAreaMixin, ItemBase):

    def __init__(self, name, contents, options: Optional[Sequence[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.contents = contents
        self.options = options
        self.overlay = overlay
        self.name = name
        super().__init__(name, contents)

    def __str__(self):
        item_str = f'\{self.name} {self.options_str} {self.contents};'
        if self.overlay:
            item_str = Uncover(item_str, overlay=self.overlay)
        return item_str

    @property
    def options_str(self) -> str:
        if self.options is None:
            return ''
        return self._wrap_with_bracket(', '.join(self.options))

    @staticmethod
    def _get_list_copy_from_list_or_none(list_or_none: Optional[list]):
        if list_or_none is None:
            return []
        return deepcopy(list_or_none)



