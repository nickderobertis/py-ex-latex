from typing import Sequence, Optional

from pyexlatex.models.item import NoOptionsNoContentsItem


class TableOfContents(NoOptionsNoContentsItem):
    name = 'tableofcontents'

    def __init__(self, options: Optional[Sequence[str]] = None, **kwargs):
        self.options = options
        super().__init__(self.name, modifiers=self.options_str, **kwargs)

    @property
    def options_str(self) -> Optional[str]:
        if self.options is None:
            return None
        options_str = ', '.join(self.options)
        return self._wrap_with_bracket(options_str)
