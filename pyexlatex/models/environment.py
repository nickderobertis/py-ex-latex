from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
from pyexlatex.models.commands.begin import Begin
from pyexlatex.models.commands.end import End


class Environment:

    def __init__(self, name, modifiers: Optional[str] = None, overlay: Optional['Overlay'] = None):
        self.name = name

        if modifiers is None:
            modifiers = ''
        if overlay is not None:
            modifiers = str(overlay) + modifiers

        self._begin = Begin(name, modifiers=modifiers)
        self._end = End(name)

    def __repr__(self):
        return f'<Environment(name={self.name})>'

    def wrap(self, other):
        from pyexlatex.logic.builder import _build
        return _build([self._begin, other, self._end])
