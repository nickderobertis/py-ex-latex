from typing import Optional
from dero.latex.models.commands.begin import Begin
from dero.latex.models.commands.end import End

class Environment:

    def __init__(self, name, modifiers: Optional[str] = None):
        self.name = name

        self._begin = Begin(name, modifiers=modifiers)
        self._end = End(name)

    def __repr__(self):
        return f'<Environment(name={self.name})>'

    def wrap(self, other):
        from dero.latex.logic.builder import _build
        return _build([self._begin, other, self._end])
