from dero.latex.models.section.base import TextAreaBase
from dero.latex.models.format.textwidth import TextWidth


class Column(TextAreaBase):
    name = 'column'

    def __init__(self, content, frac_of_text_width: float = 1.0):
        self.frac_of_text_width = frac_of_text_width

        super().__init__(self.name, content, env_modifiers=self.text_width_str)

    @property
    def text_width_str(self) -> str:
        return self._wrap_with_braces(f'{self.frac_of_text_width}{TextWidth()}')