from typing import Optional
from pyexlatex.models.format.text.color.deftypes.base import ColorDefinition


class Hex(ColorDefinition):
    """
    Define a color using a hex code, such as #21ad2a
    """
    definition_type = 'HTML'

    def __init__(self, hex_code: str, color_name: Optional[str] = None):
        self.hex_code = hex_code.strip('#')
        super().__init__(color_content=self.hex_code, color_name=color_name)
