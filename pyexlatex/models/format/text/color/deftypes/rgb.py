from typing import Optional
from pyexlatex.models.format.text.color.deftypes.base import ColorDefinition


class RGB(ColorDefinition):
    """
    Define a color using an RGB code, such as RGB(33, 173, 42)
    """
    definition_type = 'RGB'

    def __init__(self, red: int = 255, green: int = 255, blue: int = 255, color_name: Optional[str] = None):
        self.red = red
        self.green = green
        self.blue = blue
        color_content = ','.join([str(color) for color in [red, green, blue]])
        super().__init__(color_content=color_content, color_name=color_name)
