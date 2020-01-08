from typing import Optional
from pyexlatex.models.sizes.textwidth import TextWidth
from pyexlatex.models.sizes.textheight import TextHeight
from pyexlatex.models.boxes.vbox import VBox
from pyexlatex.models.section.base import TextAreaBase


class Column(TextAreaBase):
    name = 'column'
    repr_cols = [
        'contents'
        'frac_of_text_width',
        'frac_of_page_height'
    ]

    def __init__(self, content, frac_of_text_width: float = 1.0, frac_of_page_height: Optional[float] = 0.8):
        self.frac_of_text_width = frac_of_text_width
        self.add_data_from_content(content)

        if frac_of_page_height is not None:
            contents = VBox(content, size_str=f' to {frac_of_page_height}{TextHeight()}')
        else:
            contents = content

        super().__init__(self.name, contents, env_modifiers=self.text_width_str)

    @property
    def text_width_str(self) -> str:
        return self._wrap_with_braces(f'{self.frac_of_text_width}{TextWidth()}')