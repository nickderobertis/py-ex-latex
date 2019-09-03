from pyexlatex.models.sizes.textwidth import TextWidth
from pyexlatex.models.format.rule import Rule


class HLine(Rule):
    """
    Draws a horizontal line across the text width.
    """

    def __init__(self, thickness: float = 0.4):
        super().__init__(length=TextWidth(), thickness=thickness)
