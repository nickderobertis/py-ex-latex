from typing import Sequence, Optional

from pyexlatex.models.section.base import TextAreaBase


class BeamerColorBox(TextAreaBase):
    name = 'beamercolorbox'

    def __init__(self, content, color: str, options: Optional[Sequence[str]] = None, **kwargs):
        self.color = color
        self.options = options
        super().__init__(self.name, content, env_modifiers=self.modifier_str, **kwargs)

    @property
    def modifier_str(self) -> str:
        if self.options is None:
            return self._wrap_with_braces(self.color)
        options_str = ', '.join(self.options)
        return f'[{options_str}]{{{self.color}}}'
