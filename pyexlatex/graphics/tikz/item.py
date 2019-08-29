from typing import Sequence, Optional
from pyexlatex.models.item import ItemBase
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.presentation.beamer.overlay.commands.uncover import Uncover


class TikZItem(TextAreaMixin, ItemBase):

    def __init__(self, name, contents, options: Optional[Sequence[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.contents = contents
        self.options = options
        self.overlay = overlay
        self.name = name
        super().__init__(name, contents)

    def __str__(self):
        item_str = fr'\{self.name} {self.options_str} {self.contents};'
        if self.overlay:
            item_str = Uncover(item_str, overlay=self.overlay)
        return item_str

    @property
    def options_str(self) -> str:
        if self.options is None:
            return ''
        str_options = [str(option) for option in self.options]
        return self._wrap_with_bracket(', '.join(str_options))



