from typing import Sequence, Optional, List
from pyexlatex.models.item import ItemBase
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.presentation.beamer.overlay.commands.uncover import Uncover


class TikzOptionHandler:
    options: Optional[Sequence[str]] = None

    @property
    def options_str(self) -> str:
        if self.options is None:
            return ''
        str_options = [str(option) for option in self.options]
        return self._wrap_with_bracket(', '.join(str_options))

    def _wrap_with_bracket(self, to_wrap: str):
        raise NotImplementedError('must also subclass ItemBase')


class TikZItem(TextAreaMixin, ItemBase, TikzOptionHandler):
    options: Optional[List[str]]

    def __init__(self, name, contents, options: Optional[List[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.contents = contents
        self.options = options
        self.overlay = overlay
        self.name = name
        super().__init__(name, contents)

    def __str__(self):
        overlay = self.overlay if self.overlay is not None else ""
        item_str = fr'\{self.name}{overlay} {self.options_str} {self.contents};'
        return item_str





