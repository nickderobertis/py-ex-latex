from typing import Optional
import string
import random
from pyexlatex.models.item import MultiOptionSimpleItem


class ColorDefinition(MultiOptionSimpleItem):
    definition_type: Optional[str] = None
    name = 'definecolor'
    equal_attrs = [
        'color_content',
        'color_name'
    ]

    def __init__(self, color_content: str, color_name: Optional[str] = None):
        if color_name is None:
            color_name = random_color_name()
        self.color_name = color_name
        self.color_content = color_content
        self.init_data()
        self.data.packages.append('xcolor')
        super().__init__(self.name, self.color_name, self.definition_type, self.color_content)


def random_color_name(length: int = 20) -> str:
    out_str = ''
    for _ in range(length):
        out_str += random.choice(string.ascii_letters)
    return out_str
